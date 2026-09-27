-- Removes the synthetic rows of worked_example.sql through the official delete procedures.
SET NOCOUNT ON;
DECLARE @SOU_ID  varchar(20) = 'ZZTEST-CALC';
DECLARE @TAX_ID  varchar(20) = 'ZZTX';
PRINT '=== 15. Cleanup through the official delete procedures ===';
EXEC dbo.up_DeleteSoumis_Full @DeleteSOU_ID=@SOU_ID, @DeleteHeader=1;
DECLARE @uid bigint;
DECLARE curd CURSOR LOCAL FOR SELECT UniqueId FROM TAXDEF WHERE TAX_ID=@TAX_ID;
OPEN curd; FETCH NEXT FROM curd INTO @uid; WHILE @@FETCH_STATUS=0 BEGIN EXEC dbo.up_TAXDEF_Delete @UniqueId=@uid; FETCH NEXT FROM curd INTO @uid; END; CLOSE curd; DEALLOCATE curd;
DECLARE curp CURSOR LOCAL FOR SELECT UniqueId FROM PRODUITS WHERE PRO_ID LIKE 'ZZP-%';
OPEN curp; FETCH NEXT FROM curp INTO @uid; WHILE @@FETCH_STATUS=0 BEGIN EXEC dbo.up_PRODUITS_Delete @UniqueId=@uid; FETCH NEXT FROM curp INTO @uid; END; CLOSE curp; DEALLOCATE curp;
DECLARE cure CURSOR LOCAL FOR SELECT UniqueId FROM ENSEMBLE WHERE ENS_ID LIKE 'ZZENS-%';
OPEN cure; FETCH NEXT FROM cure INTO @uid; WHILE @@FETCH_STATUS=0 BEGIN EXEC dbo.up_ENSEMBLE_Delete @UniqueId=@uid; FETCH NEXT FROM cure INTO @uid; END; CLOSE cure; DEALLOCATE cure;
DECLARE curc CURSOR LOCAL FOR SELECT UniqueId FROM ENSCOMPO WHERE ENS_ID LIKE 'ZZENS-%';
OPEN curc; FETCH NEXT FROM curc INTO @uid; WHILE @@FETCH_STATUS=0 BEGIN EXEC dbo.up_ENSCOMPO_Delete @UniqueId=@uid; FETCH NEXT FROM curc INTO @uid; END; CLOSE curc; DEALLOCATE curc;

PRINT '=== 16. Proof that nothing is left behind (all counts must be 0) ===';
SELECT (SELECT COUNT(*) FROM SOUMIS   WHERE SOU_ID=@SOU_ID)          AS soumis,
       (SELECT COUNT(*) FROM SOUREL   WHERE SOU_ID=@SOU_ID)          AS sourel,
       (SELECT COUNT(*) FROM SOUPRO   WHERE SOU_ID=@SOU_ID)          AS soupro,
       (SELECT COUNT(*) FROM SOUENS   WHERE SOU_ID=@SOU_ID)          AS souens,
       (SELECT COUNT(*) FROM SOUENSCO WHERE SOU_ID=@SOU_ID)          AS souensco,
       (SELECT COUNT(*) FROM SOUBLO   WHERE SOU_ID=@SOU_ID)          AS soublo,
       (SELECT COUNT(*) FROM SOUDIV   WHERE SOU_ID=@SOU_ID)          AS soudiv,
       (SELECT COUNT(*) FROM SOUAMD   WHERE SOU_ID=@SOU_ID)          AS souamd,
       (SELECT COUNT(*) FROM SOULOTS  WHERE SOU_ID=@SOU_ID)          AS soulots,
       (SELECT COUNT(*) FROM SOULOTSCO WHERE SOU_ID=@SOU_ID)         AS soulotsco,
       (SELECT COUNT(*) FROM TAXDEF   WHERE TAX_ID=@TAX_ID)          AS taxdef,
       (SELECT COUNT(*) FROM PRODUITS WHERE PRO_ID LIKE 'ZZP-%')     AS produits,
       (SELECT COUNT(*) FROM ENSEMBLE WHERE ENS_ID LIKE 'ZZENS-%')   AS ensemble,
       (SELECT COUNT(*) FROM ENSCOMPO WHERE ENS_ID LIKE 'ZZENS-%')   AS enscompo;
