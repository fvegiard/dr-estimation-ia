-- compare_ee_databases.sql -- compare two databases on the same instance, object by object and row by row.
-- Usage:
--   sqlcmd -S <server> -U sa -P '<pwd>' -C -W -s '|' -v SRC=EE DST=EE_TEST -i compare_ee_databases.sql
-- Every result set is a difference list: an empty list means identical. The last result set is the summary.
SET NOCOUNT ON;
DECLARE @src sysname = N'$(SRC)', @dst sysname = N'$(DST)';
DECLARE @s nvarchar(300) = QUOTENAME(@src), @d nvarchar(300) = QUOTENAME(@dst);
DECLARE @sql nvarchar(max);
DECLARE @mismatch TABLE (check_name sysname, differences int);

PRINT '== 1. Database properties (' + @src + ' vs ' + @dst + ')';
SELECT name, collation_name, compatibility_level, recovery_model_desc, is_ansi_nulls_on, is_quoted_identifier_on
FROM sys.databases WHERE name IN (@src, @dst) ORDER BY CASE WHEN name = @src THEN 0 ELSE 1 END;

PRINT '== 2. Object counts by type';
SET @sql = N'
SELECT ISNULL(a.type_desc, b.type_desc) AS type_desc, a.n AS ' + QUOTENAME(@src) + N', b.n AS ' + QUOTENAME(@dst) + N'
FROM (SELECT type_desc, COUNT(*) n FROM ' + @s + N'.sys.objects WHERE is_ms_shipped = 0 GROUP BY type_desc) a
FULL JOIN (SELECT type_desc, COUNT(*) n FROM ' + @d + N'.sys.objects WHERE is_ms_shipped = 0 GROUP BY type_desc) b
  ON a.type_desc = b.type_desc
ORDER BY 1;';
EXEC sp_executesql @sql;

-- ---------------------------------------------------------------------------------------------
PRINT '== 3. Tables present in one database only';
CREATE TABLE #t3 (side sysname, schema_name sysname, table_name sysname);
SET @sql = N'
INSERT #t3 SELECT N''only in ' + @src + N''', s.name, t.name FROM ' + @s + N'.sys.tables t JOIN ' + @s + N'.sys.schemas s ON s.schema_id = t.schema_id
EXCEPT SELECT N''only in ' + @src + N''', s.name, t.name FROM ' + @d + N'.sys.tables t JOIN ' + @d + N'.sys.schemas s ON s.schema_id = t.schema_id;
INSERT #t3 SELECT N''only in ' + @dst + N''', s.name, t.name FROM ' + @d + N'.sys.tables t JOIN ' + @d + N'.sys.schemas s ON s.schema_id = t.schema_id
EXCEPT SELECT N''only in ' + @dst + N''', s.name, t.name FROM ' + @s + N'.sys.tables t JOIN ' + @s + N'.sys.schemas s ON s.schema_id = t.schema_id;';
EXEC sp_executesql @sql;
SELECT * FROM #t3 ORDER BY 1, 2, 3;
INSERT @mismatch SELECT N'3. table list', COUNT(*) FROM #t3;

-- ---------------------------------------------------------------------------------------------
PRINT '== 4. Row counts per table (COUNT(*) on both sides)';
CREATE TABLE #t4 (schema_name sysname, table_name sysname, rows_src bigint, rows_dst bigint);
SET @sql = N'
INSERT #t4 (schema_name, table_name)
SELECT s.name, t.name FROM ' + @s + N'.sys.tables t JOIN ' + @s + N'.sys.schemas s ON s.schema_id = t.schema_id;';
EXEC sp_executesql @sql;
DECLARE @sch sysname, @tbl sysname;
DECLARE c4 CURSOR LOCAL FAST_FORWARD FOR SELECT schema_name, table_name FROM #t4;
OPEN c4; FETCH NEXT FROM c4 INTO @sch, @tbl;
WHILE @@FETCH_STATUS = 0
BEGIN
    SET @sql = N'UPDATE #t4 SET rows_src = (SELECT COUNT_BIG(*) FROM ' + @s + N'.' + QUOTENAME(@sch) + N'.' + QUOTENAME(@tbl) + N')'
             + N', rows_dst = (SELECT COUNT_BIG(*) FROM ' + @d + N'.' + QUOTENAME(@sch) + N'.' + QUOTENAME(@tbl) + N')'
             + N' WHERE schema_name = @sch AND table_name = @tbl;';
    EXEC sp_executesql @sql, N'@sch sysname, @tbl sysname', @sch, @tbl;
    FETCH NEXT FROM c4 INTO @sch, @tbl;
