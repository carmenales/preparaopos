# DESARROLLO MÓVIL: NATIVA, HÍBRIDA Y PWA

La elección de la arquitectura móvil es una decisión crítica de diseño que debe basarse en el **presupuesto**, el **rendimiento** y la necesidad de acceso a **funcionalidades nativas** del dispositivo.

---

## 1. CLASIFICACIÓN Y ANÁLISIS COMPARATIVO



### 1.1. Apps Nativas
* **Características:** Desarrolladas con lenguajes propios (Kotlin/Java para Android; Swift/Objective-C para iOS).
* **Ventajas:** **Rendimiento óptimo**, acceso total y eficiente al hardware (GPS, cámara, biometría).
* **Desventajas (Criterio AGE):** **Alto coste** y **tiempo de desarrollo** (se necesitan dos bases de código), lo que dificulta la eficiencia.

### 1.2. Apps Híbridas
* **Características:** Usan tecnologías web (HTML/CSS/JS) envueltas en un contenedor nativo (**Apache Cordova** o **Capacitor**).
* **Ventajas:** **Menor coste** (una sola base de código), **fácil mantenimiento**. Permiten acceso a funciones nativas mediante plugins.
* **Desventajas:** **Rendimiento limitado** por la capa de abstracción (**WebView**).

### 1.3. Apps Web Progresivas (PWA)
* **Características:** Evolución de la Web App. Se ejecutan en el navegador, pero usan **Service Workers** para proporcionar funcionalidades nativas.
* **Ventajas (Clave para AGE):** **Distribución instantánea** (no pasa por tiendas de apps), **bajo coste**, **Modo Offline** (Service Workers) y **Notificaciones Push**.
* **Desventajas:** Acceso más limitado al hardware, rendimiento inferior a la Nativa.

---

## 2. PWA: EL MODELO DE EFICIENCIA PARA LA AGE

El modelo PWA es la opción más alineada con la **reutilización** y la **rapidez de despliegue** institucional.

| Característica de PWA | Justificación de Uso en la AGE |
| :--- | :--- |
| **Service Workers** | Permite **modo offline** y **sincronización de fondo** (ej. subir una solicitud cuando recupera la conexión). |
| **Instalación Directa** | No depende de las tiendas de apps (App Store / Google Play). Menos burocracia y **actualizaciones inmediatas**. |
| **Responsive Design** | Se adapta a cualquier dispositivo (móvil/tablet) con una sola base de código, optimizando recursos. |

---

## 3. CRITERIO DE ELECCIÓN EN EL SUPUESTO

Para justificar tu elección en el examen:

* **Elegir Nativa:** Solo si el requisito es un **rendimiento extremo** o el uso intensivo de un sensor (ej. un sistema de control de tráfico aéreo).
* **Elegir Híbrida (Cordova/React Native):** Si se requiere **acceso eficiente a biometría** (huella/facial) para la firma electrónica, sin asumir el coste de dos desarrollos nativos.
* **Elegir PWA:** Si el objetivo es la **difusión de información**, el **envío de alertas** (Notificaciones Push) o la **consulta de estado** (ej. Carpeta Ciudadana, Alertas Alimentarias) y se prioriza la **eficiencia en costes**.

---

## 4. ANÁLISIS DE FUNCIONALIDADES MÓVILES (REQUISITOS)

Si el supuesto pide diseñar una App (ej. Alertas Alimentarias o Ruraliza), justifica estas funcionalidades técnicas como Requisitos No Funcionales:

* **Notificaciones en Tiempo Real (Push):**
    * *Requisito:* Integración con servidores de notificaciones (FCM/APNs).
    * *Uso:* Alertas de seguridad inmediata (ej. "Producto retirado del mercado") o avisos de caducidad de trámites.
* **Geolocalización (GIS):**
    * *Requisito:* Acceso al GPS con gestión de permisos de privacidad.
    * *Uso:* Envío de alertas segmentadas por ubicación (ej. Solo a ciudadanos en una zona afectada) o localización de oficinas (**EGEO**).
* **Verificación de Productos (Cámara):**
    * *Requisito:* Acceso a la Cámara mediante API HTML5 o Plugin.
    * *Uso:* Funcionalidad de **escaneo de Código de Barras/QR** para verificar documentos (CSV) o consultar alertas de productos.
* **Biometría y Seguridad:**
    * *Requisito:* Acceso a sensores de Huella/FaceID.
    * *Uso:* Autenticación robusta para el acceso a la "Carpeta Ciudadana" sin introducir credenciales repetidamente.

---