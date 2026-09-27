-- New field - PRODUITS.CODEUPCDIS  -- START
  
IF NOT EXISTS (
  SELECT 
    TOP 1 *
  FROM 
    INFORMATION_SCHEMA.COLUMNS
  WHERE 
        [TABLE_NAME]  = 'PRODUITS'
    AND [COLUMN_NAME] = 'CODEUPCDIS' )
BEGIN
  ALTER TABLE
    PRODUITS
  ADD
    CODEUPCDIS VARCHAR(12)
END
GO

-- New field - PRODUITS.CODEUPCDIS  -- END


-- INDEX -- NEW -- CODEUPC -- START --

IF EXISTS 
  (
    SELECT * 
    FROM Sys.Indexes 
    WHERE 
    Name='IDX_CODEUPC' AND 
    object_id = OBJECT_ID('Produits') 
  )
  DROP INDEX [IDX_CODEUPC] ON [dbo].[PRODUITS]
GO

CREATE NONCLUSTERED INDEX [IDX_CODEUPC] ON [DBO].[PRODUITS]
(
  [CODEUPC] ASC
)  WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, SORT_IN_TEMPDB = OFF, DROP_EXISTING = OFF, ONLINE = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
GO

-- INDEX -- NEW -- CODEUPC -- END --


-- FIELD -- NEW -- PriceUpdate_Products.CODEUPC -- START --

IF NOT EXISTS (
  SELECT 
    TOP 1 *
  FROM 
    INFORMATION_SCHEMA.COLUMNS
  WHERE 
        [TABLE_NAME]  = 'PriceUpdate_Products'
    AND [COLUMN_NAME] = 'CODEUPC' )
BEGIN
  ALTER TABLE
    PriceUpdate_Products
  ADD
    CODEUPC VARCHAR(12)
END
GO

-- FIELD -- NEW -- PriceUpdate_Products.CODEUPC -- END --


-- FIELD -- NEW -- PriceUpdate_Products.CODEUPCDIS -- START --

IF NOT EXISTS (
  SELECT 
    TOP 1 *
  FROM 
    INFORMATION_SCHEMA.COLUMNS
  WHERE 
        [TABLE_NAME]  = 'PriceUpdate_Products'
    AND [COLUMN_NAME] = 'CODEUPCDIS' )
BEGIN
  ALTER TABLE
    PriceUpdate_Products
  ADD
    CODEUPCDIS VARCHAR(12)
END
GO

-- FIELD -- NEW -- PriceUpdate_Products.CODEUPCDIS -- END --


-- SP -- UPDATE -- up_PriceUpdate_SaveProduct -- START --

IF EXISTS (SELECT * FROM INFORMATION_SCHEMA.ROUTINES WHERE Routine_Type = 'PROCEDURE' AND Specific_Name = 'up_PriceUpdate_SaveProduct')
  DROP PROCEDURE up_PriceUpdate_SaveProduct
GO

CREATE PROCEDURE [dbo].[up_PriceUpdate_SaveProduct](
  @PRO_ID      varchar(20), 
  @DESC        varchar(60), 
  @CODECAT     varchar(3),
  @COUUM       varchar(2), 
  @TEMPUM      varchar(2),
  @CLEMANU     varchar(30), 
  @CODEUPC     varchar(12), 
  @CODEUPCDIS varchar(12),   
  @CLEDIST     varchar(20), 
  @DESCDIST    varchar(60),
  @QPP         float, 
  @MULCOM      float,
  @COUBRUTUNI  float, 
  @COUESC      float, 
  @PROMCOUNET  float, 
  @NOUVEAU     varchar(1), 
  @DATECOUT    datetime
) AS

INSERT INTO PriceUpdate_Products(
  PRO_ID, 
  [DESC], 
  CODECAT,
  COUUM, 
  TEMPUM,
  CLEMANU, 
  CODEUPC,
  CODEUPCDIS,  
  CLEDIST, 
  DESCDIST,
  QPP, 
  MULCOM,
  COUBRUTUNI, 
  COUESC, 
  PROMCOUNET, 
  NOUVEAU, 
  DATECOUT)
VALUES (
  @PRO_ID, 
  @DESC, 
  @CODECAT,
  @COUUM, 
  @TEMPUM,
  @CLEMANU, 
  @CODEUPC, 
  @CODEUPCDIS,  
  @CLEDIST, 
  @DESCDIST,
  @QPP, 
  @MULCOM,
  @COUBRUTUNI, 
  @COUESC, 
  @PROMCOUNET, 
  @NOUVEAU, 
  @DATECOUT)
