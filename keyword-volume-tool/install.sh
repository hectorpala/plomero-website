#!/bin/bash

# ============================================================================
# Script de Instalación Automática - Keyword Volume Tool
# ============================================================================

echo ""
echo "🚀 KEYWORD VOLUME TOOL - INSTALACIÓN AUTOMÁTICA"
echo "=================================================================="
echo ""

# Verificar Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 no encontrado. Instala Python 3.8+ primero."
    exit 1
fi

echo "✅ Python 3 encontrado: $(python3 --version)"

# Verificar Node.js
if ! command -v node &> /dev/null; then
    echo "❌ Node.js no encontrado. Instala Node.js 16+ primero."
    exit 1
fi

echo "✅ Node.js encontrado: $(node --version)"
echo ""

# ============================================================================
# BACKEND SETUP
# ============================================================================

echo "📦 PASO 1/3: Instalando Backend (Python/FastAPI)..."
echo "=================================================================="

cd backend

# Crear virtual environment
echo "   → Creando entorno virtual..."
python3 -m venv venv

# Activar virtual environment
echo "   → Activando entorno virtual..."
source venv/bin/activate

# Instalar dependencias
echo "   → Instalando dependencias..."
pip install -q -r requirements.txt

if [ $? -eq 0 ]; then
    echo "   ✅ Backend instalado correctamente"
else
    echo "   ❌ Error instalando backend"
    exit 1
fi

cd ..
echo ""

# ============================================================================
# FRONTEND SETUP
# ============================================================================

echo "📦 PASO 2/3: Instalando Frontend (React)..."
echo "=================================================================="

cd frontend

# Instalar dependencias
echo "   → Instalando dependencias npm..."
npm install --silent

if [ $? -eq 0 ]; then
    echo "   ✅ Frontend instalado correctamente"
else
    echo "   ❌ Error instalando frontend"
    exit 1
fi

cd ..
echo ""

# ============================================================================
# CREAR SCRIPTS DE INICIO
# ============================================================================

echo "📝 PASO 3/3: Creando scripts de inicio..."
echo "=================================================================="

# Script para iniciar backend
cat > start-backend.sh << 'EOF'
#!/bin/bash
cd backend
source venv/bin/activate
python main.py
EOF

chmod +x start-backend.sh

# Script para iniciar frontend
cat > start-frontend.sh << 'EOF'
#!/bin/bash
cd frontend
npm start
EOF

chmod +x start-frontend.sh

# Script para iniciar ambos (requiere tmux)
cat > start-all.sh << 'EOF'
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
EOF

chmod +x start-all.sh

echo "   ✅ Scripts creados:"
echo "      - start-backend.sh"
echo "      - start-frontend.sh"
echo "      - start-all.sh"
echo ""

# ============================================================================
# RESUMEN
# ============================================================================

echo "=================================================================="
echo "✅ INSTALACIÓN COMPLETADA"
echo "=================================================================="
echo ""
echo "📊 Todo listo para usar Keyword Volume Tool"
echo ""
echo "🚀 INICIAR APLICACIÓN:"
echo ""
echo "   Opción 1 (Automático - requiere tmux):"
echo "   ./start-all.sh"
echo ""
echo "   Opción 2 (Manual - 2 terminales):"
echo "   Terminal 1: ./start-backend.sh"
echo "   Terminal 2: ./start-frontend.sh"
echo ""
echo "🌐 URL:"
echo "   Frontend: http://localhost:3000"
echo "   Backend:  http://localhost:8000"
echo "   API Docs: http://localhost:8000/docs"
echo ""
echo "📖 DOCUMENTACIÓN:"
echo "   - INICIO_RAPIDO.md (guía en 3 pasos)"
echo "   - README.md (documentación completa)"
echo ""
echo "✨ Happy keyword research!"
echo ""
