---
id: "cm-ad-ia-p01-tema-004-gobierno-sistemas-agenticos"
title: "Gobierno de los sistemas agénticos"
type: "apunte"
status: "borrador"
processes:
  - "comunidad-madrid/administracion-digital/ia"
profiles:
  - "p01-consultor-sistemas-informacion-ia"
official_profile: "P01 - Consultor de Sistemas de Información - IA Aplicada al Ciclo de Vida del Software"
official_topic: "Tema 4. Gobierno de los sistemas agénticos"
source_ids:
tags:
  - "inteligencia-artificial"
  - "ia-agentica"
  - "gobernanza-ia"
  - "agentes-ia"
  - "supervisión-humana"
  - "hitl"
  - "seguridad"
  - "trazabilidad"
  - "agentops"
created_at: "2026-07-10"
last_reviewed: null
ai_generated: true
ai_sources:
  - "chatgpt"
  - "perplexity"
  - "gemini"
needs_human_review: true
---

# Gobierno de los sistemas agénticos

## Encaje en la convocatoria

Este tema pertenece al **Anexo 3 de la Resolución 352/2026 (BOCM 11/06/2026)** para el perfil **P01 – IA aplicada al ciclo de vida del software** de la Agencia para la Administración Digital de la Comunidad de Madrid. Es la continuación natural de los Temas 2 (IA generativa) y 3 (IA agéntica), y se centra en la **auditoría, seguridad, control de acceso, supervisión humana y marco normativo** de sistemas agénticos desplegados en la Administración.

La preparación debe cruzar arquitectura agéntica con marcos como el **AI Act (Reglamento (UE) 2024/1689)**, el **Esquema Nacional de Seguridad (RD 311/2022)**, normas ISO/IEC de gobernanza (38507, 42001), guías de la AEPD/AESIA y catálogos OWASP para LLM y aplicaciones agénticas, porque las preguntas tipo test combinan estos referentes.

## Ideas clave

1. **Gobernanza vs AgentOps:** La gobernanza define políticas, riesgos, responsabilidades y tolerancia al riesgo (ISO/IEC 38507, ISO/IEC 42001); AgentOps operacionaliza estas decisiones en el ciclo de vida del agente (permisos, HITL, trazabilidad, evaluación dinámica).
2. **Identidad no humana y acceso:** El agente debe tratarse como **identidad de máquina** (service account) bajo principio de **mínimo privilegio**, aplicando **ABAC/Zero Trust** y evitando heredar privilegios plenos del usuario.
3. **Trazabilidad y logs (Art. 12 AI Act):** Los sistemas de alto riesgo deben permitir **registro automático de eventos** durante toda su vida, capturando el funcionamiento del sistema con logs apropiados para la trazabilidad.
4. **Supervisión humana (Art. 14 AI Act):** La supervisión humana debe ser significativa, mitigando el **sesgo de automatización**, con mecanismos HITL/HOTL/HOOTL alineados con el riesgo del caso de uso.
5. **Multi‑agente y nuevos riesgos:** En ecosistemas multi‑agente emergen riesgos como **Identity & Privilege Abuse (AS103)**, **Cascading Failures (AS108)**, colusión de agentes y propagación de inyecciones indirectas.
6. **Clasificación de alto riesgo y finalidad prevista:** El AI Act y las guías de la Comisión sobre clasificación de alto riesgo valoran el **ámbito de uso, combinación con otros sistemas y finalidad prevista/razonablemente previsible**, no solo la tecnología.
7. **Transparencia, explicabilidad y “muchas manos”:** La transparencia exige que el sistema sea comprensible en todo su ciclo de vida (AESIA), y la gobernanza debe gestionar el **many‑hands problem** (responsabilidad repartida entre proveedor de modelo, integrador y deployer).
8. **Gobernanza de datos y sesgos:** RGPD, la propuesta de **Reglamento Ómnibus Digital (COM(2025) 836)** y las guías de AEPD permiten, con salvaguardas, usar categorías especiales de datos para detectar sesgos y obligan a EIPD en casos de alto riesgo.

## Desarrollo

### 1. Fundamentos de gobernanza de sistemas agénticos

