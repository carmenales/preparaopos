# MODELO DE DATOS Y PROTECCIÓN (CLASES Y RGPD)

En este apartado definimos la estructura estática de la información (Diagrama de Clases o Modelo E-R). Es el punto exacto donde debemos demostrar el cumplimiento del **ENI** (Estructura del Expediente) y del **RGPD** (Privacidad).

---

## 1. EL DIAGRAMA DE CLASES (ESTRUCTURA)

El Diagrama de Clases recoge los aspectos **estáticos** del sistema. Define qué "cosas" (entidades) vamos a gestionar y cómo se relacionan.

### 1.1. Clases Principales en un Supuesto AGE
En casi cualquier procedimiento administrativo, aparecerán estas clases. Debes dibujarlas o describirlas siempre:

1.  **Interesado (Ciudadano/Empresa):** Contiene datos personales (Nombre, DNI, Email).
2.  **Solicitud:** Contiene los datos del formulario de inicio.
3.  **Expediente:** La clase contenedora ("Carpeta").
4.  **Documento:** Los archivos (PDFs, XMLs) que forman el expediente.
5.  **Acto Administrativo (Resolución):** El resultado del trámite.

---

## 2. CUMPLIMIENTO DEL ENI (EL EXPEDIENTE ELECTRÓNICO)

Esta es la parte técnica más importante para subir nota. El **Esquema Nacional de Interoperabilidad (ENI)**, a través de su NTI de Expediente Electrónico, define estrictamente cómo debe ser la clase `Expediente`.

### 2.1. Estructura Obligatoria (Justificación para el Diagrama)
Al dibujar o describir la clase `Expediente`, debes mencionar explícitamente sus relaciones:

* **Relación de Agregación/Composición:** Un `Expediente` contiene (1..N) `Documentos`.
* **El Índice Electrónico (CLAVE):** Todo expediente debe tener obligatoriamente un **Índice**.
    * El Índice garantiza la **integridad** y el **orden** de los documentos.
    * **Firma del Índice:** El sistema debe generar una firma electrónica (normalmente un Sello de Órgano) sobre este Índice para cerrarlo y garantizar que nadie ha añadido o quitado papeles después.

> **Texto para el examen:**
> *"El modelo de datos cumple con la NTI de Expediente Electrónico. La clase 'Expediente' incluye una relación de composición con la clase 'Índice', el cual recoge la huella digital (hash) de todos los documentos foliados y es firmado electrónicamente por el sistema para garantizar su integridad."*



[Image of 3 tier deployment diagram with DMZ and firewalls]


---

## 3. CUMPLIMIENTO DEL RGPD (PRIVACIDAD DESDE EL DISEÑO)

El Reglamento General de Protección de Datos exige "Privacidad desde el Diseño". Esto significa que la seguridad se decide **antes** de crear la base de datos, no después.

### 3.1. Identificación de Datos Personales
Debes analizar los atributos de tus clases:

* **Datos Identificativos:** DNI, Nombre, Dirección (Riesgo Básico/Medio).
* **Datos Especiales (Art. 9 RGPD):** Salud, Biometría, Ideología, Religión (Riesgo Alto). *Ojo: Si el supuesto trata de Sanidad o Servicios Sociales, esto es crítico.*

### 3.2. Medidas de Diseño (Para mencionar en el texto)
Al describir el modelo de datos, añade estas justificaciones:

1.  **Minimización:** *"El modelo de datos solo incluye los atributos estrictamente necesarios para el trámite, cumpliendo el principio de minimización del RGPD."*
2.  **Seudonimización:** *"Si se van a realizar análisis estadísticos (ej. Cuadros de Mando), se crearán vistas de base de datos donde el DNI esté disociado o seudonimizado."*
3.  **Nivel de Seguridad (ENS):** *"Dado que la clase 'Interesado' almacena datos personales, el sistema hereda la necesidad de aplicar medidas de seguridad (cifrado de base de datos) correspondientes al nivel determinado en el Análisis de Riesgos."*

---

## 4. PLANTILLA DE RELACIONES UML

Usa estos términos técnicos al describir el diagrama:

* **Herencia (Es un...):**
    * *Ejemplo:* `Ciudadano` y `Empresa` heredan de la clase padre `Interesado`.
* **Composición (Es parte intrínseca de...):**
    * *Ejemplo:* El `DetalleLineaSolicitud` es parte de `Solicitud`. Si borras la solicitud, se borran las líneas.
* **Agregación (Forma parte de...):**
    * *Ejemplo:* Un `Documento` forma parte de un `Expediente`, pero el documento podría existir por sí solo antes de meterlo en la carpeta.

---

## 5. TÉCNICA PARA DEDUCIR CARDINALIDADES (TRUCO EXAMEN)

Si dudas al poner `1:N` o `M:N` en el Diagrama E/R, hazte estas dos preguntas cruzadas:

**Ejemplo: Funcionario --- Pertenece --- Departamento**

1.  **Pregunta de Ida:** ¿Un Funcionario a cuántos Departamentos pertenece como máximo?
    * *Respuesta:* A 1. (Pones un `1` en el lado Departamento).
2.  **Pregunta de Vuelta:** ¿Un Departamento cuántos Funcionarios tiene como máximo?
    * *Respuesta:* N (muchos). (Pones una `N` en el lado Funcionario).

**Resultado:** Relación **1:N**. (Un departamento tiene N funcionarios).

> **Consejo de Coherencia:** Revisa que los datos que guardas en el E-R sean suficientes para generar los **indicadores del Cuadro de Mando** que has propuesto en la otra pregunta. Si mides "Tiempos de Resolución", tu entidad `Expediente` debe tener `Fecha_Inicio` y `Fecha_Fin`.