# DIAGRAMAS DE COMPORTAMIENTO: ESTADOS Y ACTIVIDADES

Además del Diagrama de Secuencia, el análisis funcional se completa con la visión del ciclo de vida del dato (Estados) y el flujo de trabajo (Actividades).



---

## 1. DIAGRAMA DE ESTADOS (LIFECYCLE)

**¿Cuándo usarlo?**
Fundamental para definir el ciclo de vida de la clase **`Expediente`** o **`Documento`**. Muestra cómo cambia el objeto según los eventos que ocurren.

### 1.1. Estados Típicos de un Expediente AGE
Dibuja una "Máquina de Estados" con estas fases:

1.  **Borrador:** El ciudadano está rellenando el formulario (aún no hay registro).
2.  **Iniciado/Registrado:** Se ha firmado y registrado. Ya existe legalmente (Fecha de Inicio).
3.  **En Instrucción:** El funcionario está revisando, pidiendo informes (PID) o validando.
4.  **En Subsanación:** Se ha pedido al ciudadano que corrija algo. El reloj del plazo se detiene (Suspensión de Plazos).
5.  **Resuelto:** Se ha firmado la Resolución.
6.  **Notificado:** Se ha puesto a disposición en la DEHú.
7.  **Archivado:** Se ha generado el Índice ENI, se ha cerrado y enviado a Archive.

> **Justificación para el examen:**
> *"El Diagrama de Estados modela el ciclo de vida del Expediente Administrativo, definiendo las transiciones legales (ej. de Instrucción a Resolución) y los eventos que las disparan (ej. Firma del Jefe de Servicio)."*

---

## 2. DIAGRAMA DE ACTIVIDADES (FLOWCHART)

**¿Cuándo usarlo?**
Es ideal para representar el **Procedimiento Administrativo** completo, mostrando decisiones, caminos paralelos y quién hace qué. Es muy parecido a un diagrama de flujo tradicional.



### 2.1. Elementos Clave
* **Calles (Swimlanes):** Dividen el diagrama en columnas verticales, una por Actor (Ciudadano | Sistema | Funcionario). **Esto es vital**.
* **Nodo de Decisión (Rombo):** Para bifurcaciones (ej. `¿Documentación Correcta?` -> SÍ/NO).
* **Barra de División/Unión (Fork/Join):** Para tareas en paralelo (ej. Mientras se valida la firma, se consulta la PID).

### 2.2. Ejemplo de Flujo
1.  **Calle Ciudadano:** Inicia Solicitud -> Firma.
2.  **Calle Sistema:** Valida Firma -> Registra (GEISER) -> Avanza flujo.
3.  **Calle Funcionario:** Revisa Documentos -> (Decisión: ¿Correcto?)
    * *NO:* Envía a Subsanar.
    * *SÍ:* Genera Propuesta Resolución.

> **Justificación:**
> *"El Diagrama de Actividades permite visualizar el flujo de trabajo (Workflow) transversal, identificando claramente las responsabilidades de cada actor mediante el uso de calles (swimlanes)."*

---