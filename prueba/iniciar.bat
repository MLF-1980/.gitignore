@echo off
cd /d "%~dp0"

echo Iniciando el servidor SafeCore...
start "" python app_demo.py

:: Espera 2 segundos para asegurar que el servidor esté activo
timeout /t 2 >nul

echo Abriendo la aplicacion en el navegador...
start http://localhost:8000/

exit