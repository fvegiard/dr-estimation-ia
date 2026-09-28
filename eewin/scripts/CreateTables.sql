/******************************************************************************/
/* Création des tables propre à la version standard de EE                     */
/* Ces tables doivents être en tout temps identique à ceux déclarés dans le   */
/* fichier CreateTables_Calgary.sql SAUF pour les tables ayant des champs     */
/* exclusifs à la version interne. Ces champs ne doivent JAMAIS aparaitre     */  
/* dans ce fichier. Utiliser Beyond Compare au besoin pour s'assurer de       */
/* l'exactitude des table                                                     */ 
/******************************************************************************/

CREATE TABLE [dbo].[BDEE](
	[UniqueId] [bigint] IDENTITY(1,1) NOT NULL,
	[CODEVER] [varchar](20) NULL,
	[DATA] [varchar](30) NULL,
	[DESCR] [varchar](40) NULL,
	[URLFR] [varchar](100) NULL,
	[URLEN] [varchar](100) NULL,
	[SysDate] [datetime] NOT NULL DEFAULT (getdate()),
  CONSTRAINT [PK_BDEE] PRIMARY KEY CLUSTERED ([UniqueId] ASC)
)
GO

CREATE TABLE [dbo].[CLIENTS](
	[UniqueId] [bigint] IDENTITY(1,1) NOT NULL,
	[CLI_ID] [varchar](20) NULL,
	[TYPEFICHE] [varchar](1) NULL,
	[NUMERO] [varchar](20) NULL,
	[NOMCIE] [varchar](50) NULL,
	[CONTACT] [varchar](50) NULL,
	[RUE1] [varchar](50) NULL,
	[RUE2] [varchar](50) NULL,
	[VILLE] [varchar](40) NULL,
	[CODEPOSTAL] [varchar](7) NULL,
	[PROVINCE] [varchar](40) NULL,
	[PAYS] [varchar](40) NULL,
	[BOITEPOSTA] [varchar](30) NULL,
	[TEL1] [varchar](20) NULL,
	[TEL2] [varchar](20) NULL,
	[TEL3] [varchar](20) NULL,
	[FAX] [varchar](20) NULL,
	[PROFIT] [float] NULL,
	[TVFAPPL] [bit] NULL,
	[TVPAPPL] [bit] NULL,
	[NOTES] [text] NULL,
	[EMAIL] [varchar](80) NULL,
	[SITEWEB] [varchar](80) NULL,
	[SYSTEM] [bit] NULL,
	[SysDate] [datetime] NOT NULL DEFAULT (getdate()),
  CONSTRAINT [PK_CLIENTS] PRIMARY KEY CLUSTERED ([UniqueId] ASC)
)
GO

CREATE TABLE [dbo].[CLITAUX](
	[UniqueId] [bigint] IDENTITY(1,1) NOT NULL,
	[CLI_ID] [varchar](20) NULL,
	[ORDRE] [varchar](6) NULL,
	[DESCTAUX] [varchar](50) NULL,
	[COUTUNI] [float] NULL,
	[PROFIT] [float] NULL,
	[SysDate] [datetime] NOT NULL DEFAULT (getdate()),
  CONSTRAINT [PK_CLITAUX] PRIMARY KEY CLUSTERED ([UniqueId] ASC)
)
GO

CREATE TABLE [dbo].[COMMANDE](
	[UniqueId] [bigint] IDENTITY(1,1) NOT NULL,
	[COM_ID] [varchar](20) NULL,
	[COM_NO] [varchar](12) NULL,
	[SOU_ID] [varchar](20) NULL,
	[JOB_NO] [varchar](12) NULL,
	[DESCR] [varchar](60) NULL,
	[DATE_CREE] [datetime] NULL,
	[DATE_COM] [datetime] NULL,
	[DATE_LIVR] [datetime] NULL,
	[INSTRUCT] [text] NULL,
	[NOTES] [text] NULL,
	[ORDERED_ID] [varchar](20) NULL,
	[ORDERED_NO] [varchar](20) NULL,
	[BILLEDIDX] [int] NULL,
	[BILLED_ID] [varchar](20) NULL,
	[BILLED_NO] [varchar](20) NULL,
	[DELIVERIDX] [int] NULL,
	[DELIVER_ID] [varchar](20) NULL,
	[DELIVER_NO] [varchar](20) NULL,
	[COMTOTAL] [float] NULL,
	[SysDate] [datetime] NOT NULL DEFAULT (getdate()),
  CONSTRAINT [PK_COMMANDE] PRIMARY KEY CLUSTERED ([UniqueId] ASC)
)
GO

CREATE TABLE [dbo].[COMMITEM](
	[UniqueId] [bigint] IDENTITY(1,1) NOT NULL,
	[COM_ID] [varchar](20) NULL,
	[ORDRE] [varchar](6) NULL,
	[PRO_ID] [varchar](20) NULL,
	[CLEMANU] [varchar](20) NULL,
	[CLEDIST] [varchar](20) NULL,
	[CLEPERS] [varchar](20) NULL,
	[PRO_TYPE] [varchar](1) NULL,
	[DESCR] [varchar](60) NULL,
	[QTE_TOT] [float] NULL,
	[COUBRUTUNI] [float] NULL,
	[COUUM] [varchar](2) NULL,
	[COUESC] [float] NULL,
	[PROMCOUNET] [float] NULL,
	[QPP] [float] NULL,
	[MULCOM] [float] NULL,
	[CODEIMPR] [varchar](2) NULL,
	[NOTES] [TEXT] NULL, -- V2.#0001
	[SysDate] [datetime] NOT NULL DEFAULT (getdate()),
  CONSTRAINT [PK_COMMITEM] PRIMARY KEY CLUSTERED ([UniqueId] ASC)
)
GO

CREATE TABLE [dbo].[DEFBLO](
	[UniqueId] [bigint] IDENTITY(1,1) NOT NULL,
	[ORDRE] [varchar](6) NULL,
	[DESC] [varchar](40) NULL,
	[MULT] [int] NULL,
	[INCLSOU] [bit] NULL,
	[INCLFAC] [bit] NULL,
	[SYSTEM] [bit] NULL,
	[SysDate] [datetime] NOT NULL DEFAULT (getdate()),
  CONSTRAINT [PK_DEFBLO] PRIMARY KEY CLUSTERED ([UniqueId] ASC)
)
GO

