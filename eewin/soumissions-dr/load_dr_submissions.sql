-- load_dr_submissions.sql
-- Loads the real DR Électrique priced lines found in Daniel Dupuis' e-mails (see lignes.csv and each
-- <dossier>/SOURCE.txt) into the live EE database, ONLY through the official upsert procedures
-- (up_*_Update, eewin/scripts/CreateScripts.sql) and the official costing engine
-- (sp_SOU_CalculTotaux, eewin/scripts/V36_UpdateDatabase.sql:100).
--
-- Every literal below comes from a document quoted in eewin/soumissions-dr/ ; NULL means "not stated".
-- The only numbers that are not copied from a document are the engine outputs (fCoutantTotal,
-- fVendantTotal) written back into SOUMIS, and structural keys (BLO_ID/DIV_ID '1', ORDRE '1000').
--
-- Run:  docker exec -i eewin /opt/mssql-tools18/bin/sqlcmd -S localhost -U sa -P '<pwd>' -C -d EE -W -s '|' -i - < load_dr_submissions.sql
-- Idempotence: refuses to run if either SOU_ID already exists (use unload_dr_submissions.sql first).

SET NOCOUNT ON;
SET XACT_ABORT ON;

IF EXISTS (SELECT 1 FROM SOUMIS WHERE SOU_ID IN ('S-1844', '1400-INDUSTRIEL'))
BEGIN
  RAISERROR('SOUMIS S-1844 or 1400-INDUSTRIEL already loaded. Run unload_dr_submissions.sql first.', 16, 1);
  RETURN;
END;

DECLARE @rc INT;
DECLARE @today DATETIME = CAST(GETDATE() AS DATE);

-- sp_SOU_CalculTotaux returns TWO result sets when @DoLog = 1 (the @log table, then the 4 totals,
-- V36_UpdateDatabase.sql:640-650 and the final SELECT) ; INSERT ... EXEC needs a single shape, so the
-- engine is run twice: once with @DoLog = 1 (log printed = proof, SOUPRO.UnitSelling written),
-- once with @DoLog = 0 whose single result set (fCoutantTotal, fCoutantTotalPortionTVP, fVendantTotal,
-- fLaborTotal) is captured here.
IF OBJECT_ID('tempdb..#totals') IS NOT NULL DROP TABLE #totals;
CREATE TABLE #totals (
  fCoutantTotal decimal(18,6), fCoutantTotalPortionTVP decimal(18,6),
  fVendantTotal decimal(18,6), fLaborTotal decimal(18,6)
);

BEGIN TRANSACTION;

------------------------------------------------------------------------------------------------
-- 1. S-1844 — DR Électrique -> LC 2000, "SAQ — Travaux d'électricité (rez-de-chaussée)", 25 août 2026
--    Source: S-1844/Soumission_S-1844_LC2000_SAQ_.pdf.txt page 1 ; e-mail "S-1844" of 2026-08-26.
------------------------------------------------------------------------------------------------

-- 1.1 Client file (CLIENTS) — up_CLIENTS_Update, CreateScripts.sql:66
IF NOT EXISTS (SELECT 1 FROM CLIENTS WHERE CLI_ID = 'LC2000')
  EXEC @rc = dbo.up_CLIENTS_Update
    @UniqueId = NULL, @CLI_ID = 'LC2000', @TYPEFICHE = NULL, @NUMERO = NULL,
    @NOMCIE = 'LC 2000', @CONTACT = 'Tibor Demeter, Chef estimateur',
    @RUE1 = '4045, rue Lavoisier', @RUE2 = NULL, @VILLE = 'Boisbriand', @CODEPOSTAL = 'J7H 1N1',
    @PROVINCE = 'Québec', @PAYS = NULL, @BOITEPOSTA = NULL, @TEL1 = NULL, @TEL2 = NULL, @TEL3 = NULL, @FAX = NULL,
    @PROFIT = NULL, @TVFAPPL = NULL, @TVPAPPL = NULL,
    @NOTES = 'Créé le 2026-09-27 depuis la soumission S-1844 (page 1, bloc CLIENT).',
    @EMAIL = 'tdemeter@LC2000.com', @SITEWEB = NULL, @SYSTEM = 0;

