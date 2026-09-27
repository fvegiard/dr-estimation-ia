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
  PRODUITS.CODEFOUR = CASE WHEN LEFT(PRODUITS.PRO_ID, 1) = 'N' THEN 'NE' ELSE 'WE' END,
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
  LEFT(PRODUITS.PRO_ID, 3) NOT IN ('NWE', 'NOE', 'NQE', 'NME', 'WAE', 'WME', 'WOE', 'WQE')

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
  LEFT(PRODUITS.PRO_ID, 3) IN ('NWE', 'NOE', 'NQE', 'NME', 'WAE', 'WME', 'WOE', 'WQE')
GO

--Vider la table temp maintenant qu'on a fini  
--TRUNCATE TABLE PriceUpdate_Products