CREATE TABLE [dbo].[DEFDIV](
	[UniqueId] [bigint] IDENTITY(1,1) NOT NULL,
	[ORDRE] [varchar](6) NULL,
	[DESC] [varchar](40) NULL,
	[INCLSOU] [bit] NULL,
	[INCLFAC] [bit] NULL,
	[SYSTEM] [bit] NULL,
	[SysDate] [datetime] NOT NULL DEFAULT (getdate()),
  CONSTRAINT [PK_DEFDIV] PRIMARY KEY CLUSTERED ([UniqueId] ASC)
)
GO

CREATE TABLE [dbo].[ENSCOMPO](
	[UniqueId] [bigint] IDENTITY(1,1) NOT NULL,
	[ENS_ID] [varchar](20) NULL,
	[ORDRE] [varchar](6) NULL,
	[PRO_ID] [varchar](20) NULL,
	[QTE] [float] NULL,
	[QTEUM] [varchar](2) NULL,
	[TYPRATIO] [varchar](1) NULL,
	[DIV] [float] NULL,
	[DIVUM] [varchar](2) NULL,
	[SysDate] [datetime] NOT NULL DEFAULT (getdate()),
  CONSTRAINT [PK_ENSCOMPO] PRIMARY KEY CLUSTERED ([UniqueId] ASC)
)
GO

CREATE TABLE [dbo].[ENSEMBLE](
	[UniqueId] [bigint] IDENTITY(1,1) NOT NULL,
	[ENS_ID] [varchar](20) NULL,
	[CLEPERS] [varchar](20) NULL,
	[DESC] [varchar](40) NULL,
	[COUUM] [varchar](2) NULL,
	[PROFIT] [float] NULL,
	[TEMPSEC] [float] NULL,
	[TEMPUNI] [float] NULL,
	[TEMPUM] [varchar](2) NULL,
	[DATECREE] [datetime] NULL,
	[OLDESTPROD] [datetime] NULL,
	[SYSTEM] [bit] NULL,
	[USES_DISC] [bit] NULL,
	[SysDate] [datetime] NOT NULL DEFAULT (getdate()),
  CONSTRAINT [PK_ENSEMBLE] PRIMARY KEY CLUSTERED ([UniqueId] ASC)
)
GO

CREATE TABLE [dbo].[FACAMD](
	[UniqueId] [bigint] IDENTITY(1,1) NOT NULL,
	[SOU_ID] [varchar](20) NULL,
	[BLO_ID] [varchar](3) NULL,
	[DIV_ID] [varchar](3) NULL,
	[FACTMD] [float] NULL,
	[SysDate] [datetime] NOT NULL DEFAULT (getdate()),
  CONSTRAINT [PK_FACAMD] PRIMARY KEY CLUSTERED ([UniqueId] ASC)
)
GO

CREATE TABLE [dbo].[FACBLO](
	[UniqueId] [bigint] IDENTITY(1,1) NOT NULL,
	[SOU_ID] [varchar](20) NULL,
	[BLO_ID] [varchar](3) NULL,
	[DESC] [varchar](40) NULL,
	[MULT] [int] NULL,
	[SysDate] [datetime] NOT NULL DEFAULT (getdate()),
  CONSTRAINT [PK_FACBLO] PRIMARY KEY CLUSTERED ([UniqueId] ASC)
)
GO

CREATE TABLE [dbo].[FACDIV](
	[UniqueId] [bigint] IDENTITY(1,1) NOT NULL,
	[SOU_ID] [varchar](20) NULL,
	[DIV_ID] [varchar](3) NULL,
	[DESC] [varchar](40) NULL,
	[SysDate] [datetime] NOT NULL DEFAULT (getdate()),
  CONSTRAINT [PK_FACDIV] PRIMARY KEY CLUSTERED ([UniqueId] ASC)
)
GO

CREATE TABLE [dbo].[FACENS](
	[UniqueId] [bigint] IDENTITY(1,1) NOT NULL,
	[SOU_ID] [varchar](20) NULL,
	[ENS_ID] [varchar](20) NULL,
	[DESC] [varchar](40) NULL,
	[QTETOT] [float] NULL,
	[QTETOTSECT] [float] NULL,
	[CALCTIMSTP] [varchar](14) NULL,
	[COUUM] [varchar](2) NULL,
	[TEMPUNI] [float] NULL,
	[TEMPSEC] [float] NULL,
	[TEMPUM] [varchar](2) NULL,
	[DATECREE] [datetime] NULL,
	[OLDESTPROD] [datetime] NULL,
	[CLEPERS] [varchar](40) NULL,
	[PROFIT] [float] NULL,
	[SysDate] [datetime] NOT NULL DEFAULT (getdate()),
  CONSTRAINT [PK_FACENS] PRIMARY KEY CLUSTERED ([UniqueId] ASC)
)
GO

CREATE TABLE [dbo].[FACENSCO](
	[UniqueId] [bigint] IDENTITY(1,1) NOT NULL,
	[SOU_ID] [varchar](20) NULL,
	[ENS_ID] [varchar](20) NULL,
	[PRO_ID] [varchar](20) NULL,
	[ORDRE] [varchar](6) NULL,
	[QTE] [float] NULL,
	[QTEUM] [varchar](2) NULL,
	[TYPRATIO] [varchar](1) NULL,
	[DIV] [float] NULL,
	[DIVUM] [varchar](2) NULL,
	[SysDate] [datetime] NOT NULL DEFAULT (getdate()),
  CONSTRAINT [PK_FACENSCO] PRIMARY KEY CLUSTERED ([UniqueId] ASC)
)
GO

