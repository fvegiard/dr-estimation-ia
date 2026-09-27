ALTER TABLE BDEE
ALTER COLUMN NODIST [varchar](12)
GO


IF EXISTS (SELECT * FROM INFORMATION_SCHEMA.ROUTINES WHERE Routine_Type = 'PROCEDURE' AND Specific_Name = 'up_PriceUpdate_UpdateProducts')
  DROP PROCEDURE up_PriceUpdate_UpdateProducts
GO


CREATE PROCEDURE [dbo].[up_PriceUpdate_UpdateProducts] AS

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

-- 2016-11-21 EE-1044 EMadore 
-- Split du traitement en deux passe pour les produits Nedco / Westburne / Rexel et un autre pour Wolseley

-- Traitement pours logique de prix Wolseley
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
  LEFT(PRODUITS.PRO_ID, 3) NOT IN ('NWE', 'NOE', 'NQE', 'NME', 'WAE', 'WME', 'WOE', 'WQE', 'LQE')

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
  PRODUITS.CODEFOUR = CASE WHEN LEFT(PRODUITS.PRO_ID, 1) = 'N' THEN 'NE' 
                           WHEN LEFT(PRODUITS.PRO_ID, 1) = 'L' THEN 'LU' 
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
  LEFT(PRODUITS.PRO_ID, 3) IN ('NWE', 'NOE', 'NQE', 'NME', 'WAE', 'WME', 'WOE', 'WQE', 'LQE')
  
GO  


IF EXISTS (SELECT * FROM INFORMATION_SCHEMA.ROUTINES WHERE Routine_Type = 'PROCEDURE' AND Specific_Name = 'up_BDEE_Update')
  DROP PROCEDURE up_BDEE_Update
GO

CREATE PROCEDURE [dbo].[up_BDEE_Update] (
  @UniqueId bigint,
  @LVERSION	  int,
  @CODEVER	  varchar(20),
  @DATA       varchar(30),
  @NODIST	    varchar(12),
  @NOEEWIN	  varchar(6),
  @NOGEM	    varchar(6),
  @ISINT      bit,
  @DIVISIONPX varchar(2),
  @DIVISION	  varchar(3),
  @DESCR	    varchar(40),
  @URLFR	    varchar(100),
  @URLEN	    varchar(100),
  @ORDERURLFR varchar(200),
  @ORDERURLEN varchar(200),
  @PRICEURL   varchar(200),
  @AUTHURL    varchar(200),
  @AUTHGLOKEY varchar(64),
  @AUTHCLIKEY varchar(64),
  @URLMODE    char(1),
  @ISDEMO	    bit,
  @DEMOEND	  datetime,
  @SUPPORTEND	datetime,
  @MAXUSERS	  int,
  @ISSQL	    bit,
  @ISACOMBA	  bit,
  @ISAVANTAGE	bit,
  @ISSAGE50	  bit,
  @ISQUICKBK	bit,
  @MODULES    varchar(32),
  @KVERSION	  int,
  @LICENCEKEY	varchar(128)
) AS

IF @UniqueId IS NULL
BEGIN
  --Insert new data into table
  INSERT INTO BDEE (
    LVERSION, 
    CODEVER, 
    DATA, 
    NODIST, 
    NOEEWIN, 
    NOGEM, 
    ISINT, 
    DIVISIONPX, 
    DIVISION, 
    DESCR, 
    URLFR, 
    URLEN, 
    ORDERURLFR, 
    ORDERURLEN, 
    PRICEURL, 
    AUTHURL, 
    AUTHGLOKEY,
    AUTHCLIKEY,
    URLMODE,
    ISDEMO, 
    DEMOEND, 
    SUPPORTEND, 
    MAXUSERS, 
    ISSQL, 
    ISACOMBA, 
    ISAVANTAGE, 
    ISSAGE50, 
    ISQUICKBK,
    MODULES, 
    KVERSION, 
    LICENCEKEY, 
    SysDate
    )
  VALUES (
    @LVERSION, 
    @CODEVER, 
    @DATA, 
    @NODIST, 
    @NOEEWIN, 
    @NOGEM, 
    @ISINT, 
    @DIVISIONPX, 
    @DIVISION, 
    @DESCR, 
    @URLFR, 
    @URLEN, 
    @ORDERURLFR, 
    @ORDERURLEN, 
    @PRICEURL, 
    @AUTHURL,
    @AUTHGLOKEY,
    @AUTHCLIKEY, 
    @URLMODE,
    @ISDEMO, 
    @DEMOEND, 
    @SUPPORTEND, 
    @MAXUSERS, 
    @ISSQL, 
    @ISACOMBA, 
    @ISAVANTAGE, 
    @ISSAGE50, 
    @ISQUICKBK, 
    @MODULES,
    @KVERSION, 
    @LICENCEKEY, 
    GETDATE())

  --Return new ID
  RETURN @@IDENTITY
