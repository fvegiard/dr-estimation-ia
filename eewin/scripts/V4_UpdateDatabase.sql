-- 2013-10-22 EM : 
-- Corrige le problème de duplication de la compilation matériel lors du Copy/Paste d'un bloc/division d'une soumission à une autre

ALTER PROCEDURE [dbo].[up_CopySouBlocDiv] (
  @OldSouID     varchar(20), 
  @NewSouID     varchar(20),
  @OldBloc      varchar( 3),  
  @NewBloc      varchar( 3),
  @OldDivision  varchar( 3),  
  @NewDivision  varchar( 3)) AS

--Trouver le prochain ORDRE dans SOUREL
DECLARE @LastSouRelOrdre varchar(6)
SELECT  
  @LastSouRelOrdre = ISNULL(MAX(ORDRE), '000000') 
FROM 
  SOUREL 
WHERE 
  SOU_ID      = @NewSouID   AND 
  TYPERELEVE  = 'P'         AND 
  BLO_ID      = @NewBloc    AND 
  DIV_ID      = @NewDivision

DECLARE @UniqueId int
DECLARE CopySouRel CURSOR FOR
  SELECT 
    UniqueId 
  FROM 
    SOUREL 
  WHERE 
    SOU_ID      = @OldSouID   AND 
    TYPERELEVE  = 'P'         AND 
    BLO_ID      = @OldBloc    AND 
    DIV_ID      = @OldDivision 
  ORDER BY 
    ORDRE

OPEN CopySouRel

FETCH NEXT FROM CopySouRel INTO @UniqueId
WHILE @@FETCH_STATUS = 0
BEGIN
  --Augmenter le prochain ORDRE
  SELECT @LastSouRelOrdre = RIGHT('000000' + CAST(CAST(@LastSouRelOrdre as int) + 1000 as varchar), 6)

  --Copier ce SOUREL...
  INSERT INTO SOUREL (
    SOU_ID, BLO_ID, DIV_ID, TYPERELEVE, ORDRE,
    TYPEITEM, ITEM_ID, DESCR, QTE, SECTION, QTEUM,
    PROFIT, TYPETAXE, CODEIMPR, COUTANBRUT,
    TEMPSUNIT, TEMPSSEC, TEMPSUM, PROFITPLUS, PROFITMOIN)
  SELECT
    @NewSouID, @NewBloc, @NewDivision, TYPERELEVE, @LastSouRelOrdre,
    TYPEITEM, ITEM_ID, DESCR, QTE, SECTION, QTEUM,
    PROFIT, TYPETAXE, CODEIMPR, COUTANBRUT,
    TEMPSUNIT, TEMPSSEC, TEMPSUM, PROFITPLUS, PROFITMOIN
  FROM
    SOUREL
  WHERE
    UniqueId = @UniqueId

   -- This is executed as long as the previous fetch succeeds.
   FETCH NEXT FROM CopySouRel INTO @UniqueId
END

CLOSE CopySouRel
DEALLOCATE CopySouRel

--Liste des ensembles à copier
IF OBJECT_ID('tempdb..#AssembliesToCopy') IS NOT NULL
  DROP TABLE #AssembliesToCopy

SELECT
  ITEM_ID AS ENS_ID
INTO
  #AssembliesToCopy
FROM
  SOUREL
WHERE
  TYPEITEM  = 'A'           AND 
  SOU_ID    = @OldSouID     AND 
  BLO_ID    = @OldBloc      AND 
  DIV_ID    = @OldDivision  AND 
  ITEM_ID NOT IN (SELECT ENS_ID FROM SOUENS WHERE SOU_ID = @NewSouID)
GROUP BY
  ITEM_ID

--Copier les SOUENS
INSERT INTO SOUENS (
  SOU_ID, ENS_ID, [DESC],
  QTETOT, QTETOTSECT, CALCTIMSTP, COUUM,
  TEMPUNI, TEMPSEC, TEMPUM,
  DATECREE, OLDESTPROD, CLEPERS, PROFIT)
