#!/bin/bash
# Script de automatización - Evaluación 2 (Versión definitiva)

set -e

echo "================================================================================"
echo "🚀 INICIANDO SCRIPT DE AUTOMATIZACIÓN - EVALUACIÓN 2"
echo "================================================================================"

# Deshabilitar progreso interactivo de pip
export PIP_PROGRESS_BAR=off
export PIP_NO_COLOR=1
export PIP_DISABLE_PIP_VERSION_CHECK=1

echo ""
echo "📝 [1/5] Generando Dockerfile..."

cat > Dockerfile << 'EOF'
FROM python:3.9-alpine

WORKDIR /app

# Copiar requirements primero
COPY requirements.txt .

# Instalar requests sin barra de progreso y sin threads
RUN pip install --no-cache-dir --progress-bar off --no-color requests

# Copiar la aplicación
COPY app.py .

CMD ["python", "app.py"]
EOF

echo " ✅ Dockerfile generado correctamente"

# ===== PASO 2: Verificar requirements.txt =====
echo ""
echo "🔍 [2/5] Verificando requirements.txt..."
if [ ! -f "requirements.txt" ]; then
    echo "requests>=2.25.0" > requirements.txt
fi
echo " ✅ requirements.txt listo"

# ===== PASO 3: Construir imagen Docker =====
echo ""
echo "🐳 [3/5] Construyendo imagen Docker..."
docker rmi -f evaluacion2-app 2>/dev/null || true
docker build --progress=plain -t evaluacion2-app .
echo " ✅ Imagen construida exitosamente"

# ===== PASO 4: Ejecutar contenedor =====
echo ""
echo "🏃 [4/5] Ejecutando contenedor..."
docker rm -f evaluacion2_container 2>/dev/null || true
docker run --name evaluacion2_container evaluacion2-app
echo " ✅ Contenedor ejecutado"

# ===== PASO 5: Generar output.txt =====
echo ""
echo "📄 [5/5] Generando output.txt..."
{
    echo "==================== DOCKER PS -A ===================="
    docker ps -a | grep evaluacion2_container
    echo ""
    echo "==================== LOGS DE LA APLICACIÓN ===================="
    docker logs evaluacion2_container
} > output.txt
echo " ✅ output.txt generado correctamente"

echo ""
echo "================================================================================"
echo "✅ SCRIPT FINALIZADO"
echo "================================================================================"
docker ps -a | grep evaluacion2_container