-- 1.2 Block / division grid — up_SOUBLO_Update (V41:9), up_SOUDIV_Update (V41:74)
--     BLO_ID must be numeric: fn_MultBlock takes INT (SCHEMA.md, SOUBLO.MULT note).
EXEC @rc = dbo.up_SOUBLO_Update @UniqueId = NULL, @SOU_ID = 'S-1844', @BLO_ID = '1',
  @DESC = 'Rez-de-chaussée', @ACC_NO = NULL, @ACH_NO = NULL, @MULT = 1, @ORDRE = '1';
EXEC @rc = dbo.up_SOUDIV_Update @UniqueId = NULL, @SOU_ID = 'S-1844', @DIV_ID = '1',
  @ACT_NO = NULL, @DESC = 'Travaux d''électricité', @ORDRE = '1';

-- 1.3 The priced line has no product key -> named ENSEMBLE (catalogue) + SOUENS (copy in the bid)
--     up_ENSEMBLE_Update (CreateScripts.sql:650, V3:26) ; up_SOUENS_Update (CreateScripts.sql:2678, V6:701)
--     No composition (ENSCOMPO/SOUENSCO): the PDF gives none. Time and profit: not stated -> NULL.
IF NOT EXISTS (SELECT 1 FROM ENSEMBLE WHERE ENS_ID = 'DR:S-1844-FORFAIT')
  EXEC @rc = dbo.up_ENSEMBLE_Update @UniqueId = NULL, @ENS_ID = 'DR:S-1844-FORFAIT',
    @CLEPERS = 'DR:S-1844 SAQ RDC', @DESC = 'S-1844 SAQ RDC - forfait travaux d''électricité',
    @COUUM = 'U', @PROFIT = NULL, @TEMPSEC = NULL, @TEMPUNI = NULL, @TEMPUM = NULL,
    @DATECREE = @today, @OLDESTPROD = NULL, @SYSTEM = 0, @USES_DISC = 0;

EXEC @rc = dbo.up_SOUENS_Update @UniqueId = NULL, @SOU_ID = 'S-1844', @ENS_ID = 'DR:S-1844-FORFAIT',
  @ENS_ORG_ID = 'DR:S-1844-FORFAIT', @DESC = 'S-1844 SAQ RDC - forfait travaux d''électricité',
  @QTETOT = 1, @QTETOTSECT = NULL, @CALCTIMSTP = NULL, @COUUM = 'U',
  @TEMPUNI = NULL, @TEMPSEC = NULL, @TEMPUM = NULL, @DATECREE = @today, @OLDESTPROD = NULL,
  @CLEPERS = 'DR:S-1844 SAQ RDC', @PROFIT = NULL;

-- 1.4 The take-off line carrying the price — up_SOUREL_Update (CreateScripts.sql:3662, V11:3515)
--     TYPERELEVE 'O' / TYPEITEM 'O': the engine takes COUTANBRUT as the unit cost as-is
--     (sp_SOU_CalculTotaux V36:451-455 "SET @CoutantUnitaire = @COUTANBRUT"). The document gives one
--     number, the selling price ; PROFIT = 0 so that vendant = coût = 238 744,00 (V36:483-492).
EXEC @rc = dbo.up_SOUREL_Update @UniqueId = NULL, @SOU_ID = 'S-1844', @BLO_ID = '1', @DIV_ID = '1',
  @TYPERELEVE = 'O', @EXT_ID = NULL, @ORDRE = '1000', @TYPEITEM = 'O', @ITEM_ID = 'DR:S-1844-FORFAIT',
  @DESCR = 'SAQ RDC - travaux d''électricité, forfait (PDF p.1)', @QTE = 1, @SECTION = NULL, @QTEUM = 'U',
  @PROFIT = 0, @TYPETAXE = NULL, @CODEIMPR = '', @COUTANBRUT = 238744.00,
  @TEMPSUNIT = NULL, @TEMPSSEC = NULL, @TEMPSUM = NULL, @PROFITPLUS = NULL, @PROFITMOIN = NULL,
  @ACC_NO = NULL, @ACH_NO = NULL, @ACT_NO = NULL;

