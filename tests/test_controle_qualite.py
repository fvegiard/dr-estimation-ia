"""Tests du contrôle qualité bloquant (releve/controle_qualite.py) : chaque règle détecte l'erreur introduite, et un relevé propre passe."""
import importlib.util
import pathlib
import pytest

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


@pytest.mark.parametrize("classement", [
    "P1,plan,,\n",  # P2 missing
    "P1,plan,,\nP2,legende,,\nP2,autre,,\n",  # duplicate classification
    "P1,plan,,\nP2,legende,,\nUNKNOWN,autre,,\n",
])
def test_q1_requires_each_input_sheet_classified_once(tmp_path, classement):
    work = dossier(tmp_path)
    (tmp_path / "feuilles.csv").write_text("feuille,largeur_pt,hauteur_pt\nP1,100,100\nP2,100,100\n", encoding="utf-8")
    (tmp_path / "feuilles-classement.csv").write_text("feuille,type,echelle,note\n" + classement, encoding="utf-8")
    result = cq.controler(work)
    assert not result["conforme"]
    assert "Q1" in regles(result)


def test_q1_accepts_legends_and_other_sheets_without_occurrences(tmp_path):
    work = dossier(tmp_path)
    (tmp_path / "feuilles.csv").write_text("feuille,largeur_pt,hauteur_pt\nP1,100,100\nL1,100,100\nX1,100,100\n", encoding="utf-8")
    (tmp_path / "feuilles-classement.csv").write_text("feuille,type,echelle,note\nP1,plan,,\nL1,legende,,\nX1,autre,,\n", encoding="utf-8")
    assert cq.controler(work)["conforme"]


@pytest.mark.parametrize("width", ["0", "-10", "nan", "inf", "invalid"])
def test_q7_rejects_invalid_sheet_dimensions(tmp_path, width):
    work = dossier(tmp_path)
    (tmp_path / "feuilles.csv").write_text(f"feuille,largeur_pt,hauteur_pt\nP1,{width},100\n", encoding="utf-8")
    result = cq.controler(work)
    assert not result["conforme"]
    assert "Q7" in regles(result)


@pytest.mark.parametrize("x", ["15", "nan", "inf"])
def test_q7_rejects_unknown_occurrence_sheet(tmp_path, x):
    result = cq.controler(dossier(tmp_path, occ=OCC + f"UNKNOWN,KLAXON,{x},20,visuel,[K1.1]\n"))
    assert not result["conforme"]
    assert "Q7" in regles(result)


@pytest.mark.parametrize("x", ["nan", "inf", "-inf"])
def test_q7_rejects_nonfinite_coordinates(tmp_path, x):
    result = cq.controler(dossier(tmp_path, occ=OCC.replace("P1,KLAXON,10,10", f"P1,KLAXON,{x},10")))
    assert not result["conforme"]
    assert "Q7" in regles(result)


@pytest.mark.parametrize("excluded", ["1", "oui", "x", "true", " TRUE ", "X", " OUI "])
def test_exclusions_match_renderer_without_false_duplicates(tmp_path, excluded):
    rows = OCC.rstrip().splitlines()
    occ = rows[0] + ",exclure\n" + "".join(row + ",\n" for row in rows[1:])
    occ += f"P1,KLAXON,10,10,visuel,[K1.1],{excluded}\n"
    result = cq.controler(dossier(tmp_path, occ=occ))
    assert result["conforme"]
    assert result["occurrences"] == 3


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


def test_q10_lectures_arrondies_averties_sans_bloquer(tmp_path):
    """Entre le relevé lu et le relevé inventé : kimi-k3 arrondit 38 % de ses marques.

    Ce n'est pas une fabrication (Q10 ne bloque pas) mais c'est 40 fois le taux mesuré
    chez les humains (0,9 %) : l'avertissement le dit au lieu de laisser croire à un
    relevé precis."""
    melange = LUES + INVENTEES[:6]           # 6 rondes sur 16, soit 38 %
    r = cq.controler(dossier(tmp_path, occ=_occ(melange)))
    assert "Q10" not in regles(r)
    assert any(e.startswith("Q10") and "arrondies" in e for e in r["avertissements"])


def test_q10_releve_lu_sans_avertissement(tmp_path):
    """Un relevé aux coordonnées lues ne déclenche ni erreur ni avertissement Q10."""
    r = cq.controler(dossier(tmp_path, occ=_occ(LUES)))
    assert not any(e.startswith("Q10") for e in r["erreurs"] + r["avertissements"])


