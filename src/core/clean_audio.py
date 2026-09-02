import os
import subprocess
from autosubs_core import emit

def run(vid_path):
    emit(f"[*] Iniciando Limpieza de Voz (FFmpeg) para: {vid_path}")
    
    if not os.path.exists(vid_path):
        emit("[ERROR] No se encontró el archivo de audio/vídeo.")
        return
        
    out_path = os.path.splitext(vid_path)[0] + "_Limpio.wav"
    
    # FFmpeg tiene un filtro neuronal FFT integrado de denoise (afftdn) y ecualización de voz (highpass/lowpass)
    cmd = [
        "ffmpeg", "-y",
        "-i", vid_path,
        "-af", "highpass=f=200,lowpass=f=3000,afftdn=nf=-25",
        "-c:a", "pcm_s16le",
        out_path
    ]
    
    try:
        emit("[*] Procesando audio... (Aplicando filtros de ruido y aislamiento vocal)")
        subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        emit(f"[✔] Pista vocal limpia generada:\n-> {out_path}")
    except subprocess.CalledProcessError:
        emit("[ERROR] Ocurrió un error al limpiar el audio con FFmpeg.")
    except Exception as e:
        emit(f"[ERROR] {e}")
