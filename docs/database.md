# Database setup

This project uses a local MariaDB database for the legacy `preparadortai` PHP application.

The real database dump is not versioned in Git. It must be generated locally from the XAMPP/MariaDB instance and placed under:

```text
db/local/
```

The repository keeps the folder with:

```text
db/local/.gitkeep
```

but ignores SQL dumps and local database files.

## Current database

Local database name:

```text
preparadortai
```

Main tables:

```text
ptype
incorrectas
rtype
```

Approximate meaning:

```text
ptype        Multiple-choice questions.
incorrectas Incorrect options associated with ptype.id.
rtype        Relationship/matching questions.
```

## Exporting the local XAMPP database

Use `mysqldump` with `--result-file`.

Do not use PowerShell redirection with `>` to generate the SQL dump, because Windows PowerShell may write the file using UTF-16 encoding. MariaDB's Docker entrypoint expects a plain SQL file and may fail with errors such as:

```text
ERROR: ASCII '\0' appeared in the statement
```

From the repository root:

```powershell
cd C:\repositories\preparaopos
```

If the XAMPP `root` user has no password:

```powershell
& "C:\xampp\mysql\bin\mysqldump.exe" -u root --default-character-set=utf8mb4 --databases preparadortai --result-file=".\db\local\001_preparadortai_dump.sql"
```

If the XAMPP `root` user has a password:

```powershell
& "C:\xampp\mysql\bin\mysqldump.exe" -u root -p --default-character-set=utf8mb4 --databases preparadortai --result-file=".\db\local\001_preparadortai_dump.sql"
```

If using another database user:

```powershell
& "C:\xampp\mysql\bin\mysqldump.exe" -u YOUR_USER -p --default-character-set=utf8mb4 --databases preparadortai --result-file=".\db\local\001_preparadortai_dump.sql"
```

## Checking the dump

After generating the dump, verify that it is readable text:

```powershell
Get-Content .\db\local\001_preparadortai_dump.sql -TotalCount 20
```

The file should contain readable SQL statements, such as:

```sql
CREATE DATABASE
USE `preparadortai`;
CREATE TABLE ...
```

## Starting the Docker environment

From the repository root:

```powershell
docker compose up --build -d
```

The services are:

```text
Legacy PHP app: http://localhost:8080
phpMyAdmin:     http://localhost:8081
MariaDB:        localhost:3307
```

## Reinitializing the Docker database

MariaDB only imports files from `/docker-entrypoint-initdb.d` when the database volume is empty.

If the database was initialized before the SQL dump existed, or if the import failed, recreate the database volume:

```powershell
docker compose down -v
docker compose up --build -d
```

## Checking tables inside Docker

Use the root user:

```powershell
docker compose exec db mariadb -h 127.0.0.1 -u root -proot preparadortai -e "SHOW TABLES;"
```

Expected tables:

```text
incorrectas
ptype
rtype
```

You can also check with the application user:

```powershell
docker compose exec db mariadb -h 127.0.0.1 -u preparaopos -ppreparaopos preparadortai -e "SHOW TABLES;"
```

## Important Git rules

Do not commit real database dumps.

The following files should remain local:

```text
db/local/*.sql
*.sql
*.dump
*.bak
*.backup
*.sqlite
*.db
```

Only this file should be versioned inside `db/local`:

```text
db/local/.gitkeep
```
