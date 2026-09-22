# SUPUESTO RENTAWEB (AEAT) - VERSIÓN MAGISTRAL

**Enunciado:** Desarrollo de una aplicación móvil oficial para la gestión del IRPF, consulta de datos fiscales y presentación de declaraciones, alineada con la estrategia de lucha contra el fraude y asistencia al contribuyente.

---

## 1. DAFO + NORMATIVA APLICABLE

### 1.1. Introducción
El proyecto consiste en el desarrollo de una App móvil oficial. Al tratarse de un sistema público con autenticación fuerte y tratamiento de datos tributarios (Nivel ALTO), debe planificarse bajo el marco jurídico TIC de la Administración General del Estado.

### 1.2. Análisis DAFO

| ANÁLISIS INTERNO (Organismo) | ANÁLISIS EXTERNO (Entorno) |
| :--- | :--- |
| **FORTALEZAS** | **OPORTUNIDADES** |
| - **Experiencia:** AEAT dispone de gran madurez en servicios telemáticos.<br>- **Reutilización:** Uso de plataformas corporativas (**Cl@ve, PID, @firma, INSIDE**).<br>- **Datos:** Disponibilidad de datos fiscales consolidados y fiables. | - **Canal Móvil:** Elevada penetración de smartphones $\rightarrow$ Maximiza la asistencia.<br>- **Eficiencia:** Reducción de carga presencial y telefónica.<br>- **Impulso:** Alineación con España Digital 2026 y Plan de Recuperación. |
| **DEBILIDADES** | **AMENAZAS** |
| - **Complejidad:** Casuística fiscal variable según normativa autonómica.<br>- **Picos de Carga:** Alto volumen de accesos en campaña $\rightarrow$ Exige elasticidad. | - **Ciberamenazas:** Alto valor de los datos (Fraude, Phishing).<br>- **Reputación:** Impacto social muy elevado en caso de fallo.<br>- **Legislación:** Cambios normativos fiscales frecuentes. |

### 1.3. Normativa Aplicable (Magistral)
Durante el proyecto deben respetarse:

1.  **Gobernanza TIC:** **Ley 40/2015** (Arts. 156-158) sobre interoperabilidad y seguridad.
2.  **Interoperabilidad:** **ENI** (RD 4/2010) y sus NTI (Documento, Expediente, Firma).
3.  **Seguridad:** **ENS** (RD 311/2022) y Guías CCN-STIC (Serie 800). Categorización del sistema (ALTA).
4.  **Procedimiento:** **Ley 39/2015** (Arts. 14, 16, 41, 53) sobre derechos digitales, registro y notificaciones.
5.  **Identidad y Firma:** **eIDAS** y Ley 6/2020.
6.  **Protección de Datos:** **RGPD + LOPDGDD**. Base legitimadora: Misión pública (Art. 6.1.e) y EIPD obligatoria.
7.  **Accesibilidad:** **RD 1112/2018** (App accesible WCAG 2.1).

---

## 2. DIAGRAMA DE CASOS DE USO (CIUDADANO)

### 2.1. Introducción
Se representa únicamente la interacción del **Ciudadano** con la App RentaWeb. Los servicios corporativos se utilizan pero no se modelan como actores primarios.

### 2.2. Actores
* **Ciudadano** (Actor Principal).

### 2.3. Casos de Uso Principales

* **Autenticación:**
    * `Iniciar Sesión` (Vía Cl@ve PIN/Permanente).
    * `Acceso Biométrico` (Huella/Facial local).
    * `Verificar Identidad` (Dato contraste: Casilla 505).
* **Gestión Tributaria:**
    * `Consultar Borrador`.
    * `Modificar Borrador`.
    * `Confirmar y Presentar` (Genera asiento registral).
    * `Descargar PDF` (Justificante con CSV).
    * `Añadir Cónyuge`.
* **Servicios Públicos (Sin registro):**
    * `Buscar Oficinas` (GPS).
    * `Cotejar CSV`.
* **Notificaciones:**
    * `Suscribirse a Avisos Push`.
* **Cita Previa:**
    * `Solicitar Cita`.
    * `Guardar en Calendario`.

---

## 3. DIAGRAMA DE CLASES (DOMINIO)

### 3.1. Introducción
El modelo refleja el núcleo del sistema tributario, utilizando entidades administrativas habituales y coherentes con el ENI.

### 3.2. Clases del Dominio

* **Contribuyente:** `NIF`, `Nombre`, `DomicilioFiscal`, `IBAN`.
    * *Relación:* 1 $\rightarrow$ N Declaraciones.
* **Expediente:** `IDExpediente`, `Ejercicio`, `Estado` (Abierto/Cerrado), `FechaInicio`.
    * *Relación:* Composición con Documentos.
