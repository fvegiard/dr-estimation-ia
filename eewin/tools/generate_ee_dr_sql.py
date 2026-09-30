#!/usr/bin/env python3
"""Generate one consolidated T-SQL file (schema + modules + data) from a live SQL Server database.

Everything is read from the catalog views of the source database:
  - tables/columns   : sys.tables, sys.columns, sys.types, sys.identity_columns, sys.default_constraints
  - keys/indexes     : sys.key_constraints, sys.indexes, sys.index_columns, sys.foreign_keys(_columns),
                       sys.check_constraints
  - modules          : sys.sql_modules (definition = OBJECT_DEFINITION), sys.sql_expression_dependencies
  - data             : SELECT * FROM every user table (ordered by primary key / identity column)

The output is a plain UTF-8 script runnable with sqlcmd against an EMPTY database that already exists
with the same collation as the source, e.g.:

    sqlcmd -S localhost -U sa -P '<pwd>' -C -Q "CREATE DATABASE EE_TEST COLLATE French_CI_AS"
    sqlcmd -S localhost -U sa -P '<pwd>' -C -d EE_TEST -f 65001 -x -b -I -i EE_DR.sql

Usage:
    python generate_ee_dr_sql.py --server localhost --port 1433 --user sa --password '...' \
        --database EE --output ../EE_DR.sql

Only dependency: pymssql (FreeTDS based), see requirements.txt. Written for the DR Electrique "eewin" reverse-engineering
project; the generator is intentionally generic (no table names hard-coded).
"""

from __future__ import annotations

import argparse
import datetime as dt
import decimal
import hashlib
import math
import re
import sys
import uuid
from collections import defaultdict
from zoneinfo import ZoneInfo

import pymssql

ROWS_PER_INSERT = 1000  # SQL Server hard limit for a single VALUES table constructor


# --------------------------------------------------------------------------------------------------
# Helpers
# --------------------------------------------------------------------------------------------------
def q(name: str) -> str:
    """Bracket-quote an identifier."""
    return "[" + name.replace("]", "]]") + "]"


def type_spec(type_name: str, max_length: int, precision: int, scale: int) -> str:
    """Render a column/parameter data type from sys.columns metadata."""
    t = type_name.lower()
    if t in ("varchar", "char", "varbinary", "binary"):
        return f"{t}({'max' if max_length == -1 else max_length})"
    if t in ("nvarchar", "nchar"):
        return f"{t}({'max' if max_length == -1 else max_length // 2})"
    if t in ("decimal", "numeric"):
        return f"{t}({precision},{scale})"
    if t in ("datetime2", "time", "datetimeoffset"):
        return f"{t}({scale})"
    if t == "float":
        return "float" if precision == 53 else f"float({precision})"
    return t


def sql_literal(value, type_name: str) -> str:
    """Render a Python value fetched by pymssql as a T-SQL literal."""
    if value is None:
        return "NULL"
    t = type_name.lower()
    if isinstance(value, bool):
        return "1" if value else "0"
    if isinstance(value, int):
        return str(value)
    if isinstance(value, float):
        if math.isnan(value) or math.isinf(value):
            raise ValueError("NaN/Inf cannot be stored in SQL Server float")
        r = repr(value)  # shortest string that round-trips the IEEE-754 double
        return r.replace("e", "E")
    if isinstance(value, decimal.Decimal):
        return str(value)
    if isinstance(value, dt.datetime):
        if t == "datetime":
            # datetime precision is 1/300 s; pymssql already returns the .000/.003/.007 milliseconds
            return "'" + value.strftime("%Y-%m-%dT%H:%M:%S.") + f"{value.microsecond // 1000:03d}'"
        return "'" + value.isoformat(sep="T") + "'"
    if isinstance(value, dt.date):
        return "'" + value.isoformat() + "'"
    if isinstance(value, dt.time):
        return "'" + value.isoformat() + "'"
    if isinstance(value, (bytes, bytearray, memoryview)):
        b = bytes(value)
        return "0x" + b.hex() if b else "0x"
    if isinstance(value, uuid.UUID):
        return f"'{value}'"
    if isinstance(value, str):
        return n_string(value)
    raise TypeError(f"unsupported python type {type(value)!r} for SQL type {type_name}")


