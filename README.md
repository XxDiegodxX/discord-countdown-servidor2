# ⏳ CoAfina Bot — Contador Regresivo para Discord

Bot automatizado sin servidor (*serverless*) diseñado para enviar un mensaje diario de cuenta regresiva y enlaces oficiales hacia canales de Discord, optimizado para el **Hackathon CoAfina 2026**[cite: 1].

---

## 🚀 ¿Cómo funciona?

El sistema opera combinando **GitHub Actions**, un script en **Python** y un **Webhook de Discord**, sin requerir servidores encendidos 24/7 ni incurrir en costos de alojamiento:

1. **Disparador programado (GitHub Actions):**  
   A través de una regla `cron` configurada en `.github/workflows/contador.yml`, GitHub levanta un entorno virtual ligero de Ubuntu todos los días de forma automática.
2. **Cálculo de tiempos (Python):**  
   El script `contador.py` toma la fecha actual, calcula con exactitud los días y horas restantes para el inicio del evento y el cierre de inscripciones, y genera un mensaje enriquecido utilizando marcas de tiempo dinámicas de Discord (`<t:TIMESTAMP:F>`)[cite: 1].
3. **Publicación vía Webhook:**  
   El script envía el mensaje formateado directamente a Discord mediante una petición HTTP POST segura, suprimiendo previsualizaciones pesadas (`<URL>`) y manteniendo el diseño limpio y compacto. Una vez iniciado el evento, el script finaliza de manera silenciosa para no enviar alertas innecesarias.

---

## 🔒 Seguridad y Credenciales

* La URL del Webhook de Discord **no está expuesta en el código fuente**.
* Se gestiona mediante **GitHub Secrets** bajo la clave `DISCORD_WEBHOOK`[cite: 4].
* Esto permite que el repositorio sea público o compartido con colaboradores sin riesgo de filtración de acceso al canal.

---

## 🛠️ Estructura del Proyecto

```text
├── .github/
│   └── workflows/
│       └── contador.yml    # Programación cron y configuración del runner
├── contador.py             # Lógica de cálculo, formato de texto y envío
└── README.md               # Documentación general
