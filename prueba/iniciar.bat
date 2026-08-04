@echo off
cd /d "%~dp0"
echo Abriendo SafeCore...
start http://localhost:8000
"C:\Users\Lenovo\AppData\Local\Programs\Python\Python311\python.exe" app_demo.py
pause