def n_string(s: str) -> str:
    """N'...' literal, safe for sqlcmd batch parsing.

    sqlcmd interprets a line that is exactly GO, or a line starting with ':' as a command even inside a
    string literal, so such line starts are broken out of the literal with CHAR(10)/CHAR(13).
    """
    body = s.replace("'", "''")
    lines = body.split("\n")
    if len(lines) == 1:
        return "N'" + body + "'"
    out_parts: list[str] = []
    for i, line in enumerate(lines):
        if i > 0:
            stripped = line.rstrip("\r")
            if stripped.strip().upper() == "GO" or stripped.startswith(":"):
                out_parts.append("' + CHAR(10) + N'" + line)
                continue
            out_parts.append("\n" + line)
        else:
            out_parts.append(line)
    return "N'" + "".join(out_parts) + "'"


def module_text_is_batch_safe(definition: str) -> None:
    for line in definition.split("\n"):
        s = line.rstrip("\r")
        if s.strip().upper() == "GO" or s.startswith(":"):
            raise ValueError("module definition contains a sqlcmd command line: " + s)


# --------------------------------------------------------------------------------------------------
# Catalog readers
# --------------------------------------------------------------------------------------------------
class Catalog:
    def __init__(self, conn):
        self.conn = conn
        self.cur = conn.cursor(as_dict=True)

    def rows(self, sql: str, params=None):
        self.cur.execute(sql, params or ())
        return self.cur.fetchall()

    def scalar(self, sql: str, params=None):
        self.cur.execute(sql, params or ())
        r = self.cur.fetchone()
        return list(r.values())[0] if r else None

    # ---- database ----
    def database_info(self):
        return self.rows(
            """SELECT d.name, d.collation_name, d.compatibility_level, d.recovery_model_desc,
                      d.is_ansi_nulls_on, d.is_ansi_padding_on, d.is_quoted_identifier_on,
                      @@VERSION AS server_version, SYSUTCDATETIME() AS utc_now
               FROM sys.databases d WHERE d.name = DB_NAME()"""
        )[0]

    # ---- tables ----
    def tables(self):
        return self.rows(
            """SELECT t.object_id, s.name AS schema_name, t.name AS table_name, t.lock_escalation_desc
               FROM sys.tables t JOIN sys.schemas s ON s.schema_id = t.schema_id
               WHERE t.is_ms_shipped = 0
               ORDER BY s.name, t.name"""
        )

    def columns(self, object_id: int):
        return self.rows(
            """SELECT c.column_id, c.name, tp.name AS type_name, c.max_length, c.precision, c.scale,
                      c.is_nullable, c.is_identity, c.collation_name, c.is_computed, c.is_rowguidcol,
                      CONVERT(bigint, ic.seed_value) AS seed_value, CONVERT(bigint, ic.increment_value) AS increment_value,
                      CONVERT(bigint, ic.last_value) AS last_value,
                      dc.name AS default_name, dc.definition AS default_definition,
                      dc.is_system_named AS default_is_system_named,
                      cc.definition AS computed_definition, cc.is_persisted
               FROM sys.columns c
               JOIN sys.types tp ON tp.user_type_id = c.user_type_id
               LEFT JOIN sys.identity_columns ic ON ic.object_id = c.object_id AND ic.column_id = c.column_id
               LEFT JOIN sys.default_constraints dc ON dc.parent_object_id = c.object_id
                                                    AND dc.parent_column_id = c.column_id
               LEFT JOIN sys.computed_columns cc ON cc.object_id = c.object_id AND cc.column_id = c.column_id
               WHERE c.object_id = %s
               ORDER BY c.column_id""",
            (object_id,),
        )

    def key_constraints(self, object_id: int):
        """PRIMARY KEY / UNIQUE constraints with their columns."""
        cons = self.rows(
            """SELECT kc.name, kc.type, i.index_id, i.type_desc, i.is_padded, i.fill_factor,
                      i.allow_row_locks, i.allow_page_locks, i.ignore_dup_key, kc.is_system_named
               FROM sys.key_constraints kc
               JOIN sys.indexes i ON i.object_id = kc.parent_object_id AND i.index_id = kc.unique_index_id
               WHERE kc.parent_object_id = %s
               ORDER BY kc.type DESC, kc.name""",
            (object_id,),
        )
        for c in cons:
            c["columns"] = self.index_columns(object_id, c["index_id"])
        return cons

    def index_columns(self, object_id: int, index_id: int):
        return self.rows(
            """SELECT ic.key_ordinal, ic.is_included_column, ic.is_descending_key, c.name
               FROM sys.index_columns ic
               JOIN sys.columns c ON c.object_id = ic.object_id AND c.column_id = ic.column_id
               WHERE ic.object_id = %s AND ic.index_id = %s
               ORDER BY ic.is_included_column, ic.key_ordinal, ic.index_column_id""",
            (object_id, index_id),
        )

    def indexes(self, object_id: int):
        """Plain indexes (not backing a PK/UNIQUE constraint)."""
        idx = self.rows(
            """SELECT i.name, i.index_id, i.type_desc, i.is_unique, i.has_filter, i.filter_definition,
                      i.is_padded, i.fill_factor, i.allow_row_locks, i.allow_page_locks, i.ignore_dup_key,
                      i.is_disabled
               FROM sys.indexes i
               WHERE i.object_id = %s AND i.type IN (1, 2)
                 AND i.is_primary_key = 0 AND i.is_unique_constraint = 0
               ORDER BY i.index_id""",
            (object_id,),
        )
        for i in idx:
            i["columns"] = self.index_columns(object_id, i["index_id"])
        return idx

    def check_constraints(self, object_id: int):
        return self.rows(
            """SELECT name, definition, is_system_named, is_not_trusted, is_disabled
               FROM sys.check_constraints WHERE parent_object_id = %s ORDER BY name""",
            (object_id,),
        )

    def foreign_keys(self):
        fks = self.rows(
            """SELECT fk.object_id, fk.name, fk.is_system_named, fk.delete_referential_action_desc,
                      fk.update_referential_action_desc, fk.is_not_trusted, fk.is_disabled,
                      ps.name AS parent_schema, pt.name AS parent_table,
                      rs.name AS ref_schema, rt.name AS ref_table
               FROM sys.foreign_keys fk
               JOIN sys.tables pt ON pt.object_id = fk.parent_object_id
               JOIN sys.schemas ps ON ps.schema_id = pt.schema_id
               JOIN sys.tables rt ON rt.object_id = fk.referenced_object_id
               JOIN sys.schemas rs ON rs.schema_id = rt.schema_id
               ORDER BY ps.name, pt.name, fk.name"""
        )
        for fk in fks:
            fk["columns"] = self.rows(
                """SELECT pc.name AS parent_col, rc.name AS ref_col
                   FROM sys.foreign_key_columns fkc
                   JOIN sys.columns pc ON pc.object_id = fkc.parent_object_id AND pc.column_id = fkc.parent_column_id
                   JOIN sys.columns rc ON rc.object_id = fkc.referenced_object_id AND rc.column_id = fkc.referenced_column_id
                   WHERE fkc.constraint_object_id = %s ORDER BY fkc.constraint_column_id""",
                (fk["object_id"],),
            )
        return fks

    # ---- modules ----
    def modules(self):
        return self.rows(
            """SELECT o.object_id, s.name AS schema_name, o.name, o.type, o.type_desc,
                      m.definition, m.uses_ansi_nulls, m.uses_quoted_identifier, m.is_schema_bound
               FROM sys.sql_modules m
               JOIN sys.objects o ON o.object_id = m.object_id
               JOIN sys.schemas s ON s.schema_id = o.schema_id
               WHERE o.is_ms_shipped = 0
               ORDER BY o.type, s.name, o.name"""
        )

    def module_dependencies(self):
        return self.rows(
            """SELECT DISTINCT d.referencing_id, d.referenced_id
               FROM sys.sql_expression_dependencies d
               WHERE d.referenced_id IS NOT NULL AND d.referencing_id <> d.referenced_id"""
        )

    # ---- data ----
    def row_count(self, schema: str, table: str) -> int:
        return self.scalar(f"SELECT COUNT_BIG(*) AS n FROM {q(schema)}.{q(table)}")

    def fetch_rows(self, schema: str, table: str, order_cols: list[str]):
        order = ", ".join(q(c) for c in order_cols) if order_cols else None
        sql = f"SELECT * FROM {q(schema)}.{q(table)}"
        if order:
            sql += " ORDER BY " + order
        cur = self.conn.cursor()
        cur.execute(sql)
        return cur


