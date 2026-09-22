# GESTIÓN DE RIESGOS (MAGERIT v3)

El **ENS** obliga a realizar un análisis de riesgos regular. La metodología oficial de la AGE para esto es **MAGERIT v3** (y su herramienta **PILAR**).

---

## 1. CONCEPTOS CLAVE (VOCABULARIO TÉCNICO)

Para responder con propiedad, usa estos términos:

* **Activo:** Cualquier recurso del sistema necesario para que funcione (Datos, Servidores, Personal, Instalaciones).
* **Amenaza:** Causa potencial de un incidente que puede dañar un activo.
* **Vulnerabilidad:** Debilidad del sistema que permite que la amenaza se materialice.
* **Impacto:** Daño producido si la amenaza ocurre.
* **Riesgo:** Probabilidad x Impacto.

---

## 2. CATÁLOGO DE RIESGOS TÍPICOS (AMENAZAS)

En un supuesto práctico, identifica siempre estos riesgos según el tipo de activo:

| Tipo de Amenaza | Ejemplo en el Supuesto | Activo Afectado |
| :--- | :--- | :--- |
| **Desastres Naturales** | Incendio, Inundación, Corte eléctrico. | CPD, Servidores (Disponibilidad). |
| **Ataques Intencionados** | Inyección SQL, DDoS, Ransomware. | Datos, Web (Confidencialidad/Integridad). |
| **Errores Humanos** | Borrado accidental, mala configuración. | Datos (Integridad). |
| **Fallos Técnicos** | Rotura de disco duro, caída de red. | Servidores (Disponibilidad). |

---

## 3. CÓMO MINIMIZAR LOS RIESGOS (SALVAGUARDAS)

La respuesta a *"¿Cómo minimizar los riesgos?"* es proponer **Salvaguardas** (Medidas de Seguridad).

| Riesgo Identificado | Medida para Minimizarlo (Salvaguarda) |
| :--- | :--- |
| **Pérdida de Datos** (Incendio/Ransomware) | **Copias de Seguridad (Backup):** Estrategia 3-2-1 y almacenamiento en **Archive**. |
| **Caída del Servicio** (Corte eléctrico) | **Continuidad:** SAIs redundantes y Grupo Electrógeno. |
| **Acceso no autorizado** (Hacker) | **Prevención:** Firewall Perimetral y WAF. **Autenticación:** Cl@ve / Doble Factor. |
| **Fuga de Información** (Empleado desleal) | **DLP (Data Loss Prevention):** Herramientas de control de salida de datos y **Trazabilidad** (Logs). |

---

## 4. GESTIÓN DEL RIESGO RESIDUAL

Nunca se elimina el riesgo al 100%.

* **Riesgo Residual:** El riesgo que queda después de aplicar las salvaguardas. Este riesgo debe ser **aceptado** por la Dirección (Responsable de la Información).

---