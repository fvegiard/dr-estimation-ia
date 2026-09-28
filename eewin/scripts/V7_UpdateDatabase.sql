  -- 2014-11-21 EE-222 EMadore 
  -- Script de MaJ pour prix net rexel

  -- New field - Produits.DATECOUNET
IF NOT EXISTS (
  SELECT 
    TOP 1 *
  FROM 
    INFORMATION_SCHEMA.COLUMNS
  WHERE 
        [TABLE_NAME]  = 'PRODUITS'
    AND [COLUMN_NAME] = 'DATECOUNET' )
BEGIN
  ALTER TABLE
    PRODUITS
  ADD
    DATECOUNET DATETIME
END
GO

  -- New field - Produits.RESCOUNET
IF NOT EXISTS (
  SELECT 
    TOP 1 *
  FROM 
    INFORMATION_SCHEMA.COLUMNS
  WHERE 
        [TABLE_NAME]  = 'PRODUITS'
    AND [COLUMN_NAME] = 'RESCOUNET' )
BEGIN
  ALTER TABLE
    PRODUITS
  ADD
    RESCOUNET INT
END
GO

  -- Update precodure pour support des nouveaux champs
ALTER PROCEDURE [dbo].[up_PRODUITS_Update] (
  @UniqueId bigint,
  @PRO_ID varchar(20),
  @CLEMANU varchar(20),
  @CLEPERS varchar(20),
  @CLEDIST varchar(20),
  @CODEUPC varchar(12),
  @CODECAT varchar(3),
  @DESCDIST varchar(60),
  @DESC varchar(60),
  @COUBRUTUNI float,
  @COUUM varchar(2),
  @QPP float,
  @COUESC float,
  @PROMCOUNET float,
  @PROFIT float,
  @MULCOM float,
  @TEMPUNI float,
  @TEMPUM varchar(2),
  @CODEFOUR varchar(2),
  @NOUVEAU varchar(1),
  @DNR varchar(1),
  @DATECOUT datetime,
  @DATECOUNET datetime,   -- V7 EE-222 - Prix net Rexel
  @RESCOUNET int,         -- V7 EE-222 - Prix net Rexel
  @DATECREE datetime,
  @PATHPICT varchar(60),
  @PATHSPEC varchar(60),
  @IMAGE varchar(1),
  @USER1 varchar(20),
  @USER2 varchar(20)
) AS

IF @UniqueId IS NULL
BEGIN
  --Insert new data into table
  INSERT INTO PRODUITS (
    [PRO_ID],
    [CLEMANU],
    [CLEPERS],
    [CLEDIST],
    [CODEUPC],
    [CODECAT],
    [DESCDIST],
    [DESC],
    [COUBRUTUNI],
    [COUUM],
    [QPP],
    [COUESC],
    [PROMCOUNET],
    [PROFIT],
    [MULCOM],
    [TEMPUNI],
    [TEMPUM],
    [CODEFOUR],
    [NOUVEAU],
    [DNR],
    [DATECOUT],
    [DATECOUNET],   -- V7 EE-222 - Prix net Rexel
    [RESCOUNET],    -- V7 EE-222 - Prix net Rexel
    [DATECREE],
    [PATHPICT],
    [PATHSPEC],
    [IMAGE],
    [USER1],
    [USER2],
    SysDate)
  VALUES (
    @PRO_ID,
    @CLEMANU,
    @CLEPERS,
    @CLEDIST,
    @CODEUPC,
    @CODECAT,
    @DESCDIST,
    @DESC,
    @COUBRUTUNI,
    @COUUM,
    @QPP,
    @COUESC,
    @PROMCOUNET,
    @PROFIT,
    @MULCOM,
    @TEMPUNI,
    @TEMPUM,
    @CODEFOUR,
    @NOUVEAU,
    @DNR,
    @DATECOUT,
    @DATECOUNET,  -- V7 EE-222 - Prix net Rexel
    @RESCOUNET,   -- V7 EE-222 - Prix net Rexel
    @DATECREE,
    @PATHPICT,
    @PATHSPEC,
    @IMAGE,
    @USER1,
    @USER2,
    GETDATE())

  --Return new ID
  RETURN @@IDENTITY
