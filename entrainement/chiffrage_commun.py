#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# pyright: strict
"""Moteur de chiffrage commun « méthode Dupuis » — déterministe, stdlib seulement.

Le modèle ne chiffre jamais : il relève (`quantites.json`) et tranche (`decisions.json`). Ce moteur transforme
ces deux fichiers, plus `parametres.json` (taux, facteur, arrondis) et le catalogue Dupuis, en `chiffrage.json`
au schéma du banc (`taux`, `materiel`, `heures_relevees`, `heures_chargees`, `main_doeuvre`, `total_acceo`,
`facteur`, `prix_vente`, `lignes`, `par_article`, `lots`, plus `decisions` et `dossier`). Même entrée → même sortie.

Usage :
    python3 chiffrage_commun.py <dossier_run> [--kit <dossier_kit>] [--sortie <chiffrage.json>]
    <dossier_run> contient quantites.json et decisions.json ; le kit contient parametres.json et
    catalogue-prix-temps-dupuis.csv (par défaut : entrainement/<dossier>/kit, <dossier> étant le champ `dossier` de
    quantites.json ; hors du dépôt, passer --kit, par exemple `--kit .` dans un dossier de run préparé).
    Code de sortie 0 si chiffrage.json est écrit, 2 si une entrée manque ou est invalide (message « ERREUR : … »).

Schéma de quantites.json :
    {"dossier": "S-1902", "lignes": [LIGNE, …]}
    LIGNE = {"code", "desc", "q", "u", "art", "src",            # q obligatoire même si une variante le surcharge
             "prix": PRIX,                                      # obligatoire sauf si `variantes` couvre toutes les options ;
                                                                # si l'option retenue n'est pas dans `variantes.options`, la ligne garde `prix` et `q`
             "decision": {"cle": "…", "actif_si": ["…"]},       # facultatif : la ligne ne compte que si decisions[cle] ∈ actif_si
             "variantes": {"cle": "…", "options": {valeur: {"prix": PRIX, "q": nombre}}},  # facultatif : surcharge par décision
             "lot": true,                                       # facultatif (booléen) : la ligne est un prix de lot fournisseur
             "famille", "portee", "feuille"}                    # facultatifs, pour le comparateur
    PRIX = {"type": "fixe", "p": $, "h": heures}
         | {"type": "catalogue", "entrees": [{"desc": "PRISE DUPLEX 15A 120V", "mult": 1, "um": "U"}, …],
            "supplement_p": $, "supplement_h": heures}          # p/h = Σ mult × (PRIX À UTILISER / TEMPS À UTILISER) + suppléments
    `um` n'est exigé que si le catalogue a la même description sous deux unités (ex. « COND FLEX 1PO ALUM BOB » en P et en M).
    Quand une ligne a `prix` ET une variante avec `prix`, la variante gagne ; `decision` et `variantes` se combinent
    (la ligne doit d'abord être active).

Schéma de decisions.json : {cle: valeur, …} + "justifications" facultatif. Les clés et les valeurs permises sont
DECISIONS_CONNUES ; toute autre clé, valeur, `actif_si` ou option de variante est refusée (une faute de frappe ne
doit jamais faire disparaître une ligne en silence).

Arrondis : heures chargées = heures relevées (arrondies à 3 décimales) plafonnées au multiple de `arrondi_heures` ;
prix de vente = total ACCEO × facteur arrondi au multiple de `arrondi_prix` avec `round()` de Python (demi-pair),
comme la référence gelée. Les cents aussi (`round(x, 2)`).
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
CLES_DECISIONS_LIBRES: Final[frozenset[str]] = frozenset({'justifications'})

CLES_CHIFFRAGE: Final[tuple[str, ...]] = (
    'taux', 'materiel', 'heures_relevees', 'heures_chargees', 'main_doeuvre', 'total_acceo', 'facteur',
    'prix_vente', 'lignes', 'par_article', 'lots', 'decisions', 'dossier',
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


Catalogue = dict[str, dict[str, EntreeCatalogue]]   # clé normalisée → {um → entrée}


def _nombre(v: Any, ou: str) -> float:
    if isinstance(v, bool) or not isinstance(v, (int, float)):
        raise ErreurChiffrage(f"{ou} : nombre attendu, reçu {v!r}")
    f = float(v)
    if not math.isfinite(f):
        raise ErreurChiffrage(f"{ou} : nombre fini attendu, reçu {v!r}")
    return f


def _entier_positif(v: Any, ou: str) -> int:
    if isinstance(v, bool) or not isinstance(v, int) or v < 0:
        raise ErreurChiffrage(f"{ou} : entier ≥ 0 attendu, reçu {v!r}")
    return v


def _chaine(v: Any, ou: str, defaut: str | None = None) -> str:
    if v is None and defaut is not None:
        return defaut
    if not isinstance(v, str):
        raise ErreurChiffrage(f"{ou} : chaîne attendue, reçu {v!r}")
    return v


@dataclass(frozen=True)
class Parametres:
    taux: float
    facteur: float
    arrondi_heures: int = 10
    arrondi_prix: int = 1000

    @staticmethod
    def depuis(d: dict[str, Any]) -> Parametres:
        if 'taux' not in d or 'facteur' not in d:
            raise ErreurChiffrage("parametres.json : taux et facteur obligatoires")
        taux = _nombre(d['taux'], 'parametres.json taux')
        facteur = _nombre(d['facteur'], 'parametres.json facteur')
        if taux <= 0 or facteur <= 0:
            raise ErreurChiffrage("parametres.json : taux et facteur doivent être > 0")
        return Parametres(taux=taux, facteur=facteur,
                          arrondi_heures=_entier_positif(d.get('arrondi_heures', 10), 'parametres.json arrondi_heures'),
                          arrondi_prix=_entier_positif(d.get('arrondi_prix', 1000), 'parametres.json arrondi_prix'))


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


def cle_catalogue(desc: str) -> str:
    """Clé de recherche d'une description : espaces normalisés, majuscules, sans BOM."""
    return ' '.join(desc.replace('﻿', '').split()).upper()


