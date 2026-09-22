# DIAGRAMA DE FLUJO DE DATOS (DFD)

El DFD muestra cómo se mueve la información a través del sistema. En el examen, suelen pedir el **Diagrama de Contexto (Nivel 0)** o la **Descomposición en Subsistemas (Nivel 1)**.

---

## 1. DFD NIVEL 0 (DIAGRAMA DE CONTEXTO)

* **Objetivo:** Definir los límites del sistema.
* **Elemento Central:** Una única burbuja (proceso) llamada "SISTEMA X".
* **Entidades Externas:** Cuadrados alrededor (Ciudadano, Cl@ve, Registro, AEAT).
* **Flujos:** Flechas que entran y salen (Solicitud, Recibo, Consulta Datos).

*(Nota: Este diagrama ya está conceptualizado en el archivo `10_Actores_Necesidades.md`, pero aquí se formaliza la técnica).*

---

## 2. DFD NIVEL 1 (SUBSISTEMAS)

Aquí "explotamos" la burbuja central del Nivel 0 para ver qué hay dentro.



### 2.1. Elementos a Dibujar
1.  **Procesos (Burbujas):** Representan las funciones principales.
    * `1.0 Gestión de Usuarios` (Autenticación).
    * `2.0 Tramitación` (Validación y Lógica).
    * `3.0 Gestión Documental` (Generación y Guardado).
    * `4.0 Notificación` (Comunicación).
2.  **Almacenes de Datos (Líneas paralelas):** Dónde se guardan los datos en reposo.
    * `D1. Expedientes`
    * `D2. Terceros/Interesados`
    * `D3. Catálogo Trámites`
3.  **Flujos (Flechas):** Conectan procesos y almacenes.

### 2.2. Ejemplo de Flujo (Texto para Examen)
> *"El proceso '1.0 Gestión de Usuarios' recibe las credenciales del 'Ciudadano', consulta la identidad en 'Cl@ve' y, si es correcta, pasa el control al proceso '2.0 Tramitación'. Este proceso almacena la solicitud en 'D1. Expedientes' y solicita al proceso '3.0 Gestión Documental' la generación del recibo."*

---