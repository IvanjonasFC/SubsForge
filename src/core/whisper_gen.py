import sys
import os
import glob
from faster_whisper import WhisperModel
import pysrt
import time
import subprocess

# UTF-8 en la salida (Windows usa cp1252 por defecto y revienta al imprimir
# texto con caracteres no occidentales: coreano, chino, japonés, emojis...).
for _s in ("stdout", "stderr"):
    try:
        getattr(sys, _s).reconfigure(encoding="utf-8", errors="replace", line_buffering=True)
    except Exception:
        pass

def process_file(model, video_path):
    print(f"\n==========================================")
    print(f"[*] Procesando: {os.path.basename(video_path)}")
    print(f"==========================================")

    # Optimización de velocidad:
    #  - beam_size=1 (greedy): 2-3x más rápido que beam_size=5, calidad casi igual.
    #  - vad_filter: detecta y salta los silencios, gran aceleración en diálogo real.
    segments, info = model.transcribe(
        video_path,
        beam_size=1,
        task="translate",
        vad_filter=True,
        vad_parameters=dict(min_silence_duration_ms=500),
        condition_on_previous_text=False,
    )

    subs = pysrt.SubRipFile()
    for i, segment in enumerate(segments):
        sub = pysrt.SubRipItem(
            i+1, 
            start=pysrt.SubRipTime(seconds=segment.start), 
            end=pysrt.SubRipTime(seconds=segment.end), 
            text=segment.text.strip()
        )
        subs.append(sub)
        print(f"[{time.strftime('%H:%M:%S', time.gmtime(segment.start))}] {segment.text.strip()}")
        
    output_srt = os.path.splitext(video_path)[0] + "_Whisper_EN.srt"
    subs.save(output_srt, encoding='utf-8')
    print(f"[+] Subtítulo generado: {output_srt}")
    
    traductor_script = os.path.join(os.path.dirname(os.path.abspath(__file__)), "translator.py")
    env = os.environ.copy()
    env["PYTHONIOENCODING"] = "utf-8"   # el subproceso del traductor también en UTF-8
    env["PYTHONUTF8"] = "1"
    subprocess.run([sys.executable, traductor_script, output_srt, "google"], env=env)

def main(input_path):
    print(f"\n[+] Cargando modelo de IA (Faster-Whisper)...")
    # Usar todos los núcleos de la CPU acelera la transcripción notablemente.
    model = WhisperModel("small", device="cpu", compute_type="int8",
                         cpu_threads=os.cpu_count() or 4)
    
    if os.path.isdir(input_path):
        print(f"[*] Modo Maratón (Lotes) Detectado.")
        extensions = ('*.mkv', '*.mp4', '*.avi')
        videos = []
        for ext in extensions:
            videos.extend(glob.glob(os.path.join(input_path, ext)))
            
        print(f"[*] Se encontraron {len(videos)} vídeos en la carpeta.")
        for vid in videos:
            process_file(model, vid)
    else:
        process_file(model, input_path)

if __name__ == '__main__':
    if len(sys.argv) > 1:
        main(sys.argv[1])
    else:
        print("Uso: python whisper_gen.py <archivo_o_directorio>")