-- 1.5 Run the official engine on the 'O' take-off: log printed (proof), then totals captured
EXEC dbo.sp_SOU_CalculTotaux @SOU_ID = 'S-1844', @TypeReleve = 'O', @EE_CALGARY = 0,
  @ModeCalcul = 'C', @VendantUAvantVendantT = 1, @VPM = 2, @DoLog = 1;
DELETE FROM #totals;
INSERT INTO #totals
  EXEC dbo.sp_SOU_CalculTotaux @SOU_ID = 'S-1844', @TypeReleve = 'O', @EE_CALGARY = 0,
    @ModeCalcul = 'C', @VendantUAvantVendantT = 1, @VPM = 2, @DoLog = 0;

DECLARE @s1844_cout FLOAT, @s1844_vend FLOAT;
SELECT @s1844_cout = fCoutantTotal, @s1844_vend = fVendantTotal FROM #totals;
PRINT 'S-1844 engine (O): fCoutantTotal=' + CONVERT(varchar(30), CAST(@s1844_cout AS decimal(18,2))) + ' fVendantTotal=' + CONVERT(varchar(30), CAST(@s1844_vend AS decimal(18,2)));

-- 1.6 Header — up_SOUMIS_Update (CreateScripts.sql:3010, last version V22:241) ; 139 parameters, all given.
--     AUT* = "autres" family fed by TYPERELEVE 'O' (SCHEMA.md §SOUMIS). Values = engine output above.
EXEC @rc = dbo.up_SOUMIS_Update
  @UniqueId = NULL, @SOU_ID = 'S-1844',
  @ORIGIN = NULL, @ORIGINREF = NULL, @EXTAPP = NULL,
  @EXTFILE = 'eewin/soumissions-dr/S-1844/Soumission_S-1844_LC2000_SAQ_.pdf.txt',
  @NODOC = 'S-1844', @DESCDOC = 'SAQ — Travaux d''électricité (rez-de-chaussée)',
  @DATECREE = NULL, @DATEDOC = '2026-08-25', @DATEEXP = NULL, @REF_ID = NULL, @STATUT = NULL, @NOCOMMANDE = NULL,
  @NOTEINTERN = 'Source : courriel « S-1844 » de Daniel Dupuis (Estimateur Sénior) du 2026-08-26 10:48 HE, pièce jointe Soumission_S-1844_LC2000_SAQ_.pdf (3 pages). Prix forfaitaire 238 744,00 $ avant TPS/TVQ. Signataire du PDF : Jonathan Parent, Chargé de projets. Aucun détail matériel / main-d''œuvre dans le document. Chargé dans EE le 2026-09-27 (eewin/soumissions-dr).',
  @CLIENTNO = 'LC2000', @CLIENTCIE = 'LC 2000', @CLIENTCNT = 'Tibor Demeter, Chef estimateur',
  @CLIENTRUE1 = '4045, rue Lavoisier', @CLIENTRUE2 = NULL, @CLIENTVILL = 'Boisbriand', @CLIENTCP = 'J7H 1N1',
  @CLIENTPROV = 'Québec', @CLIENTPAYS = NULL, @CLIENTBP = NULL, @CLIENTTEL1 = NULL, @CLIENTTEL2 = NULL, @CLIENTTEL3 = NULL,
  @CLIENTFAX = NULL, @CLIENTEMAI = 'tdemeter@LC2000.com',
  @MEMESITE = NULL, @SITENO = NULL, @SITECIE = 'SAQ', @SITECNT = NULL, @SITERUE1 = NULL, @SITERUE2 = NULL,
  @SITEVILLE = NULL, @SITECP = NULL, @SITEPROV = NULL, @SITEPAYS = NULL, @SITEBP = NULL,
  @SITETEL1 = NULL, @SITETEL2 = NULL, @SITETEL3 = NULL, @SITEFAX = NULL, @SITEEMAIL = NULL,
  @MATTOTALMD = NULL,
  @NOTEPRINC = 'TRAVAUX : Devis — Conditions générales et techniques, et devis spécifique SAQ (plans E001, E002) ; Légende et légende (suite) des plans électriques (plans E100, E101) ; Diagrammes, panneaux électriques et calculs (plan E102) ; Détails du contrôle d''éclairage (plan E103) ; Démolition et construction — prises et services électriques, rez-de-chaussée (plans E200D, E200) ; Plan de toiture — installations existantes et construction (plan E201) ; Démolition et construction — éclairage, rez-de-chaussée (plans E300D, E300) ; Fourniture et installation de tous les matériaux, équipements et main-d''œuvre requis ; Travaux de jour. EXCLUS : Télécommunication ; Sonorisation ; Tranchée ; Percement.',
  @MATCOUTREL = NULL, @MATCOUTLOT = NULL, @MATVENDCAL = NULL, @MATPORTTVP = NULL,
  @SERCOUTCAL = NULL, @SERVENDCAL = NULL, @SERHRESCAL = NULL, @SERPORTTVP = NULL,
  @AUTCOUTCAL = @s1844_cout, @AUTVENDCAL = @s1844_vend, @AUTPORTTVP = NULL,
  @OPTIONSSOM = NULL, @MATCOUTMO = NULL, @SERCOUTMO = NULL, @AUTCOUTMO = NULL,
  @MATADMPC = NULL, @SERADMPC = NULL, @AUTADMPC = NULL, @MATADMMO = NULL, @SERADMMO = NULL, @AUTADMMO = NULL,
  @MATPROFPC = NULL, @SERPROFPC = NULL, @AUTPROFPC = NULL, @MATPROFMO = NULL, @SERPROFMO = NULL, @AUTPROFMO = NULL,
  @GLOBAJUPC = NULL, @GLOBAJUMO = NULL, @GLOBEXPLIC = NULL, @GLOBAJU2PC = NULL, @GLOBAJU2MO = NULL, @GLOBEXPL2 = NULL,
  @OPTIONSIMP = NULL, @OPIMPADJMA = NULL, @OPIMPADJLA = NULL, @OPIMPADJOT = NULL,
  @NOTEBAS = 'CONDITIONS : 1. La soumission est valide pour 30 jours. 2. Un délai de dix (10) jours ouvrables est nécessaire à la planification de la date des travaux, suite à l''acceptation de la soumission. 3. La tarification soumise par la présente offre ne tient pas compte de la TPS et la TVQ. 4. Termes de paiement, net 30 jours. 5. Intérêt de 2 % par mois (24 % par année) sur les comptes passés dus. 6. Les travaux seront effectués durant les heures normales de bureau. 7. Frais supplémentaire dû aux conditions hivernales non inclus. 8. Une facturation partielle pourrait être émise selon l''avancement des travaux. 9. Tout retard non raisonnable et non imputable à notre personnel sera facturé en supplément. 10. Les réparations, autres que spécifiées, ne sont pas comprises. Prix des matériaux de base volatil (conduits et boîtes métalliques, conduits de PVC, câbles cuivre et aluminium) : ajustement possible avec justification.',
  @MATTAXAB1 = NULL, @MATTAXAB2 = NULL, @MATTAXAB3 = NULL, @MATTAXAB4 = NULL, @MATTAXAB5 = NULL, @MATTAXAB6 = NULL,
  @SERTAXAB1 = NULL, @SERTAXAB2 = NULL, @SERTAXAB3 = NULL, @SERTAXAB4 = NULL, @SERTAXAB5 = NULL, @SERTAXAB6 = NULL,
  @AUTTAXAB1 = NULL, @AUTTAXAB2 = NULL, @AUTTAXAB3 = NULL, @AUTTAXAB4 = NULL, @AUTTAXAB5 = NULL, @AUTTAXAB6 = NULL,
  @TAXTYPCAL = NULL, @AJUTAXAB1 = NULL, @AJUTAXAB2 = NULL, @AJUTAXAB3 = NULL, @AJUTAXAB4 = NULL, @AJUTAXAB5 = NULL,
  @TOTTAXFED = NULL, @TOTTAXPRV = NULL, @TAX_ID = NULL, @APPLIQUTVF = NULL, @APPLIQUTVP = NULL, @TVPSURCOUT = NULL,
  @TOTCALCULE = 1, @CALCTIMSTP = NULL, @UMPLAN = NULL, @TYPEPROF = NULL, @MATPROFDEF = NULL, @TYPESRVPRO = NULL,
  @TAUXMD = NULL, @NUMLOTEXP = NULL, @SYSTEM = 0, @USER1 = NULL, @USER2 = NULL,
  @EST_NAME = 'Daniel Dupuis', @ACCTRANSNO = NULL, @PRJTRANSNO = NULL, @STATUTLIBF = NULL, @STATUTLIBE = NULL,
  @USER_ID = NULL, @BRANCH_ID = NULL, @OWC = NULL;

