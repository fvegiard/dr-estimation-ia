"""Sélection explicite des feuilles actives, sans inférer la portée d'un addenda."""
from __future__ import annotations

import json
from pathlib import Path

PROFILS = Path(__file__).with_name("profils_revisions")


def selection(inventaire: dict[str, dict]) -> dict | None:
    """Un profil vérifié s'applique à l'ensemble exact des PDF, quelles que soient leurs dénominations."""
    for p in sorted(PROFILS.glob("*-feuilles.json")):
        profil = json.loads(p.read_text(encoding="utf-8"))
        regles = profil["documents"]
        par_hash = {e["sha256"]: (nom, e) for nom, e in inventaire.items()}
        if not (set(regles) & set(par_hash)):
            continue
        if (set(regles) != set(par_hash) or len(par_hash) != len(inventaire) or
                any(e["classement"] not in {"plans", "addenda"} for _, e in par_hash.values())):
            raise ValueError(f"{profil['dossier']} : les PDF ne correspondent pas au jeu de révisions vérifié")
        actives, ecartees, feuilles = {}, {}, set()
        for h, regle in regles.items():
            nom, e = par_hash[h]
            actives[nom], ecartees[nom] = regle["actives"], regle["remplacees"]
            if (set(actives[nom]) & set(ecartees[nom]) or set(actives[nom]) | set(ecartees[nom]) !=
                    {str(n) for n in range(1, e["pages"] + 1)} or feuilles.intersection(actives[nom].values()) or
                    len(set(actives[nom].values())) != len(actives[nom])):
                raise ValueError(f"{profil['dossier']} : couverture ou doublon dans le profil ({nom})")
            feuilles.update(actives[nom].values())
        return {"dossier": profil["dossier"], "preuve": profil["preuve"], "actives": actives, "remplacees": ecartees}
    return None