#!/bin/bash
# Script de automatización - Evaluación 2
# Genera Dockerfile, construye imagen, ejecuta contenedor y genera output.txt
# Script de automatización - Evaluación 2
set -e

echo "================================================================================"
echo "🚀 INICIANDO SCRIPT DE AUTOMATIZACIÓN - EVALUACIÓN 2"
echo "================================================================================"

# Deshabilitar BuildKit (probar sin él)
unset DOCKER_BUILDKIT

echo ""
echo "📝 [1/5] Generando Dockerfile..."

# Dockerfile con pip menos agresivo
cat > Dockerfile << 'EOF'
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir --no-compile requests>=2.25.0
COPY app.py .
CMD ["python", "app.py"]
EOF

echo " ✅ Dockerfile generado correctamente"

# ===== PASO 2: Verificar requirements.txt =====
echo ""
echo "🔍 [2/5] Verificando requirements.txt..."
if [ ! -f "requirements.txt" ]; then
    echo " ⚠️ No existe requirements.txt, creándolo..."
    echo "requests>=2.25.0" > requirements.txt
fi
echo " ✅ requirements.txt listo"


# ===== PASO 3: Construir imagen Docker =====
echo ""
echo "🐳 [3/5] Construyendo imagen Docker..."
docker rmi -f evaluacion2-app 2>/dev/null || true
docker build -t evaluacion2-app .
echo " ✅ Imagen construida exitosamente"


# ===== PASO 4: Ejecutar contenedor =====
echo ""
echo "🏃 [4/5] Ejecutando contenedor..."
docker rm -f evaluacion2_container 2>/dev/null || true
# Comprobar si estamos en un entorno con restricciones de seccomp (como tu VM)
if docker run --security-opt seccomp=unconfined --name evaluacion2_container evaluacion2-app 2>/dev/null; then
    echo " ✅ Contenedor ejecutado (con seccomp deshabilitado)"
else
    # Fallback: ejecutar sin la opción seccomp (funciona en la mayoría de sistemas)
    docker rm -f evaluacion2_container 2>/dev/null || true
    docker run --name evaluacion2_container evaluacion2-app
    echo " ✅ Contenedor ejecutado (modo estándar)"
fi
# ===== PASO 5: Generar output.txt automáticamente =====
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
echo "✅ SCRIPT FINALIZADO - Todo correcto"
echo "================================================================================"
echo ""
echo "📊 Estado final del contenedor:"
docker ps -a | grep evaluacion2_container
echo ""
echo "📄 output.txt creado. Puedes verlo con: cat output.txt"