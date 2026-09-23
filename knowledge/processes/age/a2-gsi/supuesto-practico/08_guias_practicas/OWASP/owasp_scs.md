---
title: OWASP Smart Contract Top 10 (Edición 2026)
---

# ⛓️ OWASP Smart Contract Top 10

El **OWASP Smart Contract Top 10** es un documento de concienciación estándar diseñado para proporcionar a desarrolladores Web3, auditores y equipos de seguridad información sobre las vulnerabilidades más críticas que afectan a los contratos inteligentes (Smart Contracts) y al ecosistema blockchain.


## Objetivo

A diferencia de la web tradicional, el código desplegado en una blockchain (como Ethereum) suele ser inmutable y, a menudo, maneja o custodia directamente activos financieros de alto valor. El objetivo de este Top 10 es servir como referencia de priorización de riesgos para asegurar los protocolos frente a los fallos explotados más recientemente (donde las pérdidas se cuentan por miles de millones).


## Las 10 Vulnerabilidades Críticas en Smart Contracts (2026)

### SC01:2026 - Vulnerabilidades de Control de Acceso (Access Control Vulnerabilities)

Ocurre cuando el contrato inteligente no impone restricciones adecuadas sobre quién puede ejecutar funciones críticas, permitiendo a usuarios no autorizados tomar el control del protocolo.

#### Riesgos
* Invocación de **funciones privilegiadas** (ej. retirar fondos, cambiar el dueño, pausar el contrato) por parte de cualquiera.
* Falta de protección en funciones de inicialización que terminan siendo reclamadas por un atacante.

#### Mitigaciones
* Implementar el **principio de mínimo privilegio** en roles y permisos.
* Utilizar modificadores de control de acceso consolidados y auditados (como `Ownable` o `AccessControl` de *OpenZeppelin*).
* Proteger fuertemente las funciones administrativas detrás de billeteras **Multisig** (multisignatura) o votaciones de gobernanza.

### SC02:2026 - Vulnerabilidades de Lógica de Negocio (Business Logic Vulnerabilities)

Se refiere a fallos conceptuales en el diseño del propio protocolo (las reglas del juego) que los atacantes pueden explotar de forma perfectamente válida según el código, pero en contra de la intención del creador.

#### Riesgos
* Errores en la **contabilidad de tokens**, distribución de recompensas o cálculo de intereses.
* Abuso de los incentivos del sistema que permite a un usuario **extraer valor inmerecido** sin romper técnicamente la criptografía.

#### Mitigaciones
* Realizar un **modelado de amenazas exhaustivo** antes de escribir código.
* Aplicar **auditorías formales** y crear pruebas unitarias integrales que verifiquen invariantes económicas (la suma de saldos debe cuadrar siempre).

### SC03:2026 - Manipulación de Oráculos de Precios (Price Oracle Manipulation)

Sucede cuando los contratos dependen de fuentes de datos externas (oráculos) para determinar el precio de un activo, pero dicha fuente es vulnerable a ser alterada artificialmente.

#### Riesgos
* Un atacante utiliza gran cantidad de capital para **sesgar temporalmente el precio spot** de un token en un Exchange Descentralizado (DEX) de baja liquidez.
* Uso de ese precio inflado para **solicitar préstamos masivos (sobrecolateralizados artificialmente)** que nunca se devuelven.

#### Mitigaciones
* **Nunca depender de un único DEX spot** como fuente de precios.
* Utilizar **oráculos descentralizados robustos** (como *Chainlink*) que agregan datos de múltiples fuentes off-chain.
* Implementar **TWAP (Time-Weighted Average Price)** para que el precio sea el promedio de un periodo, mitigando picos instantáneos.

### SC04:2026 - Ataques Facilitados por Préstamos Flash (Flash Loan-Facilitated Attacks)

Un préstamo flash (*Flash Loan*) permite a un usuario pedir prestado capital ilimitado sin garantías, siempre que lo devuelva en la misma transacción. Los atacantes lo usan para amplificar pequeñas vulnerabilidades.

