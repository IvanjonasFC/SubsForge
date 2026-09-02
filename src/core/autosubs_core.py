#!/usr/bin/env python3
"""
Sidecar de AutoSubs para el shell Tauri.

Es un despachador CLI: Rust lo ejecuta como binario externo (empaquetado con
PyInstaller) y reenvía su stdout, línea a línea, a la terminal de la interfaz.

Reutiliza la lógica existente de core/ (translator, whisper_gen, ass_cleaner)
y llama a ffsubsync / ffmpeg como binarios externos del PATH.

Uso:
    autosubs-core ollama
    autosubs-core translate <archivo.srt> <google|ollama:modelo> [idioma]
    autosubs-core sync      <video> <subtitulo>
    autosubs-core whisper   <archivo_o_carpeta>
    autosubs-core mux       <video> <subtitulo>
    autosubs-core dubbing   <archivo.srt>
    autosubs-core summary   <archivo.srt> <engine>
    autosubs-core hardsub   <video> <subtitulo>
    autosubs-core clean_audio <video>
"""
import sys
import os
import json
import subprocess

# Forzar UTF-8 en la salida: en Windows, stdout usa cp1252 (charmap) por defecto
# y revienta al imprimir subtítulos con coreano/chino/japonés/emojis
# ('charmap' codec can't encode character ...). errors='replace' es una red de
# seguridad extra. Se aplica al importar, antes de cualquier print.
for _stream in ("stdout", "stderr"):
    try:
        # line_buffering=True mantiene el progreso en vivo (una línea = un flush).
        getattr(sys, _stream).reconfigure(encoding="utf-8", errors="replace", line_buffering=True)
    except Exception:
        pass

# Este archivo vive en src/core/, junto a los módulos que envuelve.
HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path:
    sys.path.insert(0, HERE)


def emit(line=""):
    print(line, flush=True)


def detect_ollama():
    try:
        import requests
        r = requests.get("http://localhost:11434/api/tags", timeout=0.8)
        models = [m["name"] for m in r.json().get("models", [])]
    except Exception:
        models = []
    # Una sola línea JSON (Rust la parsea para get_ollama)
    print(json.dumps(models), flush=True)


def main():
    if len(sys.argv) < 2:
        emit("uso: autosubs-core <ollama|translate|sync|whisper|mux|cleaner> [args...]")
        return 1

    kind = sys.argv[1]
    a = sys.argv[2:]

    if kind == "ollama":
        detect_ollama()
        return 0

    try:
        if kind == "translate":
            import translator
            engine = a[1] if len(a) > 1 else "google"
            target = a[2] if len(a) > 2 else "es"
            translator.traducir_srt(a[0], engine, target)

        elif kind == "whisper":
            import whisper_gen
            whisper_gen.main(a[0])

        elif kind == "cleaner":
            import ass_cleaner
            ass_cleaner.clean_ass(a[0])

        elif kind == "sync":
            out = os.path.splitext(a[0])[0] + "_sincronizado.srt"
            emit(f"[*] Sincronizando con ffsubsync -> {out}")
            return subprocess.call(["ffsubsync", a[0], "-i", a[1], "-o", out])

        elif kind == "mux":
            out = os.path.splitext(a[0])[0] + "_FINAL.mkv"
            emit(f"[*] Integrando con ffmpeg -> {out}")
            return subprocess.call(["ffmpeg", "-y", "-i", a[0], "-i", a[1],
                                    "-c", "copy", "-c:s", "srt", out])
        elif kind == "dubbing":
            import dubbing
            rest = list(a)
            voice = None
            if "--voice" in rest:
                vi = rest.index("--voice")
                voice = rest[vi + 1] if vi + 1 < len(rest) else None
                del rest[vi:vi + 2]
            vid = rest[1] if len(rest) > 1 and rest[1] else None
            dubbing.run(rest[0], vid, voice)

        elif kind == "summary":
            import summarizer
            engine = a[1] if len(a) > 1 else "google"
            summarizer.run(a[0], engine)

        elif kind == "hardsub":
            import hardsub
            hardsub.run(a[0], a[1])

        elif kind == "clean_audio":
            import clean_audio
            clean_audio.run(a[0])

        else:
            emit(f"[ERROR] Tarea desconocida: {kind}")
            return 1

    except IndexError:
        emit("[ERROR] Faltan argumentos para la tarea.")
        return 1
    except FileNotFoundError as e:
        emit(f"[ERROR] No se encontró el ejecutable/archivo: {e}")
        return 1
    except Exception as e:
        emit(f"[ERROR] {e}")
        return 1

    return 0


if __name__ == "__main__":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace", line_buffering=True)
    except Exception:
        pass
    sys.exit(main())