SELECT DISTINCT
  @NewSouID, ENS_ID, [DESC],
  QTETOT, QTETOTSECT, CALCTIMSTP, COUUM,
  TEMPUNI, TEMPSEC, TEMPUM,
  DATECREE, OLDESTPROD, CLEPERS, PROFIT
FROM
  SOUENS
WHERE
  ENS_ID IN (SELECT ENS_ID FROM #AssembliesToCopy) AND
  SOU_ID = @OldSouID

--Copier les SOUENSCO
INSERT INTO SOUENSCO (
  SOU_ID, ENS_ID, PRO_ID,
  ORDRE, QTE, QTEUM,
  TYPRATIO, DIV, DIVUM)
SELECT
  @NewSouID, ENS_ID, PRO_ID,
  ORDRE, QTE, QTEUM,
  TYPRATIO, DIV, DIVUM
FROM
  SOUENSCO
WHERE
  ENS_ID IN (SELECT ENS_ID FROM #AssembliesToCopy) AND
  SOU_ID = @OldSouID

--Liste des lots à copier
IF OBJECT_ID('tempdb..#LotsToCopy') IS NOT NULL
  DROP TABLE #LotsToCopy

SELECT
  ITEM_ID AS LOTS_ID
INTO
  #LotsToCopy
FROM
  SOUREL
WHERE
  TYPEITEM  = 'L'           AND
  SOU_ID    = @OldSouID     AND
  BLO_ID    = @OldBloc      AND
  DIV_ID    = @OldDivision  AND
  ITEM_ID NOT IN (SELECT LOTS_ID FROM SOULOTS WHERE SOU_ID = @NewSouID)
GROUP BY
  ITEM_ID

--Copier les SOULOTS
INSERT INTO SOULOTS (
  SOU_ID, LOTS_ID, [DESC],
  QTETOT, QTETOTSECT, CALCTIMSTP, COUUM,
  TEMPUNI, TEMPUM, DATECREE, OLDESTPROD,
  CLEPERS, PROFIT, COUTANTSEL,
  COUTANT1, COUTANT2, COUTANT3, COUTANT4)
SELECT DISTINCT
  @NewSouID, LOTS_ID, [DESC],
  QTETOT, QTETOTSECT, CALCTIMSTP, COUUM,
  TEMPUNI, TEMPUM, DATECREE, OLDESTPROD,
  CLEPERS, PROFIT, COUTANTSEL,
  COUTANT1, COUTANT2, COUTANT3, COUTANT4
FROM
  SOULOTS
WHERE
  LOTS_ID IN (SELECT LOTS_ID FROM #LotsToCopy) AND
  SOU_ID = @OldSouID

--Copier les SOULOTSCO
INSERT INTO SOULOTSCO (
  SOU_ID, LOTS_ID, PRO_ID, ORDRE, QTE, QTEUM)
SELECT
  @NewSouID, LOTS_ID, PRO_ID, ORDRE, QTE, QTEUM
FROM
  SOULOTSCO
WHERE
  LOTS_ID IN (SELECT LOTS_ID FROM #LotsToCopy) AND
  SOU_ID = @OldSouID

--Liste des produits à copier
IF OBJECT_ID('tempdb..#ProductsToCopy') IS NOT NULL
  DROP TABLE #ProductsToCopy

--Produits à copier...
SELECT DISTINCT
  ITEM_ID AS PRO_ID
INTO
  #ProductsToCopy
FROM
  SOUREL
WHERE
  TYPEITEM NOT IN ('A', 'L', 'T') AND
  SOU_ID  = @OldSouID             AND
  BLO_ID  = @OldBloc              AND
  DIV_ID  = @OldDivision          AND
  ITEM_ID NOT IN (SELECT PRO_ID FROM SOUPRO WHERE SOU_ID = @NewSouID)

--Produits à copier (ensembles)
INSERT INTO 
  #ProductsToCopy (PRO_ID)
SELECT
  PRO_ID
FROM 
  SOUENSCO
WHERE 
  ENS_ID IN (SELECT ENS_ID FROM #AssembliesToCopy) AND 
  PRO_ID NOT IN (SELECT PRO_ID FROM SOUPRO WHERE SOU_ID = @NewSouID) AND
  SOU_ID = @OldSouID
  
--Produits à copier (lots)
INSERT INTO 
  #ProductsToCopy (PRO_ID)
SELECT 
  PRO_ID
FROM 
  SOULOTSCO
WHERE 
  LOTS_ID IN (SELECT LOTS_ID FROM #LotsToCopy) AND 
  PRO_ID NOT IN (SELECT PRO_ID FROM SOUPRO WHERE SOU_ID = @NewSouID)
  
INSERT INTO SOUPRO (
  SOU_ID, PRO_ID, CLEMANU, CLEDIST, CLEPERS, [DESC],
  QTEENS, QTELOT, QTEOTH, CALCTIMSTP, COUBRUTUNI, COUUM, QPP, COUESC,
  PROMCOUNET, TEMPUNI, TEMPUM, MULCOM, CODEIMPR, CODEFOUR, CODECAT,
  DATECOUT, QTECOM, QTEACOM)
SELECT
  @NewSouID, PRO_ID, CLEMANU, CLEDIST, CLEPERS, [DESC],
  QTEENS, QTELOT, QTEOTH, CALCTIMSTP, COUBRUTUNI, COUUM, QPP, COUESC,
  PROMCOUNET, TEMPUNI, TEMPUM, MULCOM, CODEIMPR, CODEFOUR, CODECAT,
  DATECOUT, QTECOM, QTEACOM
FROM
  SOUPRO
WHERE
  SOU_ID  = @OldSouID AND
  PRO_ID IN (SELECT PRO_ID FROM #ProductsToCopy) AND
  SOU_ID = @OldSouID

DROP TABLE #AssembliesToCopy
DROP TABLE #LotsToCopy
DROP TABLE #ProductsToCopy

GO

-- 2013-10-22 EM : 
-- Corrige le problème de duplication de la compilation matériel lors du Copy/Paste d'un bloc/division d'une facture à une autre

ALTER PROCEDURE [dbo].[up_CopySouBlocDiv_FAC] (
  @OldSouID     varchar(20), 
  @NewSouID     varchar(20),
  @OldBloc      varchar(3),  
  @NewBloc      varchar(3),
  @OldDivision  varchar(3),  
  @NewDivision  varchar(3) ) AS

--Trouver le prochain ORDRE dans FACREL
DECLARE @LastSouRelOrdre varchar(6)
SELECT  
  @LastSouRelOrdre = ISNULL(MAX(ORDRE), '000000')
FROM 
  FACREL 
WHERE 
  SOU_ID      = @NewSouID   AND 
  TYPERELEVE  = 'P'         AND 
  BLO_ID      = @NewBloc    AND 
  DIV_ID      = @NewDivision

DECLARE @UniqueId int
DECLARE CopySouRel CURSOR FOR
  SELECT 
    UniqueId 
  FROM 
    FACREL 
  WHERE 
    SOU_ID      = @OldSouID     AND
    TYPERELEVE  = 'P'           AND
    BLO_ID      = @OldBloc      AND
    DIV_ID      = @OldDivision
  ORDER BY 
    ORDRE

OPEN CopySouRel

FETCH NEXT FROM CopySouRel INTO @UniqueId
WHILE @@FETCH_STATUS = 0
BEGIN
  --Augmenter le prochain ORDRE
  SELECT @LastSouRelOrdre = RIGHT('000000' + CAST(CAST(@LastSouRelOrdre as int) + 1000 as varchar), 6)

  --Copier ce FACREL...
  INSERT INTO FACREL (
    SOU_ID, BLO_ID, DIV_ID, TYPERELEVE, ORDRE,
    TYPEITEM, ITEM_ID, DESCR, QTE, SECTION, QTEUM,
    PROFIT, TYPETAXE, CODEIMPR, COUTANBRUT,
    TEMPSUNIT, TEMPSSEC, TEMPSUM, PROFITPLUS, PROFITMOIN)
  SELECT
    @NewSouID, @NewBloc, @NewDivision, TYPERELEVE, @LastSouRelOrdre,
    TYPEITEM, ITEM_ID, DESCR, QTE, SECTION, QTEUM,
    PROFIT, TYPETAXE, CODEIMPR, COUTANBRUT,
    TEMPSUNIT, TEMPSSEC, TEMPSUM, PROFITPLUS, PROFITMOIN
  FROM
    FACREL
  WHERE
    UniqueId = @UniqueId

   -- This is executed as long as the previous fetch succeeds.
   FETCH NEXT FROM CopySouRel INTO @UniqueId
END

CLOSE CopySouRel
DEALLOCATE CopySouRel

--Liste des ensembles à copier
IF OBJECT_ID('tempdb..#AssembliesToCopy') IS NOT NULL
  DROP TABLE #AssembliesToCopy

SELECT
  ITEM_ID AS ENS_ID
INTO
  #AssembliesToCopy
FROM
  FACREL
WHERE
  TYPEITEM  = 'A'           AND
  SOU_ID    = @OldSouID     AND
  BLO_ID    = @OldBloc      AND
  DIV_ID    = @OldDivision  AND
  ITEM_ID NOT IN (SELECT ENS_ID FROM FACENS WHERE SOU_ID = @NewSouID)
GROUP BY
  ITEM_ID

--Copier les FACENS
INSERT INTO FACENS (
  SOU_ID, ENS_ID, [DESC],
  QTETOT, QTETOTSECT, CALCTIMSTP, COUUM,
  TEMPUNI, TEMPSEC, TEMPUM,
  DATECREE, OLDESTPROD, CLEPERS, PROFIT)
SELECT DISTINCT
  @NewSouID, ENS_ID, [DESC],
  QTETOT, QTETOTSECT, CALCTIMSTP, COUUM,
  TEMPUNI, TEMPSEC, TEMPUM,
  DATECREE, OLDESTPROD, CLEPERS, PROFIT
FROM
  FACENS
WHERE
  ENS_ID IN (SELECT ENS_ID FROM #AssembliesToCopy) AND
  SOU_ID = @OldSouID

--Copier les FACENSCO
INSERT INTO FACENSCO (
  SOU_ID, ENS_ID, PRO_ID,
  ORDRE, QTE, QTEUM,
  TYPRATIO, DIV, DIVUM)
SELECT
  @NewSouID, ENS_ID, PRO_ID,
  ORDRE, QTE, QTEUM,
  TYPRATIO, DIV, DIVUM
FROM
  FACENSCO
WHERE
  ENS_ID IN (SELECT ENS_ID FROM #AssembliesToCopy) AND
  SOU_ID = @OldSouID

--Liste des lots à copier
IF OBJECT_ID('tempdb..#LotsToCopy') IS NOT NULL
  DROP TABLE #LotsToCopy

SELECT
  ITEM_ID AS LOTS_ID
INTO
  #LotsToCopy
FROM
  FACREL
WHERE
  TYPEITEM  = 'L'           AND
  SOU_ID    = @OldSouID     AND
  BLO_ID    = @OldBloc      AND
  DIV_ID    = @OldDivision  AND
  ITEM_ID NOT IN (SELECT LOTS_ID FROM FACLOTS WHERE SOU_ID = @NewSouID)
GROUP BY
  ITEM_ID

--Copier les FACLOTS
INSERT INTO FACLOTS (
  SOU_ID, LOTS_ID, [DESC],
  QTETOT, QTETOTSECT, CALCTIMSTP, COUUM,
  TEMPUNI, TEMPUM, DATECREE, OLDESTPROD,
  CLEPERS, PROFIT, COUTANTSEL,
  COUTANT1, COUTANT2, COUTANT3, COUTANT4)
SELECT DISTINCT
  @NewSouID, LOTS_ID, [DESC],
  QTETOT, QTETOTSECT, CALCTIMSTP, COUUM,
  TEMPUNI, TEMPUM, DATECREE, OLDESTPROD,
  CLEPERS, PROFIT, COUTANTSEL,
  COUTANT1, COUTANT2, COUTANT3, COUTANT4
FROM
  FACLOTS
WHERE
  LOTS_ID IN (SELECT LOTS_ID FROM #LotsToCopy) AND
  SOU_ID = @OldSouID

--Copier les FACLOTSCO
INSERT INTO FACLOTSCO (
  SOU_ID, LOTS_ID, PRO_ID, ORDRE, QTE, QTEUM)
SELECT
  @NewSouID, LOTS_ID, PRO_ID, ORDRE, QTE, QTEUM
FROM
  FACLOTSCO
WHERE
  LOTS_ID IN (SELECT LOTS_ID FROM #LotsToCopy) AND
  SOU_ID = @OldSouID

--Liste des produits à copier
IF OBJECT_ID('tempdb..#ProductsToCopy') IS NOT NULL
  DROP TABLE #ProductsToCopy

--Produits à copier...
SELECT DISTINCT
  ITEM_ID AS PRO_ID
INTO
  #ProductsToCopy
FROM
  FACREL
WHERE
  TYPEITEM NOT IN ('A', 'L', 'T') AND
  SOU_ID  = @OldSouID             AND
  BLO_ID  = @OldBloc              AND
  DIV_ID  = @OldDivision          AND
  ITEM_ID NOT IN (SELECT PRO_ID FROM FACPRO WHERE SOU_ID = @NewSouID)

--Produits à copier (ensembles)
INSERT INTO 
  #ProductsToCopy (PRO_ID)
SELECT 
  PRO_ID
FROM 
  FACENSCO
WHERE 
  ENS_ID IN (SELECT ENS_ID FROM #AssembliesToCopy) AND 
  PRO_ID NOT IN (SELECT PRO_ID FROM FACPRO WHERE SOU_ID = @NewSouID) AND
  SOU_ID = @OldSouID

--Produits à copier (lots)
INSERT INTO 
  #ProductsToCopy (PRO_ID)
SELECT 
  PRO_ID
FROM 
  FACLOTSCO
WHERE 
  LOTS_ID IN (SELECT LOTS_ID FROM #LotsToCopy) AND 
  PRO_ID NOT IN (SELECT PRO_ID FROM FACPRO WHERE SOU_ID = @NewSouID)

INSERT INTO FACPRO (
  SOU_ID, PRO_ID, CLEMANU, CLEDIST, CLEPERS, [DESC],
  QTEENS, QTELOT, QTEOTH, CALCTIMSTP, COUBRUTUNI, COUUM, QPP, COUESC,
  PROMCOUNET, TEMPUNI, TEMPUM, MULCOM, CODEIMPR, CODEFOUR, CODECAT,
  DATECOUT, QTECOM, QTEACOM)
SELECT
  @NewSouID, PRO_ID, CLEMANU, CLEDIST, CLEPERS, [DESC],
  QTEENS, QTELOT, QTEOTH, CALCTIMSTP, COUBRUTUNI, COUUM, QPP, COUESC,
  PROMCOUNET, TEMPUNI, TEMPUM, MULCOM, CODEIMPR, CODEFOUR, CODECAT,
  DATECOUT, QTECOM, QTEACOM
FROM
  FACPRO
WHERE
  SOU_ID  = @OldSouID AND
  PRO_ID IN (SELECT PRO_ID FROM #ProductsToCopy) AND
  SOU_ID = @OldSouID

DROP TABLE #AssembliesToCopy
DROP TABLE #LotsToCopy
DROP TABLE #ProductsToCopy

GO