# --------------------------------------------------------------------------------------------------
# Emitters
# --------------------------------------------------------------------------------------------------
def emit_table(cat: Catalog, t, out: list[str]):
    full = f"{q(t['schema_name'])}.{q(t['table_name'])}"
    cols = cat.columns(t["object_id"])
    lines = []
    for c in cols:
        if c["is_computed"]:
            line = f"    {q(c['name'])} AS {c['computed_definition']}"
            if c["is_persisted"]:
                line += " PERSISTED"
            lines.append(line)
            continue
        line = f"    {q(c['name'])} {type_spec(c['type_name'], c['max_length'], c['precision'], c['scale'])}"
        if c["collation_name"]:
            line += f" COLLATE {c['collation_name']}"
        if c["is_identity"]:
            line += f" IDENTITY({int(c['seed_value'])},{int(c['increment_value'])})"
        if c["is_rowguidcol"]:
            line += " ROWGUIDCOL"
        line += " NOT NULL" if not c["is_nullable"] else " NULL"
        if c["default_definition"] is not None:
            if c["default_is_system_named"]:
                line += f" DEFAULT {c['default_definition']}"
            else:
                line += f" CONSTRAINT {q(c['default_name'])} DEFAULT {c['default_definition']}"
        lines.append(line)

    for kc in cat.key_constraints(t["object_id"]):
        kind = "PRIMARY KEY" if kc["type"] == "PK" else "UNIQUE"
        keycols = ", ".join(
            f"{q(col['name'])} {'DESC' if col['is_descending_key'] else 'ASC'}"
            for col in kc["columns"] if not col["is_included_column"]
        )
        line = f"    CONSTRAINT {q(kc['name'])} {kind} {kc['type_desc']} ({keycols})"
        opts = index_options(kc)
        if opts:
            line += f" WITH ({opts})"
        lines.append(line)

    for ck in cat.check_constraints(t["object_id"]):
        line = f"    CONSTRAINT {q(ck['name'])} CHECK {ck['definition']}"
        lines.append(line)

    out.append(f"-- Table {full}")
    out.append(f"CREATE TABLE {full} (")
    out.append(",\n".join(lines))
    out.append(") ON [PRIMARY];")
    if t["lock_escalation_desc"] != "TABLE":
        out.append(f"ALTER TABLE {full} SET (LOCK_ESCALATION = {t['lock_escalation_desc']});")
    out.append("GO")
    out.append("")
    return cols


