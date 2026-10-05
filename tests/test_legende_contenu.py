"""Correctif E08 (2026-10-05) : familles tirées de la légende, une famille par symbole, modèle tiré du devis.

Règles générales seulement (aucune quantité de l'exemplaire) : vocabulaire des codes (`releve/legende.py`), découpe
d'un devis en articles, contrôles Q11-Q14 de `releve/controle_qualite.py`, garde d'outils du contrôle à l'aveugle.
"""
import importlib.util
import json
import pathlib
import sys

import pymupdf

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "releve"))
import legende as LG  # noqa: E402
import tool_guard  # noqa: E402

SPEC = importlib.util.spec_from_file_location("cq_leg", ROOT / "releve" / "controle_qualite.py")
cq = importlib.util.module_from_spec(SPEC); SPEC.loader.exec_module(cq)


# --- vocabulaire --------------------------------------------------------------------------------------------
def test_code_attendu_distingue_les_prises_par_symbole():
    assert LG.code_attendu("PRISE DE COURANT AU DESSUS D'UN COMPTOIR") == "CT"
    assert LG.code_attendu("Prise de courant au-dessus d'un comptoir - DDFT") == "CG"
    assert LG.code_attendu("PRISE DE COURANT AVEC DISJONCTEUR DIFFÉRENTIEL DE FUITE À LA TERRE") == "GF"
    assert LG.code_attendu("PRISE DE COURANT POUR CUISINIÈRE 50A-120/240V") == "CP"
    assert LG.code_attendu("PRISE DE COURANT SIMPLE 30 A-120/240V") == "SE"
    assert LG.code_attendu("PRISE DE COURANT DOUBLE 15A-125V") == "PC"
    assert LG.code_attendu("PRISE DE COURANT DOUBLE 15A/20A-125V (5-20RA)") == ""     # hors vocabulaire : pas de code imposé


def test_code_attendu_autres_familles():
    cas = {"RACCORD DIRECT D'UN APPAREIL SPÉCIAL": "RA", "ÉVACUATEUR DE TOILETTE. VOIR VENTILATION.": "EV",
           "COMMUTATEUR UNIPOLAIRE 15A-125V": "CU", "COMMUTATEUR UNIPOLAIRE 15A-125V (3 VOIES)": "",
           "SORTIE TÉLÉPHONIQUE": "TE", "SORTIE POUR CABLO-DISTRIBUTION (TV)": "TV", "INTERCOME (CONTRÔLE DE PORTE)": "IC",
           "AVERTISSEUR DE FUMÉE MURAL 120V": "AF", "LUMINAIRE AU MUR TYPE A": "LA", "APPAREIL D'ÉCLAIRAGE TYPE D2": "LD2",
           "PLINTHE DE CHAUFFAGE": "PL", "THERMOSTAT DE PIÈCE": "TH", "PANNEAU DE DISTRIBUTION DE LOGEMENT": "PN",
           "BOITE DE JONCTION POUR RACCORD (FUTURE) D'UN LAVE-VAISSELLE": "BJ", "MINUTERIE": ""}
    for desc, code in cas.items():
        assert LG.code_attendu(desc) == code, desc


def test_variante_puissance():
    assert LG.variante_puissance("PLINTHE 300W", "PLINTHE 1500 W")
    assert LG.variante_puissance("PLINTHE DE CHAUFFAGE 1,5 KW", "PLINTHE DE CHAUFFAGE 750W")
    assert not LG.variante_puissance("PLINTHE 300W", "PLINTHE 300W")
    assert not LG.variante_puissance("PLINTHE 300W", "THERMOSTAT")


