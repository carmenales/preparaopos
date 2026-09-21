# Plantilla de Respuesta: Evaluación de Impacto en Protección de Datos (EIPD)

> **Uso en el examen:** Esta plantilla es aplicable cuando el supuesto incluya un sistema de información que trate datos personales con características de riesgo elevado. Adapta cada bloque al contexto concreto del enunciado.

---

## ¿Qué es una EIPD?

La **Evaluación de Impacto en la Protección de Datos (EIPD)** — también denominada *Data Protection Impact Assessment* (DPIA) — es un proceso de análisis previo obligatorio regulado en el **artículo 35 del Reglamento (UE) 2016/679 (RGPD)**. Su objetivo es identificar y minimizar los riesgos que un tratamiento de datos personales puede suponer para los derechos y libertades de los interesados, especialmente cuando se usan nuevas tecnologías o se procesan datos a gran escala.

No es un mero trámite documental: es una herramienta de **privacidad desde el diseño** (*privacy by design*), que debe influir en las decisiones técnicas y organizativas del sistema antes de su puesta en marcha.

---

## ¿Cuándo se realiza? (Momento)

La EIPD debe realizarse **antes del inicio del tratamiento**, no una vez que el sistema ya está desplegado. En el ciclo de vida de un proyecto TI, el momento idóneo es durante la fase de **Análisis del Sistema de Información (ASI)** o equivalente, cuando aún se pueden incorporar medidas sin coste desproporcionado.

Debe **revisarse y actualizarse** si se producen cambios significativos en el tratamiento: nuevas funcionalidades, nuevos datos tratados, cambios en destinatarios, cambio de tecnología (p.ej., incorporar IA donde antes no la había) o si una revisión periódica detecta que los riesgos han variado.

---

## ¿Cuándo es OBLIGATORIA? (Criterios de activación)

> ⚠️ **Importante:** No todo tratamiento de datos requiere EIPD, y no todo sistema con IA implica riesgo alto. La obligación se activa cuando el tratamiento **pueda suponer un alto riesgo** para los derechos y libertades de las personas.

El artículo 35 RGPD y las directrices del Comité Europeo de Protección de Datos (CEPD) establecen que es **preceptiva si concurren al menos dos** de los siguientes factores de riesgo:

| Factor de riesgo | Ejemplos aplicados a sistemas TI |
|---|---|
| **Evaluación o puntuación / elaboración de perfiles** | Scoring crediticio, análisis de comportamiento ciudadano, recomendaciones automatizadas |
| **Decisiones automatizadas con efectos significativos** | Resolución automática de solicitudes, concesión/denegación de ayudas sin intervención humana |
| **Observación sistemática** | Videovigilancia, monitorización de actividad en red, geolocalización continua |
| **Datos de categorías especiales (art. 9 RGPD)** | Salud, origen racial/étnico, ideología política, biometría, datos de menores |
| **Tratamiento a gran escala** | Sistemas que afectan a millones de ciudadanos (AEAT, SEPE, SNS...) |
| **Cruce o combinación de datos de múltiples fuentes** | Interoperabilidad entre sistemas de distintos organismos |
| **Datos de personas vulnerables** | Menores, personas mayores, colectivos en riesgo de exclusión |
| **Uso de nuevas tecnologías** | IA, reconocimiento facial, biometría, IoT, blockchain |
| **Transferencias internacionales fuera del EEE** | Uso de proveedores cloud extracomunitarios sin garantías adecuadas |

> **Regla práctica para el examen:** Si el supuesto incluye IA que toma o apoya decisiones sobre ciudadanos + trata datos a gran escala, la EIPD es casi siempre obligatoria. Si la IA es meramente auxiliar (p.ej., autocompletado de formularios sin decisión) y no concurren otros factores, puede no serlo. Justifica siempre tu decisión.

Adicionalmente, la **AEPD publica una lista de tratamientos que requieren EIPD** (art. 35.4 RGPD), entre los que se incluyen, entre otros: tratamientos biométricos para identificación, tratamientos de datos de salud a gran escala, y sistemas de puntuación o perfilado con efectos jurídicos.

---

## ¿Quién la realiza? ¿Quién es responsable?

| Rol | Función |
|---|---|
| **Responsable del tratamiento** | El organismo público que decide los fines y medios del tratamiento (p.ej., el Ministerio promotor del sistema). Es quien tiene la **obligación legal** de realizar la EIPD |
| **Delegado de Protección de Datos (DPD/DPO)** | Debe ser **consultado obligatoriamente** durante el proceso (art. 35.2 RGPD). Su opinión y las decisiones tomadas al respecto deben documentarse |
| **Encargado del tratamiento** | Si el desarrollo lo realiza un proveedor externo, debe colaborar aportando información técnica, pero la responsabilidad de la EIPD recae en el Responsable |
| **AEPD** | Si tras la EIPD persisten riesgos residuales altos no mitigables, debe realizarse una **consulta previa a la AEPD** (art. 36 RGPD) antes del inicio del tratamiento |

> En la AGE, la Agencia Española de Protección de Datos actúa como autoridad de control supervisora.

---

## Contenido de la EIPD: Estructura de la respuesta en el examen

### 1. Descripción del tratamiento

