SET NUMERIC_ROUNDABORT OFF
GO
SET ANSI_PADDING, ANSI_WARNINGS, CONCAT_NULL_YIELDS_NULL, ARITHABORT, QUOTED_IDENTIFIER, ANSI_NULLS ON
GO
SET XACT_ABORT ON
GO
SET TRANSACTION ISOLATION LEVEL SERIALIZABLE
GO
PRINT N'Altering [dbo].[ENSEMBLE]'
GO
ALTER TABLE [dbo].[ENSEMBLE] ALTER COLUMN [DESC] [varchar] (60) NULL

GO
PRINT N'Creating index [IDX_CLEPERS] on [dbo].[ENSEMBLE]'
GO
CREATE NONCLUSTERED INDEX [IDX_CLEPERS] ON [dbo].[ENSEMBLE] ([CLEPERS])
GO
PRINT N'Creating index [IDX_ENS_ID] on [dbo].[ENSEMBLE]'
GO
CREATE NONCLUSTERED INDEX [IDX_ENS_ID] ON [dbo].[ENSEMBLE] ([ENS_ID])
GO
PRINT N'Altering [dbo].[up_ENSEMBLE_Update]'
GO


ALTER PROCEDURE [dbo].[up_ENSEMBLE_Update] (
  @UniqueId bigint,
  @ENS_ID varchar(20),
  @CLEPERS varchar(20),
  @DESC varchar(60),    -- 2012-01-19 EMadore : V3 -> Passage de 40 à 60 chars
  @COUUM varchar(2),
  @PROFIT float,
  @TEMPSEC float,
  @TEMPUNI float,
  @TEMPUM varchar(2),
  @DATECREE datetime,
  @OLDESTPROD datetime,
  @SYSTEM bit,
  @USES_DISC bit
) AS

IF @UniqueId IS NULL
BEGIN
  --Insert new data into table
  INSERT INTO ENSEMBLE (
    [ENS_ID],
    [CLEPERS],
    [DESC],
    [COUUM],
    [PROFIT],
    [TEMPSEC],
    [TEMPUNI],
    [TEMPUM],
    [DATECREE],
    [OLDESTPROD],
    [SYSTEM],
    [USES_DISC],
    SysDate)
  VALUES (
    @ENS_ID,
    @CLEPERS,
    @DESC,
    @COUUM,
    @PROFIT,
    @TEMPSEC,
    @TEMPUNI,
    @TEMPUM,
    @DATECREE,
    @OLDESTPROD,
    @SYSTEM,
    @USES_DISC,
    GETDATE())

  --Return new ID
  RETURN @@IDENTITY
END ELSE
BEGIN
  --Update data into table
  UPDATE
    ENSEMBLE
  SET
    [ENS_ID] = @ENS_ID,
    [CLEPERS] = @CLEPERS,
    [DESC] = @DESC,
    [COUUM] = @COUUM,
    [PROFIT] = @PROFIT,
    [TEMPSEC] = @TEMPSEC,
    [TEMPUNI] = @TEMPUNI,
    [TEMPUM] = @TEMPUM,
    [DATECREE] = @DATECREE,
    [OLDESTPROD] = @OLDESTPROD,
    [SYSTEM] = @SYSTEM,
    [USES_DISC] = @USES_DISC,
    SysDate = GETDATE()
  WHERE
    UniqueId = @UniqueId

  --Return updated ID
  RETURN @UniqueId
END

GO
PRINT N'Altering [dbo].[FACENS]'
GO
ALTER TABLE [dbo].[FACENS] ALTER COLUMN [DESC] [varchar] (60) NULL

GO
PRINT N'Creating index [IDX_UNIQUEKEY] on [dbo].[FACENS]'
GO
CREATE NONCLUSTERED INDEX [IDX_UNIQUEKEY] ON [dbo].[FACENS] ([SOU_ID], [ENS_ID])
GO
PRINT N'Altering [dbo].[up_FACENS_Update]'
GO


