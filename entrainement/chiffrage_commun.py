#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# pyright: strict
"""Moteur de chiffrage commun « méthode Dupuis » — déterministe, stdlib seulement.

Le modèle ne chiffre jamais : il relève (`quantites.json`) et tranche (`decisions.json`). Ce moteur transforme
ces deux fichiers, plus `parametres.json` (taux, facteur, arrondis) et le catalogue Dupuis, en `chiffrage.json`
au schéma du banc (`taux`, `materiel`, `heures_relevees`, `heures_chargees`, `main_doeuvre`, `total_acceo`,
`facteur`, `prix_vente`, `lignes`, `par_article`, `lots`). Même entrée → même sortie, à l'octet près.

Usage :
    chiffrage_commun.py <dossier_run> [--kit <dossier_kit>] [--sortie <chiffrage.json>]
    <dossier_run> contient quantites.json et decisions.json ; le kit contient parametres.json et
    catalogue-prix-temps-dupuis.csv (par défaut : le kit du dossier, entrainement/<S>/kit).

Schéma de quantites.json :
    {"dossier": "S-1902", "lignes": [LIGNE, …]}
    LIGNE = {"code", "desc", "q", "u", "art", "src",
             "prix": PRIX,                              # obligatoire sauf si `variantes` couvre toutes les options
             "decision": {"cle": "…", "actif_si": ["…"]},   # facultatif : la ligne ne compte que si decisions[cle] ∈ actif_si
             "variantes": {"cle": "…", "options": {valeur: {"prix": PRIX, "q": nombre}}},  # facultatif : surcharge par décision
             "lot": true,                               # facultatif : la ligne est un prix de lot fournisseur
             "famille", "portee", "feuille"}            # facultatifs, pour le comparateur
    PRIX = {"type": "fixe", "p": $, "h": heures}
         | {"type": "catalogue", "entrees": [{"desc": "PRISE DUPLEX 15A 120V", "mult": 1}, …],
            "supplement_p": $, "supplement_h": heures}  # p/h = Σ mult × (PRIX À UTILISER / TEMPS À UTILISER) + suppléments

Schéma de decisions.json : {cle: valeur, …} — les clés connues sont dans DECISIONS_CONNUES ; toute clé
référencée par une ligne doit être présente.
"""
from __future__ import annotations

import argparse
import csv
import json
import math
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Final, cast

PI_PAR_M: Final[float] = 3.28084

DECISIONS_CONNUES: Final[dict[str, tuple[str, ...]]] = {
    'postes_composites': ('en_plus', 'couverts'),
    'monuments': ('lumen', 'dupuis'),
    'lot_eclairage': ('detail_13034_80', 'readme_11893'),
    'eae_hors_plan': ('comptes', 'releve', 'sautes'),   # Détail (hors plan) | quantités ENLEVER/RELOCALISER du relevé | ni l'un ni l'autre
    'conduits': ('temps_pi', 'acceo_tempsec'),
}

CLES_CHIFFRAGE: Final[tuple[str, ...]] = (
    'taux', 'materiel', 'heures_relevees', 'heures_chargees', 'main_doeuvre', 'total_acceo', 'facteur',
    'prix_vente', 'lignes', 'par_article', 'lots',
)


class ErreurChiffrage(ValueError):
    """Entrée invalide : la ligne et la raison sont dans le message."""


@dataclass(frozen=True)
class EntreeCatalogue:
    desc: str
    um: str
    prix: float          # colonne « PRIX À UTILISER » (dernière valeur de Dupuis)
    temps: float         # colonne « TEMPS À UTILISER »
    date_dernier: str


