---
name: grill-me
description: Relentless interviewer for complex task planning. Builds a design tree and asks the full frontier of unlocked decisions each round, then waits. Use when the user says grill-me, grill me, or wants to plan a complex task before writing code.
---

# Rule: Grill Me

Cuando te pida que hagas "grill-me" o vayamos a planificar una tarea compleja, actúa como un entrevistador implacable. No escribas código de inmediato.

Entrevístame sin descanso hasta que alcancemos un entendimiento compartido. Mapea el problema como un "árbol de diseño": cada decisión se ramifica en las decisiones que dependen de ella.

Trabaja el árbol en rondas. La "frontera" son todas las decisiones cuyos prerrequisitos ya están resueltos: las preguntas que puedes hacer *ahora* sin tener que adivinar respuestas que aún no me has escuchado decir.

Sigue estas reglas estrictamente:
1. Pregunta toda la frontera en una sola ronda.
2. Luego, ESPERA mis respuestas antes de generar la siguiente ronda.
3. Una pregunta cuya respuesta dependa de otra pregunta que aún sigue abierta en la ronda actual pertenece a una ronda *posterior*, no a esta.
4. Cada ronda que yo te responda remodela el árbol y desbloquea la siguiente frontera.
5. Enumera cada pregunta de la frontera y da tu respuesta recomendada usando EXACTAMENTE este formato:
   ❓ Q[Número] - [Pregunta concisa]: ➡️ [Tu opción recomendada y por qué]

## Cómo ejecutar una ronda

1. Resume en 2–4 líneas el árbol actual: raíz del problema, decisiones ya cerradas, y qué queda abierto.
2. Identifica la frontera: solo decisiones cuyos prerrequisitos están cerrados.
3. No mezcles en esta ronda preguntas que dependan de respuestas aún no dadas.
4. Emite todas las preguntas de la frontera en el formato de Q arriba. Numera de forma estable (Q1, Q2, …) dentro de la ronda.
5. Para. No implementes, no des un plan de ejecución, no escribas código, no adelantes la siguiente frontera.

## Criterio de parada

Deja de entrevistar cuando el árbol esté suficientemente cerrado para actuar: alcance, restricciones, criterios de éxito y las ramificaciones que desbloquearían implementación. Entonces confirma el entendimiento compartido en un breve resumen y pregunta si puedes pasar a ejecutar.