Gobernar un sistema agéntico significa asegurar que su autonomía se ejerce únicamente dentro de una **finalidad autorizada**, con controles técnicos y organizativos que garanticen seguridad y cumplimiento normativo. El **NIST AI RMF 1.0** estructura la gestión de riesgos en cuatro funciones: **Gobernar, Mapear, Medir, Mitigar**, útiles para ordenar políticas, identificación de riesgos y controles.

La norma **ISO/IEC 38507:2022** orienta a la alta dirección sobre cómo integrar implicaciones de IA en su gobernanza corporativa, vinculando decisiones de IA a la estrategia y la rendición de cuentas. La futura norma **ISO/IEC 42001 (SGIA)** aporta un enfoque de sistema de gestión (Plan‑Do‑Check‑Act) para gobernar el ciclo de vida de casos de uso de IA, de forma similar a otros sistemas certificados (ISO 27001).

En el sector público español, la **Actuación Administrativa Automatizada (AAA)** del Art. 41 de la **Ley 40/2015** exige resolución que identifique el órgano responsable del sistema y el órgano responsable de revisar e impugnar actos dictados por sistemas automatizados. Esto implica que despliegues HOOTL que afecten derechos de ciudadanos deben estar amparados por resolución formal y encajar en actos reglados o de trámite más que en decisiones discrecionales.

### 2. Límites de autonomía, acción y gestión de accesos

#### 2.1. Acción vs autonomía

En IA agéntica conviene diferenciar:

- **Espacio de acción (action space):** conjunto de herramientas y permisos a los que el agente puede acceder (APIs, RAG, bases de datos, sistemas externos).
- **Autonomía:** grado de intervención humana exigido (HITL, HOTL, HOOTL), duración de decisiones no supervisadas y capacidad del agente para definir y ejecutar planes sin aprobación previa.

Controlar el riesgo exige limitar tanto el **action space** (qué puede hacer técnicamente) como la autonomía (cuándo y cómo se exige supervisión humana), aspecto recogido en preguntas de examen.

#### 2.2. Guardrails y límites técnicos

Los guardrails no pueden descansar solo en texto del System Prompt; deben completarse con **controles deterministas**:

- Aislamiento de ejecución (sandbox) para herramientas que ejecutan código o acceden a sistemas sensibles.
- Validación estricta de salidas del agente mediante contratos (por ejemplo, JSON Schema) antes de llamar a una API.
- Límites de recursos: cuotas de tokens, tiempos de espera, número máximo de iteraciones para prevenir bucles infinitos y ataques de denegación de cartera (wallet).

#### 2.3. Identidad no humana, ABAC y ENS

El agente debe operar con una **cuenta de servicio** propia, bajo el principio de **mínimo privilegio**, sin heredar automáticamente todos los permisos del usuario humano que lo invoca. El **Esquema Nacional de Seguridad (RD 311/2022)** recoge principios básicos como **mínimo privilegio, control de accesos, registro de actividad y gestión de riesgos**, aplicables a identidades agénticas igual que a sistemas tradicionales.

El uso de **ABAC (Attribute‑Based Access Control)** permite evaluar atributos como tipo de operación, sensibilidad de datos, contexto de red y rol del agente antes de autorizar una herramienta, alineándose con arquitecturas Zero Trust y con el Art. 20 ENS (“Mínimo privilegio”). OWASP Agentic AS103 “Identity & Privilege Abuse” describe precisamente el riesgo de operar agentes sin identidad clara propia, en un vacío de atribución que impide aplicar mínimo privilegio.

### 3. Trazabilidad y registro de decisiones (AI Act y ENS)

El **Art. 12 AI Act (Record‑keeping)** exige que los sistemas de IA de alto riesgo permitan técnicamente el **registro automático de eventos (logs)** a lo largo de su vida útil. Estos logs deben permitir identificar situaciones de riesgo, facilitar el seguimiento posterior al mercado y monitorizar la operación del sistema en relación con otras obligaciones del Reglamento.

En sistemas de reconocimiento biométrico remoto, el AI Act exige como mínimo registrar periodos de uso, bases de referencia empleadas, datos de entrada que generan coincidencias y las personas que verifican resultados. El ENS también exige **registro de actividad y detección de código dañino** (Art. 24 RD 311/2022), reforzando la necesidad de trazabilidad en sistemas que tratan información pública y datos personales.

