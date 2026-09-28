-- ============================================================================
-- EEWin estimating math - worked numeric example on the live EE database.
--
-- Everything is created through the official upsert procedures (up_*_Update),
-- quantities are rolled up with sp_SOUPRO_Quantity_V2, totals are computed with
-- sp_SOU_CalculTotaux (@DoLog = 1 so every intermediate value is printed), and
-- the synthetic rows are removed at the end with up_DeleteSoumis_Full and the
-- up_*_Delete procedures. Nothing else in the database is touched.
--
-- Run:  sqlcmd -S localhost -U sa -P '...' -C -d EE -W -s '|' -i worked_example.sql
-- Documented in ../docs/CALCUL-SOUMISSION.md (French).
-- ============================================================================
SET NOCOUNT ON;

DECLARE @SOU_ID  varchar(20) = 'ZZTEST-CALC';
DECLARE @TAX_ID  varchar(20) = 'ZZTX';

-- Safety: abort if the synthetic keys already exist.
IF EXISTS (SELECT 1 FROM SOUMIS WHERE SOU_ID = @SOU_ID) OR EXISTS (SELECT 1 FROM TAXDEF WHERE TAX_ID = @TAX_ID)
   OR EXISTS (SELECT 1 FROM PRODUITS WHERE PRO_ID LIKE 'ZZP-%') OR EXISTS (SELECT 1 FROM ENSEMBLE WHERE ENS_ID LIKE 'ZZENS-%')
BEGIN
  RAISERROR('Synthetic keys already present - clean up first.', 16, 1);
  RETURN;
END;

PRINT '=== 1. Tax definition (TAXDEF): code M -> provincial 9.975 %, federal 5 %; TVP on cost allowed ===';
EXEC dbo.up_TAXDEF_Update @UniqueId=NULL, @TAX_ID=@TAX_ID, @PROVINCE='QC',
  @ABRFEDA='GST', @ABRPRVA='QST', @ABRFEDF='TPS', @ABRPRVF='TVQ',
  @FEDINCL=0, @TVPSURCPER=1, @TVPSURCDEF=1,
  @CODESERV='S', @CODEMATE='M', @CODEAUTRE='M', @CODEAJUST='M', @DATEDEB='2026-01-01',
  @CODETAX1='M', @CODETAX2='S', @CODETAX3='', @CODETAX4='', @CODETAX5='',
  @DESCA1='Material', @DESCA2='Service', @DESCA3='', @DESCA4='', @DESCA5='',
  @DESCF1='Materiel', @DESCF2='Service', @DESCF3='', @DESCF4='', @DESCF5='',
  @TAUXFED1=5, @TAUXFED2=5, @TAUXFED3=0, @TAUXFED4=0, @TAUXFED5=0,
  @TAUXPRV1=9.975, @TAUXPRV2=0, @TAUXPRV3=0, @TAUXPRV4=0, @TAUXPRV5=0;

PRINT '=== 2. Catalogue products (PRODUITS) ===';
-- Wire #12 : 40.00 $ per CF (hundred feet), 10 % discount, 1.5 h per CF
EXEC dbo.up_PRODUITS_Update @UniqueId=NULL, @PRO_ID='ZZP-WIRE', @PRO_ID_OLD='', @PRO_ID_NEW='', @PRO_ID_Parent='',
  @CLEMANU='T90-12', @CLEPERS='', @CLEDIST='', @CODEUPC='', @CODECAT='ZZ', @DESCDIST='WIRE T90 #12', @DESC='Wire T90 #12',
  @COUBRUTUNI=40.00, @COUUM='CF', @QPP=0, @COUESC=10, @PROMCOUNET=0, @PROFIT=0, @MULCOM=1, @TEMPUNI=1.5, @TEMPUM='CF',
  @CODEFOUR='ZZ', @NOUVEAU='N', @DNR='N', @DATECOUT='2026-01-01', @DATECOUNET=NULL, @RESCOUNET=0, @DATECREE='2026-01-01',
  @PATHPICT='', @PATHSPEC='', @IMAGE='N', @USER1='', @USER2='', @PREFERED='N', @ACC_NO='', @ACH_NO='';
-- Box : list 3.00 $ per U, but special net price PROMCOUNET = 2.50 wins ; 0.25 h per U
EXEC dbo.up_PRODUITS_Update @UniqueId=NULL, @PRO_ID='ZZP-BOX', @PRO_ID_OLD='', @PRO_ID_NEW='', @PRO_ID_Parent='',
  @CLEMANU='1104', @CLEPERS='', @CLEDIST='', @CODEUPC='', @CODECAT='ZZ', @DESCDIST='BOX 1104', @DESC='Device box 1104',
  @COUBRUTUNI=3.00, @COUUM='U', @QPP=0, @COUESC=0, @PROMCOUNET=2.50, @PROFIT=0, @MULCOM=1, @TEMPUNI=0.25, @TEMPUM='U',
  @CODEFOUR='ZZ', @NOUVEAU='N', @DNR='N', @DATECOUT='2026-01-01', @DATECOUNET=NULL, @RESCOUNET=0, @DATECREE='2026-01-01',
  @PATHPICT='', @PATHSPEC='', @IMAGE='N', @USER1='', @USER2='', @PREFERED='N', @ACC_NO='', @ACH_NO='';
