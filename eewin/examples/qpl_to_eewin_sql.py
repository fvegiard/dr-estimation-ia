#!/usr/bin/env python3
"""Generate the T-SQL that feeds a Plan Expert takeoff (.qpl) into the EE database.

Only the official EEWin upsert procedures are used (up_*_Update), exactly as the
Delphi application does: there is no stored procedure in EE that reads a .qpl or
copies ENSEMBLE -> SOUENS / PRODUITS -> SOUPRO (see docs/PLAN-EXPERT-VERS-EEWIN.md).

Mapping implemented (one row per <Counter>/<Line>/<Area> that belongs to a
<Group GroupID=...> carrying an <EEExchangeData ItemType="A"|"P" ItemID=...>):

    QPL element                              -> EE column
    ------------------------------------------------------------------
    Group/@GroupID                           -> SOUREL.EXT_ID
    Group/EEExchangeData/@ItemType           -> SOUREL.TYPEITEM  (A = assembly, P = product)
    Group/EEExchangeData/@ItemID             -> SOUREL.ITEM_ID   (= SOUENS.ENS_ID / SOUPRO.PRO_ID)
    Counter|Line/@Name                       -> SOUREL.DESCR
    count(Counter/Element)                   -> SOUREL.QTE (QTEUM = 'U')
    sum(hypot(Line/Element X1Y1-X2Y2)) * k   -> SOUREL.QTE (QTEUM = SOUMIS.UMPLAN), k = --px-to-unit
    Plan ordinal (1-based)                   -> SOUREL.BLO_ID (SOUBLO row per plan, MULT = 1)
    Layer/@Index                             -> SOUREL.DIV_ID (SOUDIV row per layer)
    QPL file name                            -> SOUMIS.EXTFILE

Groups without EEExchangeData are reported as comments: they have no ITEM_ID,
so nothing in EE can price them.

Usage:
    python3 qpl_to_eewin_sql.py FILE.qpl --sou-id ZZTEST-PE --px-to-unit 1 \
        [--seed-synthetic-catalogue] [--cleanup] > out.sql
"""
import argparse
import math
import os
import sys
import xml.etree.ElementTree as ET


def q(s):
    """T-SQL string literal."""
    return "'" + str(s).replace("'", "''") + "'"