END
CLOSE c4; DEALLOCATE c4;
SELECT schema_name, table_name, rows_src AS rows_in_src, rows_dst AS rows_in_dst,
       CASE WHEN rows_src = rows_dst THEN 'same' ELSE 'DIFFERENT' END AS verdict
FROM #t4 ORDER BY rows_src DESC, table_name;
SELECT SUM(rows_src) AS total_rows_src, SUM(rows_dst) AS total_rows_dst, COUNT(*) AS tables_compared FROM #t4;
INSERT @mismatch SELECT N'4. row counts', COUNT(*) FROM #t4 WHERE rows_src <> rows_dst OR rows_dst IS NULL;

-- ---------------------------------------------------------------------------------------------
PRINT '== 5. Columns (INFORMATION_SCHEMA.COLUMNS + sys.columns attributes) differing';
CREATE TABLE #t5 (side sysname, table_name sysname, column_name sysname, ordinal int, data_type sysname,
                  char_len int, num_prec int, num_scale int, is_nullable varchar(3), column_default nvarchar(4000),
                  collation_name sysname NULL, is_identity bit, seed bigint NULL, increment bigint NULL);
SET @sql = N'
WITH a AS (
  SELECT c.TABLE_NAME, c.COLUMN_NAME, c.ORDINAL_POSITION, c.DATA_TYPE, c.CHARACTER_MAXIMUM_LENGTH, c.NUMERIC_PRECISION,
         c.NUMERIC_SCALE, c.IS_NULLABLE, c.COLUMN_DEFAULT, sc.collation_name, sc.is_identity,
         CONVERT(bigint, ic.seed_value) AS seed, CONVERT(bigint, ic.increment_value) AS increment
  FROM ' + @s + N'.INFORMATION_SCHEMA.COLUMNS c
  JOIN ' + @s + N'.sys.columns sc ON sc.object_id = OBJECT_ID(' + QUOTENAME(@src, '''') + N' + ''.'' + QUOTENAME(c.TABLE_SCHEMA) + ''.'' + QUOTENAME(c.TABLE_NAME)) AND sc.name = c.COLUMN_NAME
  LEFT JOIN ' + @s + N'.sys.identity_columns ic ON ic.object_id = sc.object_id AND ic.column_id = sc.column_id
), b AS (
  SELECT c.TABLE_NAME, c.COLUMN_NAME, c.ORDINAL_POSITION, c.DATA_TYPE, c.CHARACTER_MAXIMUM_LENGTH, c.NUMERIC_PRECISION,
         c.NUMERIC_SCALE, c.IS_NULLABLE, c.COLUMN_DEFAULT, sc.collation_name, sc.is_identity,
         CONVERT(bigint, ic.seed_value) AS seed, CONVERT(bigint, ic.increment_value) AS increment
  FROM ' + @d + N'.INFORMATION_SCHEMA.COLUMNS c
  JOIN ' + @d + N'.sys.columns sc ON sc.object_id = OBJECT_ID(' + QUOTENAME(@dst, '''') + N' + ''.'' + QUOTENAME(c.TABLE_SCHEMA) + ''.'' + QUOTENAME(c.TABLE_NAME)) AND sc.name = c.COLUMN_NAME
  LEFT JOIN ' + @d + N'.sys.identity_columns ic ON ic.object_id = sc.object_id AND ic.column_id = sc.column_id
)
INSERT #t5 SELECT N''only in ' + @src + N''', * FROM (SELECT * FROM a EXCEPT SELECT * FROM b) x
UNION ALL   SELECT N''only in ' + @dst + N''', * FROM (SELECT * FROM b EXCEPT SELECT * FROM a) y;';
EXEC sp_executesql @sql;
SELECT * FROM #t5 ORDER BY table_name, ordinal, side;
SET @sql = N'SELECT (SELECT COUNT(*) FROM ' + @s + N'.INFORMATION_SCHEMA.COLUMNS) AS columns_src, (SELECT COUNT(*) FROM ' + @d + N'.INFORMATION_SCHEMA.COLUMNS) AS columns_dst;';
EXEC sp_executesql @sql;
INSERT @mismatch SELECT N'5. columns', COUNT(*) FROM #t5;