def index_options(ix) -> str:
    """Only non-default index options are rendered (defaults: PAD_INDEX OFF, FILLFACTOR 0,
    IGNORE_DUP_KEY OFF, ALLOW_ROW_LOCKS ON, ALLOW_PAGE_LOCKS ON)."""
    opts = []
    if ix["is_padded"]:
        opts.append("PAD_INDEX = ON")
    if ix["fill_factor"] not in (0, 100):
        opts.append(f"FILLFACTOR = {ix['fill_factor']}")
    if ix["ignore_dup_key"]:
        opts.append("IGNORE_DUP_KEY = ON")
    if not ix["allow_row_locks"]:
        opts.append("ALLOW_ROW_LOCKS = OFF")
    if not ix["allow_page_locks"]:
        opts.append("ALLOW_PAGE_LOCKS = OFF")
    return ", ".join(opts)


def emit_indexes(cat: Catalog, t, out: list[str]) -> int:
    full = f"{q(t['schema_name'])}.{q(t['table_name'])}"
    n = 0
    for ix in cat.indexes(t["object_id"]):
        keycols = ", ".join(
            f"{q(c['name'])} {'DESC' if c['is_descending_key'] else 'ASC'}"
            for c in ix["columns"] if not c["is_included_column"]
        )
        incl = [q(c["name"]) for c in ix["columns"] if c["is_included_column"]]
        stmt = f"CREATE {'UNIQUE ' if ix['is_unique'] else ''}{ix['type_desc']} INDEX {q(ix['name'])} ON {full} ({keycols})"
        if incl:
            stmt += " INCLUDE (" + ", ".join(incl) + ")"
        if ix["has_filter"]:
            stmt += f" WHERE {ix['filter_definition']}"
        opts = index_options(ix)
        if opts:
            stmt += f" WITH ({opts})"
        stmt += " ON [PRIMARY];"
        out.append(stmt)
        if ix["is_disabled"]:
            out.append(f"ALTER INDEX {q(ix['name'])} ON {full} DISABLE;")
        n += 1
    return n