En un agente ReAct, la trazabilidad completa debe capturar:

1. Prompt y contexto RAG usados (entrada).
2. Razonamiento interno (*Thought*).
3. Herramienta llamada y argumentos (*Action*).
4. Respuesta de la herramienta (*Observation*) y decisión final.

Al registrar, se debe respetar **minimización de datos** (RGPD y ENS): trazabilidad no equivale a almacenar contraseñas o datos de categoría especial en claro sin medidas adicionales.

### 4. Supervisión humana: HITL, HOTL, HOOTL y sesgo de automatización

El **Art. 14 AI Act (Supervisión humana)** exige que los sistemas de IA de alto riesgo se diseñen para permitir que supervisores humanos comprendan limitaciones, interpreten resultados, puedan intervenir y detener el sistema cuando sea necesario. El Reglamento destaca el **sesgo de automatización (automation bias)** como riesgo psicológico que puede hacer que los supervisores acepten respuestas del sistema sin análisis crítico.

Se distinguen tres paradigmas de intervención:

| Paradigma | Intervención | Momento | Ejemplo típico en AAPP |
| :-------- | :----------- | :------ | :---------------------- |
| HITL      | Aprobación obligatoria antes de acción irreversible. | Pre‑ejecución | Modificar datos de expedientes, enviar notificaciones oficiales. |
| HOTL      | Supervisión continua con capacidad de detener.       | Concurrente  | Clasificación masiva de alertas de ciberseguridad o tickets. |
| HOOTL     | Autonomía total con auditoría a posteriori.          | Post‑ejecución | Etiquetado documental interno o tareas de bajo impacto. |

El **Art. 14.5 AI Act** establece una excepción estricta en sistemas de **identificación biométrica remota**: ninguna decisión basada en el sistema puede adoptarse sin verificación separada por al menos **dos personas físicas** con competencia y autoridad, salvo casos urgentes justificados. Las preguntas de examen explotan este punto concreto.

Mitigar el sesgo de automatización obliga a medir **override rates** (tasas en las que el humano corrige al agente) y tiempos de respuesta, para asegurar que la supervisión no es meramente formal.

### 5. Riesgos en sistemas multi‑agente y OWASP Agentic

Los sistemas multi‑agente amplifican riesgos debido a interacciones emergentes entre agentes con distintos roles. El informe **OWASP Top 10 for Agentic Applications** identifica amenazas como **AS103 Identity & Privilege Abuse**, **AS108 Cascading Failures** y otros problemas asociados a colusión, escaladas de privilegios y falta de trazabilidad.

Riesgos clave:

- **Colusión de agentes (Agent Collusion):** dos agentes diseñados para auditarse mutuamente pueden cooperar de forma anómala para validar decisiones erróneas o vulnerar restricciones de seguridad.
- **Cascading Failures (AS108):** un error, alucinación o acción maliciosa en la salida de un agente se utiliza como entrada irrefutable por otros agentes subsiguientes, propagando y amplificando el impacto.
- **Propagación de prompt injection indirecta:** un agente lector consume contenido malicioso (web, documento), y transmite contexto contaminado a otro agente con mayores privilegios, provocando escaladas laterales.
- **Identity & Privilege Abuse (AS103):** operar agentes sin identidad estricta propia ni modelo claro de privilegios, mezclando identidades humanas con permisos agénticos, genera un vacío de atribución que impede aplicar mínimos privilegios.

Mitigar estos riesgos exige compartimentación de contextos (“need‑to‑know”), controles cruzados entre agentes y límites claros de permisos por agente.

### 6. Clasificación de alto riesgo, finalidad prevista y gobernanza europea

El AI Act considera de alto riesgo, además de los sistemas señalados en Art. 6 y 9, los sistemas enumerados en el **Anexo III** (por ejemplo, sistemas para educación, empleo, servicios esenciales, aplicación de la ley). Las **Draft Commission Guidelines on the Classification of High‑Risk AI Systems** aclaran que sistemas inicialmente no de alto riesgo pueden convertirse en altos riesgos si se combinan con otros sistemas en ámbitos de alto riesgo.