GO

-- SP -- UPDATE -- up_PriceUpdate_SaveProduct -- END --


-- SP -- UPDATE -- up_PriceUpdate_UpdateProducts -- BEGIN --

IF EXISTS (SELECT * FROM INFORMATION_SCHEMA.ROUTINES WHERE Routine_Type = 'PROCEDURE' AND Specific_Name = 'up_PriceUpdate_UpdateProducts')
  DROP PROCEDURE up_PriceUpdate_UpdateProducts
GO

CREATE PROCEDURE [dbo].[up_PriceUpdate_UpdateProducts] AS
BEGIN
-- 2014-11-25 EE-222 EMadore -
-- Voir si possible mettre les fonction de division en SQL. Eviterai le check avec les PRO_ID et les division manuelles

-- Inserer tous les produits inexistants
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
  -- Produits qui n'existent pas deja
  PRODUITS.PRO_ID IS NULL


-- Updater tous les produits
-- 2014-11-25 EE-222 EMadore -
-- Prise en comptes des prix net Rexel

-- 2016-11-21 EE-1044 EMadore 
-- Split du traitement en deux passe pour les produits Nedco / Westburne / Rexel et un autre pour Wolseley

-- Traitement pours logique de prix Wolseley
UPDATE PRODUITS
SET 
  --Si la description personnelle n'a jamais ete modifiee alors on peut se permettre de la mettre a jour
  PRODUITS.[DESC] = CASE WHEN PRODUITS.[DESC] IS NULL OR PRODUITS.[DESC] = '' OR PRODUITS.[DESC] = PRODUITS.DESCDIST THEN PriceUpdate_Products.[DESC] ELSE PRODUITS.[DESC] END,
  PRODUITS.[CODEUPC] = CASE WHEN PRODUITS.[CODEUPC] IS NULL OR PRODUITS.[CODEUPC] = '' OR PRODUITS.[CODEUPC] = PRODUITS.CODEUPCDIS THEN PriceUpdate_Products.[CODEUPC] ELSE PRODUITS.[CODEUPC] END,  
  --Si la categorie du produit est une categorie systeme, alors on peut l'ecraser sans souci 
  PRODUITS.CODECAT = CASE WHEN PRODUITS.CODECAT IS NULL OR PRODUITS.CODECAT = '' OR LEFT(PRODUITS.CODECAT, 1) = '+' OR LEFT(PRODUITS.CODECAT, 1) = '#' THEN PriceUpdate_Products.CODECAT ELSE PRODUITS.CODECAT END,
  --Les autres champs sont communs aux inserts et aux updates
  PRODUITS.CLEMANU = PriceUpdate_Products.CLEMANU,
  PRODUITS.CODEUPCDIS = PriceUpdate_Products.CODEUPCDIS,
  PRODUITS.CLEDIST = PriceUpdate_Products.CLEDIST,
  PRODUITS.DESCDIST = PriceUpdate_Products.DESCDIST,
  PRODUITS.COUUM = PriceUpdate_Products.COUUM,
  PRODUITS.QPP = PriceUpdate_Products.QPP,
  PRODUITS.MULCOM = PriceUpdate_Products.MULCOM,
  PRODUITS.CODEFOUR = 'WE',
  PRODUITS.COUBRUTUNI = PriceUpdate_Products.COUBRUTUNI,
  PRODUITS.COUESC     = PriceUpdate_Products.COUESC,
  PRODUITS.PROMCOUNET = PriceUpdate_Products.PROMCOUNET,
  PRODUITS.DNR = 'N',
  PRODUITS.NOUVEAU = PriceUpdate_Products.NOUVEAU,
  PRODUITS.DATECOUT = PriceUpdate_Products.DATECOUT,
  PRODUITS.DATECOUNET = PriceUpdate_Products.DATECOUT
FROM
  PRODUITS 
  INNER JOIN PriceUpdate_Products
  ON PRODUITS.PRO_ID = PriceUpdate_Products.PRO_ID
WHERE
  LEFT(PRODUITS.PRO_ID, 3) NOT IN ('NWE', 'NOE', 'NQE', 'NME', 'WAE', 'WME', 'WOE', 'WQE', 'LQE','GSE','SOE')