-- ---------------------------------------------------------------------------------------------
PRINT '== 6. Indexes and key constraints (name, type, unique, PK, key columns, included columns) differing';
CREATE TABLE #t6 (side sysname, table_name sysname, index_name sysname, type_desc nvarchar(60), is_unique bit,
                  is_primary_key bit, is_unique_constraint bit, key_columns nvarchar(max), included_columns nvarchar(max),
                  allow_page_locks bit, allow_row_locks bit, fill_factor tinyint);
SET @sql = N'
WITH a AS (
  SELECT t.name AS table_name, i.name AS index_name, i.type_desc, i.is_unique, i.is_primary_key, i.is_unique_constraint,
         (SELECT STRING_AGG(QUOTENAME(c.name) + CASE WHEN ic.is_descending_key = 1 THEN '' DESC'' ELSE '' ASC'' END, '', '') WITHIN GROUP (ORDER BY ic.key_ordinal)
            FROM ' + @s + N'.sys.index_columns ic JOIN ' + @s + N'.sys.columns c ON c.object_id = ic.object_id AND c.column_id = ic.column_id
           WHERE ic.object_id = i.object_id AND ic.index_id = i.index_id AND ic.is_included_column = 0) AS key_columns,
         (SELECT STRING_AGG(QUOTENAME(c.name), '', '') WITHIN GROUP (ORDER BY ic.index_column_id)
            FROM ' + @s + N'.sys.index_columns ic JOIN ' + @s + N'.sys.columns c ON c.object_id = ic.object_id AND c.column_id = ic.column_id
           WHERE ic.object_id = i.object_id AND ic.index_id = i.index_id AND ic.is_included_column = 1) AS included_columns,
         i.allow_page_locks, i.allow_row_locks, i.fill_factor
  FROM ' + @s + N'.sys.indexes i JOIN ' + @s + N'.sys.tables t ON t.object_id = i.object_id WHERE i.type > 0
), b AS (
  SELECT t.name AS table_name, i.name AS index_name, i.type_desc, i.is_unique, i.is_primary_key, i.is_unique_constraint,
         (SELECT STRING_AGG(QUOTENAME(c.name) + CASE WHEN ic.is_descending_key = 1 THEN '' DESC'' ELSE '' ASC'' END, '', '') WITHIN GROUP (ORDER BY ic.key_ordinal)
            FROM ' + @d + N'.sys.index_columns ic JOIN ' + @d + N'.sys.columns c ON c.object_id = ic.object_id AND c.column_id = ic.column_id
           WHERE ic.object_id = i.object_id AND ic.index_id = i.index_id AND ic.is_included_column = 0) AS key_columns,
         (SELECT STRING_AGG(QUOTENAME(c.name), '', '') WITHIN GROUP (ORDER BY ic.index_column_id)
            FROM ' + @d + N'.sys.index_columns ic JOIN ' + @d + N'.sys.columns c ON c.object_id = ic.object_id AND c.column_id = ic.column_id
           WHERE ic.object_id = i.object_id AND ic.index_id = i.index_id AND ic.is_included_column = 1) AS included_columns,
         i.allow_page_locks, i.allow_row_locks, i.fill_factor
  FROM ' + @d + N'.sys.indexes i JOIN ' + @d + N'.sys.tables t ON t.object_id = i.object_id WHERE i.type > 0
)
INSERT #t6 SELECT N''only in ' + @src + N''', * FROM (SELECT * FROM a EXCEPT SELECT * FROM b) x
UNION ALL   SELECT N''only in ' + @dst + N''', * FROM (SELECT * FROM b EXCEPT SELECT * FROM a) y;';
EXEC sp_executesql @sql;
SELECT * FROM #t6 ORDER BY table_name, index_name, side;
SET @sql = N'SELECT (SELECT COUNT(*) FROM ' + @s + N'.sys.indexes i JOIN ' + @s + N'.sys.tables t ON t.object_id = i.object_id WHERE i.type > 0) AS indexes_src,
                   (SELECT COUNT(*) FROM ' + @d + N'.sys.indexes i JOIN ' + @d + N'.sys.tables t ON t.object_id = i.object_id WHERE i.type > 0) AS indexes_dst;';
