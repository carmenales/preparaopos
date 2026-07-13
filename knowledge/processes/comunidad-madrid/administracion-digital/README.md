# Comunidad de Madrid - Agencia para la Administración Digital

## Resumen

Base de conocimiento para procesos selectivos relacionados con la Agencia para la Administración Digital de la Comunidad de Madrid.

Esta carpeta contiene apuntes y, más adelante, podrá contener fuentes específicas de convocatorias de este organismo.

## Organización

```text
administracion-digital/
├── README.md
└── apuntes/
```

Más adelante se podrán añadir fuentes específicas de convocatoria:

```text
administracion-digital/
├── fuentes/
│   ├── pdf/
│   └── extracted/
```

## Apuntes

Los apuntes se guardan en:

```text
knowledge/processes/comunidad-madrid/administracion-digital/apuntes/
```

Cada apunte debe usar frontmatter YAML con esta información mínima:

- `id`
- `title`
- `type`
- `status`
- `processes`
- `official_topic`
- `source_ids`
- `tags`
- `ai_generated`
- `needs_human_review`

## Criterio

No se crean carpetas por temática.

Ejemplo: un tema de IA, ENS o protección de datos no va a una carpeta específica, sino que se etiqueta en el frontmatter del apunte:

```yaml
tags:
  - inteligencia-artificial
  - seguridad
  - normativa
```

Esto permitirá más adelante búsqueda semántica, filtros o integración con IA sin depender de una estructura de carpetas rígida.

## Fuentes comunes

Las fuentes comunes a varios procesos se guardan en:

```text
knowledge/sources/
```

Ejemplos:

- ENS.
- AI Act.
- Ley 39/2015.
- Ley 40/2015.
- RGPD.
- LOPDGDD.
- RFC, normas técnicas o documentación institucional reutilizable.

## Fuentes específicas

Las fuentes propias de una convocatoria concreta se podrán añadir más adelante dentro de este proceso.

Ejemplos:

- BOCM de convocatoria.
- Bases específicas.
- Correcciones.
- Temario oficial.
- Resoluciones del proceso.

## Convocatoria y perfiles

### Referencia de la convocatoria

La presente base de conocimiento está organizada alrededor de la convocatoria de la **Agencia para la Administración Digital de la Comunidad de Madrid**.

- **Tema de referencia:** Tema 1 del Anexo 3 de la Resolución 352/2026, de 9 de junio, de la Consejera-Delegada de la Agencia para la Administración Digital de la Comunidad de Madrid, publicada en el BOCM de 11 de junio de 2026.
- **Perfil de aplicación:** Este tema es transversal y se aplica a los perfiles **P01 (IA aplicada al ciclo de vida del software)** y **P02 (Gobierno de IA)**.
- **Bloque de oposición:** El Bloque 1 consta de **45 preguntas tipo test y 5 de reserva**, con **cuatro opciones**, **1 punto por acierto** y **-0,25 puntos por respuesta errónea**.
- **Duración y corte:** La duración máxima es de **1 hora y 30 minutos** y se exige superar el **50 % de los puntos posibles** (22,5 puntos).

### Relevancia didáctica

Dado que la penalización por fallo es relevante, el estudio debe prestar especial atención a los distractores habituales de examen, especialmente:

- clasificación vs. regresión
- clustering vs. clasificación
- stemming vs. lematización
- NLU vs. NLG
- data drift vs. concept drift
- definición técnica vs. definición jurídica del **Reglamento (UE) 2024/1689**

### Estrategia de estudio por tema

Para el tema de **Fundamentos de Inteligencia Artificial**, la adopción de la estrategia didáctica recomendada es:

- Memorizar las jerarquías: **Deep Learning ⊂ Machine Learning ⊂ Inteligencia Artificial**.
- Entender que no toda la IA es Machine Learning; existen enfoques simbólicos y basados en conocimiento, aunque la normativa exige el componente de *inferencia*.
- Distinguir claramente entre el modelo (artefacto entrenado) y el sistema de IA (solución completa que incluye interfaces, reglas de negocio y controles).
- Para P01: priorizar MLOps, CI/CD/CT, y monitorización.
- Para P02: priorizar la definición legal de IA, riesgos, y el registro de eventos (Art. 12 AI Act).

## Estado actual

Proceso en preparación.

De momento se prioriza la creación de apuntes en Markdown y la organización de fuentes comunes.
