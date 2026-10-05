# /// script
# requires-python = ">=3.12"
# dependencies = ["pymupdf>=1.24", "numpy>=1.24", "scipy>=1.11"]
# ///
"""Étape 4a (déterministe) : PDF « Plans annotés » au format cible HR26-14 (pastille pastel PAR-DESSUS le plan
vectoriel intact, calques OCG par famille, encadré « RELEVE <feuille> - MATERIEL », bordereau au format de la
feuille : matériel, agrégé ou travaux) — spec unique : docs/FORMAT-EXEMPLE.md. Remplace l'ancien rendu
raster/JPEG (Pillow sur rasters/<F>.png) : la page source reste 100% vectorielle, l'overlay est du contenu
PDF natif (pymupdf.Shape), rien n'est rasterisé.

Usage : uv run releve/render_vectoriel.py WORKDIR NOM_PROJET SORTIE_DIR
Produit SORTIE_DIR/<NOM_PROJET>-Plans-annotes.pdf (+ SORTIE_DIR/vecteur/{estimate.json,bordereau.csv,
reserves.md,feuilles.json,plans.pdf} : données intermédiaires, utiles pour audit/débogage).
Étape suivante : releve/render_pdf.py assemble Rapport-de-metre + Dossier-complet à partir de ce PDF.
"""
import json, os, sys
from pathlib import Path

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
from src.estimer.render.from_releve import build  # noqa: E402
from src.estimer.render import load_input, render  # noqa: E402


def main(work, name, out_dir):
    work, out_dir = Path(work), Path(out_dir)
    vec_dir = out_dir / "vecteur"
    res = build(work, vec_dir)
    print(f"{vec_dir}: {res['sheets']} feuilles, {res['reperes']} reperes")
    sheets = load_input(vec_dir)
    if not sheets:
        print("aucun repere compte (estimate.json vide) : rien a rendre", file=sys.stderr)
        return 1
    p_plans = out_dir / f"{name}-Plans-annotes.pdf"
    rep = render(sheets, vec_dir / "plans.pdf", p_plans)
    print(f"{p_plans}: {rep['pages']} pages, {len(rep['sheets'])} feuilles")
    chevauche = []
    for s in rep["sheets"]:
        marque = "" if s["box_in_free_space"] else " (encadre chevauche le dessin)"
        if not s["box_in_free_space"]:
            chevauche.append(s["sheet"])
        print(f"  {s['sheet']}: {s['reperes']} reperes / {s['familles']} familles / RES {s['res']}{marque}")
    # Contrôle de conformité versionné (pas seulement informatif au journal) : le rapport persiste sur disque
    # pour que STATUT.md, un futur jeu_reference_visuel.py ou une relecture humaine puisse le relire sans
    # rejouer le rendu. N'échoue pas le pipeline sur un chevauchement (une feuille très dense peut n'avoir
    # aucun espace libre) mais le signale de façon non manquable : c'est à l'auto-supervision (CLAUDE.md) de
    # juger si c'est acceptable.
    rep["reperes"] = res["reperes"]
    rep["conformite"] = {"encadre_hors_espace_libre": chevauche,
                         "cible_visuelle": "apprentissage/hr26-14-exemplaire/SOURCE.txt"}
    (out_dir / f"{name}-rendu-rapport.json").write_text(json.dumps(rep, ensure_ascii=False, indent=1), encoding="utf-8")
    if chevauche:
        print(f"ATTENTION conformité : encadré hors espace libre sur {', '.join(chevauche)} — vérifier visuellement "
              f"avant de livrer (voir {name}-rendu-rapport.json)", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main(*sys.argv[1:4]))
