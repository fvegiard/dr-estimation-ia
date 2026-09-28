-- BDEE_MULTI START --------------------------------------------------------------------------

IF NOT EXISTS (SELECT * FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = 'BDEE_MULTI')
BEGIN
  CREATE TABLE [dbo].BDEE_MULTI  (
    [UniqueId] [bigint] IDENTITY(1,1) NOT NULL,
    --BDEEM_ID  varchar(20) NOT NULL,   
    [DistributorCode] [varchar](3) NOT NULL,
    [ORDRE] [varchar](6) NOT NULL,
    [DistributorName] [varchar](40) NULL,
    [SysDate] [datetime] NOT NULL
    )
END
GO

IF EXISTS (SELECT * FROM INFORMATION_SCHEMA.TABLE_CONSTRAINTS WHERE TABLE_NAME = 'BDEE_MULTI' AND CONSTRAINT_NAME = 'PK_BDEE_MULTI')
BEGIN
  ALTER TABLE BDEE_MULTI DROP CONSTRAINT PK_BDEE_MULTI
END
GO

ALTER TABLE BDEE_MULTI ADD CONSTRAINT
  PK_BDEE_MULTI PRIMARY KEY CLUSTERED 
  (
  DistributorCode
  ) WITH( STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
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

-- BDEE_MULTI END --------------------------------------------------------------------------