------------------------------------------------------------------------------------------------
-- 2. 1400 Industriel, La Prairie — supplier quote Siemens (via FRANKLIN EMPIRE INC) to DR, 2025-12-22
--    Source: 1400-Industriel-Laprairie/courriel.txt (price) + "1400 Industriel Laprairie.pdf.txt" (BOM).
--    No DR S- number exists ; SOU_ID = '1400-INDUSTRIEL'. Not a DR bid to a client: a purchase price.
------------------------------------------------------------------------------------------------

EXEC @rc = dbo.up_SOUBLO_Update @UniqueId = NULL, @SOU_ID = '1400-INDUSTRIEL', @BLO_ID = '1',
  @DESC = 'Entrée électrique', @ACC_NO = NULL, @ACH_NO = NULL, @MULT = 1, @ORDRE = '1';
EXEC @rc = dbo.up_SOUDIV_Update @UniqueId = NULL, @SOU_ID = '1400-INDUSTRIEL', @DIV_ID = '1',
  @ACT_NO = NULL, @DESC = 'Entrée électrique', @ORDRE = '1';

-- 2.1 The switchboard is a product with a supplier price -> SOUPRO (frozen price copy),
--     up_SOUPRO_Update (CreateScripts.sql:3530, last version V15:307). COUBRUTUNI = 96 298.36 (e-mail),
--     COUUM 'U' / QPP 1 (Line 20000 "Qty 1"), DATECOUT = quote date 12/22/2025, CLEMANU = Siemens quote no.
EXEC @rc = dbo.up_SOUPRO_Update @UniqueId = NULL, @SOU_ID = '1400-INDUSTRIEL', @PRO_ID = 'DR:SB2-1400IND',
  @CLEMANU = 'gemmox000_12222500_00_00_M00', @CLEDIST = 'FRANKLIN EMPIRE INC', @CLEPERS = 'DR:SB2 4 sect. 2000A',
  @DESC = 'PPD--SB2 SWITCHBOARD - 4 SECTIONS 600Y/347 2000A 65kA',
  @QTEENS = 0, @QTELOT = 0, @QTEOTH = 1, @CALCTIMSTP = NULL,
  @COUBRUTUNI = 96298.36, @COUUM = 'U', @QPP = 1, @COUESC = NULL, @PROMCOUNET = NULL,
  @TEMPUNI = NULL, @TEMPUM = NULL, @MULCOM = NULL, @CODEIMPR = NULL, @CODEFOUR = NULL, @CODECAT = NULL,
  @DATECOUT = '2025-12-22', @DATECOUNET = NULL, @RESCOUNET = NULL, @QTECOM = NULL, @QTEACOM = NULL,
  @ISVIRT = 0, @VIRTCOUNT = NULL;