-- Receptacle : 12.00 $ per U, 25 % discount, 0.30 h per U
EXEC dbo.up_PRODUITS_Update @UniqueId=NULL, @PRO_ID='ZZP-RECEP', @PRO_ID_OLD='', @PRO_ID_NEW='', @PRO_ID_Parent='',
  @CLEMANU='5320', @CLEPERS='', @CLEDIST='', @CODEUPC='', @CODECAT='ZZ', @DESCDIST='RECEPT 15A', @DESC='Receptacle 15A 120V',
  @COUBRUTUNI=12.00, @COUUM='U', @QPP=0, @COUESC=25, @PROMCOUNET=0, @PROFIT=0, @MULCOM=1, @TEMPUNI=0.30, @TEMPUM='U',
  @CODEFOUR='ZZ', @NOUVEAU='N', @DNR='N', @DATECOUT='2026-01-01', @DATECOUNET=NULL, @RESCOUNET=0, @DATECREE='2026-01-01',
  @PATHPICT='', @PATHSPEC='', @IMAGE='N', @USER1='', @USER2='', @PREFERED='N', @ACC_NO='', @ACH_NO='';
-- EMT 3/4 : 95.00 $ per CF (hundred feet), no discount, 2.0 h per CF
EXEC dbo.up_PRODUITS_Update @UniqueId=NULL, @PRO_ID='ZZP-EMT', @PRO_ID_OLD='', @PRO_ID_NEW='', @PRO_ID_Parent='',
  @CLEMANU='EMT34', @CLEPERS='', @CLEDIST='', @CODEUPC='', @CODECAT='ZZ', @DESCDIST='EMT 3/4', @DESC='EMT conduit 3/4',
  @COUBRUTUNI=95.00, @COUUM='CF', @QPP=0, @COUESC=0, @PROMCOUNET=0, @PROFIT=0, @MULCOM=1, @TEMPUNI=2.0, @TEMPUM='CF',
  @CODEFOUR='ZZ', @NOUVEAU='N', @DNR='N', @DATECOUT='2026-01-01', @DATECOUNET=NULL, @RESCOUNET=0, @DATECREE='2026-01-01',
  @PATHPICT='', @PATHSPEC='', @IMAGE='N', @USER1='', @USER2='', @PREFERED='N', @ACC_NO='', @ACH_NO='';
-- Strap : 0.80 $ per U, no discount, 0.05 h per U
EXEC dbo.up_PRODUITS_Update @UniqueId=NULL, @PRO_ID='ZZP-STRAP', @PRO_ID_OLD='', @PRO_ID_NEW='', @PRO_ID_Parent='',
  @CLEMANU='STRAP34', @CLEPERS='', @CLEDIST='', @CODEUPC='', @CODECAT='ZZ', @DESCDIST='STRAP 3/4', @DESC='EMT strap 3/4',
  @COUBRUTUNI=0.80, @COUUM='U', @QPP=0, @COUESC=0, @PROMCOUNET=0, @PROFIT=0, @MULCOM=1, @TEMPUNI=0.05, @TEMPUM='U',
  @CODEFOUR='ZZ', @NOUVEAU='N', @DNR='N', @DATECOUT='2026-01-01', @DATECOUNET=NULL, @RESCOUNET=0, @DATECREE='2026-01-01',
  @PATHPICT='', @PATHSPEC='', @IMAGE='N', @USER1='', @USER2='', @PREFERED='N', @ACC_NO='', @ACH_NO='';

PRINT '=== 3. Catalogue assemblies (ENSEMBLE / ENSCOMPO) ===';
-- Unit assembly "receptacle" : 1 box + 1 receptacle + 20 F of wire ; 0.10 h extra per assembly
EXEC dbo.up_ENSEMBLE_Update @UniqueId=NULL, @ENS_ID='ZZENS-PRISE', @CLEPERS='4PE prise 15A', @DESC='Duplex receptacle 15A 120V',
  @COUUM='U', @PROFIT=0, @TEMPSEC=0, @TEMPUNI=0.10, @TEMPUM='U', @DATECREE='2026-01-01', @OLDESTPROD='2026-01-01', @SYSTEM=0, @USES_DISC=0;