La noción de **finalidad prevista** y los usos “razonablemente previsibles” es clave: si un proveedor declara que un sistema no debe usarse en contextos de alto riesgo, pero su marketing sugiere usos en selección de personal o decisiones educativas, se presume alto riesgo si esos usos son factibles y previsibles.

El **AI Act Explorer** y la **Oficina de IA de la Comisión** funcionan como punto de coordinación y supervisión central; la Oficina de IA tiene competencia exclusiva para supervisar proveedores de modelos de IA de propósito general (GPAI). En el ámbito español, la AEPD, AESIA y autoridades sectoriales cooperan en evaluación de impacto y supervisión de casos de uso.

### 7. Transparencia, explicabilidad y “muchas manos”

El documento de la Comisión sobre **IA fiable** establece que los sistemas deben ser **lícitos, éticos y robustos**, y la **transparencia** es un componente esencial. La guía de transparencia de **AESIA** define transparencia como la cualidad de ser interpretables y comprensibles por quienes crean, despliegan y usan la IA, ligándola directamente a técnicas de **explicabilidad** e **interpretabilidad**.

La OCDE introduce la categoría de **AI Actors** para referirse a quienes desempeñan un papel activo en el ciclo de vida de la IA (proveedores, deployers, usuarios profesionales, etc.), resaltando la necesidad de asignar responsabilidades claras. El llamado **many‑hands problem** describe la dificultad de atribuir responsabilidad en cadenas donde intervienen proveedor de modelo base, proveedor del sistema y organización deployer, problema central de la gobernanza.

Para mejorar explicabilidad, se combinan:

- **Análisis de “caja blanca”** sobre orquestadores, flujos de datos y configuraciones del agente.
- **Pruebas de “caja negra”** basadas en golden tests y evaluación sistemática de trayectorias, registrando razones y acciones.

La transparencia no implica necesariamente publicar pesos de modelos propietarios, pero sí informar sobre propósito, límites, fuentes de datos y funcionamiento básico del sistema.

### 8. Gobernanza de datos, sesgos y evaluación de impacto

La **Propuesta de Reglamento Ómnibus Digital sobre IA (COM(2025) 836)** autoriza, con salvaguardas, el tratamiento de **categorías especiales de datos personales** (ej. datos sensibles) para detectar y corregir sesgos en sistemas de IA. Esto debe hacerse respetando RGPD y medidas de seguridad estrictas para acceso, documentación y uso de dichos datos.

La **AEPD** exige realizar o revisar una **Evaluación de Impacto para la Protección de Datos (EIPD)** cuando el tratamiento entrañe **alto riesgo para derechos y libertades**, siendo frecuente en despliegues de IA en el sector público. Las guías insisten en controlar inclusión de datos personales en prompts, recomendando herramientas y procedimientos que impidan introducir accidentalmente información sensible en entradas libres de texto.

El principio de **equidad (fairness)** en el marco europeo tiene una dimensión sustantiva (resultados justos) y una dimensión procedimental (procesos transparentes, recursos accesibles, canales de reclamación), que deben reflejarse en políticas de IA y en el SGIA (ISO/IEC 42001).

La política de IA de la organización fija objetivos y tolerancia al riesgo, que sirven como referencia para evaluar los riesgos identificados en cada etapa del ciclo de vida (diseño, desarrollo, despliegue, cierre). Los **informes periódicos de riesgos** durante la fase de despliegue comunican el estado de controles y riesgos al comité de riesgos y a órganos de gobierno.

## Conceptos que suelen preguntarse (trampas comunes)