CREATE TABLE [dbo].[FACLOTS](
	[UniqueId] [bigint] IDENTITY(1,1) NOT NULL,
	[SOU_ID] [varchar](20) NULL,
	[LOTS_ID] [varchar](20) NULL,
	[DESC] [varchar](40) NULL,
	[QTETOT] [float] NULL,
	[QTETOTSECT] [float] NULL,
	[CALCTIMSTP] [varchar](14) NULL,
	[COUUM] [varchar](2) NULL,
	[TEMPUNI] [float] NULL,
	[TEMPUM] [varchar](2) NULL,
	[DATECREE] [datetime] NULL,
	[OLDESTPROD] [datetime] NULL,
	[CLEPERS] [varchar](40) NULL,
	[PROFIT] [float] NULL,
	[COUTANTSEL] [int] NULL,
	[COUTANT1] [float] NULL,
	[COUTANT2] [float] NULL,
	[COUTANT3] [float] NULL,
	[COUTANT4] [float] NULL,
	[SysDate] [datetime] NOT NULL DEFAULT (getdate()),
  CONSTRAINT [PK_FACLOTS] PRIMARY KEY CLUSTERED ([UniqueId] ASC)
)
GO

CREATE TABLE [dbo].[FACLOTSCO](
	[UniqueId] [bigint] IDENTITY(1,1) NOT NULL,
	[SOU_ID] [varchar](20) NULL,
	[LOTS_ID] [varchar](20) NULL,
	[PRO_ID] [varchar](20) NULL,
	[ORDRE] [varchar](6) NULL,
	[QTE] [float] NULL,
	[QTEUM] [varchar](2) NULL,
	[SysDate] [datetime] NOT NULL DEFAULT (getdate()),
  CONSTRAINT [PK_FACLOTSCO] PRIMARY KEY CLUSTERED ([UniqueId] ASC)
)
GO

CREATE TABLE [dbo].[FACPRO](
	[UniqueId] [bigint] IDENTITY(1,1) NOT NULL,
	[SOU_ID] [varchar](20) NULL,
	[PRO_ID] [varchar](20) NULL,
	[CLEMANU] [varchar](20) NULL,
	[CLEDIST] [varchar](20) NULL,
	[CLEPERS] [varchar](20) NULL,
	[DESC] [varchar](60) NULL,
	[QTEENS] [float] NULL,
	[QTELOT] [float] NULL,
	[QTEOTH] [float] NULL,
	[CALCTIMSTP] [varchar](14) NULL,
	[COUBRUTUNI] [float] NULL,
	[COUUM] [varchar](2) NULL,
	[QPP] [float] NULL,
	[COUESC] [float] NULL,
	[PROMCOUNET] [float] NULL,
	[TEMPUNI] [float] NULL,
	[TEMPUM] [varchar](2) NULL,
	[MULCOM] [float] NULL,
	[CODEIMPR] [varchar](20) NULL,
	[CODEFOUR] [varchar](2) NULL,
	[CODECAT] [varchar](3) NULL,
	[DATECOUT] [datetime] NULL,
	[QTECOM] [float] NULL,
	[QTEACOM] [float] NULL,
	[SysDate] [datetime] NOT NULL DEFAULT (getdate()),
  CONSTRAINT [PK_FACPRO] PRIMARY KEY CLUSTERED ([UniqueId] ASC)
)
GO

CREATE TABLE [dbo].[FACREL](
	[UniqueId] [bigint] IDENTITY(1,1) NOT NULL,
	[SOU_ID] [varchar](20) NULL,
	[BLO_ID] [varchar](3) NULL,
	[DIV_ID] [varchar](3) NULL,
	[TYPERELEVE] [varchar](1) NULL,
	[ORDRE] [varchar](6) NULL,
	[TYPEITEM] [varchar](1) NULL,
	[ITEM_ID] [varchar](20) NULL,
	[DESCR] [varchar](60) NULL,
	[QTE] [float] NULL,
	[SECTION] [float] NULL,
	[QTEUM] [varchar](2) NULL,
	[PROFIT] [float] NULL,
	[TYPETAXE] [varchar](1) NULL,
	[CODEIMPR] [varchar](2) NULL,
	[COUTANBRUT] [float] NULL,
	[TEMPSUNIT] [float] NULL,
	[TEMPSSEC] [float] NULL,
	[TEMPSUM] [varchar](2) NULL,
	[PROFITPLUS] [float] NULL,
	[PROFITMOIN] [float] NULL,
	[SysDate] [datetime] NOT NULL DEFAULT (getdate()),
  CONSTRAINT [PK_FACREL] PRIMARY KEY CLUSTERED ([UniqueId] ASC)
)
GO