EXEC dbo.up_ENSCOMPO_Update @UniqueId=NULL, @ENS_ID='ZZENS-PRISE', @ORDRE='000010', @PRO_ID='ZZP-BOX',   @QTE=1,  @QTEUM='U', @TYPRATIO='L', @DIV=0, @DIVUM='';
EXEC dbo.up_ENSCOMPO_Update @UniqueId=NULL, @ENS_ID='ZZENS-PRISE', @ORDRE='000020', @PRO_ID='ZZP-RECEP', @QTE=1,  @QTEUM='U', @TYPRATIO='L', @DIV=0, @DIVUM='';
EXEC dbo.up_ENSCOMPO_Update @UniqueId=NULL, @ENS_ID='ZZENS-PRISE', @ORDRE='000030', @PRO_ID='ZZP-WIRE',  @QTE=20, @QTEUM='F', @TYPRATIO='L', @DIV=0, @DIVUM='';
-- Linear assembly "conduit run" measured in feet : per foot 1 F EMT + 3 F wire ; per section 1 strap
EXEC dbo.up_ENSEMBLE_Update @UniqueId=NULL, @ENS_ID='ZZENS-CONDUIT', @CLEPERS='19PE0.75 #12', @DESC='EMT 3/4 + 3 x #12',
  @COUUM='F', @PROFIT=0, @TEMPSEC=0.10, @TEMPUNI=0.05, @TEMPUM='F', @DATECREE='2026-01-01', @OLDESTPROD='2026-01-01', @SYSTEM=0, @USES_DISC=0;
EXEC dbo.up_ENSCOMPO_Update @UniqueId=NULL, @ENS_ID='ZZENS-CONDUIT', @ORDRE='000010', @PRO_ID='ZZP-EMT',   @QTE=1, @QTEUM='F', @TYPRATIO='L', @DIV=1, @DIVUM='F';
EXEC dbo.up_ENSCOMPO_Update @UniqueId=NULL, @ENS_ID='ZZENS-CONDUIT', @ORDRE='000020', @PRO_ID='ZZP-WIRE',  @QTE=3, @QTEUM='F', @TYPRATIO='L', @DIV=1, @DIVUM='F';
EXEC dbo.up_ENSCOMPO_Update @UniqueId=NULL, @ENS_ID='ZZENS-CONDUIT', @ORDRE='000030', @PRO_ID='ZZP-STRAP', @QTE=1, @QTEUM='U', @TYPRATIO='S', @DIV=0, @DIVUM='';

PRINT '=== 4. Quote header (SOUMIS) ===';
EXEC dbo.up_SOUMIS_Update @UniqueId=NULL, @SOU_ID=@SOU_ID, @ORIGIN='N', @ORIGINREF='', @EXTAPP='', @EXTFILE='',
  @NODOC='ZZTEST', @DESCDOC='Synthetic quote for CALCUL-SOUMISSION.md', @DATECREE='2026-09-27', @DATEDOC='2026-09-27', @DATEEXP='2026-10-27',
  @REF_ID='', @STATUT=0, @NOCOMMANDE='', @NOTEINTERN='', @CLIENTNO='', @CLIENTCIE='', @CLIENTCNT='', @CLIENTRUE1='', @CLIENTRUE2='',
  @CLIENTVILL='', @CLIENTCP='', @CLIENTPROV='', @CLIENTPAYS='', @CLIENTBP='', @CLIENTTEL1='', @CLIENTTEL2='', @CLIENTTEL3='', @CLIENTFAX='', @CLIENTEMAI='',
  @MEMESITE=1, @SITENO='', @SITECIE='', @SITECNT='', @SITERUE1='', @SITERUE2='', @SITEVILLE='', @SITECP='', @SITEPROV='', @SITEPAYS='', @SITEBP='',
  @SITETEL1='', @SITETEL2='', @SITETEL3='', @SITEFAX='', @SITEEMAIL='',
  @MATTOTALMD=0, @NOTEPRINC='', @MATCOUTREL=0, @MATCOUTLOT=0, @MATVENDCAL=0, @MATPORTTVP=0, @SERCOUTCAL=0, @SERVENDCAL=0, @SERHRESCAL=0, @SERPORTTVP=0,
  @AUTCOUTCAL=0, @AUTVENDCAL=0, @AUTPORTTVP=0, @OPTIONSSOM='', @MATCOUTMO=0, @SERCOUTMO=0, @AUTCOUTMO=0, @MATADMPC=0, @SERADMPC=0, @AUTADMPC=0,
  @MATADMMO=0, @SERADMMO=0, @AUTADMMO=0, @MATPROFPC=0, @SERPROFPC=0, @AUTPROFPC=0, @MATPROFMO=0, @SERPROFMO=0, @AUTPROFMO=0,
  @GLOBAJUPC=0, @GLOBAJUMO=0, @GLOBEXPLIC='', @GLOBAJU2PC=0, @GLOBAJU2MO=0, @GLOBEXPL2='', @OPTIONSIMP='', @OPIMPADJMA='', @OPIMPADJLA='', @OPIMPADJOT='', @NOTEBAS='',
  @MATTAXAB1=0, @MATTAXAB2=0, @MATTAXAB3=0, @MATTAXAB4=0, @MATTAXAB5=0, @MATTAXAB6=0, @SERTAXAB1=0, @SERTAXAB2=0, @SERTAXAB3=0, @SERTAXAB4=0, @SERTAXAB5=0, @SERTAXAB6=0,
  @AUTTAXAB1=0, @AUTTAXAB2=0, @AUTTAXAB3=0, @AUTTAXAB4=0, @AUTTAXAB5=0, @AUTTAXAB6=0, @TAXTYPCAL=0, @AJUTAXAB1=0, @AJUTAXAB2=0, @AJUTAXAB3=0, @AJUTAXAB4=0, @AJUTAXAB5=0,
  @TOTTAXFED=0, @TOTTAXPRV=0, @TAX_ID=@TAX_ID, @APPLIQUTVF=1, @APPLIQUTVP=1, @TVPSURCOUT=1, @TOTCALCULE=0, @CALCTIMSTP='', @UMPLAN='F',
  @TYPEPROF='C', @MATPROFDEF=20, @TYPESRVPRO='C', @TAUXMD=65, @NUMLOTEXP=0, @SYSTEM=0, @USER1='', @USER2='', @EST_NAME='ZZ', @ACCTRANSNO='', @PRJTRANSNO='',
  @STATUTLIBF='', @STATUTLIBE='', @USER_ID='ZZ', @BRANCH_ID='', @OWC='';

