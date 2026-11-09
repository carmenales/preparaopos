---
title: Análisis y Gestión de Riesgos (MAGERIT)
---

El análisis de riesgos consiste en el estudio de las posibles amenazas, así como
los daños que estas puedan producir en los activos de la organización.

Para la evaluación de riesgos se utilizará la metodología **MAGERIT v3**
por ser el estándar oficial y la más extendida en la Administración. Para facilitar su realización y automatización, se utilizará la familia de herramientas **PILAR / MicroPILAR** del CCN-CERT, que está plenamente adaptada al ENS (RD 311/2022).

Los pasos a seguir serán determinar:

1. **Activos:** elementos relevantes para la organización (servicios, información, etc.).
2. **Amenazas:** causa potencial de un incidente que puede causar daños en los activos.
3. **Vulnerabilidad:** defecto o debilidad de un activo que habilita o facilita la materialización de una amenaza.
4. **Impacto:** consecuencia (daño) que sobre un activo tiene la materialización de una amenaza.
5. **Riesgo:** estimación del grado de exposición a que una amenaza se materialice (probabilidad x impacto).

*(Nota: Tras el cálculo del Riesgo, se pasa a la fase de **Tratamiento del Riesgo**, donde se decide si el riesgo se: Mitiga (aplicando salvaguardas/medidas del ENS), Acepta, Evita o Transfiere).*

### Clasificación de Activos

Los activos se clasifican en:

* **Esenciales:**
    * Servicios.
    * Información.
* **Subordinados:**
    * Datos que materializan la información.
    * Servicios auxiliares que se necesitan para poder organizar el sistema.
    * Aplicaciones informáticas (software) que permiten manejar los datos.
    * Equipos informáticos (hardware) que permiten hospedar datos, aplicaciones y servicios.
    * Soportes de información (dispositivos de almacenamiento de datos).
    * Equipamiento auxiliar que complementa el material informático (SAI, climatización).
    * Redes de comunicaciones que permiten intercambiar datos.
    * Instalaciones que acogen equipos informáticos y de comunicaciones.
    * Personas que explotan u operan todos los elementos anteriores.

### Dimensiones de Seguridad (ENS)

El impacto y el riesgo se evalúan en base a las dimensiones de seguridad definidas por el ENS:

* **[C] Confidencialidad:** Que la información no llegue a personas no autorizadas.
* **[I] Integridad:** Que la información no sea alterada de forma no autorizada.
* **[T] Trazabilidad:** Que se pueda rastrear quién hizo qué y cuándo.
* **[A] Autenticidad:** Que se pueda garantizar quién es el origen de los datos.
* **[D] Disponibilidad:** Que los servicios/datos estén accesibles cuando se requieran.

### Ejemplo de Matriz de Riesgos

| Activo | Amenaza | Vulnerabilidad | Impacto | Riesgo | Dimensión |
|--------|---------|----------------|---------|--------|-----------|
| Subsistema A | Que los organismos no cumplan la obligación | Baja | Alto | Medio | D |
| ^ | Problemas de sincronización | Baja | Medio | Medio | A, C, I, D |
| ^ | Código dañino en los datos (Malware) | Baja | Medio | Medio | C, I, D |
| Subsistema B | Suplantación de identidad del usuario | Baja | Medio | Medio | A, C, I |
| ^ | Ataques externos | Media | Medio | Medio | D |
| ^ | Corrupción de datos | Baja | Bajo | Medio | A, I |
| Información | Manipulación o perdida de datos | Media | Medio | Medio | I, D, T |
| ^ | Destrucción de la información | Media | Alto | Medio | D |
| Comms y Hardware | Desastres naturales | Baja | Alto | Medio | I, D, T |
| ^ | Caídas de las redes | Media | Bajo | Medio | D |
| ^ | Interceptación de información (Sniffing) | Media | Medio | Bajo | C |
| Sistemas externos | Interrupción de los servicios | Media | Alto | Alto | D |

# [Ejemplos de amenazas](https://www.ccn-cert.cni.es/documentos-publicos/1791-magerit-libro-ii-catalogo/file.html)

> *(Clasificación según el Catálogo de Elementos de MAGERIT)*

1. **Desastres naturales**
    1. Fuego
    2. Daños por agua
    3. Desastres naturales
2. **De origen industrial**
    1. Fuego
    2. Daños por agua
    3. Desastres industriales
    4. Contaminación mecánica
    5. Contaminación electromagnética
    6. Avería de origen físico o lógico
    7. Corte del suministro eléctrico
    8. Condiciones inadecuadas de temperatura o humedad
    9. Fallo de servicios de comunicaciones
    10. Interrupción de otros servicios y suministros esenciales
    11. Degradación de los soportes de almacenamiento de la información
    12. Emanaciones electromagnéticas
3. **Errores y fallos no intencionados**
    1. Errores de los usuarios
    2. Errores del administrador
    3. Errores de monitorización (log)
    4. Errores de configuración
    5. Deficiencias en la organización
    6. Difusión de software dañino
    7. Errores de [re-]encaminamiento
    8. Errores de secuencia
    9. Escapes de información
    10. Alteración accidental de la información
    11. Destrucción de información
    12. Fugas de información
    13. Vulnerabilidades de los programas (software)
    14. Errores de mantenimiento / actualización de programas (software)
    15. Errores de mantenimiento / actualización de equipos (hardware)
    16. Caída del sistema por agotamiento de recursos
    17. Pérdida de equipos
    18. Indisponibilidad del personal
4. **Ataques intencionados**
    1. Manipulación de los registros de actividad (log)
    2. Manipulación de la configuración
    3. Suplantación de la identidad del usuario
    4. Abuso de privilegios de acceso
    5. Uso no previsto
    6. Difusión de software dañino
    7. [Re-]encaminamiento de mensajes
    8. Alteración de secuencia
    9. Acceso no autorizado
    10. Análisis de tráfico
    11. Repudio
    12. Interceptación de información (escucha)
    13. Modificación deliberada de la información
    14. Destrucción de información
    15. Divulgación de información
    16. Manipulación de programas
    17. Manipulación de los equipos
    18. Denegación de servicio (DoS / DDoS)
    19. Robo
    20. Ataque destructivo
    21. Ocupación enemiga
    22. Indisponibilidad del personal
    23. Extorsión (Ransomware)
    24. Ingeniería social (picaresca / Phishing)