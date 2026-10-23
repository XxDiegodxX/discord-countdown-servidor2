import os
import sys
from datetime import datetime, timezone
import requests

# 1. Obtiene el webhook desde los secretos de GitHub
WEBHOOK_URL = os.environ.get("DISCORD_WEBHOOK")
if not WEBHOOK_URL:
    print("Error: No se encontró la variable DISCORD_WEBHOOK")
    sys.exit(1)

# 2. Configura los datos del evento
FECHA_EVENTO = datetime(2026, 11, 27, 18, 0, 0)
FECHA_CIERRE_INSCRIPCIONES = datetime(2026, 11, 4, 23, 59, 59)
NOMBRE_EVENTO = "Hackathon CoAfina 2026"

URL_INSCRIPCION = "https://forms.gle/5rfQqd1ubkmYUaSC8"
URL_WEB = "https://laa-hecap.github.io/coafina"

# Ruta local de tu imagen en el repositorio
RUTA_IMAGEN = os.path.join("imagenes", "imagen de prueba 1.png")

# 3. Cálculo de tiempos
ahora = datetime.now()
diferencia = FECHA_EVENTO - ahora
segundos_restantes = diferencia.total_seconds()
dias_restantes = diferencia.days
horas_restantes = int((segundos_restantes % 86400) // 3600)

timestamp_evento = int(FECHA_EVENTO.timestamp())
timestamp_inscripcion = int(FECHA_CIERRE_INSCRIPCIONES.timestamp())

# 4. Estado y encabezados
if dias_restantes > 1:
    cabecera = f"⏳ **¡CUENTA REGRESIVA — {NOMBRE_EVENTO}!**"
    tiempo_texto = f"Faltan **{dias_restantes} días y {horas_restantes:02d} horas**"
    color = 0x00A896
elif dias_restantes == 1:
    cabecera = f"🚨 **¡ATENCIÓN! SOLO QUEDA 1 DÍA — {NOMBRE_EVENTO}**"
    tiempo_texto = f"Faltan **1 día y {horas_restantes:02d} horas**"
    color = 0xF39C12
elif dias_restantes == 0 and segundos_restantes > 0:
    cabecera = f"🔥 **¡HOY ES EL GRAN DÍA — {NOMBRE_EVENTO}!**"
    tiempo_texto = f"Inicia en aproximadamente **{horas_restantes} horas**"
    color = 0xE74C3C
elif 0 >= segundos_restantes > -86400:
    cabecera = f"🎉 **¡EL EVENTO COMENZÓ — {NOMBRE_EVENTO}!**"
    tiempo_texto = "¡El Hackathon ya está en marcha!"
    color = 0x2ECC71
else:
    print("El evento ya concluyó.")
    sys.exit(0)

# 5. Mensaje de texto formateado (Garantiza diseño elegante aún sin embeds)
cuerpo_mensaje = (
    f"# {cabecera}\n\n"
    f"🗓️ **Tiempo restante:** {tiempo_texto} ⏳\n"
    f"🎯 **Inicio oficial:** <t:{timestamp_evento}:F> (<t:{timestamp_evento}:R>)\n\n"
    f"> **\"Aplica lo que sabes. Aprende algo nuevo.\"**\n"
    f"> Crea equipo con estudiantes de toda Latinoamérica y resuelve retos reales con datos abiertos.\n\n"
    f"📅 **Fechas:** 27, 28 y 29 de noviembre de 2026\n"
    f"🌐 **Modalidad:** 100% En línea\n"
    f"⏰ **Cierre de inscripciones:** <t:{timestamp_inscripcion}:D> (<t:{timestamp_inscripcion}:R>)\n\n"
    f"🎁 **Beneficios clave:**\n"
    f"• Premios para los mejores proyectos\n"
    f"• Fondo de ayuda para conexión\n"
    f"• No requieres equipo previo\n"
    f"• Multidisciplinario (todas las carreras aportan)\n\n"
    f"🔗 **Enlaces:**\n"
    f"👉 [Haz clic aquí para inscribirte]({URL_INSCRIPCION})\n"
    f"ℹ️ [Sitio web oficial, retos y recursos]({URL_WEB})\n"
    f"────────────────────────────────"
)

payload = {
    "username": "CoAfina Bot",
    "content": cuerpo_mensaje
}

# 6. Envío con la imagen adjunta nativamente
if os.path.exists(RUTA_IMAGEN):
    with open(RUTA_IMAGEN, "rb") as f:
        archivos = {"file": ("banner.png", f, "image/png")}
        r = requests.post(WEBHOOK_URL, data=payload, files=archivos)
else:
    r = requests.post(WEBHOOK_URL, json=payload)

if r.status_code in (200, 204):
    print("Mensaje enviado exitosamente a Discord.")
else:
    print(f"Error {r.status_code}: {r.text}")