CREATE TABLE [dbo].[FACTURES](
	[UniqueId] [bigint] IDENTITY(1,1) NOT NULL,
	[SOU_ID] [varchar](20) NULL,
	[NODOC] [varchar](12) NULL,
	[DESCDOC] [varchar](200) NULL,
	[DATECREE] [datetime] NULL,
	[DATEDOC] [datetime] NULL,
	[DATEEXP] [datetime] NULL,
	[REF_ID] [varchar](20) NULL,
	[STATUT] [int] NULL,
	[NOCOMMANDE] [varchar](20) NULL,
	[NOTEINTERN] [text] NULL,
	[CLIENTNO] [varchar](20) NULL,
	[CLIENTCIE] [varchar](50) NULL,
	[CLIENTCNT] [varchar](50) NULL,
	[CLIENTRUE1] [varchar](50) NULL,
	[CLIENTRUE2] [varchar](50) NULL,
	[CLIENTVILL] [varchar](40) NULL,
	[CLIENTCP] [varchar](7) NULL,
	[CLIENTPROV] [varchar](40) NULL,
	[CLIENTPAYS] [varchar](40) NULL,
	[CLIENTBP] [varchar](30) NULL,
	[CLIENTTEL1] [varchar](20) NULL,
	[CLIENTTEL2] [varchar](20) NULL,
	[CLIENTTEL3] [varchar](20) NULL,
	[CLIENTFAX] [varchar](20) NULL,
	[MEMESITE] [bit] NULL,
	[SITENO] [varchar](20) NULL,
	[SITECIE] [varchar](50) NULL,
	[SITECNT] [varchar](50) NULL,
	[SITERUE1] [varchar](50) NULL,
	[SITERUE2] [varchar](50) NULL,
	[SITEVILLE] [varchar](40) NULL,
	[SITECP] [varchar](7) NULL,
	[SITEPROV] [varchar](40) NULL,
	[SITEPAYS] [varchar](40) NULL,
	[SITEBP] [varchar](30) NULL,
	[SITETEL1] [varchar](20) NULL,
	[SITETEL2] [varchar](20) NULL,
	[SITETEL3] [varchar](20) NULL,
	[SITEFAX] [varchar](20) NULL,
	[MATTOTALMD] [float] NULL,
	[NOTEPRINC] [text] NULL,
	[MATCOUTREL] [float] NULL,
	[MATCOUTLOT] [float] NULL,
	[MATVENDCAL] [float] NULL,
	[MATPORTTVP] [float] NULL,
	[SERCOUTCAL] [float] NULL,
	[SERVENDCAL] [float] NULL,
	[SERHRESCAL] [float] NULL,
	[SERPORTTVP] [float] NULL,
	[AUTCOUTCAL] [float] NULL,
	[AUTVENDCAL] [float] NULL,
	[AUTPORTTVP] [float] NULL,
	[OPTIONSSOM] [varchar](40) NULL,
	[MATCOUTMO] [float] NULL,
	[SERCOUTMO] [float] NULL,
	[AUTCOUTMO] [float] NULL,
	[MATADMPC] [float] NULL,
	[SERADMPC] [float] NULL,
	[AUTADMPC] [float] NULL,
	[MATADMMO] [float] NULL,
	[SERADMMO] [float] NULL,
	[AUTADMMO] [float] NULL,
	[MATPROFPC] [float] NULL,
	[SERPROFPC] [float] NULL,
	[AUTPROFPC] [float] NULL,
	[MATPROFMO] [float] NULL,
	[SERPROFMO] [float] NULL,
	[AUTPROFMO] [float] NULL,
	[GLOBAJUPC] [float] NULL,
	[GLOBAJUMO] [float] NULL,
	[GLOBEXPLIC] [varchar](40) NULL,
	[GLOBAJU2PC] [float] NULL,
	[GLOBAJU2MO] [float] NULL,
	[GLOBEXPL2] [varchar](40) NULL,
	[OPTIONSIMP] [varchar](50) NULL,
	[OPIMPADJMA] [varchar](40) NULL,
	[OPIMPADJLA] [varchar](40) NULL,
	[OPIMPADJOT] [varchar](40) NULL,
	[NOTEBAS] [text] NULL,
	[MATTAXAB1] [float] NULL,
	[MATTAXAB2] [float] NULL,
	[MATTAXAB3] [float] NULL,
	[MATTAXAB4] [float] NULL,
	[MATTAXAB5] [float] NULL,
	[MATTAXAB6] [float] NULL,
	[SERTAXAB1] [float] NULL,
	[SERTAXAB2] [float] NULL,
	[SERTAXAB3] [float] NULL,
	[SERTAXAB4] [float] NULL,
	[SERTAXAB5] [float] NULL,
	[SERTAXAB6] [float] NULL,
	[AUTTAXAB1] [float] NULL,
	[AUTTAXAB2] [float] NULL,
	[AUTTAXAB3] [float] NULL,
	[AUTTAXAB4] [float] NULL,
	[AUTTAXAB5] [float] NULL,
	[AUTTAXAB6] [float] NULL,
	[TAXTYPCAL] [int] NULL,
	[AJUTAXAB1] [float] NULL,
	[AJUTAXAB2] [float] NULL,
	[AJUTAXAB3] [float] NULL,
	[AJUTAXAB4] [float] NULL,
	[AJUTAXAB5] [float] NULL,
	[TOTTAXFED] [float] NULL,
	[TOTTAXPRV] [float] NULL,
	[TAX_ID] [varchar](20) NULL,
	[APPLIQUTVF] [bit] NULL,
	[APPLIQUTVP] [bit] NULL,
	[TVPSURCOUT] [bit] NULL,
	[TOTCALCULE] [bit] NULL,
	[CALCTIMSTP] [varchar](14) NULL,
	[UMPLAN] [varchar](2) NULL,
	[TYPEPROF] [varchar](1) NULL,
	[MATPROFDEF] [float] NULL,
	[TYPESRVPRO] [varchar](1) NULL,
	[TAUXMD] [float] NULL,
	[NUMLOTEXP] [float] NULL,
	[SYSTEM] [bit] NULL,
	[USER1] [varchar](20) NULL,
	[USER2] [varchar](20) NULL,
	[EST_NAME] [varchar](50) NULL,
	[SysDate] [datetime] NOT NULL DEFAULT (getdate()),
  CONSTRAINT [PK_FACTURES] PRIMARY KEY CLUSTERED ([UniqueId] ASC)
)
GO

CREATE TABLE [dbo].[FACWEBLOG](
	[UniqueId] [bigint] IDENTITY(1,1) NOT NULL,
	[SOU_ID] [varchar](20) NULL,
	[WEB_ID] [varchar](15) NULL,
	[TRF_DATE] [varchar](25) NULL,
	[RESULT] [varchar](10) NULL,
	[MESSAGE] [varchar](60) NULL,
	[SysDate] [datetime] NOT NULL DEFAULT (getdate()),
  CONSTRAINT [PK_FACWEBLOG] PRIMARY KEY CLUSTERED ([UniqueId] ASC)
)
GO

CREATE TABLE [dbo].[FRAIS](
	[UniqueId] [bigint] IDENTITY(1,1) NOT NULL,
	[ORDRE] [varchar](6) NULL,
	[DESCFRAIS] [varchar](50) NULL,
	[COUTUNI] [float] NULL,
	[FRAISUM] [varchar](2) NULL,
	[PROFIT] [float] NULL,
	[INCLSOU] [bit] NULL,
	[INCLFAC] [bit] NULL,
	[SYSTEM] [bit] NULL,
	[SysDate] [datetime] NOT NULL DEFAULT (getdate()),
  CONSTRAINT [PK_FRAIS] PRIMARY KEY CLUSTERED ([UniqueId] ASC)
)
GO