END ELSE
BEGIN
  --Update data into table
  UPDATE
    PRODUITS
  SET
    [PRO_ID] = @PRO_ID,
    [CLEMANU] = @CLEMANU,
    [CLEPERS] = @CLEPERS,
    [CLEDIST] = @CLEDIST,
    [CODEUPC] = @CODEUPC,
    [CODECAT] = @CODECAT,
    [DESCDIST] = @DESCDIST,
    [DESC] = @DESC,
    [COUBRUTUNI] = @COUBRUTUNI,
    [COUUM] = @COUUM,
    [QPP] = @QPP,
    [COUESC] = @COUESC,
    [PROMCOUNET] = @PROMCOUNET,
    [PROFIT] = @PROFIT,
    [MULCOM] = @MULCOM,
    [TEMPUNI] = @TEMPUNI,
    [TEMPUM] = @TEMPUM,
    [CODEFOUR] = @CODEFOUR,
    [NOUVEAU] = @NOUVEAU,
    [DNR] = @DNR,
    [DATECOUT] = @DATECOUT,
    [DATECOUNET] = @DATECOUNET,   -- V7 EE-222 - Prix net Rexel
    [RESCOUNET] = @RESCOUNET,     -- V7 EE-222 - Prix net Rexel
    [DATECREE] = @DATECREE,
    [PATHPICT] = @PATHPICT,
    [PATHSPEC] = @PATHSPEC,
    [IMAGE] = @IMAGE,
    [USER1] = @USER1,
    [USER2] = @USER2,
    SysDate = GETDATE()
  WHERE
    UniqueId = @UniqueId

  --Return updated ID
  RETURN @UniqueId
END

GO

  -- New field - SouPro.DATECOUNET
IF NOT EXISTS (
  SELECT 
    TOP 1 *
  FROM 
    INFORMATION_SCHEMA.COLUMNS
  WHERE 
        [TABLE_NAME]  = 'SOUPRO'
    AND [COLUMN_NAME] = 'DATECOUNET' )
BEGIN
  ALTER TABLE
    SOUPRO
  ADD
    DATECOUNET DATETIME
END
GO

  -- New field - SouPro.RESCOUNET
IF NOT EXISTS (
  SELECT 
    TOP 1 *
  FROM 
    INFORMATION_SCHEMA.COLUMNS
  WHERE 
        [TABLE_NAME]  = 'SOUPRO'
    AND [COLUMN_NAME] = 'RESCOUNET' )
BEGIN
  ALTER TABLE
    SOUPRO
  ADD
    RESCOUNET INT
END
GO

ALTER PROCEDURE [dbo].[up_SOUPRO_Update] (
  @UniqueId bigint,
  @SOU_ID varchar(20),
  @PRO_ID varchar(20),
  @CLEMANU varchar(20),
  @CLEDIST varchar(20),
  @CLEPERS varchar(20),
  @DESC varchar(60),
  @QTEENS float,
  @QTELOT float,
  @QTEOTH float,
  @CALCTIMSTP varchar(14),
  @COUBRUTUNI float,
  @COUUM varchar(2),
  @QPP float,
  @COUESC float,
  @PROMCOUNET float,
  @TEMPUNI float,
  @TEMPUM varchar(2),
  @MULCOM float,
  @CODEIMPR varchar(20),
  @CODEFOUR varchar(2),
  @CODECAT varchar(3),
  @DATECOUT datetime,
  @DATECOUNET datetime,   -- V7 EE-222 - Prix net Rexel
  @RESCOUNET int,         -- V7 EE-222 - Prix net Rexel
  @QTECOM float,
  @QTEACOM float
) AS

