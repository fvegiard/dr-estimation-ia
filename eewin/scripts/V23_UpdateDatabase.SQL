

  -- New field - SOUMIS.USER_ID_UP
IF NOT EXISTS (
  SELECT 
    TOP 1 *
  FROM 
    INFORMATION_SCHEMA.COLUMNS
  WHERE 
        [TABLE_NAME]  = 'SOUMIS'
    AND [COLUMN_NAME] = 'USER_ID_UP' )
BEGIN
  ALTER TABLE
    SOUMIS
  ADD
    USER_ID_UP  VARCHAR(20);
END
GO



  -- New field - SOUMIS.USER_UPDATE
IF NOT EXISTS (
  SELECT 
    TOP 1 *
  FROM 
    INFORMATION_SCHEMA.COLUMNS
  WHERE 
        [TABLE_NAME]  = 'SOUMIS'
    AND [COLUMN_NAME] = 'USER_UPDATE' )
BEGIN
  ALTER TABLE
    SOUMIS
  ADD
    USER_UPDATE DATETIME NULL;
END
GO

-----------------------------

IF EXISTS (SELECT * FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = 'USERSESSION')
BEGIN
  DROP TABLE USERSESSION
END
GO


IF NOT EXISTS (SELECT * FROM INFORMATION_SCHEMA.TABLES WHERE Table_Name = 'USERSESSION')
BEGIN
  CREATE TABLE [dbo].USERSESSION (
  UniqueId          bigint       IDENTITY(1,1) NOT NULL,
  [SESSION_ID]      bigint ,  
  [USER_ID]   [varchar](20),       
  [SysDate]        datetime     NOT NULL DEFAULT (getdate()),
    )
END
GO


IF OBJECT_ID(N'dbo.up_USERSESSION_Update', N'P') IS NOT NULL 
    DROP PROCEDURE dbo.up_USERSESSION_Update ;
GO


CREATE PROCEDURE [dbo].[up_USERSESSION_Update] (
  @UniqueId bigint,
  @SESSION_ID bigint,
  @USER_ID VARCHAR(20)
) AS

IF @UniqueId IS NULL
BEGIN
  --Insert new data into table
  INSERT INTO USERSESSION (
    [SESSION_ID],
    [USER_ID],
    SysDate)
  VALUES (

    @SESSION_ID,
    @USER_ID,
    GETDATE())

  --Return new ID
  RETURN @@IDENTITY
END ELSE
BEGIN
  --Update data into table
  UPDATE
    USERSESSION
  SET
    [SESSION_ID] = @SESSION_ID,
    [USER_ID] = @USER_ID,
    SysDate = GETDATE()
  WHERE
    UniqueId = @UniqueId

  --Return updated ID
  RETURN @UniqueId
END
GO


IF OBJECT_ID(N'dbo.GetCurrentUserSession ', N'FN') IS NOT NULL 
    DROP FUNCTION dbo.GetCurrentUserSession  ;
GO

CREATE FUNCTION [dbo].GetCurrentUserSession()
RETURNS VARCHAR(20) 
AS BEGIN
    DECLARE @USER_ID    varchar(20)

    SELECT @USER_ID     = P.USER_ID
    FROM   USERSESSION P
    WHERE  P.SESSION_ID = @@SPID;

    RETURN @USER_ID

END
GO

IF OBJECT_ID(N'dbo.sp_Update_SoumisUseSession', N'P') IS NOT NULL 
    DROP PROCEDURE dbo.sp_Update_SoumisUseSession ;
GO

CREATE PROCEDURE [dbo].sp_Update_SoumisUseSession(@SOU_ID VARCHAR(20))
AS
  DECLARE @OLDUSERID VARCHAR(20)
  DECLARE @NEWUSERID VARCHAR(20)
  DECLARE @LASTUPDATE DATETIME
    
  SELECT @NEWUSERID = dbo.GetCurrentUserSession()
  SELECT @OLDUSERID = USER_ID_UP, @LASTUPDATE = USER_UPDATE FROM SOUMIS WHERE SOU_ID = @SOU_ID

  IF (ISNULL(@NEWUSERID,'') = '') OR (ISNULL(@OLDUSERID,'') = '') OR (ISNULL(@LASTUPDATE,'') = '') OR (@NEWUSERID <> @OLDUSERID) OR
     ((@NEWUSERID = @OLDUSERID) AND (DATEDIFF(second, @LASTUPDATE, GETDATE()) > 60))
  BEGIN
    UPDATE SOUMIS
       SET USER_ID_UP = @NEWUSERID,
           USER_UPDATE = GETDATE()
     WHERE SOU_ID = @SOU_ID 
  END;
GO

-------------------------------------------

IF OBJECT_ID(N'dbo.up_SOUAMD_Update', N'P') IS NOT NULL 
    DROP PROCEDURE dbo.up_SOUAMD_Update ;
GO


CREATE PROCEDURE [dbo].[up_SOUAMD_Update] (
  @UniqueId bigint,
  @SOU_ID varchar(20),
  @BLO_ID varchar(3),
  @DIV_ID varchar(3),
  @FACTMD float
) AS

IF @UniqueId IS NULL
BEGIN
  --Insert new data into table
  INSERT INTO SOUAMD (
    [SOU_ID],
    [BLO_ID],
    [DIV_ID],
    [FACTMD],
    SysDate)
  VALUES (
    @SOU_ID,
    @BLO_ID,
    @DIV_ID,
    @FACTMD,
    GETDATE())

  --Return new ID
  RETURN @@IDENTITY
END ELSE
BEGIN
  --Update data into table
  UPDATE
    SOUAMD
  SET
    [SOU_ID] = @SOU_ID,
    [BLO_ID] = @BLO_ID,
    [DIV_ID] = @DIV_ID,
    [FACTMD] = @FACTMD,
    SysDate = GETDATE()
  WHERE
    UniqueId = @UniqueId

    -- Mise à jour du Last user updating SOUMIS
  exec dbo.sp_Update_SoumisUseSession @SOU_ID
  
  --Return updated ID
  RETURN @UniqueId
END
GO


IF OBJECT_ID(N'dbo.up_SOUBLO_Update', N'P') IS NOT NULL 
    DROP PROCEDURE dbo.up_SOUBLO_Update ;
GO