-- 2.2 Take-off line TYPERELEVE 'P' / TYPEITEM 'P' -> engine reads SOUPRO (V36:287-311)
EXEC @rc = dbo.up_SOUREL_Update @UniqueId = NULL, @SOU_ID = '1400-INDUSTRIEL', @BLO_ID = '1', @DIV_ID = '1',
  @TYPERELEVE = 'P', @EXT_ID = NULL, @ORDRE = '1000', @TYPEITEM = 'P', @ITEM_ID = 'DR:SB2-1400IND',
  @DESCR = 'SB2 switchboard 4 sections - cotation Siemens 2025-12-22', @QTE = 1, @SECTION = NULL, @QTEUM = 'U',
  @PROFIT = 0, @TYPETAXE = NULL, @CODEIMPR = '', @COUTANBRUT = NULL,
  @TEMPSUNIT = NULL, @TEMPSSEC = NULL, @TEMPSUM = NULL, @PROFITPLUS = NULL, @PROFITMOIN = NULL,
  @ACC_NO = NULL, @ACH_NO = NULL, @ACT_NO = NULL;

-- 2.3 Official quantity roll-up (SOUPRO.QTEOTH from SOUREL) — sp_SOUPRO_Quantity_V2.
--     @REPLACE_FILTER must be > 0 and SOUREL.CODEIMPR = '' (docs/CALCUL-SOUMISSION.md §8, §11 item 4:
--     the _v2 procedures CLOSE/DEALLOCATE CUR_2 outside the IF @REPLACE_FILTER > 0 that opens it -> Msg 16916 with 0).
EXEC dbo.sp_SOUPRO_Quantity_V2 @SOU_ID = '1400-INDUSTRIEL', @REPLACE_FILTER = 1, @DoLog = 0, @SOUPROLOG = NULL;