@dataclass(frozen=True)
class Parametres:
    taux: float
    facteur: float
    arrondi_heures: int = 10
    arrondi_prix: int = 1000

    @staticmethod
    def depuis(d: dict[str, Any]) -> Parametres:
        try:
            return Parametres(taux=float(d['taux']), facteur=float(d['facteur']),
                              arrondi_heures=int(d.get('arrondi_heures', 10)), arrondi_prix=int(d.get('arrondi_prix', 1000)))
        except (KeyError, TypeError, ValueError) as e:
            raise ErreurChiffrage(f"parametres.json : taux et facteur numériques obligatoires ({e})") from e


@dataclass(frozen=True)
class LigneChiffree:
    code: str
    desc: str
    q: float
    u: str
    p: float
    h: float
    art: str
    src: str
    lot: bool

    def en_dict(self) -> dict[str, Any]:
        return {'code': self.code, 'desc': self.desc, 'q': self.q, 'u': self.u, 'p': self.p, 'h': self.h,
                'art': self.art, 'src': self.src}


def _nombre(v: Any, ou: str) -> float:
    if isinstance(v, bool) or not isinstance(v, (int, float)):
        raise ErreurChiffrage(f"{ou} : nombre attendu, reçu {v!r}")
    return float(v)


def cle_catalogue(desc: str) -> str:
    """Clé de recherche d'une description : espaces normalisés, majuscules, sans BOM."""
    return ' '.join(desc.replace('﻿', '').split()).upper()


def charger_catalogue(chemin: Path) -> dict[str, EntreeCatalogue]:
    """Lit catalogue-prix-temps-dupuis.csv (séparateur ;). Seules les colonnes « À UTILISER » servent au chiffrage."""
    with chemin.open(encoding='utf-8-sig', newline='') as f:
        lecteur = csv.DictReader(f, delimiter=';')
        cat: dict[str, EntreeCatalogue] = {}
        for ligne in lecteur:
            desc = (ligne.get('description') or '').strip()
            if not desc:
                continue
            try:
                entree = EntreeCatalogue(desc=desc, um=(ligne.get('um') or '').strip(),
                                         prix=float(ligne['prix_a_utiliser']), temps=float(ligne['temps_a_utiliser']),
                                         date_dernier=(ligne.get('date_dernier') or '').strip())
            except (KeyError, ValueError) as e:
                raise ErreurChiffrage(f"catalogue : ligne « {desc} » illisible ({e})") from e
            cat.setdefault(cle_catalogue(desc), entree)
    if not cat:
        raise ErreurChiffrage(f"catalogue vide : {chemin}")
    return cat


def resoudre_prix(spec: dict[str, Any], catalogue: dict[str, EntreeCatalogue], ou: str) -> tuple[float, float]:
    """(p, h) d'une spécification de prix. `fixe` recopie ; `catalogue` somme mult × (prix, temps) « À UTILISER »."""
    genre = spec.get('type')
    if genre == 'fixe':
        return _nombre(spec.get('p'), f"{ou} prix.p"), _nombre(spec.get('h'), f"{ou} prix.h")
    if genre == 'catalogue':
        entrees = spec.get('entrees')
        if not isinstance(entrees, list) or not entrees:
            raise ErreurChiffrage(f"{ou} : prix.entrees doit être une liste non vide")
        p = _nombre(spec.get('supplement_p', 0.0), f"{ou} supplement_p")
        h = _nombre(spec.get('supplement_h', 0.0), f"{ou} supplement_h")
        for e_brut in cast(list[Any], entrees):
            if not isinstance(e_brut, dict):
                raise ErreurChiffrage(f"{ou} : entrée de catalogue mal formée {e_brut!r}")
            e = cast(dict[str, Any], e_brut)
            desc = e.get('desc')
            if not isinstance(desc, str):
                raise ErreurChiffrage(f"{ou} : entrée sans desc")
            entree = catalogue.get(cle_catalogue(desc))
            if entree is None:
                raise ErreurChiffrage(f"{ou} : « {desc} » absent du catalogue Dupuis")
            mult = _nombre(e.get('mult', 1), f"{ou} mult de « {desc} »")
            p += mult * entree.prix
            h += mult * entree.temps
        return p, h
    raise ErreurChiffrage(f"{ou} : prix.type doit être « fixe » ou « catalogue », reçu {genre!r}")