END ELSE
BEGIN
  --Update data into table
  UPDATE
    BDEE
  SET
    LVERSION    = @LVERSION,
    CODEVER     = @CODEVER,
    DATA        = @DATA,
    NODIST      = @NODIST,
    NOEEWIN     = @NOEEWIN,
    NOGEM       = @NOGEM,
    ISINT       = @ISINT,
    DIVISIONPX  = @DIVISIONPX,
    DIVISION    = @DIVISION,
    DESCR       = @DESCR,
    URLFR       = @URLFR,
    URLEN       = @URLEN,
    ORDERURLFR  = @ORDERURLFR,
    ORDERURLEN  = @ORDERURLEN,
    PRICEURL    = @PRICEURL,
    AUTHURL     = @AUTHURL,
    AUTHGLOKEY  = @AUTHGLOKEY,
    AUTHCLIKEY  = @AUTHCLIKEY,
    URLMODE     = @URLMODE,
    ISDEMO      = @ISDEMO,
    DEMOEND     = @DEMOEND,
    SUPPORTEND  = @SUPPORTEND,
    MAXUSERS    = @MAXUSERS,
    ISSQL       = @ISSQL,
    ISACOMBA    = @ISACOMBA,
    ISAVANTAGE  = @ISAVANTAGE,
    ISSAGE50    = @ISSAGE50,
    ISQUICKBK   = @ISQUICKBK,
    MODULES     = @MODULES,
    KVERSION    = @KVERSION,
    LICENCEKEY  = @LICENCEKEY,
    SysDate     = GETDATE()
  WHERE
    UniqueId = @UniqueId

  --Return updated ID
  RETURN @UniqueId
END
GO


IF NOT EXISTS (SELECT * FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = 'PROCORRESP')
BEGIN
  CREATE TABLE [dbo].PROCORRESP (
	UniqueId    bigint      IDENTITY(1,1) NOT NULL,
	[OLDDIV] [varchar](3) NULL,
	[OLDCLEMANU] [varchar](30) NULL,
	[NEWDIV] [varchar](3) NULL,
	[NEWCLEMANU] [varchar](30) NULL,
    [SysDate]   datetime    NOT NULL DEFAULT (getdate()),
    )
END
GO

  -- Passage de 20 a 30 char pour les CLEMANU de toutes les tables
ALTER TABLE dbo.COMMITEM ALTER COLUMN CLEMANU VARCHAR(30)
GO

ALTER TABLE dbo.FACPRO ALTER COLUMN CLEMANU VARCHAR(30)
GO

ALTER TABLE dbo.PriceUpdate_Products ALTER COLUMN CLEMANU VARCHAR(30)
GO

ALTER TABLE dbo.PRODUITS ALTER COLUMN CLEMANU VARCHAR(30)
GO

ALTER TABLE dbo.SOUPRO ALTER COLUMN CLEMANU VARCHAR(30)
GO

