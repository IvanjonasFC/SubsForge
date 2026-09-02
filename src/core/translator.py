import sys
import os
import pysrt
import time
import requests
from deep_translator import GoogleTranslator

# UTF-8 en la salida (Windows usa cp1252 por defecto y revienta al imprimir
# subtítulos con coreano/chino/japonés). Se aplica también cuando whisper_gen
# lanza este script como subproceso aparte.
for _s in ("stdout", "stderr"):
    try:
        # line_buffering=True: imprime cada línea al instante (progreso en vivo).
        getattr(sys, _s).reconfigure(encoding="utf-8", errors="replace", line_buffering=True)
    except Exception:
        pass

def translate_ollama(text, model="llama3", target_lang_name="Spanish (Spain)"):
    prompt = f"Act as a professional movie subtitle translator. Translate the following subtitle block to {target_lang_name}. Keep the translation natural and contextual. ONLY output the translated text. Do not add notes, quotes, or conversational text. Preserve any HTML tags like <i> exactly as they are:\n\n{text}"
    url = "http://localhost:11434/api/generate"
    payload = {
        "model": model,
        "prompt": prompt,
        "stream": False
    }
    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        return response.json().get("response", "").strip()
    except Exception as e:
        print(f"[ERROR OLLAMA] {str(e)}")
        return text

def traducir_srt(input_file, engine="google", target_lang="es"):
    if not input_file.lower().endswith(('.srt', '.ass', '.vtt')):
        print(f'[ERROR] El traductor solo soporta subtítulos (.srt, .ass, .vtt). Archivo ignorado: {input_file}')
        return
    print(f"[+] Cargando archivo: {input_file}")
    subs = pysrt.open(input_file, encoding='utf-8')
    print(f"[+] Se han encontrado {len(subs)} líneas para traducir.")
    print(f"[*] Motor de IA activo: {engine.upper()}")
    print(f"[*] Idioma de destino: {target_lang.upper()}")
    
    LANG_MAP = {
        "es": "Spanish",
        "en": "English",
        "fr": "French",
        "de": "German",
        "it": "Italian",
        "pt": "Portuguese"
    }
    target_lang_name = LANG_MAP.get(target_lang, "Spanish")
    
    if engine == "google":
        translator = GoogleTranslator(source='auto', target=target_lang)
    else:
        ollama_model = engine.split(":", 1)[1] if ":" in engine else "llama3"

    batch_size = 40
    chunks = [subs[i:i + batch_size] for i in range(0, len(subs), batch_size)]

    import re
    from concurrent.futures import ThreadPoolExecutor

    def _translate_line(text):
        """Traduce UNA linea con reintentos. Cada llamada usa su propia instancia
        (thread-safe). Si todo falla, devuelve el original para no perder la linea."""
        if not text or not text.strip():
            return text
        tr = GoogleTranslator(source='auto', target=target_lang)
        for _ in range(3):
            try:
                t = tr.translate(text)
                if t and "Error 500" not in t and "That's an error" not in t:
                    return t
            except Exception:
                pass
            time.sleep(1.2)
        return text

    def _rescue_parallel(chunk):
        """Traduce un lote linea a linea EN PARALELO: rapido y sin descuadres."""
        with ThreadPoolExecutor(max_workers=6) as ex:
            results = list(ex.map(lambda sub: _translate_line(sub.text), chunk))
        for sub, t in zip(chunk, results):
            sub.text = t

    batching_ok = True      # el modo lote rapido sirve para este subtitulo
    consecutive_fail = 0    # lotes rapidos fallidos seguidos
    
    for c_idx, chunk in enumerate(chunks):
        print(f"[*] Procesando lote {c_idx+1} de {len(chunks)} ({len(chunk)} líneas)...")
        
        if engine == "google":
            used_fast = False
            # Modo rapido: 1 sola peticion por lote usando <hr> como separador.
            # Solo se usa mientras funcione; con algunos idiomas (p. ej. chino)
            # Google se come el separador y descuadra, asi que se abandona pronto
            # y se pasa a traduccion directa en paralelo (fiable y rapida).
            if batching_ok:
                joined_text = ' <hr> '.join(sub.text.replace('\n', ' <br> ') for sub in chunk)
                try:
                    translated = translator.translate(joined_text)
                    if translated and "Error 500" not in translated and "That's an error" not in translated:
                        parts = re.split(r'\s*<\s*hr\s*>\s*', translated, flags=re.IGNORECASE)
                        if len(parts) == len(chunk):
                            for j, sub in enumerate(chunk):
                                sub.text = parts[j].replace(' <br> ', '\n').replace('<br>', '\n')
                            used_fast = True
                            consecutive_fail = 0
                            time.sleep(0.5)
                except Exception:
                    pass
                if not used_fast:
                    consecutive_fail += 1
                    if consecutive_fail >= 2:
                        batching_ok = False
                        print("  [i] El modo rapido no encaja con este subtitulo; cambio a traduccion directa en paralelo (mas fiable).")
            if not used_fast:
                print("  [*] Traduciendo linea a linea en paralelo (6 a la vez)...")
                _rescue_parallel(chunk)
        else:
            # Ollama (siempre línea por línea para evitar alucinaciones y límite de contexto)
            for sub in chunk:
                for att in range(3):
                    try:
                        sub.text = translate_ollama(sub.text, model=ollama_model, target_lang_name=target_lang_name)
                        break
                    except Exception:
                        time.sleep(2)
            
    output_file = os.path.splitext(input_file)[0] + f"_{target_lang.upper()}.srt"
    subs.save(output_file, encoding='utf-8')
    print(f"\n[+] ¡Éxito! Subtítulo traducido guardado como:\n[+] {output_file}")

if __name__ == '__main__':
    if len(sys.argv) > 1:
        engine = sys.argv[2] if len(sys.argv) > 2 else "google"
        target = sys.argv[3] if len(sys.argv) > 3 else "es"
        traducir_srt(sys.argv[1], engine, target)
    else:
        print("Uso: python translator.py <archivo.srt> [google|ollama:modelo] [codigo_idioma]")

