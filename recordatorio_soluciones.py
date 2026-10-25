import os
import sys
from datetime import datetime
import requests

# 1. Obtener webhook desde los secretos del repositorio
WEBHOOK_URL = os.environ.get("DISCORD_WEBHOOK")
if not WEBHOOK_URL:
    print("Error: No se encontró la variable DISCORD_WEBHOOK")
    sys.exit(1)

# 2. Configuración de la fecha límite (modificable más adelante)
# Formato: Año, Mes, Día, Hora, Minuto, Segundo
FECHA_LIMITE_ENTREGA = datetime(2026, 11, 29, 18, 0, 0)
URL_SUBIDA_SOLUCIONES = "https://forms.gle/ejemplo_entrega_soluciones"

# 3. Cálculo de tiempo restante
ahora = datetime.now()
diferencia = FECHA_LIMITE_ENTREGA - ahora
segundos_restantes = diferencia.total_seconds()
dias_restantes = diferencia.days
horas_restantes = int((segundos_restantes % 86400) // 3600)

timestamp_limite = int(FECHA_LIMITE_ENTREGA.timestamp())

# Si el plazo ya venció, el script termina sin publicar nada
if segundos_restantes <= 0:
    print("El plazo de entrega ya culminó. No se envía mensaje.")
    sys.exit(0)

# 4. Formato dinámico según el tiempo disponible
if dias_restantes > 0:
    tiempo_texto = f"**{dias_restantes} días y {horas_restantes:02d} horas**"
    aviso_tono = "⏳ ¡El reloj sigue corriendo para sus proyectos!"
elif horas_restantes > 2:
    tiempo_texto = f"**{horas_restantes} horas**"
    aviso_tono = "⚡ ¡Últimas horas para finalizar su desarrollo!"
else:
    tiempo_texto = f"**menos de {horas_restantes if horas_restantes > 0 else 1} hora(s)**"
    aviso_tono = "🚨 **¡ATENCIÓN: RECTA FINAL DE ENTREGAS!**"

# 5. Cuerpo del mensaje para Discord
cuerpo_mensaje = (
    f"# 📬 Recordatorio de Entrega de Soluciones — Hackathon CoAfina\n\n"
    f"{aviso_tono}\n\n"
    f"⏰ **Fecha y hora límite:** <t:{timestamp_limite}:F> (<t:{timestamp_limite}:R>)\n"
    f"⌛ **Tiempo restante para subir:** {tiempo_texto}\n\n"
    f"> Recuerden subir el repositorio de su código, la documentación y el video/demo antes del cierre de la plataforma.\n\n"
    f"🔗 **Formulario de entrega:**\n"
    f"👉 [Haz clic aquí para enviar la solución de tu equipo](<{URL_SUBIDA_SOLUCIONES}>)"
)

payload = {
    "content": cuerpo_mensaje
}

r = requests.post(WEBHOOK_URL, json=payload)

if r.status_code in (200, 204):
    print("Recordatorio de soluciones enviado con éxito a Discord.")
else:
    print(f"Error {r.status_code}: {r.text}")
    sys.exit(1)