def charger_catalogue(chemin: Path, journal: list[str] | None = None) -> Catalogue:
    """Lit catalogue-prix-temps-dupuis.csv (séparateur ;). Seules les colonnes « À UTILISER » servent au chiffrage.
    Deux lignes qui se confondent après normalisation : même unité → la plus récente (`date_dernier`) gagne, règle
    « dernière valeur de Dupuis » ; unités différentes → les deux sont gardées et l'entrée de quantites.json doit dire `um`.
    Chaque fusion est consignée dans `journal` quand il est fourni."""
    with chemin.open(encoding='utf-8-sig', newline='') as f:
        lecteur = csv.DictReader(f, delimiter=';')
        cat: Catalogue = {}
        for ligne in lecteur:
            desc = (ligne.get('description') or '').strip()
            if not desc:
                continue
            try:
                entree = EntreeCatalogue(desc=desc, um=(ligne.get('um') or '').strip().upper(),
                                         prix=float(ligne['prix_a_utiliser']), temps=float(ligne['temps_a_utiliser']),
                                         date_dernier=(ligne.get('date_dernier') or '').strip())
            except (KeyError, ValueError) as e:
                raise ErreurChiffrage(f"catalogue : ligne « {desc} » illisible ({e})") from e
            par_um = cat.setdefault(cle_catalogue(desc), {})
            deja = par_um.get(entree.um)
            if deja is None:
                par_um[entree.um] = entree
            elif entree.date_dernier > deja.date_dernier:
                if journal is not None:
                    journal.append(f"catalogue : « {desc} » ({entree.um}) en double, {entree.date_dernier} remplace {deja.date_dernier}")
                par_um[entree.um] = entree
            elif journal is not None:
                journal.append(f"catalogue : « {desc} » ({entree.um}) en double, {deja.date_dernier} conservé ({entree.date_dernier} ignoré)")
    if not cat:
        raise ErreurChiffrage(f"catalogue vide : {chemin}")
    return cat