* **Documento (Abstracta):** `IDDocumento`, `Tipo`, `CSV`, `FechaGeneración`.
    * **Declaración (Subclase):** `Ejercicio`, `Resultado` (Devolver/Pagar), `Estado`.
    * **Borrador (Subclase):** `Tipo` (PropuestoAEAT / ModificadoUsuario).
* **Notificación:** `Tipo` (Push), `Fecha`, `Leída`.
* **Cita:** `FechaHora`, `Oficina`.

* **Regla de Negocio:** Una Declaración puede tener asociados máximo 2 borradores (Original y Modificado).

---

## 4. TECNOLOGÍA DE DESARROLLO + PERMISOS

### 4.1. Análisis de Alternativas
* **Nativa (Kotlin/Swift):** Máximo rendimiento, acceso directo y seguro al hardware criptográfico y biometría. Mayor coste de desarrollo.
* **Multiplataforma (Flutter/React):** Código compartido. Dependencia de *plugins* para acceder al hardware, lo que introduce vectores de ataque en la cadena de suministro de software.
* **Híbrida/PWA:** Descartadas por rendimiento insuficiente y falta de acceso robusto a elementos seguros del dispositivo.

### 4.2. Alternativa Seleccionada: Desarrollo Nativo
Se opta por el desarrollo **Nativo** (Kotlin para Android y Swift para iOS).

**Justificación de Seguridad (ENS Nivel ALTO):**
Dado que el sistema trata **datos tributarios** (confidencialidad Alta) y utiliza **biometría** para la autenticación, la seguridad es el factor crítico de decisión:

1.  **Seguridad por Diseño:** El desarrollo nativo elimina las capas intermedias (puentes o *bridges* de los frameworks híbridos), reduciendo la superficie de ataque.
2.  **Protección de Datos Especiales:** Permite el uso directo de los almacenes seguros de claves del hardware (**Secure Enclave** en iOS y **Trusted Execution Environment** en Android) sin intermediarios, garantizando que los datos biométricos nunca salen del entorno seguro del procesador.
3.  **Experiencia de Usuario (UX):** Garantiza la máxima fluidez y estabilidad en momentos de carga crítica (Campaña de la Renta), minimizando incidencias técnicas.

### 4.3. Permisos Necesarios (Minimización RGPD)
| Permiso | Justificación |
| :--- | :--- |
| **Biometría** | Uso de la API nativa (`BiometricPrompt` / `LocalAuthentication`) para acceso seguro. |
| **Calendario** | Solo si el usuario decide guardar la cita previa (Write-only). |
| **Ubicación** | Permiso de ubicación aproximada (*Coarse*) solo al usar el buscador de oficinas. |
| **Cámara** | Acceso efímero para escanear el CSV de documentos. |
| **Notificaciones** | Enviar avisos de estado (requiere consentimiento explícito desde Android 13/iOS). |

*(No se solicitan permisos de Contactos, SMS o Registro de Llamadas, cumpliendo el principio de Minimización del RGPD).*

---

## 5. SEGURIDAD (LÓGICA + FÍSICA ENS)

### 5.1. Introducción
El sistema se clasifica como **Nivel ALTO** (ENS) debido a la naturaleza sensible de los datos tributarios y el impacto social.

### 5.2. Seguridad Lógica (Aplicación)

* **Autenticación:** Cl@ve (Federada) + Biometría local.
* **Cifrado:** Extremo a extremo.
    * Tránsito: **TLS 1.3** con *Certificate Pinning*.
    * Reposo: **AES-256** para datos sensibles en servidor.
* **Trazabilidad:** Registro de auditoría completo (quién hizo qué) conforme a Ley 40/2015.
* **Integridad App:** Detección de *Root/Jailbreak* y ofuscación de código.
* **Protección Web:** API Gateway + WAF (Anti-inyección, Rate Limiting).

### 5.3. Seguridad Física (CPD)
Alojamiento en Nube SARA o CPD Tier III propio.

* **Acceso:** Control biométrico, CCTV y registro de entrada.
* **Disponibilidad:** Climatización redundada, SAIs y Grupos Electrógenos.
* **Incendios:** Detección precoz y extinción por gas (agente limpio).
* **Respaldo:** CPD secundario (Disaster Recovery).

### 5.4. Continuidad
Plan de Continuidad de Negocio (PCN) probado, con réplicas síncronas y monitorización 24x7.

---

## 6. CONCLUSIÓN

> *"El desarrollo de RentaWeb es plenamente viable, apoyándose en los servicios comunes de la AGE y cumpliendo estrictamente con ENS, ENI, Ley 39/40 y RGPD. El sistema proporciona mayor asistencia al ciudadano, mejora la eficiencia pública y reduce el fraude gracias a los controles automatizados."*