#### Riesgos
* Disponer de "dinero infinito" temporal para **manipular gobernanza** (comprar votos), alterar pools de liquidez o exprimir fallos lógicos a una escala devastadora.
* Transformar un pequeño bug aritmético en un **drenaje total del protocolo**.

#### Mitigaciones
* Diseñar el sistema bajo la premisa de que **cualquier usuario puede tener fondos ilimitados** temporalmente.
* Aplicar comprobaciones de estado que requieran el paso de **múltiples bloques** (haciendo inútil el ataque en una sola transacción).

### SC05:2026 - Falta de Validación de Entrada (Lack of Input Validation)

Ocurre cuando el contrato asume que los datos, direcciones o *payloads* suministrados (incluso a través de puentes *cross-chain*) son benignos sin validarlos.

#### Riesgos
* Uso de parámetros manipulados que **corrompen el estado del contrato**.
* Invocación de direcciones de tokens falsos (tokens envenenados) o ejecución de llamadas arbitrarias que puentean las defensas lógicas.

#### Mitigaciones
* Validar rigurosamente **el tamaño, formato, rango y procedencia** de cada entrada.
* Utilizar **listas blancas (allow-lists)** para restringir las direcciones de los tokens con los que el protocolo interactúa.

### SC06:2026 - Llamadas Externas No Comprobadas (Unchecked External Calls)

Se produce cuando un contrato interactúa con otro utilizando llamadas de muy bajo nivel (`call`, `delegatecall` o `send`) pero no verifica si dicha llamada tuvo éxito o fracasó.

#### Riesgos
* La llamada falla silenciosamente y devuelve `false`, pero **el contrato asume que fue un éxito** y continúa la ejecución, alterando saldos internos incorrectamente.
* Posibilidad de que fondos se queden bloqueados o la contabilidad se descuadre irremediablemente.

#### Mitigaciones
* **Comprobar siempre el valor booleano de retorno** al usar llamadas de bajo nivel y revertir (hacer *revert*) si es `false`.
* Preferir el uso de llamadas seguras mediante **interfaces de alto nivel** estructuradas (ej. `SafeERC20`).

### SC07:2026 - Errores Aritméticos: Redondeo y Precisión (Arithmetic Errors)

Los lenguajes como Solidity no soportan números de coma flotante (decimales). Los cálculos matemáticos complejos deben emularse, lo que introduce fallos de redondeo.

#### Riesgos
* **División antes de la multiplicación**, lo que causa que los valores se trunquen a cero y se pierda la precisión del cálculo.
* Atacantes explotan estos errores de redondeo para extraer fracciones de céntimo repetidamente o corromper el ratio de una *pool* de liquidez.

#### Mitigaciones
* Regla de oro en Solidity: **Multiplicar siempre antes de dividir**.
* Escalar (multiplicar) temporalmente los números por grandes factores de precisión (ej. $10^{18}$) durante los pasos intermedios del cálculo.

### SC08:2026 - Ataques de Reentrada (Reentrancy Attacks)

Es una de las vulnerabilidades más infames (responsable del hackeo del DAO original). Un contrato externo malicioso llama a la función vulnerable y, antes de que esta termine y actualice los saldos, el contrato malicioso **vuelve a invocarla iterativamente**.

#### Riesgos
* **Drenaje recursivo de fondos:** El contrato envía dinero al atacante y, como no ha descontado el saldo todavía, el atacante lo vuelve a pedir una y otra vez en un bucle cerrado dentro de la misma transacción.

#### Mitigaciones
* Implementar estrictamente el patrón **CEI (Checks-Effects-Interactions)**: 1) Comprobar, 2) Actualizar estado interno, 3) Interactuar con el exterior al final.
* Utilizar modificadores de protección como `ReentrancyGuard` (`nonReentrant`) para bloquear llamadas recursivas.