IF @UniqueId IS NULL
BEGIN
  --Insert new data into table
  INSERT INTO SOUPRO (
    [SOU_ID],
    [PRO_ID],
    [CLEMANU],
    [CLEDIST],
    [CLEPERS],
    [DESC],
    [QTEENS],
    [QTELOT],
    [QTEOTH],
    [CALCTIMSTP],
    [COUBRUTUNI],
    [COUUM],
    [QPP],
    [COUESC],
    [PROMCOUNET],
    [TEMPUNI],
    [TEMPUM],
    [MULCOM],
    [CODEIMPR],
    [CODEFOUR],
    [CODECAT],
    [DATECOUT],
    [DATECOUNET],   -- V7 EE-222 - Prix net Rexel
    [RESCOUNET],    -- V7 EE-222 - Prix net Rexel
    [QTECOM],
    [QTEACOM],
    SysDate)
  VALUES (
    @SOU_ID,
    @PRO_ID,
    @CLEMANU,
    @CLEDIST,
    @CLEPERS,
    @DESC,
    @QTEENS,
    @QTELOT,
    @QTEOTH,
    @CALCTIMSTP,
    @COUBRUTUNI,
    @COUUM,
    @QPP,
    @COUESC,
    @PROMCOUNET,
    @TEMPUNI,
    @TEMPUM,
    @MULCOM,
    @CODEIMPR,
    @CODEFOUR,
    @CODECAT,
    @DATECOUT,
    @DATECOUNET,  -- V7 EE-222 - Prix net Rexel
    @RESCOUNET,   -- V7 EE-222 - Prix net Rexel
    @QTECOM,
    @QTEACOM,
    GETDATE())

  --Return new ID
  RETURN @@IDENTITY
END ELSE
BEGIN
  --Update data into table
  UPDATE
    SOUPRO
  SET
    [SOU_ID] = @SOU_ID,
    [PRO_ID] = @PRO_ID,
    [CLEMANU] = @CLEMANU,
    [CLEDIST] = @CLEDIST,
    [CLEPERS] = @CLEPERS,
    [DESC] = @DESC,
    [QTEENS] = @QTEENS,
    [QTELOT] = @QTELOT,
    [QTEOTH] = @QTEOTH,
    [CALCTIMSTP] = @CALCTIMSTP,
    [COUBRUTUNI] = @COUBRUTUNI,
    [COUUM] = @COUUM,
    [QPP] = @QPP,
    [COUESC] = @COUESC,
    [PROMCOUNET] = @PROMCOUNET,
    [TEMPUNI] = @TEMPUNI,
    [TEMPUM] = @TEMPUM,
    [MULCOM] = @MULCOM,
    [CODEIMPR] = @CODEIMPR,
    [CODEFOUR] = @CODEFOUR,
    [CODECAT] = @CODECAT,
    [DATECOUT] = @DATECOUT,
    [DATECOUNET] = @DATECOUNET,   -- V7 EE-222 - Prix net Rexel
    [RESCOUNET] = @RESCOUNET,     -- V7 EE-222 - Prix net Rexel
    [QTECOM] = @QTECOM,
    [QTEACOM] = @QTEACOM,
    SysDate = GETDATE()
  WHERE
    UniqueId = @UniqueId

  --Return updated ID
  RETURN @UniqueId
END
GO

  -- New field - FACPRO.DATECOUNET
IF NOT EXISTS (
  SELECT 
    TOP 1 *
  FROM 
    INFORMATION_SCHEMA.COLUMNS
  WHERE 
        [TABLE_NAME]  = 'FACPRO'
    AND [COLUMN_NAME] = 'DATECOUNET' )
BEGIN
  ALTER TABLE
    FACPRO
  ADD
    DATECOUNET DATETIME
END
GO

  -- New field - FACPRO.RESCOUNET
IF NOT EXISTS (
  SELECT 
    TOP 1 *
  FROM 
    INFORMATION_SCHEMA.COLUMNS
  WHERE 
        [TABLE_NAME]  = 'FACPRO'
    AND [COLUMN_NAME] = 'RESCOUNET' )
BEGIN
  ALTER TABLE
    FACPRO
  ADD
    RESCOUNET INT
END
GO

