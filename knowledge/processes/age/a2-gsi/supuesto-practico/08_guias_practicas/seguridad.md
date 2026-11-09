---
title: Medidas de seguridad (ENS RD 311/2022)
---

## Valoración del sistema

Usar **RD 311/2022 Anexo I** y la guía **CCN-STIC-803**.

**1.** Valorar los criterios de la siguiente tabla haciéndose la pregunta
*¿Qué consecuencias tendría...*
por cada dimensión (la respuesta será una de las celdas de la tabla o *no aplica*):

* **Confidencialidad:** ...la revelación de información a personas no autorizadas?
* **Integridad:** ...la modificación de información por alguien no autorizado?
* **Trazabilidad:** ...no poder comprobar a posteriori quién ha accedido o modificado cierta información?
* **Autenticidad:** ...que la información no fuera auténtica (suplantación)?
* **Disponibilidad:** ...que una persona o sistema autorizado no pudiera usar el servicio?

| Criterio           | < | BAJO | MEDIO | ALTO |
|:-|:-|:-|:-|:-|
| **Perjuicio directo al ciudadano** | < | alguno | importante pero subsanable | grave, de difícil o imposible reparación |
| **Incumplimiento<br/>de una norma** | **legal/administrativa** | leve subsanable | material o formal no subsanable | material y formal grave |
| ^ | **regulatoria** | incumplimiento | sanción significativa | sanción grave y/o pérdida de licencia para operar |
| ^ | **contractual** | formal leve | material o formal | material o formal grave |
| ^ | **interna** | ^ | ^ | ^ |
| **Pérdidas económicas** | < | < 4% presupuesto anual | del 4% al 10% | > 10% |
| **Reputación (daño)** | < | moderado | significativo | grave |
| **Protestas** | < | individuales | públicas | masivas |
| **Delitos** | < | favorecería el delito | favorecería significativamente o<br/>dificultaría su investigación| incitaría al delito, es un delito en sí o<br/>dificultaría enormemente su investigación |



**2.** Valorar la dimensión **disponibilidad** según RTO (Recovery Time Objective):

* si RTO > 5 días: N/A
* si RTO <= 5 días: BAJO
* si RTO <= 1 día: MEDIO
* si RTO <= 4 horas: ALTO

Con ello rellenamos la tabla de valoración final:

| Activo | Tipo        | C | I | T | A | D |
|--------|-------------|---|---|---|---|---|
| Ej 1   | servicio    |   |   |   |   |   |
| Ej 2   | información |   |   |   |   |   |
| **Valor máximo (Categoría del Sistema)** | < |   |   |   |   |   |

---

## Medidas de seguridad (Anexo II - RD 311/2022)

Se usará el **RD 311/2022 Anexo II** y la guía **CCN-STIC-804**. El ENS establece un modelo basado en un **Requisito Base** de obligado cumplimiento para cada medida, al que se le suman **Refuerzos (+R1, +R2, +R3...)** proporcionales a la categoría del sistema (Básica, Media o Alta). Para los datos de carácter personal se aplicará el RGPD y la LOPD-GDD (realizando Evaluación de Impacto - Art 35 RGPD - si corresponde).

### 1. Marco Organizativo `[org]`

1. `[org.1]` **Política de seguridad de la información:** Incluir el sistema dentro de la política formalmente aprobada por el organismo (CCN-STIC-805).
2. `[org.4]` **Autorización del sistema:** Establecer un proceso formal de autorización para la entrada en operación que cubra todos los elementos del sistema.

### 2. Marco Operacional `[op]`

1. `[op.pl.1]` **Análisis de riesgos:** Base metodológica continua. Requisito Base (Informal para BAJO) + Refuerzos para análisis semiformal (MEDIO) o formal con herramientas GRC como PILAR (ALTO).
2. `[op.acc.1 AT]` **Identificación:** Definir controles que permitan saber quién accede, qué derechos recibe y registrar de forma inequívoca su actividad. Las cuentas deben deshabilitarse ante ceses o revocaciones.
3. `[op.acc.2 ICAT]` **Requisitos de acceso:** Principio de mínimo privilegio y necesidad de conocer. Garantizar que únicamente personas o sistemas autorizados interactúan con el sistema.
4. `[op.acc.5 ICAT]` **Mecanismo de autenticación (Alineado con eIDAS):**
    * **BAJO:** Un solo factor (contraseña robusta). Reglas básicas de calidad.
    * **MEDIO:** Autenticación de doble factor (MFA) o nivel *Sustancial* eIDAS (Ej: login/password + OTP, o Certificado SW).
    * **ALTO:** Múltiples factores con credenciales de nivel *Alto* eIDAS. Requiere registro presencial/telemático cualificado y uso de elementos criptográficos HW (Ej: DNIe, tarjeta criptográfica).