ALTER PROCEDURE [dbo].[up_FACENS_Update] (
  @UniqueId bigint,
  @SOU_ID varchar(20),
  @ENS_ID varchar(20),
  @DESC varchar(60),   -- 2012-01-19 EMadore V3 : Passage de 40 à 60 chars
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
  INSERT INTO FACENS (
    [SOU_ID],
    [ENS_ID],
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
    FACENS
  SET
    [SOU_ID] = @SOU_ID,
    [ENS_ID] = @ENS_ID,
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

  --Return updated ID
  RETURN @UniqueId
END


GO
PRINT N'Altering [dbo].[FACLOTS]'
GO
ALTER TABLE [dbo].[FACLOTS] ALTER COLUMN [DESC] [varchar] (60) NULL

GO
PRINT N'Creating index [IDX_UNIQUEKEY] on [dbo].[FACLOTS]'
GO
CREATE NONCLUSTERED INDEX [IDX_UNIQUEKEY] ON [dbo].[FACLOTS] ([SOU_ID], [LOTS_ID])
GO
PRINT N'Altering [dbo].[up_FACLOTS_Update]'
GO


ALTER PROCEDURE [dbo].[up_FACLOTS_Update] (
  @UniqueId bigint,
  @SOU_ID varchar(20),
  @LOTS_ID varchar(20),
  @DESC varchar(60),        -- 2012-01-19 EMadore V3 : Passage de 40 à 60 chars
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
  INSERT INTO FACLOTS (
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
    FACLOTS
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

  --Return updated ID
  RETURN @UniqueId
END

GO
PRINT N'Altering [dbo].[FACTURES]'
GO
ALTER TABLE [dbo].[FACTURES] ADD
[CLIENTEMAI] [varchar] (80) NULL,
[SITEEMAIL] [varchar] (80) NULL
GO
PRINT N'Creating index [IDX_CLIENTNO] on [dbo].[FACTURES]'
GO
CREATE NONCLUSTERED INDEX [IDX_CLIENTNO] ON [dbo].[FACTURES] ([CLIENTNO])
GO
PRINT N'Creating index [IDX_NODOC] on [dbo].[FACTURES]'
GO
CREATE NONCLUSTERED INDEX [IDX_NODOC] ON [dbo].[FACTURES] ([NODOC])
GO
PRINT N'Creating index [IDX_SOU_ID] on [dbo].[FACTURES]'
GO
CREATE NONCLUSTERED INDEX [IDX_SOU_ID] ON [dbo].[FACTURES] ([SOU_ID])
GO
PRINT N'Altering [dbo].[up_FACTURES_Update]'
GO


ALTER PROCEDURE [dbo].[up_FACTURES_Update] (
  @UniqueId bigint,
  @SOU_ID varchar(20),
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
  @EST_NAME varchar(50)
) AS

IF @UniqueId IS NULL
BEGIN
  --Insert new data into table
  INSERT INTO FACTURES (
    [SOU_ID],
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
    SysDate)
  VALUES (
    @SOU_ID,
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
    SysDate = GETDATE()
  WHERE
    UniqueId = @UniqueId

  --Return updated ID
  RETURN @UniqueId
END


GO
PRINT N'Altering [dbo].[SOUENS]'
GO
ALTER TABLE [dbo].[SOUENS] ALTER COLUMN [DESC] [varchar] (60) NULL

GO
PRINT N'Creating index [IDX_UNIQUEKEY] on [dbo].[SOUENS]'
GO
CREATE NONCLUSTERED INDEX [IDX_UNIQUEKEY] ON [dbo].[SOUENS] ([SOU_ID], [ENS_ID])
GO
PRINT N'Altering [dbo].[up_SOUENS_Update]'
GO


ALTER PROCEDURE [dbo].[up_SOUENS_Update] (
  @UniqueId bigint,
  @SOU_ID varchar(20),
  @ENS_ID varchar(20),
  @DESC varchar(60),    -- 2012-01-19 EMadore V3 : Passage de 40 à 60 chars
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

  --Return updated ID
  RETURN @UniqueId
END

GO
PRINT N'Altering [dbo].[SOULOTS]'
GO
ALTER TABLE [dbo].[SOULOTS] ALTER COLUMN [DESC] [varchar] (60) NULL

GO
PRINT N'Creating index [IDX_UNIQUEKEY] on [dbo].[SOULOTS]'
GO
CREATE NONCLUSTERED INDEX [IDX_UNIQUEKEY] ON [dbo].[SOULOTS] ([SOU_ID], [LOTS_ID])
GO
PRINT N'Altering [dbo].[up_SOULOTS_Update]'
GO


ALTER PROCEDURE [dbo].[up_SOULOTS_Update] (
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

  --Return updated ID
  RETURN @UniqueId
END

GO
PRINT N'Altering [dbo].[SOUMIS]'
GO
ALTER TABLE [dbo].[SOUMIS] ADD
[CLIENTEMAI] [varchar] (80) NULL,
[SITEEMAIL] [varchar] (80) NULL
GO
PRINT N'Creating index [IDX_CLIENTNO] on [dbo].[SOUMIS]'
GO
CREATE NONCLUSTERED INDEX [IDX_CLIENTNO] ON [dbo].[SOUMIS] ([CLIENTNO])
GO
PRINT N'Creating index [IDX_NODOC] on [dbo].[SOUMIS]'
GO
CREATE NONCLUSTERED INDEX [IDX_NODOC] ON [dbo].[SOUMIS] ([NODOC])
GO
PRINT N'Creating index [IDX_SOU_ID] on [dbo].[SOUMIS]'
GO
CREATE NONCLUSTERED INDEX [IDX_SOU_ID] ON [dbo].[SOUMIS] ([SOU_ID])
GO
PRINT N'Altering [dbo].[up_SOUMIS_Update]'
GO


ALTER PROCEDURE [dbo].[up_SOUMIS_Update] (
  @UniqueId bigint,
  @SOU_ID varchar(20),
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
  @EST_NAME varchar(50)
) AS

IF @UniqueId IS NULL
BEGIN
  --Insert new data into table
  INSERT INTO SOUMIS (
    [SOU_ID],
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
    SysDate)
  VALUES (
    @SOU_ID,
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
    SysDate = GETDATE()
  WHERE
    UniqueId = @UniqueId

  --Return updated ID
  RETURN @UniqueId
END


GO
PRINT N'Creating [dbo].[up_GetAllFieldsBut]'
GO

IF EXISTS (SELECT * FROM INFORMATION_SCHEMA.ROUTINES WHERE Routine_Type = 'PROCEDURE' AND Specific_Name = 'up_GetAllFieldsBut')
  DROP PROCEDURE up_GetAllFieldsBut
GO


-- =============================================
-- Author:		Eric Madore
-- Create date: 2011-10-19
-- Description:	Retourne toutes les colonnes de la table reçu sauf celui reçu en paramêtre
--				Utilisé pour exclure entre autre une identité
-- =============================================
CREATE PROCEDURE [dbo].[up_GetAllFieldsBut] (
	@TableName		varchar(64),			-- Nom de la table pour les champs
	@FieldName		varchar(32),			-- Nom du champ à ne pas inclure
    @SelectString	varchar(8000) output	-- Chaine qui contient la liste des champs sauf @FieldName
)
AS
BEGIN
	SET NOCOUNT ON;

	SELECT @SelectString = ''
	SELECT @SelectString = @SelectString + '[' + Name + '], ' FROM SysColumns WHERE id = Object_Id(@TableName) AND Name != @FieldName
	SELECT @SelectString = SubString(@SelectString, 1, Len(@SelectString) - Len(', '))
END


GO
PRINT N'Creating [dbo].[up_DeleteSoumis_Full]'
GO

IF EXISTS (SELECT * FROM INFORMATION_SCHEMA.ROUTINES WHERE Routine_Type = 'PROCEDURE' AND Specific_Name = 'up_DeleteSoumis_Full')
  DROP PROCEDURE up_DeleteSoumis_Full
GO


-- =============================================
-- Author:		Eric Madore
-- Create date: 2011-11-10
-- Description:	Supprime la soumission reçu
--				Note : Ne supprime pas l'entête de la soumission.
-- =============================================
CREATE PROCEDURE [dbo].[up_DeleteSoumis_Full] (
    @DeleteSOU_ID	varchar(20),	-- SOU_ID de la soumission à supprimer
	@DeleteHeader	bit = 0			-- Si UP, Indique qu'on doit aussi supprimer l'entête. 
									-- DOWN par défaut car le call est instancié dans l'application par la supression de l'entête
									-- Retourne : n/a
)
AS
BEGIN
	SET NOCOUNT ON;

		-- Delete l'entête si nécessaire
	IF @DeleteHeader = 1
		DELETE FROM SOUMIS WHERE SOU_ID = @DeleteSOU_ID

		-- Delete les sous-tables
	DELETE FROM SOUREL		WHERE SOU_ID = @DeleteSOU_ID 
	DELETE FROM SOUBLO		WHERE SOU_ID = @DeleteSOU_ID
	DELETE FROM SOUDIV		WHERE SOU_ID = @DeleteSOU_ID 
	DELETE FROM SOUAMD		WHERE SOU_ID = @DeleteSOU_ID
	DELETE FROM SOUWEBLOG	WHERE SOU_ID = @DeleteSOU_ID
	DELETE FROM SOUPRO		WHERE SOU_ID = @DeleteSOU_ID 
	DELETE FROM SOUENS		WHERE SOU_ID = @DeleteSOU_ID 
	DELETE FROM SOUENSCO	WHERE SOU_ID = @DeleteSOU_ID 
	DELETE FROM SOULOTS		WHERE SOU_ID = @DeleteSOU_ID 
	DELETE FROM SOULOTSCO	WHERE SOU_ID = @DeleteSOU_ID 	
END

GO
PRINT N'Creating [dbo].[up_DeleteFactures_Full]'
GO


IF EXISTS (SELECT * FROM INFORMATION_SCHEMA.ROUTINES WHERE Routine_Type = 'PROCEDURE' AND Specific_Name = 'up_DeleteFactures_Full')
  DROP PROCEDURE up_DeleteFactures_Full
GO


-- =============================================
-- Author:		Eric Madore
-- Create date: 2011-11-30
-- Description:	Supprime la facture reçu
-- =============================================
CREATE PROCEDURE [dbo].[up_DeleteFactures_Full] (
    @DeleteSOU_ID	varchar(20),	-- SOU_ID de la facture à supprimer
	@DeleteHeader	bit = 0			-- Si UP, Indique qu'on doit aussi supprimer l'entête. 
									-- DOWN par défaut car le call est instancié dans l'application par la supression de l'entête
									-- Retourne : n/a
)
AS
BEGIN
	SET NOCOUNT ON;

		-- Delete l'entête si nécessaire
	IF @DeleteHeader = 1
		DELETE FROM FACTURES WHERE SOU_ID = @DeleteSOU_ID

		-- Delete les sous-tables
	DELETE FROM FACREL		WHERE SOU_ID = @DeleteSOU_ID 
	DELETE FROM FACBLO		WHERE SOU_ID = @DeleteSOU_ID
	DELETE FROM FACDIV		WHERE SOU_ID = @DeleteSOU_ID 
	DELETE FROM FACAMD		WHERE SOU_ID = @DeleteSOU_ID
	DELETE FROM FACWEBLOG	WHERE SOU_ID = @DeleteSOU_ID
	DELETE FROM FACPRO		WHERE SOU_ID = @DeleteSOU_ID 
	DELETE FROM FACENS		WHERE SOU_ID = @DeleteSOU_ID 
	DELETE FROM FACENSCO	WHERE SOU_ID = @DeleteSOU_ID 
	DELETE FROM FACLOTS		WHERE SOU_ID = @DeleteSOU_ID 
	DELETE FROM FACLOTSCO	WHERE SOU_ID = @DeleteSOU_ID 	
END

GO
PRINT N'Creating [dbo].[up_CloneRecords]'
GO

IF EXISTS (SELECT * FROM INFORMATION_SCHEMA.ROUTINES WHERE Routine_Type = 'PROCEDURE' AND Specific_Name = 'up_CloneRecords')
  DROP PROCEDURE up_CloneRecords
GO

-- =============================================
-- Author:		Eric Madore
-- Create date: 2011-10-19
-- Description:	Clones les enregistrements de la table répondant à la clé recu
--				Pour l'instant, n'accepte qu'une clé de type varchar
--				Si les records n'on pas de colonnes identité, passé NULL
--				Aucun check n'est faite sur la clé primaire. DOnc, cloner un record pourais violé la clé primaire ou un autre index unique.
--					Vous devez donc vous assurer que :
--					1) Soit la clé primaire est sur l'identité (sera incréementé automatiquement)
--					2) Doit la clé primaire est sur le champ clé ou est inclu (sera mis à jour automatiquement)
-- Modifications:	
--		2012-01-26 EMadore : Ajout des colonnes dans le INSERT INTO à la fin. Sinon, les colonnes de la table temporaire et destination ne concorde pas sous 2000.
--							 Fonctionne dans ca version antérioeur sous 2005 cependant.
-- =============================================
CREATE PROCEDURE [dbo].[up_CloneRecords] (
	@TableName			varchar(64),			-- Nom de la table sur laquel cloner les records
	@KeyFieldName		varchar(32),			-- Nom du champ de clé à utilisé
	@KeyFieldValue		varchar(128),			-- Valeur du champ de clé. Tous les record répondant à cette condition seront clonés
	@NewKeyFieldValue	varchar(128) = NULL,	-- Nouvelle valeur à assigné au champ clé. Null si la valeur reste constante
	@IdentityFieldName	varchar(64) = NULL,		-- Nom du champ identité, NULL si aucun
	@KeyIndexName		varchar(32) = NULL		-- Nom de l'index de la clé, NULL si aucun
												-- Retounrne l'identité du dernier record cloné. Si un seul record cloné retourn esont identité
)
AS
BEGIN
	SET NOCOUNT ON;

	IF OBJECT_ID('tempdb..##TempTableForCloning') IS NOT NULL
		DROP TABLE ##TempTableForCloning

		-- Déclaration des variables locals
	DECLARE @SQLString		varchar(8000)
	DECLARE @SelectString	varchar(8000)
	
		-- Vas chercher tous les champs de la table sauf la champ identité au besoin
	IF @IdentityFieldName IS NULL
		SELECT @SelectString = '*'	
	ELSE
		EXEC dbo.up_GetAllFieldsBut @TableName, @IdentityFieldName, @SelectString output  

		-- On veut en premier créer un table temporaire avec la même structure que la table à cloner
		-- Assume que si on veut cloner un record que la table à au moins un record
		-- N'ajoute pas tout de suite les record car on veux spécifié notre index optimale dans un insert plus loin
		-- C'est possible dans un select mais pas dans un select into
	SELECT @SQLString =	'SELECT TOP 1 '	+ @SelectString + 
						' INTO '		+ '##TempTableForCloning' +
						' FROM '		+ @TableName
	EXEC(@SQLString)

		-- Clear la table temporaire pusique le record utilisé n'est probablement pas à cloner
	SELECT @SQLString =	'DELETE FROM ##TempTableForCloning'
	EXEC(@SQLString)

		-- Popule la table de clonage intermédiaire avec les records à cloner
	SELECT @SQLString =	'INSERT INTO '	+ '##TempTableForCloning' +  
						' SELECT '		+ @SelectString +
						' FROM '		+ @TableName

	IF @KeyIndexName IS NOT NULL
		SELECT @SQLString =	@SQLString + ' WITH (INDEX (' + @KeyIndexName + '))' 

	SELECT @SQLString =	@SQLString + ' WHERE '	+ @KeyFieldName + ' = ''' + @KeyFieldValue + ''''
	EXEC(@SQLString)

		-- Update le champ clé de la table de clonage intermédiaire avec sa nouvelle valeur au besoin
	IF @NewKeyFieldValue IS NOT NULL
	BEGIN
		SELECT @SQLString =	'UPDATE '	+ '##TempTableForCloning' +
							' SET '		+ @KeyFieldName + ' = ' + '''' + @NewKeyFieldValue + ''''
		EXEC(@SQLString)
	END		

		-- Réintègre les records clonés dans la table d'origine
	SELECT @SQLString =	'INSERT INTO '	+ @TableName + '(' + @SelectString + ')' +
						' SELECT '		+ @SelectString +
						' FROM '		+ '##TempTableForCloning'
	EXEC(@SQLString)

		-- Supprime la table temporaire utilisé
	IF OBJECT_ID('tempdb..##TempTableForCloning') IS NOT NULL
		DROP TABLE ##TempTableForCloning
END


GO
PRINT N'Creating [dbo].[up_CopySoumis_Full]'
GO

IF EXISTS (SELECT * FROM INFORMATION_SCHEMA.ROUTINES WHERE Routine_Type = 'PROCEDURE' AND Specific_Name = 'up_CopySoumis_Full')
  DROP PROCEDURE up_CopySoumis_Full
GO


-- =============================================
-- Author:		Eric Madore
-- Create date: 2011-10-19
-- Description:	Copy/paste la soumission reçu
-- =============================================
CREATE PROCEDURE [dbo].[up_CopySoumis_Full] (
    @CopySOU_ID		varchar(20),	-- SOU_ID de la soumission à copy/paster 
	@PasteSOU_ID	varchar(20)		-- SOU_ID de la soumission pasté. Doit être fournir car logique dans EE
									-- Retourne : L'identité du record pasté dans la table soumis
)
AS
BEGIN
	SET NOCOUNT ON;

		-- Clone tous les records details ayant le SOU_ID reçu de la table soumission
	EXEC up_CloneRecords 'SOUREL',		'SOU_ID',	@CopySOU_ID,	@PasteSOU_ID,	'UniqueId',	'IDX_UNIQUEKEY'
	EXEC up_CloneRecords 'SOUBLO',		'SOU_ID',	@CopySOU_ID,	@PasteSOU_ID,	'UniqueId',	'IDX_UNIQUEKEY'
	EXEC up_CloneRecords 'SOUDIV',		'SOU_ID',	@CopySOU_ID,	@PasteSOU_ID,	'UniqueId',	'IDX_UNIQUEKEY'
	EXEC up_CloneRecords 'SOUAMD',		'SOU_ID',	@CopySOU_ID,	@PasteSOU_ID,	'UniqueId',	'IDX_UNIQUEKEY'
	EXEC up_CloneRecords 'SOUWEBLOG',	'SOU_ID',	@CopySOU_ID,	@PasteSOU_ID,	'UniqueId',	'IDX_UNIQUEKEY'
	EXEC up_CloneRecords 'SOUPRO',		'SOU_ID',	@CopySOU_ID,	@PasteSOU_ID,	'UniqueId',	'IDX_UNIQUEKEY'
	EXEC up_CloneRecords 'SOUENS',		'SOU_ID',	@CopySOU_ID,	@PasteSOU_ID,	'UniqueId',	'IDX_UNIQUEKEY'
	EXEC up_CloneRecords 'SOUENSCO',	'SOU_ID',	@CopySOU_ID,	@PasteSOU_ID,	'UniqueId',	'IDX_UNIQUEKEY'
	EXEC up_CloneRecords 'SOULOTS',		'SOU_ID',	@CopySOU_ID,	@PasteSOU_ID,	'UniqueId',	'IDX_UNIQUEKEY'
	EXEC up_CloneRecords 'SOULOTSCO',	'SOU_ID',	@CopySOU_ID,	@PasteSOU_ID,	'UniqueId',	'IDX_UNIQUEKEY'

		-- Clone le record d'entête et retourne l'identité du nouveau record
		-- Si ca saute avant, on vas simplement avoir un tas de détails sans entête, facile à cleaner au besoin
	EXEC up_CloneRecords 'SOUMIS',		'SOU_ID',	@CopySOU_ID,	@PasteSOU_ID,	'UniqueId',	'IDX_SOU_ID'

		-- Met à jour les informations d'entêtes
			--WEXPORTED	= 0, -- EM : Pour la version Interne, Assigner
    UPDATE SOUMIS 
		SET NODOC		= '', 
			DESCDOC		= '+ ' + DESCDOC, 
			DATECREE	= GetDate(), 
			DATEDOC		= NULL
		WHERE SOU_ID = @PasteSOU_ID


		-- Retounre l'identité du record de soumission d'entête
    DECLARE @TempResult INT

	SELECT	@TempResult = UniqueID 
		FROM  SOUMIS
		WHERE SOU_ID = @PasteSOU_ID

	RETURN @TempResult
END


GO
PRINT N'Creating [dbo].[up_CopyFactures_Full]'
GO

IF EXISTS (SELECT * FROM INFORMATION_SCHEMA.ROUTINES WHERE Routine_Type = 'PROCEDURE' AND Specific_Name = 'up_CopyFactures_Full')
  DROP PROCEDURE up_CopyFactures_Full
GO

-- =============================================
-- Author:		Eric Madore
-- Create date: 2011-10-19
-- Description:	Copy/paste la facture reçu
--				Basé sur [up_CopySoumis_Full]
-- =============================================
CREATE PROCEDURE [dbo].[up_CopyFactures_Full] (
    @CopySOU_ID		varchar(20),	-- SOU_ID de la facture à copy/paster 
	@PasteSOU_ID	varchar(20)		-- SOU_ID de la facture pasté. Doit être fournir car logique dans EE
									-- Retourne : L'identité du record pasté dans la table soumis
)
AS
BEGIN
	SET NOCOUNT ON;

		-- Clone tous les records details ayant le SOU_ID reçu de la table soumission
	EXEC up_CloneRecords 'FACREL',		'SOU_ID',	@CopySOU_ID,	@PasteSOU_ID,	'UniqueId',	'IDX_UNIQUEKEY'
	EXEC up_CloneRecords 'FACBLO',		'SOU_ID',	@CopySOU_ID,	@PasteSOU_ID,	'UniqueId',	'IDX_UNIQUEKEY'
	EXEC up_CloneRecords 'FACDIV',		'SOU_ID',	@CopySOU_ID,	@PasteSOU_ID,	'UniqueId',	'IDX_UNIQUEKEY'
	EXEC up_CloneRecords 'FACAMD',		'SOU_ID',	@CopySOU_ID,	@PasteSOU_ID,	'UniqueId',	'IDX_UNIQUEKEY'
	EXEC up_CloneRecords 'FACWEBLOG',	'SOU_ID',	@CopySOU_ID,	@PasteSOU_ID,	'UniqueId',	'IDX_UNIQUEKEY'
	EXEC up_CloneRecords 'FACPRO',		'SOU_ID',	@CopySOU_ID,	@PasteSOU_ID,	'UniqueId',	'IDX_UNIQUEKEY'
	EXEC up_CloneRecords 'FACENS',		'SOU_ID',	@CopySOU_ID,	@PasteSOU_ID,	'UniqueId',	'IDX_UNIQUEKEY'
	EXEC up_CloneRecords 'FACENSCO',	'SOU_ID',	@CopySOU_ID,	@PasteSOU_ID,	'UniqueId',	'IDX_UNIQUEKEY'
	EXEC up_CloneRecords 'FACLOTS',		'SOU_ID',	@CopySOU_ID,	@PasteSOU_ID,	'UniqueId',	'IDX_UNIQUEKEY'
	EXEC up_CloneRecords 'FACLOTSCO',	'SOU_ID',	@CopySOU_ID,	@PasteSOU_ID,	'UniqueId',	'IDX_UNIQUEKEY'

		-- Clone le record d'entête et retourne l'identité du nouveau record
		-- Si ca saute avant, on vas simplement avoir un tas de détails sans entête, facile à cleaner au besoin
	EXEC up_CloneRecords 'FACTURES',		'SOU_ID',	@CopySOU_ID,	@PasteSOU_ID,	'UniqueId',	'IDX_SOU_ID'

		-- Met à jour les informations d'entêtes
			--WEXPORTED	= 0, -- EM : Pour la version Interne, Assigner
    UPDATE FACTURES 
		SET NODOC		= '', 
			DESCDOC		= '+ ' + DESCDOC, 
			DATECREE	= GetDate(), 
			DATEDOC		= NULL
		WHERE SOU_ID = @PasteSOU_ID
	

		-- Retounre l'identité du record de soumission d'entête
    DECLARE @TempResult INT

	SELECT	@TempResult = UniqueID 
		FROM  FACTURES
		WHERE SOU_ID = @PasteSOU_ID

	RETURN @TempResult
END

GO

PRINT N'Creating [dbo].[_DBVersion]'
GO

IF NOT EXISTS (SELECT * FROM INFORMATION_SCHEMA.TABLES WHERE Table_Name = '_DBVersion')
BEGIN
  CREATE TABLE [dbo].[_DBVersion]
  (
  [DBV_VersionNo] [int] NULL,
  [DBV_VersionFrom] [int] NULL,
  [DBV_DataPath] [varchar] (256) NULL,
  [DBV_MachineID] [varchar] (128) NULL,
  [DBV_UserID] [varchar] (128) NULL,
  [DBV_SessionID] [bigint] NULL,
  [DBV_DateTimeStart] [datetime] NULL,
  [DBV_DateTimeEnd] [datetime] NULL,
  [DBV_Success] [bit] NULL,
  [DBV_Error] [varchar] (256) NOT NULL
  )
END

GO
PRINT N'Creating index [IDX_CLI_ID] on [dbo].[CLIENTS]'
GO
CREATE NONCLUSTERED INDEX [IDX_CLI_ID] ON [dbo].[CLIENTS] ([CLI_ID])
GO
PRINT N'Creating index [IDX_CONTACT] on [dbo].[CLIENTS]'
GO
CREATE NONCLUSTERED INDEX [IDX_CONTACT] ON [dbo].[CLIENTS] ([CONTACT])
GO
PRINT N'Creating index [IDX_NOMCIE] on [dbo].[CLIENTS]'
GO
CREATE NONCLUSTERED INDEX [IDX_NOMCIE] ON [dbo].[CLIENTS] ([NOMCIE])
GO
PRINT N'Creating index [IDX_NUMERO] on [dbo].[CLIENTS]'
GO
CREATE NONCLUSTERED INDEX [IDX_NUMERO] ON [dbo].[CLIENTS] ([NUMERO])
GO
PRINT N'Creating index [IDX_TYPE_FICHE] on [dbo].[CLIENTS]'
GO
CREATE NONCLUSTERED INDEX [IDX_TYPE_FICHE] ON [dbo].[CLIENTS] ([TYPEFICHE])
GO
PRINT N'Creating index [IDX_UNIQUEKEY] on [dbo].[CLITAUX]'
GO
CREATE NONCLUSTERED INDEX [IDX_UNIQUEKEY] ON [dbo].[CLITAUX] ([CLI_ID], [ORDRE])
GO
PRINT N'Creating index [IDX_COM_ID] on [dbo].[COMMANDE]'
GO
CREATE NONCLUSTERED INDEX [IDX_COM_ID] ON [dbo].[COMMANDE] ([COM_ID])
GO
PRINT N'Creating index [IDX_COM_NO] on [dbo].[COMMANDE]'
GO
CREATE NONCLUSTERED INDEX [IDX_COM_NO] ON [dbo].[COMMANDE] ([COM_NO])
GO
PRINT N'Creating index [IDX_JOB_NO] on [dbo].[COMMANDE]'
GO
CREATE NONCLUSTERED INDEX [IDX_JOB_NO] ON [dbo].[COMMANDE] ([JOB_NO])
GO
PRINT N'Creating index [IDX_ORDERED_NO] on [dbo].[COMMANDE]'
GO
CREATE NONCLUSTERED INDEX [IDX_ORDERED_NO] ON [dbo].[COMMANDE] ([ORDERED_NO])
GO
PRINT N'Creating index [IDX_COM_ID] on [dbo].[COMMITEM]'
GO
CREATE NONCLUSTERED INDEX [IDX_COM_ID] ON [dbo].[COMMITEM] ([COM_ID], [ORDRE])
GO
PRINT N'Creating index [IDX_PRO_ID] on [dbo].[COMMITEM]'
GO
CREATE NONCLUSTERED INDEX [IDX_PRO_ID] ON [dbo].[COMMITEM] ([PRO_ID])
GO
PRINT N'Creating index [IDX_ORDRE] on [dbo].[DEFBLO]'
GO
CREATE NONCLUSTERED INDEX [IDX_ORDRE] ON [dbo].[DEFBLO] ([ORDRE])
GO
PRINT N'Creating index [IDX_ORDRE] on [dbo].[DEFDIV]'
GO
CREATE NONCLUSTERED INDEX [IDX_ORDRE] ON [dbo].[DEFDIV] ([ORDRE])
GO
PRINT N'Creating index [IDX_ENS_ID] on [dbo].[ENSCOMPO]'
GO
CREATE NONCLUSTERED INDEX [IDX_ENS_ID] ON [dbo].[ENSCOMPO] ([ENS_ID], [ORDRE])
GO
PRINT N'Creating index [IDX_PRO_ID] on [dbo].[ENSCOMPO]'
GO
CREATE NONCLUSTERED INDEX [IDX_PRO_ID] ON [dbo].[ENSCOMPO] ([PRO_ID])
GO
PRINT N'Creating index [IDX_UNIQUEKEY] on [dbo].[FACAMD]'
GO
CREATE NONCLUSTERED INDEX [IDX_UNIQUEKEY] ON [dbo].[FACAMD] ([SOU_ID], [BLO_ID], [DIV_ID])
GO
PRINT N'Creating index [IDX_UNIQUEKEY] on [dbo].[FACBLO]'
GO
CREATE NONCLUSTERED INDEX [IDX_UNIQUEKEY] ON [dbo].[FACBLO] ([SOU_ID], [BLO_ID])
GO
PRINT N'Creating index [IDX_UNIQUEKEY] on [dbo].[FACDIV]'
GO
CREATE NONCLUSTERED INDEX [IDX_UNIQUEKEY] ON [dbo].[FACDIV] ([SOU_ID], [DIV_ID])
GO
PRINT N'Creating index [IDX_ENS_ID] on [dbo].[FACENSCO]'
GO
CREATE NONCLUSTERED INDEX [IDX_ENS_ID] ON [dbo].[FACENSCO] ([ENS_ID], [ORDRE])
GO
PRINT N'Creating index [IDX_UNIQUEKEY] on [dbo].[FACENSCO]'
GO
CREATE NONCLUSTERED INDEX [IDX_UNIQUEKEY] ON [dbo].[FACENSCO] ([SOU_ID], [ENS_ID], [PRO_ID])
GO
PRINT N'Creating index [IDX_LOTS_ID] on [dbo].[FACLOTSCO]'
GO
CREATE NONCLUSTERED INDEX [IDX_LOTS_ID] ON [dbo].[FACLOTSCO] ([LOTS_ID], [ORDRE])
GO
PRINT N'Creating index [IDX_UNIQUEKEY] on [dbo].[FACLOTSCO]'
GO
CREATE NONCLUSTERED INDEX [IDX_UNIQUEKEY] ON [dbo].[FACLOTSCO] ([SOU_ID], [LOTS_ID], [PRO_ID])
GO
PRINT N'Creating index [IDX_UNIQUEKEY] on [dbo].[FACPRO]'
GO
CREATE NONCLUSTERED INDEX [IDX_UNIQUEKEY] ON [dbo].[FACPRO] ([SOU_ID], [PRO_ID])
GO
PRINT N'Creating index [IDX_UNIQUEKEY] on [dbo].[FACREL]'
GO
CREATE NONCLUSTERED INDEX [IDX_UNIQUEKEY] ON [dbo].[FACREL] ([SOU_ID], [TYPERELEVE], [BLO_ID], [DIV_ID], [ORDRE])
GO
PRINT N'Creating index [IDX_UNIQUEKEY] on [dbo].[FACWEBLOG]'
GO
CREATE NONCLUSTERED INDEX [IDX_UNIQUEKEY] ON [dbo].[FACWEBLOG] ([SOU_ID], [TRF_DATE] DESC)
GO
PRINT N'Creating index [IDX_ORDRE] on [dbo].[FRAIS]'
GO
CREATE NONCLUSTERED INDEX [IDX_ORDRE] ON [dbo].[FRAIS] ([ORDRE])
GO
PRINT N'Creating index [IDX_NOTE_ID] on [dbo].[NOTES]'
GO
CREATE NONCLUSTERED INDEX [IDX_NOTE_ID] ON [dbo].[NOTES] ([NOTE_ID])
GO
PRINT N'Creating index [IDX_PRO_ID] on [dbo].[PriceUpdate_Products]'
GO
CREATE NONCLUSTERED INDEX [IDX_PRO_ID] ON [dbo].[PriceUpdate_Products] ([PRO_ID])
GO
PRINT N'Creating index [IDX_CLEDIST] on [dbo].[PRODUITS]'
GO
CREATE NONCLUSTERED INDEX [IDX_CLEDIST] ON [dbo].[PRODUITS] ([CLEDIST])
GO
PRINT N'Creating index [IDX_CLEMANU] on [dbo].[PRODUITS]'
GO
CREATE NONCLUSTERED INDEX [IDX_CLEMANU] ON [dbo].[PRODUITS] ([CLEMANU])
GO
PRINT N'Creating index [IDX_CLEPERS] on [dbo].[PRODUITS]'
GO
CREATE NONCLUSTERED INDEX [IDX_CLEPERS] ON [dbo].[PRODUITS] ([CLEPERS])
GO
PRINT N'Creating index [IDX_CODECAT] on [dbo].[PRODUITS]'
GO
CREATE NONCLUSTERED INDEX [IDX_CODECAT] ON [dbo].[PRODUITS] ([CODECAT])
GO
PRINT N'Creating index [IDX_NOUVEAU] on [dbo].[PRODUITS]'
GO
CREATE NONCLUSTERED INDEX [IDX_NOUVEAU] ON [dbo].[PRODUITS] ([NOUVEAU])
GO
PRINT N'Creating index [IDX_PRO_ID] on [dbo].[PRODUITS]'
GO
CREATE NONCLUSTERED INDEX [IDX_PRO_ID] ON [dbo].[PRODUITS] ([PRO_ID])
GO
PRINT N'Creating index [IDX_UNIQUEKEY] on [dbo].[SOUAMD]'
GO
CREATE NONCLUSTERED INDEX [IDX_UNIQUEKEY] ON [dbo].[SOUAMD] ([SOU_ID], [BLO_ID], [DIV_ID])
GO
PRINT N'Creating index [IDX_UNIQUEKEY] on [dbo].[SOUBLO]'
GO
CREATE NONCLUSTERED INDEX [IDX_UNIQUEKEY] ON [dbo].[SOUBLO] ([SOU_ID], [BLO_ID])
GO
PRINT N'Creating index [IDX_UNIQUEKEY] on [dbo].[SOUDIV]'
GO
CREATE NONCLUSTERED INDEX [IDX_UNIQUEKEY] ON [dbo].[SOUDIV] ([SOU_ID], [DIV_ID])
GO
PRINT N'Creating index [IDX_ENS_ID] on [dbo].[SOUENSCO]'
GO
CREATE NONCLUSTERED INDEX [IDX_ENS_ID] ON [dbo].[SOUENSCO] ([ENS_ID], [ORDRE])
GO
PRINT N'Creating index [IDX_UNIQUEKEY] on [dbo].[SOUENSCO]'
GO
CREATE NONCLUSTERED INDEX [IDX_UNIQUEKEY] ON [dbo].[SOUENSCO] ([SOU_ID], [ENS_ID], [PRO_ID])
GO
PRINT N'Creating index [IDX_LOTS_ID] on [dbo].[SOULOTSCO]'
GO
CREATE NONCLUSTERED INDEX [IDX_LOTS_ID] ON [dbo].[SOULOTSCO] ([LOTS_ID], [ORDRE])
GO
PRINT N'Creating index [IDX_UNIQUEKEY] on [dbo].[SOULOTSCO]'
GO
CREATE NONCLUSTERED INDEX [IDX_UNIQUEKEY] ON [dbo].[SOULOTSCO] ([SOU_ID], [LOTS_ID], [PRO_ID])
GO
PRINT N'Creating index [IDX_UNIQUEKEY] on [dbo].[SOUPRO]'
GO
CREATE NONCLUSTERED INDEX [IDX_UNIQUEKEY] ON [dbo].[SOUPRO] ([SOU_ID], [PRO_ID])
GO
PRINT N'Creating index [IDX_UNIQUEKEY] on [dbo].[SOUREL]'
GO
CREATE NONCLUSTERED INDEX [IDX_UNIQUEKEY] ON [dbo].[SOUREL] ([SOU_ID], [TYPERELEVE], [BLO_ID], [DIV_ID], [ORDRE])
GO
PRINT N'Creating index [IDX_UNIQUEKEY] on [dbo].[SOUWEBLOG]'
GO
CREATE NONCLUSTERED INDEX [IDX_UNIQUEKEY] ON [dbo].[SOUWEBLOG] ([SOU_ID], [TRF_DATE] DESC)
GO
PRINT N'Creating index [IDX_ORDRE] on [dbo].[TAUX]'
GO
CREATE NONCLUSTERED INDEX [IDX_ORDRE] ON [dbo].[TAUX] ([ORDRE])
GO
PRINT N'Creating index [IDX_PROVINCE] on [dbo].[TAXDEF]'
GO
CREATE NONCLUSTERED INDEX [IDX_PROVINCE] ON [dbo].[TAXDEF] ([PROVINCE], [DATEDEB] DESC)
GO
PRINT N'Creating index [IDX_TAX_ID] on [dbo].[TAXDEF]'
GO
CREATE NONCLUSTERED INDEX [IDX_TAX_ID] ON [dbo].[TAXDEF] ([TAX_ID])
GO
