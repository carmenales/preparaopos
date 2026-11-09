# COMPORTAMIENTO DINÁMICO: DIAGRAMA DE SECUENCIA

El Diagrama de Secuencia describe la interacción de los objetos en el tiempo. En un supuesto de la AGE, su función principal es mostrar **cómo el sistema orquesta las llamadas a los Servicios Comunes** (Cl@ve, Firma, Registro).



---

## 1. ELEMENTOS DEL DIAGRAMA (VOCABULARIO VISUAL)

Al dibujar el diagrama, utiliza estos elementos estándar UML:

1.  **Actores (Humanos):** Representados con un "monigote" a la izquierda (ej. Ciudadano).
2.  **Líneas de Vida (Objetos/Sistemas):** Cajas en la parte superior con una línea discontinua hacia abajo.
    * **Objetos Internos:** `PortalWeb`, `ControladorTramite`, `GestorExpediente`.
    * **Sistemas Externos (Actores):** `Cl@ve`, `FIRe`, `GEISER`, `Notifica`.
3.  **Mensajes:**
    * **Síncronos (Flecha llena):** El sistema espera respuesta (ej. Validar Usuario).
    * **Asíncronos (Flecha abierta):** El sistema envía y sigue trabajando (ej. Enviar aviso email).
    * **Retorno (Línea discontinua):** La respuesta del mensaje.

---

## 2. ESCENARIOS TÍPICOS EN LA AGE (QUÉ DIBUJAR)

En el examen, dibuja uno de estos flujos críticos para demostrar conocimiento técnico.

### Escenario A: Presentación y Registro de Solicitud (El más completo)

Este flujo conecta al Ciudadano con la aplicación y el Registro.

**Secuencia Lógica:**

1.  **Ciudadano** -> `PortalWeb`: Pulsa "Enviar Solicitud".
2.  `PortalWeb` -> `LogicaNegocio`: Valida datos formulario.
3.  `LogicaNegocio` -> `Integracion_Firma`: Solicita firma de datos.
4.  `Integracion_Firma` -> **FIRe**: Ejecuta proceso de firma (Cliente/Nube).
5.  **FIRe** --> `Integracion_Firma`: Devuelve ID_Firma y Documento Firmado.
6.  `LogicaNegocio` -> `Integracion_Registro`: Solicita registro de entrada.
7.  `Integracion_Registro` -> **GEISER/REGECO**: Envía XML con datos y firma.
8.  **GEISER** --> `Integracion_Registro`: Devuelve **Justificante con CSV** y Fecha/Hora.
9.  `LogicaNegocio` -> `Persistencia`: Guarda Expediente y Justificante.
10. `PortalWeb` --> **Ciudadano**: Muestra el recibo PDF.



### Escenario B: Autenticación con Cl@ve (Inicio de Sesión)

Este flujo demuestra cómo funciona la seguridad eIDAS.

**Secuencia Lógica:**

1.  **Ciudadano** -> `PortalWeb`: Acceder a "Mi Carpeta".
2.  `PortalWeb` -> `Integracion_Identidad`: Solicitar autenticación.
3.  `Integracion_Identidad` -> **Cl@ve (Pasarela)**: Redirección SAML (Request).
4.  **Cl@ve** <-> **Ciudadano**: El usuario introduce credenciales (PIN/Perm).
5.  **Cl@ve** -> `Integracion_Identidad`: Redirección de vuelta con Token (SAML Response).
6.  `Integracion_Identidad` -> `LogicaNegocio`: Valida Token y obtiene DNI/Nombre.
7.  `LogicaNegocio`: Crea sesión de usuario.



---

## 3. RELACIÓN CON LA ARQUITECTURA DE 4 CAPAS

El diagrama debe reflejar fielmente las capas definidas en el archivo `21_Arquitectura_Paquetes.md`.

* **Regla de Oro:** La capa de `Presentación` (Web) **NUNCA** debe llamar directamente a `GEISER` o `Cl@ve`.
* **Flujo Correcto:** `Presentación` -> `Lógica Negocio` -> `Integración` -> **Sistema Externo**.
* **Justificación:** *"Este diseño asegura que la lógica de negocio permanezca agnóstica a los protocolos de comunicación externos, delegando esa responsabilidad en la capa de integración."*

---

## 4. PLANTILLA DE JUSTIFICACIÓN (TEXTO DE EXAMEN)

> "El Diagrama de Secuencia ilustra el comportamiento dinámico para el Caso de Uso 'Presentar Solicitud'. Se destaca la orquestación de servicios mediante la **Capa de Integración**:
>
> 1.  La comunicación con **FIRe** garantiza la firma no repudiable de la solicitud antes de su registro.
> 2.  La llamada síncrona a **GEISER** (vía Web Service REGECO) asegura la obtención inmediata del número de registro y la fecha oficial (sello de tiempo), requisito legal indispensable para el cómputo de plazos (Ley 39/2015).
> 3.  Finalmente, se invoca al componente de persistencia para almacenar el expediente conforme a la estructura ENI."

---