def entree_catalogue(catalogue: Catalogue, desc: str, um: str | None, ou: str) -> EntreeCatalogue:
    par_um = catalogue.get(cle_catalogue(desc))
    if not par_um:
        raise ErreurChiffrage(f"{ou} : « {desc} » absent du catalogue Dupuis")
    if um is not None:
        e = par_um.get(um.strip().upper())
        if e is None:
            raise ErreurChiffrage(f"{ou} : « {desc} » n'existe pas en unité {um!r} (unités : {sorted(par_um)})")
        return e
    if len(par_um) > 1:
        raise ErreurChiffrage(f"{ou} : « {desc} » existe sous plusieurs unités {sorted(par_um)} : précise « um » dans l'entrée")
    return next(iter(par_um.values()))


def resoudre_prix(spec: dict[str, Any], catalogue: Catalogue, ou: str) -> tuple[float, float]:
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
            um_brut = e.get('um')
            if um_brut is not None and not isinstance(um_brut, str):
                raise ErreurChiffrage(f"{ou} : um de « {desc} » doit être une chaîne")
            entree = entree_catalogue(catalogue, desc, um_brut, ou)
            mult = _nombre(e.get('mult', 1), f"{ou} mult de « {desc} »")
            p += mult * entree.prix
            h += mult * entree.temps
        return p, h
    raise ErreurChiffrage(f"{ou} : prix.type doit être « fixe » ou « catalogue », reçu {genre!r}")


def valider_decisions(decisions: dict[str, Any]) -> None:
    """decisions.json : clés et valeurs dans DECISIONS_CONNUES (plus `justifications`)."""
    for cle, valeur in decisions.items():
        if cle in CLES_DECISIONS_LIBRES:
            continue
        attendues = DECISIONS_CONNUES.get(cle)
        if attendues is None:
            raise ErreurChiffrage(f"decisions.json : clé inconnue « {cle} » (connues : {sorted(DECISIONS_CONNUES)})")
        if valeur not in attendues:
            raise ErreurChiffrage(f"decisions.json : « {cle} » = {valeur!r}, valeurs connues {attendues}")


def _cle_decision(cle: Any, ou: str) -> str:
    if not isinstance(cle, str) or cle not in DECISIONS_CONNUES:
        raise ErreurChiffrage(f"{ou} : décision inconnue {cle!r} (connues : {sorted(DECISIONS_CONNUES)})")
    return cle


def _valeur_decision(cle: str, decisions: dict[str, Any], ou: str) -> str:
    if cle not in decisions:
        raise ErreurChiffrage(f"{ou} : la décision « {cle} » n'est pas dans decisions.json")
    v = decisions[cle]
    if not isinstance(v, str) or v not in DECISIONS_CONNUES[cle]:
        raise ErreurChiffrage(f"{ou} : decisions[{cle}] = {v!r}, valeurs connues {DECISIONS_CONNUES[cle]}")
    return v


def ligne_active(ligne: dict[str, Any], decisions: dict[str, Any], ou: str) -> bool:
    dec_brut = ligne.get('decision')
    if dec_brut is None:
        return True
    if not isinstance(dec_brut, dict):
        raise ErreurChiffrage(f"{ou} : decision doit être un objet {{cle, actif_si}}")
    dec = cast(dict[str, Any], dec_brut)
    cle = _cle_decision(dec.get('cle'), ou)
    actif_si_brut = dec.get('actif_si')
    if not isinstance(actif_si_brut, list) or not actif_si_brut:
        raise ErreurChiffrage(f"{ou} : decision.actif_si doit être une liste non vide de valeurs de « {cle} »")
    actif_si = cast(list[Any], actif_si_brut)
    inconnues = [x for x in actif_si if not isinstance(x, str) or x not in DECISIONS_CONNUES[cle]]
    if inconnues:
        raise ErreurChiffrage(f"{ou} : decision.actif_si contient des valeurs inconnues pour « {cle} » : {inconnues} (connues : {DECISIONS_CONNUES[cle]})")
    return _valeur_decision(cle, decisions, ou) in actif_si