# --- devis ----------------------------------------------------------------------------------------------------
def _page_devis(tmp_path):
    doc = pymupdf.open()
    pg = doc.new_page(width=1200, height=800)
    y = 60
    lignes = [("1.GENERALITES", True), ("TEXTE GENERAL.", False),
              ("2.PRISES ELECTRIQUES", True), ("PRISE 15 A NEMA 5-15R INVIOLABLE.", False),
              ("MARQUE SPECIFIEE : HUBBELL MODELE HBL5262", False),
              ("PRISE 20 A GFCI.", False), ("MARQUE SPECIFIEE : ACME, SERIE X20", False),
              ("3.", True)]
    for t, gras in lignes:
        pg.insert_text((60, y), t, fontname="hebo" if gras else "helv", fontsize=8)
        y += 14
    pg.insert_text((83, y - 14), "APPAREILS D'ECLAIRAGE", fontname="hebo", fontsize=8)   # « 3. » + titre sur la même ligne
    pg.insert_text((60, y), "TYPE Z REGLETTE 600 MM.", fontname="helv", fontsize=8)
    pg.insert_text((60, y + 14), "1.GENERAL BIS", fontname="hebo", fontsize=8)          # numérotation qui repart
    pg.insert_text((60, y + 28), "AUTRE PARTIE.", fontname="helv", fontsize=8)
    p = tmp_path / "devis.pdf"; doc.save(p)
    return pymupdf.open(p)[0]


def test_articles_devis(tmp_path):
    arts = LG.articles_devis(_page_devis(tmp_path))
    par = {(a["partie"], a["article"]): a for a in arts}
    assert par[(1, "2.1")]["modele"] == "HUBBELL HBL5262" and "5-15R" in par[(1, "2.1")]["texte"]
    assert par[(1, "2.2")]["modele"] == "ACME X20"
    assert par[(1, "3.1")]["titre"] == "APPAREILS D'ECLAIRAGE" and par[(1, "3.1")]["modele"] == ""
    assert (2, "1.1") in par


# --- contrôles Q11-Q14 -----------------------------------------------------------------------------------------
LEG = ("feuille,section,no,symbole,description,code,statut,qte,preuve\n"
       "L00,ELECTRICITE,L01,cercle barre,PRISE DE COURANT AU DESSUS D'UN COMPTOIR,CT,compte,2,P1\n"
       "L00,ELECTRICITE,L02,cercle,PRISE DE COURANT DOUBLE 15A-125V,PC,compte,1,P1\n"
       "L00,ELECTRICITE,L03,carre,MINUTERIE,,absent,0,P1 toutes tuiles\n")
NOM_OK = ("label,famille,forme,rgb,jeton_regex,description,source,code,materiel,modele,discipline,legende\n"
          "CT,prise,cercle,,,,leg,CT,PRISE DE COURANT AU DESSUS D'UN COMPTOIR,HUBBELL A,electricite,L01\n"
          "CG,prise,cercle,,,,leg,CG,PRISE DE COURANT AU DESSUS D'UN COMPTOIR - DDFT,HUBBELL B,electricite,L01\n"
          "PC,prise,cercle,,,,leg,PC,PRISE DE COURANT DOUBLE 15A-125V,HUBBELL C,electricite,L02\n"
          "PL,chauffage,,,,,plan,PL,PLINTHE DE CHAUFFAGE (hors legende - R-001),MODELE NON INDIQUE DANS LA SOURCE ELECTRIQUE,electricite,HORS LEGENDE\n")
OCC_OK = ("feuille,label,x_pt,y_pt,source,note,designation\n"
          "P1,CT,11.3,12.7,visuel,,\nP1,CG,21.3,12.7,visuel,,C4\nP1,PC,31.3,12.7,visuel,,\n"
          "P1,PL,41.3,12.7,visuel,,\"300 W C13,15\"\nP1,PL,51.3,12.7,visuel,,\"1500 W C10,12\"\n")


def dossier(tmp_path, nomen=NOM_OK, occ=OCC_OK, leg=LEG, devis=True, roles="P1,plan\nL00,legende\n"):
    fichiers = {"feuilles.csv": "feuille,largeur_pt,hauteur_pt,role\n" + "\n".join(f"{r.split(',')[0]},100,100,{r.split(',')[1]}"
                                                                                 for r in roles.strip().splitlines()) + "\n",
                "feuilles-classement.csv": "feuille,type,echelle,note\nP1,plan,,\nL00,legende,,\n",
                "nomenclature.csv": nomen, "occurrences-visuel.csv": occ, "reserves.md": "R-001 PL hors legende",
                "rapport-releve.md": "ok"}
    if leg is not None:
        fichiers["legende.csv"] = leg
    for nom, txt in fichiers.items():
        (tmp_path / nom).write_text(txt, encoding="utf-8")
    if devis:
        (tmp_path / "devis").mkdir(exist_ok=True)
        (tmp_path / "devis" / "D1-articles.csv").write_text(
            "feuille,partie,section,titre,article,marque,modele,texte,x_pt,y_pt\nD1,1,2,PRISES,2.1,HUBBELL A,HUBBELL A,x,0,0\n",
            encoding="utf-8")
    return str(tmp_path)


