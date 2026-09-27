
  -- New field - SOUMIS.USER_ID
IF NOT EXISTS (
  SELECT 
    TOP 1 *
  FROM 
    INFORMATION_SCHEMA.COLUMNS
  WHERE 
        [TABLE_NAME]  = 'SOUMIS'
    AND [COLUMN_NAME] = 'USER_ID' )
BEGIN
  ALTER TABLE
    SOUMIS
  ADD
    USER_ID  VARCHAR(20);
END
GO

  -- New field - SOUMIS.BRANCH_ID
IF NOT EXISTS (
  SELECT 
    TOP 1 *
  FROM 
    INFORMATION_SCHEMA.COLUMNS
  WHERE 
        [TABLE_NAME]  = 'SOUMIS'
    AND [COLUMN_NAME] = 'BRANCH_ID' )
BEGIN
  ALTER TABLE
    SOUMIS
  ADD
    BRANCH_ID  VARCHAR(20);
END
GO

  -- New field - SOUMIS.OWC
IF NOT EXISTS (
  SELECT 
    TOP 1 *
  FROM 
    INFORMATION_SCHEMA.COLUMNS
  WHERE 
        [TABLE_NAME]  = 'SOUMIS'
    AND [COLUMN_NAME] = 'OWC' )
BEGIN
  ALTER TABLE
    SOUMIS
  ADD
    OWC  VARCHAR(2);
END
GO


  -- New field - BDEE.CUSTDESC
IF NOT EXISTS (
  SELECT 
    TOP 1 *
  FROM 
    INFORMATION_SCHEMA.COLUMNS
  WHERE 
        [TABLE_NAME]  = 'BDEE'
    AND [COLUMN_NAME] = 'CUSTDESC' )
BEGIN
  ALTER TABLE
    BDEE
  ADD
    CUSTDESC  VARCHAR(30);
END
GO


IF OBJECT_ID(N'dbo.up_BDEE_Update', N'P') IS NOT NULL 
    DROP PROCEDURE dbo.up_BDEE_Update ;
GO

CREATE PROCEDURE [dbo].[up_BDEE_Update] (
  @UniqueId bigint,
  @LVERSION	  int,
  @CODEVER	  varchar(20),
  @DATA       varchar(30),
  @NODIST	    varchar(12),
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
  @LICENCEKEY	varchar(128),
  @CUSTDESC   varchar(30)  
  
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
	CUSTDESC,
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
	@CUSTDESC,
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
	CUSTDESC    = @CUSTDESC,
    SysDate     = GETDATE()
  WHERE
    UniqueId = @UniqueId

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

  --Return updated ID
  RETURN @UniqueId
END
GO



IF OBJECT_ID(N'dbo.EE_Calgary', N'FN') IS NOT NULL 
    DROP FUNCTION dbo.EE_Calgary ;
GO


CREATE FUNCTION [dbo].EE_Calgary()
RETURNS BIT
AS BEGIN
   DECLARE @RES  BIT

IF NOT EXISTS (
  SELECT 
    TOP 1 *
  FROM 
    INFORMATION_SCHEMA.COLUMNS
  WHERE 
        [TABLE_NAME]  = 'PRODUITS'
    AND [COLUMN_NAME] = 'LC' )
BEGIN
  SET @RES = 0;
END ELSE
BEGIN
  SET @RES = 1;
END;

RETURN @RES;

END
GO


IF OBJECT_ID(N'dbo.up_PriceUpdate_UpdateProducts', N'P') IS NOT NULL 
    DROP PROCEDURE dbo.up_PriceUpdate_UpdateProducts ;
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

-- Traitement pours logique de prix Wolseley pour les clients régulier
UPDATE PRODUITS
SET 
  --Si la description personnelle n'a jamais ete modifiee alors on peut se permettre de la mettre a jour
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
  AND (LEFT(PRODUITS.PRO_ID, 3) IN ('WOP', 'WQP', 'WEP', 'WWP') AND (dbo.EE_Calgary() = 0))

  -- Traitement pour les clients Sonepar (Lumen, Sesco, Gescan) ainsi que pour les employés de Wolseley (Interne / EE_Calgary)
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
  -- PRODUITS.DATECOUNET = CASE WHEN LEFT(PRODUITS.PRO_ID, 3) IN ('NWE', 'NOE', 'NQE', 'NME', 'WAE', 'WME', 'WOE', 'WQE') THEN PRODUITS.DATECOUNET ELSE PriceUpdate_Products.DATECOUT END  -- Date Prix net = Date cout brut pour Wosleley (validÃ© ici comme pas Rexel)
FROM
  PRODUITS 
  INNER JOIN PriceUpdate_Products
  ON PRODUITS.PRO_ID = PriceUpdate_Products.PRO_ID
WHERE
  LEFT(PRODUITS.PRO_ID, 3) IN ('NWE', 'NOE', 'NQE', 'NME', 'WAE', 'WME', 'WOE', 'WQE', 'LQE','GSE','SOE')
  OR (LEFT(PRODUITS.PRO_ID, 3) IN ('WOP', 'WQP', 'WEP', 'WWP') AND (dbo.EE_Calgary() = 1))
END
GO
