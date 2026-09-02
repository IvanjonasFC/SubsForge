@echo off
title SubsForge
cd /d "%~dp0"

rem Abre la app YA compilada (no recompila nada).
set "EXE=src-tauri\target\release\autosubs-pro.exe"

if not exist "%EXE%" (
  echo ============================================================
  echo   No se encuentra la app compilada:
  echo     %EXE%
  echo.
  echo   Compilala primero:
  echo     1) build-sidecar.bat        (empaqueta el nucleo Python)
  echo     2) cargo tauri build        (genera el .exe y el instalador)
  echo ============================================================
  pause
  exit /b 1
)

start "" "%EXE%"
exit /b 0
