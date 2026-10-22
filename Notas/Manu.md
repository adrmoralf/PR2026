# 🧑‍💻 Manu — Notas personales

## 🎯 Tarea principal

**Configuración de Node-RED como orquestador del sistema + integración con Telegram**

## 📋 Subtareas

- [ ] **Instalar Node-RED**
  - [ ] Desplegarlo como contenedor independiente en laptop/PC con volumen persistente para `/data` y puerto `1880`
  - [ ] Configurar acceso al editor; no exponerlo públicamente sin autenticación

- [ ] **Aprender los fundamentos de Node-RED**
  - [ ] Entender el concepto de nodos, flujos y mensajes (`msg.payload`)
  - [ ] Practicar con nodos básicos: inject, debug, function, switch
  - [ ] Aprender a importar/exportar flujos (JSON)

- [ ] **Crear el bot de Telegram**
  - [ ] Hablar con [@BotFather](https://t.me/BotFather) para crear el bot
  - [ ] Guardar el token del bot de forma segura
  - [ ] Instalar un nodo compatible con Telegram **Bot API** (por ejemplo, `node-red-contrib-telegrambot`; evitar confundirlo con nodos de userbot/cuenta personal)
  - [ ] Configurar el nodo Telegram con el token del bot
  - [ ] Probar envío/recepción de mensajes básicos

- [ ] **Diseñar el flujo de pedidos**
  - [ ] Definir interacción guiada (menú, selección de mesa/productos, revisar y confirmar pedido)
  - [ ] Autorizar chat/usuario y validar mesa/productos contra una lista cerrada
  - [ ] Crear ID único por pedido y evitar duplicados por reintentos/reinicio
  - [ ] Persistir pedidos y estados (`recibido`, `pendiente`, `en_camino`, `llegado`, `entregado`, `cancelado`, `error`)
  - [ ] Empezar con cola FIFO y definir robot ocupado, cancelación, fallo, pérdida de red y vuelta a cocina/espera
  - [ ] Diferenciar confirmación de recepción, llegada del robot y entrega confirmada

- [ ] **Conectar Node-RED con ROS 2**
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

- [ ] **Dashboard de monitorización (opcional)**
  - [ ] Instalar `node-red-dashboard` para crear un panel web
  - [ ] Mostrar estado del robot, pedidos pendientes y entregas completadas

## 📝 Notas

### Decisiones de arquitectura (2026-10-22)

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

