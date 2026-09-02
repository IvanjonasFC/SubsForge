@echo off
title SubsForge - Regenerar sidecar
cd /d "%~dp0"
echo ============================================================
echo   SubsForge - Regenerando el nucleo (sidecar) con PyInstaller
echo   Empaqueta src\core\*.py en autosubs-core.exe para Tauri.
echo   Hazlo cada vez que cambie algo en src\core\.
echo ============================================================
echo.

set "PY="
where py >nul 2>nul && set "PY=py"
if not defined PY ( where python >nul 2>nul && set "PY=python" )
if not defined PY (
  echo [ERROR] No se encontro Python. Instalalo desde https://www.python.org y marca "Add Python to PATH".
  pause & exit /b 1
)

echo [*] Instalando / actualizando dependencias...
%PY% -m pip install --quiet --disable-pip-version-check pyinstaller edge-tts
if exist requirements.txt %PY% -m pip install --quiet --disable-pip-version-check -r requirements.txt

cd src\core
echo.
echo [*] Empaquetando (puede tardar 1-3 minutos)...
%PY% -m PyInstaller --onefile --console --name autosubs-core autosubs_core.py ^
  --collect-all faster_whisper --collect-all ctranslate2 --collect-all pysubs2 ^
  --collect-all edge_tts ^
  --hidden-import translator --hidden-import whisper_gen --hidden-import ass_cleaner ^
  --hidden-import dubbing --hidden-import summarizer --hidden-import hardsub --hidden-import clean_audio ^
  --noconfirm

if not exist "dist\autosubs-core.exe" (
  echo.
  echo [ERROR] Fallo el empaquetado. Revisa los mensajes de arriba.
  cd ..\..
  pause & exit /b 1
)

echo.
echo [*] Copiando el .exe a src-tauri\binaries ...
if not exist "..\..\src-tauri\binaries" mkdir "..\..\src-tauri\binaries"
move /Y "dist\autosubs-core.exe" "..\..\src-tauri\binaries\autosubs-core-x86_64-pc-windows-msvc.exe" >nul

echo [*] Limpiando temporales...
rmdir /S /Q build >nul 2>nul
rmdir /S /Q dist >nul 2>nul
del /Q autosubs-core.spec >nul 2>nul

cd ..\..
echo.
echo ============================================================
echo   LISTO. Sidecar regenerado con todos los arreglos.
echo   Ahora ejecuta:   cargo tauri build      (instalador)
echo             o bien: cargo tauri dev        (para probar)
echo ============================================================
pause
