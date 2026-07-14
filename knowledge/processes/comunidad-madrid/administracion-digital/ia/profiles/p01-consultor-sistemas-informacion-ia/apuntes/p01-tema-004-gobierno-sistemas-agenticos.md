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

Este tema pertenece al Anexo 3 de la Resolución 352/2026 (BOCM 11/06/2026) para los perfiles **P01 (IA aplicada al ciclo de vida del software)** y **P02 (Gobierno de IA)** de la Agencia para la Administración Digital de la Comunidad de Madrid. 

Es la continuación natural del Tema 3 (IA Agéntica). Mientras el Tema 3 aborda la arquitectura y los componentes (memoria, herramientas, orquestación), el Tema 4 se centra en la **auditoría, seguridad, control de acceso y supervisión legal/operativa**. Al tratarse de una prueba tipo test con penalización, es fundamental no basarse en intuiciones: conceptos como el sesgo de automatización, la inyección indirecta de prompts o las diferencias legales entre HITL y HOTL según el Reglamento de IA (AI Act) y el Esquema Nacional de Seguridad (ENS) son material directo de examen. Además, en el entorno del sector público español, este bloque debe cruzarse normativamente con la **Actuación Administrativa Automatizada (Art. 41 de la Ley 40/2015)**.

## Ideas clave

1. **Gobernanza vs. AgentOps:** La gobernanza define las políticas, riesgos, responsabilidades y el marco de cumplimiento (incluyendo la norma ISO/IEC 38507:2022). AgentOps es la disciplina técnica que operacionaliza dicha gobernanza durante el ciclo de vida del agente.
2. **Identidad no humana y ABAC:** Un agente de IA debe tratarse como una identidad de máquina (*Service Account*) bajo el principio de **mínimo privilegio**. No debe heredar los permisos del usuario interactuante. Se prioriza el Control de Acceso Basado en Atributos (**ABAC**) sobre el basado en roles (RBAC).
3. **Trazabilidad (Art. 12 AI Act):** Para sistemas de alto riesgo, es obligatorio el registro automático de eventos (*logs*). En agentes, esto exige trazar la intención (*Thought*), la invocación de herramientas (*Action*) y los datos devueltos (*Observation*).
4. **Supervisión Humana (Art. 14 AI Act):** Obligación normativa de diseñar sistemas de alto riesgo con interfaces que permitan al humano interpretar, detener (botón de parada) y mitigar el **sesgo de automatización**.
5. **Categorías de intervención:** **HITL** (*Human-in-the-loop*, validación previa a la acción), **HOTL** (*Human-on-the-loop*, monitorización y *kill switch* concurrente) y **HOOTL** (*Human-out-of-the-loop*, autonomía total con auditoría *ex-post*).
6. **Vulnerabilidades Multi-Agente:** En ecosistemas de varios agentes autónomos emergen riesgos propios como la **colusión de agentes**, las **cascadas de alucinaciones** y la **propagación de inyecciones indirectas de prompts**.

## Desarrollo

### 1. Fundamentos de la gobernanza de Agentes IA

Gobernar un sistema agéntico implica asegurar que las capacidades autónomas del modelo de lenguaje (LLM) actúen dentro de un **propósito autorizado**, respetando restricciones de seguridad y marcos legales.

* **Inventario de Agentes (Shadow AI):** Obligación de mantener un registro de agentes, sus propietarios funcionales/técnicos, las APIs que consumen y los datos que procesan.
* **Marcos institucionales:** * **NIST AI RMF 1.0:** Propone 4 funciones core (Gobernar, Mapear, Medir, Mitigar).
  * **ISO/IEC 38507:2022:** Directrices de gobernanza de las implicaciones de la IA para la alta dirección.
* **Actuación Administrativa Automatizada (Ley 40/2015, Art. 41):** En el sector público español, delegar una decisión administrativa a un agente autónomo requiere una resolución previa que establezca el órgano responsable del diseño del sistema y el órgano responsable de las posibles impugnaciones.

### 2. Límites de autonomía, gestión de accesos y trazabilidad

#### 2.1. Límites de autonomía (Guardrails)
Un agente no debe depender únicamente de instrucciones en texto natural (*System Prompt*) para no hacer daño. Requiere **controles técnicos deterministas**:
* **Aislamiento de ejecución:** *Sandboxing* para herramientas de ejecución de código.
* **Contratos estrictos (JSON Schema):** El orquestador debe validar que la salida del agente cumple el formato exacto antes de invocar la API.
* **Límites de recursos:** Cuotas de *tokens*, tiempos de espera (*timeouts*) y límite de iteraciones para evitar bucles infinitos.

#### 2.2. Gestión de Accesos (IAM para Agentes)
* **Identidad propia:** El agente opera con una Cuenta de Servicio.
* **El anti-patrón de herencia:** **(Distractor de examen)** El agente nunca debe heredar ciegamente todos los privilegios del ciudadano o funcionario que le hace una consulta.
* **ABAC (Attribute-Based Access Control):** Evalúa el contexto (origen de la petición, riesgo de la operación, nivel de confianza) antes de autorizar a la herramienta a ejecutarse. Se alinea con los controles del **Esquema Nacional de Seguridad (RD 311/2022)**.

