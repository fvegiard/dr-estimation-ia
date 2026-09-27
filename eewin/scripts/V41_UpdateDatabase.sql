  -- Correctif - Absence des champs Avantages dans les SP de plusieurs tables

  -- DROP PROCEDURE up_SOUBLO_Update
IF OBJECT_ID(N'dbo.up_SOUBLO_Update', N'P') IS NOT NULL 
    DROP PROCEDURE dbo.up_SOUBLO_Update;
GO

  -- CREATE PROCEDURE up_SOUBLO_Update
CREATE PROCEDURE [dbo].[up_SOUBLO_Update] (
  @UniqueId bigint,
  @SOU_ID varchar(20),
  @BLO_ID varchar(3),
  @DESC varchar(40),
  @ACC_NO varchar(20),
  @ACH_NO varchar(20),
  @MULT int,
  @ORDRE varchar(6)
) AS

IF @UniqueId IS NULL
BEGIN
  --Insert new data into table
  INSERT INTO SOUBLO (
    [SOU_ID],
    [BLO_ID],
    [DESC],
    [ACC_NO],
    [ACH_NO],
    [MULT],
    [ORDRE],
    SysDate)
  VALUES (
    @SOU_ID,
    @BLO_ID,
    @DESC,
    @ACC_NO,
    @ACH_NO,
    @MULT,
    @ORDRE,
    GETDATE())

  --Return new ID
  RETURN @@IDENTITY
END ELSE
BEGIN
  --Update data into table
  UPDATE
    SOUBLO
  SET
    [SOU_ID] = @SOU_ID,
    [BLO_ID] = @BLO_ID,
    [DESC] = @DESC,
    [ACC_NO] = @ACC_NO,
    [ACH_NO] = @ACH_NO,
    [MULT] = @MULT,
    [ORDRE] = @ORDRE,
    SysDate = GETDATE()
  WHERE
    UniqueId = @UniqueId

  --Return updated ID
  RETURN @UniqueId
END
GO
---------------------


  -- DROP PROCEDURE up_SOUDIV_Update
IF OBJECT_ID(N'dbo.up_SOUDIV_Update', N'P') IS NOT NULL 
    DROP PROCEDURE dbo.up_SOUDIV_Update;
GO

  -- CREATE PROCEDURE up_SOUDIV_Update
CREATE PROCEDURE [dbo].[up_SOUDIV_Update] (
  @UniqueId bigint,
  @SOU_ID varchar(20),
  @DIV_ID varchar(3),
  @ACT_NO VARCHAR(20),  
  @DESC varchar(40),
  @ORDRE varchar(6)
) AS

IF @UniqueId IS NULL
BEGIN
  --Insert new data into table
  INSERT INTO SOUDIV (
    [SOU_ID],
    [DIV_ID],
    [ACT_NO],	
    [DESC],
    [ORDRE],
    SysDate)
  VALUES (
    @SOU_ID,
    @DIV_ID,
    @ACT_NO,
    @DESC,
    @ORDRE,
    GETDATE())

  --Return new ID
  RETURN @@IDENTITY
END ELSE
BEGIN
  --Update data into table
  UPDATE
    SOUDIV
  SET
    [SOU_ID] = @SOU_ID,
    [DIV_ID] = @DIV_ID,
    [ACT_NO] = @ACT_NO,	
    [DESC] = @DESC,
    [ORDRE] = @ORDRE,
    SysDate = GETDATE()
  WHERE
    UniqueId = @UniqueId

  --Return updated ID
  RETURN @UniqueId
END
GO
