"""
Doblaje automático (TTS) para SubsForge.

Lee el diálogo real del .srt, sintetiza cada línea con edge-tts (voz en español)
y arma una única pista de audio colocando cada clip en su marca de tiempo, de
modo que el doblaje queda sincronizado con el subtítulo. Si se aporta un vídeo,
genera un .mkv con audio dual (original + doblaje).

Dependencias: edge-tts (pip install edge-tts), pysrt y FFmpeg/ffprobe en el PATH.
"""
import os
import sys
import asyncio
import subprocess
import tempfile
import shutil

import pysrt
from autosubs_core import emit

VOICE = "es-ES-AlvaroNeural"   # voz de doblaje por defecto
SR = 24000                     # frecuencia de muestreo común para todos los tramos
FFMPEG_QUIET = {"stdout": subprocess.DEVNULL, "stderr": subprocess.DEVNULL}


def _duration(path):
    """Duración en segundos de un archivo de audio, vía ffprobe."""
    try:
        out = subprocess.run(
            ["ffprobe", "-v", "error", "-show_entries", "format=duration",
             "-of", "default=nokey=1:noprint_wrappers=1", path],
            capture_output=True, text=True)
        return float(out.stdout.strip())
    except Exception:
        return 0.0


async def _synth(text, path, voice):
    import edge_tts
    await edge_tts.Communicate(text, voice).save(path)


def run(srt_path, vid_path=None, voice=None):
    voice = voice or VOICE
    emit(f"[*] Iniciando Doblaje Automático (TTS) para: {srt_path}")
    emit(f"[*] Voz seleccionada: {voice}")

    if not os.path.exists(srt_path):
        emit("[ERROR] No se encontró el subtítulo.")
        return

    try:
        import edge_tts  # noqa: F401
    except ImportError:
        emit("[ERROR] La librería 'edge-tts' no está instalada. Ejecuta: pip install edge-tts")
        return

    try:
        subs = pysrt.open(srt_path, encoding="utf-8")
    except Exception as e:
        emit(f"[ERROR] No se pudo leer el subtítulo: {e}")
        return

    emit(f"[*] {len(subs)} líneas de diálogo detectadas. Cargando motor TTS (Edge-TTS)…")

    tmp = tempfile.mkdtemp(prefix="subsforge_dub_")
    list_path = os.path.join(tmp, "concat.txt")
    cursor = 0.0        # posición actual en la línea de tiempo (s)
    spoken = 0          # líneas realmente sintetizadas

    try:
        with open(list_path, "w", encoding="utf-8") as lst:
            for i, sub in enumerate(subs):
                text = (sub.text_without_tags or "").replace("\n", " ").strip()
                if not text:
                    continue

                start = sub.start.ordinal / 1000.0
                gap = start - cursor
                # Silencio para alinear el inicio del clip con su marca de tiempo.
                # Si el clip anterior se solapó (gap<=0), encadenamos sin hueco.
                if gap > 0.02:
                    sil = os.path.join(tmp, f"sil_{i}.wav")
                    subprocess.run(
                        ["ffmpeg", "-y", "-f", "lavfi",
                         "-i", f"anullsrc=r={SR}:cl=mono", "-t", f"{gap:.3f}", sil],
                        check=True, **FFMPEG_QUIET)
                    lst.write(f"file '{sil}'\n")
                    cursor += gap

                raw = os.path.join(tmp, f"clip_{i}.mp3")
                asyncio.run(_synth(text, raw, voice))
                wav = os.path.join(tmp, f"clip_{i}.wav")
                subprocess.run(
                    ["ffmpeg", "-y", "-i", raw, "-ar", str(SR), "-ac", "1", wav],
                    check=True, **FFMPEG_QUIET)

                lst.write(f"file '{wav}'\n")
                cursor += _duration(wav)
                spoken += 1
                if spoken % 20 == 0:
                    emit(f"[*] Sintetizadas {spoken}/{len(subs)} líneas…")

        if spoken == 0:
            emit("[ERROR] El subtítulo no contenía diálogo utilizable.")
            return

        out_audio = os.path.splitext(srt_path)[0] + "_doblaje.wav"
        emit("[*] Uniendo los tramos en una sola pista sincronizada…")
        subprocess.run(
            ["ffmpeg", "-y", "-f", "concat", "-safe", "0",
             "-i", list_path, "-c", "copy", out_audio],
            check=True, **FFMPEG_QUIET)
        emit(f"[✔] Pista de doblaje generada y sincronizada ({spoken} líneas):\n-> {out_audio}")

        if vid_path and os.path.exists(vid_path):
            emit("[*] Vídeo detectado. Generando archivo con audio dual (original + doblaje)…")
            out_video = os.path.splitext(vid_path)[0] + "_DOBLADO.mkv"
            subprocess.run(
                ["ffmpeg", "-y",
                 "-i", vid_path,
                 "-i", out_audio,
                 "-map", "0:v:0",
                 "-map", "0:a:0?",
                 "-map", "1:a:0",
                 "-c:v", "copy",
                 "-c:a:0", "copy",
                 "-c:a:1", "aac",
                 "-metadata:s:a:0", "title=Original",
                 "-metadata:s:a:1", "title=Doblaje",
                 out_video],
                check=True, **FFMPEG_QUIET)
            emit(f"[❭] ¡Película lista! Audio original + doblaje en español:\n-> {out_video}")

    except subprocess.CalledProcessError as e:
        emit(f"[ERROR] Falló FFmpeg durante el doblaje: {e}")
    except Exception as e:
        emit(f"[ERROR] Falló la síntesis o integración: {e}")
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        run(sys.argv[1],
            sys.argv[2] if len(sys.argv) > 2 else None,
            sys.argv[3] if len(sys.argv) > 3 else None)
    else:
        print("Uso: python dubbing.py <archivo.srt> [video] [voz]")