- **Responsable del tratamiento:** [Organismo del supuesto]
- **Finalidad:** [Objetivo del sistema]
- **Base jurídica** (art. 6 RGPD): interés público / obligación legal / consentimiento...
- **Categorías de datos tratados:** identificativos, económicos, categorías especiales (art. 9)...
- **Colectivos afectados:** ciudadanos en general / menores / funcionarios...
- **Destinatarios y cesiones:** otros organismos, proveedores cloud, terceros países
- **Plazo de conservación:** según normativa sectorial o política de retención

### 2. Evaluación de la necesidad y proporcionalidad

Justificar que el tratamiento es **necesario** para la finalidad perseguida y **proporcional** al riesgo que supone. Valorar si podrían alcanzarse los mismos fines tratando menos datos o con menor intrusión en la privacidad (principio de minimización, art. 5.1.c RGPD).

### 3. Identificación y valoración de riesgos

Usar el esquema **riesgo = probabilidad × impacto** y clasificar en nivel Bajo / Medio / Alto:

| Riesgo identificado | Probabilidad | Impacto | Nivel |
|---|---|---|---|
| Acceso no autorizado a datos personales | Media | Alto | **Alto** |
| Decisión automatizada incorrecta con perjuicio al interesado | Media | Alto | **Alto** |
| Sesgo algorítmico → discriminación (si hay IA) | Media | Alto | **Alto** |
| Fuga de datos de entrenamiento del modelo (si hay IA) | Baja | Alto | **Medio** |
| Uso de datos fuera de la finalidad declarada | Baja | Medio | **Medio** |
| Suplantación de identidad en canal digital | Baja | Alto | **Medio** |

> Si el sistema incorpora IA, incluir siempre el **riesgo de sesgo algorítmico** y la falta de explicabilidad de las decisiones. Conecta con el **AI Act** si el sistema puede clasificarse como de alto riesgo (Anexo III del Reglamento UE 2024/1689).

### 4. Medidas para mitigar los riesgos

**Técnicas:**
- Cifrado en tránsito (TLS 1.3) y en reposo (AES-256)
- Pseudonimización o anonimización donde sea posible
- Control de acceso basado en roles (RBAC) + principio de mínimo privilegio
- Auditoría y trazabilidad de accesos a datos personales
- Supresión automática de datos al vencer el plazo de conservación
- *Si hay IA:* supervisión humana de decisiones de alto impacto, documentación técnica del modelo, evaluaciones periódicas de sesgo, explicabilidad (XAI)

**Organizativas:**
- Registro de actividades de tratamiento (art. 30 RGPD)
- Cláusulas de protección de datos en contratos con encargados
- Procedimiento documentado para el ejercicio de derechos ARSLOP (Acceso, Rectificación, Supresión, Limitación, Oposición, Portabilidad)
- Especial atención al **derecho de oposición a decisiones automatizadas** (art. 22 RGPD) si el sistema toma decisiones sin intervención humana
- Formación del personal en protección de datos
- Nombramiento/consulta del DPO

**Normativas de referencia a citar:**
- RGPD (Reglamento UE 2016/679), arts. 5, 6, 9, 22, 25, 35 y 36
- LOPDGDD (LO 3/2018), especialmente si hay datos de menores
- Guía de la AEPD para una EIPD
- ENS (RD 311/2022) — para las medidas de seguridad técnicas en sistemas de la AGE
- *Si hay IA:* Reglamento UE 2024/1689 (AI Act)

### 5. Conclusión y consulta previa a la AEPD

Indicar el **nivel de riesgo residual** tras aplicar las medidas. Si persisten riesgos residuales altos no mitigables con medidas razonables, el Responsable debe realizar una **consulta previa a la AEPD** (art. 36 RGPD) antes de iniciar el tratamiento, quien dispondrá de 8 semanas (prorrogables 6 semanas más) para emitir su respuesta.

La EIPD es un **documento vivo**: debe revisarse periódicamente y ante cualquier cambio significativo en el tratamiento.

---

## Conexión con AI Act (para supuestos con IA)

Si el sistema incorpora IA, añadir en el bloque de descripción o conclusión:

> *"Adicionalmente al artículo 35 RGPD, el sistema debe evaluarse bajo el Reglamento UE 2024/1689 (AI Act). Si el sistema realiza toma de decisiones que afectan a derechos de ciudadanos en el ámbito de una administración pública (p.ej., gestión de prestaciones, acceso a servicios públicos), podría clasificarse como sistema de **alto riesgo** (Anexo III, categoría 5 del AI Act). Esto impone obligaciones adicionales: sistema de gestión de riesgos, datos de entrenamiento de alta calidad, documentación técnica, registro de eventos, transparencia ante el usuario, supervisión humana y evaluación de conformidad antes del despliegue."*

> ⚠️ No todos los sistemas con IA son de alto riesgo según el AI Act. Un chatbot de información general (sin decisiones que afecten a derechos) sería de **riesgo limitado**, con obligaciones menores (básicamente transparencia: el ciudadano debe saber que interactúa con una IA).

---

## Resumen esquemático para respuesta rápida en examen

```
EIPD
├── 1. ¿Es obligatoria? → Justificar con ≥2 factores del art. 35 RGPD
├── 2. Descripción del tratamiento → Responsable, finalidad, datos, base jurídica, destinatarios, plazos
├── 3. Necesidad y proporcionalidad → ¿Es el mínimo de datos necesario?
├── 4. Identificación de riesgos → Tabla probabilidad × impacto
├── 5. Medidas de mitigación → Técnicas + organizativas + normativas (ENS + RGPD [+ AI Act])
└── 6. Conclusión → Riesgo residual + ¿consulta previa a AEPD?
```