EXEC sp_executesql @sql;
INSERT @mismatch SELECT N'6. indexes/keys', COUNT(*) FROM #t6;

-- ---------------------------------------------------------------------------------------------
PRINT '== 7. Default constraints (table, column, definition; names compared only when user-named) differing';
CREATE TABLE #t7 (side sysname, table_name sysname, column_name sysname, definition nvarchar(max), constraint_name sysname NULL);
SET @sql = N'
WITH a AS (
  SELECT OBJECT_NAME(dc.parent_object_id, DB_ID(' + QUOTENAME(@src, '''') + N')) AS table_name, c.name AS column_name, dc.definition,
         CASE WHEN dc.is_system_named = 1 THEN NULL ELSE dc.name END AS constraint_name
  FROM ' + @s + N'.sys.default_constraints dc JOIN ' + @s + N'.sys.columns c ON c.object_id = dc.parent_object_id AND c.column_id = dc.parent_column_id
), b AS (
  SELECT OBJECT_NAME(dc.parent_object_id, DB_ID(' + QUOTENAME(@dst, '''') + N')) AS table_name, c.name AS column_name, dc.definition,
         CASE WHEN dc.is_system_named = 1 THEN NULL ELSE dc.name END AS constraint_name
  FROM ' + @d + N'.sys.default_constraints dc JOIN ' + @d + N'.sys.columns c ON c.object_id = dc.parent_object_id AND c.column_id = dc.parent_column_id
)
INSERT #t7 SELECT N''only in ' + @src + N''', * FROM (SELECT * FROM a EXCEPT SELECT * FROM b) x
UNION ALL   SELECT N''only in ' + @dst + N''', * FROM (SELECT * FROM b EXCEPT SELECT * FROM a) y;';
EXEC sp_executesql @sql;
SELECT * FROM #t7 ORDER BY table_name, column_name, side;
SET @sql = N'SELECT (SELECT COUNT(*) FROM ' + @s + N'.sys.default_constraints) AS defaults_src, (SELECT COUNT(*) FROM ' + @d + N'.sys.default_constraints) AS defaults_dst,
                   (SELECT COUNT(*) FROM ' + @s + N'.sys.foreign_keys) AS fks_src, (SELECT COUNT(*) FROM ' + @d + N'.sys.foreign_keys) AS fks_dst,
                   (SELECT COUNT(*) FROM ' + @s + N'.sys.check_constraints) AS checks_src, (SELECT COUNT(*) FROM ' + @d + N'.sys.check_constraints) AS checks_dst;';
EXEC sp_executesql @sql;
INSERT @mismatch SELECT N'7. defaults', COUNT(*) FROM #t7;

-- ---------------------------------------------------------------------------------------------
PRINT '== 8. Modules (procedures/functions/views/triggers): name, type, SHA2_256 of definition, SET options differing';
CREATE TABLE #t8 (side sysname, schema_name sysname, object_name sysname, type char(2), definition_sha256 varbinary(32),
                  uses_ansi_nulls bit, uses_quoted_identifier bit);