ALTER PROCEDURE [dbo].[up_FACPRO_Update] (
  @UniqueId bigint,
  @SOU_ID varchar(20),
  @PRO_ID varchar(20),
  @CLEMANU varchar(20),
  @CLEDIST varchar(20),
  @CLEPERS varchar(20),
  @DESC varchar(60),
  @QTEENS float,
  @QTELOT float,
  @QTEOTH float,
  @CALCTIMSTP varchar(14),
  @COUBRUTUNI float,
  @COUUM varchar(2),
  @QPP float,
  @COUESC float,
  @PROMCOUNET float,
  @TEMPUNI float,
  @TEMPUM varchar(2),
  @MULCOM float,
  @CODEIMPR varchar(20),
  @CODEFOUR varchar(2),
  @CODECAT varchar(3),
  @DATECOUT datetime,
  @DATECOUNET datetime,   -- V7 EE-222 - Prix net Rexel
  @RESCOUNET int,         -- V7 EE-222 - Prix net Rexel
  @QTECOM float,
  @QTEACOM float
) AS

IF @UniqueId IS NULL
BEGIN
  --Insert new data into table
  INSERT INTO FACPRO (
    [SOU_ID],
    [PRO_ID],
    [CLEMANU],
    [CLEDIST],
    [CLEPERS],
    [DESC],
    [QTEENS],
    [QTELOT],
    [QTEOTH],
    [CALCTIMSTP],
    [COUBRUTUNI],
    [COUUM],
    [QPP],
    [COUESC],
    [PROMCOUNET],
    [TEMPUNI],
    [TEMPUM],
    [MULCOM],
    [CODEIMPR],
    [CODEFOUR],
    [CODECAT],
    [DATECOUT],
    [DATECOUNET],   -- V7 EE-222 - Prix net Rexel
    [RESCOUNET],    -- V7 EE-222 - Prix net Rexel
    [QTECOM],
    [QTEACOM],
    SysDate)
  VALUES (
    @SOU_ID,
    @PRO_ID,
    @CLEMANU,
    @CLEDIST,
    @CLEPERS,
    @DESC,
    @QTEENS,
    @QTELOT,
    @QTEOTH,
    @CALCTIMSTP,
    @COUBRUTUNI,
    @COUUM,
    @QPP,
    @COUESC,
    @PROMCOUNET,
    @TEMPUNI,
    @TEMPUM,
    @MULCOM,
    @CODEIMPR,
    @CODEFOUR,
    @CODECAT,
    @DATECOUT,
    @DATECOUNET,  -- V7 EE-222 - Prix net Rexel
    @RESCOUNET,   -- V7 EE-222 - Prix net Rexel
    @QTECOM,
    @QTEACOM,
    GETDATE())

  --Return new ID
  RETURN @@IDENTITY
END ELSE
BEGIN
  --Update data into table
  UPDATE
    FACPRO
  SET
    [SOU_ID] = @SOU_ID,
    [PRO_ID] = @PRO_ID,
    [CLEMANU] = @CLEMANU,
    [CLEDIST] = @CLEDIST,
    [CLEPERS] = @CLEPERS,
    [DESC] = @DESC,
    [QTEENS] = @QTEENS,
    [QTELOT] = @QTELOT,
    [QTEOTH] = @QTEOTH,
    [CALCTIMSTP] = @CALCTIMSTP,
    [COUBRUTUNI] = @COUBRUTUNI,
    [COUUM] = @COUUM,
    [QPP] = @QPP,
    [COUESC] = @COUESC,
    [PROMCOUNET] = @PROMCOUNET,
    [TEMPUNI] = @TEMPUNI,
    [TEMPUM] = @TEMPUM,
    [MULCOM] = @MULCOM,
    [CODEIMPR] = @CODEIMPR,
    [CODEFOUR] = @CODEFOUR,
    [CODECAT] = @CODECAT,
    [DATECOUT] = @DATECOUT,
    [DATECOUNET] = @DATECOUNET,   -- V7 EE-222 - Prix net Rexel
    [RESCOUNET] = @RESCOUNET,     -- V7 EE-222 - Prix net Rexel
    [QTECOM] = @QTECOM,
    [QTEACOM] = @QTEACOM,
    SysDate = GETDATE()
  WHERE
    UniqueId = @UniqueId

  --Return updated ID
  RETURN @UniqueId
END
GO

ALTER PROCEDURE [dbo].[up_PriceUpdate_UpdateProducts] AS

-- 2014-11-25 EE-222 EMadore -
-- Voir si possible mettre les fonction de division en SQL. Eviterai le check avec les PRO_ID et les division manuelles