UPDATE PRODUITS
SET 
  --Si la description personnelle n'a jamais ete modifiee alors on peut se permettre de la mettre a jour
  PRODUITS.[DESC] = CASE WHEN PRODUITS.[DESC] IS NULL OR PRODUITS.[DESC] = '' OR PRODUITS.[DESC] = PRODUITS.DESCDIST THEN PriceUpdate_Products.[DESC] ELSE PRODUITS.[DESC] END,
  PRODUITS.[CODEUPC] = CASE WHEN PRODUITS.[CODEUPC] IS NULL OR PRODUITS.[CODEUPC] = '' OR PRODUITS.[CODEUPC] = PRODUITS.CODEUPCDIS THEN PriceUpdate_Products.[CODEUPC] ELSE PRODUITS.[CODEUPC] END,  
  --Si la categorie du produit est une categorie systeme, alors on peut l'ecraser sans souci 
  PRODUITS.CODECAT = CASE WHEN PRODUITS.CODECAT IS NULL OR PRODUITS.CODECAT = '' OR LEFT(PRODUITS.CODECAT, 1) = '+' OR LEFT(PRODUITS.CODECAT, 1) = '#' THEN PriceUpdate_Products.CODECAT ELSE PRODUITS.CODECAT END,
  --Les autres champs sont communs aux inserts et aux updates
  PRODUITS.CLEMANU = PriceUpdate_Products.CLEMANU,
  PRODUITS.CODEUPCDIS = PriceUpdate_Products.CODEUPCDIS,
  PRODUITS.CLEDIST = PriceUpdate_Products.CLEDIST,
  PRODUITS.DESCDIST = PriceUpdate_Products.DESCDIST,
  PRODUITS.COUUM = PriceUpdate_Products.COUUM,
  PRODUITS.QPP = PriceUpdate_Products.QPP,
  PRODUITS.MULCOM = PriceUpdate_Products.MULCOM,
  PRODUITS.CODEFOUR = CASE WHEN LEFT(PRODUITS.PRO_ID, 1) = 'N' THEN 'NE' 
                           WHEN LEFT(PRODUITS.PRO_ID, 1) = 'L' THEN 'LE' 
                           WHEN LEFT(PRODUITS.PRO_ID, 1) = 'G' THEN 'GE' 
                           WHEN LEFT(PRODUITS.PRO_ID, 1) = 'S' THEN 'SE' 
                           ELSE 'WE' END ,
  PRODUITS.COUBRUTUNI = CASE WHEN PRODUITS.DATECOUNET IS NULL THEN 0 ELSE PRODUITS.COUBRUTUNI END, -- Initialise à 0 a l'ajout, sinon, ne touche pas à ce prix. MaJ de prix découplé.
  PRODUITS.COUESC     = CASE WHEN PRODUITS.DATECOUNET IS NULL THEN 0 ELSE PRODUITS.COUESC END,     -- Initialise à 0 a l'ajout, sinon, ne touche pas à ce prix. MaJ de prix découplé.
  PRODUITS.PROMCOUNET = CASE WHEN PRODUITS.DATECOUNET IS NULL THEN 0 ELSE PRODUITS.PROMCOUNET END, -- Initialise à 0 a l'ajout, sinon, ne touche pas à ce prix. MaJ de prix découplé.
  PRODUITS.DNR = 'N',
  PRODUITS.NOUVEAU = PriceUpdate_Products.NOUVEAU,
  PRODUITS.DATECOUT = PriceUpdate_Products.DATECOUT -- Juste date de MaJ de liste, pas de date de MaJ de prix net.
  -- PRODUITS.DATECOUNET = CASE WHEN LEFT(PRODUITS.PRO_ID, 3) IN ('NWE', 'NOE', 'NQE', 'NME', 'WAE', 'WME', 'WOE', 'WQE') THEN PRODUITS.DATECOUNET ELSE PriceUpdate_Products.DATECOUT END  -- Date Prix net = Date cout brut pour Wosleley (validé ici comme pas Rexel)
FROM
  PRODUITS 
  INNER JOIN PriceUpdate_Products
  ON PRODUITS.PRO_ID = PriceUpdate_Products.PRO_ID
WHERE
  LEFT(PRODUITS.PRO_ID, 3) IN ('NWE', 'NOE', 'NQE', 'NME', 'WAE', 'WME', 'WOE', 'WQE', 'LQE','GSE','SOE')
END
GO

