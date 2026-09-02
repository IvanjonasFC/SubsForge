import os
import subprocess
from autosubs_core import emit

def run(vid_path, srt_path):
    emit(f"[*] Preparando incrustación permanente de subtítulos (Hardsub).")
    emit(f"[*] Vídeo: {vid_path}")
    emit(f"[*] Subtítulo: {srt_path}")
    
    if not os.path.exists(vid_path) or not os.path.exists(srt_path):
        emit("[ERROR] Faltan los archivos de origen.")
        return
        
    out_path = os.path.splitext(vid_path)[0] + "_HARDSUB.mp4"
    
    # FFmpeg requiere que la ruta del subtítulo escape los dos puntos y contrabarras en Windows
    # Ej: C:\video.srt -> C\:/video.srt o simplemente usar barras normales
    safe_srt = srt_path.replace('\\', '/').replace(':', '\\:')
    
    cmd = [
        "ffmpeg", "-y",
        "-i", vid_path,
        "-vf", f"subtitles={safe_srt}",
        "-c:v", "libx264",
        "-preset", "fast",
        "-c:a", "copy",
        out_path
    ]
    
    emit("[*] Iniciando FFmpeg... Esto puede tardar bastante dependiendo de la duración del vídeo.")
    try:
        # En una app de producción real, interceptaríamos stdout/stderr para mostrar el %
        subprocess.run(cmd, check=True)
        emit(f"[✔] Vídeo quemado con éxito:\n-> {out_path}")
    except subprocess.CalledProcessError:
        emit("[ERROR] El proceso de FFmpeg falló. Asegúrate de que FFmpeg está instalado y los formatos son correctos.")
    except Exception as e:
        emit(f"[ERROR] {e}")
