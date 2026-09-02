# API reference (IPC)

SubsForge has two inter-process communication boundaries. This reference is the
exact contract between them; keeping the three implementations (Rust, `app.py`
and the sidecar) aligned is what guarantees each tool receives its arguments
correctly.

---

## Boundary 1 — Interface <-> Shell

The interface calls commands and listens for events through the `BRIDGE` object.
Under Tauri, each command is a `#[tauri::command]` in `src-tauri/src/lib.rs`;
under PyWebView, a method of the `Api` class in `src/webui/app.py`.

### Commands

| Command (Tauri) | Method (PyWebView) | Arguments | Returns |
| --- | --- | --- | --- |
| `win_minimize` | `win_min` | — | void |
| `win_toggle_maximize` | `win_max` | — | void |
| `win_close` | `win_close` | — | void |
| `open_url` | `open_url` | `{ url }` | void |
| `pick_file` | `pick_file` | — | absolute path `string` or `null` |
| `pick_folder` | `pick_folder` | — | absolute path `string` or `null` |
| `get_ollama` | `get_ollama` | — | `string[]` (model names; `[]` if Ollama is not running) |
| `run_task` | `run` | `{ kind, args }` | void (non-blocking) |
| `show_info` | — (uses its own modal) | `{ message }` | void |

### `run_task` — map of `kind` to `args`

The frontend builds `args` from the files chosen per tool (keys come from the `v`
field of each row in `TABS`) plus the AI engine.

| `kind` | `args` | Notes |
| --- | --- | --- |
| `translate` | `{ path, engine }` | `engine`: `google` or `ollama:<model>` |
| `sync` | `{ vid, sub }` | |
| `whisper` | `{ src }` | file or folder |
| `mux` | `{ vid, sub }` | |
| `cleaner` | `{ file }` | `.ass` file |
| `dubbing` | `{ srt, vid? }` | `vid` optional (dual audio if provided) |
| `summary` | `{ srt, engine }` | real summary only with `ollama:<model>` |
| `hardsub` | `{ vid, sub }` | |
| `clean_audio` | `{ vid }` | video or audio |

> **Maintenance note.** Adding a tool means touching THREE places: the
> `match kind` in `run_task` in `lib.rs`, the `ARG_ORDER` dictionary in `app.py`,
> and `TABS`/`I18N` in the frontend. If `run_task` does not handle a `kind`, the
> task is launched with no arguments and fails with "missing arguments".

### Events (Tauri only)

Rust emits two events the frontend listens for with `listen`:

- `term-line` — payload `string`: one line of process output. The frontend
  appends it to the terminal as-is (trimming the trailing newline).
- `term-done` — payload `{ code: number }`: the process has finished.

Under PyWebView the equivalent is a direct
`window.evaluate_js("termAppend(...)")` call from the process thread.

### Window

`decorations: false`, `transparent: false`, `width: 1060`, `height: 710`,
`minWidth: 920`, `minHeight: 610`, `title: "SubsForge"`. The drag region uses
`data-tauri-drag-region` (Tauri) and `pywebview-drag-region` (PyWebView).

---

## Boundary 2 — Shell <-> Sidecar (CLI)

The shell runs the `autosubs-core` binary (declared in
`tauri.conf.json > bundle.externalBin` as `binaries/autosubs-core`) and forwards
its `stdout`. PyInstaller appends the target-triple suffix, e.g.
`autosubs-core-x86_64-pc-windows-msvc.exe`.

### Subcommands

```
autosubs-core ollama                                # prints ONE JSON line: ["llama3","mistral"] (or [])
autosubs-core translate   <srt> <engine> [lang]     # engine: google | ollama:model ; default lang is es
autosubs-core sync        <video> <sub>
autosubs-core whisper     <file_or_folder>
autosubs-core mux         <video> <sub>
autosubs-core cleaner     <file.ass>
autosubs-core dubbing     <srt> [video]
autosubs-core summary     <srt> <engine>
autosubs-core hardsub     <video> <sub>
autosubs-core clean_audio <video>
```

### Output contract

- Line-buffered output (`PYTHONUNBUFFERED=1`); each line is a progress message.
  Prefix conventions are: `[*]` step in progress, `[+]`/`[OK]` success,
  `[!]` warning, `[ERROR]` failure.
- Exit code `0` = success.
- For `get_ollama`, Rust runs `autosubs-core ollama`, captures `stdout` and
  parses the single-line JSON.
- `ffsubsync` and `ffmpeg` are called as binaries on the `PATH`; they are not
  bundled.

### Integration example (Rust)

```rust
let sidecar = app.shell().sidecar("autosubs-core")?;
let (mut rx, _child) = sidecar.args(cmd_args).spawn()?;
tokio::spawn(async move {
    while let Some(event) = rx.recv().await {
        match event {
            CommandEvent::Stdout(d) | CommandEvent::Stderr(d) => {
                if let Ok(line) = String::from_utf8(d) { let _ = app.emit("term-line", line); }
            }
            CommandEvent::Terminated(p) => {
                let _ = app.emit("term-done", serde_json::json!({ "code": p.code.unwrap_or(0) }));
            }
            _ => {}
        }
    }
});
```
