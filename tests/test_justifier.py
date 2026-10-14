"""Dossier de justification des désaccords `src.validation.justifier` —
consommateur du contrat gelé `ecarts-classes.csv` (en-tête exact, positions
`x:y` pixels IA). Fixtures écrites ici même : aucune dépendance à
`classer_ecarts`.
"""
from __future__ import annotations

import pytest

from src.validation import justifier

EN_TETE = "classe,feuille_humaine,feuille_ia,libelle_humain,libelle_ia,position_humaine,position_ia,detail"

CSV_FIXTURE = (
    EN_TETE + "\n"
    'omission,E08-1,,Luminaire DS1,,512:340,,"raster ex08-1.png"\n'
    "en_trop,,E08-1,,Prise duplex,,741:1290,\n"
    "mauvaise_famille,E08-1,E08-1,Détecteur de fumée,Boîte de jonction,498:331,512:340,"
    "raster ex08-1.png\n"
)


def _ecrire_fixture(tmp_path, contenu: str = CSV_FIXTURE):
    csv_path = tmp_path / "ecarts-classes.csv"
    csv_path.write_text(contenu, encoding="utf-8")
    return csv_path


def _remplir(texte: str, marqueur: str, preuve: str, verdict: str) -> str:
    """Simule le remplissage à la main : cellules preuve/verdict de la ligne
    du tableau qui contient `marqueur`."""
    lignes = []
    for l in texte.splitlines():
        if l.startswith("|") and marqueur in l:
            cells = l.split("|")
            assert len(cells) >= 9, f"ligne inattendue : {l}"
            cells[-3], cells[-2] = f" {preuve} ", f" {verdict} "
            l = "|".join(cells)
        lignes.append(l)
    return "\n".join(lignes)


def _remplir_tout(texte: str) -> str:
    texte = _remplir(texte, "Luminaire DS1", "tuile E08-1 r2c3 : étiquette DS1 vue sur le plan",
                     "estimateur correct")
    texte = _remplir(texte, "Prise duplex", "tuile E08-1 r3c1 : prise dessinée, absente du relevé IA",
                     "IA correcte")
    texte = _remplir(texte, "Boîte de jonction",
                     "légende E08 : carré plein = détecteur ; cercle = boîte",
                     "ambigu -> réserve")
    return texte


# --------------------------------------------------------------- génération

def test_generer_dossier_lignes_positions_rappels(tmp_path):
    csv_path = _ecrire_fixture(tmp_path)
    sortie = justifier.generer_dossier(csv_path, tmp_path)
    assert sortie == tmp_path / "justifications.md" and sortie.is_file()
    contenu = sortie.read_text(encoding="utf-8")
    lignes_tab = [l for l in contenu.splitlines()
                  if l.startswith("|") and any(v in l for v in ("Luminaire DS1", "Prise duplex", "Boîte de jonction"))]
    assert len(lignes_tab) == 3          # 1 ligne du tableau par désaccord
    # positions exactes, pixels IA rendues en x, y
    assert "humain 512, 340" in contenu
    assert "IA 741, 1290" in contenu
    assert "IA 512, 340 ; humain 498, 331" in contenu
    # raster lu dans la colonne detail du contrat
    assert "(raster ex08-1.png)" in contenu
    # rappels étapes 5 et 7
    assert "Symétrie" in contenu and "l'estimateur qui s'est trompé" in contenu
    assert "quantité plus élevée seule n'est jamais une amélioration" in contenu
    assert "sans preuve = non tranché" in contenu
    assert "ambigu → réserve" in contenu
    # preuve et verdict à remplir (cellules vides) — la ligne reste 7 colonnes
    for l in lignes_tab:
        cells = [c.strip() for c in l.strip().strip("|").split("|")]
        assert len(cells) == 7
        assert cells[5] == "" and cells[6] == ""


def test_generer_sortie_surchargee(tmp_path):
    csv_path = _ecrire_fixture(tmp_path)
    cible = tmp_path / "sous" / "dossier-a-remplir.md"
    sortie = justifier.generer_dossier(csv_path, tmp_path / "autre", sortie=cible)
    assert sortie == cible and cible.is_file()
    assert not (tmp_path / "justifications.md").exists()


