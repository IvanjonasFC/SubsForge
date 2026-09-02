import sys
import os
import pysubs2

def clean_ass(input_path):
    print(f"[*] Leyendo archivo original: {input_path}")
    try:
        subs = pysubs2.load(input_path)
        print(f"[*] Detectados {len(subs)} eventos de subtítulo.")
        print(f"[*] Limpiando estilos, efectos visuales y posiciones (Anime)...")
        
        output_path = os.path.splitext(input_path)[0] + "_LIMPIO.srt"
        subs.save(output_path, format="srt")
        
        print(f"[+] ¡Éxito! Archivo SRT de texto puro generado en:")
        print(f"[+] {output_path}")
    except Exception as e:
        print(f"[ERROR] No se pudo procesar el archivo ASS: {str(e)}")

if __name__ == '__main__':
    if len(sys.argv) > 1:
        clean_ass(sys.argv[1])
    else:
        print("Uso: python ass_cleaner.py <archivo.ass>")