def _valeur_decision(cle: Any, decisions: dict[str, Any], ou: str) -> str:
    if not isinstance(cle, str):
        raise ErreurChiffrage(f"{ou} : decision.cle doit être une chaîne")
    if cle not in decisions:
        raise ErreurChiffrage(f"{ou} : la décision « {cle} » n'est pas dans decisions.json")
    v = decisions[cle]
    if not isinstance(v, str):
        raise ErreurChiffrage(f"{ou} : decisions[{cle}] doit être une chaîne, reçu {v!r}")
    return v


def ligne_active(ligne: dict[str, Any], decisions: dict[str, Any], ou: str) -> bool:
    dec_brut = ligne.get('decision')
    if dec_brut is None:
        return True
    if not isinstance(dec_brut, dict):
        raise ErreurChiffrage(f"{ou} : decision doit être un objet {{cle, actif_si}}")
    dec = cast(dict[str, Any], dec_brut)
    valeur = _valeur_decision(dec.get('cle'), decisions, ou)
    actif_si_brut = dec.get('actif_si')
    if not isinstance(actif_si_brut, list):
        raise ErreurChiffrage(f"{ou} : decision.actif_si doit être une liste de chaînes")
    actif_si = cast(list[Any], actif_si_brut)
    if not all(isinstance(x, str) for x in actif_si):
        raise ErreurChiffrage(f"{ou} : decision.actif_si doit être une liste de chaînes")
    return valeur in actif_si


def _appliquer_variantes(ligne: dict[str, Any], decisions: dict[str, Any], ou: str) -> tuple[dict[str, Any] | None, float | None]:
    """Retourne (prix surchargé, q surchargé) selon la valeur de la décision de `variantes`, sinon (None, None)."""
    var_brut = ligne.get('variantes')
    if var_brut is None:
        return None, None
    if not isinstance(var_brut, dict):
        raise ErreurChiffrage(f"{ou} : variantes doit être un objet {{cle, options}}")
    var = cast(dict[str, Any], var_brut)
    valeur = _valeur_decision(var.get('cle'), decisions, ou)
    options_brut = var.get('options')
    if not isinstance(options_brut, dict):
        raise ErreurChiffrage(f"{ou} : variantes.options doit être un objet")
    options = cast(dict[str, Any], options_brut)
    if valeur not in options:
        raise ErreurChiffrage(f"{ou} : aucune variante pour « {var.get('cle')} = {valeur} » (options : {sorted(options)})")
    opt_brut = options.get(valeur)
    if not isinstance(opt_brut, dict):
        raise ErreurChiffrage(f"{ou} : variante « {valeur} » mal formée")
    opt = cast(dict[str, Any], opt_brut)
    prix_brut = opt.get('prix')
    if prix_brut is not None and not isinstance(prix_brut, dict):
        raise ErreurChiffrage(f"{ou} : variante « {valeur} » : prix doit être un objet")
    prix = None if prix_brut is None else cast(dict[str, Any], prix_brut)
    q = opt.get('q')
    return prix, (None if q is None else _nombre(q, f"{ou} variante q"))


