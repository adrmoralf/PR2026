# 🧑‍💻 Manu — Notas personales

## 🎯 Tarea principal

**Configuración de Node-RED como orquestador del sistema + integración con Telegram**

## 📋 Subtareas

- [ ] **Instalar Node-RED**
  - [x] Desplegar Node-RED en laptop/PC en puerto `1880`
  - [ ] Configurar acceso al editor; no exponerlo públicamente sin autenticación

- [x] **Aprender los fundamentos de Node-RED**
  - [x] Entender el concepto de nodos, flujos y mensajes (`msg.payload`)
  - [x] Practicar con nodos básicos: inject, debug, function, switch, http in, http response
  - [x] Aprender a importar/exportar flujos (JSON)

- [x] **Crear el bot de Telegram**
  - [x] Hablar con [@BotFather](https://t.me/BotFather) para crear el bot
  - [x] Guardar el token del bot de forma segura
  - [x] Instalar nodo compatible con Telegram **Bot API** (`node-red-contrib-telegrambot`)
  - [x] Configurar el nodo Telegram con el token del bot
  - [x] Probar envío/recepción de mensajes básicos

- [x] **Diseñar el flujo de pedidos y Mini App (Web App)**
  - [x] Prototipar lectura de chat por regex básico (`/mesa\s*(\d+)/i`) y botones Inline Keyboards (`callback_query`)
  - [x] Evaluar y descartar Inline Keyboards por conflictos de caché en el nodo (`10-function.js setup`) y refresco continuo de mensajes
  - [x] Desarrollar **Telegram Mini App (Web App)** servida desde Node-RED (`GET /carta_app`) con catálogo interactivo HTML/CSS/JS, botones `+`/`-`, cálculo de precios y carrito flotante
  - [x] Configurar túnel seguro HTTPS con **Ngrok** apuntando al puerto `1880` (requisito de Telegram Web Apps)
  - [x] Sistema de códigos QR y asignación de mesas mediante Deep Links de Telegram (`/start MESA`) propagados como parámetro URL (`?mesa=X`)
  - [x] Endpoint backend (`POST /recibir_pedido`) para procesar el payload JSON de la comanda y enviar confirmación al cliente por Telegram
  - [x] Persistir pedidos en base de datos **SQLite** (`bar.db`, tabla `pedidos`) con estado `pendiente`
  - [ ] Robustecer control de duplicados e idempotencia

- [ ] **Dashboard de monitorización / Cocina**
  - [ ] Crear interfaz gráfica en Node-RED Dashboard para que empleados de cocina/barra visualicen pedidos de `bar.db`
  - [ ] Implementar botón de "Pedido Listo" para marcar comandas y disparar el robot

- [ ] **Conectar Node-RED con ROS 2**
  - [ ] Conectar el botón de "Pedido Listo" del Dashboard con la lógica de navegación (Nav2 / rosbridge)
  - [ ] Ejecutar `rosbridge_suite` en el grafo ROS 2 Humble del robot y comprobar disponibilidad de sus operaciones de acción
  - [ ] Configurar WebSocket `ws://<IP-ROSbot>:9090`, alcance de red y controles de acceso
  - [ ] Probar desde Node-RED lectura de estado ROS y goal de navegación supervisado
  - [ ] Crear catálogo mesa→pose `{x, y, yaw}` en `map`, con ubicaciones levantadas en RViz y ensayadas
  - [ ] Enviar goals a Nav2 `NavigateToPose`; procesar aceptación, feedback, resultado, cancelación y timeout
  - [ ] Mantener `/cmd_vel` fuera del flujo de pedidos; utilizarlo solo para teleoperación supervisada

- [ ] **Validar el servicio de camarero de forma progresiva**
  - [ ] Construir/cargar mapa de restaurante y validar pose inicial/localización
  - [ ] Probar robot vacío y velocidad reducida con supervisión y paro físico accesible
  - [ ] Ensayar pérdida de Wi-Fi, reinicios, mesa inaccesible, cancelación y pedidos repetidos
  - [ ] Confirmar llegada y entrega con interacción del cliente o personal; no marcar entregado solo por llegar
  - [ ] Probar primero con carga inerte y luego con el servicio real

## 📝 Notas

### Registro de Avances: Sistema de Recepción - Robot Camarero (2026-10-22)

#### 1. Configuración de Base de Datos (SQLite)
* **Hito:** Se ha integrado correctamente el nodo SQLite en Node-RED.
* **Archivo:** `bar.db`
* **Estructura:** Se ha automatizado la creación de la tabla de comandas utilizando la siguiente consulta SQL al arrancar el flujo:
  ```sql
  CREATE TABLE IF NOT EXISTS pedidos (
      id INTEGER PRIMARY KEY AUTOINCREMENT, 
      mesa TEXT, 
      comanda TEXT, 
      estado TEXT DEFAULT 'pendiente'
  );
  ```

#### 2. Evolución de la Interfaz en Telegram
El sistema ha iterado por tres fases para mejorar la experiencia de usuario:
1. **Lectura de chat:** Regex básico (`/mesa\s*(\d+)/i`) para extraer pedidos escritos manualmente.
2. **Botones Integrados (Inline Keyboards):** Uso de `callback_query`. *Nota técnica:* Se descartó debido a conflictos de caché en el nodo de Telegram (error persistente en `10-function.js setup`) y a la necesidad de actualizar el mensaje constantemente para crear un "carrito".
3. **Telegram Mini Apps (Web Apps) - [VERSIÓN FINAL]:** Se optó por servir una aplicación web en HTML/JS directamente desde Node-RED hacia la interfaz nativa de Telegram.

#### 3. Arquitectura de la Mini App (Web App)
Se ha convertido Node-RED en un servidor web mediante los nodos `http in` y `http response`.
* **Endpoint del Front-end (`GET /carta_app`):** Sirve un diseño en HTML/CSS/JS con el menú del restaurante.
  * *Funcionalidades:* Botones de incremento/decremento (`+`/`-`), cálculo automático del precio total, carrito interactivo y botón flotante de envío a cocina.
* **Endpoint del Back-end (`POST /recibir_pedido`):** Recibe el payload JSON desde la Mini App cuando el usuario pulsa "Enviar a cocina", inserta los datos en SQLite y ordena al bot de Telegram que envíe un mensaje de confirmación al chat del cliente.

#### 4. Enlace Seguro y Túneles (Ngrok)
* Para cumplir con el requisito de Telegram de usar `HTTPS` en las Web Apps, se ha configurado **Ngrok** apuntando al puerto local `1880`.
* **URL Actual de trabajo:** `https://unglazed-record-pedigree.ngrok-free.dev`
* *Observación:* Se resolvieron los errores de autenticación (`ERR_NGROK_105`) configurando correctamente el Authtoken, y el error de host caído (`ERR_NGROK_3200`) actualizando la URL dinámica en el nodo Function de Node-RED.

#### 5. Sistema de Códigos QR y Asignación de Mesas
* **Generación:** Se utilizan enlaces Deep Link nativos de Telegram con el formato `https://t.me/NOMBRE_BOT?start=NUMERO_MESA`.
* **Captura en Node-RED:** El nodo receptor lee el texto `/start X`.
* **Inyección a la Web App:** El número de mesa se inyecta dinámicamente como parámetro en la URL de Ngrok (`?mesa=X`), permitiendo que el Front-end (HTML) lo lea mediante `URLSearchParams` y asigne el pedido a la mesa correcta de forma 100% autónoma.

#### 6. Próximos Pasos (Pendiente)
1. **Dashboard de Cocina/Barra:** Crear la interfaz gráfica en Node-RED Dashboard para que los empleados visualicen los registros insertados en `bar.db`, permitiendo marcar los pedidos como "Listos".
2. **Despacho del Robot:** Conectar el botón de "Pedido Listo" del Dashboard con la lógica de navegación (Nav2 / rosbridge) para enviar al robot Husarion a la mesa correspondiente.

---

### Decisiones de arquitectura previas (2026-10-22)

- El uso final es robot camarero: los clientes piden comida a una mesa mediante bot Telegram; Node-RED valida/orquesta y manda una pose de mesa a Nav2. El robot comunica llegada y la entrega requiere confirmación explícita.
- Node-RED se plantea en un contenedor aparte en laptop/PC, con `/data` persistente. No instalar ROS en ese contenedor para esta integración.
- Conectar con WebSocket rosbridge ejecutado en el grafo ROS 2 Humble del robot. Antes de diseñar el flujo final, verificar soporte de acciones en la versión concreta de rosbridge; el protocolo ROS 2 documenta goals, feedback, resultados y cancelación.
- Para desplegar cambios del stack oficial en el robot, la documentación del submódulo recomienda `just sync <host>` (rsync y vigilancia de archivos); no hace falta hacer `git pull` del robot en cada edición. Revisar el `.env` y requisitos del equipo antes de ejecutar `just start-rosbot`.
- El nodo de Telegram debe usar Telegram Bot API; el paquete llamado `node-red-node-telegrambot` puede ser un userbot basado en cuenta personal y no es equivalente.

Referencias:
- [Node-RED en Docker y persistencia](https://nodered.org/docs/getting-started/docker)
- [Nodo de Telegram Bot API](https://flows.nodered.org/node/node-red-contrib-telegrambot)
- [Protocolo rosbridge ROS 2](https://github.com/RobotWebTools/rosbridge_suite/blob/ros2/ROSBRIDGE_PROTOCOL.md)
- [Nav2: acciones ROS 2](https://docs.nav2.org/jazzy/getting_started/navigation_concepts/ros2.html)
- [Stack oficial rosbot-autonomy](https://github.com/husarion/rosbot-autonomy/tree/ros2router)
