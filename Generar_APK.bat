@echo off
setlocal
cd /d "%~dp0"
powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0generar-apk.ps1"
if errorlevel 1 echo No se genero el APK. Revisa el mensaje anterior.
pause
