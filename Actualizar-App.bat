@echo off
setlocal
title SubsForge - Actualizar y abrir
cd /d "%~dp0"
echo ============================================================
echo   SubsForge - Actualizar la app y abrirla
echo     1) Regenerar el sidecar Python (SIEMPRE, a prueba de fallos)
echo     2) cargo tauri build  (mete frontend + sidecar en el .exe)
echo     3) Abrir la app
echo ============================================================
echo.

rem ---------- Requisitos ----------
set "PY="
where py >nul 2>nul && set "PY=py"
if not defined PY ( where python >nul 2>nul && set "PY=python" )
if not defined PY ( echo [ERROR] Falta Python. Instalalo desde https://www.python.org & pause & exit /b 1 )
where cargo >nul 2>nul || ( echo [ERROR] Falta Rust. Instalalo desde https://rustup.rs & pause & exit /b 1 )
cargo tauri --help >nul 2>nul || ( echo [ERROR] Falta la CLI de Tauri.  Instala:  cargo install tauri-cli & pause & exit /b 1 )

rem ---------- Paso 1: sidecar (SIEMPRE, para no correr nunca una version vieja) ----------
echo [1/3] Regenerando el sidecar Python (1-2 min)...
%PY% -m pip install --quiet --disable-pip-version-check pyinstaller edge-tts
if exist requirements.txt %PY% -m pip install --quiet --disable-pip-version-check -r requirements.txt
pushd src\core
%PY% -m PyInstaller --onefile --console --name autosubs-core autosubs_core.py ^
  --collect-all faster_whisper --collect-all ctranslate2 --collect-all pysubs2 ^
  --collect-all edge_tts ^
  --hidden-import translator --hidden-import whisper_gen --hidden-import ass_cleaner ^
  --hidden-import dubbing --hidden-import summarizer --hidden-import hardsub --hidden-import clean_audio ^
  --noconfirm
if not exist "dist\autosubs-core.exe" ( echo [ERROR] Fallo PyInstaller. Revisa arriba. & popd & pause & exit /b 1 )
if not exist "..\..\src-tauri\binaries" mkdir "..\..\src-tauri\binaries"
move /Y "dist\autosubs-core.exe" "..\..\src-tauri\binaries\autosubs-core-x86_64-pc-windows-msvc.exe" >nul
rmdir /S /Q build >nul 2>nul
rmdir /S /Q dist  >nul 2>nul
del /Q autosubs-core.spec >nul 2>nul
popd

rem ---------- Paso 2: compilar la app ----------
echo.
echo [2/3] Compilando con Tauri (unos minutos)...
cargo tauri build
if errorlevel 1 ( echo [ERROR] Fallo cargo tauri build. Revisa los mensajes de arriba. & pause & exit /b 1 )

rem ---------- Paso 3: abrir ----------
echo.
echo [3/3] Abriendo la app...
set "EXE=src-tauri\target\release\autosubs-pro.exe"
if exist "%EXE%" ( start "" "%EXE%" ) else ( echo [AVISO] No encuentro %EXE% ; revisa src-tauri\target\release. )

echo.
echo ============================================================
echo   LISTO. La app abierta ya lleva TODOS los cambios (frontend y Python).
echo ============================================================
pause