PRINT '=== 5. Block (SOUBLO, MULT=2), division (SOUDIV) and labor factor (SOUAMD, FACTMD=1.5) ===';
EXEC dbo.up_SOUBLO_Update @UniqueId=NULL, @SOU_ID=@SOU_ID, @BLO_ID='1', @DESC='Block x2 (two identical floors)', @ACC_NO='', @ACH_NO='', @MULT=2, @ORDRE='000010';
EXEC dbo.up_SOUDIV_Update @UniqueId=NULL, @SOU_ID=@SOU_ID, @DIV_ID='1', @ACT_NO='', @DESC='Division 1', @ORDRE='000010';
EXEC dbo.up_SOUAMD_Update @UniqueId=NULL, @SOU_ID=@SOU_ID, @BLO_ID='1', @DIV_ID='1', @FACTMD=1.5;

PRINT '=== 6. Quote copies of the products (SOUPRO) - same prices as the catalogue ===';
-- The application copies PRODUITS -> SOUPRO when a product enters a quote; no SQL procedure does it,
-- so the copy is made here explicitly through up_SOUPRO_Update.
DECLARE @p_id varchar(20), @p_clemanu varchar(30), @p_desc varchar(60), @p_cou float, @p_um varchar(2), @p_qpp float,
        @p_esc float, @p_prom float, @p_tmp float, @p_tmpum varchar(2), @p_mul float, @p_cat varchar(3), @p_four varchar(2);
DECLARE cur CURSOR LOCAL FOR
  SELECT PRO_ID, CLEMANU, [DESC], COUBRUTUNI, COUUM, QPP, COUESC, PROMCOUNET, TEMPUNI, TEMPUM, MULCOM, CODECAT, CODEFOUR
  FROM PRODUITS WHERE PRO_ID LIKE 'ZZP-%' ORDER BY PRO_ID;
OPEN cur; FETCH NEXT FROM cur INTO @p_id,@p_clemanu,@p_desc,@p_cou,@p_um,@p_qpp,@p_esc,@p_prom,@p_tmp,@p_tmpum,@p_mul,@p_cat,@p_four;
WHILE @@FETCH_STATUS = 0
BEGIN
  EXEC dbo.up_SOUPRO_Update @UniqueId=NULL, @SOU_ID=@SOU_ID, @PRO_ID=@p_id, @CLEMANU=@p_clemanu, @CLEDIST='', @CLEPERS='', @DESC=@p_desc,
    @QTEENS=0, @QTELOT=0, @QTEOTH=0, @CALCTIMSTP='', @COUBRUTUNI=@p_cou, @COUUM=@p_um, @QPP=@p_qpp, @COUESC=@p_esc, @PROMCOUNET=@p_prom,
    @TEMPUNI=@p_tmp, @TEMPUM=@p_tmpum, @MULCOM=@p_mul, @CODEIMPR='', @CODEFOUR=@p_four, @CODECAT=@p_cat, @DATECOUT='2026-01-01', @DATECOUNET=NULL,
    @RESCOUNET=0, @QTECOM=0, @QTEACOM=0, @ISVIRT=0, @VIRTCOUNT=0;
  FETCH NEXT FROM cur INTO @p_id,@p_clemanu,@p_desc,@p_cou,@p_um,@p_qpp,@p_esc,@p_prom,@p_tmp,@p_tmpum,@p_mul,@p_cat,@p_four;