def regles(res):
    return [e.split()[0] for e in res["erreurs"]]


def test_releve_conforme_a_la_legende(tmp_path):
    r = cq.controler(dossier(tmp_path))
    assert r["conforme"], r["erreurs"]


def test_q11_legende_fournie_sans_transcription(tmp_path):
    assert "Q11" in regles(cq.controler(dossier(tmp_path, leg=None)))


def test_q11_ligne_de_legende_oubliee(tmp_path):
    leg = LEG.replace("MINUTERIE,,absent,0,P1 toutes tuiles", "MINUTERIE,,,,")
    errs = cq.controler(dossier(tmp_path, leg=leg))["erreurs"]
    assert any(e.startswith("Q11") and "L03" in e for e in errs)


def test_q11_absent_sans_preuve_et_compte_sans_occurrence(tmp_path):
    leg = LEG.replace("absent,0,P1 toutes tuiles", "absent,0,")
    assert any("sans preuve" in e for e in cq.controler(dossier(tmp_path, leg=leg))["erreurs"])
    occ = "\n".join(l for l in OCC_OK.splitlines() if ",PC," not in l) + "\n"
    errs = cq.controler(dossier(tmp_path, occ=occ))["erreurs"]
    assert any(e.startswith("Q11") and "L02" in e for e in errs)


def test_q11_famille_sans_ligne_de_legende(tmp_path):
    nomen = NOM_OK.replace(",electricite,L02", ",electricite,")
    assert any(e.startswith("Q11") and "'PC'" in e for e in cq.controler(dossier(tmp_path, nomen=nomen))["erreurs"])


def test_q12_symbole_eclate_par_puissance(tmp_path):
    nomen = NOM_OK.replace("PL,chauffage,,,,,plan,PL,PLINTHE DE CHAUFFAGE (hors legende - R-001)",
                           "PLINTHE 300W,chauffage,,,,,plan,PL,PLINTHE DE CHAUFFAGE 300W") \
        + "PLINTHE 1500W,chauffage,,,,,plan,PL,PLINTHE DE CHAUFFAGE 1500W,X,electricite,HORS LEGENDE\n"
    occ = OCC_OK.replace(",PL,41.3", ",PLINTHE 300W,41.3").replace(",PL,51.3", ",PLINTHE 1500W,51.3")
    assert "Q12" in regles(cq.controler(dossier(tmp_path, nomen=nomen, occ=occ)))


def test_q12_meme_ligne_meme_code(tmp_path):
    nomen = NOM_OK + "PC DEMI,prise,cercle,,,,leg,PC,PRISE DE COURANT DOUBLE 15A-125V 1/2 COMMANDEE,HUBBELL C,electricite,L02\n"
    occ = OCC_OK + "P1,PC DEMI,61.3,12.7,visuel,,\n"
    assert "Q12" in regles(cq.controler(dossier(tmp_path, nomen=nomen, occ=occ)))


def test_q13_modele_vide_malgre_devis(tmp_path):
    nomen = NOM_OK.replace(",HUBBELL C,", ",,")
    (tmp_path / "a").mkdir(); (tmp_path / "b").mkdir()
    assert "Q13" in regles(cq.controler(dossier(tmp_path / "a", nomen=nomen)))
    assert "Q13" not in regles(cq.controler(dossier(tmp_path / "b", nomen=nomen, devis=False)))


def test_q14_code_invente(tmp_path):
    nomen = NOM_OK.replace("PC,prise,cercle,,,,leg,PC,", "PC,prise,cercle,,,,leg,PD,")
    errs = cq.controler(dossier(tmp_path, nomen=nomen))["erreurs"]
    assert any(e.startswith("Q14") and "'PD'" in e and "'PC'" in e for e in errs)


