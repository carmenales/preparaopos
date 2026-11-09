---
title: OWASP Transversal - Patrones Comunes y Específicos
---

# 🌐 OWASP Transversal: Patrones Comunes y Específicos

Al analizar las listas del OWASP Top 10 para Aplicaciones Web, Móviles, LLMs, Agentes de IA y Smart Contracts, se hace evidente que **los fundamentos de los ataques y las defensas comparten raíces profundas**, aunque la tecnología subyacente cambie. Proteger estos ecosistemas en la Administración requiere alinear las soluciones técnicas con el **ENS (RD 311/2022)** y el **RGPD/LOPDGDD**.

## 1. Riesgos y Mitigaciones Universales (Comunes)

Estos vectores de ataque atraviesan absolutamente todos los ecosistemas de software modernos.

### 1.1. Riesgos en la Cadena de Suministro (Supply Chain)
Todas las plataformas dependen de ecosistemas externos, heredando sus vulnerabilidades.

* **Riesgos:** 
    * Uso de bibliotecas de terceros desactualizadas o maliciosas en Web y SDKs vulnerables en Móvil. 
    * En IA, el riesgo recae en modelos base, plugins o servidores MCP comprometidos desde su origen.
* **Mitigaciones:** 
    * Mantener un inventario exhaustivo mediante **SBOM** o AI-SBOM. 
    * Usar proveedores verificados y auditar firmas digitales.
* **Normativa:** 
    * ENS 
        * `[op.exp.1]` Inventario de activos para el SBOM.
        * `[op.ext.3]` Protección de la cadena de suministro.
        * `[mp.sw.1]` Desarrollo de aplicaciones. 
    * RGPD `Art. 28` Garantías del Encargado del Tratamiento.
  
!!! note "Cómo justificarlo en el supuesto:"
    *Mantener actualizado un inventario de activos de software mediante un SBOM (Software Bill of Materials) revisándolo de forma continuada frente a vulnerabilidades, y evaluar los riesgos derivados de la cadena de suministro externa.*

### 1.2. Inyección y Falta de Validación de Entrada
*El principio de "toda entrada es maliciosa hasta que se demuestre lo contrario".*

* **Riesgos:** 
    * Inyección SQL o XSS en Web y Móvil. 
    * Direcciones de tokens envenenados o payloads corruptos en Smart Contracts.
    * Inyección de Prompts directa/indirecta y Subversión del Flujo de Intención (MCP) que altera los objetivos en modelos de IA.
* **Mitigaciones:** 
    * Tratar todo dato como no confiable (**Zero Trust**). 
    * Usar listas blancas (*allow-lists*), parametrización de consultas y sanitización. 
    * En IA, separar claramente el *System Prompt* del contenido del usuario y usar *parsers* de contexto.
* **Normativa:** 
    * ENS 
        * `[mp.sw.1]` Desarrollo de aplicaciones.
        * `[op.exp.6]` Protección frente a código dañino.

!!! note "Cómo justificarlo en el supuesto:"
    *Aplicar el principio de 'confianza cero' en las entradas, implementando sanitización estricta, listas blancas y consultas parametrizadas para garantizar un desarrollo de aplicaciones seguro frente a inyecciones de código dañino.*

### 1.3. Exceso de Privilegios y Fallos de Control de Acceso
Otorgar más permisos de los estrictamente necesarios es la principal puerta de compromiso.

* **Riesgos:** 
    * Invocación de funciones de administrador por usuarios rasos en Web (IDOR) y Smart Contracts. 
    * Permisos excesivos solicitados al SO en Móvil. 
    * "Agencia Excesiva" o *Scope Creep* en IA: el modelo toma decisiones destructivas sin supervisión.
* **Mitigaciones:** 
    * Aplicar el principio de **Mínimo Privilegio** (o *Mínima Agencia* en IA). 
    * Requerir aprobación humana (*Human-in-the-Loop*) para acciones críticas. 
    * Delegar autorizaciones siempre al backend seguro.
* **Normativa:** 
    * ENS 
        * `[op.acc.2]` Requisitos de acceso.
        * `[op.acc.3]` Segregación de funciones y tareas. 
    * RGPD `Art. 22` Decisiones automatizadas.