CREATE TABLE [dbo].[IMPRIMER](
	[UniqueId] [bigint] IDENTITY(1,1) NOT NULL,
	[NOMCONFIG] [varchar](30) NULL,
	[TYPECONFIG] [varchar](20) NULL,
	[NOMIMPRIM] [varchar](30) NULL,
	[LANGUE] [int] NULL,
	[OBJECT] [text] NULL,
	[SYSTEM] [bit] NULL,
	[SysDate] [datetime] NOT NULL DEFAULT (getdate()),
  CONSTRAINT [PK_IMPRIMER] PRIMARY KEY CLUSTERED ([UniqueId] ASC)
)
GO

CREATE TABLE [dbo].[NOTES](
	[UniqueId] [bigint] IDENTITY(1,1) NOT NULL,
	[NOTE_ID] [varchar](20) NULL,
	[DESCR] [varchar](40) NULL,
	[NOTE] [text] NULL,
	[NOTETYPE] [varchar](2) NULL,
	[DEFAULT] [bit] NULL,
	[SysDate] [datetime] NOT NULL DEFAULT (getdate()),
  CONSTRAINT [PK_NOTES] PRIMARY KEY CLUSTERED ([UniqueId] ASC)
)
GO

CREATE TABLE [dbo].[PROCAT](
	[UniqueId] [bigint] IDENTITY(1,1) NOT NULL,
	[CODECAT] [varchar](3) NULL,
	[DESC] [varchar](40) NULL,
	[SysDate] [datetime] NOT NULL DEFAULT (getdate()),
  CONSTRAINT [PK_PROCAT] PRIMARY KEY CLUSTERED ([UniqueId] ASC)
)
GO

CREATE TABLE [dbo].[PRODUITS](
	[UniqueId] [bigint] IDENTITY(1,1) NOT NULL,
	[PRO_ID] [varchar](20) NULL,
	[CLEMANU] [varchar](20) NULL,
	[CLEPERS] [varchar](20) NULL,
	[CLEDIST] [varchar](20) NULL,
	[CODEUPC] [varchar](12) NULL,
	[CODECAT] [varchar](3) NULL,
	[DESCDIST] [varchar](60) NULL,
	[DESC] [varchar](60) NULL,
	[COUBRUTUNI] [float] NULL,
	[COUUM] [varchar](2) NULL,
	[QPP] [float] NULL,
	[COUESC] [float] NULL,
	[PROMCOUNET] [float] NULL,
	[PROFIT] [float] NULL,
	[MULCOM] [float] NULL,
	[TEMPUNI] [float] NULL,
	[TEMPUM] [varchar](2) NULL,
	[CODEFOUR] [varchar](2) NULL,
	[NOUVEAU] [varchar](1) NULL,
	[DNR] [varchar](1) NULL,
	[DATECOUT] [datetime] NULL,
	[DATECREE] [datetime] NULL,
	[PATHPICT] [varchar](60) NULL,
	[PATHSPEC] [varchar](60) NULL,
	[IMAGE] [varchar](1) NULL,
	[USER1] [varchar](20) NULL,
	[USER2] [varchar](20) NULL,
	[SysDate] [datetime] NOT NULL DEFAULT (getdate()),
  CONSTRAINT [PK_PRODUITS] PRIMARY KEY CLUSTERED ([UniqueId] ASC)
)
GO

CREATE TABLE [dbo].[PROFGRID](
	[UniqueId] [bigint] IDENTITY(1,1) NOT NULL,
	[UM] [varchar](2) NULL,
	[PRIXBAS] [float] NULL,
	[PRIXHAUT] [float] NULL,
	[PROFIT] [float] NULL,
	[SysDate] [datetime] NOT NULL DEFAULT (getdate()),
  CONSTRAINT [PK_PROFGRID] PRIMARY KEY CLUSTERED ([UniqueId] ASC)
)
GO

CREATE TABLE [dbo].[PROGLOSS](
	[UniqueId] [bigint] IDENTITY(1,1) NOT NULL,
	[TYPEGLOSS] [varchar](2) NULL,
	[CATEGORIE] [varchar](30) NULL,
	[SOUSCAT] [varchar](30) NULL,
	[CODE] [varchar](20) NULL,
	[DESCRIPTIO] [varchar](50) NULL,
	[CODEBANK] [varchar](3) NULL,
	[SysDate] [datetime] NOT NULL DEFAULT (getdate()),
  CONSTRAINT [PK_PROGLOSS] PRIMARY KEY CLUSTERED ([UniqueId] ASC)
)
GO

CREATE TABLE [dbo].[SOUAMD](
	[UniqueId] [bigint] IDENTITY(1,1) NOT NULL,
	[SOU_ID] [varchar](20) NULL,
	[BLO_ID] [varchar](3) NULL,
	[DIV_ID] [varchar](3) NULL,
	[FACTMD] [float] NULL,
	[SysDate] [datetime] NOT NULL DEFAULT (getdate()),
  CONSTRAINT [PK_SOUAMD] PRIMARY KEY CLUSTERED ([UniqueId] ASC)
)
GO

CREATE TABLE [dbo].[SOUBLO](
	[UniqueId] [bigint] IDENTITY(1,1) NOT NULL,
	[SOU_ID] [varchar](20) NULL,
	[BLO_ID] [varchar](3) NULL,
	[DESC] [varchar](40) NULL,
	[MULT] [int] NULL,
	[SysDate] [datetime] NOT NULL DEFAULT (getdate()),
  CONSTRAINT [PK_SOUBLO] PRIMARY KEY CLUSTERED ([UniqueId] ASC)
)
GO

CREATE TABLE [dbo].[SOUDIV](
	[UniqueId] [bigint] IDENTITY(1,1) NOT NULL,
	[SOU_ID] [varchar](20) NULL,
	[DIV_ID] [varchar](3) NULL,
	[DESC] [varchar](40) NULL,
	[SysDate] [datetime] NOT NULL DEFAULT (getdate()),
  CONSTRAINT [PK_SOUDIV] PRIMARY KEY CLUSTERED ([UniqueId] ASC)
)
GO

