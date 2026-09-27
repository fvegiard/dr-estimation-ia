-- EULA START --------------------------------------------------------------------------

IF NOT EXISTS (SELECT * FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = 'EULA')
BEGIN
  CREATE TABLE [dbo].EULA (
	  UniqueId  bigint      IDENTITY(1,1) NOT NULL,
    ULA_ID    varchar(20) NOT NULL,
    DATESTART datetime    NOT NULL,
    TEXT_EN   text,
    TEXT_FR   text,
    [SysDate] datetime    NOT NULL DEFAULT (getdate()),
    )
END
GO

IF EXISTS (SELECT * FROM INFORMATION_SCHEMA.TABLE_CONSTRAINTS WHERE TABLE_NAME = 'EULA' AND CONSTRAINT_NAME = 'PK_EULA')
BEGIN
  ALTER TABLE EULA DROP CONSTRAINT PK_EULA
END
GO

ALTER TABLE EULA ADD CONSTRAINT
  PK_EULA PRIMARY KEY CLUSTERED 
  (
  ULA_ID
  ) WITH( STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
GO

IF EXISTS (SELECT * FROM INFORMATION_SCHEMA.ROUTINES WHERE Routine_Type = 'PROCEDURE' AND Specific_Name = 'up_EULA_Update')
  DROP PROCEDURE up_EULA_Update
GO

CREATE PROCEDURE [dbo].[up_EULA_Update] (
  @UniqueId   bigint,
  @ULA_ID     varchar(20),
  @DATESTART  datetime,
  @TEXT_EN    text,
  @TEXT_FR    text
) AS

IF @UniqueId IS NULL
BEGIN
  --Insert new data into table
  INSERT INTO EULA (
    [ULA_ID],
    [DATESTART],
    [TEXT_EN], 
    [TEXT_FR], 
    SysDate)
  VALUES (
    @ULA_ID,
    @DATESTART,
    @TEXT_EN,
    @TEXT_FR,
    GETDATE())

  --Return new ID
  RETURN @@IDENTITY
END ELSE
BEGIN
  --Update data into table
  UPDATE
    EULA
  SET
    [ULA_ID]    = @ULA_ID,
    [DATESTART] = @DATESTART,
    [TEXT_EN]   = @TEXT_EN,
    [TEXT_FR]   = @TEXT_FR,
    SysDate     = GETDATE()
  WHERE
    UniqueId = @UniqueId

  --Return updated ID
  RETURN @UniqueId
END
GO

-- EULA END --------------------------------------------------------------------------


-- EULAUSER START --------------------------------------------------------------------------


IF NOT EXISTS (SELECT * FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = 'EULAUSER')
BEGIN
  CREATE TABLE [dbo].EULAUSER (
	  UniqueId    bigint      IDENTITY(1,1) NOT NULL,
    ULA_ID      varchar(20) NOT NULL,
    DATEACCEPT  datetime    NOT NULL,
    [USER]      varchar(64) NOT NULL,
    [SysDate]   datetime    NOT NULL DEFAULT (getdate()),
    )
END
GO

IF EXISTS (SELECT * FROM INFORMATION_SCHEMA.TABLE_CONSTRAINTS WHERE TABLE_NAME = 'EULAUSER' AND CONSTRAINT_NAME = 'PK_EULAUSER')
BEGIN
  ALTER TABLE EULAUSER DROP CONSTRAINT PK_EULAUSER
END
GO

ALTER TABLE EULAUSER ADD CONSTRAINT
  PK_EULAUSER PRIMARY KEY CLUSTERED 
  (
  ULA_ID,
  [USER]
  ) WITH( STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
GO

IF EXISTS (SELECT * FROM INFORMATION_SCHEMA.ROUTINES WHERE Routine_Type = 'PROCEDURE' AND Specific_Name = 'up_EULAUSER_Update')
  DROP PROCEDURE up_EULAUSER_Update
GO

CREATE PROCEDURE [dbo].[up_EULAUSER_Update] (
  @UniqueId   bigint,
  @ULA_ID     varchar(20),
  @DATEACCEPT datetime,
  @USER       varchar(64)
) AS

IF @UniqueId IS NULL
BEGIN
  --Insert new data into table
  INSERT INTO EULAUSER (
    [ULA_ID],
    [DATEACCEPT],
    [USER], 
    SysDate)
  VALUES (
    @ULA_ID,
    @DATEACCEPT,
    @USER,
    GETDATE())

  --Return new ID
  RETURN @@IDENTITY
END ELSE
BEGIN
  --Update data into table
  UPDATE
    EULAUSER
  SET
    [ULA_ID]      = @ULA_ID,
    [DATEACCEPT]  = @DATEACCEPT,
    [USER]        = @USER,
    SysDate = GETDATE()
  WHERE
    UniqueId = @UniqueId

  --Return updated ID
  RETURN @UniqueId
END
GO

  -- New field - DEFBLO.ACC_NO
IF NOT EXISTS (
  SELECT 
    TOP 1 *
  FROM 
    INFORMATION_SCHEMA.COLUMNS
  WHERE 
        [TABLE_NAME]  = 'DEFBLO'
    AND [COLUMN_NAME] = 'ACC_NO' )
BEGIN
  ALTER TABLE
    DEFBLO
  ADD
    ACC_NO VARCHAR(20)
END
GO

IF EXISTS (SELECT * FROM INFORMATION_SCHEMA.ROUTINES WHERE Routine_Type = 'PROCEDURE' AND Specific_Name = 'up_DEFBLO_Update')
  DROP PROCEDURE up_DEFBLO_Update
GO

CREATE PROCEDURE [dbo].[up_DEFBLO_Update] (
  @UniqueId bigint,
  @ORDRE varchar(6),
  @DESC varchar(40),
  @MULT int,
  @INCLSOU bit,
  @INCLFAC bit,
  @ACC_NO VARCHAR(20),
  @SYSTEM bit
) AS

IF @UniqueId IS NULL
BEGIN
  --Insert new data into table
  INSERT INTO DEFBLO (
    [ORDRE],
    [DESC],
    [MULT],
    [INCLSOU],
    [INCLFAC],
    [ACC_NO],
    [SYSTEM],
    SysDate)
  VALUES (
    @ORDRE,
    @DESC,
    @MULT,
    @INCLSOU,
    @INCLFAC,
    @ACC_NO,
    @SYSTEM,
    GETDATE())

  --Return new ID
  RETURN @@IDENTITY
END ELSE
BEGIN
  --Update data into table
  UPDATE
    DEFBLO
  SET
    [ORDRE] = @ORDRE,
    [DESC] = @DESC,
    [MULT] = @MULT,
    [INCLSOU] = @INCLSOU,
    [INCLFAC] = @INCLFAC,
    [ACC_NO] = @ACC_NO,
    [SYSTEM] = @SYSTEM,
    SysDate = GETDATE()
  WHERE
    UniqueId = @UniqueId

  --Return updated ID
  RETURN @UniqueId
END
GO

  -- New field - FRAIS.ACC_NO
IF NOT EXISTS (
  SELECT 
    TOP 1 *
  FROM 
    INFORMATION_SCHEMA.COLUMNS
  WHERE 
        [TABLE_NAME]  = 'FRAIS'
    AND [COLUMN_NAME] = 'ACC_NO' )
BEGIN
  ALTER TABLE
    FRAIS
  ADD
    ACC_NO VARCHAR(20)
END
GO

IF EXISTS (SELECT * FROM INFORMATION_SCHEMA.ROUTINES WHERE Routine_Type = 'PROCEDURE' AND Specific_Name = 'up_FRAIS_Update')
  DROP PROCEDURE up_FRAIS_Update
GO

CREATE PROCEDURE [dbo].[up_FRAIS_Update] (
  @UniqueId bigint,
  @ORDRE varchar(6),
  @DESCFRAIS varchar(50),
  @COUTUNI float,
  @FRAISUM varchar(2),
  @PROFIT float,
  @INCLSOU bit,
  @INCLFAC bit,
  @ACC_NO varchar (20),
  @SYSTEM bit
) AS

IF @UniqueId IS NULL
BEGIN
  --Insert new data into table
  INSERT INTO FRAIS (
    [ORDRE],
    [DESCFRAIS],
    [COUTUNI],
    [FRAISUM],
    [PROFIT],
    [INCLSOU],
    [INCLFAC],
    [ACC_NO],
    [SYSTEM],
    SysDate)
  VALUES (
    @ORDRE,
    @DESCFRAIS,
    @COUTUNI,
    @FRAISUM,
    @PROFIT,
    @INCLSOU,
    @INCLFAC,
    @ACC_NO,
    @SYSTEM,
    GETDATE())

  --Return new ID
  RETURN @@IDENTITY
END ELSE
BEGIN
  --Update data into table
  UPDATE
    FRAIS
  SET
    [ORDRE] = @ORDRE,
    [DESCFRAIS] = @DESCFRAIS,
    [COUTUNI] = @COUTUNI,
    [FRAISUM] = @FRAISUM,
    [PROFIT] = @PROFIT,
    [INCLSOU] = @INCLSOU,
    [INCLFAC] = @INCLFAC,
    [ACC_NO] = @ACC_NO,
    [SYSTEM] = @SYSTEM,
    SysDate = GETDATE()
  WHERE
    UniqueId = @UniqueId

  --Return updated ID
  RETURN @UniqueId
END
GO

  -- New field - TAUX.ACC_NO
IF NOT EXISTS (
  SELECT 
    TOP 1 *
  FROM 
    INFORMATION_SCHEMA.COLUMNS
  WHERE 
        [TABLE_NAME]  = 'TAUX'
    AND [COLUMN_NAME] = 'ACC_NO' )
BEGIN
  ALTER TABLE
    TAUX
  ADD
    ACC_NO VARCHAR(20)
END
GO

IF EXISTS (SELECT * FROM INFORMATION_SCHEMA.ROUTINES WHERE Routine_Type = 'PROCEDURE' AND Specific_Name = 'up_TAUX_Update')
  DROP PROCEDURE up_TAUX_Update
GO

CREATE PROCEDURE [dbo].[up_TAUX_Update] (
  @UniqueId bigint,
  @ORDRE varchar(6),
  @DESCTAUX varchar(50),
  @COUTUNI float,
  @PROFIT float,
  @INCLSOU bit,
  @INCLFAC bit,
  @ACC_NO varchar(20),
  @SYSTEM bit
) AS

IF @UniqueId IS NULL
BEGIN
  --Insert new data into table
  INSERT INTO TAUX (
    [ORDRE],
    [DESCTAUX],
    [COUTUNI],
    [PROFIT],
    [INCLSOU],
    [INCLFAC],
    [ACC_NO],
    [SYSTEM],
    SysDate)
  VALUES (
    @ORDRE,
    @DESCTAUX,
    @COUTUNI,
    @PROFIT,
    @INCLSOU,
    @INCLFAC,
    @ACC_NO,
    @SYSTEM,
    GETDATE())

  --Return new ID
  RETURN @@IDENTITY
END ELSE
BEGIN
  --Update data into table
  UPDATE
    TAUX
  SET
    [ORDRE] = @ORDRE,
    [DESCTAUX] = @DESCTAUX,
    [COUTUNI] = @COUTUNI,
    [PROFIT] = @PROFIT,
    [INCLSOU] = @INCLSOU,
    [INCLFAC] = @INCLFAC,
    [ACC_NO] = @ACC_NO,
    [SYSTEM] = @SYSTEM,
    SysDate = GETDATE()
  WHERE
    UniqueId = @UniqueId

  --Return updated ID
  RETURN @UniqueId
END
GO

  -- New field - SOUBLO.ACC_NO
IF NOT EXISTS (
  SELECT 
    TOP 1 *
  FROM 
    INFORMATION_SCHEMA.COLUMNS
  WHERE 
        [TABLE_NAME]  = 'SOUBLO'
    AND [COLUMN_NAME] = 'ACC_NO' )
BEGIN
  ALTER TABLE
    SOUBLO
  ADD
    ACC_NO VARCHAR(20)
END
GO


IF EXISTS (SELECT * FROM INFORMATION_SCHEMA.ROUTINES WHERE Routine_Type = 'PROCEDURE' AND Specific_Name = 'up_SOUBLO_Update')
  DROP PROCEDURE up_SOUBLO_Update
GO

CREATE PROCEDURE [dbo].[up_SOUBLO_Update] (
  @UniqueId bigint,
  @SOU_ID varchar(20),
  @BLO_ID varchar(3),
  @DESC varchar(40),
  @ACC_NO varchar(20),
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
    [MULT],
    SysDate)
  VALUES (
    @SOU_ID,
    @BLO_ID,
    @DESC,
    @ACC_NO,
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
    [MULT] = @MULT,
    SysDate = GETDATE()
  WHERE
    UniqueId = @UniqueId

  --Return updated ID
  RETURN @UniqueId
END
GO

  -- New field - FACBLO.ACC_NO
IF NOT EXISTS (
  SELECT 
    TOP 1 *
  FROM 
    INFORMATION_SCHEMA.COLUMNS
  WHERE 
        [TABLE_NAME]  = 'FACBLO'
    AND [COLUMN_NAME] = 'ACC_NO' )
BEGIN
  ALTER TABLE
    FACBLO
  ADD
    ACC_NO VARCHAR(20)
END
GO

IF EXISTS (SELECT * FROM INFORMATION_SCHEMA.ROUTINES WHERE Routine_Type = 'PROCEDURE' AND Specific_Name = 'up_FACBLO_Update')
  DROP PROCEDURE up_FACBLO_Update
GO

CREATE PROCEDURE [dbo].[up_FACBLO_Update] (
  @UniqueId bigint,
  @SOU_ID varchar(20),
  @BLO_ID varchar(3),
  @DESC varchar(40),
  @ACC_NO varchar(20),
  @MULT int
) AS

IF @UniqueId IS NULL
BEGIN
  --Insert new data into table
  INSERT INTO FACBLO (
    [SOU_ID],
    [BLO_ID],
    [DESC],
    [ACC_NO],
    [MULT],
    SysDate)
  VALUES (
    @SOU_ID,
    @BLO_ID,
    @DESC,
    @ACC_NO,
    @MULT,
    GETDATE())

  --Return new ID
  RETURN @@IDENTITY
END ELSE
BEGIN
  --Update data into table
  UPDATE
    FACBLO
  SET
    [SOU_ID] = @SOU_ID,
    [BLO_ID] = @BLO_ID,
    [DESC] = @DESC,
    [ACC_NO] = @ACC_NO,
    [MULT] = @MULT,
    SysDate = GETDATE()
  WHERE
    UniqueId = @UniqueId

  --Return updated ID
  RETURN @UniqueId
END
GO

  -- New field - SOUREL.ACC_NO
IF NOT EXISTS (
  SELECT 
    TOP 1 *
  FROM 
    INFORMATION_SCHEMA.COLUMNS
  WHERE 
        [TABLE_NAME]  = 'SOUREL'
    AND [COLUMN_NAME] = 'ACC_NO' )
BEGIN
  ALTER TABLE
    SOUREL
  ADD
    ACC_NO VARCHAR(20)
END
GO

IF EXISTS (SELECT * FROM INFORMATION_SCHEMA.ROUTINES WHERE Routine_Type = 'PROCEDURE' AND Specific_Name = 'up_SOUREL_Update')
  DROP PROCEDURE up_SOUREL_Update
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
  @ACC_NO varchar(20)
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
    SysDate = GETDATE()
  WHERE
    UniqueId = @UniqueId

  --Return updated ID
  RETURN @UniqueId
END
GO

  -- New field - FACREL.ACC_NO
IF NOT EXISTS (
  SELECT 
    TOP 1 *
  FROM 
    INFORMATION_SCHEMA.COLUMNS
  WHERE 
        [TABLE_NAME]  = 'FACREL'
    AND [COLUMN_NAME] = 'ACC_NO' )
BEGIN
  ALTER TABLE
    FACREL
  ADD
    ACC_NO VARCHAR(20)
END
GO

IF EXISTS (SELECT * FROM INFORMATION_SCHEMA.ROUTINES WHERE Routine_Type = 'PROCEDURE' AND Specific_Name = 'up_FACREL_Update')
  DROP PROCEDURE up_FACREL_Update
GO

CREATE PROCEDURE [dbo].[up_FACREL_Update] (
  @UniqueId bigint,
  @SOU_ID varchar(20),
  @BLO_ID varchar(3),
  @DIV_ID varchar(3),
  @TYPERELEVE varchar(1),
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
  @ACC_NO char(20)
) AS

IF @UniqueId IS NULL
BEGIN
  --Insert new data into table
  INSERT INTO FACREL (
    [SOU_ID],
    [BLO_ID],
    [DIV_ID],
    [TYPERELEVE],
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
    SysDate)
  VALUES (
    @SOU_ID,
    @BLO_ID,
    @DIV_ID,
    @TYPERELEVE,
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
    GETDATE())

  --Return new ID
  RETURN @@IDENTITY
END ELSE
BEGIN
  --Update data into table
  UPDATE
    FACREL
  SET
    [SOU_ID] = @SOU_ID,
    [BLO_ID] = @BLO_ID,
    [DIV_ID] = @DIV_ID,
    [TYPERELEVE] = @TYPERELEVE,
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
    SysDate = GETDATE()
  WHERE
    UniqueId = @UniqueId

  --Return updated ID
  RETURN @UniqueId
END
GO

  -- New field - CLITAUX.ACC_NO
IF NOT EXISTS (
  SELECT 
    TOP 1 *
  FROM 
    INFORMATION_SCHEMA.COLUMNS
  WHERE 
        [TABLE_NAME]  = 'CLITAUX'
    AND [COLUMN_NAME] = 'ACC_NO' )
BEGIN
  ALTER TABLE
    CLITAUX
  ADD
    ACC_NO VARCHAR(20)
END
GO

IF EXISTS (SELECT * FROM INFORMATION_SCHEMA.ROUTINES WHERE Routine_Type = 'PROCEDURE' AND Specific_Name = 'up_CLITAUX_Update')
  DROP PROCEDURE up_CLITAUX_Update
GO

CREATE PROCEDURE [dbo].[up_CLITAUX_Update] (
  @UniqueId bigint,
  @CLI_ID varchar(20),
  @ORDRE varchar(6),
  @DESCTAUX varchar(50),
  @COUTUNI float,
  @PROFIT float,
  @ACC_NO varchar(20)
) AS

IF @UniqueId IS NULL
BEGIN
  --Insert new data into table
  INSERT INTO CLITAUX (
    [CLI_ID],
    [ORDRE],
    [DESCTAUX],
    [COUTUNI],
    [PROFIT],
    [ACC_NO],
    SysDate)
  VALUES (
    @CLI_ID,
    @ORDRE,
    @DESCTAUX,
    @COUTUNI,
    @PROFIT,
    @ACC_NO,
    GETDATE())

  --Return new ID
  RETURN @@IDENTITY
END ELSE
BEGIN
  --Update data into table
  UPDATE
    CLITAUX
  SET
    [CLI_ID] = @CLI_ID,
    [ORDRE] = @ORDRE,
    [DESCTAUX] = @DESCTAUX,
    [COUTUNI] = @COUTUNI,
    [PROFIT] = @PROFIT,
    [ACC_NO] = @ACC_NO,
    SysDate = GETDATE()
  WHERE
    UniqueId = @UniqueId

  --Return updated ID
  RETURN @UniqueId
END
GO


  -- New field - SOUMIS.PRJTRANSNO
IF NOT EXISTS (
  SELECT 
    TOP 1 *
  FROM 
    INFORMATION_SCHEMA.COLUMNS
  WHERE 
        [TABLE_NAME]  = 'SOUMIS'
    AND [COLUMN_NAME] = 'PRJTRANSNO' )
BEGIN
  ALTER TABLE
    SOUMIS
  ADD
    PRJTRANSNO VARCHAR(15)
END
GO

IF EXISTS (SELECT * FROM INFORMATION_SCHEMA.ROUTINES WHERE Routine_Type = 'PROCEDURE' AND Specific_Name = 'up_SOUMIS_Update')
  DROP PROCEDURE up_SOUMIS_Update
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
  @PRJTRANSNO varchar(15)
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
    SysDate = GETDATE()
  WHERE
    UniqueId = @UniqueId

  --Return updated ID
  RETURN @UniqueId
END
GO

  -- New field - FACTURES.PRJTRANSNO
IF NOT EXISTS (
  SELECT 
    TOP 1 *
  FROM 
    INFORMATION_SCHEMA.COLUMNS
  WHERE 
        [TABLE_NAME]  = 'FACTURES'
    AND [COLUMN_NAME] = 'PRJTRANSNO' )
BEGIN
  ALTER TABLE
    FACTURES
  ADD
    PRJTRANSNO VARCHAR(15)
END
GO

IF EXISTS (SELECT * FROM INFORMATION_SCHEMA.ROUTINES WHERE Routine_Type = 'PROCEDURE' AND Specific_Name = 'up_FACTURES_Update')
  DROP PROCEDURE up_FACTURES_Update
GO

CREATE PROCEDURE [dbo].[up_FACTURES_Update] (
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
  @CLIENTEMAI varchar(80),  -- 2012-01-19 EMadore V3 - Ajout
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
  @SITEEMAIL varchar(80),  -- 2012-01-19 EMadore V3 - Ajout
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
  @PRJTRANSNO varchar(15)
) AS

IF @UniqueId IS NULL
BEGIN
  --Insert new data into table
  INSERT INTO FACTURES (
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
    [CLIENTEMAI],   -- 2012-01-19 EMadore V3 : Ajout
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
    [SITEEMAIL],    -- 2012-01-19 EMadore V3 - Ajout
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
    @CLIENTEMAI,   -- 2012-01-19 EMadore V3 : Ajout
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
    @SITEEMAIL,   -- 2012-01-19 EMadore V3 : Ajout
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
    GETDATE())

  --Return new ID
  RETURN @@IDENTITY
END ELSE
BEGIN
  --Update data into table
  UPDATE
    FACTURES
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
    [CLIENTEMAI] = @CLIENTEMAI,   -- 2012-01-19 EMadore V3 : Ajout
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
    [SITEEMAIL] = @SITEEMAIL,  -- 2012-01-19 EMAdore V3 : Ajout
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
    SysDate = GETDATE()
  WHERE
    UniqueId = @UniqueId

  --Return updated ID
  RETURN @UniqueId
END
GO

  -- New field - BDEE.MODULES
IF NOT EXISTS (
  SELECT 
    TOP 1 *
  FROM 
    INFORMATION_SCHEMA.COLUMNS
  WHERE 
        [TABLE_NAME]  = 'BDEE'
    AND [COLUMN_NAME] = 'MODULES' )
BEGIN
  ALTER TABLE
    BDEE
  ADD
    MODULES VARCHAR(32)
END
GO

  -- New field - BDEE.ORDERURLFR
IF NOT EXISTS (
  SELECT 
    TOP 1 *
  FROM 
    INFORMATION_SCHEMA.COLUMNS
  WHERE 
        [TABLE_NAME]  = 'BDEE'
    AND [COLUMN_NAME] = 'ORDERURLFR' )
BEGIN
  ALTER TABLE
    BDEE
  ADD
    ORDERURLFR VARCHAR(200)
END
GO

  -- New field - BDEE.ORDERURLEN
IF NOT EXISTS (
  SELECT 
    TOP 1 *
  FROM 
    INFORMATION_SCHEMA.COLUMNS
  WHERE 
        [TABLE_NAME]  = 'BDEE'
    AND [COLUMN_NAME] = 'ORDERURLEN' )
BEGIN
  ALTER TABLE
    BDEE
  ADD
    ORDERURLEN VARCHAR(200)
END
GO

  -- New field - BDEE.PRICEURL
IF NOT EXISTS (
  SELECT 
    TOP 1 *
  FROM 
    INFORMATION_SCHEMA.COLUMNS
  WHERE 
        [TABLE_NAME]  = 'BDEE'
    AND [COLUMN_NAME] = 'PRICEURL' )
BEGIN
  ALTER TABLE
    BDEE
  ADD
    PRICEURL VARCHAR(200)
END
GO

  -- New field - BDEE.AUTHURL
IF NOT EXISTS (
  SELECT 
    TOP 1 *
  FROM 
    INFORMATION_SCHEMA.COLUMNS
  WHERE 
        [TABLE_NAME]  = 'BDEE'
    AND [COLUMN_NAME] = 'AUTHURL' )
BEGIN
  ALTER TABLE
    BDEE
  ADD
    AUTHURL VARCHAR(200)
END
GO


  -- New field - BDEE.AUTHGLOKEY
IF NOT EXISTS (
  SELECT 
    TOP 1 *
  FROM 
    INFORMATION_SCHEMA.COLUMNS
  WHERE 
        [TABLE_NAME]  = 'BDEE'
    AND [COLUMN_NAME] = 'AUTHGLOKEY' )
BEGIN
  ALTER TABLE
    BDEE
  ADD
    AUTHGLOKEY VARCHAR(64)
END
GO

  -- New field - BDEE.AUTHCLIKEY
IF NOT EXISTS (
  SELECT 
    TOP 1 *
  FROM 
    INFORMATION_SCHEMA.COLUMNS
  WHERE 
        [TABLE_NAME]  = 'BDEE'
    AND [COLUMN_NAME] = 'AUTHCLIKEY' )
BEGIN
  ALTER TABLE
    BDEE
  ADD
    AUTHCLIKEY VARCHAR(64)
END
GO

  -- New field - BDEE.URLMODE
IF NOT EXISTS (
  SELECT 
    TOP 1 *
  FROM 
    INFORMATION_SCHEMA.COLUMNS
  WHERE 
        [TABLE_NAME]  = 'BDEE'
    AND [COLUMN_NAME] = 'URLMODE' )
BEGIN
  ALTER TABLE
    BDEE
  ADD
    URLMODE CHAR(1)
END
GO

IF EXISTS (SELECT * FROM INFORMATION_SCHEMA.ROUTINES WHERE Routine_Type = 'PROCEDURE' AND Specific_Name = 'up_BDEE_Update')
  DROP PROCEDURE up_BDEE_Update
GO

CREATE PROCEDURE [dbo].[up_BDEE_Update] (
  @UniqueId bigint,
  @LVERSION	  int,
  @CODEVER	  varchar(20),
  @DATA       varchar(30),
  @NODIST	    varchar(6),
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

IF NOT EXISTS (
  SELECT 
    TOP 1 *
  FROM 
    INFORMATION_SCHEMA.COLUMNS
  WHERE 
        [TABLE_NAME]  = 'DEFDIV'
    AND [COLUMN_NAME] = 'ACT_NO' )
BEGIN
  ALTER TABLE
    DEFDIV
  ADD
    ACT_NO VARCHAR(20)
END
GO

IF EXISTS (SELECT * FROM INFORMATION_SCHEMA.ROUTINES WHERE Routine_Type = 'PROCEDURE' AND Specific_Name = 'up_DEFDIV_Update')
  DROP PROCEDURE up_DEFDIV_Update
GO

CREATE PROCEDURE [dbo].[up_DEFDIV_Update] (
  @UniqueId bigint,
  @ORDRE varchar(6),
  @DESC varchar(40),
  @INCLSOU bit,
  @INCLFAC bit,
  @ACT_NO VARCHAR(20),
  @SYSTEM bit
) AS

IF @UniqueId IS NULL
BEGIN
  --Insert new data into table
  INSERT INTO DEFDIV (
    [ORDRE],
    [DESC],
    [INCLSOU],
    [INCLFAC],
    [ACT_NO],
    [SYSTEM],
    SysDate)
  VALUES (
    @ORDRE,
    @DESC,
    @INCLSOU,
    @INCLFAC,
    @ACT_NO,
    @SYSTEM,
    GETDATE())

  --Return new ID
  RETURN @@IDENTITY
END ELSE
BEGIN
  --Update data into table
  UPDATE
    DEFDIV
  SET
    [ORDRE]   = @ORDRE,
    [DESC]    = @DESC,
    [INCLSOU] = @INCLSOU,
    [INCLFAC] = @INCLFAC,
    [ACT_NO]  = @ACT_NO,
    [SYSTEM]  = @SYSTEM,
    SysDate   = GETDATE()
  WHERE
    UniqueId = @UniqueId

  --Return updated ID
  RETURN @UniqueId
END
GO



IF NOT EXISTS (
  SELECT 
    TOP 1 *
  FROM 
    INFORMATION_SCHEMA.COLUMNS
  WHERE 
        [TABLE_NAME]  = 'SOUDIV'
    AND [COLUMN_NAME] = 'ACT_NO' )
BEGIN
  ALTER TABLE
    SOUDIV
  ADD
    ACT_NO VARCHAR(20)
END
GO

IF EXISTS (SELECT * FROM INFORMATION_SCHEMA.ROUTINES WHERE Routine_Type = 'PROCEDURE' AND Specific_Name = 'up_SOUDIV_Update')
  DROP PROCEDURE up_SOUDIV_Update
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

  --Return updated ID
  RETURN @UniqueId
END
GO


IF NOT EXISTS (
  SELECT 
    TOP 1 *
  FROM 
    INFORMATION_SCHEMA.COLUMNS
  WHERE 
        [TABLE_NAME]  = 'PROCAT'
    AND [COLUMN_NAME] = 'ACC_NO' )
BEGIN
  ALTER TABLE
    PROCAT
  ADD
    ACC_NO VARCHAR(20)
END
GO

IF EXISTS (SELECT * FROM INFORMATION_SCHEMA.ROUTINES WHERE Routine_Type = 'PROCEDURE' AND Specific_Name = 'up_PROCAT_Update')
  DROP PROCEDURE up_PROCAT_Update
GO

CREATE PROCEDURE [dbo].[up_PROCAT_Update] (
  @UniqueId bigint,
  @CODECAT varchar(3),
  @DESC varchar(40),
  @ACC_NO varchar(20)
) AS

IF @UniqueId IS NULL
BEGIN
  --Insert new data into table
INSERT INTO [dbo].[PROCAT]
           ([CODECAT]
           ,[DESC]
	   ,[ACC_NO]
           ,[SysDate])
     VALUES
           (@CODECAT,
            @DESC,
            @ACC_NO,
            GETDATE())

  --Return new ID
  RETURN @@IDENTITY
END ELSE
BEGIN
  --Update data into table
  UPDATE
    PROCAT
  SET
    [CODECAT] = @CODECAT,
    [DESC]    = @DESC,
    [ACC_NO]  = @ACC_NO,
    [SysDate] = GETDATE()   
  WHERE
    UniqueId  = @UniqueId

  --Return updated ID
  RETURN @UniqueId
END
GO


IF NOT EXISTS (
  SELECT 
    TOP 1 *
  FROM 
    INFORMATION_SCHEMA.COLUMNS
  WHERE 
        [TABLE_NAME]  = 'FACDIV'
    AND [COLUMN_NAME] = 'ACT_NO' )
BEGIN
  ALTER TABLE
    FACDIV
  ADD
    ACT_NO VARCHAR(20)
END
GO	

IF EXISTS (SELECT * FROM INFORMATION_SCHEMA.ROUTINES WHERE Routine_Type = 'PROCEDURE' AND Specific_Name = 'up_FACDIV_Update')
  DROP PROCEDURE up_FACDIV_Update
GO 



CREATE PROCEDURE [dbo].[up_FACDIV_Update] (
  @UniqueId bigint,
  @SOU_ID varchar(20),
  @DIV_ID varchar(3),
  @ACT_NO VARCHAR(20),  
  @DESC varchar(40)
) AS

IF @UniqueId IS NULL
BEGIN
  --Insert new data into table
  INSERT INTO FACDIV (
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
    FACDIV
  SET
    [SOU_ID] = @SOU_ID,
    [DIV_ID] = @DIV_ID,
    [ACT_NO]  = @ACT_NO,	
    [DESC] = @DESC,
    SysDate = GETDATE()
  WHERE
    UniqueId = @UniqueId

  --Return updated ID
  RETURN @UniqueId
END
GO


  -- New field - PROCAT.ACH_NO

IF NOT EXISTS (
  SELECT 
    TOP 1 *
  FROM 
    INFORMATION_SCHEMA.COLUMNS
  WHERE 
        [TABLE_NAME]  = 'PROCAT'
    AND [COLUMN_NAME] = 'ACH_NO' )
BEGIN
  ALTER TABLE
    PROCAT
  ADD
    ACH_NO VARCHAR(20)
END
GO

IF EXISTS (SELECT * FROM INFORMATION_SCHEMA.ROUTINES WHERE Routine_Type = 'PROCEDURE' AND Specific_Name = 'up_PROCAT_Update')
  DROP PROCEDURE up_PROCAT_Update
GO

CREATE PROCEDURE [dbo].[up_PROCAT_Update] (
  @UniqueId bigint,
  @CODECAT varchar(3),
  @DESC varchar(40),
  @ACC_NO varchar(20),
  @ACH_NO varchar(20)
) AS

IF @UniqueId IS NULL
BEGIN
  --Insert new data into table
INSERT INTO [dbo].[PROCAT]
           ([CODECAT]
           ,[DESC]
	   ,[ACC_NO]
	   ,[ACH_NO]
           ,[SysDate])
     VALUES
           (@CODECAT,
            @DESC,
            @ACC_NO,
            @ACH_NO,
            GETDATE())

  --Return new ID
  RETURN @@IDENTITY
END ELSE
BEGIN
  --Update data into table
  UPDATE
    PROCAT
  SET
    [CODECAT] = @CODECAT,
    [DESC]    = @DESC,
    [ACC_NO]  = @ACC_NO,
    [ACH_NO]  = @ACH_NO,
    [SysDate] = GETDATE()   
  WHERE
    UniqueId  = @UniqueId

  --Return updated ID
  RETURN @UniqueId
END
GO	


  -- New field - DEFBLO.ACH_NO
IF NOT EXISTS (
  SELECT 
    TOP 1 *
  FROM 
    INFORMATION_SCHEMA.COLUMNS
  WHERE 
        [TABLE_NAME]  = 'DEFBLO'
    AND [COLUMN_NAME] = 'ACH_NO' )
BEGIN
  ALTER TABLE
    DEFBLO
  ADD
    ACH_NO VARCHAR(20)
END
GO

IF EXISTS (SELECT * FROM INFORMATION_SCHEMA.ROUTINES WHERE Routine_Type = 'PROCEDURE' AND Specific_Name = 'up_DEFBLO_Update')
  DROP PROCEDURE up_DEFBLO_Update
GO

CREATE PROCEDURE [dbo].[up_DEFBLO_Update] (
  @UniqueId bigint,
  @ORDRE varchar(6),
  @DESC varchar(40),
  @MULT int,
  @INCLSOU bit,
  @INCLFAC bit,
  @ACC_NO VARCHAR(20),
  @ACH_NO VARCHAR(20),
  @SYSTEM bit
) AS

IF @UniqueId IS NULL
BEGIN
  --Insert new data into table
  INSERT INTO DEFBLO (
    [ORDRE],
    [DESC],
    [MULT],
    [INCLSOU],
    [INCLFAC],
    [ACC_NO],
    [ACH_NO],
    [SYSTEM],
    SysDate)
  VALUES (
    @ORDRE,
    @DESC,
    @MULT,
    @INCLSOU,
    @INCLFAC,
    @ACC_NO,
    @ACH_NO,
    @SYSTEM,
    GETDATE())

  --Return new ID
  RETURN @@IDENTITY
END ELSE
BEGIN
  --Update data into table
  UPDATE
    DEFBLO
  SET
    [ORDRE] = @ORDRE,
    [DESC] = @DESC,
    [MULT] = @MULT,
    [INCLSOU] = @INCLSOU,
    [INCLFAC] = @INCLFAC,
    [ACC_NO] = @ACC_NO,
    [ACH_NO] = @ACH_NO,
    [SYSTEM] = @SYSTEM,
    SysDate = GETDATE()
  WHERE
    UniqueId = @UniqueId

  --Return updated ID
  RETURN @UniqueId
END
GO


  -- New field - SOUBLO.ACH_NO
IF NOT EXISTS (
  SELECT 
    TOP 1 *
  FROM 
    INFORMATION_SCHEMA.COLUMNS
  WHERE 
        [TABLE_NAME]  = 'SOUBLO'
    AND [COLUMN_NAME] = 'ACH_NO' )
BEGIN
  ALTER TABLE
    SOUBLO
  ADD
    ACH_NO VARCHAR(20)
END
GO


IF EXISTS (SELECT * FROM INFORMATION_SCHEMA.ROUTINES WHERE Routine_Type = 'PROCEDURE' AND Specific_Name = 'up_SOUBLO_Update')
  DROP PROCEDURE up_SOUBLO_Update
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

  --Return updated ID
  RETURN @UniqueId
END
GO

  -- New field - FACBLO.ACH_NO
IF NOT EXISTS (
  SELECT 
    TOP 1 *
  FROM 
    INFORMATION_SCHEMA.COLUMNS
  WHERE 
        [TABLE_NAME]  = 'FACBLO'
    AND [COLUMN_NAME] = 'ACH_NO' )
BEGIN
  ALTER TABLE
    FACBLO
  ADD
    ACH_NO VARCHAR(20)
END
GO

IF EXISTS (SELECT * FROM INFORMATION_SCHEMA.ROUTINES WHERE Routine_Type = 'PROCEDURE' AND Specific_Name = 'up_FACBLO_Update')
  DROP PROCEDURE up_FACBLO_Update
GO

CREATE PROCEDURE [dbo].[up_FACBLO_Update] (
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
  INSERT INTO FACBLO (
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
    FACBLO
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

  --Return updated ID
  RETURN @UniqueId
END
GO

  -- New field - SOUREL.ACH_NO
IF NOT EXISTS (
  SELECT 
    TOP 1 *
  FROM 
    INFORMATION_SCHEMA.COLUMNS
  WHERE 
        [TABLE_NAME]  = 'SOUREL'
    AND [COLUMN_NAME] = 'ACH_NO' )
BEGIN
  ALTER TABLE
    SOUREL
  ADD
    ACH_NO VARCHAR(20)
END
GO

IF EXISTS (SELECT * FROM INFORMATION_SCHEMA.ROUTINES WHERE Routine_Type = 'PROCEDURE' AND Specific_Name = 'up_SOUREL_Update')
  DROP PROCEDURE up_SOUREL_Update
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
  @ACH_NO varchar(20)
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
    SysDate = GETDATE()
  WHERE
    UniqueId = @UniqueId

  --Return updated ID
  RETURN @UniqueId
END
GO

  -- New field - FACREL.ACH_NO
IF NOT EXISTS (
  SELECT 
    TOP 1 *
  FROM 
    INFORMATION_SCHEMA.COLUMNS
  WHERE 
        [TABLE_NAME]  = 'FACREL'
    AND [COLUMN_NAME] = 'ACH_NO' )
BEGIN
  ALTER TABLE
    FACREL
  ADD
    ACH_NO VARCHAR(20)
END
GO

IF EXISTS (SELECT * FROM INFORMATION_SCHEMA.ROUTINES WHERE Routine_Type = 'PROCEDURE' AND Specific_Name = 'up_FACREL_Update')
  DROP PROCEDURE up_FACREL_Update
GO

CREATE PROCEDURE [dbo].[up_FACREL_Update] (
  @UniqueId bigint,
  @SOU_ID varchar(20),
  @BLO_ID varchar(3),
  @DIV_ID varchar(3),
  @TYPERELEVE varchar(1),
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
  @ACC_NO char(20),
  @ACH_NO char(20)
) AS

IF @UniqueId IS NULL
BEGIN
  --Insert new data into table
  INSERT INTO FACREL (
    [SOU_ID],
    [BLO_ID],
    [DIV_ID],
    [TYPERELEVE],
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
    SysDate)
  VALUES (
    @SOU_ID,
    @BLO_ID,
    @DIV_ID,
    @TYPERELEVE,
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
    GETDATE())

  --Return new ID
  RETURN @@IDENTITY
END ELSE
BEGIN
  --Update data into table
  UPDATE
    FACREL
  SET
    [SOU_ID] = @SOU_ID,
    [BLO_ID] = @BLO_ID,
    [DIV_ID] = @DIV_ID,
    [TYPERELEVE] = @TYPERELEVE,
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
    SysDate = GETDATE()
  WHERE
    UniqueId = @UniqueId

  --Return updated ID
  RETURN @UniqueId
END
GO

  -- New field - CLITAUX.ACH_NO
IF NOT EXISTS (
  SELECT 
    TOP 1 *
  FROM 
    INFORMATION_SCHEMA.COLUMNS
  WHERE 
        [TABLE_NAME]  = 'CLITAUX'
    AND [COLUMN_NAME] = 'ACH_NO' )
BEGIN
  ALTER TABLE
    CLITAUX
  ADD
    ACH_NO VARCHAR(20)
END
GO

IF EXISTS (SELECT * FROM INFORMATION_SCHEMA.ROUTINES WHERE Routine_Type = 'PROCEDURE' AND Specific_Name = 'up_CLITAUX_Update')
  DROP PROCEDURE up_CLITAUX_Update
GO

CREATE PROCEDURE [dbo].[up_CLITAUX_Update] (
  @UniqueId bigint,
  @CLI_ID varchar(20),
  @ORDRE varchar(6),
  @DESCTAUX varchar(50),
  @COUTUNI float,
  @PROFIT float,
  @ACC_NO varchar(20),
  @ACH_NO varchar(20)
) AS

IF @UniqueId IS NULL
BEGIN
  --Insert new data into table
  INSERT INTO CLITAUX (
    [CLI_ID],
    [ORDRE],
    [DESCTAUX],
    [COUTUNI],
    [PROFIT],
    [ACC_NO],
    [ACH_NO],
    SysDate)
  VALUES (
    @CLI_ID,
    @ORDRE,
    @DESCTAUX,
    @COUTUNI,
    @PROFIT,
    @ACC_NO,
    @ACH_NO,
    GETDATE())

  --Return new ID
  RETURN @@IDENTITY
END ELSE
BEGIN
  --Update data into table
  UPDATE
    CLITAUX
  SET
    [CLI_ID] = @CLI_ID,
    [ORDRE] = @ORDRE,
    [DESCTAUX] = @DESCTAUX,
    [COUTUNI] = @COUTUNI,
    [PROFIT] = @PROFIT,
    [ACC_NO] = @ACC_NO,
    [ACH_NO] = @ACH_NO,
    SysDate = GETDATE()
  WHERE
    UniqueId = @UniqueId

  --Return updated ID
  RETURN @UniqueId
END
GO

  -- New field - TAUX.ACH_NO
IF NOT EXISTS (
  SELECT 
    TOP 1 *
  FROM 
    INFORMATION_SCHEMA.COLUMNS
  WHERE 
        [TABLE_NAME]  = 'TAUX'
    AND [COLUMN_NAME] = 'ACH_NO' )
BEGIN
  ALTER TABLE
    TAUX
  ADD
    ACH_NO VARCHAR(20)
END
GO

IF EXISTS (SELECT * FROM INFORMATION_SCHEMA.ROUTINES WHERE Routine_Type = 'PROCEDURE' AND Specific_Name = 'up_TAUX_Update')
  DROP PROCEDURE up_TAUX_Update
GO

CREATE PROCEDURE [dbo].[up_TAUX_Update] (
  @UniqueId bigint,
  @ORDRE varchar(6),
  @DESCTAUX varchar(50),
  @COUTUNI float,
  @PROFIT float,
  @INCLSOU bit,
  @INCLFAC bit,
  @ACC_NO varchar(20),
  @ACH_NO varchar(20),  
  @SYSTEM bit
) AS

IF @UniqueId IS NULL
BEGIN
  --Insert new data into table
  INSERT INTO TAUX (
    [ORDRE],
    [DESCTAUX],
    [COUTUNI],
    [PROFIT],
    [INCLSOU],
    [INCLFAC],
    [ACC_NO],
    [ACH_NO],	
    [SYSTEM],
    SysDate)
  VALUES (
    @ORDRE,
    @DESCTAUX,
    @COUTUNI,
    @PROFIT,
    @INCLSOU,
    @INCLFAC,
    @ACC_NO,
	@ACH_NO,
    @SYSTEM,
    GETDATE())

  --Return new ID
  RETURN @@IDENTITY
END ELSE
BEGIN
  --Update data into table
  UPDATE
    TAUX
  SET
    [ORDRE] = @ORDRE,
    [DESCTAUX] = @DESCTAUX,
    [COUTUNI] = @COUTUNI,
    [PROFIT] = @PROFIT,
    [INCLSOU] = @INCLSOU,
    [INCLFAC] = @INCLFAC,
    [ACC_NO] = @ACC_NO,
    [ACH_NO] = @ACH_NO,	
    [SYSTEM] = @SYSTEM,
    SysDate = GETDATE()
  WHERE
    UniqueId = @UniqueId

  --Return updated ID
  RETURN @UniqueId
END
GO

  -- New field - FRAIS.ACH_NO
IF NOT EXISTS (
  SELECT 
    TOP 1 *
  FROM 
    INFORMATION_SCHEMA.COLUMNS
  WHERE 
        [TABLE_NAME]  = 'FRAIS'
    AND [COLUMN_NAME] = 'ACH_NO' )
BEGIN
  ALTER TABLE
    FRAIS
  ADD
    ACH_NO VARCHAR(20)
END
GO

IF EXISTS (SELECT * FROM INFORMATION_SCHEMA.ROUTINES WHERE Routine_Type = 'PROCEDURE' AND Specific_Name = 'up_FRAIS_Update')
  DROP PROCEDURE up_FRAIS_Update
GO

CREATE PROCEDURE [dbo].[up_FRAIS_Update] (
  @UniqueId bigint,
  @ORDRE varchar(6),
  @DESCFRAIS varchar(50),
  @COUTUNI float,
  @FRAISUM varchar(2),
  @PROFIT float,
  @INCLSOU bit,
  @INCLFAC bit,
  @ACC_NO varchar (20),
  @ACH_NO varchar (20),
  @SYSTEM bit
) AS

IF @UniqueId IS NULL
BEGIN
  --Insert new data into table
  INSERT INTO FRAIS (
    [ORDRE],
    [DESCFRAIS],
    [COUTUNI],
    [FRAISUM],
    [PROFIT],
    [INCLSOU],
    [INCLFAC],
    [ACC_NO],
    [ACH_NO],
    [SYSTEM],
    SysDate)
  VALUES (
    @ORDRE,
    @DESCFRAIS,
    @COUTUNI,
    @FRAISUM,
    @PROFIT,
    @INCLSOU,
    @INCLFAC,
    @ACC_NO,
    @ACH_NO,
    @SYSTEM,
    GETDATE())

  --Return new ID
  RETURN @@IDENTITY
END ELSE
BEGIN
  --Update data into table
  UPDATE
    FRAIS
  SET
    [ORDRE] = @ORDRE,
    [DESCFRAIS] = @DESCFRAIS,
    [COUTUNI] = @COUTUNI,
    [FRAISUM] = @FRAISUM,
    [PROFIT] = @PROFIT,
    [INCLSOU] = @INCLSOU,
    [INCLFAC] = @INCLFAC,
    [ACC_NO] = @ACC_NO,
    [ACH_NO] = @ACH_NO,
    [SYSTEM] = @SYSTEM,
    SysDate = GETDATE()
  WHERE
    UniqueId = @UniqueId

  --Return updated ID
  RETURN @UniqueId
END
GO


  -- New field - PROCAT.ACT_NO

IF NOT EXISTS (
  SELECT 
    TOP 1 *
  FROM 
    INFORMATION_SCHEMA.COLUMNS
  WHERE 
        [TABLE_NAME]  = 'PROCAT'
    AND [COLUMN_NAME] = 'ACT_NO' )
BEGIN
  ALTER TABLE
    PROCAT
  ADD
    ACT_NO VARCHAR(20)
END
GO

IF EXISTS (SELECT * FROM INFORMATION_SCHEMA.ROUTINES WHERE Routine_Type = 'PROCEDURE' AND Specific_Name = 'up_PROCAT_Update')
  DROP PROCEDURE up_PROCAT_Update
GO

CREATE PROCEDURE [dbo].[up_PROCAT_Update] (
  @UniqueId bigint,
  @CODECAT varchar(3),
  @DESC varchar(40),
  @ACC_NO varchar(20),
  @ACH_NO varchar(20),
  @ACT_NO varchar(20)  
) AS

IF @UniqueId IS NULL
BEGIN
  --Insert new data into table
INSERT INTO [dbo].[PROCAT]
           ([CODECAT]
           ,[DESC]
	   ,[ACC_NO]
	   ,[ACH_NO]
	   ,[ACT_NO]	   
           ,[SysDate])
     VALUES
           (@CODECAT,
            @DESC,
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
    PROCAT
  SET
    [CODECAT] = @CODECAT,
    [DESC]    = @DESC,
    [ACC_NO]  = @ACC_NO,
    [ACH_NO]  = @ACH_NO,
    [ACT_NO]  = @ACT_NO,	
    [SysDate] = GETDATE()   
  WHERE
    UniqueId  = @UniqueId

  --Return updated ID
  RETURN @UniqueId
END
GO	


  -- New field - SOUREL.ACT_NO
IF NOT EXISTS (
  SELECT 
    TOP 1 *
  FROM 
    INFORMATION_SCHEMA.COLUMNS
  WHERE 
        [TABLE_NAME]  = 'SOUREL'
    AND [COLUMN_NAME] = 'ACT_NO' )
BEGIN
  ALTER TABLE
    SOUREL
  ADD
    ACT_NO VARCHAR(20)
END
GO

IF EXISTS (SELECT * FROM INFORMATION_SCHEMA.ROUTINES WHERE Routine_Type = 'PROCEDURE' AND Specific_Name = 'up_SOUREL_Update')
  DROP PROCEDURE up_SOUREL_Update
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

  --Return updated ID
  RETURN @UniqueId
END
GO

  -- New field - FACREL.ACT_NO
IF NOT EXISTS (
  SELECT 
    TOP 1 *
  FROM 
    INFORMATION_SCHEMA.COLUMNS
  WHERE 
        [TABLE_NAME]  = 'FACREL'
    AND [COLUMN_NAME] = 'ACT_NO' )
BEGIN
  ALTER TABLE
    FACREL
  ADD
    ACT_NO VARCHAR(20)
END
GO

IF EXISTS (SELECT * FROM INFORMATION_SCHEMA.ROUTINES WHERE Routine_Type = 'PROCEDURE' AND Specific_Name = 'up_FACREL_Update')
  DROP PROCEDURE up_FACREL_Update
GO

CREATE PROCEDURE [dbo].[up_FACREL_Update] (
  @UniqueId bigint,
  @SOU_ID varchar(20),
  @BLO_ID varchar(3),
  @DIV_ID varchar(3),
  @TYPERELEVE varchar(1),
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
  @ACC_NO char(20),
  @ACH_NO char(20),
  @ACT_NO char(20)  
) AS

IF @UniqueId IS NULL
BEGIN
  --Insert new data into table
  INSERT INTO FACREL (
    [SOU_ID],
    [BLO_ID],
    [DIV_ID],
    [TYPERELEVE],
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
    FACREL
  SET
    [SOU_ID] = @SOU_ID,
    [BLO_ID] = @BLO_ID,
    [DIV_ID] = @DIV_ID,
    [TYPERELEVE] = @TYPERELEVE,
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

  --Return updated ID
  RETURN @UniqueId
END
GO

  -- New field - CLITAUX.ACT_NO
IF NOT EXISTS (
  SELECT 
    TOP 1 *
  FROM 
    INFORMATION_SCHEMA.COLUMNS
  WHERE 
        [TABLE_NAME]  = 'CLITAUX'
    AND [COLUMN_NAME] = 'ACT_NO' )
BEGIN
  ALTER TABLE
    CLITAUX
  ADD
    ACT_NO VARCHAR(20)
END
GO

IF EXISTS (SELECT * FROM INFORMATION_SCHEMA.ROUTINES WHERE Routine_Type = 'PROCEDURE' AND Specific_Name = 'up_CLITAUX_Update')
  DROP PROCEDURE up_CLITAUX_Update
GO

CREATE PROCEDURE [dbo].[up_CLITAUX_Update] (
  @UniqueId bigint,
  @CLI_ID varchar(20),
  @ORDRE varchar(6),
  @DESCTAUX varchar(50),
  @COUTUNI float,
  @PROFIT float,
  @ACC_NO varchar(20),
  @ACH_NO varchar(20),
  @ACT_NO varchar(20)  
) AS

IF @UniqueId IS NULL
BEGIN
  --Insert new data into table
  INSERT INTO CLITAUX (
    [CLI_ID],
    [ORDRE],
    [DESCTAUX],
    [COUTUNI],
    [PROFIT],
    [ACC_NO],
    [ACH_NO],
    [ACT_NO],	
    SysDate)
  VALUES (
    @CLI_ID,
    @ORDRE,
    @DESCTAUX,
    @COUTUNI,
    @PROFIT,
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
    CLITAUX
  SET
    [CLI_ID] = @CLI_ID,
    [ORDRE] = @ORDRE,
    [DESCTAUX] = @DESCTAUX,
    [COUTUNI] = @COUTUNI,
    [PROFIT] = @PROFIT,
    [ACC_NO] = @ACC_NO,
    [ACH_NO] = @ACH_NO,
    [ACT_NO] = @ACT_NO,	
    SysDate = GETDATE()
  WHERE
    UniqueId = @UniqueId

  --Return updated ID
  RETURN @UniqueId
END
GO

  -- New field - TAUX.ACT_NO
IF NOT EXISTS (
  SELECT 
    TOP 1 *
  FROM 
    INFORMATION_SCHEMA.COLUMNS
  WHERE 
        [TABLE_NAME]  = 'TAUX'
    AND [COLUMN_NAME] = 'ACT_NO' )
BEGIN
  ALTER TABLE
    TAUX
  ADD
    ACT_NO VARCHAR(20)
END
GO

IF EXISTS (SELECT * FROM INFORMATION_SCHEMA.ROUTINES WHERE Routine_Type = 'PROCEDURE' AND Specific_Name = 'up_TAUX_Update')
  DROP PROCEDURE up_TAUX_Update
GO

CREATE PROCEDURE [dbo].[up_TAUX_Update] (
  @UniqueId bigint,
  @ORDRE varchar(6),
  @DESCTAUX varchar(50),
  @COUTUNI float,
  @PROFIT float,
  @INCLSOU bit,
  @INCLFAC bit,
  @ACC_NO varchar(20),
  @ACH_NO varchar(20),
  @ACT_NO varchar(20),  
  @SYSTEM bit
) AS

IF @UniqueId IS NULL
BEGIN
  --Insert new data into table
  INSERT INTO TAUX (
    [ORDRE],
    [DESCTAUX],
    [COUTUNI],
    [PROFIT],
    [INCLSOU],
    [INCLFAC],
    [ACC_NO],
    [ACH_NO],	
    [ACT_NO],		
    [SYSTEM],
    SysDate)
  VALUES (
    @ORDRE,
    @DESCTAUX,
    @COUTUNI,
    @PROFIT,
    @INCLSOU,
    @INCLFAC,
    @ACC_NO,
	@ACH_NO,
	@ACT_NO,	
    @SYSTEM,
    GETDATE())

  --Return new ID
  RETURN @@IDENTITY
END ELSE
BEGIN
  --Update data into table
  UPDATE
    TAUX
  SET
    [ORDRE] = @ORDRE,
    [DESCTAUX] = @DESCTAUX,
    [COUTUNI] = @COUTUNI,
    [PROFIT] = @PROFIT,
    [INCLSOU] = @INCLSOU,
    [INCLFAC] = @INCLFAC,
    [ACC_NO] = @ACC_NO,
    [ACH_NO] = @ACH_NO,
	[ACT_NO] = @ACT_NO,	
    [SYSTEM] = @SYSTEM,
    SysDate = GETDATE()
  WHERE
    UniqueId = @UniqueId

  --Return updated ID
  RETURN @UniqueId
END
GO

  -- New field - FRAIS.ACT_NO
IF NOT EXISTS (
  SELECT 
    TOP 1 *
  FROM 
    INFORMATION_SCHEMA.COLUMNS
  WHERE 
        [TABLE_NAME]  = 'FRAIS'
    AND [COLUMN_NAME] = 'ACT_NO' )
BEGIN
  ALTER TABLE
    FRAIS
  ADD
    ACT_NO VARCHAR(20)
END
GO

IF EXISTS (SELECT * FROM INFORMATION_SCHEMA.ROUTINES WHERE Routine_Type = 'PROCEDURE' AND Specific_Name = 'up_FRAIS_Update')
  DROP PROCEDURE up_FRAIS_Update
GO

CREATE PROCEDURE [dbo].[up_FRAIS_Update] (
  @UniqueId bigint,
  @ORDRE varchar(6),
  @DESCFRAIS varchar(50),
  @COUTUNI float,
  @FRAISUM varchar(2),
  @PROFIT float,
  @INCLSOU bit,
  @INCLFAC bit,
  @ACC_NO varchar (20),
  @ACH_NO varchar (20),
  @ACT_NO varchar (20),  
  @SYSTEM bit
) AS

IF @UniqueId IS NULL
BEGIN
  --Insert new data into table
  INSERT INTO FRAIS (
    [ORDRE],
    [DESCFRAIS],
    [COUTUNI],
    [FRAISUM],
    [PROFIT],
    [INCLSOU],
    [INCLFAC],
    [ACC_NO],
    [ACH_NO],
    [ACT_NO],	
    [SYSTEM],
    SysDate)
  VALUES (
    @ORDRE,
    @DESCFRAIS,
    @COUTUNI,
    @FRAISUM,
    @PROFIT,
    @INCLSOU,
    @INCLFAC,
    @ACC_NO,
    @ACH_NO,
    @ACT_NO,	
    @SYSTEM,
    GETDATE())

  --Return new ID
  RETURN @@IDENTITY
END ELSE
BEGIN
  --Update data into table
  UPDATE
    FRAIS
  SET
    [ORDRE] = @ORDRE,
    [DESCFRAIS] = @DESCFRAIS,
    [COUTUNI] = @COUTUNI,
    [FRAISUM] = @FRAISUM,
    [PROFIT] = @PROFIT,
    [INCLSOU] = @INCLSOU,
    [INCLFAC] = @INCLFAC,
    [ACC_NO] = @ACC_NO,
    [ACH_NO] = @ACH_NO,
    [ACT_NO] = @ACT_NO,	
    [SYSTEM] = @SYSTEM,
    SysDate = GETDATE()
  WHERE
    UniqueId = @UniqueId

  --Return updated ID
  RETURN @UniqueId
END
GO
