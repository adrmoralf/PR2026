# 🧑‍💻 Manu — Notas personales

## 🎯 Tarea principal

**Configuración de Node-RED como orquestador del sistema + integración con Telegram**

## 📋 Subtareas

- [ ] **Instalar Node-RED**
  - [ ] Instalar Node.js (v18 LTS o superior)
  - [ ] Instalar Node-RED globalmente (`npm install -g node-red`)
  - [ ] Arrancar Node-RED y acceder al editor en `http://localhost:1880`

- [ ] **Aprender los fundamentos de Node-RED**
  - [ ] Entender el concepto de nodos, flujos y mensajes (`msg.payload`)
  - [ ] Practicar con nodos básicos: inject, debug, function, switch
  - [ ] Aprender a importar/exportar flujos (JSON)

- [ ] **Crear el bot de Telegram**
  - [ ] Hablar con [@BotFather](https://t.me/BotFather) para crear el bot
  - [ ] Guardar el token del bot de forma segura
  - [ ] Instalar el nodo `node-red-contrib-telegrambot` desde el editor
  - [ ] Configurar el nodo Telegram con el token del bot
  - [ ] Probar envío/recepción de mensajes básicos

- [ ] **Diseñar el flujo de pedidos**
  - [ ] Definir los comandos del bot (ej: `/pedir`, `/menu`, `/estado`)
  - [ ] Crear un flujo que reciba un pedido y lo procese
  - [ ] Asignar cada pedido a un número de mesa
  - [ ] Gestionar cola de pedidos (si hay varios pedidos simultáneos)
  - [ ] Enviar confirmación al cliente por Telegram

- [ ] **Conectar Node-RED con ROS2**
  - [ ] Investigar opciones: `rosbridge_websocket` + nodo WebSocket en Node-RED, o MQTT bridge
  - [ ] Instalar `rosbridge_suite` para la distribución ROS 2 acordada con Adri
  - [ ] Crear un flujo que envíe goals de navegación al robot cuando llegue un pedido
  - [ ] Probar el envío de un waypoint (coordenadas de mesa) desde Node-RED

- [ ] **Dashboard de monitorización (opcional)**
  - [ ] Instalar `node-red-dashboard` para crear un panel web
  - [ ] Mostrar estado del robot, pedidos pendientes y entregas completadas

## 📝 Notas

_(Apunta aquí lo que vayas descubriendo, problemas, soluciones, etc.)_