SET @sql = N'
WITH a AS (
  SELECT s.name AS schema_name, o.name AS object_name, o.type, HASHBYTES(''SHA2_256'', m.definition) AS definition_sha256, m.uses_ansi_nulls, m.uses_quoted_identifier
  FROM ' + @s + N'.sys.sql_modules m JOIN ' + @s + N'.sys.objects o ON o.object_id = m.object_id JOIN ' + @s + N'.sys.schemas s ON s.schema_id = o.schema_id
  WHERE o.is_ms_shipped = 0
), b AS (
  SELECT s.name AS schema_name, o.name AS object_name, o.type, HASHBYTES(''SHA2_256'', m.definition) AS definition_sha256, m.uses_ansi_nulls, m.uses_quoted_identifier
  FROM ' + @d + N'.sys.sql_modules m JOIN ' + @d + N'.sys.objects o ON o.object_id = m.object_id JOIN ' + @d + N'.sys.schemas s ON s.schema_id = o.schema_id
  WHERE o.is_ms_shipped = 0
)
INSERT #t8 SELECT N''only in ' + @src + N''', * FROM (SELECT * FROM a EXCEPT SELECT * FROM b) x
UNION ALL   SELECT N''only in ' + @dst + N''', * FROM (SELECT * FROM b EXCEPT SELECT * FROM a) y;';
EXEC sp_executesql @sql;
SELECT side, schema_name, object_name, type, CONVERT(char(64), definition_sha256, 2) AS definition_sha256, uses_ansi_nulls, uses_quoted_identifier
FROM #t8 ORDER BY object_name, side;
SET @sql = N'SELECT ISNULL(a.type, b.type) AS type, a.n AS modules_src, b.n AS modules_dst, a.chars AS definition_chars_src, b.chars AS definition_chars_dst
FROM (SELECT o.type, COUNT(*) n, SUM(LEN(m.definition)) chars FROM ' + @s + N'.sys.sql_modules m JOIN ' + @s + N'.sys.objects o ON o.object_id = m.object_id GROUP BY o.type) a
FULL JOIN (SELECT o.type, COUNT(*) n, SUM(LEN(m.definition)) chars FROM ' + @d + N'.sys.sql_modules m JOIN ' + @d + N'.sys.objects o ON o.object_id = m.object_id GROUP BY o.type) b ON a.type = b.type
ORDER BY 1;';
EXEC sp_executesql @sql;
INSERT @mismatch SELECT N'8. modules', COUNT(*) FROM #t8;

-- ---------------------------------------------------------------------------------------------
PRINT '== 9. Identity current values (sys.identity_columns.last_value) differing';
CREATE TABLE #t9 (side sysname, table_name sysname, column_name sysname, last_value bigint NULL);
SET @sql = N'
WITH a AS (SELECT OBJECT_NAME(object_id, DB_ID(' + QUOTENAME(@src, '''') + N')) AS t, name, CONVERT(bigint, last_value) AS last_value FROM ' + @s + N'.sys.identity_columns),
     b AS (SELECT OBJECT_NAME(object_id, DB_ID(' + QUOTENAME(@dst, '''') + N')) AS t, name, CONVERT(bigint, last_value) AS last_value FROM ' + @d + N'.sys.identity_columns)