CREATE TABLE [dbo].[SOUENS](
	[UniqueId] [bigint] IDENTITY(1,1) NOT NULL,
	[SOU_ID] [varchar](20) NULL,
	[ENS_ID] [varchar](20) NULL,
	[DESC] [varchar](40) NULL,
	[QTETOT] [float] NULL,
	[QTETOTSECT] [float] NULL,
	[CALCTIMSTP] [varchar](14) NULL,
	[COUUM] [varchar](2) NULL,
	[TEMPUNI] [float] NULL,
	[TEMPSEC] [float] NULL,
	[TEMPUM] [varchar](2) NULL,
	[DATECREE] [datetime] NULL,
	[OLDESTPROD] [datetime] NULL,
	[CLEPERS] [varchar](40) NULL,
	[PROFIT] [float] NULL,
	[SysDate] [datetime] NOT NULL DEFAULT (getdate()),
  CONSTRAINT [PK_SOUENS] PRIMARY KEY CLUSTERED ([UniqueId] ASC)
)
GO

CREATE TABLE [dbo].[SOUENSCO](
	[UniqueId] [bigint] IDENTITY(1,1) NOT NULL,
	[SOU_ID] [varchar](20) NULL,
	[ENS_ID] [varchar](20) NULL,
	[PRO_ID] [varchar](20) NULL,
	[ORDRE] [varchar](6) NULL,
	[QTE] [float] NULL,
	[QTEUM] [varchar](2) NULL,
	[TYPRATIO] [varchar](1) NULL,
	[DIV] [float] NULL,
	[DIVUM] [varchar](2) NULL,
	[SysDate] [datetime] NOT NULL DEFAULT (getdate()),
  CONSTRAINT [PK_SOUENSCO] PRIMARY KEY CLUSTERED ([UniqueId] ASC)
)
GO

CREATE TABLE [dbo].[SOULOTS](
	[UniqueId] [bigint] IDENTITY(1,1) NOT NULL,
	[SOU_ID] [varchar](20) NULL,
	[LOTS_ID] [varchar](20) NULL,
	[DESC] [varchar](40) NULL,
	[QTETOT] [float] NULL,
	[QTETOTSECT] [float] NULL,
	[CALCTIMSTP] [varchar](14) NULL,
	[COUUM] [varchar](2) NULL,
	[TEMPUNI] [float] NULL,
	[TEMPUM] [varchar](2) NULL,
	[DATECREE] [datetime] NULL,
	[OLDESTPROD] [datetime] NULL,
	[CLEPERS] [varchar](40) NULL,
	[PROFIT] [float] NULL,
	[COUTANTSEL] [int] NULL,
	[COUTANT1] [float] NULL,
	[COUTANT2] [float] NULL,
	[COUTANT3] [float] NULL,
	[COUTANT4] [float] NULL,
	[SysDate] [datetime] NOT NULL DEFAULT (getdate()),
  CONSTRAINT [PK_SOULOTS] PRIMARY KEY CLUSTERED ([UniqueId] ASC)
)
GO

CREATE TABLE [dbo].[SOULOTSCO](
	[UniqueId] [bigint] IDENTITY(1,1) NOT NULL,
	[SOU_ID] [varchar](20) NULL,
	[LOTS_ID] [varchar](20) NULL,
	[PRO_ID] [varchar](20) NULL,
	[ORDRE] [varchar](6) NULL,
	[QTE] [float] NULL,
	[QTEUM] [varchar](2) NULL,
	[SysDate] [datetime] NOT NULL DEFAULT (getdate()),
  CONSTRAINT [PK_SOULOTSCO] PRIMARY KEY CLUSTERED ([UniqueId] ASC)
)
GO