ALTER PROCEDURE [dbo].[up_FACPRO_Update] (
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


ALTER PROCEDURE [dbo].[up_SOUPRO_Update] (
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


ALTER PROCEDURE [dbo].[up_PriceUpdate_SaveProduct](
  @PRO_ID     varchar(20), 
  @DESC       varchar(60), 
  @CODECAT    varchar(3),
  @COUUM      varchar(2), 
  @TEMPUM     varchar(2),
  @CLEMANU    varchar(30), 
  @CLEDIST    varchar(20), 
  @DESCDIST   varchar(60),
  @QPP        float, 
  @MULCOM     float,
  @COUBRUTUNI float, 
  @COUESC     float, 
  @PROMCOUNET float, 
  @NOUVEAU    varchar(1), 
  @DATECOUT   datetime
) AS

INSERT INTO PriceUpdate_Products(
  PRO_ID, 
  [DESC], 
  CODECAT,
  COUUM, 
  TEMPUM,
  CLEMANU, 
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


ALTER PROCEDURE [dbo].[up_PRODUITS_Update] (
  @UniqueId bigint,
  @PRO_ID varchar(20),
  @PRO_ID_OLD varchar(20), -- V9 EE-682 Supercedes
  @PRO_ID_NEW varchar(20), -- V9 EE-682 Supercedes
  @CLEMANU varchar(30),
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
  @USER2 varchar(20),
  @PREFERED varchar(1)    -- V8 EE-263 - Prix net Rexel Phase 2
) AS

IF @UniqueId IS NULL
BEGIN
  --Insert new data into table
  INSERT INTO PRODUITS (
    [PRO_ID],
    [PRO_ID_OLD],   -- V9 EE-682 Supercedes
    [PRO_ID_NEW],   -- V9 EE-682 Supercedes
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
    [PREFERED],     -- V8 EE-263 - Prix net Rexel Phase 2
    SysDate)
  VALUES (
    @PRO_ID,
    @PRO_ID_OLD,   -- V9 EE-682 Supercedes
    @PRO_ID_NEW,   -- V9 EE-682 Supercedes
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
    @PREFERED,    -- V8 EE-263 - Prix net Rexel Phase 2
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
    [PRO_ID_OLD] = @PRO_ID_OLD,   -- V9 EE-682 Supercedes
    [PRO_ID_NEW] = @PRO_ID_NEW,   -- V9 EE-682 Supercedes
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
    [PREFERED] = CASE WHEN @PREFERED IS NULL THEN [PREFERED] ELSE @PREFERED END,  -- V8 EE-263 - Prix net Rexel Phase 2
    SysDate = GETDATE()
  WHERE
    UniqueId = @UniqueId

  --Return updated ID
  RETURN @UniqueId
END
GO


ALTER PROCEDURE [dbo].[up_COMMITEM_Update] (
  @UniqueId bigint,
  @COM_ID varchar(20),
  @ORDRE varchar(6),
  @PRO_ID varchar(20),
  @CLEMANU varchar(30),
  @CLEDIST varchar(20),
  @CLEPERS varchar(20),
  @PRO_TYPE varchar(1),
  @DESCR varchar(60),
  @QTE_TOT float,
  @COUBRUTUNI float,
  @COUUM varchar(2),
  @COUESC float,
  @PROMCOUNET float,
  @QPP float,
  @MULCOM float,
  @CODEIMPR varchar(2),
  @NOTES      text        = '' -- Update V2.#0001
) AS

IF @UniqueId IS NULL
BEGIN
  --Insert new data into table
  INSERT INTO COMMITEM (
    [COM_ID],
    [ORDRE],
    [PRO_ID],
    [CLEMANU],
    [CLEDIST],
    [CLEPERS],
    [PRO_TYPE],
    [DESCR],
    [QTE_TOT],
    [COUBRUTUNI],
    [COUUM],
    [COUESC],
    [PROMCOUNET],
    [QPP],
    [MULCOM],
    [CODEIMPR],
    [NOTES],      -- Update V2.#0001
    SysDate)
  VALUES (
    @COM_ID,
    @ORDRE,
    @PRO_ID,
    @CLEMANU,
    @CLEDIST,
    @CLEPERS,
    @PRO_TYPE,
    @DESCR,
    @QTE_TOT,
    @COUBRUTUNI,
    @COUUM,
    @COUESC,
    @PROMCOUNET,
    @QPP,
    @MULCOM,
    @CODEIMPR,
    @NOTES,     -- Update V2.#0001
    GETDATE())

  --Return new ID
  RETURN @@IDENTITY
END ELSE
BEGIN
  --Update data into table
  UPDATE
    COMMITEM
  SET
    [COM_ID] = @COM_ID,
    [ORDRE] = @ORDRE,
    [PRO_ID] = @PRO_ID,
    [CLEMANU] = @CLEMANU,
    [CLEDIST] = @CLEDIST,
    [CLEPERS] = @CLEPERS,
    [PRO_TYPE] = @PRO_TYPE,
    [DESCR] = @DESCR,
    [QTE_TOT] = @QTE_TOT,
    [COUBRUTUNI] = @COUBRUTUNI,
    [COUUM] = @COUUM,
    [COUESC] = @COUESC,
    [PROMCOUNET] = @PROMCOUNET,
    [QPP] = @QPP,
    [MULCOM] = @MULCOM,
    [CODEIMPR] = @CODEIMPR,
    [NOTES] = @NOTES,           -- Update V2.#0001
    SysDate = GETDATE()
  WHERE
    UniqueId = @UniqueId

  --Return updated ID
  RETURN @UniqueId
END
GO
