---
id: "cm-ad-ia-p02-tema-005-marco-regulatorio-cumplimiento-estandares"
title: "Marco Regulatorio, Cumplimiento y Estándares"
type: "apunte"
status: "borrador"
processes:
  - "comunidad-madrid/administracion-digital/ia"
profiles:
  - "p02-consultor-sistemas-informacion-ia"
official_profile: "P02 - Consultor de Sistemas de Información - Especialista en Gobierno de IA"
official_topic: "Tema 5. Marco Regulatorio, Cumplimiento y Estándares"
source_ids: []
tags:
  - "cumplimiento"
  - "ai-act"
  - "rgpd"
  - "lopdgdd"
  - "propiedad-intelectual"
  - "iso-iec-42001"
  - "sgia"
  - "proveedores-ia"
  - "responsables-despliegue"
created_at: "2026-07-14"
last_reviewed: null
ai_generated: true
ai_sources:
  - "perplexity"
  - "chatgpt"
  - "gemini"
  - "base-apunte"
  - "eur-lex"
needs_human_review: true
---

# Marco Regulatorio, Cumplimiento y Estándares

## Encaje en la convocatoria

Este tema es el **núcleo jurídico-técnico** del perfil **P02: Consultor de Sistemas de Información especialista en Gobierno de IA** (Tema 5 del Anexo 3 de la Resolución 352/2026). El tribunal exige un conocimiento riguroso de la arquitectura del **Reglamento (UE) 2024/1689 (Ley de IA / *AI Act*)**, focalizándose en el enfoque basado en riesgos, la distinción exacta de roles (Proveedor frente a Responsable del despliegue), la interacción normativa con el **RGPD** y los marcos certificables como la norma **ISO/IEC 42001**. 

En un examen tipo test con penalización, no se admiten aproximaciones vagas; se evaluarán excepciones legales, plazos de aplicación y obligaciones documentales específicas. Es fundamental entender la complementariedad entre las evaluaciones de impacto (DPIA/EIPD del RGPD vs. FRIA de la Ley de IA) y el tratamiento de la propiedad intelectual en el entrenamiento de modelos.

## Ideas clave

1.  **AI Act (Enfoque Basado en Riesgo):** Reglamento europeo de aplicación directa. Clasifica los sistemas en 4 niveles: Riesgo Inaceptable (Prohibido, Art. 5), Alto Riesgo (Altamente regulado, Art. 6), Riesgo de Transparencia (Deepfakes/Chatbots, Art. 50) y Riesgo Mínimo.
2.  **Roles Legales Críticos:** 
    *   **Proveedor (*Provider*):** Quien desarrolla la IA y la pone en el mercado con su marca. Soporta la carga de certificación (Marcado CE).
    *   **Responsable del Despliegue (*Deployer*):** Quien usa el sistema bajo su autoridad (ej. la Administración Pública). Tradicionalmente mal llamado "usuario".
3.  **El "Cambio Sustancial" (Asunción de Rol):** Si un Responsable del despliegue modifica sustancialmente la finalidad de un sistema de IA (ej. adaptando un modelo de propósito general para convertirlo en un sistema de alto riesgo), asume automáticamente las obligaciones legales de **Proveedor**.
4.  **Excepción de Datos Sensibles (Art. 10.5 AI Act):** Permite tratar categorías especiales de datos personales (Art. 9 RGPD) de manera excepcional y temporal con el único fin de **detectar y corregir sesgos** en sistemas de alto riesgo.
5.  **DPIA vs. FRIA:** La Evaluación de Impacto de Protección de Datos (EIPD/DPIA del RGPD) evalúa riesgos para la privacidad. La Evaluación de Impacto sobre los Derechos Fundamentales (FRIA, Art. 27 AI Act) evalúa impactos más amplios (tutela judicial, no discriminación) y **complementa** a la DPIA; no la sustituye.
6.  **ISO/IEC 42001 (SGIA):** Primer estándar internacional **certificable** para implementar un Sistema de Gestión de IA. Basado en el ciclo de mejora continua (PHVA) y estructurado para integrarse con la ISO 27001 (Seguridad). No certifica algoritmos, certifica la gobernanza de la organización.
7.  **Propiedad Intelectual y Modelos GPAI:** El AI Act obliga a los proveedores de Modelos de IA de Uso General (GPAI) a publicar un resumen suficientemente detallado del contenido usado para el entrenamiento y respetar las reservas de derechos de autor (minería de textos y datos - TDM).

## Desarrollo

### 1. Reglamento Europeo de Inteligencia Artificial (AI Act – UE 2024/1689)

Publicado en el DOUE el 12 de julio de 2024. Es una norma de mercado interior, seguridad y derechos fundamentales de aplicación directa (*hard law*).