-- SP -- UPDATE -- up_PriceUpdate_UpdateProducts -- END --


-- New field - SOUPRO.ISVIRT  -- START
  
IF NOT EXISTS (
  SELECT 
    TOP 1 *
  FROM 
    INFORMATION_SCHEMA.COLUMNS
  WHERE 
        [TABLE_NAME]  = 'SOUPRO'
    AND [COLUMN_NAME] = 'ISVIRT' )
BEGIN
  ALTER TABLE
    SOUPRO
  ADD
    ISVIRT BIT
END
GO

-- New field - SOUPRO.ISVIRT  -- END


-- New field - SOUPRO.VIRTCOUNT  -- START
  
IF NOT EXISTS (
  SELECT 
    TOP 1 *
  FROM 
    INFORMATION_SCHEMA.COLUMNS
  WHERE 
        [TABLE_NAME]  = 'SOUPRO'
    AND [COLUMN_NAME] = 'VIRTCOUNT' )
BEGIN
  ALTER TABLE
    SOUPRO
  ADD
    VIRTCOUNT INT
END
GO

-- New field - SOUPRO.VIRTCOUNT  -- END


-- SP -- UPDATE -- up_SOUPRO_Update -- BEGIN --

IF EXISTS (SELECT * FROM INFORMATION_SCHEMA.ROUTINES WHERE Routine_Type = 'PROCEDURE' AND Specific_Name = 'up_SOUPRO_Update')
  DROP PROCEDURE up_SOUPRO_Update
GO

CREATE PROCEDURE [dbo].[up_SOUPRO_Update] (
  @UniqueId bigint,
  @SOU_ID varchar(20),
  @PRO_ID varchar(20),
  @CLEMANU varchar(30),
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
  @QTEACOM float,
  @ISVIRT bit,
  @VIRTCOUNT int
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
    [ISVIRT],
    [VIRTCOUNT],
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
    @ISVIRT,
    @VIRTCOUNT,
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
    [ISVIRT] = @ISVIRT,
    [VIRTCOUNT] = @VIRTCOUNT,
    SysDate = GETDATE()
  WHERE
    UniqueId = @UniqueId

  --Return updated ID
  RETURN @UniqueId
END
GO

-- SP -- UPDATE -- up_SOUPRO_Update -- END --


-- New field - FACPRO.ISVIRT  -- START
  
IF NOT EXISTS (
  SELECT 
    TOP 1 *
  FROM 
    INFORMATION_SCHEMA.COLUMNS
  WHERE 
        [TABLE_NAME]  = 'FACPRO'
    AND [COLUMN_NAME] = 'ISVIRT' )
BEGIN
  ALTER TABLE
    FACPRO
  ADD
    ISVIRT BIT
END
GO

-- New field - FACPRO.ISVIRT  -- END


-- New field - FACPRO.VIRTCOUNT  -- START
  
IF NOT EXISTS (
  SELECT 
    TOP 1 *
  FROM 
    INFORMATION_SCHEMA.COLUMNS
  WHERE 
        [TABLE_NAME]  = 'FACPRO'
    AND [COLUMN_NAME] = 'VIRTCOUNT' )
BEGIN
  ALTER TABLE
    FACPRO
  ADD
    VIRTCOUNT INT
END
GO

-- New field - FACPRO.VIRTCOUNT  -- END


-- SP -- UPDATE -- up_FACPRO_Update -- BEGIN --

IF EXISTS (SELECT * FROM INFORMATION_SCHEMA.ROUTINES WHERE Routine_Type = 'PROCEDURE' AND Specific_Name = 'up_FACPRO_Update')
  DROP PROCEDURE up_FACPRO_Update
GO


CREATE PROCEDURE [dbo].[up_FACPRO_Update] (
  @UniqueId bigint,
  @SOU_ID varchar(20),
  @PRO_ID varchar(20),
  @CLEMANU varchar(30),
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
  @QTEACOM float,
  @ISVIRT bit,
  @VIRTCOUNT int
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
    [ISVIRT],
    [VIRTCOUNT],
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
    @ISVIRT,
    @VIRTCOUNT,
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
    [ISVIRT] = @ISVIRT,
    [VIRTCOUNT] = @VIRTCOUNT,
    SysDate = GETDATE()
  WHERE
    UniqueId = @UniqueId

  --Return updated ID
  RETURN @UniqueId
END
GO

-- SP -- UPDATE -- up_FACPRO_Update -- END --