### SC09:2026 - Desbordamiento y Subdesbordamiento de Enteros (Integer Overflow and Underflow)

Surge cuando una operación matemática excede el valor máximo o mínimo que el tipo de variable (ej. `uint256`) puede almacenar, dando "la vuelta" como el cuentakilómetros de un coche antiguo (un saldo de 0 menos 1 pasa a ser un saldo infinito).

#### Riesgos
* Atacantes logran crear **balances inflados artificialmente** o sobrepasar límites de suministro forzando un *underflow*.

#### Mitigaciones
* Compilar siempre utilizando **Solidity versión 0.8.0 o superior** (que incluye protección y reversión automática por defecto frente a estos errores).
* En versiones antiguas, utilizar obligatoriamente librerías matemáticas seguras como **`SafeMath`**. No usar bloques `unchecked` sin un análisis extremo.

### SC10:2026 - Vulnerabilidades de Proxys y Actualización (Proxy & Upgradeability Vulnerabilities)

Como los contratos son inmutables, la industria inventó el "Patrón Proxy" para poder actualizar la lógica derivando llamadas de un contrato Proxy hacia una Implementación. Configurarlo mal es letal.

#### Riesgos
* Dejar funciones críticas `initialize()` sin asegurar, permitiendo que **un atacante "inicialice" el contrato y se nombre administrador**.
* **Choques de almacenamiento (*Storage Collisions*)**: Alterar el orden de las variables al subir una nueva versión del contrato corrompe toda la base de datos de la aplicación.

#### Mitigaciones
* Proteger celosamente las funciones de inicialización con modificadores `initializer`.
* Usar los estándares de proxy consolidados (como el **almacenamiento no estructurado EIP-1967** de OpenZeppelin).
* Nunca cambiar el orden ni eliminar variables de estado al lanzar versiones nuevas; solo añadir nuevas variables al final.


## Tabla Resumen (Smart Contract Top 10 - 2026)

| ID | Riesgo (Categoría) | Palabra Clave / Concepto | Defensa / Mitigación Principal |
|:---|:---|:---|:---|
| **SC01** | Control de Acceso | Robo de admin, funciones sin restringir. | Mínimo privilegio, modificadores (Ownable/Multisig). |
| **SC02** | Lógica de Negocio | Fallos en contabilidad, economía del protocolo. | Pruebas formales, test de invariantes, modelado de amenazas. |
| **SC03** | Manipulación de Oráculos | Alterar precios de DEX para sacar préstamos. | Oráculos descentralizados (Chainlink), usar TWAP. |
| **SC04** | Préstamos Flash (Flash Loans)| Dinero infinito temporal, magnifica bugs. | Comprobaciones a nivel multi-bloque. |
| **SC05** | Falta Validación de Entrada | Direcciones falsas, payload corrupto. | Allow-lists (listas blancas), sanitizar parámetros. |
| **SC06** | Llamadas Externas (Unchecked)| `call` falla silenciosamente y el código sigue. | Verificar el boolean de retorno o usar `SafeERC20`. |
| **SC07** | Errores Aritméticos | Pérdida de precisión, truncado a cero. | Multiplicar antes de dividir, escalar variables temporalmente. |
| **SC08** | Reentrada (Reentrancy) | Llamada recursiva, drenar sin actualizar saldo. | Patrón CEI (Checks-Effects-Interactions), `ReentrancyGuard`. |
| **SC09** | Overflow / Underflow | Bucle matemático de variables, saldo infinito. | Usar Solidity >= 0.8.0 o librería `SafeMath`. |
| **SC10** | Proxys y Actualizaciones | Ataque al `initialize()`, Storage Collision. | Usar estándar EIP-1967, nunca alterar el orden de variables. |

## Bibliografía
* [OWASP Smart Contract Top 10 Project (2026)](https://scs.owasp.org/sctop10/)
* [OWASP Smart Contract Security Verification Standard (SCSVS)](https://scs.owasp.org/)