def emit_foreign_keys(cat: Catalog, out: list[str]) -> int:
    fks = cat.foreign_keys()
    for fk in fks:
        parent = f"{q(fk['parent_schema'])}.{q(fk['parent_table'])}"
        ref = f"{q(fk['ref_schema'])}.{q(fk['ref_table'])}"
        pcols = ", ".join(q(c["parent_col"]) for c in fk["columns"])
        rcols = ", ".join(q(c["ref_col"]) for c in fk["columns"])
        check = "NOCHECK" if fk["is_not_trusted"] else "CHECK"
        stmt = (
            f"ALTER TABLE {parent} WITH {check} ADD CONSTRAINT {q(fk['name'])} FOREIGN KEY ({pcols}) "
            f"REFERENCES {ref} ({rcols})"
        )
        if fk["delete_referential_action_desc"] != "NO_ACTION":
            stmt += " ON DELETE " + fk["delete_referential_action_desc"].replace("_", " ")
        if fk["update_referential_action_desc"] != "NO_ACTION":
            stmt += " ON UPDATE " + fk["update_referential_action_desc"].replace("_", " ")
        out.append(stmt + ";")
        if fk["is_disabled"]:
            out.append(f"ALTER TABLE {parent} NOCHECK CONSTRAINT {q(fk['name'])};")
    return len(fks)


def topo_sort(items, deps):
    """Kahn topological sort; items = list of object_id, deps = {referencing: {referenced}}."""
    ids = set(items)
    indeg = {i: 0 for i in ids}
    rev = defaultdict(set)
    for a in ids:
        for b in deps.get(a, ()):
            if b in ids and b != a:
                indeg[a] += 1
                rev[b].add(a)
    ready = sorted(i for i in ids if indeg[i] == 0)
    order = []
    while ready:
        n = ready.pop(0)
        order.append(n)
        for m in sorted(rev[n]):
            indeg[m] -= 1
            if indeg[m] == 0:
                ready.append(m)
        ready.sort()
    if len(order) != len(ids):
        raise RuntimeError("cyclic dependency between modules")
    return order


HEADER_RX = re.compile(
    r"CREATE\s+(?:PROC(?:EDURE)?|FUNCTION|VIEW|TRIGGER)\s+"
    r"((?:\[?[^\s\[\]\.(]+\]?\.)?\[?[^\s\[\]\.(]+\]?)",
    re.IGNORECASE,
)


def header_name(definition: str) -> str | None:
    """Object name written in the CREATE header of a module definition (without schema/brackets)."""
    m = HEADER_RX.search(definition)
    if not m:
        return None
    return m.group(1).split(".")[-1].strip("[]")


