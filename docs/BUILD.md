# Build and deployment

This guide covers the production path: build the Python sidecar, package the app
with Tauri, regenerate the icon and produce the installer. It also includes the
simpler PyWebView mode for development.

## Prerequisites

| Component | Use | Notes |
| --- | --- | --- |
| Python 3.8+ | core and sidecar | on the `PATH` |
| FFmpeg | merge, hardsub, dubbing, cleanup | binary on the `PATH` |
| ffsubsync | VAD sync | `pip install ffsubsync` |
| Rust + Cargo | build Tauri | production build only |
| Node.js | Tauri CLI (`@tauri-apps/cli`) | production build only |
| WebView2 | interface engine on Windows | included in Windows 10/11 |
| Ollama (optional) | local translation and summary | https://ollama.com |

Python dependencies: `pip install -r requirements.txt`
(pywebview, requests, faster-whisper, ffsubsync, deep-translator, pysrt,
pysubs2, edge-tts).

## A. Development mode (PyWebView)

No build. On Windows:

```bat
SubsForge.bat            :: launches the interface with no console
SubsForge-Debug.bat      :: launches with a console to see errors
```

On any platform: `python src/webui/app.py`.

## B. Production build (Tauri)

### B.1 Build the sidecar with PyInstaller

From `src/core/`:

```bash
pip install pyinstaller edge-tts
pyinstaller --onefile --console --name autosubs-core autosubs_core.py \
  --collect-all faster_whisper --collect-all ctranslate2 --collect-all pysubs2 \
  --collect-all edge_tts \
  --hidden-import translator --hidden-import whisper_gen --hidden-import ass_cleaner \
  --hidden-import dubbing --hidden-import summarizer --hidden-import hardsub \
  --hidden-import clean_audio
```

The `--hidden-import` flags are required because `autosubs_core.py` imports each
module lazily (inside the function), and PyInstaller's static analysis does not
always detect them. Without them, the packaged app would fail with
"No module named …" when using that tool.

Rename the executable to the *target triple* and place it where Tauri expects it:

```bash
# Windows x64
move dist\autosubs-core.exe ..\..\src-tauri\binaries\autosubs-core-x86_64-pc-windows-msvc.exe
```

> The Whisper model (`small`) is **not** in the `.exe`: it is downloaded on first
> use. Keeping that download on demand keeps the installer light.

### B.2 Regenerate the icon

The application icon is generated from `src-tauri/app-icon.png` (1024x1024). If
you change that file you **must** regenerate the `src-tauri/icons/` set, because
the `.exe`/installer embeds those files, not `app-icon.png`:

```bash
cargo tauri icon src-tauri/app-icon.png
```

This rewrites `icon.ico`, `icon.icns`, the PNGs (`32x32`, `128x128`,
`128x128@2x`, …) and the Microsoft Store `Square*Logo.png` files. After
regenerating, **rebuild**: the icon only updates when the binary is rebuilt.

> Typical cause of "the icon is still an orange square": `app-icon.png` was
> replaced but `src-tauri/icons/` was not regenerated, or the app was not rebuilt.

### B.3 Package

```bash
cargo tauri build
```

This produces the `SubsForge.exe` executable and the installers in
`src-tauri/target/release/bundle/` (`.msi` via WiX and/or `.exe` via NSIS on
Windows). The product and installer names come from `productName` in
`tauri.conf.json` (`SubsForge`).

## Relevant configuration (`tauri.conf.json`)

```json
{
  "productName": "SubsForge",
  "identifier": "com.subsforge.app",
  "build":  { "frontendDist": "../src/webui" },
  "app":    { "withGlobalTauri": true,
              "windows": [{ "title": "SubsForge", "width": 1060, "height": 710,
                            "minWidth": 920, "minHeight": 610,
                            "decorations": false, "transparent": false }] },
  "bundle": { "externalBin": ["binaries/autosubs-core"], "icon": [ … ] }
}
```

- `withGlobalTauri: true` is required for the frontend to use
  `window.__TAURI__.core.invoke` and `.event.listen`.
- `frontendDist` points at the static interface; there is no `beforeDevCommand`.

## Versions

`tauri 2.1`, `tauri-plugin-shell 2.0`, `tauri-plugin-dialog 2.0`,
`tauri-plugin-log 2.0`, `@tauri-apps/api ^2`, `@tauri-apps/cli ^2`.

> Minor maintenance note: in `src-tauri/Cargo.toml`, `tauri-build` is pinned to
> `2.0.0-rc`. It is worth bumping to stable `2.0` in a future iteration; not
> urgent while the current build compiles.

## Release checklist

1. `pip install -r requirements.txt` with no errors.
2. Sidecar built and renamed in `src-tauri/binaries/`.
3. `app-icon.png` updated -> `cargo tauri icon` -> correct icon.
4. `cargo tauri build` with no errors.
5. Test on a clean machine: FFmpeg on the `PATH`, first launch downloads the
   Whisper model, all nine tools respond.
6. Verify the executable and window show **SubsForge** and the new icon.
