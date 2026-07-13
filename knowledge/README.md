# Base de conocimiento

Esta carpeta contiene la base documental y los apuntes de preparación de oposiciones.

La aplicación de tests vive en `apps/`. Esta base de conocimiento vive separada en `knowledge/` para poder reutilizarla en distintos procesos selectivos y, más adelante, conectarla con funcionalidades de búsqueda, generación de tests o asistencia con IA.

## Objetivo

Organizar:

- Fuentes oficiales: leyes, reales decretos, normativa, bases de convocatorias, PDFs y documentos de referencia.
- Apuntes generados o revisados a partir de esas fuentes.
- Material específico de cada proceso selectivo.
- Metadatos suficientes para poder buscar por organismo, proceso, perfil, materia, etiquetas o fuente.

## Estructura inicial

```text
knowledge/
├── README.md
├── _templates/
│   └── apunte.md
├── fuentes/
│   ├── sources.yml
│   ├── pdf/
│   └── extracted/
└── procesos/
    └── comunidad-madrid/
        ├── administracion-digital/
        │   ├── README.md
        │   ├── apuntes/
        │   └── fuentes/
        │       ├── pdf/
        │       └── extracted/
        └── sermas/
            ├── README.md
            ├── apuntes/
            └── fuentes/
                ├── pdf/
                └── extracted/
```

## Criterio de organización

La organización principal es por proceso u organismo, no por temática.

Ejemplo:

```text
knowledge/procesos/comunidad-madrid/administracion-digital/apuntes/
knowledge/procesos/comunidad-madrid/ciberseguridad/apuntes/
```

Las materias como seguridad, procedimiento administrativo, protección de datos, cloud, redes o IA se indicarán mediante etiquetas en el frontmatter de cada apunte.

Ejemplo:

```yaml
tags:
  - seguridad
  - ens
  - normativa
  - administracion-publica
```

Así, más adelante, un buscador o un sistema con IA podrá recuperar los apuntes por etiquetas y por contenido semántico, sin depender de carpetas temáticas rígidas.

## Fuentes comunes

Las fuentes que sirven para varios procesos selectivos se registran en:

```text
knowledge/fuentes/sources.yml
knowledge/fuentes/pdf/
knowledge/fuentes/extracted/
```

Ejemplos:

- Ley 39/2015.
- Ley 40/2015.
- Real Decreto 311/2022, Esquema Nacional de Seguridad.
- RGPD.
- LOPDGDD.
- TREBEP.
- Normativa común del sector público.

## Fuentes específicas de proceso

Las fuentes propias de un proceso concreto se guardan dentro del proceso correspondiente.

Ejemplo:

```text
knowledge/procesos/comunidad-madrid/administracion-digital/fuentes/
knowledge/procesos/comunidad-madrid/ciberseguridad/fuentes/
```

Ahí entrarían:

- Bases de la convocatoria.
- Temario oficial de ese proceso.
- Correcciones de bases.
- Listados o resoluciones específicas.
- Documentos propios del organismo convocante.

## Apuntes

Los apuntes se escribirán en Markdown (`.md`) con frontmatter YAML.

Ejemplo de ubicación:

```text
knowledge/procesos/comunidad-madrid/administracion-digital/apuntes/ens-principios-basicos.md
```

Cada apunte debe indicar:

- Procesos a los que aplica.
- Perfiles, si procede.
- Fuentes utilizadas.
- Etiquetas temáticas.
- Estado de revisión.
- Si ha sido generado con IA y si requiere revisión humana.

## Estados recomendados

```text
borrador
en_revision
revisado
desactualizado
```

## Convención de nombres

Usar nombres en minúsculas, sin tildes y con guiones:

```text
ens-principios-basicos.md
ley-39-2015-actos-administrativos.md
rgpd-principios-tratamiento.md
bases-administracion-digital-2026.pdf
```

## Criterio para IA futura

Esta estructura está pensada para permitir una futura arquitectura de búsqueda o RAG:

- PDFs oficiales como fuente original.
- Texto extraído en Markdown o texto plano.
- Apuntes estructurados y revisables.
- Metadatos en YAML.
- Etiquetas temáticas.
- Relación explícita entre apuntes y fuentes.

El objetivo no es cerrar ahora una arquitectura definitiva, sino crear una base ordenada que pueda evolucionar.
