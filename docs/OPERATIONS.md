# Operations, security and troubleshooting

## Security model

SubsForge follows the Tauri v2 capability model: the interface can only invoke
what is explicitly declared in `src-tauri/capabilities/default.json`.

Currently granted permissions:

- Window controls: `minimize`, `maximize`, `unmaximize`, `toggle-maximize`,
  `is-maximized`, `close`, `start-dragging`.
- `dialog:allow-open` — file/folder dialogs.
- `shell:allow-execute` **restricted to the sidecar**: only
  `binaries/autosubs-core` may be executed as a *sidecar*, with arguments. There
  is no arbitrary shell execution.

```json
{ "identifier": "shell:allow-execute",
  "allow": [{ "name": "binaries/autosubs-core", "sidecar": true, "args": true }] }
```

### Hardening recommendations

1. **CSP.** `tauri.conf.json` does not yet define `app.security.csp`. For
   production, a strict policy that only allows own resources is advisable, e.g.
   `"default-src 'self'; img-src 'self' data:; style-src 'self' 'unsafe-inline'"`.
   The interface already bundles everything in a single file (no CDNs), which
   makes a closed CSP easy.
2. **`open_url`.** Uses `tauri_plugin_shell::open`. Limit destinations to your own
   domains (portfolio, GitHub, ollama.com) to minimize the attack surface.
3. **User input.** Paths come from native dialogs, not free text; even so, the
   frontend escapes content it inserts into the DOM (the `esc()` helper), and
   `hardsub.py` escapes the `.srt` path for FFmpeg.
4. **No telemetry or network beyond what is documented.** The only outbound
   traffic is: Google Translate (the `google` engine), Ollama on
   `localhost:11434`, and the initial Whisper model download. Everything else is
   local.

## Logging

- **Rust:** `tauri-plugin-log` records task starts, URL opens and window/sidecar
  errors (`info!`, `warn!`, `error!`).
- **Python core:** each module prints its progress to `stdout`, shown live in the
  interface terminal.
- **Legacy:** the old GUI (`src/main.py`, CustomTkinter) writes to `autosubs.log`.
  It is not part of the production path.

## Troubleshooting

> **Before packaging with Tauri: rebuild the sidecar.** The
> `src-tauri/binaries/autosubs-core-*.exe` binary is generated with PyInstaller
> from `src/core/`. If you add or change modules in `core/` you **must**
> regenerate that `.exe`; otherwise the packaged app runs an old version of the
> core and new tasks fail even though the button exists. See [BUILD.md](BUILD.md)
> § B.1. In PyWebView mode this does not apply: it uses the `.py` files live.

| Symptom | Likely cause | Fix |
| --- | --- | --- |
| "Install local AI" shows nothing | (resolved) it used `alert()`, unsupported in WebView2 | Now opens an in-app modal. If it reappears, check `ollamaGuide()` in `index.html`. |
| The icon is an orange square | `src-tauri/icons/` not regenerated after changing `app-icon.png`, or not rebuilt | `cargo tauri icon` then `cargo tauri build`. |
| Dubbing/Summary/Hardsub/Voice cleanup fail with "missing arguments" (in Tauri) | (resolved) `run_task` did not cover those `kind`s | All four arms are in `lib.rs`. When adding tasks, update the `match`. |
| "Executable not found: ffmpeg/ffsubsync" | Not on the `PATH` | Install FFmpeg and `pip install ffsubsync`. |
| The "AI engine" menu shows no models | Ollama is not running | Start Ollama and `ollama run llama3`; restart the app. |
| The Google summary is generic | Google does not summarize | Use `ollama:<model>`. |
| Transcription is slow on first use | Downloading the Whisper `small` model | Normal the first time; it is then cached. |
| Google translation stalls | Temporary ban from volume | Retries and line-by-line rescue are built in; wait and retry. |

## Known limitations and roadmap

- **Dubbing (TTS):** implemented — it reads the real dialogue from the `.srt` and
  syncs each line by timestamp (silences between segments). Possible future
  improvement: tempo adjustment (atempo) to remove drift in very dense dialogue.
- **FFmpeg progress:** hardsub and cleanup do not report a percentage; FFmpeg's
  `stderr` could be intercepted for a real progress bar.
- **CSP:** the strict policy described above is still to be defined.
- **Auto-update and signed installers:** on the Tauri roadmap.
- **On-demand model download:** already applied to Whisper; extensible to other
  resources for a lighter installer.