5. `[op.exp.1]` **Inventario de activos:** Detallar naturaleza, valor e identificar al responsable de cada activo del sistema.
6. `[op.exp.6]` **Protección frente a código dañino:** Despliegue de sistemas antimalware, monitorización de puntos de entrada/salida y firewalls.
7. `[op.exp.8 T]` **Registro de la actividad:** Trazabilidad de *qué*, *quién*, *cuándo* y éxito/fracaso.
    * **BAJO ->** Registros locales básicos en los servidores.
    * **MEDIO ->** Revisión y centralización de registros.
    * **ALTO ->** Recolección automática, custodia segura y **correlación de eventos** (SIEM).
8. `[op.nub.1]` **Protección de servicios en la nube:** Aplicación de controles específicos para la provisión y consumo de servicios Cloud (públicos, privados o híbridos).
9. `[op.ext.3]` **Protección de la cadena de suministro:** Exigencia de garantías de seguridad y cumplimiento del ENS a los proveedores tecnológicos y terceros que dan soporte al sistema.

#### Medidas adicionales para categoría MEDIA (Requieren Refuerzos +R):

1. `[op.exp.5]` **Gestión de cambios:** Evitar modificaciones no controladas en producción. Separación de entornos.
2. `[op.exp.7]` **Gestión de Incidentes:** Obligación de reportar incidentes al CCN-CERT. Registro de evidencias forenses y cadena de custodia legal.
3. `[op.acc.3 ICAT]` **Segregación de funciones y tareas:** Separación mediante controles lógicos de tareas incompatibles (ej: desarrollo y producción, o auditoría y administración).
4. `[op.mon.1]` **Detección de intrusión:** Uso de sistemas de detección/prevención de intrusiones (IDS/IPS) para monitorizar el sistema.

#### Medidas adicionales para categoría ALTA (Refuerzos Máximos):

1. `[op.pl.5]` **Componentes certificados:** Uso obligatorio de productos cuyas funcionalidades de seguridad hayan sido certificadas (Common Criteria) o incluidas en el Catálogo CPSTIC del CCN.
2. `[op.cont.2]` **Plan de Continuidad:** Integración obligatoria en el Plan de Continuidad de Negocio (BCP) y Plan de Recuperación ante Desastres (DRP) del Organismo.
3. `[op.exp.10 T]` **Protección de registros de actividad:** Garantizar que los logs no puedan ser alterados ni siquiera por los administradores del sistema (WORM, envíos directos al SIEM aislados).

### 3. Medidas de Protección `[mp]`

1. `[mp.if.1]` **Protección de instalaciones:** Áreas separadas y con control de acceso físico riguroso.
2. `[mp.per.3]` **Concienciación:** Formación continua del personal en ciberseguridad.
3. `[mp.com.1]` **Perímetro seguro:** Uso de cortafuegos (en **ALTA** serán de distintos fabricantes en cascada y alta disponibilidad).
4. `[mp.info.1]` **Datos de carácter personal:** Cumplimiento estricto del RGPD y LOPD-GDD.
5. `[mp.info.9 D]` **Copias de seguridad:** Políticas de retención, cifrado y pruebas de restauración periódicas.

#### Por categoría MEDIA:

1. `[mp.com.2 C]` **Protección de la confidencialidad (Comunicaciones):** Uso de túneles VPN IPSec/SSL para comunicaciones por redes no confiables. En **ALTA** se usarán preferentemente dispositivos criptográficos HW (cifradores).
2. `[mp.sw.1]` **Desarrollo de aplicaciones:** Entornos separados (Desarrollo, Preproducción, Producción). Metodología de desarrollo seguro (DevSecOps) y revisión/auditoría de código antes del paso a producción.
3. `[mp.arq.1]` **Protección en la arquitectura:** (Nueva familia ENS) Aplicar principios de diseño seguro por defecto, alta disponibilidad y segregación funcional.

#### Para categoría ALTA:

1. `[mp.com.4]` **Segregación de redes:** Microsegmentación, DMZs y control estricto de los flujos de información (Zero Trust).
2. `[mp.com.9 D]` **Medios alternativos:** Líneas de comunicaciones de respaldo independientes.
3. `[mp.info.3 C]` **Cifrado de la información:** Datos cifrados en reposo y en tránsito.
4. `[mp.info.5 T]` **Sellos de tiempo:** Uso de sellos de tiempo cualificados para garantizar el no repudio.