| Concepto                       | Realidad técnica/jurídica                                                                 | Distractor típico en examen                                      |
| :----------------------------- | :---------------------------------------------------------------------------------------- | :---------------------------------------------------------------- |
| Sesgo de automatización       | Riesgo humano reconocido en Art. 14 AI Act: supervisores confían demasiado en el sistema. | “Es un bug del modelo, no un problema humano.”         |
| ABAC vs RBAC                  | ABAC evalúa atributos contextuales; RBAC asigna roles estáticos; ABAC encaja mejor en Zero Trust ENS. | “RBAC basta para gobernar agentes en AAPP.”             |
| HITL vs HOTL                  | HITL exige aprobación previa; HOTL permite actuar pero con supervisión y kill switch. | “Ambos significan lo mismo: el humano está ‘presente’”. |
| Identity & Privilege Abuse    | Falta de identidad propia y de mínimo privilegio, riesgo descrito en AS103 OWASP Agentic. | “Se refiere solo al robo de contraseñas humanas.”       |
| Cascading Failures            | Error en un agente se toma como verdad por otros, propagando impacto sistémico. | “Se limita a caídas físicas del servidor de modelos.”   |
| Actuación Administrativa Aut. | Requiere resolución formal que identifique órgano responsable de sistema y de impugnaciones. | “Basta con usar IA en cualquier acto administrativo.”   |
| Alto riesgo por combinación   | Sistemas no altos riesgos pueden ser de alto riesgo al combinarse en ámbitos del Anexo III. | “La clasificación depende solo del tipo de modelo.”     |
| Transparencia AESIA           | Sistema debe ser comprensible para actores durante todo el ciclo de vida, ligado a explicabilidad. | “Significa publicar todo el código fuente y pesos del modelo.” |
| Cifrado homomórfico           | Permite operar matemáticamente sobre datos cifrados sin descifrarlos en memoria. | “Solo protege datos en tránsito, no en procesamiento.”  |
| Golden tests/dataset          | Conjuntos de referencia para evaluar comportamiento y riesgos, no repositorios de credenciales. | “Son backups de todos los datos sensibles del sistema.” |

## Posibles preguntas tipo test

**Pregunta 1.** El Art. 12 del AI Act exige que los sistemas de IA de alto riesgo:

A. Funcionen exclusivamente sin conexión a redes externas.  
B. Permitan técnicamente el registro automático de eventos (logs) durante toda su vida útil.  
C. Almacenen todos los datos de entrada en claro sin cifrado.  
D. Sean de código abierto para facilitar auditorías comunitarias.  

**Respuesta correcta: B.**

---

**Pregunta 2.** En la gobernanza de agentes de IA que consultan bases de datos ciudadanas, la práctica correcta basada en mínimo privilegio es:

A. Ejecutar las consultas reutilizando el token de sesión del ciudadano con todos sus permisos.  
B. Otorgar al agente credenciales de administrador global para evitar errores de autorización.  
C. Asignar al agente una identidad propia de servicio con permisos limitados y control de acceso basado en atributos (ABAC).  
D. Excluir al agente del ámbito de aplicación del ENS.  

**Respuesta correcta: C.**

---

**Pregunta 3.** ¿Qué riesgo describe mejor la amenaza OWASP Agentic AS103 “Identity & Privilege Abuse”?

A. El uso de protocolos criptográficos obsoletos en comunicaciones entre agentes.  
B. El funcionamiento de agentes sin identidad propia clara, operando con privilegios excesivos heredados de usuarios humanos.  
C. El uso de modelos de código abierto sin auditoría de seguridad.  
D. La saturación de la base vectorial por exceso de consultas concurrentes.  

**Respuesta correcta: B.**

---

**Pregunta 4.** Según el Art. 14.5 del AI Act, en sistemas de identificación biométrica remota de alto riesgo:

A. Se prohíbe cualquier uso en espacios públicos.  
B. Las decisiones pueden tomarse exclusivamente por sistemas automáticos certificados.  
C. Toda decisión basada en el sistema debe ser verificada por separado por al menos dos personas físicas.  
D. Basta con un supervisor humano único si el sistema tiene precisión superior al 99 %.  

**Respuesta correcta: C.**

---

**Pregunta 5.** En un ecosistema multi‑agente, la amenaza descrita como “Cascading Failures” se refiere a:

A. Fallos de hardware que desconectan simultáneamente todos los agentes.  
B. Un error o alucinación de un agente que se usa como entrada fiable por otros agentes, propagando daño sistémico.  
C. Pérdida de conectividad entre agentes y el modelo fundacional.  
D. Exceso de logs que saturan el sistema de observabilidad.  

**Respuesta correcta: B.**

---

**Pregunta 6.** En el contexto de la gobernanza de IA, el “many‑hands problem” describe:

A. La necesidad de tener múltiples operadores humanos simultáneos para manejar cada agente.  
B. La ambigüedad sobre quién es responsable cuando varias entidades participan en el ciclo de vida de la IA (proveedor de modelo, integrador, deployer).  
C. La saturación de recursos por exceso de agentes con herramientas de escritura en la misma base de datos.  
D. La obligación de realizar duplicadas evaluaciones de impacto para cada caso de uso.  

