---
id: "cm-ad-innovacion-y-transformacion-digital-tema-005-ens"
title: "Real Decreto 311/2022 - ENS"
type: "apunte"
status: "borrador"
processes:
  - "comunidad-madrid/administracion-digital/innovacion-y-transformacion-digital"
profiles:
  - "p06-ingeniero-desarrollo"
official_profiles:
  - "P06 - Ingeniero de Desarrollo"
official_topic: "Tema 5. Real Decreto 311/2022, de 3 de mayo, por el que se regula el Esquema Nacional de Seguridad"
source_ids: []
tags:
  - "ens"
  - "esquema-nacional-de-seguridad"
  - "rd-311-2022"
  - "principios-basicos"
  - "disposiciones-generales"
  - "medidas-seguridad"
  - "ccn-cert"
created_at: "2026-09-09"
last_reviewed: "2026-09-09"
ai_generated: true
ai_sources:
  - "perplexity"
  - "chatgpt"
  - "gemini"
needs_human_review: true
---

# Tema 5. Real Decreto 311/2022, de 3 de mayo, por el que se regula el Esquema Nacional de Seguridad

## 1. Capítulo I. Disposiciones Generales

**Objeto**
El Real Decreto 311/2022 regula el Esquema Nacional de Seguridad (ENS), establecido en el artículo 156.2 de la Ley 40/2015, de 1 de octubre, de Régimen Jurídico del Sector Público. El ENS determina la política de seguridad en la utilización de medios electrónicos, constituida por los principios básicos y requisitos mínimos necesarios para una protección adecuada de la información tratada y los servicios prestados. Su finalidad es asegurar el acceso, la confidencialidad, la integridad, la trazabilidad, la autenticidad, la disponibilidad y la conservación de los datos. 

**Ámbito de aplicación**
El ENS resulta de aplicación obligatoria a los siguientes supuestos:
*   **Sector Público:** En los términos definidos por el artículo 2 de la Ley 40/2015.
*   **Sistemas con información clasificada:** Aplicable sin perjuicio de la Ley 9/1968, de 5 de abril, de Secretos Oficiales, admitiéndose medidas complementarias derivadas de compromisos internacionales.
*   **Sector Privado:** Aplicable a los sistemas de información de las entidades del sector privado cuando presten servicios o provean soluciones a las entidades del sector público vinculados al ejercicio de competencias y potestades administrativas. La entidad privada debe contar con una política de seguridad aprobada por su máximo órgano ejecutivo, y los pliegos de contratación exigirán la conformidad con el ENS (extensible a su cadena de suministro según el análisis de riesgos).
*   **Redes y servicios 5G:** Su instalación y explotación por el sector público requiere la aplicación conjunta del ENS y del Real Decreto-ley 7/2022, de 29 de marzo.

**Sistemas de información que traten datos personales**
Se aplicará directamente el Reglamento (UE) 2016/679 (RGPD), la Ley Orgánica 3/2018 (LOPDGDD) y la Ley Orgánica 7/2021. En caso de discrepancia, prevalecerán las medidas resultantes del análisis de riesgos o evaluación de impacto en materia de protección de datos frente a las del ENS, únicamente si resultan ser más agravadas o estrictas.

## 2. Capítulo II. Principios Básicos

La seguridad de la información se rige imperativamente por siete principios básicos:

1.  **Seguridad como un proceso integral:** Constituido por todos los elementos humanos, materiales, técnicos, jurídicos y organizativos. Excluye actuaciones puntuales o coyunturales, exigiendo concienciación a todos los niveles para evitar que la ignorancia o falta de coordinación constituyan fuentes de riesgo.
2.  **Gestión de la seguridad basada en los riesgos:** El análisis y gestión de riesgos es una actividad continua y actualizada que permite mantener un entorno controlado, minimizando riesgos a niveles aceptables mediante una aplicación proporcionada de medidas.
3.  **Prevención, detección, respuesta y conservación:** Exige un ciclo continuo que abarca medidas de prevención (disuasión y reducción de exposición), detección proactiva de ciberincidentes, respuesta oportuna para la restauración de servicios, y conservación para garantizar la disponibilidad durante todo el ciclo vital de la información digital.
4.  **Existencia de líneas de defensa:** Implementación de una estrategia de defensa en profundidad constituida por múltiples capas (organizativas, físicas y lógicas). Si una capa es comprometida, se reduce la probabilidad de compromiso global.
5.  **Vigilancia continua:** Detección de actividades o comportamientos anómalos para una respuesta oportuna.
6.  **Reevaluación periódica:** Las medidas de seguridad se evaluarán y actualizarán periódicamente, permitiendo replanteamientos de la arquitectura de seguridad si la evolución de los riesgos lo exige.
7.  **Diferenciación de responsabilidades:** En los sistemas de información deben encontrarse estrictamente diferenciadas las figuras de: Responsable de la información, Responsable del servicio, Responsable de la seguridad y Responsable del sistema. La responsabilidad de la seguridad debe estar segregada de la responsabilidad sobre la explotación operativa.

## 3. Categorización de los Sistemas de Información (Anexo I)

La categoría de seguridad de un sistema modula el esfuerzo de seguridad requerido bajo el principio de proporcionalidad, basándose en la valoración del impacto que tendría un incidente en las siguientes dimensiones de seguridad: Confidencialidad [C], Integridad [I], Trazabilidad [T], Autenticidad [A] y Disponibilidad [D].

**Niveles de impacto por dimensión:**
*   **BAJO:** Perjuicio limitado sobre las funciones, los activos o los individuos.
*   **MEDIO:** Perjuicio grave (reducción significativa de la capacidad, daño significativo a activos, incumplimiento material de ley).
*   **ALTO:** Perjuicio muy grave (anulación efectiva de la capacidad, daño irreparable, incumplimiento grave de la ley).

**Determinación de la categoría global del sistema:**
*   **ALTA:** Si alguna de sus dimensiones alcanza el nivel ALTO.
*   **MEDIA:** Si alguna de sus dimensiones alcanza el nivel MEDIO, y ninguna el ALTO.
*   **BÁSICA:** Si alguna dimensión alcanza el nivel BAJO, y ninguna es superior.

## 4. Requisitos Mínimos y Medidas de Seguridad (Anexo II)

Para el cumplimiento del ENS, las entidades deben aprobar una **Política de Seguridad** que incluya objetivos, marco regulatorio, roles, estructura del comité de seguridad y directrices de documentación. Las medidas de seguridad exigibles se estructuran en tres grandes marcos:

### 4.1 Marco Organizativo [org]
Conjunto de medidas relacionadas con la organización global de la seguridad de la entidad.
*   **[org.1] Política de seguridad:** Documento fundacional aprobado por el órgano competente.
*   **[org.2] Normativa de seguridad:** Documentos que describen el uso correcto de equipos y la responsabilidad del personal.
*   **[org.3] Procedimientos de seguridad:** Detalle operativo de la ejecución de tareas, responsabilidades y tratamiento de la información.
*   **[org.4] Proceso de autorización:** Control formal para el uso de instalaciones, entrada en producción de equipos/aplicaciones, interconexiones y uso de medios portátiles.

