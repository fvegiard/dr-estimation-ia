"""Tests du contrôle qualité bloquant (releve/controle_qualite.py) : chaque règle détecte l'erreur introduite, et un relevé propre passe."""
import os, importlib.util, pathlib

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


def test_ecart_reference_bloquant(tmp_path):
    w = dossier(tmp_path)
    ref = tmp_path / "ref.csv"; ref.write_text("feuille,designation,qte\nX,K,2\nX,DT,5\n", encoding="utf-8")
    r = cq.controler(w, str(ref), "X")
    assert not r["conforme"] and any("famille DT" in e for e in r["erreurs"])
    ref.write_text("feuille,designation,qte\nX,K,2\nX,DT,1\n", encoding="utf-8")
    assert cq.controler(w, str(ref), "X")["conforme"]