**Respuesta correcta: B.**

---

**Pregunta 7.** Según la AEPD, ¿cuándo es imperativo realizar o revisar una Evaluación de Impacto para la Protección de Datos (EIPD) en un sistema de IA?

A. Siempre que se utilice IA, aunque no trate datos personales.  
B. Solo si el sistema se ha desarrollado internamente.  
C. Cuando el tratamiento entrañe un alto riesgo para los derechos y libertades de las personas.  
D. Únicamente tras un incidente grave de seguridad.  

**Respuesta correcta: C.**

---

**Pregunta 8.** En el marco del ENS, el principio de “seguridad como proceso integral” implica que:

A. La seguridad se limita a controles técnicos sobre servidores.  
B. Abarca elementos humanos, materiales, técnicos, jurídicos y organizativos relacionados con el sistema de información.  
C. Permite tratar la seguridad como actuaciones puntuales de auditoría sin continuidad.  
D. Se aplica solo a sistemas que tratan información clasificada.  

**Respuesta correcta: B.**

---

**Pregunta 9.** ¿Qué relación establece la norma ISO/IEC 42001 entre la política de IA de la organización y la evaluación de riesgos?

A. La evaluación de riesgos se limita a la fase de desmantelamiento del sistema.  
B. La política fija objetivos y tolerancia al riesgo, que sirven como criterios para evaluar riesgos en todas las etapas del ciclo de vida.  
C. La evaluación de riesgos es exclusivamente cualitativa y ajena a la política.  
D. La política de IA debe ser definida por el proveedor del modelo fundacional.  

**Respuesta correcta: B.**

---

**Pregunta 10.** ¿Qué efecto tiene la Propuesta de Reglamento Ómnibus Digital (COM(2025) 836) en la gobernanza de datos para detección de sesgos?

A. Elimina la aplicación del RGPD cuando se trate de IA generativa.  
B. Autoriza, con salvaguardas, el uso de categorías especiales de datos personales para detectar y corregir sesgos.  
C. Prohíbe totalmente el uso de datos personales en entrenamiento.  
D. Permite vender libremente datos sensibles a terceros.  

**Respuesta correcta: B.**

## Normativa o fuentes relacionadas

- **Reglamento (UE) 2024/1689 (AI Act):** Arts. 9, 12, 14, Anexo III, definiciones de alto riesgo, supervisión humana y registro de eventos.
- **Ley 40/2015, de Régimen Jurídico del Sector Público:** Art. 41 sobre Actuación Administrativa Automatizada.
- **Real Decreto 311/2022 (ENS):** principios básicos (seguridad como proceso integral, prevención/detección/respuesta, mínimo privilegio), requisitos mínimos y registro de actividad.
- **ISO/IEC 38507:2022:** gobernanza de implicaciones de IA para la alta dirección.
- **ISO/IEC 42001 (SGIA):** sistema de gestión de IA basado en enfoque de ciclo de vida y evaluación de riesgos.
- **NIST AI RMF 1.0 y NIST AI 600‑1 (Generative AI Profile):** gestión de riesgos y perfiles para IA generativa.
- **OWASP Top 10 for LLM Applications y OWASP Top 10 for Agentic Applications:** riesgos como LLM01 Prompt Injection, LLM02 Sensitive Information Disclosure, AS103 Identity & Privilege Abuse, AS108 Cascading Failures.
- **Guías AEPD/AESIA:** transparencia, explicabilidad, evaluaciones de impacto y principios de diseño responsable de sistemas de IA.

## Dudas o puntos pendientes

- La terminología “AgentOps”, “IA agéntica”, “ReAct”, “MCP” o “Agent‑to‑Agent” procede de la práctica industrial y no de normas vinculantes; el AI Act regula **sistemas de IA** según su uso y riesgo, con independencia de estas etiquetas.
- Existe debate doctrinal sobre la **reserva de humanidad** en actos administrativos que afectan derechos fundamentales: la postura más garantista limita la autonomía plena (HOOTL) a actos reglados o de mero trámite, reservando decisiones discrecionales y sancionadoras a órganos humanos.