def parse_qpl(path):
    root = ET.parse(path).getroot()
    if root.tag != "QuoterPlanSession":
        sys.exit("not a Plan Expert file: root is %s" % root.tag)
    project = root.find("Project").get("Name")
    groups = {}
    for g in root.findall("Plans/Group"):
        ee = g.find("EEExchangeData")
        if ee is not None:
            groups[g.get("GroupID")] = dict(ee.attrib)
    drawn = []          # every counted/measured object, linked or not
    for pidx, plan in enumerate(root.find("Plans").findall("Plan"), start=1):
        scale = plan.find("Scale").attrib
        for layer in plan.find("Layers"):
            for el in layer:
                if el.tag not in ("Counter", "Line", "Area"):
                    continue
                elems = el.findall("Element")
                length_px = 0.0
                if el.tag == "Line":
                    length_px = sum(
                        math.hypot(float(e.get("X2")) - float(e.get("X1")),
                                   float(e.get("Y2")) - float(e.get("Y1")))
                        for e in elems)
                drawn.append(dict(
                    plan_idx=pidx, plan=plan.get("Name"), plan_file=plan.get("FileName"),
                    layer_idx=layer.get("Index"), layer=layer.get("Name"),
                    kind=el.tag, name=el.get("Name"), group=el.get("GroupID"),
                    n=len(elems), length_px=length_px, scale=scale,
                ))
    prices = [dict(p.attrib) for p in root.findall("Prices/Price")]
    return project, groups, drawn, prices


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("qpl")
    ap.add_argument("--sou-id", required=True)
    ap.add_argument("--px-to-unit", type=float, required=True,
                    help="factor applied to Line lengths in pixels to get SOUMIS.UMPLAN units "
                         "(the .qpl does not document its Scale semantics; pass 1 to keep pixels)")
    ap.add_argument("--umplan", default="F", help="SOUMIS.UMPLAN / QTEUM of Line rows (Sys_Units code)")
    ap.add_argument("--profit", type=float, default=0.0, help="SOUREL.PROFIT (%%) of every imported row")
    ap.add_argument("--typetaxe", default="M", help="SOUREL.TYPETAXE of every imported row")
    ap.add_argument("--seed-synthetic-catalogue", action="store_true",
                    help="create a clearly labelled synthetic ENSEMBLE/ENSCOMPO/PRODUITS for each linked "
                         "ItemType=A group (the rebuilt EE database has 0 catalogue rows)")
    ap.add_argument("--cleanup", action="store_true", help="emit the cleanup script instead of the import")
    a = ap.parse_args()

    project, groups, drawn, prices = parse_qpl(a.qpl)
    linked = [d for d in drawn if d["group"] in groups]
    unlinked = [d for d in drawn if d["group"] not in groups]
    sou = q(a.sou_id)
    out = []
    w = out.append

    if a.cleanup:
        w("-- Cleanup of the rows created by qpl_to_eewin_sql.py for %s (official delete procedures only)." % a.sou_id)
        w("SET NOCOUNT ON;")
        w("EXEC dbo.up_DeleteSoumis_Full @DeleteSOU_ID=%s, @DeleteHeader=1;" % sou)
        if a.seed_synthetic_catalogue:
            w("DECLARE @uid bigint;")
            for tbl, col, proc in (("ENSCOMPO", "ENS_ID", "up_ENSCOMPO_Delete"),
                                   ("ENSEMBLE", "ENS_ID", "up_ENSEMBLE_Delete"),
                                   ("PRODUITS", "PRO_ID", "up_PRODUITS_Delete")):
                ids = ([q(g["ItemID"]) for g in groups.values() if g["ItemType"] == "A"]
                       if tbl != "PRODUITS" else ["'ZZPE-%'"])
                cond = ("%s LIKE %s" % (col, ids[0])) if tbl == "PRODUITS" else ("%s IN (%s)" % (col, ",".join(ids)))
                w("DECLARE c_%s CURSOR LOCAL FOR SELECT UniqueId FROM %s WHERE %s;" % (tbl, tbl, cond))
                w("OPEN c_%s; FETCH NEXT FROM c_%s INTO @uid; WHILE @@FETCH_STATUS=0 BEGIN EXEC dbo.%s @UniqueId=@uid; "
                  "FETCH NEXT FROM c_%s INTO @uid; END; CLOSE c_%s; DEALLOCATE c_%s;" % (tbl, tbl, proc, tbl, tbl, tbl))
        w("SELECT (SELECT COUNT(*) FROM SOUMIS WHERE SOU_ID=%s) AS soumis, (SELECT COUNT(*) FROM SOUREL WHERE SOU_ID=%s) AS sourel,"
          " (SELECT COUNT(*) FROM SOUPRO WHERE SOU_ID=%s) AS soupro, (SELECT COUNT(*) FROM SOUENS WHERE SOU_ID=%s) AS souens,"
          " (SELECT COUNT(*) FROM SOUENSCO WHERE SOU_ID=%s) AS souensco, (SELECT COUNT(*) FROM SOUBLO WHERE SOU_ID=%s) AS soublo,"
          " (SELECT COUNT(*) FROM SOUDIV WHERE SOU_ID=%s) AS soudiv, (SELECT COUNT(*) FROM ENSEMBLE WHERE ENS_ID IN (%s)) AS ensemble,"
          " (SELECT COUNT(*) FROM PRODUITS WHERE PRO_ID LIKE 'ZZPE-%%') AS produits;"
          % ((sou,) * 7 + (",".join(q(g["ItemID"]) for g in groups.values()) or "''",)))
        print("\n".join(out))
        return

    w("-- Generated by qpl_to_eewin_sql.py from %s" % os.path.basename(a.qpl))
    w("-- Project: %s | plans: %d | drawn objects: %d | EE-linked groups: %d | Prices: %d (CostEach != 0: %d)"
      % (project, max((d["plan_idx"] for d in drawn), default=0), len(drawn), len(groups), len(prices),
         sum(1 for p in prices if p.get("CostEach") not in ("0", None))))
    w("SET NOCOUNT ON;")
    w("DECLARE @SOU_ID varchar(20) = %s;" % sou)
    w("IF EXISTS (SELECT 1 FROM SOUMIS WHERE SOU_ID = @SOU_ID) BEGIN RAISERROR('SOU_ID already exists', 16, 1); RETURN; END;")

    if a.seed_synthetic_catalogue:
        w("PRINT '=== 0. SYNTHETIC catalogue (composition invented for the proof; only ENS_ID/CLEPERS/DESC come from the .qpl) ===';")
        w("EXEC dbo.up_PRODUITS_Update @UniqueId=NULL, @PRO_ID='ZZPE-CONDUIT', @PRO_ID_OLD='', @PRO_ID_NEW='', @PRO_ID_Parent='',"
          " @CLEMANU='SYNTH-EMT', @CLEPERS='', @CLEDIST='', @CODEUPC='', @CODECAT='ZZ', @DESCDIST='SYNTHETIC conduit', @DESC='SYNTHETIC conduit (per 100 ft)',"
          " @COUBRUTUNI=100.00, @COUUM='CF', @QPP=0, @COUESC=0, @PROMCOUNET=0, @PROFIT=0, @MULCOM=1, @TEMPUNI=2.0, @TEMPUM='CF',"
          " @CODEFOUR='ZZ', @NOUVEAU='N', @DNR='N', @DATECOUT='2026-01-01', @DATECOUNET=NULL, @RESCOUNET=0, @DATECREE='2026-01-01',"
          " @PATHPICT='', @PATHSPEC='', @IMAGE='N', @USER1='', @USER2='', @PREFERED='N', @ACC_NO='', @ACH_NO='';")
        w("EXEC dbo.up_PRODUITS_Update @UniqueId=NULL, @PRO_ID='ZZPE-WIRE', @PRO_ID_OLD='', @PRO_ID_NEW='', @PRO_ID_Parent='',"
          " @CLEMANU='SYNTH-W12', @CLEPERS='', @CLEDIST='', @CODEUPC='', @CODECAT='ZZ', @DESCDIST='SYNTHETIC wire', @DESC='SYNTHETIC wire #12 (per 100 ft)',"
          " @COUBRUTUNI=40.00, @COUUM='CF', @QPP=0, @COUESC=0, @PROMCOUNET=0, @PROFIT=0, @MULCOM=1, @TEMPUNI=1.0, @TEMPUM='CF',"
          " @CODEFOUR='ZZ', @NOUVEAU='N', @DNR='N', @DATECOUT='2026-01-01', @DATECOUNET=NULL, @RESCOUNET=0, @DATECREE='2026-01-01',"
          " @PATHPICT='', @PATHSPEC='', @IMAGE='N', @USER1='', @USER2='', @PREFERED='N', @ACC_NO='', @ACH_NO='';")
        for gid, g in groups.items():
            if g["ItemType"] != "A":
                continue
            # A conduit assembly: 1 ft of conduit + N conductors per ft; N read from the QPL name 'conduit 3/4 03c12' when possible.
            n_cond = 3
            try:
                tail = g["Name"].split()[-1]          # e.g. 03c12
                n_cond = int(tail.lower().split("c")[0])
            except (ValueError, IndexError):
                pass
            w("EXEC dbo.up_ENSEMBLE_Update @UniqueId=NULL, @ENS_ID=%s, @CLEPERS=%s, @DESC=%s, @COUUM='F', @PROFIT=0, @TEMPSEC=0, @TEMPUNI=0, @TEMPUM='F',"
              " @DATECREE='2026-01-01', @OLDESTPROD='2026-01-01', @SYSTEM=0, @USES_DISC=0;"
              % (q(g["ItemID"]), q(g["PersonalKey"] or g["Key"]), q(("SYNTHETIC " + g["Description"])[:60])))
            w("EXEC dbo.up_ENSCOMPO_Update @UniqueId=NULL, @ENS_ID=%s, @ORDRE='000010', @PRO_ID='ZZPE-CONDUIT', @QTE=1, @QTEUM='F', @TYPRATIO='L', @DIV=1, @DIVUM='F';" % q(g["ItemID"]))
            w("EXEC dbo.up_ENSCOMPO_Update @UniqueId=NULL, @ENS_ID=%s, @ORDRE='000020', @PRO_ID='ZZPE-WIRE', @QTE=%d, @QTEUM='F', @TYPRATIO='L', @DIV=1, @DIVUM='F';" % (q(g["ItemID"]), n_cond))

    w("PRINT '=== 1. Header (SOUMIS): EXTFILE = the .qpl file, UMPLAN = unit of plan measurements ===';")
    w("DECLARE @NOW datetime = GETDATE();")
    w("EXEC dbo.up_SOUMIS_Update @UniqueId=NULL, @SOU_ID=@SOU_ID, @ORIGIN='', @ORIGINREF='', @EXTAPP='', @EXTFILE=%s,"
      % q(os.path.basename(a.qpl)[:200]))
    w("  @NODOC=%s, @DESCDOC=%s, @DATECREE=@NOW, @DATEDOC=@NOW, @DATEEXP=NULL," % (q(a.sou_id[:20]), q(project[:200])))
    w("  @REF_ID='', @STATUT=0, @NOCOMMANDE='', @NOTEINTERN='', @CLIENTNO='', @CLIENTCIE='', @CLIENTCNT='', @CLIENTRUE1='', @CLIENTRUE2='',")
    w("  @CLIENTVILL='', @CLIENTCP='', @CLIENTPROV='', @CLIENTPAYS='', @CLIENTBP='', @CLIENTTEL1='', @CLIENTTEL2='', @CLIENTTEL3='', @CLIENTFAX='', @CLIENTEMAI='',")
    w("  @MEMESITE=1, @SITENO='', @SITECIE='', @SITECNT='', @SITERUE1='', @SITERUE2='', @SITEVILLE='', @SITECP='', @SITEPROV='', @SITEPAYS='', @SITEBP='',")
    w("  @SITETEL1='', @SITETEL2='', @SITETEL3='', @SITEFAX='', @SITEEMAIL='',")
    w("  @MATTOTALMD=0, @NOTEPRINC='', @MATCOUTREL=0, @MATCOUTLOT=0, @MATVENDCAL=0, @MATPORTTVP=0, @SERCOUTCAL=0, @SERVENDCAL=0, @SERHRESCAL=0, @SERPORTTVP=0,")
    w("  @AUTCOUTCAL=0, @AUTVENDCAL=0, @AUTPORTTVP=0, @OPTIONSSOM='', @MATCOUTMO=0, @SERCOUTMO=0, @AUTCOUTMO=0, @MATADMPC=0, @SERADMPC=0, @AUTADMPC=0,")
    w("  @MATADMMO=0, @SERADMMO=0, @AUTADMMO=0, @MATPROFPC=0, @SERPROFPC=0, @AUTPROFPC=0, @MATPROFMO=0, @SERPROFMO=0, @AUTPROFMO=0,")
    w("  @GLOBAJUPC=0, @GLOBAJUMO=0, @GLOBEXPLIC='', @GLOBAJU2PC=0, @GLOBAJU2MO=0, @GLOBEXPL2='', @OPTIONSIMP='', @OPIMPADJMA='', @OPIMPADJLA='', @OPIMPADJOT='', @NOTEBAS='',")
    w("  @MATTAXAB1=0, @MATTAXAB2=0, @MATTAXAB3=0, @MATTAXAB4=0, @MATTAXAB5=0, @MATTAXAB6=0, @SERTAXAB1=0, @SERTAXAB2=0, @SERTAXAB3=0, @SERTAXAB4=0, @SERTAXAB5=0, @SERTAXAB6=0,")
    w("  @AUTTAXAB1=0, @AUTTAXAB2=0, @AUTTAXAB3=0, @AUTTAXAB4=0, @AUTTAXAB5=0, @AUTTAXAB6=0, @TAXTYPCAL=0, @AJUTAXAB1=0, @AJUTAXAB2=0, @AJUTAXAB3=0, @AJUTAXAB4=0, @AJUTAXAB5=0,")
    w("  @TOTTAXFED=0, @TOTTAXPRV=0, @TAX_ID='', @APPLIQUTVF=1, @APPLIQUTVP=1, @TVPSURCOUT=1, @TOTCALCULE=0, @CALCTIMSTP='', @UMPLAN=%s," % q(a.umplan))
    w("  @TYPEPROF='C', @MATPROFDEF=0, @TYPESRVPRO='C', @TAUXMD=0, @NUMLOTEXP=0, @SYSTEM=0, @USER1='', @USER2='', @EST_NAME='', @ACCTRANSNO='', @PRJTRANSNO='',")
    w("  @STATUTLIBF='', @STATUTLIBE='', @USER_ID='', @BRANCH_ID='', @OWC='';")

    w("PRINT '=== 2. One block per plan that carries a linked object (SOUBLO, BLO_ID numeric for fn_MultBlock), one division per layer (SOUDIV) ===';")
    for pidx, pname in sorted({(d["plan_idx"], d["plan"]) for d in linked}):
        w("EXEC dbo.up_SOUBLO_Update @UniqueId=NULL, @SOU_ID=@SOU_ID, @BLO_ID=%s, @DESC=%s, @ACC_NO='', @ACH_NO='', @MULT=1, @ORDRE=%s;"
          % (q(str(pidx)), q(pname[:40]), q("%06d" % (pidx * 10))))
    for lidx, lname in sorted({(d["layer_idx"], d["layer"]) for d in linked}):
        w("EXEC dbo.up_SOUDIV_Update @UniqueId=NULL, @SOU_ID=@SOU_ID, @DIV_ID=%s, @ACT_NO='', @DESC=%s, @ORDRE=%s;"
          % (q(str(lidx)), q(lname[:40]), q("%06d" % ((int(lidx) + 1) * 10))))

    ens_ids = sorted({g["ItemID"] for g in groups.values() if g["ItemType"] == "A"})
    pro_ids = sorted({g["ItemID"] for g in groups.values() if g["ItemType"] == "P"})
    w("PRINT '=== 3. Quote copies of the catalogue: ENSEMBLE -> SOUENS, ENSCOMPO -> SOUENSCO, PRODUITS -> SOUPRO (no SQL procedure does this; the application does) ===';")
    w("DECLARE @e_id varchar(20), @e_cle varchar(20), @e_desc varchar(60), @e_um varchar(2), @e_prof float, @e_tsec float, @e_tuni float, @e_tum varchar(2), @e_dc datetime, @e_op datetime;")
    w("DECLARE c_ens CURSOR LOCAL FOR SELECT ENS_ID, CLEPERS, [DESC], COUUM, PROFIT, TEMPSEC, TEMPUNI, TEMPUM, DATECREE, OLDESTPROD FROM ENSEMBLE WHERE ENS_ID IN (%s);"
      % (",".join(q(e) for e in ens_ids) or "''"))
    w("OPEN c_ens; FETCH NEXT FROM c_ens INTO @e_id,@e_cle,@e_desc,@e_um,@e_prof,@e_tsec,@e_tuni,@e_tum,@e_dc,@e_op;")
    w("WHILE @@FETCH_STATUS = 0 BEGIN")
    w("  EXEC dbo.up_SOUENS_Update @UniqueId=NULL, @SOU_ID=@SOU_ID, @ENS_ID=@e_id, @ENS_ORG_ID=@e_id, @DESC=@e_desc, @QTETOT=0, @QTETOTSECT=0, @CALCTIMSTP='',"
      " @COUUM=@e_um, @TEMPUNI=@e_tuni, @TEMPSEC=@e_tsec, @TEMPUM=@e_tum, @DATECREE=@e_dc, @OLDESTPROD=@e_op, @CLEPERS=@e_cle, @PROFIT=@e_prof;")
    w("  FETCH NEXT FROM c_ens INTO @e_id,@e_cle,@e_desc,@e_um,@e_prof,@e_tsec,@e_tuni,@e_tum,@e_dc,@e_op; END; CLOSE c_ens; DEALLOCATE c_ens;")
    w("DECLARE @c_ens varchar(20), @c_ordre varchar(6), @c_pro varchar(20), @c_qte float, @c_um varchar(2), @c_tr varchar(1), @c_div float, @c_divum varchar(2);")
    w("DECLARE c_cmp CURSOR LOCAL FOR SELECT ENS_ID, ORDRE, PRO_ID, QTE, QTEUM, TYPRATIO, DIV, DIVUM FROM ENSCOMPO WHERE ENS_ID IN (%s) ORDER BY ENS_ID, ORDRE;"
      % (",".join(q(e) for e in ens_ids) or "''"))
    w("OPEN c_cmp; FETCH NEXT FROM c_cmp INTO @c_ens,@c_ordre,@c_pro,@c_qte,@c_um,@c_tr,@c_div,@c_divum;")
    w("WHILE @@FETCH_STATUS = 0 BEGIN")
    w("  EXEC dbo.up_SOUENSCO_Update @UniqueId=NULL, @SOU_ID=@SOU_ID, @ENS_ID=@c_ens, @PRO_ID=@c_pro, @ORDRE=@c_ordre, @QTE=@c_qte, @QTEUM=@c_um, @TYPRATIO=@c_tr, @DIV=@c_div, @DIVUM=@c_divum;")
    w("  FETCH NEXT FROM c_cmp INTO @c_ens,@c_ordre,@c_pro,@c_qte,@c_um,@c_tr,@c_div,@c_divum; END; CLOSE c_cmp; DEALLOCATE c_cmp;")
    w("DECLARE @p_id varchar(20), @p_clemanu varchar(30), @p_cledist varchar(20), @p_clepers varchar(20), @p_desc varchar(60), @p_cou float, @p_um varchar(2), @p_qpp float,"
      " @p_esc float, @p_prom float, @p_tmp float, @p_tmpum varchar(2), @p_mul float, @p_cat varchar(3), @p_four varchar(2), @p_dcout datetime;")
    w("DECLARE c_pro CURSOR LOCAL FOR SELECT PRO_ID, CLEMANU, CLEDIST, CLEPERS, [DESC], COUBRUTUNI, COUUM, QPP, COUESC, PROMCOUNET, TEMPUNI, TEMPUM, MULCOM, CODECAT, CODEFOUR, DATECOUT"
      " FROM PRODUITS WHERE PRO_ID IN (SELECT PRO_ID FROM ENSCOMPO WHERE ENS_ID IN (%s)) OR PRO_ID IN (%s) ORDER BY PRO_ID;"
      % (",".join(q(e) for e in ens_ids) or "''", ",".join(q(p) for p in pro_ids) or "''"))
    w("OPEN c_pro; FETCH NEXT FROM c_pro INTO @p_id,@p_clemanu,@p_cledist,@p_clepers,@p_desc,@p_cou,@p_um,@p_qpp,@p_esc,@p_prom,@p_tmp,@p_tmpum,@p_mul,@p_cat,@p_four,@p_dcout;")
    w("WHILE @@FETCH_STATUS = 0 BEGIN")
    w("  EXEC dbo.up_SOUPRO_Update @UniqueId=NULL, @SOU_ID=@SOU_ID, @PRO_ID=@p_id, @CLEMANU=@p_clemanu, @CLEDIST=@p_cledist, @CLEPERS=@p_clepers, @DESC=@p_desc,"
      " @QTEENS=0, @QTELOT=0, @QTEOTH=0, @CALCTIMSTP='', @COUBRUTUNI=@p_cou, @COUUM=@p_um, @QPP=@p_qpp, @COUESC=@p_esc, @PROMCOUNET=@p_prom,"
      " @TEMPUNI=@p_tmp, @TEMPUM=@p_tmpum, @MULCOM=@p_mul, @CODEIMPR='', @CODEFOUR=@p_four, @CODECAT=@p_cat, @DATECOUT=@p_dcout, @DATECOUNET=NULL,"
      " @RESCOUNET=0, @QTECOM=0, @QTEACOM=0, @ISVIRT=0, @VIRTCOUNT=0;")
    w("  FETCH NEXT FROM c_pro INTO @p_id,@p_clemanu,@p_cledist,@p_clepers,@p_desc,@p_cou,@p_um,@p_qpp,@p_esc,@p_prom,@p_tmp,@p_tmpum,@p_mul,@p_cat,@p_four,@p_dcout; END; CLOSE c_pro; DEALLOCATE c_pro;")

    w("PRINT '=== 4. Takeoff lines (SOUREL, TYPERELEVE=P): one per plan x layer x linked group; EXT_ID = GroupID ===';")
    ordre = 0
    for d in linked:
        g = groups[d["group"]]
        ordre += 10
        if d["kind"] == "Counter":
            qte, um = d["n"], "U"
        else:
            qte, um = round(d["length_px"] * a.px_to_unit, 3), a.umplan
        w("-- %s GroupID=%s '%s' on plan #%d '%s' (%s), layer %s: %d elements%s"
          % (d["kind"], d["group"], d["name"], d["plan_idx"], d["plan"], d["plan_file"], d["layer_idx"], d["n"],
             (", %.1f px x %g" % (d["length_px"], a.px_to_unit)) if d["kind"] == "Line" else ""))
        w("EXEC dbo.up_SOUREL_Update @UniqueId=NULL, @SOU_ID=@SOU_ID, @BLO_ID=%s, @DIV_ID=%s, @TYPERELEVE='P', @EXT_ID=%s, @ORDRE=%s,"
          % (q(str(d["plan_idx"])), q(str(d["layer_idx"])), q(d["group"][:20]), q("%06d" % ordre)))
        w("  @TYPEITEM=%s, @ITEM_ID=%s, @DESCR=%s, @QTE=%s, @SECTION=0, @QTEUM=%s, @PROFIT=%g, @TYPETAXE=%s, @CODEIMPR='',"
          % (q(g["ItemType"]), q(g["ItemID"]), q((d["name"] or g["Description"])[:60]), qte, q(um), a.profit, q(a.typetaxe)))
        w("  @COUTANBRUT=0, @TEMPSUNIT=0, @TEMPSSEC=0, @TEMPSUM='', @PROFITPLUS=0, @PROFITMOIN=0, @ACC_NO='', @ACH_NO='', @ACT_NO='';")

    w("PRINT '=== 5. Not importable: drawn objects whose group has no EEExchangeData (no ITEM_ID -> nothing to price) ===';")
    w("-- %d objects in %d groups, e.g.:" % (len(unlinked), len({d["group"] for d in unlinked})))
    for d in unlinked[:8]:
        w("--   %s GroupID=%s '%s' plan #%d layer %s: %d elements" % (d["kind"], d["group"], d["name"], d["plan_idx"], d["layer_idx"], d["n"]))

    w("PRINT '=== 6. Roll-up: sp_SOUPRO_Quantity_V2 -> SOUPRO.QTEENS / QTEOTH ===';")
    # @REPLACE_FILTER must be > 0: with 0 the three sp_SOU_UpdateQteTotal*_v2 procedures CLOSE a cursor (CUR_2)
    # they never opened (6 x Msg 16916, executed 2026-09-27). With > 0 they EXEC dbo.sp_SOU_CalculCodeImpr for
    # every SOUREL row whose CODEIMPR <> '' - a call that fails (Msg 2812) in the rebuilt database because the
    # procedure only exists under the literal name [dbo].[dbo.sp_SOU_CalculCodeImpr] (docs/SCHEMA.md section 6).
    # Every SOUREL row above is therefore written with @CODEIMPR='' (section 4).
    w("EXEC dbo.sp_SOUPRO_Quantity_V2 @SOU_ID=@SOU_ID, @REPLACE_FILTER=1, @DoLog=0, @SOUPROLOG='';")
    w("SELECT BLO_ID, DIV_ID, EXT_ID, TYPEITEM, ITEM_ID, DESCR, QTE, QTEUM FROM SOUREL WHERE SOU_ID=@SOU_ID ORDER BY ORDRE;")
    w("SELECT ENS_ID, ENS_ORG_ID, CLEPERS, [DESC], COUUM FROM SOUENS WHERE SOU_ID=@SOU_ID;")
    w("SELECT ENS_ID, PRO_ID, QTE, QTEUM, TYPRATIO, DIV, DIVUM FROM SOUENSCO WHERE SOU_ID=@SOU_ID ORDER BY ENS_ID, ORDRE;")
    w("SELECT PRO_ID, COUUM, QTEENS, QTEOTH, QTELOT, CALCTIMSTP FROM SOUPRO WHERE SOU_ID=@SOU_ID ORDER BY PRO_ID;")
    w("SELECT SOU_ID, EXTAPP, EXTFILE, UMPLAN, CALCTIMSTP FROM SOUMIS WHERE SOU_ID=@SOU_ID;")
    w("PRINT '=== 7. Totals of the material takeoff (sp_SOU_CalculTotaux P, ModeCalcul=C, DoLog=1) ===';")
    w("EXEC dbo.sp_SOU_CalculTotaux @SOU_ID=@SOU_ID, @TypeReleve='P', @EE_CALGARY=0, @ModeCalcul='C', @VendantUAvantVendantT=1, @VPM=2, @DoLog=1;")
    print("\n".join(out))


if __name__ == "__main__":
    main()
