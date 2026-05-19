# 🏆 Evaluación 2 - Consola Deportiva con TheSportsDB

**Asignatura:** Programación y Redes Virtualizadas (DRY7122)

**Versión:** 1.4

---

## 📋 1. Stakeholder (Usuario específico)

**Perfil:** Analista táctico de un club de fútbol amateur o escuela deportiva.

**Necesidad real:** El analista debe preparar informes tácticos y scouting de equipos rivales, pero actualmente pierde más de 2 horas diarias navegando en múltiples páginas web copiando manualmente datos de ligas, equipos y jugadores.

**Problema concreto:**
- Exceso de tiempo en tareas repetitivas
- Riesgo de errores al copiar datos manualmente
- Dependencia de conexión a múltiples sitios web

---

## 💡 2. Propuesta de Valor (Solución)

La herramienta desarrollada permite:
- ✅ Consulta automática de datos deportivos en segundos
- ✅ Salida estructurada por consola
- ✅ Portabilidad mediante contenedor Docker
- ✅ Traza de ejecución con output.txt para auditoría

**Impacto:** Reducción del 95% del tiempo en la obtención de datos.

---

## 🔧 3. Variables de Entorno

```bash
# Opcional (TheSportsDB no requiere autenticación)
export SPORTSDB_KEY="tu_api_key_si_la_requiriera"