def chiffrer_lignes(quantites: dict[str, Any], decisions: dict[str, Any], catalogue: dict[str, EntreeCatalogue]) -> list[LigneChiffree]:
    """Lignes actives, prix et temps résolus, dans l'ordre du fichier (l'ordre fixe les arrondis)."""
    lignes = quantites.get('lignes')
    if not isinstance(lignes, list) or not lignes:
        raise ErreurChiffrage("quantites.json : « lignes » doit être une liste non vide")
    for cle, valeur in decisions.items():
        if cle == 'justifications':
            continue
        attendues = DECISIONS_CONNUES.get(cle)
        if attendues is not None and valeur not in attendues:
            raise ErreurChiffrage(f"decisions.json : « {cle} » = {valeur!r}, valeurs connues {attendues}")
    codes: set[str] = set()
    resultat: list[LigneChiffree] = []
    for i, brut in enumerate(cast(list[Any], lignes)):
        if not isinstance(brut, dict):
            raise ErreurChiffrage(f"ligne {i} : objet attendu")
        ligne = cast(dict[str, Any], brut)
        code = ligne.get('code')
        ou = f"ligne {i} ({code})"
        if not isinstance(code, str) or not code:
            raise ErreurChiffrage(f"ligne {i} : code manquant")
        if code in codes:
            raise ErreurChiffrage(f"{ou} : code en double")
        codes.add(code)
        if not ligne_active(ligne, decisions, ou):
            continue
        prix_var, q_var = _appliquer_variantes(ligne, decisions, ou)
        spec_brut = prix_var if prix_var is not None else ligne.get('prix')
        if not isinstance(spec_brut, dict):
            raise ErreurChiffrage(f"{ou} : prix manquant (ni prix, ni variante applicable)")
        spec = cast(dict[str, Any], spec_brut)
        p, h = resoudre_prix(spec, catalogue, ou)
        q = q_var if q_var is not None else _nombre(ligne.get('q'), f"{ou} q")
        if q < 0 or p < 0 or h < 0:
            raise ErreurChiffrage(f"{ou} : q, p et h doivent être ≥ 0")
        art = ligne.get('art')
        if not isinstance(art, str) or not art:
            raise ErreurChiffrage(f"{ou} : article du bordereau manquant")
        resultat.append(LigneChiffree(code=code, desc=str(ligne.get('desc', '')), q=q, u=str(ligne.get('u', 'u')), p=p, h=h,
                                      art=art, src=str(ligne.get('src', '')), lot=bool(ligne.get('lot', False))))
    return resultat


def totaux(lignes: list[LigneChiffree], params: Parametres) -> dict[str, Any]:
    """Sommaire ACCEO et prix de vente, mêmes formules et mêmes arrondis que la référence gelée."""
    mat = 0.0
    hrs = 0.0
    for x in lignes:
        mat += x.q * x.p
        hrs += x.q * x.h
    arr = params.arrondi_heures
    hrs_ch = math.ceil(hrs / arr) * arr if arr > 0 else hrs
    mo = hrs_ch * params.taux
    total_acceo = mat + mo
    echelle = mo / (hrs * params.taux) if hrs > 0 and params.taux > 0 else 1.0   # arrondi des heures réparti au prorata
    par_art: dict[str, list[float]] = {}
    for x in lignes:
        v = par_art.setdefault(x.art, [0.0, 0.0])
        v[0] += x.q * x.p
        v[1] += x.q * x.h
    total_arrondi = round(total_acceo, 2)
    ap = params.arrondi_prix
    prix_vente = round(total_arrondi * params.facteur / ap) * ap if ap > 0 else round(total_arrondi * params.facteur, 2)
    return {
        'taux': params.taux,
        'materiel': round(mat, 2),
        'heures_relevees': round(hrs, 3),
        'heures_chargees': hrs_ch,
        'main_doeuvre': round(mo, 2),
        'total_acceo': total_arrondi,
        'facteur': params.facteur,
        'prix_vente': prix_vente,
        'lignes': [x.en_dict() for x in lignes],
        'par_article': {a: {'materiel': round(v[0], 2), 'heures': round(v[1], 2),
                            'mo': round(v[1] * params.taux * echelle, 2),
                            'total': round(v[0] + v[1] * params.taux * echelle, 2)} for a, v in sorted(par_art.items())},
        'lots': {x.code: round(x.q * x.p, 2) for x in lignes if x.lot},
    }


