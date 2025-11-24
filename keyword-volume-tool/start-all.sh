#!/bin/bash

echo ""
echo "🚀 Iniciando Keyword Volume Tool..."
echo ""

# Verificar si tmux está instalado
if ! command -v tmux &> /dev/null; then
    echo "❌ tmux no encontrado."
    echo ""
    echo "Opción 1: Instalar tmux"
    echo "  brew install tmux (macOS)"
    echo "  sudo apt install tmux (Linux)"
    echo ""
    echo "Opción 2: Iniciar manualmente en 2 terminales:"
    echo "  Terminal 1: ./start-backend.sh"
    echo "  Terminal 2: ./start-frontend.sh"
    echo ""
    exit 1
fi

# Crear sesión tmux con 2 paneles
tmux new-session -d -s keyword-tool

# Panel 1: Backend
tmux send-keys -t keyword-tool "cd backend && source venv/bin/activate && python main.py" C-m

# Dividir ventana horizontalmente
tmux split-window -h -t keyword-tool

# Panel 2: Frontend (esperar 3 segundos para que backend inicie)
tmux send-keys -t keyword-tool "sleep 3 && cd frontend && npm start" C-m

# Adjuntar a la sesión
echo "✅ Servicios iniciados en tmux"
echo ""
echo "Para ver los logs:"
echo "  tmux attach -t keyword-tool"
echo ""
echo "Para detener:"
echo "  tmux kill-session -t keyword-tool"
echo ""

# Esperar 5 segundos y abrir navegador
sleep 5

# Abrir navegador
if command -v open &> /dev/null; then
    open http://localhost:3000
elif command -v xdg-open &> /dev/null; then
    xdg-open http://localhost:3000
fi

echo "🌐 Aplicación disponible en: http://localhost:3000"
echo ""