def _variantes(ligne: dict[str, Any], decisions: dict[str, Any], ou: str) -> tuple[dict[str, Any] | None, float | None]:
    """Valide `variantes` (toutes les options) et retourne (prix, q) de l'option retenue, sinon (None, None)."""
    var_brut = ligne.get('variantes')
    if var_brut is None:
        return None, None
    if not isinstance(var_brut, dict):
        raise ErreurChiffrage(f"{ou} : variantes doit être un objet {{cle, options}}")
    var = cast(dict[str, Any], var_brut)
    cle = _cle_decision(var.get('cle'), ou)
    options_brut = var.get('options')
    if not isinstance(options_brut, dict) or not options_brut:
        raise ErreurChiffrage(f"{ou} : variantes.options doit être un objet non vide")
    options = cast(dict[str, Any], options_brut)
    inconnues = [k for k in options if k not in DECISIONS_CONNUES[cle]]
    if inconnues:
        raise ErreurChiffrage(f"{ou} : variantes.options contient des valeurs inconnues pour « {cle} » : {inconnues} (connues : {DECISIONS_CONNUES[cle]})")
    for k, opt_brut in options.items():
        if not isinstance(opt_brut, dict):
            raise ErreurChiffrage(f"{ou} : variante « {k} » mal formée")
        opt = cast(dict[str, Any], opt_brut)
        if 'prix' in opt and not isinstance(opt['prix'], dict):
            raise ErreurChiffrage(f"{ou} : variante « {k} » : prix doit être un objet")
        if 'q' in opt:
            _nombre(opt['q'], f"{ou} variante « {k} » q")
    valeur = _valeur_decision(cle, decisions, ou)
    if valeur not in options:
        if isinstance(ligne.get('prix'), dict):
            return None, None                       # repli documenté : le prix et la quantité de la ligne
        raise ErreurChiffrage(f"{ou} : aucune variante pour « {cle} = {valeur} » et pas de prix de repli (options : {sorted(options)})")
    opt = cast(dict[str, Any], options[valeur])
    prix = cast(dict[str, Any], opt['prix']) if 'prix' in opt else None
    q = _nombre(opt['q'], f"{ou} variante q") if 'q' in opt else None
    return prix, q


def chiffrer_lignes(quantites: dict[str, Any], decisions: dict[str, Any], catalogue: Catalogue) -> list[LigneChiffree]:
    """Lignes actives, prix et temps résolus, dans l'ordre du fichier (l'ordre fixe les arrondis). Toute ligne est
    validée (code, q, étiquettes), active ou non : une étiquette fausse est une erreur, jamais une ligne qui disparaît."""
    lignes = quantites.get('lignes')
    if not isinstance(lignes, list) or not lignes:
        raise ErreurChiffrage("quantites.json : « lignes » doit être une liste non vide")
    valider_decisions(decisions)
    if decisions.get('conduits') == 'acceo_tempsec':
        raise ErreurChiffrage("decisions.json : conduits = acceo_tempsec n'est pas pris en charge : le catalogue n'a pas de colonne TEMPSEC "
                              "(temps par section de 10 pi) ; utiliser temps_pi")
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
        q_ligne = _nombre(ligne.get('q'), f"{ou} q")
        desc = _chaine(ligne.get('desc'), f"{ou} desc", '')
        u = _chaine(ligne.get('u'), f"{ou} u", 'u')
        src = _chaine(ligne.get('src'), f"{ou} src", '')
        lot_brut = ligne.get('lot', False)
        if not isinstance(lot_brut, bool):
            raise ErreurChiffrage(f"{ou} : lot doit être un booléen")
        art = ligne.get('art')
        if not isinstance(art, str) or not art:
            raise ErreurChiffrage(f"{ou} : article du bordereau manquant")
        actif = ligne_active(ligne, decisions, ou)
        prix_var, q_var = _variantes(ligne, decisions, ou)
        if not actif:
            continue
        spec_brut = prix_var if prix_var is not None else ligne.get('prix')
        if not isinstance(spec_brut, dict):
            raise ErreurChiffrage(f"{ou} : prix manquant (ni prix, ni variante applicable)")
        p, h = resoudre_prix(cast(dict[str, Any], spec_brut), catalogue, ou)
        q = q_var if q_var is not None else q_ligne
        if q < 0 or p < 0 or h < 0:
            raise ErreurChiffrage(f"{ou} : q, p et h doivent être ≥ 0")
        resultat.append(LigneChiffree(code=code, desc=desc, q=q, u=u, p=p, h=h, art=art, src=src, lot=lot_brut))
    return resultat