def chiffrer(quantites: dict[str, Any], decisions: dict[str, Any], params: Parametres,
             catalogue: dict[str, EntreeCatalogue]) -> dict[str, Any]:
    """quantites + decisions + paramètres + catalogue → chiffrage.json (dict)."""
    lignes = chiffrer_lignes(quantites, decisions, catalogue)
    sortie = totaux(lignes, params)
    sortie['decisions'] = {k: v for k, v in decisions.items() if k != 'justifications'}
    sortie['dossier'] = quantites.get('dossier')
    return sortie


def lire_json(chemin: Path) -> dict[str, Any]:
    try:
        with chemin.open(encoding='utf-8') as f:
            d = json.load(f)
    except FileNotFoundError:
        raise ErreurChiffrage(f"fichier manquant : {chemin}") from None
    except json.JSONDecodeError as e:
        raise ErreurChiffrage(f"{chemin} : JSON invalide ({e})") from e
    if not isinstance(d, dict):
        raise ErreurChiffrage(f"{chemin} : objet JSON attendu")
    return cast(dict[str, Any], d)


def chiffrer_dossier(dossier_run: Path, kit: Path, catalogue_csv: Path | None = None) -> dict[str, Any]:
    quantites = lire_json(dossier_run / 'quantites.json')
    decisions = lire_json(dossier_run / 'decisions.json')
    params = Parametres.depuis(lire_json(kit / 'parametres.json'))
    catalogue = charger_catalogue(catalogue_csv or kit / 'catalogue-prix-temps-dupuis.csv')
    return chiffrer(quantites, decisions, params, catalogue)


def ecrire_json(d: dict[str, Any], chemin: Path) -> None:
    with chemin.open('w', encoding='utf-8') as f:
        json.dump(d, f, ensure_ascii=False, indent=1)
        f.write('\n')


def resume(c: dict[str, Any]) -> str:
    lignes = [f"Matériel (vendant Dupuis + lots) : {c['materiel']:,.2f} $",
              f"Heures relevées : {c['heures_relevees']:,.2f} h  → chargées : {c['heures_chargees']} h × {c['taux']} $ = {c['main_doeuvre']:,.2f} $",
              f"TOTAL ACCEO : {c['total_acceo']:,.2f} $  × {c['facteur']} → PRIX DE VENTE {c['prix_vente']:,.0f} $"]
    for a, v in c['par_article'].items():
        lignes.append(f"  {a}: mat {v['materiel']:9,.0f} $  h {v['heures']:7.1f}  total {v['total']:9,.0f} $")
    return '\n'.join(lignes).replace(',', ' ')


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Chiffrage déterministe « méthode Dupuis » à partir de quantites.json + decisions.json")
    ap.add_argument('dossier_run', type=Path, help='dossier contenant quantites.json et decisions.json')
    ap.add_argument('--kit', type=Path, default=None, help='dossier du kit (parametres.json, catalogue) ; défaut : kit du dossier S')
    ap.add_argument('--catalogue', type=Path, default=None, help='catalogue CSV (défaut : <kit>/catalogue-prix-temps-dupuis.csv)')
    ap.add_argument('--sortie', type=Path, default=None, help='fichier de sortie (défaut : <dossier_run>/chiffrage.json)')
    args = ap.parse_args(argv)
    dossier_run: Path = args.dossier_run
    kit: Path = args.kit if args.kit is not None else Path(__file__).resolve().parent / 'S-1902' / 'kit'
    try:
        c = chiffrer_dossier(dossier_run, kit, args.catalogue)
    except ErreurChiffrage as e:
        print(f"ERREUR : {e}", file=sys.stderr)
        return 2
    sortie: Path = args.sortie if args.sortie is not None else dossier_run / 'chiffrage.json'
    ecrire_json(c, sortie)
    print(resume(c))
    print(f"→ {sortie}")
    return 0


if __name__ == '__main__':
    sys.exit(main())