-- Insérer tous les produits inexistants
INSERT INTO PRODUITS (
  PRO_ID, 
  TEMPUM, 
  DATECREE)
SELECT
  PriceUpdate_Products.PRO_ID, 
  PriceUpdate_Products.TEMPUM,
  getdate()
FROM
  PriceUpdate_Products 
  LEFT JOIN PRODUITS 
  ON PriceUpdate_Products.PRO_ID = PRODUITS.PRO_ID
WHERE
  -- Produits qui n'existent pas déja
  PRODUITS.PRO_ID IS NULL


-- Updater tous les produits
-- 2014-11-25 EE-222 EMadore -
-- Prise en comptes des prix net Rexel
UPDATE
  PRODUITS
SET 
  --Si la description personnelle n'a jamais été modifiée alors on peut se permettre de la mettre à jour
  PRODUITS.[DESC] = CASE WHEN PRODUITS.[DESC] IS NULL OR PRODUITS.[DESC] = '' OR PRODUITS.[DESC] = PRODUITS.DESCDIST THEN PriceUpdate_Products.[DESC] ELSE PRODUITS.[DESC] END,
  --Si la catégorie du produit est une catégorie système, alors on peut l'écraser sans souci 
  PRODUITS.CODECAT = CASE WHEN PRODUITS.CODECAT IS NULL OR PRODUITS.CODECAT = '' OR LEFT(PRODUITS.CODECAT, 1) = '+' OR LEFT(PRODUITS.CODECAT, 1) = '#' THEN PriceUpdate_Products.CODECAT ELSE PRODUITS.CODECAT END,
  --Les autres champs sont communs aux inserts et aux updates
  PRODUITS.CLEMANU = PriceUpdate_Products.CLEMANU,
  PRODUITS.CLEDIST = PriceUpdate_Products.CLEDIST,
  PRODUITS.DESCDIST = PriceUpdate_Products.DESCDIST,
  PRODUITS.COUUM = PriceUpdate_Products.COUUM,
  PRODUITS.QPP = PriceUpdate_Products.QPP,
  PRODUITS.MULCOM = PriceUpdate_Products.MULCOM,
  PRODUITS.CODEFOUR = CASE WHEN LEFT(PRODUITS.PRO_ID, 1) = 'N' THEN 'NE' ELSE 'WE' END,
  PRODUITS.COUBRUTUNI = PriceUpdate_Products.COUBRUTUNI,
  PRODUITS.COUESC     = CASE WHEN LEFT(PRODUITS.PRO_ID, 3) IN ('NWE', 'NOE', 'NQE', 'NME', 'WAE', 'WME', 'WOE', 'WQE') THEN PRODUITS.COUESC ELSE PriceUpdate_Products.COUESC END,     -- Prix net pas dans le catlogue pour Rexel
  PRODUITS.PROMCOUNET = CASE WHEN LEFT(PRODUITS.PRO_ID, 3) IN ('NWE', 'NOE', 'NQE', 'NME', 'WAE', 'WME', 'WOE', 'WQE') THEN PRODUITS.PROMCOUNET ELSE PriceUpdate_Products.PROMCOUNET END, -- Prix net pas dans le catlogue pour Rexel
  PRODUITS.DNR = 'N',
  PRODUITS.NOUVEAU = PriceUpdate_Products.NOUVEAU,
  PRODUITS.DATECOUT = PriceUpdate_Products.DATECOUT,
  PRODUITS.DATECOUNET = CASE WHEN LEFT(PRODUITS.PRO_ID, 3) IN ('NWE', 'NOE', 'NQE', 'NME', 'WAE', 'WME', 'WOE', 'WQE') THEN PRODUITS.DATECOUNET ELSE PriceUpdate_Products.DATECOUT END  -- Date Prix net = Date cout brut pour Wosleley (validé ici comme pas Rexel)
FROM
  PRODUITS 
  INNER JOIN PriceUpdate_Products
  ON PRODUITS.PRO_ID = PriceUpdate_Products.PRO_ID


--Vider la table temp maintenant qu'on a fini  
--TRUNCATE TABLE PriceUpdate_Products

GO