END
CLOSE cur; DEALLOCATE cur;

PRINT '=== 7. Quote copies of the assemblies (SOUENS / SOUENSCO) ===';
EXEC dbo.up_SOUENS_Update @UniqueId=NULL, @SOU_ID=@SOU_ID, @ENS_ID='ZZENS-PRISE', @ENS_ORG_ID='ZZENS-PRISE', @DESC='Duplex receptacle 15A 120V',
  @QTETOT=0, @QTETOTSECT=0, @CALCTIMSTP='', @COUUM='U', @TEMPUNI=0.10, @TEMPSEC=0, @TEMPUM='U', @DATECREE='2026-01-01', @OLDESTPROD='2026-01-01', @CLEPERS='4PE prise 15A', @PROFIT=0;
EXEC dbo.up_SOUENSCO_Update @UniqueId=NULL, @SOU_ID=@SOU_ID, @ENS_ID='ZZENS-PRISE', @PRO_ID='ZZP-BOX',   @ORDRE='000010', @QTE=1,  @QTEUM='U', @TYPRATIO='L', @DIV=0, @DIVUM='';
EXEC dbo.up_SOUENSCO_Update @UniqueId=NULL, @SOU_ID=@SOU_ID, @ENS_ID='ZZENS-PRISE', @PRO_ID='ZZP-RECEP', @ORDRE='000020', @QTE=1,  @QTEUM='U', @TYPRATIO='L', @DIV=0, @DIVUM='';
EXEC dbo.up_SOUENSCO_Update @UniqueId=NULL, @SOU_ID=@SOU_ID, @ENS_ID='ZZENS-PRISE', @PRO_ID='ZZP-WIRE',  @ORDRE='000030', @QTE=20, @QTEUM='F', @TYPRATIO='L', @DIV=0, @DIVUM='';
EXEC dbo.up_SOUENS_Update @UniqueId=NULL, @SOU_ID=@SOU_ID, @ENS_ID='ZZENS-CONDUIT', @ENS_ORG_ID='ZZENS-CONDUIT', @DESC='EMT 3/4 + 3 x #12',
  @QTETOT=0, @QTETOTSECT=0, @CALCTIMSTP='', @COUUM='F', @TEMPUNI=0.05, @TEMPSEC=0.10, @TEMPUM='F', @DATECREE='2026-01-01', @OLDESTPROD='2026-01-01', @CLEPERS='19PE0.75 #12', @PROFIT=0;
EXEC dbo.up_SOUENSCO_Update @UniqueId=NULL, @SOU_ID=@SOU_ID, @ENS_ID='ZZENS-CONDUIT', @PRO_ID='ZZP-EMT',   @ORDRE='000010', @QTE=1, @QTEUM='F', @TYPRATIO='L', @DIV=1, @DIVUM='F';
EXEC dbo.up_SOUENSCO_Update @UniqueId=NULL, @SOU_ID=@SOU_ID, @ENS_ID='ZZENS-CONDUIT', @PRO_ID='ZZP-WIRE',  @ORDRE='000020', @QTE=3, @QTEUM='F', @TYPRATIO='L', @DIV=1, @DIVUM='F';
EXEC dbo.up_SOUENSCO_Update @UniqueId=NULL, @SOU_ID=@SOU_ID, @ENS_ID='ZZENS-CONDUIT', @PRO_ID='ZZP-STRAP', @ORDRE='000030', @QTE=1, @QTEUM='U', @TYPRATIO='S', @DIV=0, @DIVUM='';

PRINT '=== 7b. A lot (SOULOTS / SOULOTSCO): 10 straps + 50 F of EMT, 4 h per lot, computed cost (COUTANTSEL=0) ===';
EXEC dbo.up_SOULOTS_Update @UniqueId=NULL, @SOU_ID=@SOU_ID, @LOTS_ID='ZZLOT-RACK', @DESC='Rack: 10 straps + 50 ft EMT', @QTETOT=0, @QTETOTSECT=0, @CALCTIMSTP='',
  @COUUM='U', @TEMPUNI=4.0, @TEMPUM='U', @DATECREE='2026-01-01', @OLDESTPROD='2026-01-01', @CLEPERS='RACK', @PROFIT=0,
  @COUTANTSEL=0, @COUTANT1=0, @COUTANT2=0, @COUTANT3=0, @COUTANT4=0;