def _plan_cercles(tmp_path):
    """Feuille P1 : trois cercles Ø16 trait 1 (même symbole) et un cercle Ø10 trait 0,5 (autre chose)."""
    (tmp_path / "feuilles").mkdir(exist_ok=True)
    doc = pymupdf.open()
    pg = doc.new_page(width=100, height=100)
    for cx, cy, r, w in ((20.5, 20.5, 8, 1), (50.5, 20.5, 8, 1), (80.5, 70.5, 8, 1), (50.5, 70.5, 5, 0.5)):
        pg.draw_circle((cx, cy), r, width=w)
    doc.save(tmp_path / "feuilles" / "P1.pdf")


def test_q15_symbole_identique_non_releve(tmp_path):
    nomen = ("label,famille,forme,rgb,jeton_regex,description,source,code,materiel,modele,discipline,legende\n"
             "PC,prise,cercle,,,,leg,PC,PRISE DE COURANT DOUBLE 15A-125V,HUBBELL C,electricite,L02\n")
    occ = "feuille,label,x_pt,y_pt,source,note\nP1,PC,20.5,20.5,visuel,\nP1,PC,50.5,20.5,visuel,\n"
    leg = LEG.replace("CT,compte,2,P1", "CT,absent,0,P1 vu").replace(
        "PC,compte,1,P1", "PC,compte,2,P1")
    w = dossier(tmp_path, nomen=nomen, occ=occ, leg=leg, devis=False)
    _plan_cercles(tmp_path)
    errs = cq.controler(w)["erreurs"]
    q15 = [e for e in errs if e.startswith("Q15")]
    assert len(q15) == 1 and "(80.5, 70.5)" in q15[0], errs           # le cercle Ø10 (autre signature) n'est pas signalé
    (tmp_path / "reserves.md").write_text("R-001 PL\nR-002 Q15 (80, 71) : bulle de détail, pas un appareil\n", encoding="utf-8")
    assert not [e for e in cq.controler(w)["erreurs"] if e.startswith("Q15")]


# --- garde d'outils : contrôle à l'aveugle seulement --------------------------------------------------------------
def test_tool_guard_controle_qualite(tmp_path):
    root = str(tmp_path)
    ok = tool_guard.validate("Bash", {"command": f"uv run releve/controle_qualite.py {root}"}, str(ROOT), root)
    assert ok is None
    ref = tool_guard.validate("Bash", {"command": f"uv run releve/controle_qualite.py {root} --reference x.csv"}, str(ROOT), root)
    assert ref and "un seul argument" in ref
    dehors = tool_guard.validate("Bash", {"command": f"uv run releve/controle_qualite.py {ROOT}"}, str(ROOT), root)
    assert dehors and "hors du dossier" in dehors


def test_outil_controle_autorise_partout():
    """Le contrôle est autorisé de la même façon dans les 4 routes d'agent (SDK, CLI, compétence, sous-agent)."""
    motif = "uv run releve/controle_qualite.py *"
    assert motif in (ROOT / "releve" / "agent_sdk.py").read_text(encoding="utf-8")
    assert motif in (ROOT / "releve" / "run.py").read_text(encoding="utf-8")
    assert motif in (ROOT / ".claude" / "skills" / "releve-planexpert" / "SKILL.md").read_text(encoding="utf-8")
    assert motif in (ROOT / ".claude" / "agents" / "releveur.md").read_text(encoding="utf-8")


def test_competence_sans_donnee_de_l_exemplaire():
    """Essai à l'aveugle : la compétence ne contient aucun modèle ni quantité de l'exemplaire HR26-14 (E08/E15)."""
    txt = (ROOT / ".claude" / "skills" / "releve-planexpert" / "SKILL.md").read_text(encoding="utf-8")
    for interdit in ("LEVITON", "CANARM", "STELPRO", "T5320", "RGF20", "ICW52", "2651-2/3W", "REGLETTE DEL 550"):
        assert interdit not in txt, interdit
    json.dumps(txt)  # le fichier reste du texte valide
