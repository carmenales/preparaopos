"""Lector mínimo de los scripts SQL de importación generados para MariaDB.

Solo entiende lo que usan los ficheros de ``imports/*/generated``:
- ``SET @var := 'texto'`` / ``SET @var = LAST_INSERT_ID()``
- ``INSERT INTO tabla (col, ...) VALUES (...), (...) [ON DUPLICATE KEY UPDATE ...]``
- valores: cadenas con comillas simples ('' como escape), NULL, números, @variables y NOW().

El resto de sentencias (DELETE, START TRANSACTION, COMMIT, SET NAMES...) se ignoran.
No ejecuta nada: devuelve las filas insertadas para que el importador las procese.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field

LAST_INSERT_ID = object()  # marcador: la variable apunta a la última fila de ptype


@dataclass
class InsertRow:
    table: str
    values: dict[str, object]
    statement_index: int


@dataclass
class ParsedDump:
    rows: list[InsertRow] = field(default_factory=list)


def split_statements(sql: str) -> list[str]:
    """Divide por ';' fuera de cadenas y elimina comentarios de línea ``--``."""
    statements: list[str] = []
    buf: list[str] = []
    i, n = 0, len(sql)
    in_str = False
    while i < n:
        ch = sql[i]
        if in_str:
            buf.append(ch)
            if ch == "'":
                if i + 1 < n and sql[i + 1] == "'":
                    buf.append("'")
                    i += 1
                else:
                    in_str = False
            elif ch == "\\" and i + 1 < n:
                buf.append(sql[i + 1])
                i += 1
        elif ch == "'":
            in_str = True
            buf.append(ch)
        elif ch == "-" and sql.startswith("--", i) and (i == 0 or sql[i - 1] in "\n\r \t"):
            while i < n and sql[i] != "\n":
                i += 1
            continue
        elif ch == ";":
            stmt = "".join(buf).strip()
            if stmt:
                statements.append(stmt)
            buf = []
        else:
            buf.append(ch)
        i += 1
    tail = "".join(buf).strip()
    if tail:
        statements.append(tail)
    return statements


_TOKEN_RE = re.compile(
    r"""\s*(?:
        (?P<str>'(?:[^'\\]|''|\\.)*')
      | (?P<null>NULL)\b
      | (?P<now>NOW\(\))
      | (?P<var>@[A-Za-z_][A-Za-z0-9_]*)
      | (?P<num>-?\d+(?:\.\d+)?)
      | (?P<lit>LAST_INSERT_ID\(\))
    )\s*""",
    re.VERBOSE | re.IGNORECASE,
)


def _unquote(token: str) -> str:
    body = token[1:-1]
    out: list[str] = []
    i = 0
    while i < len(body):
        ch = body[i]
        if ch == "'" and i + 1 < len(body) and body[i + 1] == "'":
            out.append("'")
            i += 2
        elif ch == "\\" and i + 1 < len(body):
            nxt = body[i + 1]
            out.append({"n": "\n", "t": "\t", "r": "\r", "0": "\0"}.get(nxt, nxt))
            i += 2
        else:
            out.append(ch)
            i += 1
    return "".join(out)


def _parse_value(text: str, pos: int, variables: dict[str, object]) -> tuple[object, int]:
    m = _TOKEN_RE.match(text, pos)
    if not m:
        raise ValueError(f"Valor SQL no reconocido cerca de: {text[pos:pos + 60]!r}")
    if m.group("str") is not None:
        value: object = _unquote(m.group("str"))
    elif m.group("null"):
        value = None
    elif m.group("now"):
        value = None
    elif m.group("var"):
        name = m.group("var").lower()
        if name not in variables:
            raise ValueError(f"Variable SQL sin definir: {name}")
        value = variables[name]
    elif m.group("num"):
        raw = m.group("num")
        value = float(raw) if "." in raw else int(raw)
    else:
        value = LAST_INSERT_ID
    return value, m.end()


def _parse_tuples(text: str, variables: dict[str, object]) -> list[list[object]]:
    tuples: list[list[object]] = []
    pos = 0
    while True:
        while pos < len(text) and text[pos] in " \t\r\n,":
            pos += 1
        if pos >= len(text) or text[pos] != "(":
            break
        pos += 1
        values: list[object] = []
        while True:
            value, pos = _parse_value(text, pos, variables)
            values.append(value)
            if text[pos] == ",":
                pos += 1
                continue
            if text[pos] == ")":
                pos += 1
                break
            raise ValueError(f"Tupla mal formada cerca de: {text[pos:pos + 60]!r}")
        tuples.append(values)
    return tuples


_INSERT_RE = re.compile(r"^INSERT\s+INTO\s+`?(\w+)`?\s*\(([^)]*)\)\s*VALUES\s*", re.IGNORECASE | re.DOTALL)
_SET_RE = re.compile(r"^SET\s+(@\w+)\s*:?=\s*(.+)$", re.IGNORECASE | re.DOTALL)
_ON_DUP_RE = re.compile(r"\)\s*ON\s+DUPLICATE\s+KEY\s+UPDATE\b.*$", re.IGNORECASE | re.DOTALL)


def parse_dump(sql: str) -> ParsedDump:
    parsed = ParsedDump()
    variables: dict[str, object] = {}
    for index, stmt in enumerate(split_statements(sql)):
        set_match = _SET_RE.match(stmt)
        if set_match and not stmt.upper().startswith(("SET NAMES", "SET CHARACTER")):
            value, _ = _parse_value(set_match.group(2), 0, variables)
            variables[set_match.group(1).lower()] = value
            continue

        insert_match = _INSERT_RE.match(stmt)
        if not insert_match:
            continue
        table = insert_match.group(1).lower()
        columns = [c.strip().strip("`") for c in insert_match.group(2).split(",")]
        body = stmt[insert_match.end():]
        body = _ON_DUP_RE.sub(")", body)
        for values in _parse_tuples(body, variables):
            if len(values) != len(columns):
                raise ValueError(f"{table}: {len(columns)} columnas y {len(values)} valores en la sentencia {index}")
            parsed.rows.append(InsertRow(table, dict(zip(columns, values)), index))
    return parsed
