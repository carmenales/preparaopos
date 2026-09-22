# 50. SEGURIDAD: CATEGORIZACIÓN ENS Y ANÁLISIS DE RIESGOS

El **Esquema Nacional de Seguridad (ENS)**, regulado por el **RD 311/2022**, es de obligado cumplimiento para todo el Sector Público. En el supuesto práctico, debes definir la categoría del sistema para saber qué medidas de seguridad aplicar.



[Image of ENS security dimensions and categorization process]


---

## 1. PASO 1: VALORACIÓN DE LAS DIMENSIONES (RIESGO)

Lo primero es valorar el impacto que tendría un incidente en la información y los servicios. Se analizan 5 dimensiones:

| Dimensión | Definición | Ejemplo de Impacto Alto |
| :--- | :--- | :--- |
| **Confidencialidad (C)** | Que nadie no autorizado vea los datos. | Fuga de datos de salud o violencia de género. |
| **Integridad (I)** | Que los datos no sean modificados. | Modificación de una cuenta bancaria en un pago o una sentencia. |
| **Disponibilidad (D)** | Que el sistema funcione cuando se necesita. | Caída de la Sede Electrónica el último día de plazo de una beca. |
| **Autenticidad (A)** | Garantizar quién hace qué. | Suplantación de identidad de un cargo público. |
| **Trazabilidad (T)** | Saber qué ha pasado (logs). | Imposibilidad de auditar quién accedió a un expediente sensible. |

**Niveles de Impacto:**

* **BAJO:** Perjuicio limitado. El servicio se recupera fácil.
* **MEDIO:** Perjuicio grave. El servicio tarda en recuperarse.
* **ALTO:** Perjuicio muy grave (seguridad pública, alarmas sociales).

---

## 2. PASO 2: DETERMINACIÓN DE LA CATEGORÍA DEL SISTEMA

La categoría del sistema se determina por el valor **más alto** de cualquiera de sus dimensiones (Principio de "el eslabón más fuerte marca la necesidad").

| Categoría | Criterio (Anexo I del ENS) | Ejemplo Típico |
| :--- | :--- | :--- |
| **BÁSICA** | Ninguna dimensión es superior a **BAJO**. | Portal informativo, intranet de noticias. |
| **MEDIA** | Al menos una dimensión es **MEDIA**, ninguna es ALTA. | Sede Electrónica estándar, Gestión de personal. |
| **ALTA** | Al menos una dimensión es **ALTA**. | Salud, Seguridad Ciudadana (Policía), Hacienda (Datos Tributarios). |

> **Regla de Oro para el Examen:** Ante la duda en un supuesto estándar de tramitación, suele ser categoría **MEDIA** (por la disponibilidad de la sede y la confidencialidad de datos personales básicos/medios). Si hay datos de SALUD o POLICÍA, es **ALTA**.

---

## 3. PASO 3: SELECCIÓN DE MEDIDAS DE SEGURIDAD (ANEXO II)

Una vez tienes la categoría, aplicas el **Anexo II** del RD 311/2022. No hace falta saberlas todas, pero sí citar las importantes en tu justificación.

### Medidas Clave a Citar (Toolkit de Examen):
1.  **Marco Organizativo [org]:**
    * Política de Seguridad aprobada.
    * Roles definidos (Responsable de la Información, del Servicio, de Seguridad).
2.  **Marco Operacional [op]:**
    * **[op.acc] Control de Acceso:** Identificación robusta (Cl@ve).
    * **[op.pl.2] Arquitectura de Seguridad:** Defensa en profundidad (DMZ, Firewalls).
    * **[op.mon] Monitorización:** Sondas SAT-INET del CCN.
3.  **Medidas de Protección [mp]:**
    * **[mp.info.2] Calificación de la Información:** Etiquetado de datos.
    * **[mp.com.2] Protección de Comunicaciones:** Uso de VPNs y TLS.
    * **[mp.si.3] Protección de Servidores:** Bastionado (Hardening) de los equipos.

---

## 4. PLANTILLA DE JUSTIFICACIÓN (TEXTO DE EXAMEN)

Usa esta plantilla para responder a la pregunta *"Analice la seguridad del sistema propuesto"*.

> "El sistema maneja datos de carácter personal y ofrece servicios electrónicos a los ciudadanos, por lo que se rige por el **RD 311/2022 (ENS)**.
>
> **1. Valoración:** Se identifican las dimensiones de seguridad. Dado que la interrupción del servicio afectaría a derechos de los ciudadanos, la **Disponibilidad** se valora como MEDIA. La **Confidencialidad** se valora como MEDIA (datos personales estándar).
>
> **2. Categorización:** Al tener dimensiones de nivel MEDIO y ninguna ALTA, el sistema se clasifica de categoría **MEDIA**.
>
> **3. Medidas de Seguridad:** Se aplicarán las medidas del **Anexo II** correspondientes a la categoría Media.
> * Se realizará un **Análisis de Riesgos** siguiendo la metodología **MAGERIT v3** (utilizando la herramienta PILAR).
> * Se implementará una defensa en profundidad (medida **op.pl.2**) con segmentación de redes y cortafuegos.
> * Se protegerán las comunicaciones (**mp.com.2**) mediante canales cifrados (HTTPS/TLS) y VPNs para administradores.
> * Se desplegarán herramientas de detección y respuesta (Sondas SAT-INET) integradas con el CCN-CERT."

---

## 5. RELACIÓN CON EL RGPD (PRIVACIDAD)

El ENS y el RGPD van de la mano.

* El **Análisis de Riesgos** del ENS sirve como base técnica para la seguridad que exige el RGPD.
* Si el riesgo para los derechos y libertades es alto, el RGPD exige una **EIPD (Evaluación de Impacto en Protección de Datos)**, que complementa al análisis de riesgos del ENS.

---