CREATE TABLE [dbo].[SOUMIS](
	[UniqueId] [bigint] IDENTITY(1,1) NOT NULL,
	[SOU_ID] [varchar](20) NULL,
	[NODOC] [varchar](12) NULL,
	[DESCDOC] [varchar](200) NULL,
	[DATECREE] [datetime] NULL,
	[DATEDOC] [datetime] NULL,
	[DATEEXP] [datetime] NULL,
	[REF_ID] [varchar](20) NULL,
	[STATUT] [int] NULL,
	[NOCOMMANDE] [varchar](20) NULL,
	[NOTEINTERN] [text] NULL,
	[CLIENTNO] [varchar](20) NULL,
	[CLIENTCIE] [varchar](50) NULL,
	[CLIENTCNT] [varchar](50) NULL,
	[CLIENTRUE1] [varchar](50) NULL,
	[CLIENTRUE2] [varchar](50) NULL,
	[CLIENTVILL] [varchar](40) NULL,
	[CLIENTCP] [varchar](7) NULL,
	[CLIENTPROV] [varchar](40) NULL,
	[CLIENTPAYS] [varchar](40) NULL,
	[CLIENTBP] [varchar](30) NULL,
	[CLIENTTEL1] [varchar](20) NULL,
	[CLIENTTEL2] [varchar](20) NULL,
	[CLIENTTEL3] [varchar](20) NULL,
	[CLIENTFAX] [varchar](20) NULL,
	[MEMESITE] [bit] NULL,
	[SITENO] [varchar](20) NULL,
	[SITECIE] [varchar](50) NULL,
	[SITECNT] [varchar](50) NULL,
	[SITERUE1] [varchar](50) NULL,
	[SITERUE2] [varchar](50) NULL,
	[SITEVILLE] [varchar](40) NULL,
	[SITECP] [varchar](7) NULL,
	[SITEPROV] [varchar](40) NULL,
	[SITEPAYS] [varchar](40) NULL,
	[SITEBP] [varchar](30) NULL,
	[SITETEL1] [varchar](20) NULL,
	[SITETEL2] [varchar](20) NULL,
	[SITETEL3] [varchar](20) NULL,
	[SITEFAX] [varchar](20) NULL,
	[MATTOTALMD] [float] NULL,
	[NOTEPRINC] [text] NULL,
	[MATCOUTREL] [float] NULL,
	[MATCOUTLOT] [float] NULL,
	[MATVENDCAL] [float] NULL,
	[MATPORTTVP] [float] NULL,
	[SERCOUTCAL] [float] NULL,
	[SERVENDCAL] [float] NULL,
	[SERHRESCAL] [float] NULL,
	[SERPORTTVP] [float] NULL,
	[AUTCOUTCAL] [float] NULL,
	[AUTVENDCAL] [float] NULL,
	[AUTPORTTVP] [float] NULL,
	[OPTIONSSOM] [varchar](40) NULL,
	[MATCOUTMO] [float] NULL,
	[SERCOUTMO] [float] NULL,
	[AUTCOUTMO] [float] NULL,
	[MATADMPC] [float] NULL,
	[SERADMPC] [float] NULL,
	[AUTADMPC] [float] NULL,
	[MATADMMO] [float] NULL,
	[SERADMMO] [float] NULL,
	[AUTADMMO] [float] NULL,
	[MATPROFPC] [float] NULL,
	[SERPROFPC] [float] NULL,
	[AUTPROFPC] [float] NULL,
	[MATPROFMO] [float] NULL,
	[SERPROFMO] [float] NULL,
	[AUTPROFMO] [float] NULL,
	[GLOBAJUPC] [float] NULL,
	[GLOBAJUMO] [float] NULL,
	[GLOBEXPLIC] [varchar](40) NULL,
	[GLOBAJU2PC] [float] NULL,
	[GLOBAJU2MO] [float] NULL,
	[GLOBEXPL2] [varchar](40) NULL,
	[OPTIONSIMP] [varchar](50) NULL,
	[OPIMPADJMA] [varchar](40) NULL,
	[OPIMPADJLA] [varchar](40) NULL,
	[OPIMPADJOT] [varchar](40) NULL,
	[NOTEBAS] [text] NULL,
	[MATTAXAB1] [float] NULL,
	[MATTAXAB2] [float] NULL,
	[MATTAXAB3] [float] NULL,
	[MATTAXAB4] [float] NULL,
	[MATTAXAB5] [float] NULL,
	[MATTAXAB6] [float] NULL,
	[SERTAXAB1] [float] NULL,
	[SERTAXAB2] [float] NULL,
	[SERTAXAB3] [float] NULL,
	[SERTAXAB4] [float] NULL,
	[SERTAXAB5] [float] NULL,
	[SERTAXAB6] [float] NULL,
	[AUTTAXAB1] [float] NULL,
	[AUTTAXAB2] [float] NULL,
	[AUTTAXAB3] [float] NULL,
	[AUTTAXAB4] [float] NULL,
	[AUTTAXAB5] [float] NULL,
	[AUTTAXAB6] [float] NULL,
	[TAXTYPCAL] [int] NULL,
	[AJUTAXAB1] [float] NULL,
	[AJUTAXAB2] [float] NULL,
	[AJUTAXAB3] [float] NULL,
	[AJUTAXAB4] [float] NULL,
	[AJUTAXAB5] [float] NULL,
	[TOTTAXFED] [float] NULL,
	[TOTTAXPRV] [float] NULL,
	[TAX_ID] [varchar](20) NULL,
	[APPLIQUTVF] [bit] NULL,
	[APPLIQUTVP] [bit] NULL,
	[TVPSURCOUT] [bit] NULL,
	[TOTCALCULE] [bit] NULL,
	[CALCTIMSTP] [varchar](14) NULL,
	[UMPLAN] [varchar](2) NULL,
	[TYPEPROF] [varchar](1) NULL,
	[MATPROFDEF] [float] NULL,
	[TYPESRVPRO] [varchar](1) NULL,
	[TAUXMD] [float] NULL,
	[NUMLOTEXP] [float] NULL,
	[SYSTEM] [bit] NULL,
	[USER1] [varchar](20) NULL,
	[USER2] [varchar](20) NULL,
	[EST_NAME] [varchar](50) NULL,
	[SysDate] [datetime] NOT NULL DEFAULT (getdate()),
  CONSTRAINT [PK_SOUMIS] PRIMARY KEY CLUSTERED ([UniqueId] ASC)
)
GO

CREATE TABLE [dbo].[SOUPRO](
	[UniqueId] [bigint] IDENTITY(1,1) NOT NULL,
	[SOU_ID] [varchar](20) NULL,
	[PRO_ID] [varchar](20) NULL,
	[CLEMANU] [varchar](20) NULL,
	[CLEDIST] [varchar](20) NULL,
	[CLEPERS] [varchar](20) NULL,
	[DESC] [varchar](60) NULL,
	[QTEENS] [float] NULL,
	[QTELOT] [float] NULL,
	[QTEOTH] [float] NULL,
	[CALCTIMSTP] [varchar](14) NULL,
	[COUBRUTUNI] [float] NULL,
	[COUUM] [varchar](2) NULL,
	[QPP] [float] NULL,
	[COUESC] [float] NULL,
	[PROMCOUNET] [float] NULL,
	[TEMPUNI] [float] NULL,
	[TEMPUM] [varchar](2) NULL,
	[MULCOM] [float] NULL,
	[CODEIMPR] [varchar](20) NULL,
	[CODEFOUR] [varchar](2) NULL,
	[CODECAT] [varchar](3) NULL,
	[DATECOUT] [datetime] NULL,
	[QTECOM] [float] NULL,
	[QTEACOM] [float] NULL,
	[SysDate] [datetime] NOT NULL DEFAULT (getdate()),
  CONSTRAINT [PK_SOUPRO] PRIMARY KEY CLUSTERED ([UniqueId] ASC)
)
GO

CREATE TABLE [dbo].[SOUREL](
	[UniqueId] [bigint] IDENTITY(1,1) NOT NULL,
	[SOU_ID] [varchar](20) NULL,
	[BLO_ID] [varchar](3) NULL,
	[DIV_ID] [varchar](3) NULL,
	[TYPERELEVE] [varchar](1) NULL,
	[ORDRE] [varchar](6) NULL,
	[TYPEITEM] [varchar](1) NULL,
	[ITEM_ID] [varchar](20) NULL,
	[DESCR] [varchar](60) NULL,
	[QTE] [float] NULL,
	[SECTION] [float] NULL,
	[QTEUM] [varchar](2) NULL,
	[PROFIT] [float] NULL,
	[TYPETAXE] [varchar](1) NULL,
	[CODEIMPR] [varchar](2) NULL,
	[COUTANBRUT] [float] NULL,
	[TEMPSUNIT] [float] NULL,
	[TEMPSSEC] [float] NULL,
	[TEMPSUM] [varchar](2) NULL,
	[PROFITPLUS] [float] NULL,
	[PROFITMOIN] [float] NULL,
	[SysDate] [datetime] NOT NULL DEFAULT (getdate()),
  CONSTRAINT [PK_SOUREL] PRIMARY KEY CLUSTERED ([UniqueId] ASC)
)
GO