def test_generer_aucun_desaccord(tmp_path):
    csv_path = _ecrire_fixture(tmp_path, EN_TETE + "\n")
    sortie = justifier.generer_dossier(csv_path, tmp_path)
    contenu = sortie.read_text(encoding="utf-8")
    assert "Aucun désaccord à justifier" in contenu
    rapport = justifier.controler_justifications(sortie)
    assert rapport.etat == "COMPLET" and rapport.lignes == 0


# ------------------------------------------------------------------ contrôle

def test_controler_fichier_tranche(tmp_path):
    csv_path = _ecrire_fixture(tmp_path)
    dossier = justifier.generer_dossier(csv_path, tmp_path)
    rempli = _remplir_tout(dossier.read_text(encoding="utf-8"))
    dossier.write_text(rempli, encoding="utf-8")
    rapport = justifier.controler_justifications(dossier, ecarts_csv=csv_path)
    assert rapport.lignes == 3
    assert rapport.tranches == 3 and rapport.non_tranches == 0
    assert rapport.ambigus == 1          # « ambigu -> réserve » accepté
    assert rapport.lignes_csv_absentes == []
    assert rapport.etat == "COMPLET"
    assert justifier.main(["controler", str(dossier), "--ecarts", str(csv_path)]) == 0


def test_controler_verdict_vide_ou_sans_preuve(tmp_path):
    csv_path = _ecrire_fixture(tmp_path)
    dossier = justifier.generer_dossier(csv_path, tmp_path)
    texte = dossier.read_text(encoding="utf-8")
    texte = _remplir(texte, "Luminaire DS1", "tuile E08-1 r2c3 : vu au plan", "IA correcte")
    # ligne 2 : verdict rempli mais preuve vide — ligne 3 : rien du tout
    texte = _remplir(texte, "Prise duplex", "", "IA correcte")
    dossier.write_text(texte, encoding="utf-8")
    rapport = justifier.controler_justifications(dossier)
    assert rapport.non_tranches == 2
    assert len(rapport.sans_preuve) == 1
    assert any("sans preuve" in d for d in rapport.details)
    assert any("verdict vide" in d for d in rapport.details)
    assert rapport.tranches == 1
    assert rapport.etat == "INCOMPLET"
    assert justifier.main(["controler", str(dossier)]) == 1


def test_controler_estimateur_correct_sans_preuve(tmp_path):
    csv_path = _ecrire_fixture(tmp_path)
    dossier = justifier.generer_dossier(csv_path, tmp_path)
    texte = _remplir(dossier.read_text(encoding="utf-8"), "Luminaire DS1", "",
                     "estimateur correct")
    dossier.write_text(texte, encoding="utf-8")
    rapport = justifier.controler_justifications(dossier)
    assert rapport.non_tranches == 3      # 1 sans preuve + 2 verdicts vides
    assert len(rapport.sans_preuve) == 1
    assert any("estimateur correct" in d and "sans preuve" in d for d in rapport.details)
    assert any("estimateur correct" in d for d in rapport.sans_preuve)


def test_controler_accents_verdicts_reconnus(tmp_path):
    csv_path = _ecrire_fixture(tmp_path)
    dossier = justifier.generer_dossier(csv_path, tmp_path)
    texte = dossier.read_text(encoding="utf-8")
    texte = _remplir(texte, "Luminaire DS1", "vue au zoom", "Estimateur correct")
    texte = _remplir(texte, "Prise duplex", "vue au zoom", "IA CORRECTE")
    texte = _remplir(texte, "Boîte de jonction", "vue au zoom", "Ambigu -> réserve")
    dossier.write_text(texte, encoding="utf-8")
    rapport = justifier.controler_justifications(dossier)
    assert rapport.tranches == 3 and rapport.non_tranches == 0
    assert rapport.ambigus == 1


