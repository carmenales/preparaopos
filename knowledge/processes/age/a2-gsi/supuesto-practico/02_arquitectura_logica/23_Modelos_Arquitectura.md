# MODELOS DE ARQUITECTURA: CAPAS VS MICROSERVICIOS

La elección del modelo arquitectónico define la escalabilidad y el mantenimiento del sistema. En el examen, debes justificar por qué eliges uno u otro.



[Image of comparison diagram Monolithic vs Microservices architecture]


---

## 1. ARQUITECTURA DE CAPAS (MONOLITO MODULAR)

Es el estándar tradicional y robusto para la mayoría de aplicaciones administrativas de tamaño medio.

### 1.1. Modelo de 3 Capas (Clásico)
1.  **Presentación:** Interfaz de Usuario (Web/App).
2.  **Negocio:** Reglas y procesos.
3.  **Datos:** Persistencia.

### 1.2. Modelo de 4 Capas (Moderno/AGE)

Se añade una capa para desacoplar la integración, vital en la administración electrónica.

4.  **Capa de Servicios / Integración:** Se sitúa entre Negocio y Datos (o transversal). Gestiona la comunicación con **Servicios Comunes** (Cl@ve, INSIDE) y APIs externas.

---

## 2. ARQUITECTURA DE MICROSERVICIOS

Enfoque distribuido donde la aplicación se divide en pequeños servicios autónomos.

### 2.1. Principios Clave
* **Descomposición:** Cada servicio tiene su propia lógica y **su propia base de datos** (BBDD descentralizada).
* **Comunicación:** Vía API REST o Bus de Eventos (Kafka/RabbitMQ).
* **API Gateway:** Punto único de entrada que gestiona la seguridad y el enrutamiento.

---

## 3. TABLA DE DECISIÓN (CRITERIO DE EXAMEN)

Usa esta tabla para justificar tu elección ante el tribunal.

| Criterio | Arquitectura de Capas (3/4) | Microservicios |
| :--- | :--- | :--- |
| **Complejidad** | Baja/Media. Fácil de desplegar y testear. | Alta. Requiere orquestación (Kubernetes) y monitorización compleja. |
| **Escalabilidad** | Limitada (se escala toda la aplicación). | **Excelente**. Se escala solo el servicio que lo necesita (ej. el módulo de firma). |
| **Equipos** | Ideal para equipos pequeños/medianos. | Ideal para equipos grandes distribuidos (cada equipo lleva un servicio). |
| **Datos** | Base de datos única (ACID fácil). | Datos distribuidos (Consistencia eventual). |

> **VEREDICTO EXPERTO:**
> 
> * **Elige 4 Capas** si el supuesto es un trámite administrativo estándar (solicitud, tramitación, resolución). Es más barato, rápido de desarrollar y fácil de mantener para un organismo medio.
> * **Elige Microservicios** si el sistema es crítico, masivo y requiere alta disponibilidad granular (ej. Sistema de Citas de Salud, Gestión de Aduanas) o si se espera una evolución constante de módulos independientes.

---