#### 1.1. Fechas clave de aplicación (Escalonada)
*   **Agosto 2024:** Entrada en vigor.
*   **Febrero 2025 (6 meses):** Aplicación de Prácticas de IA Prohibidas (Riesgo Inaceptable).
*   **Agosto 2025 (12 meses):** Reglas para Modelos de IA de Uso General (GPAI) y sanciones.
*   **Agosto 2026 (24 meses):** **Aplicación General.** Sistemas de alto riesgo del Anexo III.
*   **Agosto 2027 (36 meses):** Sistemas de alto riesgo del Anexo I (componentes de seguridad de productos regulados).

#### 1.2. Clasificación de Riesgos
*   **Riesgo Inaceptable (Prácticas Prohibidas - Art. 5):**
    *   Técnicas manipuladoras subliminales que causen daño.
    *   Explotación de vulnerabilidades.
    *   *Social Scoring* (puntuación social) por autoridades públicas.
    *   Riesgo penal predictivo basado *únicamente* en perfiles de personalidad.
    *   Identificación biométrica remota "en tiempo real" en espacios públicos con fines policiales (con excepciones judiciales muy tasadas).
*   **Alto Riesgo (Art. 6):**
    *   *Anexo I:* Componentes de seguridad de productos armonizados (ej. aviación, productos sanitarios).
    *   *Anexo III:* Casos de uso sensibles: Biometría, Infraestructuras críticas, Educación, Empleo, Acceso a servicios públicos esenciales, Aplicación de la ley, Migración y Administración de Justicia.
    *   *Excepción (Art. 6.3):* Un sistema del Anexo III no es de alto riesgo si solo realiza una tarea de procedimiento limitada o preparatoria y no plantea riesgo de perjuicio. *Excepción a la excepción:* La **elaboración de perfiles (*profiling*)** es siempre de alto riesgo.
*   **Riesgo Limitado / Transparencia (Art. 50):** Obligación de informar a las personas que interactúan con IA (chatbots) o marcar contenido sintético (*deepfakes*) en formato legible por máquina.

### 2. Obligaciones para Proveedores y Responsables del Despliegue

#### 2.1. Obligaciones del Proveedor de Alto Riesgo (Art. 16)
Asume la carga de garantizar la conformidad *ex ante* (antes de la comercialización):
*   Implantar un Sistema de Gestión de Calidad (Art. 17).
*   Elaborar la Documentación Técnica (Art. 11).
*   Someter el sistema a Evaluación de Conformidad (Art. 43).
*   Generar la Declaración UE de Conformidad (Art. 47) y colocar el **Marcado CE** (Art. 48).
*   Inscribir el sistema en la Base de Datos de la UE (Art. 49).
*   Establecer un sistema de Seguimiento Poscomercialización (Art. 72).
*   Conservar los archivos de registro (*logs*) generados automáticamente, cuando estén bajo su control.

#### 2.2. Obligaciones del Responsable del Despliegue de Alto Riesgo (Art. 26)
*Deployer* (típicamente, la Administración Pública):
*   Utilizar el sistema *exclusivamente* conforme a las instrucciones del proveedor.
*   Garantizar **supervisión humana** por personas competentes y formadas.
*   Conservar los *logs* bajo su control por un periodo mínimo de **6 meses**.
*   Realizar la Evaluación de Impacto sobre los Derechos Fundamentales (**FRIA**, Art. 27) antes del despliegue (obligatorio para organismos públicos).

### 3. Tratamiento de Datos Personales y Propiedad Intelectual

#### 3.1. Intersección RGPD, LOPDGDD y AI Act
El AI Act y la normativa de protección de datos se aplican de forma **acumulativa**. El AI Act no proporciona una base legitimadora autónoma para tratar datos personales (Art. 6 RGPD).
*   **Privacidad desde el Diseño (Art. 25 RGPD):** Obliga a integrar medidas técnicas (minimización, seudonimización) desde la concepción de la arquitectura de la IA.
*   **DPIA vs. FRIA:** Si un sistema requiere una Evaluación de Impacto de Protección de Datos (DPIA/EIPD - Art. 35 RGPD) y una FRIA (Art. 27 AI Act), la FRIA **complementará** a la DPIA. No se excluyen ni se sustituyen.

#### 3.2. Propiedad Intelectual e IA Generativa (Modelos GPAI)
El marco de derechos de autor tradicional exige intervención humana, generando un vacío normativo sobre la titularidad de obras creadas autónomamente por IA.
*   **Obligaciones para Proveedores de GPAI (Art. 53 AI Act):**
    1.  Establecer políticas para respetar los derechos de autor (Directiva UE 2019/790).
    2.  Respetar la reserva de derechos (*opt-out*) para la minería de textos y datos (TDM).
    3.  Elaborar y publicar un **resumen suficientemente detallado** del contenido utilizado para el entrenamiento del modelo.