!!! note "Cómo justificarlo en el supuesto:"
    *Implementar un modelo basado en el Mínimo Privilegio y control de acceso a dispositivos, segregando funciones en el backend e imponiendo supervisión humana (Human-in-the-Loop) para evitar decisiones automatizadas de alto impacto.*

### 1.4. Comunicaciones, Criptografía Insegura y Almacenamiento
La protección de los datos en tránsito y en reposo sigue siendo un reto transversal.

* **Riesgos:** 
    * Uso de HTTP, algoritmos obsoletos (MD5, SHA1) o almacenamiento de credenciales en plano en Web y Móvil. 
    * Falta de cifrado entre agentes de IA (*spoofing*) o exposición de secretos en configuraciones MCP.
* **Mitigaciones:** 
    * Forzar siempre conexiones seguras (**HTTPS/mTLS**). 
    * Usar estándares criptográficos modernos apoyados en hardware (HSM, Keystore nativo) o gestores de secretos corporativos (Vaults).
* **Normativa:** 
    * ENS 
        * `[mp.com.2]` Protección de la confidencialidad.
        * `[mp.com.3]` Protección de la integridad y de la autenticidad.
        * `[mp.info.3]` Cifrado de la información en reposo.
    * RGPD `Art. 32` Seguridad del tratamiento.

!!! note "Cómo justificarlo en el supuesto:"
    *Asegurar la información garantizando su confidencialidad mediante protocolos robustos en tránsito (mTLS/HTTPS) y criptografía fuerte en reposo (AES-256) empleando contenedores nativos (Keystore) o soluciones tipo Vault.*

### 1.5. Sandboxing, Configuración Incorrecta y Manejo de Errores
Dejar puertas abiertas por fallos de diseño o durante el paso a producción.

* **Riesgos:** 
    * Credenciales por defecto, modo *debug* activado o trazas de error expuestas. 
    * Ejecución de código malicioso (RCE) por parte de agentes autónomos o llamadas externas no comprobadas en Blockchain.
* **Mitigaciones:** 
    * Automatizar el endurecimiento (*hardening*). 
    * Aplicar el principio de **"fallar cerrado" (*fail-closed*)** ante excepciones. 
    * Confinar la ejecución de herramientas de IA en entornos aislados (**Sandboxing**) y contenedores efímeros.
* **Normativa:** 
    * ENS 
        * `[op.exp.3]` Gestión de la configuración de seguridad.
        * `[op.acc.3]` Segregación de funciones y tareas.
        * `[mp.sw.1]` Desarrollo de aplicaciones.

!!! note "Cómo justificarlo en el supuesto:"
    *Realizar una gestión de la configuración segura mediante bastionado (hardening) previo al despliegue y garantizar que la ejecución de herramientas se segregue en entornos aislados (Sandboxing) bajo el principio de 'fallar cerrado'.*

### 1.6. Falta de Auditoría, Registro y Monitorización
El sistema carece de mecanismos proactivos para registrar eventos, dejando a los administradores "ciegos".

* **Riesgos:** 
    * Operar en "caja negra" sin historial de actividades críticas. 
    * Persistencia indetectada de atacantes o "Agentes Rebeldes" (*behavioral drift*) en IA.
* **Mitigaciones:** 
    * Registro exhaustivo centralizado en un SIEM. 
    * Monitorización de anomalías y alertas proactivas. 
    * *Precaución:* Sanitizar los logs para no registrar contraseñas o datos personales (PII) en claro.
* **Normativa:** 
    * ENS 
        * `[op.exp.8]` Registro de la actividad.
        * `[op.mon.1]` Detección de intrusión.
        * `[op.mon.3]` Vigilancia. 
    * RGPD `Art. 25` Privacidad por Diseño.

!!! note "Cómo justificarlo en el supuesto:"
    *Centralizar el registro de actividad en un SIEM para la vigilancia y detección de anomalías, asegurando el enmascaramiento previo de PII en los logs para cumplir con la Privacidad por Diseño.*


## 2. Vectores de Ataque Específicos por Dominio

Aunque existen fundamentos compartidos, cada arquitectura introduce vulnerabilidades exclusivas:

### 🔗 Ecosistema Web3 y Smart Contracts
Derivados de la inmutabilidad del código y el manejo directo de activos financieros.

