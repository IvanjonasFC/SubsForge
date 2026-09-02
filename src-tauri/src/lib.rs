use tauri::Manager;
use tauri::Emitter;
use tauri_plugin_shell::ShellExt;
use tauri_plugin_shell::process::CommandEvent;
use tauri_plugin_dialog::DialogExt;
use log::{error, info, warn};

#[tauri::command]
fn win_minimize(window: tauri::Window) {
    window.minimize().unwrap_or_else(|e| error!("Error al minimizar: {}", e));
}

#[tauri::command]
fn win_toggle_maximize(window: tauri::Window) {
    if window.is_maximized().unwrap_or(false) {
        window.unmaximize().unwrap_or_else(|e| error!("Error al desmaximizar: {}", e));
    } else {
        window.maximize().unwrap_or_else(|e| error!("Error al maximizar: {}", e));
    }
}

#[tauri::command]
fn win_close(window: tauri::Window) {
    window.close().unwrap_or_else(|e| error!("Error al cerrar: {}", e));
}

#[tauri::command]
fn show_info(app: tauri::AppHandle, message: String) {
    app.dialog()
        .message(message)
        .title("SubsForge")
        .show(|_| {});
}

#[tauri::command]
fn open_url(app: tauri::AppHandle, url: String) {
    info!("Opening URL: {}", url);
    let _ = app.shell().open(url, None).map_err(|e| error!("Failed to open URL: {}", e));
}

#[tauri::command]
async fn pick_file(app: tauri::AppHandle) -> Result<Option<String>, String> {
    let file_path = app.dialog().file().blocking_pick_file();
    Ok(file_path.map(|p| p.to_string()))
}

#[tauri::command]
async fn pick_folder(app: tauri::AppHandle) -> Result<Option<String>, String> {
    let folder_path = app.dialog().file().blocking_pick_folder();
    Ok(folder_path.map(|p| p.to_string()))
}

#[tauri::command]
async fn get_ollama(app: tauri::AppHandle) -> Result<Vec<String>, String> {
    let sidecar = app.shell().sidecar("autosubs-core").map_err(|e| e.to_string())?;
    let output = sidecar.args(["ollama"]).output().await.map_err(|e| e.to_string())?;
    
    if output.status.success() {
        let stdout = String::from_utf8(output.stdout).unwrap_or_default();
        let models: Vec<String> = serde_json::from_str(&stdout).unwrap_or_default();
        Ok(models)
    } else {
        Ok(vec![])
    }
}

#[tauri::command]
async fn run_task(app: tauri::AppHandle, kind: String, args: std::collections::HashMap<String, String>) -> Result<(), String> {
    info!("Iniciando tarea: {} con args: {:?}", kind, args);
    let sidecar = app.shell().sidecar("autosubs-core").map_err(|e| {
        error!("No se pudo inicializar el sidecar: {}", e);
        e.to_string()
    })?;
    
    let mut cmd_args = vec![kind.clone()];
    match kind.as_str() {
        "translate" => {
            if let (Some(path), Some(engine)) = (args.get("path"), args.get("engine")) {
                cmd_args.push(path.clone());
                cmd_args.push(engine.clone());
            }
        }
        "sync" => {
            if let (Some(vid), Some(sub)) = (args.get("vid"), args.get("sub")) {
                cmd_args.push(vid.clone());
                cmd_args.push(sub.clone());
            }
        }
        "whisper" => {
            if let Some(src) = args.get("src") {
                cmd_args.push(src.clone());
            }
        }
        "mux" => {
            if let (Some(vid), Some(sub)) = (args.get("vid"), args.get("sub")) {
                cmd_args.push(vid.clone());
                cmd_args.push(sub.clone());
            }
        }
        "cleaner" => {
            if let Some(file) = args.get("file") {
                cmd_args.push(file.clone());
            }
        }
        "dubbing" => {
            if let Some(srt) = args.get("srt") {
                cmd_args.push(srt.clone());
                if let Some(vid) = args.get("vid") {
                    if !vid.is_empty() {
                        cmd_args.push(vid.clone());
                    }
                }
                // La voz viaja como flag para no descuadrar las posiciones
                // cuando el vídeo (opcional) va vacío.
                if let Some(voice) = args.get("voice") {
                    if !voice.is_empty() {
                        cmd_args.push("--voice".to_string());
                        cmd_args.push(voice.clone());
                    }
                }
            }
        }
        "summary" => {
            if let (Some(srt), Some(engine)) = (args.get("srt"), args.get("engine")) {
                cmd_args.push(srt.clone());
                cmd_args.push(engine.clone());
            }
        }
        "hardsub" => {
            if let (Some(vid), Some(sub)) = (args.get("vid"), args.get("sub")) {
                cmd_args.push(vid.clone());
                cmd_args.push(sub.clone());
            }
        }
        "clean_audio" => {
            if let Some(vid) = args.get("vid") {
                cmd_args.push(vid.clone());
            }
        }
        _ => {}
    }

    let command = sidecar.args(cmd_args);
    let (mut rx, _child) = command.spawn().map_err(|e| {
        error!("Fallo al ejecutar el sidecar: {}", e);
        e.to_string()
    })?;

    tokio::spawn(async move {
        while let Some(event) = rx.recv().await {
            match event {
                CommandEvent::Stdout(data) => {
                    if let Ok(line) = String::from_utf8(data) {
                        let _ = app.emit("term-line", line);
                    }
                }
                CommandEvent::Stderr(data) => {
                    if let Ok(line) = String::from_utf8(data) {
                        let _ = app.emit("term-line", line);
                    }
                }
                CommandEvent::Terminated(payload) => {
                    let code = payload.code.unwrap_or(0);
                    let _ = app.emit("term-done", serde_json::json!({ "code": code }));
                }
                _ => {}
            }
        }
    });

    Ok(())
}

pub fn run() {
    tauri::Builder::default()
        .plugin(tauri_plugin_log::Builder::new().build())
        .plugin(tauri_plugin_shell::init())
        .plugin(tauri_plugin_dialog::init())
        .invoke_handler(tauri::generate_handler![
            win_minimize,
            win_toggle_maximize,
            win_close,
            open_url,
            pick_file,
            pick_folder,
            get_ollama,
            run_task,
            show_info
        ])
        .run(tauri::generate_context!())
        .expect("error while running tauri application");
}