### 4. Sistemas de Gestión de Inteligencia Artificial (SGIA) e ISO/IEC 42001

Un **SGIA** es el marco organizativo para dirigir y controlar el desarrollo, uso y operación de sistemas de IA, estableciendo políticas, roles, riesgos y métricas.

#### 4.1. Norma ISO/IEC 42001:2023
*   **Naturaleza:** Es el primer estándar internacional **certificable** para implementar un SGIA. Es una Norma de Sistema de Gestión (NSG) que utiliza la Estructura Armonizada (HLS), lo que permite su integración fluida con la ISO 27001 (Seguridad) o la ISO 9001 (Calidad).
*   **Metodología:** Basada en el ciclo de mejora continua PHVA (Planificar-Hacer-Verificar-Actuar).
*   **Alcance:** No certifica que un algoritmo concreto sea "ético" o "libre de sesgos", sino que la organización dispone de los procesos documentados, controles y auditorías necesarias para gobernar responsablemente sus actividades de IA.
*   **Novedad Específica (Evaluación de Impacto):** A diferencia de la ISO 27001 que evalúa riesgos *hacia la organización*, la ISO/IEC 42001 (Cláusula 6.1.4) exige evaluar el impacto del sistema de IA *hacia los individuos y la sociedad*, alineándose con la FRIA de la Ley de IA.

## Conceptos que suelen preguntarse

| Concepto / Distractor | Realidad Jurídica / Técnica |
| :--- | :--- |
| **FRIA vs. DPIA** | La FRIA (Ley IA) complementa a la DPIA (RGPD). No se sustituyen. |
| **"Usuario" en el AI Act** | El término jurídico correcto para quien usa la IA bajo su autoridad (ej. una Consejería) es **Responsable del Despliegue (*Deployer*)**. |
| **Tratamiento de Datos Sensibles** | Permitido excepcionalmente por el Art. 10.5 del AI Act con el fin exclusivo de **detectar y corregir sesgos** en sistemas de alto riesgo. |
| **Marcado CE** | Es obligación exclusiva del **Proveedor**, tras realizar la Evaluación de Conformidad (no es del Responsable del Despliegue). |
| **Cambio de Finalidad Sustancial** | Si el Responsable del Despliegue modifica sustancialmente el sistema y lo convierte en Alto Riesgo, asume el rol y las obligaciones de **Proveedor**. |
| **ISO/IEC 42001** | Certifica la **gobernanza de la organización** (SGIA), no certifica la seguridad a nivel de código de un modelo específico de IA. |
| **Retención de Logs (Responsable Despliegue)** | Periodo mínimo obligatorio de **6 meses** (Art. 26.6 AI Act). |

## Posibles preguntas tipo test

**Pregunta 1.** Según el Reglamento (UE) 2024/1689 (Ley de IA), ¿cuándo asume un "responsable del despliegue" (*deployer*) las obligaciones legales equivalentes a las de un "proveedor"?
A. Cuando ejecuta el sistema en servidores on-premises en lugar de en la nube.
B. Cuando modifica la finalidad prevista de un sistema de IA ya puesto en servicio, de tal manera que se convierta en un sistema de IA de alto riesgo.
C. Cuando designa al personal responsable de la supervisión humana del sistema.
D. Cuando el sistema procesa datos personales de categorías especiales.
**Respuesta correcta: B.** *(El Artículo 25 establece que un responsable del despliegue será considerado proveedor y asumirá sus obligaciones, como el Marcado CE, si modifica sustancialmente el sistema o cambia su finalidad).*

**Pregunta 2.** La Agencia para la Administración Digital desea implantar un sistema de IA de alto riesgo. Según el Art. 26 del Reglamento de IA, ¿cuál es el plazo mínimo predeterminado durante el cual la Agencia (como responsable del despliegue) debe conservar los archivos de registro (*logs*) generados automáticamente, siempre que estén bajo su control?
A. 30 días.
B. 6 meses.
C. 1 año.
D. 10 años.
**Respuesta correcta: B.** *(El Artículo 26.6 estipula explícitamente un periodo de retención de al menos seis meses para el responsable del despliegue).*