def emit_modules(cat: Catalog, out: list[str], types_filter: set[str] | None = None) -> dict:
    mods = cat.modules()
    if types_filter is not None:
        mods = [m for m in mods if m["type"].strip() in types_filter]
    by_id = {m["object_id"]: m for m in mods}
    deps = defaultdict(set)
    for d in cat.module_dependencies():
        if d["referencing_id"] in by_id and d["referenced_id"] in by_id:
            deps[d["referencing_id"]].add(d["referenced_id"])

    groups = [
        ("Functions (scalar, inline and multi-statement)", {"FN", "IF", "TF"}),
        ("Views", {"V"}),
        ("Stored procedures", {"P"}),
        ("Triggers", {"TR"}),
    ]
    counts = {}
    name_of = lambda oid: (by_id[oid]["schema_name"], by_id[oid]["name"])
    for title, types in groups:
        ids = [m["object_id"] for m in mods if m["type"].strip() in types]
        if not ids:
            continue
        # Functions and views have no deferred name resolution: create referenced ones first.
        # Sorting keys are names so the output is deterministic between two runs.
        if types & {"FN", "IF", "TF", "V"}:
            ordered = topo_sort(sorted(ids, key=name_of), deps)
        else:
            # Modules renamed with sp_rename keep the OLD name in their definition text (documented
            # sp_rename behaviour). They are created first under that old name then renamed, so that a
            # later module legitimately carrying the old name does not collide.
            ordered = sorted(ids, key=lambda oid: (0 if renamed(by_id[oid]) else 1, name_of(oid)))
        out.append(f"-- ===== {title}: {len(ordered)} =====")
        out.append("")
        for oid in ordered:
            m = by_id[oid]
            module_text_is_batch_safe(m["definition"])
            out.append(f"SET ANSI_NULLS {'ON' if m['uses_ansi_nulls'] else 'OFF'};")
            out.append(f"SET QUOTED_IDENTIFIER {'ON' if m['uses_quoted_identifier'] else 'OFF'};")
            out.append("GO")
            definition = m["definition"]
            if not definition.endswith("\n"):
                definition += "\n"
            out.append(definition.rstrip("\n"))
            out.append("GO")
            if renamed(m):
                old_name = header_name(m["definition"])
                out.append(
                    f"-- sys.objects.name is {m['name']!r} but the stored definition says {old_name!r}: "
                    "reproduce the sp_rename done by the official scripts"
                )
                out.append(
                    f"EXEC sys.sp_rename @objname = N'{q(m['schema_name'])}.{q(old_name)}', "
                    f"@newname = N'{m['name'].replace(chr(39), chr(39) * 2)}', @objtype = 'OBJECT';"
                )
                out.append("GO")
            out.append("")
        counts[title] = len(ordered)
    return counts


def renamed(m) -> bool:
    hn = header_name(m["definition"])
    return hn is not None and hn.lower() != m["name"].lower()


def emit_data(cat: Catalog, t, cols, out: list[str]) -> int:
    schema, table = t["schema_name"], t["table_name"]
    full = f"{q(schema)}.{q(table)}"
    n = cat.row_count(schema, table)
    if n == 0:
        return 0
    insertable = [c for c in cols if not c["is_computed"]]
    has_identity = any(c["is_identity"] for c in insertable)
    pk = [kc for kc in cat.key_constraints(t["object_id"]) if kc["type"] == "PK"]
    if pk:
        order_cols = [c["name"] for c in pk[0]["columns"] if not c["is_included_column"]]
    else:
        order_cols = [c["name"] for c in insertable if c["is_identity"]] or [insertable[0]["name"]]

    col_list = ", ".join(q(c["name"]) for c in insertable)
    type_by_name = {c["name"]: c["type_name"] for c in cols}

    out.append(f"-- Data {full}: {n} rows")
    if has_identity:
        out.append(f"SET IDENTITY_INSERT {full} ON;")
    cur = cat.fetch_rows(schema, table, order_cols)
    names = [d[0] for d in cur.description]
    idx = [names.index(c["name"]) for c in insertable]
    batch = []
    written = 0

    def flush():
        nonlocal batch
        if not batch:
            return
        out.append(f"INSERT INTO {full} ({col_list}) VALUES")
        out.append(",\n".join(batch) + ";")
        batch = []

    for row in cur:
        vals = ", ".join(sql_literal(row[i], type_by_name[names[i]]) for i in idx)
        batch.append(f"({vals})")
        written += 1
        if len(batch) == ROWS_PER_INSERT:
            flush()
    flush()
    if has_identity:
        out.append(f"SET IDENTITY_INSERT {full} OFF;")
    out.append("GO")
    out.append("")
    if written != n:
        raise RuntimeError(f"{full}: counted {n} rows but fetched {written}")
    return written