CREATE PROCEDURE [dbo].[up_SOUBLO_Update] (
  @UniqueId bigint,
  @SOU_ID varchar(20),
  @BLO_ID varchar(3),
  @DESC varchar(40),
  @ACC_NO varchar(20),
  @ACH_NO varchar(20),
  @MULT int
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
    SysDate)
  VALUES (
    @SOU_ID,
    @BLO_ID,
    @DESC,
    @ACC_NO,
    @ACH_NO,
    @MULT,
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
    SysDate = GETDATE()
  WHERE
    UniqueId = @UniqueId

    -- Mise à jour du Last user updating SOUMIS
  exec dbo.sp_Update_SoumisUseSession @SOU_ID
  
  --Return updated ID
  RETURN @UniqueId
END
GO


IF OBJECT_ID(N'dbo.up_SOUDIV_Update', N'P') IS NOT NULL 
    DROP PROCEDURE dbo.up_SOUDIV_Update ;
GO

CREATE PROCEDURE [dbo].[up_SOUDIV_Update] (
  @UniqueId bigint,
  @SOU_ID varchar(20),
  @DIV_ID varchar(3),
  @ACT_NO VARCHAR(20),  
  @DESC varchar(40)
) AS

IF @UniqueId IS NULL
BEGIN
  --Insert new data into table
  INSERT INTO SOUDIV (
    [SOU_ID],
    [DIV_ID],
    [ACT_NO],	
    [DESC],
    SysDate)
  VALUES (
    @SOU_ID,
    @DIV_ID,
    @ACT_NO,	
    @DESC,
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
    [DESC]   = @DESC,
    SysDate  = GETDATE()
  WHERE
    UniqueId = @UniqueId

    -- Mise à jour du Last user updating SOUMIS
  exec dbo.sp_Update_SoumisUseSession @SOU_ID
  
  --Return updated ID
  RETURN @UniqueId
END
GO


IF OBJECT_ID(N'dbo.up_SOUENS_Update', N'P') IS NOT NULL 
    DROP PROCEDURE dbo.up_SOUENS_Update ;
GO


CREATE PROCEDURE [dbo].[up_SOUENS_Update] (
  @UniqueId bigint,
  @SOU_ID varchar(20),
  @ENS_ID varchar(20),
  @ENS_ORG_ID varchar(20),  -- 2014-08-12 EMadore V6 : New
  @DESC varchar(60),        -- 2012-01-19 EMadore V3 : Passage de 40 à 60 chars
  @QTETOT float,
  @QTETOTSECT float,
  @CALCTIMSTP varchar(14),
  @COUUM varchar(2),
  @TEMPUNI float,
  @TEMPSEC float,
  @TEMPUM varchar(2),
  @DATECREE datetime,
  @OLDESTPROD datetime,
  @CLEPERS varchar(40),
  @PROFIT float
) AS

IF @UniqueId IS NULL
BEGIN
  --Insert new data into table
  INSERT INTO SOUENS (
    [SOU_ID],
    [ENS_ID],
    [ENS_ORG_ID],
    [DESC],
    [QTETOT],
    [QTETOTSECT],
    [CALCTIMSTP],
    [COUUM],
    [TEMPUNI],
    [TEMPSEC],
    [TEMPUM],
    [DATECREE],
    [OLDESTPROD],
    [CLEPERS],
    [PROFIT],
    SysDate)
  VALUES (
    @SOU_ID,
    @ENS_ID,
    @ENS_ORG_ID,
    @DESC,
    @QTETOT,
    @QTETOTSECT,
    @CALCTIMSTP,
    @COUUM,
    @TEMPUNI,
    @TEMPSEC,
    @TEMPUM,
    @DATECREE,
    @OLDESTPROD,
    @CLEPERS,
    @PROFIT,
    GETDATE())

  --Return new ID
  RETURN @@IDENTITY
END ELSE
BEGIN
  --Update data into table
  UPDATE
    SOUENS
  SET
    [SOU_ID] = @SOU_ID,
    [ENS_ID] = @ENS_ID,
    [ENS_ORG_ID] = @ENS_ORG_ID,
    [DESC] = @DESC,
    [QTETOT] = @QTETOT,
    [QTETOTSECT] = @QTETOTSECT,
    [CALCTIMSTP] = @CALCTIMSTP,
    [COUUM] = @COUUM,
    [TEMPUNI] = @TEMPUNI,
    [TEMPSEC] = @TEMPSEC,
    [TEMPUM] = @TEMPUM,
    [DATECREE] = @DATECREE,
    [OLDESTPROD] = @OLDESTPROD,
    [CLEPERS] = @CLEPERS,
    [PROFIT] = @PROFIT,
    SysDate = GETDATE()
  WHERE
    UniqueId = @UniqueId

    -- Mise à jour du Last user updating SOUMIS
  exec dbo.sp_Update_SoumisUseSession @SOU_ID
  
  --Return updated ID
  RETURN @UniqueId
END
GO


IF OBJECT_ID(N'dbo.up_SOUENSCO_Update', N'P') IS NOT NULL 
    DROP PROCEDURE dbo.up_SOUENSCO_Update ;
GO

CREATE PROCEDURE [dbo].[up_SOUENSCO_Update] (
  @UniqueId bigint,
  @SOU_ID varchar(20),
  @ENS_ID varchar(20),
  @PRO_ID varchar(20),
  @ORDRE varchar(6),
  @QTE float,
  @QTEUM varchar(2),
  @TYPRATIO varchar(1),
  @DIV float,
  @DIVUM varchar(2)
) AS

IF @UniqueId IS NULL
BEGIN
  --Insert new data into table
  INSERT INTO SOUENSCO (
    [SOU_ID],
    [ENS_ID],
    [PRO_ID],
    [ORDRE],
    [QTE],
    [QTEUM],
    [TYPRATIO],
    [DIV],
    [DIVUM],
    SysDate)
  VALUES (
    @SOU_ID,
    @ENS_ID,
    @PRO_ID,
    @ORDRE,
    @QTE,
    @QTEUM,
    @TYPRATIO,
    @DIV,
    @DIVUM,
    GETDATE())

  --Return new ID
  RETURN @@IDENTITY
END ELSE
BEGIN
  --Update data into table
  UPDATE
    SOUENSCO
  SET
    [SOU_ID] = @SOU_ID,
    [ENS_ID] = @ENS_ID,
    [PRO_ID] = @PRO_ID,
    [ORDRE] = @ORDRE,
    [QTE] = @QTE,
    [QTEUM] = @QTEUM,
    [TYPRATIO] = @TYPRATIO,
    [DIV] = @DIV,
    [DIVUM] = @DIVUM,
    SysDate = GETDATE()
  WHERE
    UniqueId = @UniqueId

    -- Mise à jour du Last user updating SOUMIS
  exec dbo.sp_Update_SoumisUseSession @SOU_ID
  
  --Return updated ID
  RETURN @UniqueId
END
GO


IF OBJECT_ID(N'dbo.up_SOULOTS_Update', N'P') IS NOT NULL 
    DROP PROCEDURE dbo.up_SOULOTS_Update ;
GO

CREATE PROCEDURE [dbo].[up_SOULOTS_Update] (
  @UniqueId bigint,
  @SOU_ID varchar(20),
  @LOTS_ID varchar(20),
  @DESC varchar(60),         -- 2012-01-19 EMadore V3 : Passage de 40 à 60 chars
  @QTETOT float,
  @QTETOTSECT float,
  @CALCTIMSTP varchar(14),
  @COUUM varchar(2),
  @TEMPUNI float,
  @TEMPUM varchar(2),
  @DATECREE datetime,
  @OLDESTPROD datetime,
  @CLEPERS varchar(40),
  @PROFIT float,
  @COUTANTSEL int,
  @COUTANT1 float,
  @COUTANT2 float,
  @COUTANT3 float,
  @COUTANT4 float
) AS

IF @UniqueId IS NULL
BEGIN
  --Insert new data into table
  INSERT INTO SOULOTS (
    [SOU_ID],
    [LOTS_ID],
    [DESC],
    [QTETOT],
    [QTETOTSECT],
    [CALCTIMSTP],
    [COUUM],
    [TEMPUNI],
    [TEMPUM],
    [DATECREE],
    [OLDESTPROD],
    [CLEPERS],
    [PROFIT],
    [COUTANTSEL],
    [COUTANT1],
    [COUTANT2],
    [COUTANT3],
    [COUTANT4],
    SysDate)
  VALUES (
    @SOU_ID,
    @LOTS_ID,
    @DESC,
    @QTETOT,
    @QTETOTSECT,
    @CALCTIMSTP,
    @COUUM,
    @TEMPUNI,
    @TEMPUM,
    @DATECREE,
    @OLDESTPROD,
    @CLEPERS,
    @PROFIT,
    @COUTANTSEL,
    @COUTANT1,
    @COUTANT2,
    @COUTANT3,
    @COUTANT4,
    GETDATE())

  --Return new ID
  RETURN @@IDENTITY
END ELSE
BEGIN
  --Update data into table
  UPDATE
    SOULOTS
  SET
    [SOU_ID] = @SOU_ID,
    [LOTS_ID] = @LOTS_ID,
    [DESC] = @DESC,
    [QTETOT] = @QTETOT,
    [QTETOTSECT] = @QTETOTSECT,
    [CALCTIMSTP] = @CALCTIMSTP,
    [COUUM] = @COUUM,
    [TEMPUNI] = @TEMPUNI,
    [TEMPUM] = @TEMPUM,
    [DATECREE] = @DATECREE,
    [OLDESTPROD] = @OLDESTPROD,
    [CLEPERS] = @CLEPERS,
    [PROFIT] = @PROFIT,
    [COUTANTSEL] = @COUTANTSEL,
    [COUTANT1] = @COUTANT1,
    [COUTANT2] = @COUTANT2,
    [COUTANT3] = @COUTANT3,
    [COUTANT4] = @COUTANT4,
    SysDate = GETDATE()
  WHERE
    UniqueId = @UniqueId

    -- Mise à jour du Last user updating SOUMIS
  exec dbo.sp_Update_SoumisUseSession @SOU_ID
  
  --Return updated ID
  RETURN @UniqueId
END
GO


IF OBJECT_ID(N'dbo.up_SOULOTSCO_Update', N'P') IS NOT NULL 
    DROP PROCEDURE dbo.up_SOULOTSCO_Update ;
GO


CREATE PROCEDURE [dbo].[up_SOULOTSCO_Update] (
  @UniqueId bigint,
  @SOU_ID varchar(20),
  @LOTS_ID varchar(20),
  @PRO_ID varchar(20),
  @ORDRE varchar(6),
  @QTE float,
  @QTEUM varchar(2)
) AS

IF @UniqueId IS NULL
BEGIN
  --Insert new data into table
  INSERT INTO SOULOTSCO (
    [SOU_ID],
    [LOTS_ID],
    [PRO_ID],
    [ORDRE],
    [QTE],
    [QTEUM],
    SysDate)
  VALUES (
    @SOU_ID,
    @LOTS_ID,
    @PRO_ID,
    @ORDRE,
    @QTE,
    @QTEUM,
    GETDATE())

  --Return new ID
  RETURN @@IDENTITY
END ELSE
BEGIN
  --Update data into table
  UPDATE
    SOULOTSCO
  SET
    [SOU_ID] = @SOU_ID,
    [LOTS_ID] = @LOTS_ID,
    [PRO_ID] = @PRO_ID,
    [ORDRE] = @ORDRE,
    [QTE] = @QTE,
    [QTEUM] = @QTEUM,
    SysDate = GETDATE()
  WHERE
    UniqueId = @UniqueId

    -- Mise à jour du Last user updating SOUMIS
  exec dbo.sp_Update_SoumisUseSession @SOU_ID
  
  --Return updated ID
  RETURN @UniqueId
END
GO


IF OBJECT_ID(N'dbo.up_SOUPRO_Update', N'P') IS NOT NULL 
    DROP PROCEDURE dbo.up_SOUPRO_Update ;
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

    -- Mise à jour du Last user updating SOUMIS
  exec dbo.sp_Update_SoumisUseSession @SOU_ID
  
  --Return updated ID
  RETURN @UniqueId
END
GO


IF OBJECT_ID(N'dbo.up_SOUREL_Update', N'P') IS NOT NULL 
    DROP PROCEDURE dbo.up_SOUREL_Update ;
GO

CREATE PROCEDURE [dbo].[up_SOUREL_Update] (
  @UniqueId bigint,
  @SOU_ID varchar(20),
  @BLO_ID varchar(3),
  @DIV_ID varchar(3),
  @TYPERELEVE varchar(1),
  @EXT_ID varchar(20),
  @ORDRE varchar(6),
  @TYPEITEM varchar(1),
  @ITEM_ID varchar(20),
  @DESCR varchar(60),
  @QTE float,
  @SECTION float,
  @QTEUM varchar(2),
  @PROFIT float,
  @TYPETAXE varchar(1),
  @CODEIMPR varchar(2),
  @COUTANBRUT float,
  @TEMPSUNIT float,
  @TEMPSSEC float,
  @TEMPSUM varchar(2),
  @PROFITPLUS float,
  @PROFITMOIN float,
  @ACC_NO varchar(20),
  @ACH_NO varchar(20),
  @ACT_NO varchar(20)
) AS

IF @UniqueId IS NULL
BEGIN
  --Insert new data into table
  INSERT INTO SOUREL (
    [SOU_ID],
    [BLO_ID],
    [DIV_ID],
    [TYPERELEVE],
    [EXT_ID],
    [ORDRE],
    [TYPEITEM],
    [ITEM_ID],
    [DESCR],
    [QTE],
    [SECTION],
    [QTEUM],
    [PROFIT],
    [TYPETAXE],
    [CODEIMPR],
    [COUTANBRUT],
    [TEMPSUNIT],
    [TEMPSSEC],
    [TEMPSUM],
    [PROFITPLUS],
    [PROFITMOIN],
    [ACC_NO],
    [ACH_NO],
    [ACT_NO],
    SysDate)
  VALUES (
    @SOU_ID,
    @BLO_ID,
    @DIV_ID,
    @TYPERELEVE,
    @EXT_ID,
    @ORDRE,
    @TYPEITEM,
    @ITEM_ID,
    @DESCR,
    @QTE,
    @SECTION,
    @QTEUM,
    @PROFIT,
    @TYPETAXE,
    @CODEIMPR,
    @COUTANBRUT,
    @TEMPSUNIT,
    @TEMPSSEC,
    @TEMPSUM,
    @PROFITPLUS,
    @PROFITMOIN,
    @ACC_NO,
    @ACH_NO,
    @ACT_NO,
    GETDATE())

  --Return new ID
  RETURN @@IDENTITY
END ELSE
BEGIN
  --Update data into table
  UPDATE
    SOUREL
  SET
    [SOU_ID] = @SOU_ID,
    [BLO_ID] = @BLO_ID,
    [DIV_ID] = @DIV_ID,
    [TYPERELEVE] = @TYPERELEVE,
    [EXT_ID] = @EXT_ID,
    [ORDRE] = @ORDRE,
    [TYPEITEM] = @TYPEITEM,
    [ITEM_ID] = @ITEM_ID,
    [DESCR] = @DESCR,
    [QTE] = @QTE,
    [SECTION] = @SECTION,
    [QTEUM] = @QTEUM,
    [PROFIT] = @PROFIT,
    [TYPETAXE] = @TYPETAXE,
    [CODEIMPR] = @CODEIMPR,
    [COUTANBRUT] = @COUTANBRUT,
    [TEMPSUNIT] = @TEMPSUNIT,
    [TEMPSSEC] = @TEMPSSEC,
    [TEMPSUM] = @TEMPSUM,
    [PROFITPLUS] = @PROFITPLUS,
    [PROFITMOIN] = @PROFITMOIN,
    [ACC_NO] = @ACC_NO,
    [ACH_NO] = @ACH_NO,
    [ACT_NO] = @ACT_NO,
    SysDate = GETDATE()
  WHERE
    UniqueId = @UniqueId

    -- Mise à jour du Last user updating SOUMIS
  exec dbo.sp_Update_SoumisUseSession @SOU_ID

  --Return updated ID
  RETURN @UniqueId
END
GO


IF OBJECT_ID(N'dbo.up_SOUWEBLOG_Update', N'P') IS NOT NULL 
    DROP PROCEDURE dbo.up_SOUWEBLOG_Update ;
GO

CREATE PROCEDURE [dbo].[up_SOUWEBLOG_Update] (
  @UniqueId bigint,
  @SOU_ID varchar(20),
  @WEB_ID varchar(15),
  @TRF_DATE varchar(25),
  @RESULT varchar(10),
  @MESSAGE varchar(60)
) AS

IF @UniqueId IS NULL
BEGIN
  --Insert new data into table
  INSERT INTO SOUWEBLOG (
    [SOU_ID],
    [WEB_ID],
    [TRF_DATE],
    [RESULT],
    [MESSAGE],
    SysDate)
  VALUES (
    @SOU_ID,
    @WEB_ID,
    @TRF_DATE,
    @RESULT,
    @MESSAGE,
    GETDATE())

  --Return new ID
  RETURN @@IDENTITY
END ELSE
BEGIN
  --Update data into table
  UPDATE
    SOUWEBLOG
  SET
    [SOU_ID] = @SOU_ID,
    [WEB_ID] = @WEB_ID,
    [TRF_DATE] = @TRF_DATE,
    [RESULT] = @RESULT,
    [MESSAGE] = @MESSAGE,
    SysDate = GETDATE()
  WHERE
    UniqueId = @UniqueId

    -- Mise à jour du Last user updating SOUMIS
  exec dbo.sp_Update_SoumisUseSession @SOU_ID
  
  --Return updated ID
  RETURN @UniqueId
END
GO


IF OBJECT_ID(N'dbo.up_SOUMIS_Update', N'P') IS NOT NULL 
    DROP PROCEDURE dbo.up_SOUMIS_Update ;
GO


CREATE PROCEDURE [dbo].[up_SOUMIS_Update] (
  @UniqueId bigint,
  @SOU_ID varchar(20),
  @ORIGIN char(1),          -- 2014-07-31 EMadore V6 - Ajout  
  @ORIGINREF varchar(200),  -- 2014-07-31 EMadore V6 - Ajout  
  @EXTAPP char(1),          -- 2014-07-31 EMadore V6 - Ajout  
  @EXTFILE varchar(200),    -- 2014-07-31 EMadore V6 - Ajout  
  @NODOC varchar(12),
  @DESCDOC varchar(200),
  @DATECREE datetime,
  @DATEDOC datetime,
  @DATEEXP datetime,
  @REF_ID varchar(20),
  @STATUT int,
  @NOCOMMANDE varchar(20),
  @NOTEINTERN text,
  @CLIENTNO varchar(20),
  @CLIENTCIE varchar(50),
  @CLIENTCNT varchar(50),
  @CLIENTRUE1 varchar(50),
  @CLIENTRUE2 varchar(50),
  @CLIENTVILL varchar(40),
  @CLIENTCP varchar(7),
  @CLIENTPROV varchar(40),
  @CLIENTPAYS varchar(40),
  @CLIENTBP varchar(30),
  @CLIENTTEL1 varchar(20),
  @CLIENTTEL2 varchar(20),
  @CLIENTTEL3 varchar(20),
  @CLIENTFAX varchar(20),
  @CLIENTEMAI varchar(80),  -- 2012-01-19 EMadore V3 : Ajout
  @MEMESITE bit,
  @SITENO varchar(20),
  @SITECIE varchar(50),
  @SITECNT varchar(50),
  @SITERUE1 varchar(50),
  @SITERUE2 varchar(50),
  @SITEVILLE varchar(40),
  @SITECP varchar(7),
  @SITEPROV varchar(40),
  @SITEPAYS varchar(40),
  @SITEBP varchar(30),
  @SITETEL1 varchar(20),
  @SITETEL2 varchar(20),
  @SITETEL3 varchar(20),
  @SITEFAX varchar(20),
  @SITEEMAIL varchar(80),  -- 2012-01-19 EMadore V3 : Ajout
  @MATTOTALMD float,
  @NOTEPRINC text,
  @MATCOUTREL float,
  @MATCOUTLOT float,
  @MATVENDCAL float,
  @MATPORTTVP float,
  @SERCOUTCAL float,
  @SERVENDCAL float,
  @SERHRESCAL float,
  @SERPORTTVP float,
  @AUTCOUTCAL float,
  @AUTVENDCAL float,
  @AUTPORTTVP float,
  @OPTIONSSOM varchar(40),
  @MATCOUTMO float,
  @SERCOUTMO float,
  @AUTCOUTMO float,
  @MATADMPC float,
  @SERADMPC float,
  @AUTADMPC float,
  @MATADMMO float,
  @SERADMMO float,
  @AUTADMMO float,
  @MATPROFPC float,
  @SERPROFPC float,
  @AUTPROFPC float,
  @MATPROFMO float,
  @SERPROFMO float,
  @AUTPROFMO float,
  @GLOBAJUPC float,
  @GLOBAJUMO float,
  @GLOBEXPLIC varchar(40),
  @GLOBAJU2PC float,
  @GLOBAJU2MO float,
  @GLOBEXPL2 varchar(40),
  @OPTIONSIMP varchar(50),
  @OPIMPADJMA varchar(40),
  @OPIMPADJLA varchar(40),
  @OPIMPADJOT varchar(40),
  @NOTEBAS text,
  @MATTAXAB1 float,
  @MATTAXAB2 float,
  @MATTAXAB3 float,
  @MATTAXAB4 float,
  @MATTAXAB5 float,
  @MATTAXAB6 float,
  @SERTAXAB1 float,
  @SERTAXAB2 float,
  @SERTAXAB3 float,
  @SERTAXAB4 float,
  @SERTAXAB5 float,
  @SERTAXAB6 float,
  @AUTTAXAB1 float,
  @AUTTAXAB2 float,
  @AUTTAXAB3 float,
  @AUTTAXAB4 float,
  @AUTTAXAB5 float,
  @AUTTAXAB6 float,
  @TAXTYPCAL int,
  @AJUTAXAB1 float,
  @AJUTAXAB2 float,
  @AJUTAXAB3 float,
  @AJUTAXAB4 float,
  @AJUTAXAB5 float,
  @TOTTAXFED float,
  @TOTTAXPRV float,
  @TAX_ID varchar(20),
  @APPLIQUTVF bit,
  @APPLIQUTVP bit,
  @TVPSURCOUT bit,
  @TOTCALCULE bit,
  @CALCTIMSTP varchar(14),
  @UMPLAN varchar(2),
  @TYPEPROF varchar(1),
  @MATPROFDEF float,
  @TYPESRVPRO varchar(1),
  @TAUXMD float,
  @NUMLOTEXP float,
  @SYSTEM bit,
  @USER1 varchar(20),
  @USER2 varchar(20),
  @EST_NAME varchar(50),
  @ACCTRANSNO varchar(12),
  @PRJTRANSNO varchar(15),
  @STATUTLIBF varchar(30), 
  @STATUTLIBE varchar(30),
  @USER_ID varchar(20),
  @BRANCH_ID varchar(20),
  @OWC varchar(2)
) AS

IF @UniqueId IS NULL
BEGIN
  --Insert new data into table
  INSERT INTO SOUMIS (
    [SOU_ID],
    [ORIGIN],     -- 2014-07-31 EMadore V6 - Ajout
    [ORIGINREF],  -- 2014-07-31 EMadore V6 - Ajout
    [EXTAPP],     -- 2014-07-31 EMadore V6 - Ajout
    [EXTFILE],    -- 2014-07-31 EMadore V6 - Ajout
    [NODOC],
    [DESCDOC],
    [DATECREE],
    [DATEDOC],
    [DATEEXP],
    [REF_ID],
    [STATUT],
    [NOCOMMANDE],
    [NOTEINTERN],
    [CLIENTNO],
    [CLIENTCIE],
    [CLIENTCNT],
    [CLIENTRUE1],
    [CLIENTRUE2],
    [CLIENTVILL],
    [CLIENTCP],
    [CLIENTPROV],
    [CLIENTPAYS],
    [CLIENTBP],
    [CLIENTTEL1],
    [CLIENTTEL2],
    [CLIENTTEL3],
    [CLIENTFAX],
    [CLIENTEMAI],  -- 2012-01-19 EMadore V3 : Ajout
    [MEMESITE],
    [SITENO],
    [SITECIE],
    [SITECNT],
    [SITERUE1],
    [SITERUE2],
    [SITEVILLE],
    [SITECP],
    [SITEPROV],
    [SITEPAYS],
    [SITEBP],
    [SITETEL1],
    [SITETEL2],
    [SITETEL3],
    [SITEFAX],
    [SITEEMAIL],  -- 2012-01-19 EMadore V3 : Ajout 
    [MATTOTALMD],
    [NOTEPRINC],
    [MATCOUTREL],
    [MATCOUTLOT],
    [MATVENDCAL],
    [MATPORTTVP],
    [SERCOUTCAL],
    [SERVENDCAL],
    [SERHRESCAL],
    [SERPORTTVP],
    [AUTCOUTCAL],
    [AUTVENDCAL],
    [AUTPORTTVP],
    [OPTIONSSOM],
    [MATCOUTMO],
    [SERCOUTMO],
    [AUTCOUTMO],
    [MATADMPC],
    [SERADMPC],
    [AUTADMPC],
    [MATADMMO],
    [SERADMMO],
    [AUTADMMO],
    [MATPROFPC],
    [SERPROFPC],
    [AUTPROFPC],
    [MATPROFMO],
    [SERPROFMO],
    [AUTPROFMO],
    [GLOBAJUPC],
    [GLOBAJUMO],
    [GLOBEXPLIC],
    [GLOBAJU2PC],
    [GLOBAJU2MO],
    [GLOBEXPL2],
    [OPTIONSIMP],
    [OPIMPADJMA],
    [OPIMPADJLA],
    [OPIMPADJOT],
    [NOTEBAS],
    [MATTAXAB1],
    [MATTAXAB2],
    [MATTAXAB3],
    [MATTAXAB4],
    [MATTAXAB5],
    [MATTAXAB6],
    [SERTAXAB1],
    [SERTAXAB2],
    [SERTAXAB3],
    [SERTAXAB4],
    [SERTAXAB5],
    [SERTAXAB6],
    [AUTTAXAB1],
    [AUTTAXAB2],
    [AUTTAXAB3],
    [AUTTAXAB4],
    [AUTTAXAB5],
    [AUTTAXAB6],
    [TAXTYPCAL],
    [AJUTAXAB1],
    [AJUTAXAB2],
    [AJUTAXAB3],
    [AJUTAXAB4],
    [AJUTAXAB5],
    [TOTTAXFED],
    [TOTTAXPRV],
    [TAX_ID],
    [APPLIQUTVF],
    [APPLIQUTVP],
    [TVPSURCOUT],
    [TOTCALCULE],
    [CALCTIMSTP],
    [UMPLAN],
    [TYPEPROF],
    [MATPROFDEF],
    [TYPESRVPRO],
    [TAUXMD],
    [NUMLOTEXP],
    [SYSTEM],
    [USER1],
    [USER2],
    [EST_NAME],
    [ACCTRANSNO],
    [PRJTRANSNO],
    [STATUTLIBF], 
    [STATUTLIBE],  	
    [USER_ID],
    [BRANCH_ID], 
    [OWC], 
    SysDate)
  VALUES (
    @SOU_ID,
    @ORIGIN,    -- 2014-07-31 EMadore V6 - Ajout
    @ORIGINREF, -- 2014-07-31 EMadore V6 - Ajout
    @EXTAPP,    -- 2014-07-31 EMadore V6 - Ajout
    @EXTFILE,   -- 2014-07-31 EMadore V6 - Ajout
    @NODOC,
    @DESCDOC,
    @DATECREE,
    @DATEDOC,
    @DATEEXP,
    @REF_ID,
    @STATUT,
    @NOCOMMANDE,
    @NOTEINTERN,
    @CLIENTNO,
    @CLIENTCIE,
    @CLIENTCNT,
    @CLIENTRUE1,
    @CLIENTRUE2,
    @CLIENTVILL,
    @CLIENTCP,
    @CLIENTPROV,
    @CLIENTPAYS,
    @CLIENTBP,
    @CLIENTTEL1,
    @CLIENTTEL2,
    @CLIENTTEL3,
    @CLIENTFAX,
    @CLIENTEMAI,  -- 2012-01-19 EMadore V3 : Ajout
    @MEMESITE,
    @SITENO,
    @SITECIE,
    @SITECNT,
    @SITERUE1,
    @SITERUE2,
    @SITEVILLE,
    @SITECP,
    @SITEPROV,
    @SITEPAYS,
    @SITEBP,
    @SITETEL1,
    @SITETEL2,
    @SITETEL3,
    @SITEFAX,
    @SITEEMAIL,    -- 2012-01-19 V3 : Ajout
    @MATTOTALMD,
    @NOTEPRINC,
    @MATCOUTREL,
    @MATCOUTLOT,
    @MATVENDCAL,
    @MATPORTTVP,
    @SERCOUTCAL,
    @SERVENDCAL,
    @SERHRESCAL,
    @SERPORTTVP,
    @AUTCOUTCAL,
    @AUTVENDCAL,
    @AUTPORTTVP,
    @OPTIONSSOM,
    @MATCOUTMO,
    @SERCOUTMO,
    @AUTCOUTMO,
    @MATADMPC,
    @SERADMPC,
    @AUTADMPC,
    @MATADMMO,
    @SERADMMO,
    @AUTADMMO,
    @MATPROFPC,
    @SERPROFPC,
    @AUTPROFPC,
    @MATPROFMO,
    @SERPROFMO,
    @AUTPROFMO,
    @GLOBAJUPC,
    @GLOBAJUMO,
    @GLOBEXPLIC,
    @GLOBAJU2PC,
    @GLOBAJU2MO,
    @GLOBEXPL2,
    @OPTIONSIMP,
    @OPIMPADJMA,
    @OPIMPADJLA,
    @OPIMPADJOT,
    @NOTEBAS,
    @MATTAXAB1,
    @MATTAXAB2,
    @MATTAXAB3,
    @MATTAXAB4,
    @MATTAXAB5,
    @MATTAXAB6,
    @SERTAXAB1,
    @SERTAXAB2,
    @SERTAXAB3,
    @SERTAXAB4,
    @SERTAXAB5,
    @SERTAXAB6,
    @AUTTAXAB1,
    @AUTTAXAB2,
    @AUTTAXAB3,
    @AUTTAXAB4,
    @AUTTAXAB5,
    @AUTTAXAB6,
    @TAXTYPCAL,
    @AJUTAXAB1,
    @AJUTAXAB2,
    @AJUTAXAB3,
    @AJUTAXAB4,
    @AJUTAXAB5,
    @TOTTAXFED,
    @TOTTAXPRV,
    @TAX_ID,
    @APPLIQUTVF,
    @APPLIQUTVP,
    @TVPSURCOUT,
    @TOTCALCULE,
    @CALCTIMSTP,
    @UMPLAN,
    @TYPEPROF,
    @MATPROFDEF,
    @TYPESRVPRO,
    @TAUXMD,
    @NUMLOTEXP,
    @SYSTEM,
    @USER1,
    @USER2,
    @EST_NAME,
    @ACCTRANSNO,
    @PRJTRANSNO,
    @STATUTLIBF, 
    @STATUTLIBE,  	
    @USER_ID,
    @BRANCH_ID, 
    @OWC,
    GETDATE())

  --Return new ID
  RETURN @@IDENTITY
END ELSE
BEGIN
  --Update data into table
  UPDATE
    SOUMIS
  SET
    [SOU_ID] = @SOU_ID,
    [ORIGIN] = @ORIGIN,       -- 2014-07-31 EMadore V6 - Ajout
    [ORIGINREF] = @ORIGINREF, -- 2014-07-31 EMadore V6 - Ajout
    [EXTAPP] = @EXTAPP,       -- 2014-07-31 EMadore V6 - Ajout
    [EXTFILE] = @EXTFILE,     -- 2014-07-31 EMadore V6 - Ajout
    [NODOC] = @NODOC,
    [DESCDOC] = @DESCDOC,
    [DATECREE] = @DATECREE,
    [DATEDOC] = @DATEDOC,
    [DATEEXP] = @DATEEXP,
    [REF_ID] = @REF_ID,
    [STATUT] = @STATUT,
    [NOCOMMANDE] = @NOCOMMANDE,
    [NOTEINTERN] = @NOTEINTERN,
    [CLIENTNO] = @CLIENTNO,
    [CLIENTCIE] = @CLIENTCIE,
    [CLIENTCNT] = @CLIENTCNT,
    [CLIENTRUE1] = @CLIENTRUE1,
    [CLIENTRUE2] = @CLIENTRUE2,
    [CLIENTVILL] = @CLIENTVILL,
    [CLIENTCP] = @CLIENTCP,
    [CLIENTPROV] = @CLIENTPROV,
    [CLIENTPAYS] = @CLIENTPAYS,
    [CLIENTBP] = @CLIENTBP,
    [CLIENTTEL1] = @CLIENTTEL1,
    [CLIENTTEL2] = @CLIENTTEL2,
    [CLIENTTEL3] = @CLIENTTEL3,
    [CLIENTFAX] = @CLIENTFAX,
    [CLIENTEMAI] = @CLIENTEMAI,  -- 2012-01-19 EMadore V3 : Ajout
    [MEMESITE] = @MEMESITE,
    [SITENO] = @SITENO,
    [SITECIE] = @SITECIE,
    [SITECNT] = @SITECNT,
    [SITERUE1] = @SITERUE1,
    [SITERUE2] = @SITERUE2,
    [SITEVILLE] = @SITEVILLE,
    [SITECP] = @SITECP,
    [SITEPROV] = @SITEPROV,
    [SITEPAYS] = @SITEPAYS,
    [SITEBP] = @SITEBP,
    [SITETEL1] = @SITETEL1,
    [SITETEL2] = @SITETEL2,
    [SITETEL3] = @SITETEL3,
    [SITEFAX] = @SITEFAX,
    [SITEEMAIL] = @SITEEMAIL,   -- 2012-01-19 EMadore V3 : Ajout
    [MATTOTALMD] = @MATTOTALMD,
    [NOTEPRINC] = @NOTEPRINC,
    [MATCOUTREL] = @MATCOUTREL,
    [MATCOUTLOT] = @MATCOUTLOT,
    [MATVENDCAL] = @MATVENDCAL,
    [MATPORTTVP] = @MATPORTTVP,
    [SERCOUTCAL] = @SERCOUTCAL,
    [SERVENDCAL] = @SERVENDCAL,
    [SERHRESCAL] = @SERHRESCAL,
    [SERPORTTVP] = @SERPORTTVP,
    [AUTCOUTCAL] = @AUTCOUTCAL,
    [AUTVENDCAL] = @AUTVENDCAL,
    [AUTPORTTVP] = @AUTPORTTVP,
    [OPTIONSSOM] = @OPTIONSSOM,
    [MATCOUTMO] = @MATCOUTMO,
    [SERCOUTMO] = @SERCOUTMO,
    [AUTCOUTMO] = @AUTCOUTMO,
    [MATADMPC] = @MATADMPC,
    [SERADMPC] = @SERADMPC,
    [AUTADMPC] = @AUTADMPC,
    [MATADMMO] = @MATADMMO,
    [SERADMMO] = @SERADMMO,
    [AUTADMMO] = @AUTADMMO,
    [MATPROFPC] = @MATPROFPC,
    [SERPROFPC] = @SERPROFPC,
    [AUTPROFPC] = @AUTPROFPC,
    [MATPROFMO] = @MATPROFMO,
    [SERPROFMO] = @SERPROFMO,
    [AUTPROFMO] = @AUTPROFMO,
    [GLOBAJUPC] = @GLOBAJUPC,
    [GLOBAJUMO] = @GLOBAJUMO,
    [GLOBEXPLIC] = @GLOBEXPLIC,
    [GLOBAJU2PC] = @GLOBAJU2PC,
    [GLOBAJU2MO] = @GLOBAJU2MO,
    [GLOBEXPL2] = @GLOBEXPL2,
    [OPTIONSIMP] = @OPTIONSIMP,
    [OPIMPADJMA] = @OPIMPADJMA,
    [OPIMPADJLA] = @OPIMPADJLA,
    [OPIMPADJOT] = @OPIMPADJOT,
    [NOTEBAS] = @NOTEBAS,
    [MATTAXAB1] = @MATTAXAB1,
    [MATTAXAB2] = @MATTAXAB2,
    [MATTAXAB3] = @MATTAXAB3,
    [MATTAXAB4] = @MATTAXAB4,
    [MATTAXAB5] = @MATTAXAB5,
    [MATTAXAB6] = @MATTAXAB6,
    [SERTAXAB1] = @SERTAXAB1,
    [SERTAXAB2] = @SERTAXAB2,
    [SERTAXAB3] = @SERTAXAB3,
    [SERTAXAB4] = @SERTAXAB4,
    [SERTAXAB5] = @SERTAXAB5,
    [SERTAXAB6] = @SERTAXAB6,
    [AUTTAXAB1] = @AUTTAXAB1,
    [AUTTAXAB2] = @AUTTAXAB2,
    [AUTTAXAB3] = @AUTTAXAB3,
    [AUTTAXAB4] = @AUTTAXAB4,
    [AUTTAXAB5] = @AUTTAXAB5,
    [AUTTAXAB6] = @AUTTAXAB6,
    [TAXTYPCAL] = @TAXTYPCAL,
    [AJUTAXAB1] = @AJUTAXAB1,
    [AJUTAXAB2] = @AJUTAXAB2,
    [AJUTAXAB3] = @AJUTAXAB3,
    [AJUTAXAB4] = @AJUTAXAB4,
    [AJUTAXAB5] = @AJUTAXAB5,
    [TOTTAXFED] = @TOTTAXFED,
    [TOTTAXPRV] = @TOTTAXPRV,
    [TAX_ID] = @TAX_ID,
    [APPLIQUTVF] = @APPLIQUTVF,
    [APPLIQUTVP] = @APPLIQUTVP,
    [TVPSURCOUT] = @TVPSURCOUT,
    [TOTCALCULE] = @TOTCALCULE,
    [CALCTIMSTP] = @CALCTIMSTP,
    [UMPLAN] = @UMPLAN,
    [TYPEPROF] = @TYPEPROF,
    [MATPROFDEF] = @MATPROFDEF,
    [TYPESRVPRO] = @TYPESRVPRO,
    [TAUXMD] = @TAUXMD,
    [NUMLOTEXP] = @NUMLOTEXP,
    [SYSTEM] = @SYSTEM,
    [USER1] = @USER1,
    [USER2] = @USER2,
    [EST_NAME] = @EST_NAME,
    [ACCTRANSNO] = @ACCTRANSNO,
    [PRJTRANSNO] = @PRJTRANSNO,
    [STATUTLIBF]  = @STATUTLIBF,
    [STATUTLIBE]  = @STATUTLIBE,	
    [USER_ID] = @USER_ID,
    [BRANCH_ID]  = @BRANCH_ID,
    [OWC]  = @OWC,	
    SysDate = GETDATE()
  WHERE
    UniqueId = @UniqueId

    -- Mise à jour du Last user updating SOUMIS
  exec dbo.sp_Update_SoumisUseSession @SOU_ID	

  --Return updated ID
  RETURN @UniqueId
END
GO

-----------------------

IF OBJECT_ID(N'dbo.up_SOUAMD_Delete', N'P') IS NOT NULL 
    DROP PROCEDURE dbo.up_SOUAMD_Delete ;
GO

CREATE PROCEDURE [dbo].[up_SOUAMD_Delete] (
  @UniqueId bigint
) AS

DECLARE @SOU_ID	VARCHAR(20)
SELECT @SOU_ID = D.SOU_ID FROM SOUAMD D WHERE D.UniqueId = @UniqueId

DELETE FROM SOUAMD WHERE UniqueId = @UniqueId


  -- Mise à jour du Last user updating SOUMIS
exec dbo.sp_Update_SoumisUseSession @SOU_ID	
GO


IF OBJECT_ID(N'dbo.up_SOUBLO_Delete', N'P') IS NOT NULL 
    DROP PROCEDURE dbo.up_SOUBLO_Delete ;
GO

CREATE PROCEDURE [dbo].[up_SOUBLO_Delete] (
  @UniqueId bigint
) AS

DECLARE @SOU_ID	VARCHAR(20)
SELECT @SOU_ID = D.SOU_ID FROM SOUBLO D WHERE D.UniqueId = @UniqueId

DELETE FROM SOUBLO WHERE UniqueId = @UniqueId


  -- Mise à jour du Last user updating SOUMIS
exec dbo.sp_Update_SoumisUseSession @SOU_ID	
GO


IF OBJECT_ID(N'dbo.[up_SOUDIV_Delete]', N'P') IS NOT NULL 
    DROP PROCEDURE dbo.[up_SOUDIV_Delete] ;
GO

CREATE PROCEDURE [dbo].[up_SOUDIV_Delete] (
  @UniqueId bigint
) AS

DECLARE @SOU_ID	VARCHAR(20)
SELECT @SOU_ID = D.SOU_ID FROM SOUDIV D WHERE D.UniqueId = @UniqueId

DELETE FROM SOUDIV WHERE UniqueId = @UniqueId


  -- Mise à jour du Last user updating SOUMIS
exec dbo.sp_Update_SoumisUseSession @SOU_ID	
GO

IF OBJECT_ID(N'dbo.[up_SOUENS_Delete]', N'P') IS NOT NULL 
    DROP PROCEDURE dbo.[up_SOUENS_Delete] ;
GO

CREATE PROCEDURE [dbo].[up_SOUENS_Delete] (
  @UniqueId bigint
) AS

DECLARE @SOU_ID	VARCHAR(20)
SELECT @SOU_ID = D.SOU_ID FROM SOUENS D WHERE D.UniqueId = @UniqueId

DELETE FROM SOUENS WHERE UniqueId = @UniqueId


  -- Mise à jour du Last user updating SOUMIS
exec dbo.sp_Update_SoumisUseSession @SOU_ID	
GO


IF OBJECT_ID(N'dbo.[up_SOUENSCO_Delete]', N'P') IS NOT NULL 
    DROP PROCEDURE dbo.[up_SOUENSCO_Delete] ;
GO

CREATE PROCEDURE [dbo].[up_SOUENSCO_Delete] (
  @UniqueId bigint
) AS

DECLARE @SOU_ID	VARCHAR(20)
SELECT @SOU_ID = D.SOU_ID FROM SOUENSCO D WHERE D.UniqueId = @UniqueId

DELETE FROM SOUENSCO WHERE UniqueId = @UniqueId


  -- Mise à jour du Last user updating SOUMIS
exec dbo.sp_Update_SoumisUseSession @SOU_ID	
GO

IF OBJECT_ID(N'dbo.[up_SOULOTS_Delete]', N'P') IS NOT NULL 
    DROP PROCEDURE dbo.[up_SOULOTS_Delete] ;
GO

CREATE PROCEDURE [dbo].[up_SOULOTS_Delete] (
  @UniqueId bigint
) AS

DECLARE @SOU_ID	VARCHAR(20)
SELECT @SOU_ID = D.SOU_ID FROM SOULOTS D WHERE D.UniqueId = @UniqueId

DELETE FROM SOULOTS WHERE UniqueId = @UniqueId


  -- Mise à jour du Last user updating SOUMIS
exec dbo.sp_Update_SoumisUseSession @SOU_ID	
GO

IF OBJECT_ID(N'dbo.[up_SOULOTSCO_Delete]', N'P') IS NOT NULL 
    DROP PROCEDURE dbo.[up_SOULOTSCO_Delete] ;
GO

CREATE PROCEDURE [dbo].[up_SOULOTSCO_Delete] (
  @UniqueId bigint
) AS

DECLARE @SOU_ID	VARCHAR(20)
SELECT @SOU_ID = D.SOU_ID FROM SOULOTSCO D WHERE D.UniqueId = @UniqueId

DELETE FROM SOULOTSCO WHERE UniqueId = @UniqueId


  -- Mise à jour du Last user updating SOUMIS
exec dbo.sp_Update_SoumisUseSession @SOU_ID	
GO

IF OBJECT_ID(N'dbo.[up_SOUPRO_Delete]', N'P') IS NOT NULL 
    DROP PROCEDURE dbo.[up_SOUPRO_Delete] ;
GO

CREATE PROCEDURE [dbo].[up_SOUPRO_Delete] (
  @UniqueId bigint
) AS

DECLARE @SOU_ID	VARCHAR(20)
SELECT @SOU_ID = D.SOU_ID FROM SOUPRO D WHERE D.UniqueId = @UniqueId

DELETE FROM SOUPRO WHERE UniqueId = @UniqueId


  -- Mise à jour du Last user updating SOUMIS
exec dbo.sp_Update_SoumisUseSession @SOU_ID	
GO


IF OBJECT_ID(N'dbo.[up_SOUREL_Delete]', N'P') IS NOT NULL 
    DROP PROCEDURE dbo.[up_SOUREL_Delete] ;
GO

CREATE PROCEDURE [dbo].[up_SOUREL_Delete] (
  @UniqueId bigint
) AS

DECLARE @SOU_ID	VARCHAR(20)
SELECT @SOU_ID = D.SOU_ID FROM SOUREL D WHERE D.UniqueId = @UniqueId

DELETE FROM SOUREL WHERE UniqueId = @UniqueId


  -- Mise à jour du Last user updating SOUMIS
exec dbo.sp_Update_SoumisUseSession @SOU_ID	
GO

IF OBJECT_ID(N'dbo.[up_SOUWEBLOGL_Delete]', N'P') IS NOT NULL 
    DROP PROCEDURE dbo.[up_SOUWEBLOGL_Delete] ;
GO

CREATE PROCEDURE [dbo].[up_SOUWEBLOGL_Delete] (
  @UniqueId bigint
) AS

DECLARE @SOU_ID	VARCHAR(20)
SELECT @SOU_ID = D.SOU_ID FROM SOUWEBLOG D WHERE D.UniqueId = @UniqueId

DELETE FROM SOUWEBLOG WHERE UniqueId = @UniqueId


  -- Mise à jour du Last user updating SOUMIS
exec dbo.sp_Update_SoumisUseSession @SOU_ID	
GO