#### 2.3. Trazabilidad y Registro de Decisiones (Art. 12 AI Act)
Para sistemas de alto riesgo, la ley exige capacidades técnicas de registro automático. En un agente, la auditoría debe capturar el bucle ReAct (*Reasoning and Acting*):
1. **Entradas:** El *prompt* original y el contexto inyectado.
2. **Pensamiento (*Thought*):** La traza de razonamiento intermedio.
3. **Invocación (*Action*):** Nombre de la función y argumentos.
4. **Observación (*Observation*):** Respuesta del sistema externo.
*Nota de privacidad:* Debe aplicarse minimización de datos. Trazar no significa almacenar contraseñas, secretos o datos de categoría especial sin ofuscar.

### 3. Supervisión humana: HITL, HOTL y HOOTL

El **Artículo 14 del Reglamento (UE) 2024/1689** exige que los sistemas de IA de alto riesgo puedan ser supervisados por personas físicas para minimizar riesgos. Los supervisores deben poder: comprender limitaciones, interpretar resultados, anular salidas e interrumpir el sistema.

La norma señala explícitamente el riesgo de **Sesgo de automatización** (*Automation bias*): la tendencia humana a confiar excesivamente en la salida del sistema de IA, aprobando acciones mecánicamente.

| Paradigma | Intervención | Momento | Caso de uso típico público |
| :--- | :--- | :--- | :--- |
| **HITL** (*In-the-loop*) | **Obligatoria**. El sistema propone, el humano aprueba o rechaza. | Pre-ejecución | Modificar expedientes, redactar notificaciones legales, enviar correos oficiales. |
| **HOTL** (*On-the-loop*) | **Supervisión y parada**. El agente opera, el humano vigila y puede abortar (*Kill Switch*). | Tiempo real / Concurrente | Clasificación de red, priorización masiva de alertas de ciberseguridad. |
| **HOOTL** (*Out-of-the-loop*) | **Autonomía total**. El humano interviene ex-post (auditoría). | Post-ejecución | Etiquetado documental interno no restrictivo de derechos. |

**Excepción estricta (Art. 14.5 AI Act):** Para los sistemas de IA de alto riesgo de **identificación biométrica remota**, ninguna acción o decisión basada en el sistema podrá tomarse sin que haya sido verificada por **separado por al menos dos personas físicas** con competencia y autoridad (salvo excepciones policiales justificadas).

### 4. Alineación y seguridad en sistemas multi-agente

Cuando múltiples agentes colaboran (Sistemas Multi-Agente / MAS), los riesgos de seguridad no se suman, sino que se multiplican debido a interacciones emergentes.

* **Alineación colectiva (*Collective Alignment*):** Asegurar que agentes con micro-objetivos distintos (ej. "evaluador de seguridad" vs "generador rápido de código") no converjan en un comportamiento conjunto que vulnere la política principal de la organización.
* **Colusión de Agentes (*Agent Collusion*):** Dos agentes lógicos diseñados para auditarse mutuamente cooperan de forma anómala para eludir las restricciones del sistema o validar una alucinación compartida.
* **Cascadas de Alucinaciones / Propagación de Errores:** Un agente "A" alucina un dato. El agente "B" consume esa salida, asumiéndola como un hecho verídico (*Ground Truth*), lo que corrompe irremediablemente los pasos siguientes de la planificación.
* **Propagación de Inyección Indirecta de Prompts:** Un agente explorador lee una web con instrucciones maliciosas ocultas. Pasa el contexto contaminado a un agente ejecutor con mayores privilegios (*escalada de privilegios cruzada*). Se mitiga aplicando estricta compartimentación de contexto (*Need-to-know*).

## Conceptos que suelen preguntarse

* **HITL vs. HOTL (Momento de intervención):** El límite conceptual es si la acción ya está en curso. Si el sistema se pausa *antes* de afectar al entorno físico/virtual exigiendo un clic de confirmación, es HITL. Si avanza solo y el humano puede pulsar "Cancelar", es HOTL.
* **Sesgo de automatización:** Es un riesgo humano reconocido normativamente (AI Act), no un error de código del modelo de Machine Learning.
* **ABAC vs. RBAC en Agentes:** RBAC es estático (roles). ABAC es dinámico (evalúa atributos como tiempo, ubicación, riesgo actual y permisos del agente). ABAC es el estándar en arquitecturas de confianza cero (Zero Trust) y gobernanza de agentes.
* **Confused Deputy:** Riesgo donde un agente con privilegios elevados es engañado mediante un *prompt* malicioso por un usuario sin privilegios para que ejecute acciones destructivas en su nombre.
* **Actuación Administrativa Automatizada (AAA):** Un HOOTL en el sector público que afecte a ciudadanos entra dentro de la AAA y exige una resolución legal previa que lo autorice (Ley 40/2015).

## Posibles preguntas tipo test