def emit_identity_sync(cat: Catalog, tables_cols, out: list[str]) -> int:
    """Make IDENT_CURRENT() of every identity column equal to the source.

    sys.identity_columns.last_value is NULL until the first insert. For a table that holds rows,
    DBCC CHECKIDENT RESEED to last_value is enough. For an EMPTY table whose identity was used then
    the rows deleted, DBCC CHECKIDENT on a fresh table would make the NEXT value = last_value (docs:
    "if no rows have been inserted since the table was created ... the first row inserted uses
    new_reseed_value"), so a throw-away row carrying the identity value is inserted then deleted:
    afterwards the next value is last_value + increment, exactly as in the source.
    """
    n = 0
    for t, cols in tables_cols:
        full = f"{q(t['schema_name'])}.{q(t['table_name'])}"
        ident = [c for c in cols if c["is_identity"]]
        if not ident or ident[0]["last_value"] is None:
            continue
        c = ident[0]
        last = int(c["last_value"])
        rows = cat.row_count(t["schema_name"], t["table_name"])
        if rows > 0:
            out.append(f"DBCC CHECKIDENT ('{t['schema_name']}.{t['table_name']}', RESEED, {last}) WITH NO_INFOMSGS;")
        else:
            required = [x for x in cols if not x["is_computed"] and not x["is_nullable"] and x["default_definition"] is None]
            names = ", ".join(q(x["name"]) for x in required)
            vals = ", ".join(str(last) if x["is_identity"] else placeholder(x["type_name"]) for x in required)
            out.append(f"SET IDENTITY_INSERT {full} ON;")
            out.append(f"INSERT INTO {full} ({names}) VALUES ({vals});")
            out.append(f"SET IDENTITY_INSERT {full} OFF;")
            out.append(f"DELETE FROM {full} WHERE {q(c['name'])} = {last};")
        n += 1
    out.append("GO")
    out.append("")
    return n


def placeholder(type_name: str) -> str:
    t = type_name.lower()
    if t in ("varchar", "char", "nvarchar", "nchar", "text", "ntext", "sysname"):
        return "N''"
    if t in ("datetime", "smalldatetime", "datetime2", "date"):
        return "'1900-01-01'"
    if t in ("varbinary", "binary", "image"):
        return "0x"
    if t == "uniqueidentifier":
        return "'00000000-0000-0000-0000-000000000000'"
    if t == "time":
        return "'00:00:00'"
    return "0"


