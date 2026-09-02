# SubsForge — web interface (PyWebView)

A professional desktop interface for SubsForge, built with **PyWebView**: your
Python backend (the scripts in `../core/`) stays the same, and the UI is drawn
with HTML/CSS/JS, reusing the design system of
[ivanjonasfc.dev](https://ivanjonasfc.dev) (real glass blur, grid, a mouse-tracking
glow, translucent cards and a live terminal).

On Windows it renders with **WebView2** (the Edge/Chromium engine already included
in Windows 10/11), so the look matches the portfolio and resource use is minimal
(~8 MB, ~50 MB of RAM).

## Requirements

```bash
pip install pywebview requests
```

(The WebView2 Runtime ships with Windows 10/11. If it is missing:
https://developer.microsoft.com/microsoft-edge/webview2/)

## Run

```bash
python src/webui/app.py
```

Or point your launcher `.bat` at that file.

## Structure

- `index.html` — the whole interface (HTML + CSS + JS in a single file).
- `app.py` — the PyWebView shell: a frameless window, file dialogs, and task
  execution that streams output to the live terminal.

## Notes

- The fonts (Space Grotesk / Inter / JetBrains Mono) load from Google Fonts. For
  fully offline use you can self-host them: the `.ttf` files are already in
  `../assets/fonts/` — swap them for local `@font-face` rules in `index.html`.
- The subtitle logic is unchanged: it still calls `core/translator.py`,
  `core/whisper_gen.py`, `core/ass_cleaner.py`, `ffsubsync` and `ffmpeg`.
