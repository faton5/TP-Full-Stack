@echo off
cd /d "%~dp0"

echo >>> Lancement du backend Flask (port 5000)...
start "Backend Flask" cmd /k "cd Backend && venv\Scripts\python app.py"

echo >>> Lancement du serveur frontend (port 8080)...
start "Frontend" cmd /k "cd frontend && python -m http.server 8080 --bind 127.0.0.1"

timeout /t 2 /nobreak >nul

echo.
echo   Backend  : http://localhost:5000/api/suggestions
echo   Frontend : http://localhost:8080
echo.
echo Ferme les fenetres Backend et Frontend pour tout arreter.

start http://localhost:8080
