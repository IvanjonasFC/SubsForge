# Operaciones, seguridad y resolución de problemas

## Modelo de seguridad

SubsForge sigue el modelo de capacidades de Tauri v2: la interfaz solo puede
invocar lo que se declara explícitamente en `src-tauri/capabilities/default.json`.

Permisos concedidos actualmente:

- Controles de ventana: `minimize`, `maximize`, `unmaximize`,
  `toggle-maximize`, `is-maximized`, `close`, `start-dragging`.
- `dialog:allow-open` — diálogos de archivo/carpeta.
- `shell:allow-execute` **restringido al sidecar**: solo se permite ejecutar
  `binaries/autosubs-core` como *sidecar*, con argumentos. No hay ejecución de
  shell arbitraria.

```json
{ "identifier": "shell:allow-execute",
  "allow": [{ "name": "binaries/autosubs-core", "sidecar": true, "args": true }] }
```

### Recomendaciones de endurecimiento

1. **CSP.** `tauri.conf.json` no define aún `app.security.csp`. Para producción
   conviene una política estricta que solo permita recursos propios, p. ej.:
   `"default-src 'self'; img-src 'self' data:; style-src 'self' 'unsafe-inline'"`.
   La interfaz ya incorpora todo en un único archivo (sin CDNs), lo que facilita
   una CSP cerrada.
2. **`open_url`.** Usa `tauri_plugin_shell::open`. Limita los destinos a los
   dominios propios (portfolio, GitHub, ollama.com) si se quiere minimizar la
   superficie.
3. **Entradas del usuario.** Las rutas provienen de diálogos nativos, no de
   texto libre; aun así, el frontend escapa el contenido que inserta en el DOM
   (helper `esc()`), y `hardsub.py` escapa la ruta del `.srt` para FFmpeg.
4. **Sin telemetría ni red salvo lo documentado.** La única red saliente es:
   Google Translate (motor `google`), Ollama en `localhost:11434`, y la descarga
   inicial del modelo de Whisper. El resto es local.

## Registro de eventos (logging)

- **Rust:** `tauri-plugin-log` registra inicio de tareas, apertura de URLs y
  errores de ventana/sidecar (`info!`, `warn!`, `error!`).
- **Núcleo Python:** cada módulo imprime su progreso por `stdout`, que se ve en
  vivo en la terminal de la interfaz.
- **Legacy:** la GUI antigua (`src/main.py`, CustomTkinter) escribe en
  `autosubs.log`. No forma parte del camino de producción.

## Resolución de problemas

> **Antes de empaquetar con Tauri: reconstruye el sidecar.** El binario
> `src-tauri/binaries/autosubs-core-*.exe` se genera con PyInstaller a partir de
> `src/core/`. Si añades o cambias módulos de `core/` (p. ej. las 4 herramientas
> nuevas o `dubbing.py`) **debes regenerar ese .exe**; si no, la app empaquetada
> ejecutará una versión antigua del núcleo y las tareas nuevas fallarán aunque el
> botón exista. Ver [BUILD.md](BUILD.md) § B.1. En modo PyWebView no aplica: usa
> los `.py` en vivo.


| Síntoma | Causa probable | Solución |
| --- | --- | --- |
| "Instalar IA local" no muestra nada | (resuelto) usaba `alert()`, no soportado en WebView2 | Ahora abre un modal propio in-app. Si reaparece, revisar `ollamaGuide()` en `index.html`. |
| El icono es un cuadrado naranja | `src-tauri/icons/` no regenerado tras cambiar `app-icon.png`, o falta recompilar | `cargo tauri icon` y luego `cargo tauri build`. |
| Doblaje/Resumen/Hardsub/Limpiar voz fallan con "Faltan argumentos" (en Tauri) | (resuelto) `run_task` no cubría esos `kind` | Los cuatro brazos ya están en `lib.rs`. Al añadir tareas, actualizar el `match`. |
| "No se encontró el ejecutable: ffmpeg/ffsubsync" | No están en el PATH | Instalar FFmpeg y `pip install ffsubsync`. |
| El menú "Motor IA" no muestra modelos | Ollama no está corriendo | Arrancar Ollama y `ollama run llama3`; reiniciar la app. |
| El resumen con Google es genérico | Google no resume | Usar `ollama:<modelo>`. |
| La transcripción tarda en el primer uso | Descarga del modelo `small` de Whisper | Es normal la primera vez; queda cacheado. |
| Traducción con Google se detiene | Baneo temporal por volumen | Reintentos y rescate línea a línea ya integrados; esperar y reintentar. |

## Limitaciones conocidas y hoja de ruta

- **Doblaje (TTS):** implementado — lee el diálogo real del `.srt` y sincroniza
  cada línea por marca de tiempo (silencios entre tramos). Mejora futura posible:
  ajuste de tempo (atempo) para eliminar la deriva en diálogos muy densos.
- **Progreso de FFmpeg:** hardsub y limpieza no reportan porcentaje; se podría
  interceptar el `stderr` de FFmpeg para una barra de progreso real.
- **CSP:** pendiente de definir la política estricta descrita arriba.
- **Auto-actualización e instaladores firmados:** en la hoja de ruta de Tauri.
- **Descarga de modelos bajo demanda:** ya aplicada a Whisper; extensible a otros
  recursos para un instalador más ligero.

## Contactos y referencias del proyecto

- Contrato de coordinación de la migración a Tauri: `docs/CONTRATO_TAURI.md`.
- Bitácora de la migración: `migracion_tauri.log` (raíz del repo).
- Ampliación de herramientas (referencia histórica): `docs/AMPLIACION_TOOLS.md`.