# --------------------------------------------------------------------------------------------------
# Main
# --------------------------------------------------------------------------------------------------
def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--server", default="localhost")
    ap.add_argument("--port", type=int, default=1433)
    ap.add_argument("--user", default="sa")
    ap.add_argument("--password", required=True)
    ap.add_argument("--database", default="EE")
    ap.add_argument("--output", required=True)
    args = ap.parse_args()

    conn = pymssql.connect(server=args.server, port=args.port, user=args.user, password=args.password,
                           database=args.database, charset="UTF-8")
    cat = Catalog(conn)
    info = cat.database_info()

    out: list[str] = []
    hdr_index = len(out)
    out.append("")  # header placeholder

    out.append(":on error exit")
    out.append("SET NOCOUNT ON;")
    out.append("SET ANSI_NULLS ON;")
    out.append("SET QUOTED_IDENTIFIER ON;")
    out.append("SET ANSI_PADDING ON;")
    out.append("GO")
    out.append("-- ===== Target guard =====")
    out.append("IF DB_NAME() IN (N'master', N'tempdb', N'model', N'msdb')")
    out.append("    RAISERROR('EE_DR.sql: refuse to run in system database %s', 16, 1, @@SERVERNAME);")
    out.append(f"IF CONVERT(sysname, DATABASEPROPERTYEX(DB_NAME(), 'Collation')) <> N'{info['collation_name']}'")
    out.append(f"    RAISERROR('EE_DR.sql: target database collation must be {info['collation_name']}', 16, 1);")
    out.append("IF EXISTS (SELECT 1 FROM sys.tables WHERE is_ms_shipped = 0)")
    out.append("    RAISERROR('EE_DR.sql: target database already contains user tables', 16, 1);")
    out.append("GO")
    out.append("")

    # Stored procedures are created BEFORE the tables on purpose: with deferred name resolution a
    # procedure compiles when the tables it references do not exist yet, whereas once a table exists
    # every column it names is checked (Msg 207). The source database holds procedures written for
    # columns that later update scripts dropped (e.g. SOUPRO.INASSEMBLIE, added by V21 and dropped by
    # V36); creating them after the tables would fail although they exist in the source.
    mod_counts = emit_modules(cat, out, {"P"})

    tables = cat.tables()
    out.append(f"-- ===== Tables: {len(tables)} =====")
    out.append("")
    tables_cols = []
    for t in tables:
        cols = emit_table(cat, t, out)
        tables_cols.append((t, cols))

    out.append("-- ===== Indexes (not backing a PK/UNIQUE constraint) =====")
    n_idx = 0
    for t, _ in tables_cols:
        n_idx += emit_indexes(cat, t, out)
    out.append("GO")
    out.append("")

    out.append("-- ===== Foreign keys =====")
    n_fk = emit_foreign_keys(cat, out)
    out.append("GO")
    out.append("")

    mod_counts.update(emit_modules(cat, out, {"FN", "IF", "TF", "V", "TR"}))

    out.append("-- ===== Data =====")
    out.append("")
    n_rows = 0
    n_tables_with_rows = 0
    for t, cols in tables_cols:
        w = emit_data(cat, t, cols, out)
        n_rows += w
        n_tables_with_rows += 1 if w else 0

    out.append("-- ===== Identity values (IDENT_CURRENT) aligned with the source =====")
    n_ident = emit_identity_sync(cat, tables_cols, out)

    out.append("-- ===== End =====")
    out.append("PRINT 'EE_DR.sql applied to ' + DB_NAME();")
    out.append("GO")

    now_local = dt.datetime.now(ZoneInfo("America/Toronto"))
    header = [
        "-- EE_DR.sql -- consolidated schema + modules + reference data + DR seeded rows",
        f"-- Generated {now_local.strftime('%Y-%m-%d %H:%M:%S %Z')} by eewin/tools/generate_ee_dr_sql.py (pymssql {pymssql.__version__})",
        f"-- Source database: {info['name']} on {info['server_version'].splitlines()[0].strip()}",
        f"-- Source collation: {info['collation_name']}, compatibility_level {info['compatibility_level']}",
        f"-- Tables {len(tables)}, indexes {n_idx}, foreign keys {n_fk}, "
        + ", ".join(f"{k.split(' (')[0].lower()} {v}" for k, v in mod_counts.items())
        + f", rows {n_rows} in {n_tables_with_rows} tables, identity resync {n_ident}",
        "--",
        "-- Reload (empty target database with the same collation):",
        f"--   sqlcmd -S <server> -U sa -P '<pwd>' -C -Q \"CREATE DATABASE EE_TEST COLLATE {info['collation_name']}\"",
        "--   sqlcmd -S <server> -U sa -P '<pwd>' -C -d EE_TEST -f 65001 -x -b -I -i EE_DR.sql",
        "-- File is UTF-8 (-f 65001); -x disables sqlcmd variable substitution; -b/:on error exit stop on first error.",
    ]
    out[hdr_index] = "\n".join(header)

    text = "\n".join(out) + "\n"
    with open(args.output, "w", encoding="utf-8", newline="\n") as f:
        f.write(text)
    sha = hashlib.sha256(text.encode("utf-8")).hexdigest()
    print(f"wrote {args.output}: {len(text.encode('utf-8'))} bytes, sha256 {sha}")
    print(f"tables={len(tables)} indexes={n_idx} fks={n_fk} modules={mod_counts} rows={n_rows} identity_resync={n_ident}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