def test_controler_ligne_csv_absente_signalee(tmp_path):
    csv_path = _ecrire_fixture(tmp_path)
    dossier = justifier.generer_dossier(csv_path, tmp_path)
    texte = dossier.read_text(encoding="utf-8")
    # le dossier omet la ligne « Prise duplex »
    texte = "\n".join(l for l in texte.splitlines() if "Prise duplex" not in l)
    texte = _remplir(texte, "Luminaire DS1", "tuile E08-1", "IA correcte")
    texte = _remplir(texte, "Boîte de jonction", "légende E08", "ambigu → réserve")
    dossier.write_text(texte, encoding="utf-8")
    rapport = justifier.controler_justifications(dossier, ecarts_csv=csv_path)
    assert rapport.tranches == 2 and rapport.non_tranches == 0
    assert len(rapport.lignes_csv_absentes) == 1
    assert "en_trop" in rapport.lignes_csv_absentes[0]
    assert rapport.etat == "INCOMPLET"
    assert justifier.main(["controler", str(dossier), "--ecarts", str(csv_path)]) == 1


def test_controler_doublon_deux_occurrences_meme_cle(tmp_path):
    csv_path = _ecrire_fixture(
        tmp_path,
        EN_TETE + "\n"
        "doublon,E08-1,E08-1,K,K,10:20,10:20,\n"
        "doublon,E08-1,E08-1,K,K,10:20,10:20,\n",
    )
    dossier = justifier.generer_dossier(csv_path, tmp_path)
    texte = dossier.read_text(encoding="utf-8")
    # deux lignes CSV identiques : n'en trancher qu'une seule dans le dossier
    lignes = texte.splitlines()
    del lignes[next(i for i, l in enumerate(lignes) if l.startswith("| doublon"))]
    texte = "\n".join(lignes)
    texte = _remplir(texte, "| K |", "deux marques IA superposées", "IA correcte")
    dossier.write_text(texte, encoding="utf-8")
    rapport = justifier.controler_justifications(dossier, ecarts_csv=csv_path)
    assert rapport.tranches == 1 and rapport.non_tranches == 0
    # 1 occurrence du doublon en double reste attendue dans le dossier
    assert len(rapport.lignes_csv_absentes) == 1
    assert "doublon" in rapport.lignes_csv_absentes[0]
    assert rapport.etat == "INCOMPLET"


# ------------------------------------------------------------------- contrat

def test_erreurs_contrat_code_2(tmp_path):
    csv_path = _ecrire_fixture(tmp_path)
    # en-tête hors contrat (ordre permuté)
    mauvais = tmp_path / "mauvais.csv"
    mauvais.write_text(
        "classe,feuille_ia,feuille_humaine,libelle_humain,libelle_ia,"
        "position_humaine,position_ia,detail\nomission,,,,,,,\n", encoding="utf-8")
    with pytest.raises(justifier.JustifierErreur, match="en-tête hors contrat"):
        justifier.generer_dossier(mauvais, tmp_path)
    # classe inconnue
    mauvaise_classe = tmp_path / "classe.csv"
    mauvaise_classe.write_text(
        EN_TETE + "\nfaux_positif,E08-1,E08-1,A,B,,,,\n", encoding="utf-8")
    assert justifier.main(["generer", "--ecarts", str(mauvaise_classe),
                           "--dossier", str(tmp_path)]) == 2
    # position sans le format x:y pixels IA
    mauvaise_pos = tmp_path / "position.csv"
    mauvaise_pos.write_text(
        EN_TETE + "\nomission,E08-1,E08-1,A,B,abc:12,,\n", encoding="utf-8")
    assert justifier.main(["generer", "--ecarts", str(mauvaise_pos),
                           "--dossier", str(tmp_path)]) == 2
    # fichier de contrôle introuvable
    assert justifier.main(["controler", str(tmp_path / "absent.md")]) == 2
    # dossier sans tableau
    sans_tableau = tmp_path / "vide.md"
    sans_tableau.write_text("rien ici", encoding="utf-8")
    assert justifier.main(["controler", str(sans_tableau)]) == 2