EXEC dbo.up_SOULOTSCO_Update @UniqueId=NULL, @SOU_ID=@SOU_ID, @LOTS_ID='ZZLOT-RACK', @PRO_ID='ZZP-STRAP', @ORDRE='000010', @QTE=10, @QTEUM='U';
EXEC dbo.up_SOULOTSCO_Update @UniqueId=NULL, @SOU_ID=@SOU_ID, @LOTS_ID='ZZLOT-RACK', @PRO_ID='ZZP-EMT',   @ORDRE='000020', @QTE=50, @QTEUM='F';

PRINT '=== 8. Takeoff lines (SOUREL) ===';
-- P/A : 10 receptacle assemblies, profit 20 %, tax code M, block 1 (x2), division 1 (labor x1.5)
EXEC dbo.up_SOUREL_Update @UniqueId=NULL, @SOU_ID=@SOU_ID, @BLO_ID='1', @DIV_ID='1', @TYPERELEVE='P', @EXT_ID='', @ORDRE='000010',
  @TYPEITEM='A', @ITEM_ID='ZZENS-PRISE', @DESCR='10 receptacles', @QTE=10, @SECTION=0, @QTEUM='U', @PROFIT=20, @TYPETAXE='M', @CODEIMPR='',
  @COUTANBRUT=0, @TEMPSUNIT=0, @TEMPSSEC=0, @TEMPSUM='', @PROFITPLUS=0, @PROFITMOIN=0, @ACC_NO='', @ACH_NO='', @ACT_NO='';
-- P/A : 100 F of conduit run in 10 sections, profit 20 %
EXEC dbo.up_SOUREL_Update @UniqueId=NULL, @SOU_ID=@SOU_ID, @BLO_ID='1', @DIV_ID='1', @TYPERELEVE='P', @EXT_ID='', @ORDRE='000020',
  @TYPEITEM='A', @ITEM_ID='ZZENS-CONDUIT', @DESCR='100 ft conduit run, 10 sections', @QTE=100, @SECTION=10, @QTEUM='F', @PROFIT=20, @TYPETAXE='M', @CODEIMPR='',
  @COUTANBRUT=0, @TEMPSUNIT=0, @TEMPSSEC=0, @TEMPSUM='', @PROFITPLUS=0, @PROFITMOIN=0, @ACC_NO='', @ACH_NO='', @ACT_NO='';
-- P/P : 5 loose receptacles, profit 30 %
EXEC dbo.up_SOUREL_Update @UniqueId=NULL, @SOU_ID=@SOU_ID, @BLO_ID='1', @DIV_ID='1', @TYPERELEVE='P', @EXT_ID='', @ORDRE='000030',
  @TYPEITEM='P', @ITEM_ID='ZZP-RECEP', @DESCR='5 spare receptacles', @QTE=5, @SECTION=0, @QTEUM='U', @PROFIT=30, @TYPETAXE='M', @CODEIMPR='',
  @COUTANBRUT=0, @TEMPSUNIT=0, @TEMPSSEC=0, @TEMPSUM='', @PROFITPLUS=0, @PROFITMOIN=0, @ACC_NO='', @ACH_NO='', @ACT_NO='';
-- P/L : 1 lot, profit 15 %
EXEC dbo.up_SOUREL_Update @UniqueId=NULL, @SOU_ID=@SOU_ID, @BLO_ID='1', @DIV_ID='1', @TYPERELEVE='P', @EXT_ID='', @ORDRE='000040',
  @TYPEITEM='L', @ITEM_ID='ZZLOT-RACK', @DESCR='1 rack lot', @QTE=1, @SECTION=0, @QTEUM='U', @PROFIT=15, @TYPETAXE='M', @CODEIMPR='',
  @COUTANBRUT=0, @TEMPSUNIT=0, @TEMPSSEC=0, @TEMPSUM='', @PROFITPLUS=0, @PROFITMOIN=0, @ACC_NO='', @ACH_NO='', @ACT_NO='';
-- S/S : 8 hours of service at 65.00 $/h, profit 25 %, tax code S (not in the M bucket)
EXEC dbo.up_SOUREL_Update @UniqueId=NULL, @SOU_ID=@SOU_ID, @BLO_ID='1', @DIV_ID='1', @TYPERELEVE='S', @EXT_ID='', @ORDRE='000010',
  @TYPEITEM='S', @ITEM_ID='LABOR', @DESCR='Electrician 8 h', @QTE=8, @SECTION=0, @QTEUM='U', @PROFIT=25, @TYPETAXE='S', @CODEIMPR='',
  @COUTANBRUT=65.00, @TEMPSUNIT=0, @TEMPSSEC=0, @TEMPSUM='', @PROFITPLUS=0, @PROFITMOIN=0, @ACC_NO='', @ACH_NO='', @ACT_NO='';
