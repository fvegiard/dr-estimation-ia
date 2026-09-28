-- BDEE_MULTI ADJUST START --------------------------------------------------------------------------

  -- New field - BDEE_MULTI.ORDRE
IF NOT EXISTS (
  SELECT 
    TOP 1 *
  FROM 
    INFORMATION_SCHEMA.COLUMNS
  WHERE 
        [TABLE_NAME]  = 'BDEE_MULTI'
    AND [COLUMN_NAME] = 'ORDRE' )
BEGIN
  ALTER TABLE
    BDEE_MULTI
  ADD
    ORDRE  varchar(6);
END
GO

  -- New field - PRODUITS.PRO_ID_Parent
IF NOT EXISTS (
  SELECT 
    TOP 1 *
  FROM 
    INFORMATION_SCHEMA.COLUMNS
  WHERE 
        [TABLE_NAME]  = 'PRODUITS'
    AND [COLUMN_NAME] = 'PRO_ID_Parent' )
BEGIN
  ALTER TABLE
    PRODUITS
  ADD
    PRO_ID_Parent  varchar(20);
END
GO


IF EXISTS (SELECT * FROM INFORMATION_SCHEMA.ROUTINES WHERE Routine_Type = 'PROCEDURE' AND Specific_Name = 'up_BDEE_MULTI_Update')
  DROP PROCEDURE up_BDEE_MULTI_Update
GO

CREATE PROCEDURE [dbo].[up_BDEE_MULTI_Update] (
  @UniqueId   bigint,
  @DistributorCode  varchar(3),
  @ORDRE varchar(6),
  @DistributorName  varchar(40)
) AS

IF @UniqueId IS NULL
BEGIN
  --Insert new data into table
  INSERT INTO BDEE_MULTI (
    [DistributorCode],
    [ORDRE],
    [DistributorName],
    SysDate)
  VALUES (
    @DistributorCode,
    @ORDRE,
    @DistributorName,
    GETDATE())

  --Return new ID
  RETURN @@IDENTITY
END ELSE
BEGIN
  --Update data into table
  UPDATE
    BDEE_MULTI
  SET
    [DistributorCode] = @DistributorCode,
    [ORDRE]           = @ORDRE,
    [DistributorName] = @DistributorName,
    SysDate           = GETDATE()
  WHERE
    UniqueId = @UniqueId

  --Return updated ID
  RETURN @UniqueId
END
GO

-- BDEE_MULTI ADJUST END --------------------------------------------------------------------------
