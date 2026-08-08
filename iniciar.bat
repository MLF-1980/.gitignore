@echo off
:: Cambiar al directorio donde está el archivo .bat
cd /d "%~dp0"

echo Iniciando servidor...
:: Iniciar el servidor en segundo plano
start "" python -m src.main

:: Esperar unos segundos para dar tiempo a que el servidor levante
timeout /t 2 >nul

:: Abrir el navegador en la dirección del servidor
start http://localhost:8000