-- O/O : one lump-sum "other" item at 300.00 $, profit 10 %, tax code M
EXEC dbo.up_SOUREL_Update @UniqueId=NULL, @SOU_ID=@SOU_ID, @BLO_ID='1', @DIV_ID='1', @TYPERELEVE='O', @EXT_ID='', @ORDRE='000010',
  @TYPEITEM='O', @ITEM_ID='PERMIT', @DESCR='Permit', @QTE=1, @SECTION=0, @QTEUM='U', @PROFIT=10, @TYPETAXE='M', @CODEIMPR='',
  @COUTANBRUT=300.00, @TEMPSUNIT=0, @TEMPSSEC=0, @TEMPSUM='', @PROFITPLUS=0, @PROFITMOIN=0, @ACC_NO='', @ACH_NO='', @ACT_NO='';

PRINT '';
PRINT '=== 9. Unit conversion ratios actually used (fn_UM_GetRatioDeConversion) ===';
SELECT 'F -> CF' AS conv, dbo.fn_UM_GetRatioDeConversion('F','CF',0) AS ratio UNION ALL
SELECT 'F -> C (no row: different compatibility group -> 0)', dbo.fn_UM_GetRatioDeConversion('F','C',0) UNION ALL
SELECT 'F -> F',           dbo.fn_UM_GetRatioDeConversion('F','F',0)  UNION ALL
SELECT 'U -> U',           dbo.fn_UM_GetRatioDeConversion('U','U',0)  UNION ALL
SELECT 'F -> base(CF)=F',  dbo.fn_UM_GetRatioDeConversion('F', dbo.fn_UM_GetUniteDeBase('CF'), 0);
SELECT 'nature(F)' AS q, dbo.fn_UM_GetNatureUnite('F') AS v UNION ALL SELECT 'nature(U)', dbo.fn_UM_GetNatureUnite('U');

PRINT '';
PRINT '=== 10. Quantity roll-up: sp_SOUPRO_Quantity_V2 -> SOUPRO.QTEENS / QTEOTH / QTELOT ===';
-- @REPLACE_FILTER must be > 0: with 0 the three sp_SOU_UpdateQteTotal*_v2 procs CLOSE a cursor (CUR_2) they never opened (Msg 16916).
EXEC dbo.sp_SOUPRO_Quantity_V2 @SOU_ID=@SOU_ID, @REPLACE_FILTER=1, @DoLog=0, @SOUPROLOG='';
SELECT PRO_ID, COUUM, QTEENS, QTEOTH, QTELOT, QTEENS+QTEOTH+QTELOT AS QTE_TOTAL_base_unit FROM SOUPRO WHERE SOU_ID=@SOU_ID ORDER BY PRO_ID;

PRINT '';
-- @DoLog=1 also matters for the result: SOUPRO.UnitSelling is derived from the @Log table variable that is only
-- filled when @DoLog=1 (sp_SOU_CalculTotaux l. 496-510, 565-568). With @DoLog=0 UnitSelling is never written.
PRINT '=== 11a. Totals, material takeoff (P), ModeCalcul=C (markup on cost), VendantUAvantVendantT=1, VPM=2, DoLog=1 ===';
EXEC dbo.sp_SOU_CalculTotaux @SOU_ID=@SOU_ID, @TypeReleve='P', @EE_CALGARY=0, @ModeCalcul='C', @VendantUAvantVendantT=1, @VPM=2, @DoLog=1;
PRINT '=== 11b. Totals, service takeoff (S) ===';
EXEC dbo.sp_SOU_CalculTotaux @SOU_ID=@SOU_ID, @TypeReleve='S', @EE_CALGARY=0, @ModeCalcul='C', @VendantUAvantVendantT=1, @VPM=2, @DoLog=1;
PRINT '=== 11c. Totals, other takeoff (O) ===';
EXEC dbo.sp_SOU_CalculTotaux @SOU_ID=@SOU_ID, @TypeReleve='O', @EE_CALGARY=0, @ModeCalcul='C', @VendantUAvantVendantT=1, @VPM=2, @DoLog=1;

PRINT '';
PRINT '=== 12. Taxable amounts written back into SOUMIS (MATTAXAB*, SERTAXAB*, AUTTAXAB*) and UnitSelling in SOUPRO ===';
SELECT MATTAXAB1, MATTAXAB2, SERTAXAB1, SERTAXAB2, AUTTAXAB1, AUTTAXAB2 FROM SOUMIS WHERE SOU_ID=@SOU_ID;
SELECT PRO_ID, UnitSelling FROM SOUPRO WHERE SOU_ID=@SOU_ID ORDER BY PRO_ID;