def heures_chargees(heures_relevees: float, arrondi: int) -> float:
    """Plafond au multiple de `arrondi`, décidé sur les heures arrondies à 3 décimales (jamais sur le bruit flottant :
    200 × 0,55 h = 110,000…01 doit donner 110, pas 120)."""
    hrs_r = round(heures_relevees, 3)
    if arrondi <= 0:
        return hrs_r
    return math.ceil(round(hrs_r / arrondi, 9)) * arrondi


def totaux(lignes: list[LigneChiffree], params: Parametres) -> dict[str, Any]:
    """Sommaire ACCEO et prix de vente, mêmes formules et mêmes arrondis que la référence gelée."""
    mat = 0.0
    hrs = 0.0
    for x in lignes:
        mat += x.q * x.p
        hrs += x.q * x.h
    hrs_ch = heures_chargees(hrs, params.arrondi_heures)
    mo = hrs_ch * params.taux
    total_acceo = mat + mo
    echelle = mo / (hrs * params.taux) if hrs > 0 else 1.0   # arrondi des heures réparti au prorata (comme la référence)
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


def chiffrer(quantites: dict[str, Any], decisions: dict[str, Any], params: Parametres, catalogue: Catalogue) -> dict[str, Any]:
    """quantites + decisions + paramètres + catalogue → chiffrage.json (dict, clés CLES_CHIFFRAGE)."""
    lignes = chiffrer_lignes(quantites, decisions, catalogue)
    sortie = totaux(lignes, params)
    sortie['decisions'] = {k: v for k, v in decisions.items() if k not in CLES_DECISIONS_LIBRES}
    sortie['dossier'] = quantites.get('dossier')
    manquantes = [k for k in CLES_CHIFFRAGE if k not in sortie]
    if manquantes:
        raise ErreurChiffrage(f"chiffrage incomplet : {manquantes}")
    return sortie


def _constante_interdite(s: str) -> Any:
    raise ErreurChiffrage(f"valeur JSON interdite : {s} (NaN et Infinity ne sont pas des quantités)")


def lire_json(chemin: Path) -> dict[str, Any]:
    try:
        with chemin.open(encoding='utf-8') as f:
            d = json.load(f, parse_constant=_constante_interdite)
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
    try:
        kit: Path | None = args.kit
        if kit is None:
            dossier = lire_json(dossier_run / 'quantites.json').get('dossier')
            if not isinstance(dossier, str) or not dossier:
                raise ErreurChiffrage("quantites.json : champ « dossier » manquant, impossible de déduire le kit ; passer --kit")
            kit = Path(__file__).resolve().parent / dossier / 'kit'
            if not (kit / 'parametres.json').exists():
                raise ErreurChiffrage(f"kit introuvable pour le dossier {dossier} ({kit}) ; passer --kit <dossier du kit>")
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
