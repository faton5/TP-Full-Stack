#!/bin/bash

ROOT="$(cd "$(dirname "$0")" && pwd)"

echo ">>> Lancement du backend Flask (port 5000)..."
cd "$ROOT/Backend"
venv/bin/python app.py &
BACKEND_PID=$!

echo ">>> Lancement du serveur frontend (port 8080)..."
cd "$ROOT/frontend"
python3 -m http.server 8080 --bind 127.0.0.1 &
FRONTEND_PID=$!

# Arrêter les deux processus proprement quand on fait Ctrl+C
trap "echo ''; echo '>>> Arrêt...'; kill $BACKEND_PID $FRONTEND_PID 2>/dev/null; exit 0" INT TERM

sleep 1
echo ""
echo "  Backend  : http://localhost:5000/api/suggestions"
echo "  Frontend : http://localhost:8080"
echo ""
echo "Ctrl+C pour tout arrêter."

# Ouvrir le navigateur
xdg-open http://localhost:8080 2>/dev/null &

wait $BACKEND_PID $FRONTEND_PID
