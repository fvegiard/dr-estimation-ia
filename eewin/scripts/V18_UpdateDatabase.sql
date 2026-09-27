IF EXISTS (SELECT * FROM INFORMATION_SCHEMA.ROUTINES WHERE Routine_Type = 'PROCEDURE' AND Specific_Name = 'up_PriceUpdate_DiscontinueProducts')
  DROP PROCEDURE up_PriceUpdate_DiscontinueProducts
GO

CREATE PROCEDURE [dbo].[up_PriceUpdate_DiscontinueProducts] (
  @Division varchar(3),
  @UpdateDate datetime
) AS

UPDATE 
  PRODUITS
SET 
  DNR = 'Y',
  NOUVEAU = 'N'
WHERE
  PRO_ID LIKE @Division + '%'
  AND DATECOUT <> @UpdateDate
  AND LEN(PRO_ID) <> 20
GO

  -- New field - BDEE.SRCHWEBURL
IF NOT EXISTS (
  SELECT 
    TOP 1 *
  FROM 
    INFORMATION_SCHEMA.COLUMNS
  WHERE 
        [TABLE_NAME]  = 'BDEE'
    AND [COLUMN_NAME] = 'SRCHWEBURL' )
BEGIN
  ALTER TABLE
    BDEE
  ADD
    SRCHWEBURL VARCHAR(200)
END
GO