PRINT '';
PRINT '=== 13. Same material takeoff with ModeCalcul=G (gross margin: cost / (1 - profit%)) ===';
EXEC dbo.sp_SOU_CalculTotaux @SOU_ID=@SOU_ID, @TypeReleve='P', @EE_CALGARY=0, @ModeCalcul='G', @VendantUAvantVendantT=1, @VPM=2, @DoLog=0;

PRINT '';
PRINT '=== 14. Same material takeoff, VendantUAvantVendantT=0 (total first, then unit = total / qty) ===';
EXEC dbo.sp_SOU_CalculTotaux @SOU_ID=@SOU_ID, @TypeReleve='P', @EE_CALGARY=0, @ModeCalcul='C', @VendantUAvantVendantT=0, @VPM=2, @DoLog=0;

PRINT '';
PRINT '=== 15. Cleanup through the official delete procedures ===';
EXEC dbo.up_DeleteSoumis_Full @DeleteSOU_ID=@SOU_ID, @DeleteHeader=1;
DECLARE @uid bigint;
DECLARE curd CURSOR LOCAL FOR SELECT UniqueId FROM TAXDEF WHERE TAX_ID=@TAX_ID;
OPEN curd; FETCH NEXT FROM curd INTO @uid; WHILE @@FETCH_STATUS=0 BEGIN EXEC dbo.up_TAXDEF_Delete @UniqueId=@uid; FETCH NEXT FROM curd INTO @uid; END; CLOSE curd; DEALLOCATE curd;
DECLARE curp CURSOR LOCAL FOR SELECT UniqueId FROM PRODUITS WHERE PRO_ID LIKE 'ZZP-%';
OPEN curp; FETCH NEXT FROM curp INTO @uid; WHILE @@FETCH_STATUS=0 BEGIN EXEC dbo.up_PRODUITS_Delete @UniqueId=@uid; FETCH NEXT FROM curp INTO @uid; END; CLOSE curp; DEALLOCATE curp;
DECLARE cure CURSOR LOCAL FOR SELECT UniqueId FROM ENSEMBLE WHERE ENS_ID LIKE 'ZZENS-%';
OPEN cure; FETCH NEXT FROM cure INTO @uid; WHILE @@FETCH_STATUS=0 BEGIN EXEC dbo.up_ENSEMBLE_Delete @UniqueId=@uid; FETCH NEXT FROM cure INTO @uid; END; CLOSE cure; DEALLOCATE cure;
DECLARE curc CURSOR LOCAL FOR SELECT UniqueId FROM ENSCOMPO WHERE ENS_ID LIKE 'ZZENS-%';
OPEN curc; FETCH NEXT FROM curc INTO @uid; WHILE @@FETCH_STATUS=0 BEGIN EXEC dbo.up_ENSCOMPO_Delete @UniqueId=@uid; FETCH NEXT FROM curc INTO @uid; END; CLOSE curc; DEALLOCATE curc;

PRINT '=== 16. Proof that nothing is left behind (all counts must be 0) ===';
SELECT (SELECT COUNT(*) FROM SOUMIS   WHERE SOU_ID=@SOU_ID)          AS soumis,
       (SELECT COUNT(*) FROM SOUREL   WHERE SOU_ID=@SOU_ID)          AS sourel,
       (SELECT COUNT(*) FROM SOUPRO   WHERE SOU_ID=@SOU_ID)          AS soupro,
       (SELECT COUNT(*) FROM SOUENS   WHERE SOU_ID=@SOU_ID)          AS souens,
       (SELECT COUNT(*) FROM SOUENSCO WHERE SOU_ID=@SOU_ID)          AS souensco,
       (SELECT COUNT(*) FROM SOUBLO   WHERE SOU_ID=@SOU_ID)          AS soublo,
       (SELECT COUNT(*) FROM SOUDIV   WHERE SOU_ID=@SOU_ID)          AS soudiv,
       (SELECT COUNT(*) FROM SOUAMD   WHERE SOU_ID=@SOU_ID)          AS souamd,
       (SELECT COUNT(*) FROM SOULOTS  WHERE SOU_ID=@SOU_ID)          AS soulots,
       (SELECT COUNT(*) FROM SOULOTSCO WHERE SOU_ID=@SOU_ID)         AS soulotsco,
       (SELECT COUNT(*) FROM TAXDEF   WHERE TAX_ID=@TAX_ID)          AS taxdef,
       (SELECT COUNT(*) FROM PRODUITS WHERE PRO_ID LIKE 'ZZP-%')     AS produits,
       (SELECT COUNT(*) FROM ENSEMBLE WHERE ENS_ID LIKE 'ZZENS-%')   AS ensemble,
       (SELECT COUNT(*) FROM ENSCOMPO WHERE ENS_ID LIKE 'ZZENS-%')   AS enscompo;
