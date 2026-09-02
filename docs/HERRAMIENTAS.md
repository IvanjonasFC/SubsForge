# Herramientas

SubsForge expone nueve herramientas. Cada una recibe uno o dos archivos, imprime
su progreso en la terminal y escribe su resultado **junto al archivo de origen**
(mismo directorio, con un sufijo). Ninguna sobrescribe el original.

Módulo de referencia entre paréntesis; todos viven en `src/core/`.

## 1. Traductor IA (`translator.py`)

Traduce un `.srt` a español (u otro idioma). Dos motores:

- **Google** (`deep_translator.GoogleTranslator`): por lotes de 40 líneas, con
  separadores `<hr>`/`<br>` protegidos, reintentos (hasta 3) y un modo de rescate
  línea a línea si un lote descuadra. Incluye pausas de cortesía para evitar
  baneos temporales.
- **Ollama** (`ollama:<modelo>`): línea a línea, con un *prompt* de traductor
  profesional que preserva etiquetas HTML como `<i>`. 100 % local.

Entrada: `.srt`, motor, idioma opcional (`es` por defecto; mapa a Spanish,
English, French, German, Italian, Portuguese). Salida: `<nombre>_<IDIOMA>.srt`.

## 2. Sincronización VAD (`autosubs_core.py` → `ffsubsync`)

Alinea un subtítulo desfasado usando detección de actividad de voz sobre el
audio del vídeo. Entrada: vídeo + subtítulo. Salida:
`<subtitulo>_sincronizado.srt`. Requiere `ffsubsync` en el PATH.

## 3. Transcripción Whisper (`whisper_gen.py`)

Transcribe con `faster-whisper` (modelo `small`, CPU, `int8`). Usa
`task="translate"`, de modo que **genera subtítulos en inglés** y a continuación
los traduce a español con el motor Google (encadena `translator.py`). Acepta un
archivo o una carpeta entera (modo lote: `.mkv`, `.mp4`, `.avi`). Salida:
`<video>_Whisper_EN.srt` y su traducción. El modelo se descarga en el primer uso.

## 4. Fusión Lossless (`autosubs_core.py` → `ffmpeg`)

Remuxea el subtítulo dentro de un contenedor `.mkv` sin recodificar (`-c copy`),
en segundos. Entrada: vídeo `.mkv` + subtítulo `.srt`. Salida:
`<video>_FINAL.mkv`.

## 5. Limpiador Anime (`ass_cleaner.py`)

Convierte `.ass` complejos (estilos, efectos, posiciones típicos de fansubs) en
`.srt` de texto plano compatible con televisores y reproductores, vía
`pysubs2`. Entrada: `.ass`. Salida: `<nombre>_LIMPIO.srt`.

## 6. Doblaje automático — TTS (`dubbing.py`)

Genera una pista de voz con `edge-tts` (Microsoft; gratis y sin clave) y, si se
aporta un vídeo, crea un `.mkv` con **audio dual** (original + doblaje) mapeando
las pistas con FFmpeg. Entrada: `.srt` (+ vídeo opcional). Salidas:
`<srt>_doblaje.wav` y, con vídeo, `<video>_DOBLADO.mkv`. Requiere `edge-tts`
(`pip install edge-tts`).

**Selector de voz.** La pestaña incluye un desplegable "Voz de doblaje" con voces
reales de edge-tts agrupadas por idioma (varias de español —España, México,
Argentina, Colombia, EE. UU.— más inglés, francés, alemán, italiano, portugués,
japonés, coreano y chino). Por defecto `es-ES-AlvaroNeural`. La voz viaja al
sidecar como flag `--voice <id>`, así que el vídeo opcional puede ir vacío sin
descuadrar los argumentos. Para añadir más voces basta con ampliar la lista
`VOICES` en `index.html` con cualquier ID válido de `edge-tts --list-voices`.

> **Sincronización.** Lee el diálogo real del `.srt`, sintetiza cada línea y la
> coloca en su marca de tiempo insertando silencios entre tramos, de modo que el
> doblaje queda alineado con el subtítulo. Si un clip TTS dura más que su hueco,
> se encadena sin cortarlo (puede acumular una ligera deriva en diálogos muy
> densos; se re-alinea en cada pausa). Requiere `ffprobe` (viene con FFmpeg).

## 7. Resumen y capítulos (`summarizer.py`)

Extrae el texto del `.srt` (heurística que descarta índices y tiempos), lo
recorta a ~20 000 caracteres y pide a la IA un resumen sin spoilers más 4–5
capítulos con marcas de tiempo. Entrada: `.srt` + motor. Salida:
`<srt>_resumen.txt`.

> El resumen real requiere **Ollama** (`ollama:<modelo>`, vía
> `http://localhost:11434/api/generate`). Con el motor Google se muestra un
> resultado de demostración, porque Google Translate no resume.

## 8. Subtítulos incrustados — Hardsub (`hardsub.py`)

Quema los subtítulos de forma permanente en el vídeo con el filtro `subtitles`
de FFmpeg, recodificando vídeo (`libx264`, `preset fast`) y copiando el audio.
Escapa correctamente la ruta del `.srt` para Windows. Entrada: vídeo +
subtítulo. Salida: `<video>_HARDSUB.mp4`. Es la operación más lenta (depende de
la duración del vídeo).

## 9. Limpieza de voz (`clean_audio.py`)

Aísla y limpia la voz con la cadena de filtros de FFmpeg
`highpass=f=200, lowpass=f=3000, afftdn=nf=-25` (paso alto/bajo para la banda
vocal + reducción de ruido FFT). Entrada: vídeo o audio. Salida:
`<nombre>_Limpio.wav` (PCM 16 bits).

---

## Tabla resumen

| Herramienta | `kind` | Entrada | Salida | Motor / dependencia |
| --- | --- | --- | --- | --- |
| Traductor IA | `translate` | `.srt` | `_<IDIOMA>.srt` | deep-translator / Ollama |
| Sincronización VAD | `sync` | vídeo + sub | `_sincronizado.srt` | ffsubsync |
| Transcripción Whisper | `whisper` | vídeo/carpeta | `_Whisper_EN.srt` (+trad.) | faster-whisper |
| Fusión Lossless | `mux` | `.mkv` + `.srt` | `_FINAL.mkv` | FFmpeg |
| Limpiador Anime | `cleaner` | `.ass` | `_LIMPIO.srt` | pysubs2 |
| Doblaje TTS | `dubbing` | `.srt` (+vídeo) | `_doblaje.wav` / `_DOBLADO.mkv` | edge-tts + FFmpeg (selector de voz) |
| Resumen y capítulos | `summary` | `.srt` | `_resumen.txt` | Ollama |
| Hardsub | `hardsub` | vídeo + `.srt` | `_HARDSUB.mp4` | FFmpeg (libx264) |
| Limpieza de voz | `clean_audio` | vídeo/audio | `_Limpio.wav` | FFmpeg (afftdn) |