* **Ataques de Reentrada (Reentrancy):** Llamadas recursivas para drenar fondos antes de actualizar saldos. 
    * Mitigado con el patrón **CEI (*Checks-Effects-Interactions*)**.
* **Préstamos Flash (*Flash Loans*):** Capital ilimitado temporal para magnificar errores. 
    * Mitigado con comprobaciones de **múltiples bloques**.
* **Manipulación de Oráculos:** Alterar el precio de un token en un exchange. 
    *  Mitigado usando oráculos descentralizados (Chainlink) y precios **TWAP**.
* **Vulnerabilidades de Proxys:** Malas configuraciones al intentar "actualizar" contratos inmutables. 
    * Mitigado asegurando **rutinas de configuración de un solo uso** (bloqueadas tras el despliegue) y previniendo **colisiones de almacenamiento** (añadiendo nuevas variables siempre al final, sin alterar el orden original).

!!! note "Cómo justificarlo en el supuesto:"
    *Exigir auditorías de código formales y análisis estático (SAST) previas al despliegue, e implementar patrones seguros de desarrollo como CEI, protección de rutinas de configuración inicial y el uso de billeteras multifirma (Multisig) para la gobernanza.*

### 2. Vectores de Ataque Específicos por Dominio

Aunque existen fundamentos compartidos, cada arquitectura introduce vulnerabilidades exclusivas que deben abordarse desde el diseño:

### 📱 Ecosistema Móvil (Android / iOS)

| Riesgo / Vulnerabilidad | Descripción del Impacto | Mitigación Principal |
|:---|:---|:---|
| **Protección insuficiente de binarios** | Ingeniería inversa o clonación de la app (*repackaging*). | Aplicar **ofuscación** y detección de *Tampering/Root/Jailbreak*. |
| **Controles de privacidad del SO inadecuados** | Fugas accidentales por capturas de pantalla en 2º plano o portapapeles. | **Enmascarar la pantalla** al pasar a segundo plano y limpiar portapapeles. |

### 🧠 Modelos de Lenguaje Masivo (LLMs)

| Riesgo / Vulnerabilidad | Descripción del Impacto | Mitigación Principal |
|:---|:---|:---|
| **Fuga del Prompt de Sistema** | Robo de instrucciones fundamentales y directrices ocultas. | Diseñar asumiendo que **el prompt no es secreto** (no incluir credenciales). |
| **Desinformación y Alucinaciones** | Confianza ciega del usuario en salidas falsas generadas por la IA (*overreliance*). | Arquitectura de **anclaje de datos (Grounding / RAG)** con fuentes veraces. |
| **Consumo Ilimitado (*Denial of Wallet*)**| Peticiones complejas que agotan las cuotas financieras o de cómputo. | Establecer **topes estrictos de tokens** y límites de velocidad (*rate limiting*). |

### 🤖 Inteligencia Artificial Agéntica y Protocolos MCP

| Riesgo / Vulnerabilidad | Descripción del Impacto | Mitigación Principal |
|:---|:---|:---|
| **Fallos en Cascada y Bucles** | Un error se propaga por la red de agentes al intentar corregirse a sí mismo (*self-looping*). | Implementar **cortacircuitos (*circuit breakers*)** y límites de iteraciones. |
| **Explotación de Confianza Humana** | Ingeniería social abusando del tono conversacional y persuasivo de la IA. | **Filtrado de persuasión** e indicadores visuales claros de interacción con IA. |
| **Sobre-compartición de Contexto** | Devolver información excesiva al LLM, mezclando o filtrando datos de otros usuarios. | Aplicar el principio de *Need-to-Know* y **filtrado de salida (*egress filtering*)**. |


## 3. Conceptos Clave en Arquitecturas de IA (2026)

### El Principio de "Mínima Agencia" (*Least Agency*)
Evolución del mínimo privilegio para sistemas autónomos. Consiste en otorgar al agente únicamente la capacidad de decisión y los permisos estrictamente necesarios. Se sostiene en 4 pilares:

1. **Limitación de herramientas (*Scoping*):** Restringir los plugins. (Ej. Si el agente solo debe leer métricas, su plugin no debe tener capacidad de borrado).
2. **Identidades separadas y trazables:** Asignar credenciales de servicio (Service Accounts) propias a cada agente, en lugar de heredar todos los permisos del usuario humano.
3. **Aprobación humana (*Human-in-the-Loop*):** Retirar la autonomía total en acciones de alto impacto (modificar producción, enviar emails). Requiere un "OK" humano.
4. **Aislamiento (*Sandboxing*):** Confinar la ejecución de herramientas o código generado en contenedores efímeros y aislados.

### El Patrón "Cápsula de Intención" (*Intent Capsule*)
Defensa diseñada para mitigar el **Secuestro del Objetivo (Goal Hijack)**. 

* **Qué es:** Actúa como un envoltorio inmutable alrededor de las instrucciones base del agente. 
* **Cómo funciona:** Obliga al agente a recordar y evaluar su mandato original en cada ciclo de ejecución, comparando su próxima acción planificada con esta "cápsula".


## Resumen para el Supuesto Práctico

| Caso | Vulnerabilidad | Mitigación | Normativa |
|:---|:---|:---|:---|
| *Se han alterado registros en la BD / o un agente de IA borra un fichero al leer un PDF malicioso.* | **Falta de Validación de Entrada / Injection** | Consultas parametrizadas, Listas Blancas (Allow-lists), Sanitización. | **ENS `[mp.sw.1]`, `[op.exp.6]`**. |
| *La aplicación ha sido comprometida a través de una librería open-source desactualizada o un plugin de IA.* | **Vulnerabilidad de Cadena de Suministro** | Generar y auditar un **SBOM**, escanear dependencias. | **ENS `[op.exp.1]`, `[mp.sw.1]`, `[op.ext.3]`**. |
| *Un Agente de IA decide autónomamente modificar la infraestructura cloud usando credenciales del administrador.* | **Agencia Excesiva / Abuso de Privilegios** | Principio de **Mínima Agencia**, Identidades separadas y obligar **Human-in-the-loop**. | **ENS `[op.acc.2]`, `[op.acc.3]` / RGPD Art. 22**. |
| *Se detecta ejecución de comandos de sistema a través de las herramientas de IA o llamadas no comprobadas.* | **Sandboxing / Ejecución Inesperada** | Ejecutar herramientas y código en entornos **aislados (Sandboxing)** / contenedores. | **ENS `[op.exp.3]`, `[op.acc.3]`, `[mp.sw.1]`**. |
| *La App móvil o Web revela en texto plano errores internos con rutas del servidor o contraseñas por defecto.* | **Configuración Incorrecta / Criptografía** | Endurecimiento (*Hardening*) automatizado, "Fallar cerrado", protocolos seguros. | **ENS `[op.exp.3]`, `[mp.com.2/3]`, `[mp.info.3]`**. |
| *El sistema de IA genera respuestas convincentes pero falsas, y un operador las usa para tomar decisiones.* | **Desinformación / Overreliance** | Arquitectura **RAG (Grounding)** con fuentes de verdad corporativas. | **RGPD Art. 5.1.d (Exactitud)**. |
| *Un Smart Contract se vacía porque un atacante pide retirar saldo iterativamente antes de que se actualice la variable.* | **Ataque de Reentrada (Reentrancy)** | Patrón **CEI (Checks-Effects-Interactions)** y modificadores seguros. | **ENS `[mp.sw.1]`**. |
| *Un Agente de IA entra en un bucle infinito intentando resolver un error, consumiendo 5.000€ en API.* | **Fallos en Cascada / Unbounded Consumption**| **Cortacircuitos (*Circuit Breakers*)**, límites estrictos de tokens e iteraciones. | **ENS `[mp.sw.1]`**. |
| *La App móvil ha sido destripada y se capturan pantallas con datos de ciudadanos circulando por ahí.* | **Privacidad Inadecuada / Binarios** | **Enmascarar pantalla** en 2º plano, no loguear PII, Ofuscación. | **RGPD Art. 25**. |
| *No se pueden depurar responsabilidades tras un incidente porque el sistema no guardó trazas de acceso.* | **Falta de Auditoría y Monitorización** | Registro centralizado en **SIEM** sanitizando datos sensibles, vigilancia activa. | **ENS `[op.exp.8]`, `[op.mon.1]`, `[op.mon.3]`**. |