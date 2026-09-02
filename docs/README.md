# Technical documentation — SubsForge

Production-level documentation for the **SubsForge** subtitle toolkit, organized
by audience and task. Start with whichever you need.

| Document | Purpose |
| --- | --- |
| [ARCHITECTURE.md](ARCHITECTURE.md) | System design, the three layers, the IPC model and data flow. |
| [API.md](API.md) | Reference for the two IPC boundaries: `invoke` commands (Frontend <-> Rust) and the sidecar CLI (Rust <-> Python). |
| [TOOLS.md](TOOLS.md) | The nine tools: inputs, outputs, engines and the files they generate. |
| [BUILD.md](BUILD.md) | Build the sidecar (PyInstaller), package with Tauri, regenerate the icon and produce the installer. |
| [OPERATIONS.md](OPERATIONS.md) | Security, permissions, logging, troubleshooting and known limitations. |

## One-line summary

SubsForge is a desktop app that translates, generates, syncs, merges, cleans,
dubs, summarizes and burns in video subtitles, running locally. The interface is
web-based (HTML/CSS/JS), the desktop shell is **Tauri** (with **PyWebView** as an
alternative), and the heavy processing lives in a **Python core** that runs as a
separate process so it never blocks the interface.

## Documentation conventions

- Code paths are relative to the repository root.
- `invoke` command names and CLI subcommand names are written in `monospace`.
- "Sidecar" = the Python binary (`autosubs-core`) that Tauri launches as a child process.
- The internal Rust crate name (`autosubs-pro`) and sidecar binary name
  (`autosubs-core`) are kept for build compatibility; they are **not** the
  product's visible name, which is **SubsForge**.

Product version: 1.0.0 · Documentation last revised: 2026-09-01.
