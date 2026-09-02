# Contributing to SubsForge

Thanks for considering a contribution to SubsForge! Contributions of all sizes
are welcome — code, docs and bug reports.

## Architecture overview

SubsForge uses a modular three-layer architecture:

- **Frontend (`src/webui/`)** — vanilla JS and HTML/CSS. Lightweight and decoupled.
- **Backend bridge (`src-tauri/`)** — Rust with Tauri 2. Handles native OS interactions, IPC and security.
- **AI sidecar (`src/core/`)** — a Python binary that runs the heavy ML tasks (faster-whisper, CTranslate2) without blocking the UI thread.

## Development setup

You need Node.js, Rust/Cargo and Python installed.

### 1. Build the Python sidecar

Before launching the Tauri app you must compile the Python sidecar so the Rust
backend can spawn it.

```bash
cd src/core
pip install pyinstaller -r ../../requirements.txt
pyinstaller --onefile --console --name autosubs-core autosubs_core.py \
  --collect-all faster_whisper --collect-all ctranslate2 --collect-all pysubs2
```

Move the generated executable to `src-tauri/binaries/`, appending your target OS
triple (e.g. `autosubs-core-x86_64-pc-windows-msvc.exe` on Windows). See
[`docs/BUILD.md`](docs/BUILD.md) for the full build, including the extra
`--hidden-import` flags needed for every tool.

### 2. Run the Tauri app

From the repository root:

```bash
npx @tauri-apps/cli@^2 dev
```

For a no-build workflow, the PyWebView shell runs the Python modules live:
`python src/webui/app.py`.

## Commit style

We follow [Conventional Commits](https://www.conventionalcommits.org):
`feat:`, `fix:`, `chore:`, `docs:`, `refactor:`, `style:`, `test:`.

## Pull request process

1. Make sure the app starts and the affected tool works.
2. Do not commit secrets: `.env`, keys and tokens stay out (see `.gitignore`).
3. Update the docs when you change the interface, an IPC command, or a tool's
   arguments (three sites stay in sync — see [`docs/API.md`](docs/API.md)).
4. Describe the expected and the actual behavior clearly in the PR.

## Reporting issues

Please use the provided GitHub issue templates, describe the expected versus
actual behavior, and attach logs or error traces whenever possible.
