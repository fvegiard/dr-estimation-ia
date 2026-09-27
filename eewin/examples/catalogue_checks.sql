-- Catalogue mechanics: reproducible checks against the live EE database.
-- Run: docker exec -i eewin /opt/mssql-tools18/bin/sqlcmd -S localhost -U sa -P '<pw>' -C -d EE -W -s '|' -i catalogue_checks.sql
-- Every result below is cited in eewin/docs/CATALOGUE-ET-LIEN-QPL.md.
SET NOCOUNT ON;

PRINT '--- 1. Row counts of the catalogue tables (only PROCORRESP carries data)';
SELECT t.name AS tbl, p.rows
FROM sys.tables t
JOIN sys.partitions p ON p.object_id = t.object_id AND p.index_id IN (0, 1)
WHERE t.name IN ('PRODUITS', 'PriceUpdate_Products', 'PROCORRESP', 'ENSEMBLE', 'ENSCOMPO', 'PROCAT', 'PROGLOSS', 'BDEE', 'BDEE_MULTI')
ORDER BY t.name;

PRINT '--- 2. PROCORRESP: old division -> new division';
SELECT OLDDIV, NEWDIV, COUNT(*) AS n
FROM PROCORRESP
GROUP BY OLDDIV, NEWDIV
ORDER BY n DESC;

PRINT '--- 3. PROCORRESP: totals, identical keys, distinct pairs, key lengths';
SELECT COUNT(*) AS total_rows,
       SUM(CASE WHEN OLDCLEMANU = NEWCLEMANU THEN 1 ELSE 0 END) AS same_clemanu,
       SUM(CASE WHEN OLDDIV = NEWDIV THEN 1 ELSE 0 END) AS same_div,
       COUNT(DISTINCT OLDDIV + '|' + OLDCLEMANU) AS distinct_old_pairs,
       COUNT(DISTINCT NEWDIV + '|' + NEWCLEMANU) AS distinct_new_pairs,
       MAX(LEN(OLDCLEMANU)) AS max_len_old,
       MAX(LEN(NEWCLEMANU)) AS max_len_new,
       COUNT(ISUSER) AS isuser_not_null
FROM PROCORRESP;

PRINT '--- 4. The 16 ItemType="P" keys found in Dupuis QPLs vs PROCORRESP.NEWCLEMANU (NEWDIV = LQE)';
SELECT k.qpl_key,
       COUNT(p.UniqueId) AS n_rows_lqe,
       MIN(p.OLDDIV + ':' + p.OLDCLEMANU) AS example_old_key
FROM (VALUES ('IBE52171K'), ('HOFASE884'), ('HOFASE12124'), ('IBE72151K'), ('HOFASE24246'), ('HOFASE664'),
             ('HOFASE12126'), ('HUBHBL2810'), ('CAB3/0BARECU'), ('SCEPVC2'), ('CAB3/0RW90GRE'), ('SCEPVC11/4'),
             ('CONEMT11/2'), ('CAB1/0RW90GRE'), ('CAB12/2AC90150'), ('CAB12/3AC90150')) k(qpl_key)
LEFT JOIN PROCORRESP p ON p.NEWCLEMANU = k.qpl_key AND p.NEWDIV = 'LQE'
GROUP BY k.qpl_key
ORDER BY n_rows_lqe DESC, k.qpl_key;

PRINT '--- 5. Which modules read PROCORRESP / CLEPERS / TEMPUNI';
SELECT o.type, o.name,
       CASE WHEN m.definition LIKE '%PROCORRESP%' THEN 'PROCORRESP ' ELSE '' END +
       CASE WHEN m.definition LIKE '%CLEPERS%' THEN 'CLEPERS ' ELSE '' END +
       CASE WHEN m.definition LIKE '%TEMPUNI%' THEN 'TEMPUNI' ELSE '' END AS touches
FROM sys.sql_modules m
JOIN sys.objects o ON o.object_id = m.object_id
WHERE m.definition LIKE '%PROCORRESP%' OR m.definition LIKE '%CLEPERS%' OR m.definition LIKE '%TEMPUNI%'
ORDER BY o.name;

PRINT '--- 6. Columns of PriceUpdate_Products (what a distributor file can deliver)';
SELECT STRING_AGG(COLUMN_NAME + ':' + DATA_TYPE + ISNULL('(' + CAST(CHARACTER_MAXIMUM_LENGTH AS varchar) + ')', ''), ', ')
       WITHIN GROUP (ORDER BY ORDINAL_POSITION) AS columns_
FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = 'PriceUpdate_Products';

PRINT '--- 7. Unit codes accepted in COUUM / TEMPUM / QTEUM (Sys_Units)';
SELECT UnitId, CodeEN, CodeFR, Type, Package, ForProducts, ForAssemblies, BaseUnitCodeEN, BaseUnitRatio
FROM Sys_Units ORDER BY UnitId;

PRINT '--- 8. Indexes on the key columns';
SELECT t.name AS tbl, i.name AS idx,
       STRING_AGG(c.name, ',') WITHIN GROUP (ORDER BY ic.key_ordinal) AS cols
FROM sys.indexes i
JOIN sys.tables t ON t.object_id = i.object_id
JOIN sys.index_columns ic ON ic.object_id = i.object_id AND ic.index_id = i.index_id
JOIN sys.columns c ON c.object_id = ic.object_id AND c.column_id = ic.column_id
WHERE t.name IN ('PRODUITS', 'ENSEMBLE', 'ENSCOMPO', 'PriceUpdate_Products')
GROUP BY t.name, i.name
ORDER BY 1, 2;
