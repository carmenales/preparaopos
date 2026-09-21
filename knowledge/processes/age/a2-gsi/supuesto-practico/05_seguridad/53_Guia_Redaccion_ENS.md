# 1.1 ESQUEMA NACIONAL DE SEGURIDAD (ENS)

**Objetivo:** Saber aplicar el ENS a una solución técnica en un examen, tanto tipo test como en el supuesto práctico.

## ¿Qué es el ENS?
El ENS es el marco obligatorio que regula la seguridad de los sistemas de información del sector público.

Se establece en el:

* **Real Decreto 311/2022** (vigente, sustituye al RD 3/2010).

Su finalidad principal es:
> Garantizar que todos los servicios electrónicos de las AAPP se presten con la seguridad adecuada, protegiendo la información y los servicios.

## Dónde aplica (clave para examen)
El ENS aplica a:

* Administración General del Estado
* CCAA, EELL
* Organismos públicos
* Entidades de derecho público
* **Empresas contratistas** cuando desarrollan o explotan sistemas públicos (Esto último cae muy frecuentemente en preguntas).

## Principios básicos del ENS
Los candidatos suelen confundirse, pero hay que saberse la lista. Los principios del ENS son:

1. Seguridad integral
2. Gestión de riesgos
3. Prevención, reacción y recuperación
4. Funciones diferenciadas
5. Revaluación periódica
6. Seguridad por defecto
7. Línea de defensa múltiple
8. Sección de medidas proporcionada
9. Mejora continua

En examen se suelen preguntar por ambigüedad en redacciones.

## Seguridad en dimensiones (IMPORTANTÍSIMO)
Todo sistema en ENS debe asegurar:

* Confidencialidad
* Integridad
* Disponibilidad
* Autenticidad
* Trazabilidad

Muchas preguntas del práctico piden justificar un diseño, un control, o un mecanismo usando estas palabras.

**Ejemplo de frase tipo:**
> Para garantizar trazabilidad según el ENS se habilitará el registro de actividad (AU-01), protegido contra alteraciones y con conservación mínima conforme a NTI.

## Clasificación de los sistemas
El ENS clasifica cada servicio en 3 niveles:

* Básico
* Medio
* Alto

En función del impacto que produzca una brecha de seguridad en las 5 dimensiones. En supuesto práctico debemos indicar el nivel, aunque sea aproximado.

**Texto tipo:**
> Dada la naturaleza del servicio y el impacto sobre datos personales y continuidad, el sistema se clasificaría como nivel Medio.

## Medidas del ENS (qué hay que saber para examen)
El ENS organiza sus medidas en 3 grandes bloques:

### Marco organizativo
Ejemplos:

* Política de seguridad
* Roles y responsabilidades
* Comité de seguridad
* Formación
* Clasificación de información

### Marco operativo
Ejemplos:

* Análisis y gestión de riesgos
* Control de cambios
* Plan de continuidad
* Registro de actividad
* Gestión de incidentes

### Medidas de protección
Ejemplos:

* Acceso
* Autenticación
* Cifrado
* Integridad
* Hardening
* Protección de red

Para examen no hace falta memorizar todas, pero sí:

* Las más citadas en preguntas
* Saber justificar soluciones mediante medidas ENS

## Cómo aplicar el ENS en un supuesto práctico
Este es el punto clave del examen. Se espera que:

* Plantees el sistema
* Identifiques los riesgos
* Asignes medidas ENS coherentes
* Justifiques por qué esas medidas

**Estructura de respuesta recomendada:**

**Paso 1 – Indicar que el sistema debe cumplir ENS**
> El sistema deberá alinearse con el ENS según RD 311/2022 al tratarse de un servicio electrónico prestado en el sector público.

**Paso 2 – Definir nivel estimado**
> Dado que el servicio gestiona datos personales y se presta 24x7, el impacto obliga a un nivel de seguridad Medio.

**Paso 3 – Aplicar controles ENS**
Ejemplos habituales en desarrollo:

| Objetivo | Medida ENS |
| :--- | :--- |
| Autenticación de usuarios | RA-02 – autenticación reforzada |
| Control de acceso | AC-01 / AC-02 |
| Registro y trazabilidad | AU-01 – registro de actividad |
| Integridad del código | OP-01 – control de cambios |
| Cifrado en tránsito | SC-03 – protección de comunicaciones |
| Separación de entornos | OP-02 |
| Auditoría | AU-02 |

**Texto tipo:**
> Para garantizar la trazabilidad se habilitará registro de actividad (AU-01), conservado según NTI de Política de Gestión de Documentos Electrónicos.

**Paso 4 – Integrarlo con el diseño técnico**
Ejemplo para una aplicación móvil (AEAT, Seguridad Social, etc.):
> La aplicación móvil se comunicará mediante API REST cifrada (SC-03) y cada petición incluirá token de sesión autenticado por Cl@ve (RA-02), asegurando autenticidad e integridad.

Este tipo de redacción sube automáticamente la nota.

## Controles ENS que se deben mencionar casi siempre
En el supuesto práctico, aunque sea breve, suelen sumar:

* Autenticación reforzada
* Control de accesos
* Separación de entornos
* Registro de actividad
* Cifrado
* Gestión de incidentes
* Copias de seguridad
* Continuidad y recuperación