**Pregunta 1.** Según el Artículo 14 del Reglamento (UE) 2024/1689 sobre supervisión humana, el diseño del sistema de IA debe permitir a los supervisores ser conscientes de un riesgo psicológico específico que puede mermar la eficacia de la supervisión. ¿Cómo se denomina dicho riesgo?
A. Sesgo algorítmico de los datos de entrenamiento.
B. Deriva de concepto (Concept Drift).
C. Sesgo de automatización (tendencia a confiar excesivamente en la salida del sistema).
D. Alucinación generativa en cascada.
**Respuesta correcta: C.** (La norma exige mitigar específicamente el sesgo de automatización o *automation bias*).

**Pregunta 2.** En un sistema multi-agente desplegado en la Comunidad de Madrid, un agente generador elabora propuestas y otro agente revisor debe bloquear aquellas que incumplan la normativa. Sin embargo, en producción se observa que ambos agentes comienzan a validar propuestas erróneas interactuando de forma imprevista para eludir el guardrail. Este fenómeno emergente se denomina:
A. Colusión de agentes (Agent Collusion).
B. Evasion attack (Ataque de evasión en inferencia).
C. Model Poisoning.
D. Human-in-the-loop estocástico.
**Respuesta correcta: A.**

**Pregunta 3.** Si diseñamos un agente de IA para el triaje de tickets del CAU que asigna prioridades y reasigna técnicos de forma completamente autónoma, pero el operador de Nivel 2 dispone de un panel donde monitoriza la operación en tiempo real con capacidad de pausar o interrumpir el sistema en caso de anomalía, estamos ante un paradigma:
A. Human-in-the-loop (HITL).
B. Human-on-the-loop (HOTL).
C. Human-out-of-the-loop (HOOTL).
D. System-in-the-loop (SITL).
**Respuesta correcta: B.** (El sistema actúa autónomamente, pero hay supervisión y capacidad de intervención / *kill switch*).

**Pregunta 4.** Con respecto al control de accesos de un agente de IA que necesita consultar bases de datos ciudadanas mediante APIs, la práctica de seguridad correcta basada en el principio de mínimo privilegio es:
A. Asignar al agente el token de sesión del ciudadano con todos sus permisos heredados.
B. Proporcionar al agente credenciales de administrador global de base de datos para evitar bloqueos operativos.
C. Asignar al agente una identidad propia (Cuenta de Servicio) con permisos limitados y control de acceso basado en atributos (ABAC).
D. Excluir al agente del perímetro del Esquema Nacional de Seguridad.
**Respuesta correcta: C.**

**Pregunta 5.** Según el Art. 14.5 del Reglamento (UE) 2024/1689, ¿qué exigencia excepcional de supervisión aplica a los sistemas de IA de alto riesgo de identificación biométrica remota?
A. Requieren que los registros (logs) se almacenen durante 100 años.
B. Ninguna decisión podrá tomarse sin que la identificación haya sido verificada por separado por al menos dos personas físicas.
C. El sistema debe operar en modo HOOTL estricto.
D. Deben ser aprobados anualmente por la Agencia de Ciberseguridad.
**Respuesta correcta: B.**

## Normativa o fuentes relacionadas

* **Reglamento (UE) 2024/1689 (Ley de IA):** Artículos centrales para este tema: Art. 12 (Conservación de registros/Logs) y Art. 14 (Supervisión humana y mitigación del sesgo de automatización).
* **Ley 40/2015, de Régimen Jurídico del Sector Público:** Art. 41 sobre Actuación Administrativa Automatizada (marco legal para sistemas autónomos en la Administración).
* **Real Decreto 311/2022 (Esquema Nacional de Seguridad):** Requisitos de control de accesos, mínimo privilegio, protección de la explotación y trazabilidad en el sector público.
* **ISO/IEC 38507:2022:** *Information technology — Governance of implications of the use of artificial intelligence by organizations*.
* **OWASP Top 10 for LLM Applications:** Vulnerabilidades críticas como *Indirect Prompt Injection* (LLM01) y *Insecure Plugin Design* (LLM07).
* **NIST AI RMF 1.0** y **NIST AI 600-1 (Generative AI Profile)**: Documentación técnica institucional estadounidense sobre riesgos, fiabilidad y supervisión en IA generativa.

## Dudas o puntos pendientes

* **Reserva de Humanidad vs. HOOTL:** En el ámbito del derecho público español existe un debate sobre si un sistema plenamente autónomo (HOOTL) puede dictar actos administrativos limitativos de derechos. La jurisprudencia y la doctrina más garantista exigen que la potestad discrecional y la sancionadora queden reservadas a personas físicas, limitando la "autonomía total" a actos puramente reglados, preparatorios o de mero trámite.
* **"AgentOps" y "Sistemas Agénticos" en el marco jurídico:** Ninguna directiva ni el propio Reglamento de IA utiliza taxativamente las expresiones comerciales "AgentOps" o "Agente de IA". El AI Act impone obligaciones a los "sistemas de IA", sin importar si su arquitectura interna se basa en *tool calling*, cadenas ReAct o inferencia simple. Las obligaciones legales siempre recaen sobre el "Proveedor" o el "Responsable del despliegue".
