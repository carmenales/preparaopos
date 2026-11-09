# MACRODATOS (BIG DATA) Y ANALÍTICA

Este archivo justifica la incorporación de soluciones de Big Data cuando el volumen, la velocidad o la variedad de los datos superan la capacidad de las bases de datos tradicionales.

---

## 1. ¿CUÁNDO PROPONER BIG DATA EN UN SUPUESTO?

No lo propongas "porque sí". Úsalo si el enunciado menciona:

* **Volumen masivo:** Logs de todos los ciudadanos, sensores IoT, redes sociales.
* **Análisis Predictivo:** Detección de fraude fiscal (AEAT), predicción de epidemias, análisis de comportamiento.
* **Datos no estructurados:** Análisis de texto libre, imágenes, vídeo.

---

## 2. ARQUITECTURA DE DATOS (EL LAGO DE DATOS)

Se propone una arquitectura complementaria al sistema transaccional:

1.  **Data Lake (Lago de Datos):** Repositorio centralizado donde se vuelca la información "en crudo" (Raw Data).
2.  **Procesamiento:**
    * **Batch (Por lotes):** Para informes mensuales (Tecnología: **Hadoop / Spark**).
    * **Streaming (Tiempo real):** Para alertas inmediatas (Tecnología: **Kafka / Spark Streaming**).
3.  **Visualización:** Cuadros de Mando avanzados (Tecnología: **PowerBI / Tableau** / Soluciones Open Source como **Kibana**).

---

## 3. OFICINA DEL DATO Y GOBIERNO

Es fundamental mencionar la **Oficina del Dato** de la AGE (Secretaría de Estado de Digitalización).

* **Objetivo:** Fomentar la compartición y el uso eficiente de los datos en la administración.
* **RISP:** Reutilización de la Información del Sector Público (Datos Abiertos).

---