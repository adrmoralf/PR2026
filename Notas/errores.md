# 🐛 Registro de Errores

Aquí se documentan los errores cometidos durante el desarrollo del proyecto, tanto por los integrantes del equipo como por la IA asistente. El objetivo es aprender de ellos y no repetirlos.

## Formato

| Fecha | Quién | Descripción del error | Solución aplicada |
|-------|-------|----------------------|-------------------|
| 2026-10-22 | Manu | Conflictos de caché en el nodo de Telegram (`10-function.js setup`) y necesidad de actualizar constantemente el mensaje al usar botones Inline Keyboards para armar el carrito. | Descartar Inline Keyboards y migrar a Telegram Mini Apps (Web Apps) en HTML/JS servidas directamente desde Node-RED (`GET /carta_app`). |
| 2026-10-22 | Manu | Error de autenticación `ERR_NGROK_105` al levantar el túnel Ngrok HTTPS hacia el puerto 1880 de Node-RED. | Configurar adecuadamente el Authtoken de Ngrok en el entorno local. |
| 2026-10-22 | Manu | Error de host caído / endpoint inaccesible `ERR_NGROK_3200` en Ngrok tras regenerarse la URL dinámica del túnel. | Actualizar la nueva URL pública de Ngrok en el nodo Function de Node-RED encargado de construir los enlaces a la Web App. |
| 2026-10-15 | Antigravity (IA) | _(Ningún error registrado aún)_ | — |

---

## Notas
- Añadir cada error nuevo al inicio de la tabla para tener los más recientes primero.
- Ser específicos en la descripción: incluir el comando, archivo o concepto involucrado.
- La columna "Quién" puede ser: **Adri**, **Manu**, **Rubén**, **Irene** o **Antigravity (IA)**.