# kimi-k3 sur DSI01 : 38 % des marques sur un multiple de 10, mais 104/104 sur un multiple de 5.
# L'arrondi fin ressemble à une lecture précise ; c'est la même invention, en plus discret.
ARRONDI_FIN = [(15, 45), (55, 10), (25, 75), (90, 35), (45, 65), (5, 20), (60, 55), (35, 15), (80, 85), (20, 60)]


def test_q10_grille_de_5_bloquante(tmp_path):
    """Toutes les marques sur un multiple de 5 : bloqué même si peu sont multiples de 10.

    Base mesurée sur les 319 marques des relevés humains du dépôt : 3,1 % seulement
    tombent sur un multiple de 5 dans les deux axes. 100 % n'est pas une lecture."""
    r = cq.controler(dossier(tmp_path, occ=_occ(ARRONDI_FIN)))
    assert "Q10" in regles(r)
    assert r["grilles_suspectes"]["P1"]["pas"] == 5
    assert not r["conforme"]


def test_q10_base_humaine_sous_le_seuil_de_5():
    """Les coordonnées lues ne s'alignent pas non plus sur 5 pt : pas de fausse alerte."""
    assert cq.grille_suspecte(LUES) is None
    assert cq.part_arrondie(LUES, pas=5) == 0.0


def test_q8_nomme_la_confusion_probable(tmp_path):
    """Un libellé jamais relevé est le plus souvent absorbé par un voisin de même famille et forme.

    Cas réel kimi-k3 sur DSI01 : AVERTISSEUR FUMEE AUTONOME lu dans la légende, écrit dans la
    nomenclature, jamais relevé ; ses 36 appareils comptés en DETECTEUR FUMEE. Q8 doit nommer le
    voisin pour que « il manque un appareil » devienne « lequel l'a absorbé »."""
    nomen = (NOMEN + "AVERTISSEUR FUMEE AUTONOME,alarme,cercle,,,avertisseur 120V,leg\n"
                     "DETECTEUR FUMEE,alarme,cercle,,,detecteur reseau,leg\n")
    occ = OCC + "P1,DETECTEUR FUMEE,45,10,visuel,[DF1.1]\nP1,DETECTEUR FUMEE,55,10,visuel,[DF1.2]\n"
    e = [x for x in cq.controler(dossier(tmp_path, nomen=nomen, occ=occ))["erreurs"]
         if x.startswith("Q8") and "AVERTISSEUR FUMEE AUTONOME" in x]
    assert e and "confusion probable avec 'DETECTEUR FUMEE'" in e[0] and "2 marques" in e[0]


def test_q8_prefere_le_voisin_qui_partage_les_mots(tmp_path):
    """Le voisin le plus probable partage le vocabulaire, pas seulement la famille.

    Sans ce classement, DETECTEUR THERMIQUE 135F était rattaché au libellé le plus fréquent
    (DETECTEUR FUMEE) au lieu du générique qui l'absorbe réellement."""
    nomen = (NOMEN + "DETECTEUR THERMIQUE 135F,alarme,cercle,,,thermique fixe,leg\n"
                     "DETECTEUR FUMEE,alarme,cercle,,,fumee,leg\n")
    occ = ("feuille,label,x_pt,y_pt,source,note\n"
           + "".join(f"P1,DETECTEUR FUMEE,{10+i},10,visuel,[DF1.{i+1}]\n" for i in range(5))
           + "P1,DETECTEUR THERMIQUE,80,10,visuel,[DT1.1]\n")
    e = [x for x in cq.controler(dossier(tmp_path, nomen=nomen, occ=occ))["erreurs"]
         if x.startswith("Q8") and "135F" in x]
    assert e and "'DETECTEUR THERMIQUE'" in e[0] and "mot(s) en commun" in e[0]


def test_q8_sans_voisin_reste_simple(tmp_path):
    """Sans voisin de même famille et forme, Q8 ne doit pas inventer de piste."""
    nomen = NOMEN + "RELAIS ADRESSABLE,distribution,losange,,,relais,leg\n"
    e = [x for x in cq.controler(dossier(tmp_path, nomen=nomen))["erreurs"]
         if x.startswith("Q8") and "RELAIS" in x]
    assert e and "confusion probable" not in e[0]