### 4.2 Marco Operacional [op]
Medidas destinadas a proteger la operación del sistema como conjunto integral.
*   **[op.pl] Planificación:** Análisis de riesgos, arquitectura de seguridad, adquisición de componentes, gestión de la capacidad y uso de componentes certificados (Catálogo CPSTIC del CCN).
*   **[op.acc] Control de acceso:** Requisitos de identificación y autenticación. Establece el principio de mínimo privilegio y la necesidad de segregación de funciones. Distingue requisitos estrictos de autenticación, incluyendo el uso de doble factor y certificados cualificados, especialmente desde zonas no controladas.
*   **[op.exp] Explotación:** Inventario de activos, gestión de la configuración (regla de funcionalidad mínima y seguridad por defecto), mantenimiento, gestión de cambios, protección frente a código dañino (EDR, listas blancas), gestión de incidentes y registro de actividad (trazabilidad y sincronización de relojes).
*   **[op.ext] Recursos externos:** Acuerdos de nivel de servicio (SLA), protección de la cadena de suministro e interconexión de sistemas.
*   **[op.nub] Servicios en la nube:** Protección específica para modelos SaaS, PaaS e IaaS, exigiendo certificaciones y configuraciones acordes a las guías CCN-STIC.
*   **[op.cont] Continuidad del servicio:** Análisis de impacto (BIA), plan de continuidad de negocio (BCP), pruebas periódicas y previsión de medios alternativos.
*   **[op.mon] Monitorización:** Herramientas de detección de intrusión (IDS/IPS), sistemas de métricas y vigilancia continua mediante recolección y correlación de eventos (SIEM).

### 4.3 Medidas de Protección [mp]
Enfocadas a salvaguardar activos concretos según su naturaleza y exigencia de nivel.
*   **[mp.if] Instalaciones e infraestructuras:** Áreas separadas, control de acceso físico, energía eléctrica redundante y protección frente a incendios/inundaciones.
*   **[mp.per] Gestión del personal:** Caracterización del puesto, deberes, obligaciones, concienciación y formación continua.
*   **[mp.eq] Equipos:** Puesto de trabajo despejado y bloqueado, protección avanzada de dispositivos portátiles (cifrado de disco) y control de dispositivos conectados a la red (IoT, BYOD).
*   **[mp.com] Comunicaciones:** Establecimiento de un perímetro seguro (cortafuegos, DMZ), protección de la confidencialidad (VPN, IPsec) y segmentación lógica/física de redes (VLANs).
*   **[mp.si] Soportes de información:** Marcado, criptografía (algoritmos autorizados por CCN), custodia, transporte, borrado seguro y destrucción de soportes.
*   **[mp.sw] Aplicaciones informáticas:** Separación de entornos (desarrollo, preproducción y producción), metodología de desarrollo seguro (DevSecOps) y pruebas de aceptación.
*   **[mp.info] Información:** Calificación de la información, protección de datos personales, firma electrónica, sellos de tiempo, limpieza de metadatos y copias de seguridad probadas.
*   **[mp.s] Servicios:** Protección del correo electrónico (antispam, antimalware), protección de aplicaciones web (WAF, prevención de inyecciones) y mitigación de denegación de servicio (DoS/DDoS).

## 5. Auditoría, Gobernanza y Respuesta a Incidentes

**Auditoría de Seguridad (Artículo 31 y Anexo III)**
*   Los sistemas de información deben someterse a una auditoría regular ordinaria al menos **cada dos años** para verificar el cumplimiento del ENS.
*   Con carácter extraordinario, se realizará auditoría siempre que se produzcan modificaciones sustanciales en los sistemas.
*   En sistemas de categoría BÁSICA, la auditoría puede sustituirse por una autoevaluación documentada. En categorías MEDIA y ALTA se requiere auditoría externa formal.
*   El Informe Nacional del Estado de la Seguridad (INES) consolida la información anual de todas las Administraciones Públicas a través del CCN.

**Respuesta a Incidentes y el CCN-CERT (Artículos 33 y 34)**
*   La capacidad técnica de respuesta se articula en torno al **CCN-CERT** (Computer Emergency Response Team del Centro Criptológico Nacional).
*   Las entidades del sector público están obligadas a notificar al CCN-CERT aquellos incidentes que tengan un impacto significativo en la seguridad de sus sistemas.
*   El CCN-CERT coordina la respuesta a nivel nacional, emite directrices técnicas (Guías CCN-STIC) y establece las alertas sobre vulnerabilidades y ciberamenazas avanzadas.
*   Tras un incidente grave, el CCN-CERT determinará técnicamente el riesgo de reconexión del sistema afectado y dictará las salvaguardas a implementar para su reactivación segura.
