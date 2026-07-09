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

## Estado actual

Proceso en preparación.

De momento se prioriza la creación de apuntes en Markdown y la organización de fuentes comunes.
