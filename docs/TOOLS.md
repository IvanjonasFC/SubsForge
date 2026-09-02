# Tools

SubsForge exposes nine tools. Each takes one or two files, prints its progress to
the terminal, and writes its result **next to the source file** (same directory,
with a suffix). None overwrites the original.

The reference module is shown in parentheses; they all live in `src/core/`.

## 1. AI translator (`translator.py`)

Translates an `.srt` into Spanish (or another language). Two engines:

- **Google** (`deep_translator.GoogleTranslator`): in batches of 40 lines, with
  protected `<hr>`/`<br>` separators, retries (up to 3), and a line-by-line
  rescue mode if a batch goes out of sync. Includes courtesy pauses to avoid
  temporary bans.
- **Ollama** (`ollama:<model>`): line by line, with a professional-translator
  prompt that preserves HTML tags like `<i>`. Fully local.

Input: `.srt`, engine, optional language (`es` by default; maps to Spanish,
English, French, German, Italian, Portuguese). Output: `<name>_<LANG>.srt`.

## 2. VAD sync (`autosubs_core.py` -> `ffsubsync`)

Realigns an out-of-sync subtitle using voice-activity detection over the video
audio. Input: video + subtitle. Output: `<subtitle>_synced.srt`. Requires
`ffsubsync` on the `PATH`.

## 3. Whisper transcription (`whisper_gen.py`)

Transcribes with `faster-whisper` (`small` model, CPU, `int8`). It uses
`task="translate"`, so it **produces English subtitles** and then translates them
to Spanish with the Google engine (chaining `translator.py`). Accepts a file or a
whole folder (batch mode: `.mkv`, `.mp4`, `.avi`). Output: `<video>_Whisper_EN.srt`
and its translation. The model is downloaded on first use.

## 4. Lossless merge (`autosubs_core.py` -> `ffmpeg`)

Remuxes the subtitle into an `.mkv` container without re-encoding (`-c copy`), in
seconds. Input: `.mkv` video + `.srt` subtitle. Output: `<video>_FINAL.mkv`.

## 5. Anime cleaner (`ass_cleaner.py`)

Converts complex `.ass` files (styles, effects, positioning typical of fansubs)
into plain-text `.srt` compatible with TVs and players, via `pysubs2`. Input:
`.ass`. Output: `<name>_CLEAN.srt`.

## 6. Automatic dubbing — TTS (`dubbing.py`)

Generates a voice track with `edge-tts` (Microsoft; free, no key) and, if a video
is provided, creates an `.mkv` with **dual audio** (original + dub) by mapping the
tracks with FFmpeg. Input: `.srt` (+ optional video). Outputs: `<srt>_dub.wav`
and, with a video, `<video>_DUBBED.mkv`. Requires `edge-tts`
(`pip install edge-tts`).

**Voice selector.** The tab includes a "Dubbing voice" dropdown with real
edge-tts voices grouped by language (several Spanish variants — Spain, Mexico,
Argentina, Colombia, US — plus English, French, German, Italian, Portuguese,
Japanese, Korean and Chinese). Default: `es-ES-AlvaroNeural`. The voice travels to
the sidecar as a `--voice <id>` flag, so the optional video can be empty without
misaligning the arguments. To add more voices, extend the `VOICES` list in
`index.html` with any valid ID from `edge-tts --list-voices`.

> **Sync.** It reads the real dialogue from the `.srt`, synthesizes each line and
> places it at its timestamp by inserting silences between segments, so the dub
> stays aligned with the subtitle. If a TTS clip is longer than its slot it is
> chained without cutting (which can accumulate slight drift in very dense
> dialogue; it re-aligns at each pause). Requires `ffprobe` (ships with FFmpeg).

## 7. Summary and chapters (`summarizer.py`)

Extracts the text from the `.srt` (a heuristic that drops indices and timings),
trims it to ~20,000 characters, and asks the AI for a spoiler-free summary plus
4–5 timestamped chapters. Input: `.srt` + engine. Output: `<srt>_summary.txt`.

> A real summary requires **Ollama** (`ollama:<model>`, via
> `http://localhost:11434/api/generate`). With the Google engine a demo result is
> shown, because Google Translate does not summarize.

## 8. Hardsub — burned-in subtitles (`hardsub.py`)

Burns the subtitles permanently into the video with FFmpeg's `subtitles` filter,
re-encoding the video (`libx264`, `preset fast`) and copying the audio. It
correctly escapes the `.srt` path for Windows. Input: video + subtitle. Output:
`<video>_HARDSUB.mp4`. This is the slowest operation (depends on video length).

## 9. Voice cleanup (`clean_audio.py`)

Isolates and cleans the voice with the FFmpeg filter chain
`highpass=f=200, lowpass=f=3000, afftdn=nf=-25` (high/low pass for the vocal band
+ FFT noise reduction). Input: video or audio. Output: `<name>_Clean.wav`
(16-bit PCM).

---

## Summary table

| Tool | `kind` | Input | Output | Engine / dependency |
| --- | --- | --- | --- | --- |
| AI translator | `translate` | `.srt` | `_<LANG>.srt` | deep-translator / Ollama |
| VAD sync | `sync` | video + sub | `_synced.srt` | ffsubsync |
| Whisper transcription | `whisper` | video/folder | `_Whisper_EN.srt` (+trans.) | faster-whisper |
| Lossless merge | `mux` | `.mkv` + `.srt` | `_FINAL.mkv` | FFmpeg |
| Anime cleaner | `cleaner` | `.ass` | `_CLEAN.srt` | pysubs2 |
| TTS dubbing | `dubbing` | `.srt` (+video) | `_dub.wav` / `_DUBBED.mkv` | edge-tts + FFmpeg (voice selector) |
| Summary and chapters | `summary` | `.srt` | `_summary.txt` | Ollama |
| Hardsub | `hardsub` | video + `.srt` | `_HARDSUB.mp4` | FFmpeg (libx264) |
| Voice cleanup | `clean_audio` | video/audio | `_Clean.wav` | FFmpeg (afftdn) |
