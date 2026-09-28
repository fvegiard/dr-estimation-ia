
  -- New field - PRODUITS.SHOWONWEB
IF NOT EXISTS (
  SELECT 
    TOP 1 *
  FROM 
    INFORMATION_SCHEMA.COLUMNS
  WHERE 
        [TABLE_NAME]  = 'PRODUITS'
    AND [COLUMN_NAME] = 'SHOWONWEB' )
BEGIN
  ALTER TABLE
    PRODUITS
  ADD
    SHOWONWEB VARCHAR(1) default '1'
END
GO

BEGIN
  update PRODUITS set SHOWONWEB = '1'
  where SHOWONWEB is NULL
END
GO

  -- New field - PriceUpdate_Products.SHOWONWEB
IF NOT EXISTS (
  SELECT 
    TOP 1 *
  FROM 
    INFORMATION_SCHEMA.COLUMNS
  WHERE 
        [TABLE_NAME]  = 'PriceUpdate_Products'
    AND [COLUMN_NAME] = 'SHOWONWEB' )
BEGIN
  ALTER TABLE
    PriceUpdate_Products
  ADD
    SHOWONWEB VARCHAR(1)
END
GO

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
  @SHOWONWEB   varchar(1),  
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
  SHOWONWEB,
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
  @SHOWONWEB,
  @QPP, 
  @MULCOM,
  @COUBRUTUNI, 
  @COUESC, 
  @PROMCOUNET, 
  @NOUVEAU, 
  @DATECOUT)
GO

IF EXISTS (SELECT * FROM INFORMATION_SCHEMA.ROUTINES WHERE Routine_Type = 'PROCEDURE' AND Specific_Name = 'up_PriceUpdate_UpdateProducts')
  DROP PROCEDURE up_PriceUpdate_UpdateProducts
GO


CREATE PROCEDURE [dbo].[up_PriceUpdate_UpdateProducts] AS
BEGIN
-- 2018-06-12 EE-1723 EMadore -
-- Les prix pouvaient etre remis a 0 si les usager n'avaient pas fait encore de MaJ de prix
-- Le check etait fait sur la derniere date de MaJ de prix net
-- Resultat, nos ancien client Rexel avait des produits avec des prix mais sans jamais avoir fait de MaJ
-- Les changement plus bas assure que ces prix sont preserver.

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
  --Si la description personnelle n'a jamais ete modifiee alors on peut se permettre de la mettre a†jour
  PRODUITS.[DESC] = CASE WHEN PRODUITS.[DESC] IS NULL OR PRODUITS.[DESC] = '' OR PRODUITS.[DESC] = PRODUITS.DESCDIST THEN PriceUpdate_Products.[DESC] ELSE PRODUITS.[DESC] END,
  PRODUITS.[CODEUPC] = CASE WHEN PRODUITS.[CODEUPC] IS NULL OR PRODUITS.[CODEUPC] = '' OR PRODUITS.[CODEUPC] = PRODUITS.CODEUPCDIS THEN PriceUpdate_Products.[CODEUPC] ELSE PRODUITS.[CODEUPC] END,  
  --Si la categorie du produit est une categorie systeme, alors on peut l'ecraser sans souci 
  PRODUITS.CODECAT = CASE WHEN PRODUITS.CODECAT IS NULL OR PRODUITS.CODECAT = '' OR LEFT(PRODUITS.CODECAT, 1) = '+' OR LEFT(PRODUITS.CODECAT, 1) = '#' THEN PriceUpdate_Products.CODECAT ELSE PRODUITS.CODECAT END,
  --Les autres champs sont communs aux inserts et aux updates
  PRODUITS.CLEMANU = PriceUpdate_Products.CLEMANU,
  PRODUITS.CODEUPCDIS = PriceUpdate_Products.CODEUPCDIS,
  PRODUITS.SHOWONWEB = PriceUpdate_Products.SHOWONWEB,  
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
  PRODUITS.SHOWONWEB = PriceUpdate_Products.SHOWONWEB,  
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
  PRODUITS.COUBRUTUNI = CASE WHEN PRODUITS.DATECOUNET IS NULL THEN COALESCE(PRODUITS.COUBRUTUNI, 0) ELSE PRODUITS.COUBRUTUNI END, -- Initialise a 0 a l'ajout, sinon, ne touche pas a ce prix. MaJ de prix decouplee.
  PRODUITS.COUESC     = CASE WHEN PRODUITS.DATECOUNET IS NULL THEN COALESCE(PRODUITS.COUESC, 0) ELSE PRODUITS.COUESC END,     -- Initialise a 0 a l'ajout, sinon, ne touche pas a ce prix. MaJ de prix decouplee.
  PRODUITS.PROMCOUNET = CASE WHEN PRODUITS.DATECOUNET IS NULL THEN COALESCE(PRODUITS.PROMCOUNET, 0) ELSE PRODUITS.PROMCOUNET END, -- Initialise a 0 a l'ajout, sinon, ne touche pas a ce prix. MaJ de prix decouplee.
  PRODUITS.DNR = 'N',
  PRODUITS.NOUVEAU = PriceUpdate_Products.NOUVEAU,
  PRODUITS.DATECOUT = PriceUpdate_Products.DATECOUT -- Juste date de MaJ de liste, pas de date de MaJ de prix net.
  -- PRODUITS.DATECOUNET = CASE WHEN LEFT(PRODUITS.PRO_ID, 3) IN ('NWE', 'NOE', 'NQE', 'NME', 'WAE', 'WME', 'WOE', 'WQE') THEN PRODUITS.DATECOUNET ELSE PriceUpdate_Products.DATECOUT END  -- Date Prix net = Date cout brut pour Wosleley (valid√© ici comme pas Rexel)
FROM
  PRODUITS 
  INNER JOIN PriceUpdate_Products
  ON PRODUITS.PRO_ID = PriceUpdate_Products.PRO_ID
WHERE
  LEFT(PRODUITS.PRO_ID, 3) IN ('NWE', 'NOE', 'NQE', 'NME', 'WAE', 'WME', 'WOE', 'WQE', 'LQE','GSE','SOE')
END
GO