-- 2.4 Engine on the 'P' take-off: log printed (proof, writes SOUPRO.UnitSelling), then totals captured
EXEC dbo.sp_SOU_CalculTotaux @SOU_ID = '1400-INDUSTRIEL', @TypeReleve = 'P', @EE_CALGARY = 0,
  @ModeCalcul = 'C', @VendantUAvantVendantT = 1, @VPM = 2, @DoLog = 1;
DELETE FROM #totals;
INSERT INTO #totals
  EXEC dbo.sp_SOU_CalculTotaux @SOU_ID = '1400-INDUSTRIEL', @TypeReleve = 'P', @EE_CALGARY = 0,
    @ModeCalcul = 'C', @VendantUAvantVendantT = 1, @VPM = 2, @DoLog = 0;

DECLARE @ind_cout FLOAT, @ind_vend FLOAT;
SELECT @ind_cout = fCoutantTotal, @ind_vend = fVendantTotal FROM #totals;
PRINT '1400-INDUSTRIEL engine (P): fCoutantTotal=' + CONVERT(varchar(30), CAST(@ind_cout AS decimal(18,2))) + ' fVendantTotal=' + CONVERT(varchar(30), CAST(@ind_vend AS decimal(18,2)));

-- 2.5 Header. MAT* family fed by TYPERELEVE 'P' (MATCOUTREL = coût matériel du relevé).
EXEC @rc = dbo.up_SOUMIS_Update
  @UniqueId = NULL, @SOU_ID = '1400-INDUSTRIEL',
  @ORIGIN = NULL, @ORIGINREF = NULL, @EXTAPP = NULL,
  @EXTFILE = 'eewin/soumissions-dr/1400-Industriel-Laprairie/1400 Industriel Laprairie.pdf.txt',
  @NODOC = NULL, @DESCDOC = 'Soumission 1400 Industriel Laprairie — entrée électrique changée au complet (bâtisse de GE), avec Hydro-Québec',
  @DATECREE = NULL, @DATEDOC = NULL, @DATEEXP = NULL, @REF_ID = NULL, @STATUT = NULL, @NOCOMMANDE = NULL,
  @NOTEINTERN = 'Source : courriel « Fwd: Soumission 1400 Industriel Laprairie » de Daniel Dupuis du 2026-02-13, transfert de Johnny Gemme (Siemens Canada) du 2025-12-22 à Stéphane Robert : « Voici votre soumission tel que demandé : 96 298.36$ (22-24 semaines de livraison après approbation des dessins) ». Étude arc flash + coordination : prix à venir. Demande de Stéphane Robert du 2025-12-20 : entrée électrique complète, mesurage HQ, entrée par le dessous de la cellule, dérivations vers le haut en cuivre, référence 65 kA, projet avec Sylvain Bédard (C Bédard). Aucun numéro S- ni prix de vente DR connu. Chargé dans EE le 2026-09-27.',
  @CLIENTNO = NULL, @CLIENTCIE = NULL, @CLIENTCNT = NULL, @CLIENTRUE1 = NULL, @CLIENTRUE2 = NULL, @CLIENTVILL = NULL,
  @CLIENTCP = NULL, @CLIENTPROV = NULL, @CLIENTPAYS = NULL, @CLIENTBP = NULL, @CLIENTTEL1 = NULL, @CLIENTTEL2 = NULL,
  @CLIENTTEL3 = NULL, @CLIENTFAX = NULL, @CLIENTEMAI = NULL,
  @MEMESITE = NULL, @SITENO = NULL, @SITECIE = 'GE', @SITECNT = NULL, @SITERUE1 = '1400 Industriel', @SITERUE2 = NULL,
  @SITEVILLE = 'La Prairie', @SITECP = NULL, @SITEPROV = NULL, @SITEPAYS = NULL, @SITEBP = NULL,
  @SITETEL1 = NULL, @SITETEL2 = NULL, @SITETEL3 = NULL, @SITEFAX = NULL, @SITEEMAIL = NULL,
  @MATTOTALMD = NULL, @NOTEPRINC = NULL,
  @MATCOUTREL = @ind_cout, @MATCOUTLOT = NULL, @MATVENDCAL = @ind_vend, @MATPORTTVP = NULL,
  @SERCOUTCAL = NULL, @SERVENDCAL = NULL, @SERHRESCAL = NULL, @SERPORTTVP = NULL,
  @AUTCOUTCAL = NULL, @AUTVENDCAL = NULL, @AUTPORTTVP = NULL,
  @OPTIONSSOM = NULL, @MATCOUTMO = NULL, @SERCOUTMO = NULL, @AUTCOUTMO = NULL,
  @MATADMPC = NULL, @SERADMPC = NULL, @AUTADMPC = NULL, @MATADMMO = NULL, @SERADMMO = NULL, @AUTADMMO = NULL,
  @MATPROFPC = NULL, @SERPROFPC = NULL, @AUTPROFPC = NULL, @MATPROFMO = NULL, @SERPROFMO = NULL, @AUTPROFMO = NULL,
  @GLOBAJUPC = NULL, @GLOBAJUMO = NULL, @GLOBEXPLIC = NULL, @GLOBAJU2PC = NULL, @GLOBAJU2MO = NULL, @GLOBEXPL2 = NULL,
  @OPTIONSIMP = NULL, @OPIMPADJMA = NULL, @OPIMPADJLA = NULL, @OPIMPADJOT = NULL, @NOTEBAS = NULL,
  @MATTAXAB1 = NULL, @MATTAXAB2 = NULL, @MATTAXAB3 = NULL, @MATTAXAB4 = NULL, @MATTAXAB5 = NULL, @MATTAXAB6 = NULL,
  @SERTAXAB1 = NULL, @SERTAXAB2 = NULL, @SERTAXAB3 = NULL, @SERTAXAB4 = NULL, @SERTAXAB5 = NULL, @SERTAXAB6 = NULL,
  @AUTTAXAB1 = NULL, @AUTTAXAB2 = NULL, @AUTTAXAB3 = NULL, @AUTTAXAB4 = NULL, @AUTTAXAB5 = NULL, @AUTTAXAB6 = NULL,
  @TAXTYPCAL = NULL, @AJUTAXAB1 = NULL, @AJUTAXAB2 = NULL, @AJUTAXAB3 = NULL, @AJUTAXAB4 = NULL, @AJUTAXAB5 = NULL,
  @TOTTAXFED = NULL, @TOTTAXPRV = NULL, @TAX_ID = NULL, @APPLIQUTVF = NULL, @APPLIQUTVP = NULL, @TVPSURCOUT = NULL,
  @TOTCALCULE = 1, @CALCTIMSTP = NULL, @UMPLAN = NULL, @TYPEPROF = NULL, @MATPROFDEF = NULL, @TYPESRVPRO = NULL,
  @TAUXMD = NULL, @NUMLOTEXP = NULL, @SYSTEM = 0, @USER1 = NULL, @USER2 = NULL,
  @EST_NAME = NULL, @ACCTRANSNO = NULL, @PRJTRANSNO = NULL, @STATUTLIBF = NULL, @STATUTLIBE = NULL,
  @USER_ID = NULL, @BRANCH_ID = NULL, @OWC = NULL;

COMMIT TRANSACTION;
PRINT 'Loaded: SOUMIS S-1844 (O forfait 238744.00) and 1400-INDUSTRIEL (P SB2 96298.36).';
