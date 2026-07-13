# Study Assistant MVP

Aplicación mínima para consultar la base de conocimiento Markdown.

## Flujo

```text
knowledge/**/*.md
        ↓
scripts/build_knowledge_index.py
        ↓
apps/studyassistant/data/knowledge_index.json
        ↓
apps/studyassistant/*.php
```

## Generar índice

Desde la raíz del repositorio:

```powershell
python .\scripts\build_knowledge_index.py
```

## Ejecutar en local

Opción sencilla sin tocar Docker:

```powershell
php -S localhost:8090 -t apps/studyassistant
```

Abrir:

```text
http://localhost:8090
```

## Alcance

Incluye:

- Listado de apuntes.
- Búsqueda por texto.
- Filtros por etiqueta, proceso y estado.
- Vista de apunte.
- Renderizado básico de Markdown.
- Lectura de metadatos desde frontmatter.

No incluye:

- Base de datos.
- Integración con IA.
- RAG.
- Progreso de estudio.
- Docker propio.
- Renderizado Markdown completo con Composer.
