"""Tests du contrôle qualité bloquant (releve/controle_qualite.py) : chaque règle détecte l'erreur introduite, et un relevé propre passe."""
import importlib.util
import pathlib

SPEC = importlib.util.spec_from_file_location("cq", pathlib.Path(__file__).resolve().parents[1] / "releve" / "controle_qualite.py")
cq = importlib.util.module_from_spec(SPEC); SPEC.loader.exec_module(cq)

NOMEN = "label,famille,forme,rgb,jeton_regex,description,source\nKLAXON,alarme,carre,,K,KLAXON,leg\nDETECTEUR THERMIQUE,alarme,cercle,,DT,DT,leg\n"
OCC = ("feuille,label,x_pt,y_pt,source,note\n"
       "P1,KLAXON,10,10,visuel,[K1.1]\nP1,KLAXON,20,10,visuel,[K1.2]\nP1,DETECTEUR THERMIQUE,30,10,visuel,[DT1.1]\n")


def dossier(tmp_path, nomen=NOMEN, occ=OCC, reserves="R-001 rien"):
    for nom, txt in {"feuilles.csv": "feuille,largeur_pt,hauteur_pt\nP1,100,100\n", "feuilles-classement.csv": "feuille,type,echelle,note\nP1,plan,,\n",
                     "nomenclature.csv": nomen, "occurrences-visuel.csv": occ, "reserves.md": reserves, "rapport-releve.md": "ok"}.items():
        (tmp_path / nom).write_text(txt, encoding="utf-8")
    return str(tmp_path)


def regles(res):
    return {e.split()[0] for e in res["erreurs"]}


def test_releve_propre_conforme(tmp_path):
    assert cq.controler(dossier(tmp_path))["conforme"]


def test_erreurs_introduites_detectees(tmp_path):
    occ = OCC + ("P1,DETECTEUR THERMIQUE,40,10,visuel,[K1.5]\n"     # Q4 classement + Q6 trou K1.3-K1.4
                 "P1,KLAXON,50,10,visuel,[K1.1]\n"                  # Q5 doublon
                 "P1,INCONNU,500,10,visuel,\n")                     # Q2 + Q7
    nomen = NOMEN + "KLAXON,alarme,carre,,P,PIEZO,leg\nRELAIS,alarme,carre,,RA,RELAIS,leg\n"   # Q3 fusion + Q8 jamais relevé
    assert {"Q2", "Q3", "Q4", "Q5", "Q6", "Q7", "Q8"} <= regles(cq.controler(dossier(tmp_path, nomen, occ)))


def test_trou_justifie_en_reserve(tmp_path):
    occ = OCC + "P1,KLAXON,40,10,visuel,[K1.4]\n"
    assert "Q6" in regles(cq.controler(dossier(tmp_path, occ=occ)))
    assert cq.controler(dossier(tmp_path, occ=occ, reserves="R-001 K1.3 hors feuille\nR-002 K1.3 et K1.4? non : K1.3"))["conforme"]


def test_ligne_mal_formee_signalee_sans_planter(tmp_path):
    """Un CSV d'agent avec une virgule non échappée ne doit pas faire planter le contrôle.

    csv.DictReader range le surplus dans une liste sous la clé None : le contrôle
    plantait dessus (AttributeError) au lieu de rapporter la ligne. Constaté sur la
    nomenclature produite par gemma-4-31b.
    """
    nomen = NOMEN + "SIRENE, extérieure,alarme,carre,,S,SIRENE,leg,champ en trop\n"
    r = cq.controler(dossier(tmp_path, nomen=nomen))
    assert "Q0" in regles(r)
    assert any("champ" in e and "trop" in e for e in r["erreurs"])


def test_ecart_reference_bloquant(tmp_path):
    w = dossier(tmp_path)
    ref = tmp_path / "ref.csv"; ref.write_text("feuille,designation,qte\nX,K,2\nX,DT,5\n", encoding="utf-8")
    r = cq.controler(w, str(ref), "X")
    assert not r["conforme"] and any("famille DT" in e for e in r["erreurs"])
    ref.write_text("feuille,designation,qte\nX,K,2\nX,DT,1\n", encoding="utf-8")
    assert cq.controler(w, str(ref), "X")["conforme"]


def _occ(points):
    lignes = "".join(f"P1,KLAXON,{x},{y},visuel,[K1.{i}]\n" for i, (x, y) in enumerate(points, start=1))
    return "feuille,label,x_pt,y_pt,source,note\n" + lignes


# un relevé lu sur un plan : coordonnées quelconques (aucun alignement)
LUES = [(13, 47), (56, 12), (28, 73), (91, 35), (44, 68), (7, 22), (62, 51), (35, 19), (78, 84), (21, 60)]
# un relevé inventé : tout tombe sur des multiples de 10, comme gemma-4-31b sur DSI01
INVENTEES = [(10, 40), (50, 10), (30, 70), (90, 30), (40, 60), (10, 20), (60, 50), (30, 10), (80, 80), (20, 60)]


def test_q10_coordonnees_lues_ne_declenchent_pas():
    """Aucune fausse alerte : des positions réelles ne s'alignent pas sur une grille."""
    assert cq.grille_suspecte(LUES) is None


def test_q10_grille_inventee_bloquante(tmp_path):
    """53/53 marques multiples de 10 en x ET en y : le modèle invente au lieu de lire."""
    r = cq.controler(dossier(tmp_path, occ=_occ(INVENTEES)))
    assert "Q10" in regles(r)
    assert r["grilles_suspectes"]["P1"] == {"pas": 10, "alignees": 10, "total": 10}
    assert not r["conforme"]


def test_q10_ignore_les_petits_releves():
    """Sous le seuil, l'alignement reste une coïncidence plausible : on n'accuse pas."""
    assert cq.grille_suspecte(INVENTEES[:4]) is None


def test_q10_tolere_quelques_coincidences():
    """Une minorité de coordonnées rondes dans un relevé lu ne doit pas bloquer."""
    assert cq.grille_suspecte(LUES + INVENTEES[:2]) is None