**Con una frase así:**
> Se establecerá un control de acceso basado en roles (AC-02), registro de actividad (AU-01), cifrado TLS (SC-03), gestión de incidentes y separación completa de entornos (OP-02) para evitar accesos no autorizados.

## ENS + Desarrollo Seguro
Cuando el examen mezcla ENS + desarrollo de software, lo que suele querer es:

* Validación de entrada
* Controles anti-inyección
* Gestión de errores sin mostrar información sensible
* Registro centralizado
* Revisiones de código
* Análisis automatizado (DevSecOps)

**Frase que funciona muy bien:**
> Siguiendo el ENS se establecerán prácticas de desarrollo seguro, incluyendo validación exhaustiva de entrada, análisis estático y dinámico de código y pruebas de seguridad antes del paso a producción.

## ENS y DevOps
El ENS encaja perfectamente con CI/CD. Cosas que suman puntos:

* Pipeline automático
* Firma de artefactos
* Control de versiones
* Trazabilidad de despliegues
* Inventario de componentes

**Frase tipo:**
> Cada versión quedará inventariada y firmada digitalmente, garantizando trazabilidad y control de cambios conforme al ENS (OP-01).

## ENS y diagramas UML
Si en el mismo supuesto hay un diagrama de despliegue, el ENS puede aparecer en:

* Cifrado de comunicaciones (flechas HTTPS)
* Cortafuegos
* DMZ
* Nodo de auditoría
* Logs centralizados

**Ejemplo de cómo justificarlo:**
> El nodo de registro centralizado permite cumplir la medida AU-01 de trazabilidad, evitando manipulación local de logs.

Esto sube la puntuación automáticamente.

## Preguntas tipo test frecuentes del ENS
Las más típicas:

* Saber que el RD 311/2022 sustituyó al RD 3/2010
* Saber que aplica también a contratistas
* Identificar dimensiones de seguridad
* Clasificación (básico / medio / alto)
* Medidas del marco organizativo / operativo / protección
* Qué significa “seguridad por defecto”
* Qué es trazabilidad en ENS

---

# Ejemplo real de cómo meter ENS en una respuesta

## Contexto del supuesto
**Pregunta típica:**
“Elabore la respuesta al diseño de una aplicación web para la tramitación electrónica de solicitudes de ayudas, destinada a usuarios ciudadanos, indicando aspectos técnicos, de seguridad y normativa aplicable.”

## Ejemplo de fragmentos que podrías contestar en el examen

**1. Al justificar la arquitectura:**
> La solución propuesta se desarrollará siguiendo una arquitectura multicapa (presentación, lógica de negocio y persistencia), desplegada en la infraestructura corporativa y cumpliendo los requisitos de seguridad establecidos por el Esquema Nacional de Seguridad (ENS), garantizando la disponibilidad, integridad, confidencialidad, autenticidad, trazabilidad y conservación de la información tratada.

**2. Al tratar control de accesos y usuarios**
> El acceso a la aplicación se realizará mediante identificación y autenticación de usuarios conforme al ENS y utilizando los servicios comunes de la AGE, como:
> 
> * Clave para autenticación,
> * @firma o FIRe para firma electrónica avanzada,
> * Registro de actividad y trazabilidad según las medidas del ENS.

**3. Al justificar medidas de seguridad concretas**
> Siguiendo el ENS, se aplicarán medidas técnicas tales como:
> 
> * Control de acceso reforzado,
> * Cifrado de comunicaciones mediante TLS,
> * Registro y monitorización de eventos,
> * Gestión de copias de seguridad,
> * Gestión de vulnerabilidades y parches, acordes al nivel de seguridad resultante del análisis de riesgos del sistema.

**4. Al mencionar documentación y ciclo de vida**
> La documentación del sistema incluirá la Declaración de Aplicabilidad, el Informe del Estado de Seguridad, el Plan de Adecuación al ENS, así como el registro de incidencias y evidencias derivadas del proceso continuo de mantenimiento y mejora, en cumplimiento del principio de mejora continua exigido por el ENS.

**5. Si quieres citar que todo desarrollo debe alinearse con la organización**
> El sistema se integrará en el SGSI corporativo y cumplirá con el Real Decreto 311/2022, que desarrolla el ENS, garantizando que todas las medidas adoptadas son proporcionales al riesgo y se mantienen actualizadas durante todo el ciclo de vida del servicio digital.

**6. Metiendo ENS si te preguntan por pruebas o calidad**
> En el proceso de pruebas se incluirán controles de seguridad como:
> 
> * Pruebas de penetración,
> * Análisis de vulnerabilidades,
> * Verificación de trazabilidad de acciones,
> * Verificación de los controles ENS definidos para el nivel del sistema.

**7. Meterlo en una frase “comodín” válida para casi cualquier pregunta**
> Todas las decisiones adoptadas se realizarán en cumplimiento del Esquema Nacional de Seguridad, asegurando que el sistema mantiene un nivel adecuado de protección de los activos, proporcional a los riesgos y alineado con la política de seguridad del organismo.

## Resultado
Si metes 3–5 frases como estas repartidas por la respuesta:

* Suena completamente real,
* Da la impresión de absoluta solvencia técnica,
* Demuestra que respetas normativa,
* Y suma puntos aunque el resto del examen esté más flojo.