CREATE TABLE [dbo].[SOUWEBLOG](
	[UniqueId] [bigint] IDENTITY(1,1) NOT NULL,
	[SOU_ID] [varchar](20) NULL,
	[WEB_ID] [varchar](15) NULL,
	[TRF_DATE] [varchar](25) NULL,
	[RESULT] [varchar](10) NULL,
	[MESSAGE] [varchar](60) NULL,
	[SysDate] [datetime] NOT NULL DEFAULT (getdate()),
  CONSTRAINT [PK_SOUWEBLOG] PRIMARY KEY CLUSTERED ([UniqueId] ASC)
)
GO

CREATE TABLE [dbo].[TAUX](
	[UniqueId] [bigint] IDENTITY(1,1) NOT NULL,
	[ORDRE] [varchar](6) NULL,
	[DESCTAUX] [varchar](50) NULL,
	[COUTUNI] [float] NULL,
	[PROFIT] [float] NULL,
	[INCLSOU] [bit] NULL,
	[INCLFAC] [bit] NULL,
	[SYSTEM] [bit] NULL,
	[SysDate] [datetime] NOT NULL DEFAULT (getdate()),
  CONSTRAINT [PK_TAUX] PRIMARY KEY CLUSTERED ([UniqueId] ASC)
)
GO

CREATE TABLE [dbo].[TAXDEF](
	[UniqueId] [bigint] IDENTITY(1,1) NOT NULL,
	[TAX_ID] [varchar](20) NULL,
	[PROVINCE] [varchar](2) NULL,
	[ABRFEDA] [varchar](6) NULL,
	[ABRPRVA] [varchar](6) NULL,
	[ABRFEDF] [varchar](6) NULL,
	[ABRPRVF] [varchar](6) NULL,
	[FEDINCL] [bit] NULL,
	[TVPSURCPER] [bit] NULL,
	[TVPSURCDEF] [bit] NULL,
	[CODESERV] [varchar](1) NULL,
	[CODEMATE] [varchar](1) NULL,
	[CODEAUTRE] [varchar](1) NULL,
	[CODEAJUST] [varchar](1) NULL,
	[DATEDEB] [datetime] NULL,
	[CODETAX1] [varchar](1) NULL,
	[CODETAX2] [varchar](1) NULL,
	[CODETAX3] [varchar](1) NULL,
	[CODETAX4] [varchar](1) NULL,
	[CODETAX5] [varchar](1) NULL,
	[DESCA1] [varchar](20) NULL,
	[DESCA2] [varchar](20) NULL,
	[DESCA3] [varchar](20) NULL,
	[DESCA4] [varchar](20) NULL,
	[DESCA5] [varchar](20) NULL,
	[DESCF1] [varchar](20) NULL,
	[DESCF2] [varchar](20) NULL,
	[DESCF3] [varchar](20) NULL,
	[DESCF4] [varchar](20) NULL,
	[DESCF5] [varchar](20) NULL,
	[TAUXFED1] [float] NULL,
	[TAUXFED2] [float] NULL,
	[TAUXFED3] [float] NULL,
	[TAUXFED4] [float] NULL,
	[TAUXFED5] [float] NULL,
	[TAUXPRV1] [float] NULL,
	[TAUXPRV2] [float] NULL,
	[TAUXPRV3] [float] NULL,
	[TAUXPRV4] [float] NULL,
	[TAUXPRV5] [float] NULL,
	[SysDate] [datetime] NOT NULL DEFAULT (getdate()),
  CONSTRAINT [PK_TAXDEF] PRIMARY KEY CLUSTERED ([UniqueId] ASC)
)
GO

CREATE TABLE [dbo].[PriceUpdate_Products](
  [PRO_ID]      varchar(20), 
  [DESC]        varchar(60), 
  [CODECAT]     varchar(3),
  [COUUM]       varchar(2), 
  [TEMPUM]      varchar(2),
  [CLEMANU]     varchar(20), 
  [CLEDIST]     varchar(20), 
  [DESCDIST]    varchar(60),
  [QPP]         float, 
  [MULCOM]      float,
  [COUBRUTUNI]  float, 
  [COUESC]      float, 
  [PROMCOUNET]  float, 
  [NOUVEAU]     varchar(1), 
  [DATECOUT]    datetime
)
GO

CREATE TABLE [dbo].[Sys_Units](
	[UnitId] [int] NOT NULL,
	[CodeEN] [varchar](2) NOT NULL,
	[CodeFR] [varchar](2) NOT NULL,
	[Type] [varchar](1) NOT NULL,
	[Package] [bit] NOT NULL,
    [ForQuantity] [bit] NOT NULL,
    [ForProducts] [bit] NOT NULL,
    [ForAssemblies] [bit] NOT NULL,
    [BaseUnitCodeEN] [varchar](2) NOT NULL,
    [BaseUnitRatio] [int] NOT NULL,
    [CompatibilityGroup] [varchar](1) NOT NULL,
	[DescriptionEN] [varchar](35) NOT NULL,
	[DescriptionFR] [varchar](35) NOT NULL,
  CONSTRAINT [PK_Units] PRIMARY KEY CLUSTERED ([UnitId] ASC)
)
GO

CREATE TABLE [dbo].[Sys_UnitsConversion](
	[ConversionId] [int] NOT NULL,
	[UnitFrom] [varchar](2) NOT NULL,
	[UnitTo] [varchar](2) NOT NULL,
	[Ratio] [float] NOT NULL,
	[UnitToUnit] [bit] NOT NULL,
    [PackageToUnit] [bit] NOT NULL,
    [UnitToPackage] [bit] NOT NULL,
  CONSTRAINT [PK_UnitsConversion] PRIMARY KEY CLUSTERED ([ConversionId] ASC)
)
GO

CREATE TABLE [dbo].[_TransferCompleted](
	[DbfSource] [varchar](250) NULL,
	[CompletedOn] [datetime] NULL,
	[TransferVersion] int NULL
)
GO

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
