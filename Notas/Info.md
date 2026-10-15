# 📋 Información del Proyecto — PR2026

## Descripción

Proyecto de robótica inspirado en los **restaurantes de sushi con gatos robot** 🐱🍣. El objetivo es desarrollar un robot camarero autónomo capaz de llevar platos desde la cocina hasta las mesas de los clientes.

- **Robot:** ROSbot 2R (Husarion) — plataforma con LiDAR, IMU y cámaras para navegación autónoma.
- **Automatización:** Node-RED como orquestador central para gestionar la lógica de pedidos, rutas y estado del robot.
- **Pedidos:** Los clientes (cada integrante con su móvil) hacen pedidos a través de un **bot de Telegram**, que se comunica con Node-RED.

### Flujo general

```
Cliente (Telegram) → Bot Telegram → Node-RED → ROSbot 2R (ROS2) → Entrega en mesa
```

## 👥 Integrantes

| Nombre | Archivo de notas |
|--------|-----------------|
| Adri   | [Adri.md](Adri.md) |
| Manu   | [Manu.md](Manu.md) |
| Rubén  | [Ruben.md](Ruben.md) |
| Irene  | [Irene.md](Irene.md) |

## 🎯 Objetivos

1. Configurar y poner en marcha el **ROSbot 2R** con ROS2.
2. Implementar **navegación autónoma** (SLAM, localización, planificación de rutas) para que el robot se desplace entre cocina y mesas.
3. Crear un **bot de Telegram** para que los clientes hagan pedidos desde su móvil.
4. Desarrollar flujos en **Node-RED** que conecten los pedidos de Telegram con las órdenes de movimiento del robot.
5. Definir un **mapa del restaurante** con las posiciones de las mesas y la cocina.
6. Integrar todo el sistema: pedido → procesamiento → navegación → entrega.
7. Documentar todo el proceso y errores encontrados.

## 🗓️ Entregas

| Entrega | Fecha límite | Descripción | Estado |
|---------|-------------|-------------|--------|
| _Pendiente de definir_ | — | — | ⬜ |

> **Nota:** Actualizar esta tabla a medida que se conozcan las fechas y requisitos de cada entrega.

## 🛠️ Tecnologías

| Componente | Tecnología |
|------------|-----------|
| **Robot** | ROSbot 2R (Husarion) |
| **Framework robótico** | ROS2 Humble |
| **Navegación** | Nav2 (Navigation Stack 2) |
| **Automatización / Orquestador** | Node-RED |
| **Interfaz de pedidos** | Bot de Telegram |
| **Lenguajes** | Python / C++ (ROS2), JavaScript (Node-RED) |
| **SO** | Ubuntu (Linux) |

## 📂 Estructura del Repositorio

```
PR2026/
├── Notas/
│   ├── Adri.md        # Notas personales de Adri
│   ├── Manu.md        # Notas personales de Manu
│   ├── Ruben.md       # Notas personales de Rubén
│   ├── Irene.md       # Notas personales de Irene
│   ├── errores.md     # Registro de errores
│   ├── diario.md      # Diario de desarrollo
│   └── Info.md        # Este archivo
└── (código fuente por crear)
```

## 🔗 Recursos Útiles

- [ROSbot 2R — Quick Start (Husarion)](https://husarion.com/tutorials/howtostart/rosbot2r-quick-start/)
- [Documentación ROS2 Humble](https://docs.ros.org/en/humble/)
- [Nav2 — Navigation Stack 2](https://docs.nav2.org/)
- [Node-RED](https://nodered.org/docs/)
- [Node-RED Telegram (node-red-contrib-telegrambot)](https://flows.nodered.org/node/node-red-contrib-telegrambot)
- [Telegram Bot API](https://core.telegram.org/bots/api)

## 📝 Memoria del Proyecto

- [Memoria LaTeX (Overleaf)](https://www.overleaf.com/project/6ad0f3f618a8107fa81a76ec/share#dd594ebbde5234fac3de13eb5a6ef8c0eabac783d2ebbf31)
