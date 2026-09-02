@echo off
title SubsForge - Modo Desarrollo
cd /d "%~dp0"
echo ============================================================
echo   SubsForge - Modo Desarrollo (Tauri, hot reload)
echo.
echo   OJO: esto NO abre el .exe ya compilado. Recompila una
echo   version de desarrollo (la primera vez tarda varios minutos).
echo   Para solo ABRIR la app ya hecha, usa  SubsForge.bat
echo ============================================================
echo.

where cargo >nul 2>nul
if errorlevel 1 (
  echo [ERROR] No se encontro 'cargo'. Instala Rust desde https://rustup.rs
  pause & exit /b 1
)

rem Comprobar que la CLI de Tauri esta instalada
cargo tauri --help >nul 2>nul
if errorlevel 1 (
  echo [ERROR] Falta la CLI de Tauri ^(por eso fallaba^).
  echo Instalala con UNO de estos comandos y vuelve a ejecutar este .bat:
  echo.
  echo     cargo install tauri-cli
  echo         o bien
  echo     npm install -g @tauri-apps/cli
  echo.
  pause & exit /b 1
)

cargo tauri dev
echo.
echo (La app de desarrollo se cerro. Si hubo errores, aparecen arriba.)
pause
