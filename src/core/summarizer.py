import os
import json
import requests
from autosubs_core import emit

def run(srt_path, engine):
    emit(f"[*] Analizando subtítulo para resumen: {srt_path}")
    emit(f"[*] Motor seleccionado: {engine}")
    
    if not os.path.exists(srt_path):
        emit(f"[ERROR] No se encontró el subtítulo: {srt_path}")
        return
        
    try:
        with open(srt_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            
        # Extraer solo el texto (heurística simple para evitar los tiempos)
        text_lines = [l.strip() for l in lines if not l.strip().isdigit() and '-->' not in l and l.strip()]
        full_text = " ".join(text_lines)
        
        # Recortar si es exageradamente largo para no petar la memoria de la IA de golpe
        if len(full_text) > 20000:
            full_text = full_text[:20000] + "... (recortado)"
            
        emit("[*] Guion extraído. Solicitando resumen y capítulos a la IA...")
        
        prompt = (
            "Lee el siguiente guion de un vídeo y haz dos cosas en español:\n"
            "1. Escribe un resumen atractivo sin spoilers.\n"
            "2. Inventa 4 o 5 capítulos lógicos con formato de marca de tiempo (ej. 00:00 - Introducción).\n\n"
            f"Guion:\n{full_text}"
        )
        
        out_path = os.path.splitext(srt_path)[0] + "_resumen.txt"
        
        if engine.startswith("ollama:"):
            model = engine.split(":")[1]
            payload = {
                "model": model,
                "prompt": prompt,
                "stream": False
            }
            resp = requests.post("http://localhost:11434/api/generate", json=payload, timeout=300)
            resp.raise_for_status()
            result = resp.json().get("response", "")
        else:
            # Fallback a un mock si eligen google o no tienen ollama configurado
            emit("[!] Advertencia: Google Translate no soporta resúmenes. Usa Ollama. (Mostrando demo...)")
            result = "Resumen generado con IA.\n\nCapítulos:\n00:00 - Inicio\n10:00 - Nudo\n20:00 - Desenlace"
            
        with open(out_path, 'w', encoding='utf-8') as f:
            f.write(result)
            
        emit(f"[✔] Resumen y Capítulos generados con éxito:\n-> {out_path}")
        
    except Exception as e:
        emit(f"[ERROR] Fallo al generar el resumen: {e}")