**Pregunta 3.** Si la Administración, como responsable del despliegue, está obligada a realizar una Evaluación de Impacto sobre los Derechos Fundamentales (FRIA) según el Art. 27 del AI Act, y el sistema también requiere una Evaluación de Impacto de Protección de Datos (EIPD/DPIA) según el Art. 35 del RGPD, ¿cuál es el procedimiento normativo establecido?
A. La FRIA sustituye y deroga la necesidad de realizar la EIPD para evitar duplicidades.
B. La EIPD sustituye a la FRIA, eximiendo de cumplir con la Ley de IA.
C. La FRIA complementará a dicha Evaluación de Impacto de Protección de Datos (EIPD).
D. Debe elegirse solo una de ellas a criterio del Delegado de Protección de Datos.
**Respuesta correcta: C.** *(El Artículo 27.4 de la Ley de IA establece la complementariedad de ambas evaluaciones, ya que evalúan espectros de riesgo diferentes pero interconectados).*

**Pregunta 4.** En relación a la norma ISO/IEC 42001 (Sistema de Gestión de Inteligencia Artificial), ¿cuál de las siguientes afirmaciones es correcta?
A. Es una guía técnica no vinculante y no certificable por una entidad externa.
B. Es una Norma de Sistema de Gestión (NSG) certificable, que especifica requisitos para establecer, implementar, mantener y mejorar un SGIA en la organización.
C. Su estructura difiere completamente de la ISO 27001, impidiendo su integración operativa.
D. Sustituye legalmente a la obligatoriedad de realizar el Marcado CE en la Unión Europea.
**Respuesta correcta: B.** *(La ISO 42001 es un estándar certificable (Tipo A) de estructura armonizada (HLS) que certifica la gestión organizativa, no sustituyendo las obligaciones legales del AI Act).*

**Pregunta 5.** De acuerdo con el Reglamento de IA (UE) 2024/1689, el uso de sistemas de identificación biométrica remota "en tiempo real" en espacios de acceso público con fines de garantía del cumplimiento del derecho (policiales) está calificado como:
A. Riesgo de Transparencia, requiriendo únicamente señalización visible.
B. Alto Riesgo, permitido libremente si el sistema cuenta con Marcado CE.
C. Riesgo inaceptable, sin posibilidad de excepción bajo ninguna circunstancia.
D. Riesgo inaceptable (Práctica prohibida), salvo excepciones tasadas, estrictamente necesarias y sujetas a autorización judicial previa o inminente.
**Respuesta correcta: D.** *(El Artículo 5 veta este uso con carácter general, abriendo una lista muy cerrada de excepciones).*

**Pregunta 6.** Según el Reglamento (UE) 2024/1689 (Ley de IA), ¿cuál de las siguientes obligaciones recae específicamente sobre los proveedores de Modelos de IA de Uso General (GPAI)?
A. Implementar la supervisión humana directa en cada inferencia del usuario final.
B. Elaborar y publicar un resumen suficientemente detallado del contenido utilizado para el entrenamiento del modelo.
C. Anonimizar obligatoriamente todos los datos de entrada en tiempo real.
D. Realizar una FRIA antes de su introducción en el mercado.
**Respuesta correcta: B.** *(Obligación explícita del Artículo 53 relacionada con la transparencia y los derechos de autor para modelos GPAI).*

## Normativa o fuentes relacionadas

*   **Reglamento (UE) 2024/1689 (Ley de Inteligencia Artificial):** Especialmente los Artículos 5 (Prácticas prohibidas), 6 (Clasificación Alto Riesgo), 10.5 (Datos sensibles para sesgos), 16 (Obligaciones Proveedor), 25 (Responsabilidades en cadena de valor), 26 (Obligaciones Responsable del despliegue), 27 (FRIA), 50 (Transparencia) y 53 (Modelos GPAI).
*   **Reglamento (UE) 2016/679 (RGPD):** Artículos 22 (Decisiones automatizadas), 25 (Privacidad desde el diseño) y 35 (EIPD).
*   **Ley Orgánica 3/2018 (LOPDGDD).**
*   **ISO/IEC 42001:2023:** *Information technology — Artificial intelligence — Management system*. Estándar internacional certificable para SGIA.

## Dudas o puntos pendientes

*   **Estatus y Plantilla de la FRIA:** La Ley de IA delega en la Oficina de IA el desarrollo de un "modelo de cuestionario" o plantilla para facilitar la FRIA (Art. 27). Hasta la publicación de dicho modelo oficial, las administraciones se guían por metodologías afines (como ALTAI de la UE o propuestas del Consejo de Europa) para documentar los seis elementos obligatorios del Art. 27.1.
*   **Jurisprudencia sobre Propiedad Intelectual en IAG:** La autoría de las obras generadas por IA es un área de vacío normativo (no resuelta por la LPI española, que exige autoría humana). Se esperan resoluciones judiciales a nivel europeo que clarifiquen si existen derechos sobre los *prompts* complejos o el contenido generado, y cómo aplicar efectivamente las excepciones de minería de textos y datos (TDM) de la Directiva UE 2019/790.