INSERT #t9 SELECT N''only in ' + @src + N''', * FROM (SELECT * FROM a EXCEPT SELECT * FROM b) x
UNION ALL   SELECT N''only in ' + @dst + N''', * FROM (SELECT * FROM b EXCEPT SELECT * FROM a) y;';
EXEC sp_executesql @sql;
SELECT * FROM #t9 ORDER BY table_name, side;
SET @sql = N'SELECT OBJECT_NAME(a.object_id, DB_ID(' + QUOTENAME(@src, '''') + N')) AS table_name, CONVERT(bigint, a.last_value) AS last_value_src, CONVERT(bigint, b.last_value) AS last_value_dst
FROM ' + @s + N'.sys.identity_columns a JOIN ' + @d + N'.sys.identity_columns b ON OBJECT_NAME(a.object_id, DB_ID(' + QUOTENAME(@src, '''') + N')) = OBJECT_NAME(b.object_id, DB_ID(' + QUOTENAME(@dst, '''') + N'))
WHERE a.last_value IS NOT NULL OR b.last_value IS NOT NULL ORDER BY 1;';
EXEC sp_executesql @sql;
INSERT @mismatch SELECT N'9. identity values', COUNT(*) FROM #t9;

-- ---------------------------------------------------------------------------------------------
PRINT '== 10. Data: full row-by-row EXCEPT in both directions for every table (text columns cast to varchar(max))';
CREATE TABLE #t10 (table_name sysname, rows_src bigint, rows_dst bigint, only_in_src bigint, only_in_dst bigint);
DECLARE @cols nvarchar(max);
DECLARE c10 CURSOR LOCAL FAST_FORWARD FOR SELECT schema_name, table_name FROM #t4 WHERE rows_dst IS NOT NULL;
OPEN c10; FETCH NEXT FROM c10 INTO @sch, @tbl;
WHILE @@FETCH_STATUS = 0
BEGIN
    SET @cols = NULL;
    SET @sql = N'SELECT @cols = STRING_AGG(CASE WHEN tp.name IN (''text'', ''ntext'') THEN ''CONVERT(nvarchar(max), '' + QUOTENAME(c.name) + '') AS '' + QUOTENAME(c.name)
                                                WHEN tp.name = ''image'' THEN ''CONVERT(varbinary(max), '' + QUOTENAME(c.name) + '') AS '' + QUOTENAME(c.name)
                                                ELSE QUOTENAME(c.name) END, '', '') WITHIN GROUP (ORDER BY c.column_id)
                 FROM ' + @s + N'.sys.columns c JOIN ' + @s + N'.sys.types tp ON tp.user_type_id = c.user_type_id
                 WHERE c.object_id = OBJECT_ID(' + QUOTENAME(@src + N'.' + @sch + N'.' + @tbl, '''') + N');';
    EXEC sp_executesql @sql, N'@cols nvarchar(max) OUTPUT', @cols OUTPUT;
    SET @sql = N'INSERT #t10 SELECT @tbl,
        (SELECT COUNT_BIG(*) FROM ' + @s + N'.' + QUOTENAME(@sch) + N'.' + QUOTENAME(@tbl) + N'),
        (SELECT COUNT_BIG(*) FROM ' + @d + N'.' + QUOTENAME(@sch) + N'.' + QUOTENAME(@tbl) + N'),
        (SELECT COUNT_BIG(*) FROM (SELECT ' + @cols + N' FROM ' + @s + N'.' + QUOTENAME(@sch) + N'.' + QUOTENAME(@tbl) + N' EXCEPT SELECT ' + @cols + N' FROM ' + @d + N'.' + QUOTENAME(@sch) + N'.' + QUOTENAME(@tbl) + N') x),
        (SELECT COUNT_BIG(*) FROM (SELECT ' + @cols + N' FROM ' + @d + N'.' + QUOTENAME(@sch) + N'.' + QUOTENAME(@tbl) + N' EXCEPT SELECT ' + @cols + N' FROM ' + @s + N'.' + QUOTENAME(@sch) + N'.' + QUOTENAME(@tbl) + N') y);';
    EXEC sp_executesql @sql, N'@tbl sysname', @tbl;
    FETCH NEXT FROM c10 INTO @sch, @tbl;
END
CLOSE c10; DEALLOCATE c10;
SELECT table_name, rows_src, rows_dst, only_in_src, only_in_dst,
       CASE WHEN rows_src = rows_dst AND only_in_src = 0 AND only_in_dst = 0 THEN 'identical' ELSE 'DIFFERENT' END AS verdict
FROM #t10 WHERE rows_src > 0 OR rows_dst > 0 ORDER BY rows_src DESC, table_name;
SELECT COUNT(*) AS tables_with_rows_compared, SUM(rows_src) AS rows_src, SUM(rows_dst) AS rows_dst, SUM(only_in_src) AS only_in_src, SUM(only_in_dst) AS only_in_dst FROM #t10;
INSERT @mismatch SELECT N'10. data (row-level EXCEPT)', COUNT(*) FROM #t10 WHERE rows_src <> rows_dst OR only_in_src <> 0 OR only_in_dst <> 0;
INSERT @mismatch SELECT N'10b. tables skipped by data check (must be 0)', (SELECT COUNT(*) FROM #t4) - (SELECT COUNT(*) FROM #t10);

-- ---------------------------------------------------------------------------------------------
PRINT '== SUMMARY (0 differences everywhere = ' + @dst + ' is a faithful copy of ' + @src + ')';
SELECT check_name, differences FROM @mismatch ORDER BY check_name;
SELECT CASE WHEN SUM(differences) = 0 THEN 'IDENTICAL' ELSE 'DIFFERENCES FOUND' END AS overall_verdict, SUM(differences) AS total_differences FROM @mismatch;

DROP TABLE #t3; DROP TABLE #t4; DROP TABLE #t5; DROP TABLE #t6; DROP TABLE #t7; DROP TABLE #t8; DROP TABLE #t9; DROP TABLE #t10;
