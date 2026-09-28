/*
Script created by SQL Compare version 6.2.1 from Red Gate Software Ltd at 2014-08-12 08:39:32
Run this script on D00106\EEWIN.EEWin_3_126 to make it the same as D00106\EEWIN.EEWin_3_128
Please back up your database before running this script
*/
SET NUMERIC_ROUNDABORT OFF
GO
SET ANSI_PADDING, ANSI_WARNINGS, CONCAT_NULL_YIELDS_NULL, ARITHABORT, QUOTED_IDENTIFIER, ANSI_NULLS ON
GO
IF EXISTS (SELECT * FROM tempdb..sysobjects WHERE id=OBJECT_ID('tempdb..#tmpErrors')) DROP TABLE #tmpErrors
GO
CREATE TABLE [dbo].#tmpErrors (Error int)
GO
SET XACT_ABORT ON
GO
SET TRANSACTION ISOLATION LEVEL SERIALIZABLE
GO
BEGIN TRANSACTION
GO
PRINT N'Altering [dbo].[FACENS]'
GO
ALTER TABLE [dbo].[FACENS] ADD
[ENS_ORG_ID] [varchar] (20) COLLATE French_CI_AS NULL
GO
IF @@ERROR<>0 AND @@TRANCOUNT>0 ROLLBACK TRANSACTION
GO
IF @@TRANCOUNT=0 BEGIN INSERT INTO #tmpErrors (Error) SELECT 1 BEGIN TRANSACTION END
GO
PRINT N'Altering [dbo].[up_FACENS_Update]'
GO
ALTER PROCEDURE [dbo].[up_FACENS_Update] (
  @UniqueId bigint,
  @SOU_ID varchar(20),
  @ENS_ID varchar(20),
  @ENS_ORG_ID varchar(20), -- 2014-08-12 EMadore V6 : New
  @DESC varchar(60),       -- 2012-01-19 EMadore V3 : Passage de 40 à 60 chars
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
    FACENS
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

  --Return updated ID
  RETURN @UniqueId
END


GO
IF @@ERROR<>0 AND @@TRANCOUNT>0 ROLLBACK TRANSACTION
GO
IF @@TRANCOUNT=0 BEGIN INSERT INTO #tmpErrors (Error) SELECT 1 BEGIN TRANSACTION END
GO
PRINT N'Altering [dbo].[FACREL]'
GO
ALTER TABLE [dbo].[FACREL] ADD
[EXT_ID] [varchar] (20) COLLATE French_CI_AS NULL
GO
IF @@ERROR<>0 AND @@TRANCOUNT>0 ROLLBACK TRANSACTION
GO
IF @@TRANCOUNT=0 BEGIN INSERT INTO #tmpErrors (Error) SELECT 1 BEGIN TRANSACTION END
GO
PRINT N'Altering [dbo].[FACTURES]'
GO
ALTER TABLE [dbo].[FACTURES] ADD
[ORIGIN] [char] (1) COLLATE French_CI_AS NULL,
[ORIGINREF] [varchar] (200) COLLATE French_CI_AS NULL,
[EXTAPP] [char] (1) COLLATE French_CI_AS NULL,
[EXTFILE] [varchar] (200) COLLATE French_CI_AS NULL
GO
IF @@ERROR<>0 AND @@TRANCOUNT>0 ROLLBACK TRANSACTION
GO
IF @@TRANCOUNT=0 BEGIN INSERT INTO #tmpErrors (Error) SELECT 1 BEGIN TRANSACTION END
GO
PRINT N'Altering [dbo].[up_FACTURES_Update]'
GO
ALTER PROCEDURE [dbo].[up_FACTURES_Update] (
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
  @EST_NAME varchar(50)
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
    SysDate = GETDATE()
  WHERE
    UniqueId = @UniqueId

  --Return updated ID
  RETURN @UniqueId
END


GO
IF @@ERROR<>0 AND @@TRANCOUNT>0 ROLLBACK TRANSACTION
GO
IF @@TRANCOUNT=0 BEGIN INSERT INTO #tmpErrors (Error) SELECT 1 BEGIN TRANSACTION END
GO
PRINT N'Altering [dbo].[SOUENS]'
GO
ALTER TABLE [dbo].[SOUENS] ADD
[ENS_ORG_ID] [varchar] (20) COLLATE French_CI_AS NULL
GO
IF @@ERROR<>0 AND @@TRANCOUNT>0 ROLLBACK TRANSACTION
GO
IF @@TRANCOUNT=0 BEGIN INSERT INTO #tmpErrors (Error) SELECT 1 BEGIN TRANSACTION END
GO
PRINT N'Altering [dbo].[up_SOUENS_Update]'
GO
ALTER PROCEDURE [dbo].[up_SOUENS_Update] (
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

  --Return updated ID
  RETURN @UniqueId
END

GO
IF @@ERROR<>0 AND @@TRANCOUNT>0 ROLLBACK TRANSACTION
GO
IF @@TRANCOUNT=0 BEGIN INSERT INTO #tmpErrors (Error) SELECT 1 BEGIN TRANSACTION END
GO
PRINT N'Altering [dbo].[SOUMIS]'
GO
ALTER TABLE [dbo].[SOUMIS] ADD
[ORIGIN] [char] (1) COLLATE French_CI_AS NULL,
[ORIGINREF] [varchar] (200) COLLATE French_CI_AS NULL,
[EXTAPP] [char] (1) COLLATE French_CI_AS NULL,
[EXTFILE] [varchar] (200) COLLATE French_CI_AS NULL
GO
IF @@ERROR<>0 AND @@TRANCOUNT>0 ROLLBACK TRANSACTION
GO
IF @@TRANCOUNT=0 BEGIN INSERT INTO #tmpErrors (Error) SELECT 1 BEGIN TRANSACTION END
GO
PRINT N'Altering [dbo].[up_SOUMIS_Update]'
GO
ALTER PROCEDURE [dbo].[up_SOUMIS_Update] (
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
  @EST_NAME varchar(50)
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
    SysDate = GETDATE()
  WHERE
    UniqueId = @UniqueId

  --Return updated ID
  RETURN @UniqueId
END


GO
IF @@ERROR<>0 AND @@TRANCOUNT>0 ROLLBACK TRANSACTION
GO
IF @@TRANCOUNT=0 BEGIN INSERT INTO #tmpErrors (Error) SELECT 1 BEGIN TRANSACTION END
GO
PRINT N'Altering [dbo].[SOUREL]'
GO
ALTER TABLE [dbo].[SOUREL] ADD
[EXT_ID] [varchar] (20) COLLATE French_CI_AS NULL
GO
IF @@ERROR<>0 AND @@TRANCOUNT>0 ROLLBACK TRANSACTION
GO
IF @@TRANCOUNT=0 BEGIN INSERT INTO #tmpErrors (Error) SELECT 1 BEGIN TRANSACTION END
GO
PRINT N'Altering [dbo].[up_SOUREL_Update]'
GO
ALTER PROCEDURE [dbo].[up_SOUREL_Update] (
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
  @PROFITMOIN float
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
    SysDate = GETDATE()
  WHERE
    UniqueId = @UniqueId

  --Return updated ID
  RETURN @UniqueId
END
GO
IF @@ERROR<>0 AND @@TRANCOUNT>0 ROLLBACK TRANSACTION
GO
IF @@TRANCOUNT=0 BEGIN INSERT INTO #tmpErrors (Error) SELECT 1 BEGIN TRANSACTION END
GO
PRINT N'Altering [dbo].[up_CopySoumis_Full]'
GO
--  =============================================
--  Author:		Eric Madore
--  Create date: 2011-10-19
--  Description:	Copy/paste la soumission reçu
--  Modifications :
--    2014-07-31 EMadore :
--      Assignation de l'origine des copy/paste  
--  =============================================

ALTER PROCEDURE [dbo].[up_CopySoumis_Full] (
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
    UPDATE 
      SOUMIS 
		SET 
      ORIGIN    = 'C',    -- TO_CopyPaste en Delphi
      ORIGINREF = @PasteSOU_ID,
      NODOC		  = '', 
			DESCDOC		= '+ ' + DESCDOC, 
			DATECREE	= GetDate(), 
			DATEDOC		= NULL
		WHERE 
      SOU_ID = @PasteSOU_ID

		-- Retounre l'identité du record de soumission d'entête
    DECLARE @TempResult INT

	SELECT	@TempResult = UniqueID 
		FROM  SOUMIS
		WHERE SOU_ID = @PasteSOU_ID

	RETURN @TempResult
END


GO
IF @@ERROR<>0 AND @@TRANCOUNT>0 ROLLBACK TRANSACTION
GO
IF @@TRANCOUNT=0 BEGIN INSERT INTO #tmpErrors (Error) SELECT 1 BEGIN TRANSACTION END
GO
PRINT N'Altering [dbo].[up_CopyFactures_Full]'
GO
--  =============================================
--  Author:		Eric Madore
--  Create date: 2011-10-19
--  Description:	
--    Copy/paste la facture reçu
--    Basé sur [up_CopySoumis_Full]
--  Modifications :
--    2014-07-31 EMadore :
--      Assignation de l'origine des copy/paste  
--  =============================================
ALTER PROCEDURE [dbo].[up_CopyFactures_Full] (
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
    UPDATE 
      FACTURES 
		SET 
      ORIGIN    = 'C',          -- TO_CopyPaste en Delphi
      ORIGINREF = @CopySOU_ID,  
      NODOC		  = '', 
			DESCDOC		= '+ ' + DESCDOC, 
			DATECREE	= GetDate(), 
			DATEDOC		= NULL
		WHERE 
      SOU_ID = @PasteSOU_ID
	
		-- Retounre l'identité du record de soumission d'entête
    DECLARE @TempResult INT

	SELECT	@TempResult = UniqueID 
		FROM  FACTURES
		WHERE SOU_ID = @PasteSOU_ID

	RETURN @TempResult
END



GO
IF @@ERROR<>0 AND @@TRANCOUNT>0 ROLLBACK TRANSACTION
GO
IF @@TRANCOUNT=0 BEGIN INSERT INTO #tmpErrors (Error) SELECT 1 BEGIN TRANSACTION END
GO
IF EXISTS (SELECT * FROM #tmpErrors) ROLLBACK TRANSACTION
GO
IF @@TRANCOUNT>0 BEGIN
PRINT 'The database update succeeded'
COMMIT TRANSACTION
END
ELSE PRINT 'The database update failed'
GO
DROP TABLE #tmpErrors
GO
