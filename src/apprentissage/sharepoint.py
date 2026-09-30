"""Lecture anonyme du dossier « Mes projets » (OneDrive de Daniel Dupuis) par son lien public.

Le lien « toute personne disposant du lien » suffit : une première requête GET donne un jeton FedAuth
d'invité, puis l'API REST SharePoint liste et télécharge les fichiers. Aucun compte, aucune synchro OneDrive :
marche aussi bien sur ce PC que dans Copilot cloud ou l'action GitHub.

On ne rapatrie que ce qui sert à l'apprentissage : chaque .qpl et les pages PNG posées à côté
(le reste — PDF reçus, addendas, Excel — n'est pas téléchargé).

    python -m src.apprentissage.sharepoint --annees 2026 2025 --sortie "G:\\My Drive\\Plan expert\\Mes projets Dupuis"
    python -m src.apprentissage.sharepoint --annees 2026 --sauf "Z:\\Soumission\\mes projets"   # seulement les nouveaux
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import requests

LIEN = ("https://drelectrique-my.sharepoint.com/:f:/g/personal/ddupuis_dreelectrique_com/"
        "IgBqqIkcjPYNQahlhlIbaYy-AdBj4ikAtBgabqkbixpch3I?e=M83mbn")
SITE = "https://drelectrique-my.sharepoint.com/personal/ddupuis_dreelectrique_com"
RACINE = "/personal/ddupuis_dreelectrique_com/Documents/Documents/Plan Expert/Mes projets"
JSON = {"Accept": "application/json;odata=nometadata"}


def annee(nom: str) -> str | None:
    m = re.search(r"\((?:\d{1,2}-)?[^)]*?(20\d\d)\)", nom) or re.search(r"(20\d\d)", nom)
    return m.group(1) if m else None


class MesProjets:
    def __init__(self, lien: str = LIEN, site: str = SITE, racine: str = RACINE):
        self.site, self.racine = site, racine
        self.s = requests.Session()
        r = self.s.get(lien, timeout=60)
        r.raise_for_status()
        if "FedAuth" not in self.s.cookies:
            raise RuntimeError("le lien public n'a pas donné de jeton d'invité (lien expiré ou restreint ?)")

    def _api(self, quoi: str, chemin: str, **kw):
        url = f"{self.site}/_api/web/{quoi}(decodedurl=@a)"
        return self.s.get(url + kw.pop("suite", ""), params={"@a": "'" + chemin.replace("'", "''") + "'"},
                          timeout=kw.pop("timeout", 120), **kw)

    def dossiers(self, chemin: str) -> list[dict]:
        r = self._api("GetFolderByServerRelativePath", chemin, suite="/Folders", headers=JSON)
        r.raise_for_status()
        return [d for d in r.json()["value"] if d["Name"] != "Forms"]

    def fichiers(self, chemin: str) -> list[dict]:
        r = self._api("GetFolderByServerRelativePath", chemin, suite="/Files", headers=JSON)
        r.raise_for_status()
        return r.json()["value"]

    def projets(self) -> list[str]:
        return sorted(d["Name"] for d in self.dossiers(self.racine))

    def dossiers_qpl(self, projet: str):
        """(chemin relatif du sous-dossier, [.qpl], [.png]) pour chaque sous-dossier qui contient un .qpl."""
        pile = [""]
        while pile:
            rel = pile.pop()
            abs_ = f"{self.racine}/{projet}" + (f"/{rel}" if rel else "")
            fs = self.fichiers(abs_)
            qpl = [f for f in fs if f["Name"].lower().endswith(".qpl")]
            if qpl:
                png = [f for f in fs if f["Name"].lower().endswith(".png")]
                yield rel, qpl, png
            pile += [f"{rel}/{d['Name']}".lstrip("/") for d in self.dossiers(abs_)]

    def telecharger(self, chemin_abs: str, dest: Path, taille: int) -> bool:
        if dest.is_file() and dest.stat().st_size == taille:
            return False
        dest.parent.mkdir(parents=True, exist_ok=True)
        r = self._api("GetFileByServerRelativePath", chemin_abs, suite="/$value", stream=True, timeout=600)
        r.raise_for_status()
        tmp = dest.with_name(dest.name + ".part")
        with open(tmp, "wb") as fh:
            for bloc in r.iter_content(1 << 20):
                fh.write(bloc)
        tmp.replace(dest)
        return True


def miroir_qpl(cache: Path, fils: int = 8, journal=print, mp: MesProjets | None = None) -> dict[Path, tuple[str, int]]:
    """Copie seulement les .qpl (petits) dans `cache` et renvoie {chemin local attendu du PNG : (chemin distant, taille)}.

    Les PNG des pages (≈ 60 Go au total) restent en ligne : `lien_humain` ne télécharge que les pages dont il
    découpe un exemple, dans un dossier temporaire effacé aussitôt. Rien n'est synchronisé sur le PC.
    """
    mp = mp or MesProjets()
    projets = [p for p in mp.projets() if not p.startswith("_")]
    journal(f"OneDrive « Mes projets » : {len(projets)} dossiers, inventaire des .qpl…")
    distants: dict[Path, tuple[str, int]] = {}

    def un(projet):
        loc, travaux = {}, []
        try:
            for rel, qpls, pngs in mp.dossiers_qpl(projet):
                base = f"{mp.racine}/{projet}/" + (f"{rel}/" if rel else "")
                dossier = cache / projet / rel
                for f in qpls:
                    travaux.append((base + f["Name"], dossier / f["Name"], int(f["Length"])))
                for f in pngs:
                    loc[dossier / f["Name"]] = (base + f["Name"], int(f["Length"]))
            for t in travaux:
                mp.telecharger(*t)
        except requests.RequestException as e:
            journal(f"  {projet} : illisible ({e})")
        return loc

    with ThreadPoolExecutor(fils) as ex:
        for i, loc in enumerate(ex.map(un, projets), 1):
            distants.update(loc)
            if i % 50 == 0:
                journal(f"  {i}/{len(projets)} projets inventoriés")
    return distants


def importer(sortie: Path, annees: list[str], sauf: Path | None = None, fils: int = 8, journal=print) -> dict:
    mp = MesProjets()
    deja = {p.name for p in sauf.iterdir() if p.is_dir()} if sauf and sauf.is_dir() else set()
    tous = mp.projets()
    choisis = [p for a in annees for p in tous if annee(p) == a and p not in deja]
    journal(f"{len(tous)} projets en ligne ; {len(choisis)} à rapatrier (années {', '.join(annees)}"
            + (f", hors {len(deja)} déjà présents sous {sauf}" if deja else "") + ")")
    bilan = {"projets": [], "fichiers": 0, "octets": 0}
    with ThreadPoolExecutor(fils) as ex:
        for i, projet in enumerate(choisis, 1):
            travaux = []
            for rel, qpls, pngs in mp.dossiers_qpl(projet):
                for f in qpls + pngs:
                    src = f"{mp.racine}/{projet}/" + (f"{rel}/" if rel else "") + f["Name"]
                    travaux.append((src, sortie / projet / rel / f["Name"], int(f["Length"])))
            if not travaux:
                journal(f"  [{i}/{len(choisis)}] {projet} : aucun .qpl")
                continue
            neufs = sum(ex.map(lambda t: mp.telecharger(*t), travaux))
            octets = sum(t[2] for t in travaux)
            bilan["projets"].append({"projet": projet, "fichiers": len(travaux), "octets": octets})
            bilan["fichiers"] += len(travaux)
            bilan["octets"] += octets
            journal(f"  [{i}/{len(choisis)}] {projet} : {len(travaux)} fichiers ({neufs} nouveaux), "
                    f"{octets / 1e6:.0f} Mo")
    sortie.mkdir(parents=True, exist_ok=True)
    (sortie / "_import-mes-projets.json").write_text(json.dumps(bilan, ensure_ascii=False, indent=1), "utf-8")
    return bilan


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--sortie", type=Path, required=True)
    ap.add_argument("--annees", nargs="+", default=["2026", "2025"])
    ap.add_argument("--sauf", type=Path, help="ignorer les projets déjà présents dans ce dossier (ex. Z:)")
    ap.add_argument("--fils", type=int, default=8)
    a = ap.parse_args(argv)
    b = importer(a.sortie, a.annees, a.sauf, a.fils, journal=lambda s: print(s, flush=True))
    print(f"fini : {len(b['projets'])} projets, {b['fichiers']} fichiers, {b['octets'] / 1e9:.2f} Go")
    return 0


if __name__ == "__main__":
    sys.exit(main())
