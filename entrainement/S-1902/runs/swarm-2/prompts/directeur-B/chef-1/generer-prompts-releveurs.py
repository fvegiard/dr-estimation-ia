#!/usr/bin/env python3
"""Génère les 3 prompts des releveurs B1-1, B1-2, B1-3 (chef de lot B1, essaim 2, S-1902).

Les blocs communs (RÈGLES D'AVEUGLE, MÉCANIQUE DE RELAIS, kit, règles de prix, nomenclature, formats,
vérifications) sont COPIÉS MOT POUR MOT depuis prompts/directeur-B/chef-1.md (le prompt du chef de lot) ;
toutes les valeurs de catalogue citées dans les briefs sont LUES dans le CSV (aucune frappe à la main).
Ne lit que le dossier de travail /home/claude/entrainement/S-1902/swarm-2/.
"""
import csv
import re
import sys

RACINE = '/home/claude/entrainement/S-1902/swarm-2/'
CAT = RACINE + 'catalogue-prix-temps-dupuis.csv'
CHEF = RACINE + 'prompts/directeur-B/chef-1.md'
SORTIE = RACINE + 'prompts/directeur-B/chef-1/releveur-{m}.md'

rows = list(csv.DictReader(open(CAT, encoding='utf-8-sig'), delimiter=';'))
assert len(rows) == 2068, len(rows)


def ligne(desc, um='U'):
    t = [r for r in rows if r['description'] == desc and r['um'] == um]
    assert len(t) == 1, (desc, um, len(t))
    return t[0]


def cand(desc, um='U'):
    r = ligne(desc, um)
    return (f"« {r['description']} » um={r['um']} p={r['prix_a_utiliser']} h={r['temps_a_utiliser']} "
            f"nb_projets={r['nb_projets']} dernier {r['date_dernier']} ({r['projet_dernier']})")


# ----------------------------------------------------------------------------------------------
# Blocs communs copiés depuis le prompt du chef de lot
# ----------------------------------------------------------------------------------------------
chef_lignes = open(CHEF, encoding='utf-8').read().split('\n')


def trouve(prefixe, debut=0):
    for i in range(debut, len(chef_lignes)):
        if chef_lignes[i].startswith(prefixe):
            return i
    raise SystemExit('introuvable : ' + prefixe)


def bloc(prefixe_debut, prefixe_fin):
    i = trouve(prefixe_debut)
    j = trouve(prefixe_fin, i + 1)
    return '\n'.join(chef_lignes[i:j]).rstrip('\n')


# RÈGLES D'AVEUGLE : de « RÈGLES D'AVEUGLE (obligatoires… » à la ligne vide qui suit « (Un releveur ne délègue… »
i0 = trouve("RÈGLES D'AVEUGLE (obligatoires")
i1 = trouve('   (Un releveur ne délègue à personne', i0) + 1
REGLES = '\n'.join(chef_lignes[i0:i1])
assert REGLES.count('\n') == 12, REGLES.count('\n')

# MÉCANIQUE DE RELAIS : bloc entre les deux ``` du prompt du chef
i0 = trouve('MÉCANIQUE DE RELAIS (à recopier mot pour mot')
i1 = trouve('```', i0)
MECA = '\n'.join(chef_lignes[i0:i1])

KIT = bloc('## Le kit — comment lire chaque fichier', '## Règles de prix et de temps')
KIT = KIT.replace('## Le kit — comment lire chaque fichier (à transmettre tel quel à tes releveurs)',
                  '## Le kit — comment lire chaque fichier')
PRIX = bloc('## Règles de prix et de temps', '## Nomenclature des codes')
PRIX = PRIX.replace('## Règles de prix et de temps (à transmettre tel quel)', '## Règles de prix et de temps')
NOMEN = bloc('## Nomenclature des codes', '## Format de `src`, `u` et `art`')
FORMAT_SRC = bloc('## Format de `src`, `u` et `art`', '## Format JSON')
FORMAT_JSON = bloc('## Format JSON', '## Vérifications avant d')
VERIF = bloc('## Vérifications avant d', '## Ton lot B1')

# ----------------------------------------------------------------------------------------------
# Les 44 codes : arbitrage du chef de lot (valeurs relues dans le CSV par le générateur)
# ----------------------------------------------------------------------------------------------
PREC = 'portée absente du relevé — correspondance de précaution'

EP = 'ENLEVER PRISE'
RP = 'RELO PRISE'
CPE = 'CONTACT DE PORTE ENL'

SPEC = {}


def add(code, **kw):
    assert code not in SPEC, code
    SPEC[code] = kw


# ---- Prises --------------------------------------------------------------------------------
add('PC-I', desc='Prise double 15 A 120 V neuve', u='U', art='3.28', portee='INSTALLER 25',
    lib='« PRISE DE COURANT DOUBLE 15A- 120V » (famille PRISE DOUBLE 15A, légende E-001)',
    regle='Règle 1 : repère METHODE « prise duplex 15 A 64,81 $ / 1,175 h » (p ET h égalent le repère).',
    retenu=[('PRISE DUPLEX 15A 120V', 'U', 1)],
    ecartes=['PRISE DUPLEX 15/20A 120V', 'PRISE', 'PRISE 15A 125V', 'DROP DE PRISE'],
    notes=["R-007 : le relevé ne distingue pas les prises 15 A et 20 A ; le repère METHODE (15 A, 64,81 $) prévaut — "
           "à dire en note.",
           "Ne JAMAIS ajouter les prises/plaques Lumen LEV16252W / LEV16352W / LEV80401NW (feuille « Matériel Lumen ») : "
           "le prix d'assemblage Dupuis inclut déjà boîte, plaque et raccord."])
add('PC-E', desc='Prise double 15 A enlevée', u='U', art='3.22', portee='ENLEVER 7',
    lib='famille PRISE DOUBLE 15A, portée ENLEVER',
    regle='Règle 1 : repère METHODE « prise enlevée 0,35 h » → « ENLEVER PRISE » (h = 0,35, p = 0).',
    retenu=[(EP, 'U', 1)],
    ecartes=['PRISES A DEMANTELER'],
    notes=["« PRISES A DEMANTELER » est plus récent (2026-09-23) mais h = 0,2 : écarté par la règle 1 (repère 0,35 h). "
           "ENLEVER → p = 0 (temps seulement)."])
add('PC-R', desc='Prise double 15 A relocalisée', u='U', art='3.22', portee='RELOCALISER 8',
    lib='famille PRISE DOUBLE 15A, portée RELOCALISER',
    regle='Règle 1 : repère METHODE « relocalisation de prise 1,5 h » → « RELO PRISE » (p = 0, h = 1,5).',
    retenu=[(RP, 'U', 1)],
    ecartes=[],
    notes=["RELOCALISER → prix selon le catalogue (ici 0 $) + temps de relocalisation."])
add('PU-I', desc='Prise double 15 A USB neuve (Leviton Decora USB)', u='U', art='3.27', portee='INSTALLER 20',
    lib='« PRISE DE COURANT DOUBLE 15A- 120V TYPE Leviton Decora USB » (famille PRISE USB ; Q14 : code PU conservé)',
    regle='Règle 1 : repère METHODE « USB 77,45 $ / 1,125 h ».',
    retenu=[('PRISE USB 125V 15 AMP', 'U', 1)],
    ecartes=['PRISE DUPLEX 15A 120V'],
    notes=["Ne PAS utiliser le prix Lumen LEVT5633W (48,66 $) ni LEV80401NW : Dupuis a le libellé et le prix "
           "d'assemblage inclut boîte, plaque, raccord.",
           "« PRISE DUPLEX 15A 120V » est la prise ordinaire (PC-I), pas la USB : à noter comme écarté."])
add('PU-E', desc='Prise USB enlevée', u='U', art='3.22', portee='absente du relevé', precaution=True,
    lib='aucune (portée absente)',
    regle='Même libellé que PC-E (harmonisation obligatoire).',
    retenu=[(EP, 'U', 1)], ecartes=['PRISES A DEMANTELER'],
    analogue="une prise USB enlevée se démonte comme une prise ordinaire (repère METHODE prise enlevée 0,35 h)",
    notes=[])
add('PU-R', desc='Prise USB relocalisée', u='U', art='3.22', portee='absente du relevé', precaution=True,
    lib='aucune (portée absente)',
    regle='Même libellé que PC-R (harmonisation obligatoire).',
    retenu=[(RP, 'U', 1)], ecartes=[],
    analogue="une prise USB relocalisée se déplace comme une prise ordinaire (repère METHODE relocalisation de prise 1,5 h)",
    notes=[])
add('PG-I', desc='Prise double 15 A DDFT (GFI) neuve', u='U', art='3.30', portee='INSTALLER 22',
    lib='« PRISE DOUBLE DDFT (moitié pleine) » (famille PRISE DDFT, légende E-001)',
    regle='Règle 1 : repère METHODE « DDFT 65,38 $ / 1,3 h ».',
    retenu=[('PRISE DUPLEX 20A 125V GFI', 'U', 1)],
    ecartes=['PRISE DUPLEX 15A 120V GFI', 'PRISE GFI', 'PRISE GFI WP', 'RECEPT DDFT AUTO TEST 20 A125V INVIOL BLANC'],
    notes=["OBLIGATOIRE (reserves.md R-007) : la famille PRISE DDFT du relevé contient aussi les prises "
           "M.A.L.T. isolées (barre pleine ; bordereau 3.29 « Prises doubles 15A-120V MALT isolées »), non "
           "départagées au relevé. Cherche dans le catalogue (motifs MALT, ISOL, ORANGE, \\bIG\\b, DDFT, GFI, GFCI) un "
           "libellé distinct et DIS dans les notes ce que tu as cherché et trouvé. Le chef de lot n'a trouvé aucun "
           "libellé « prise M.A.L.T. isolée » (les libellés « TIGE MALT », « BARRE … ISOL », « ISOLATEUR », "
           "« BOITE TIGE MALT » sont d'autres objets) : sans libellé distinct, PG-I porte les deux variantes au prix DDFT.",
           "« RECEPT DDFT AUTO TEST 20 A125V INVIOL BLANC » (22,54 $ / 0,25 h) est un récepteur seul (sans boîte ni plaque), "
           "pas un prix d'assemblage : écarté.",
           "Ne PAS ajouter LEVGFNT1W (Lumen) : prix d'assemblage Dupuis."])
add('PG-E', desc='Prise DDFT enlevée', u='U', art='3.22', portee='ENLEVER 4',
    lib='famille PRISE DDFT, portée ENLEVER',
    regle='Même libellé que PC-E (harmonisation obligatoire ; règle 1, repère 0,35 h).',
    retenu=[(EP, 'U', 1)], ecartes=['PRISES A DEMANTELER'], notes=[])
add('PG-R', desc='Prise DDFT relocalisée', u='U', art='3.22', portee='RELOCALISER 1',
    lib='famille PRISE DDFT, portée RELOCALISER',
    regle='Même libellé que PC-R (harmonisation obligatoire ; règle 1, repère 1,5 h).',
    retenu=[(RP, 'U', 1)], ecartes=[], notes=[])

# ---- Commande, chauffage -------------------------------------------------------------------
add('INT-I', desc='Interrupteur simple 15 A 120 V neuf', u='U', art='3.35', portee='INSTALLER 5',
    lib='« INTERRUPTEUR SIMPLE » (famille INT SIMPLE, légende E-001)',
    regle='Règle 1 : repère METHODE « interrupteur 75,47 $ ».',
    retenu=[('INTERRUPTEUR 15A 120V', 'U', 1)],
    ecartes=['INTERRUPTEUR', 'INTERR DECO 15A 120V BLANC', 'INTERRUPTEUR 15A 347V'],
    notes=["Le bâtiment a des luminaires en 347 V : « INTERRUPTEUR 15A 347V » (57,24 $ / 1,325 h) est écarté parce que "
           "le repère METHODE (75,47 $) désigne « INTERRUPTEUR 15A 120V » ; le dire en note."])
add('INT-E', desc='Interrupteur enlevé', u='U', art='3.22', portee='ENLEVER 1',
    lib='famille INT SIMPLE, portée ENLEVER',
    regle=("Règles 2 à 4 (pas de repère) : « ENLEVER INTERRUPTEUR » et « INTERRUPTEUR A DEMANTELER » décrivent le MÊME objet et la "
           "MÊME action (règle 2 : égalité) ; nb_projets = 1 pour les deux (règle 3 : égalité) ; règle 4 : date_dernier le plus "
           "récent → « INTERRUPTEUR A DEMANTELER »."),
    retenu=[('INTERRUPTEUR A DEMANTELER', 'U', 1)], ecartes=['ENLEVER INTERRUPTEUR'],
    notes=["Arbitrage mécanique par la règle 4 (date). Écrire dans les notes l'alternative « ENLEVER INTERRUPTEUR » "
           "(0,35 h, même famille S-1835 que ENLEVER PRISE) : le chef de lot / le directeur pourra la préférer pour la cohérence."])
add('INT-R', desc='Interrupteur relocalisé', u='U', art='3.22', portee='absente du relevé', precaution=True,
    lib='aucune (portée absente)',
    regle='Libellé direct : « RELO INT » (règle 2 : même objet, même action).',
    retenu=[('RELO INT', 'U', 1)], ecartes=[], notes=[])
add('TH-I', desc='Thermostat neuf', u='U', art='3.23', portee='INSTALLER 2',
    lib='« THERMOSTAT » (famille THERMOSTAT, chauffage)',
    regle='Règle 1 : repère METHODE « thermostat 35 $ ».',
    retenu=[('THERMOSTAT', 'U', 1)],
    ecartes=['THERMOSTAT B/V', 'THERMOSTAT TS', 'THERMOSTAT ELECTRONIQUE INTEGRE', 'THERMOSTAT FDP'],
    notes=["« THERMOSTAT ELECTRONIQUE INTEGRE » (h = 0) est écarté (temps nul pour un vrai travail)."])
add('TH-E', desc='Thermostat enlevé', u='U', art='3.22', portee='absente du relevé', precaution=True,
    lib='aucune (portée absente)',
    regle='Aucun libellé direct → analogue Dupuis (même action, objet voisin : dispositif mural) : « ENLEVER PRISE ».',
    retenu=[(EP, 'U', 1)], ecartes=['INTERRUPTEUR A DEMANTELER'],
    analogue="aucun libellé « ENLEVER THERMOSTAT » ; dispositif mural ≈ prise enlevée (repère METHODE 0,35 h)",
    notes=[])
add('TH-R', desc='Thermostat relocalisé', u='U', art='3.22', portee='absente du relevé', precaution=True,
    lib='aucune (portée absente)',
    regle='Aucun libellé direct → analogue Dupuis : « RELO PRISE » (même valeur que « RELO INT »).',
    retenu=[(RP, 'U', 1)], ecartes=['RELO INT'],
    analogue="aucun libellé « RELO THERMOSTAT » ; dispositif mural ≈ prise relocalisée (repère METHODE 1,5 h)",
    notes=[])

# ---- Télécom -------------------------------------------------------------------------------
add('SD-I', desc='Sortie data (informatique/audio) neuve', u='U', art='3.33', portee='INSTALLER 65',
    lib='« SORTIE INFORMATIQUE/AUDIO » (famille SORTIE DATA, légende E-001)',
    regle='Règle 1 : repère METHODE « tel/data 3/4 22,32 $ / 0,89 h » (p ET h égalent le repère).',
    retenu=[('TEL/DATA 3/4', 'U', 1)],
    ecartes=['TEL/DATA', 'SORTIE DATA', 'SORTIE RESEAU', 'SORTIE TEL'],
    notes=["GROSSE LIGNE (65 unités) : « TEL/DATA » (nb_projets 17, 13,96 $ / 0,63 h) a le plus grand nb_projets mais la règle 1 "
           "(repère 22,32 $ / 0,89 h) passe avant la règle 3 ; METHODE dit « tel/data 0,63–0,89 h » — écrire la plage en note "
           "et l'écart de matériel/heures que représenterait l'autre libellé par unité (22,32−13,96 $ ; 0,89−0,63 h)."])
add('SD-E', desc='Sortie data enlevée', u='U', art='3.22', portee='ENLEVER 17',
    lib='famille SORTIE DATA, portée ENLEVER',
    regle=("Aucun libellé « ENLEVER DATA » (cherche ENLEV, ENL, DEMANTEL, DEPOS, DEBRANCH avant de conclure) → analogue Dupuis "
           "(même action, objet voisin : dispositif mural) « ENLEVER PRISE » ; le jugement (Estimation_2) A-03 (0,4 h/u) n'est "
           "qu'un repli — un analogue Dupuis vaut mieux."),
    retenu=[(EP, 'U', 1)], ecartes=['PRISES A DEMANTELER'],
    analogue="aucun libellé « ENLEVER DATA » ; sortie data = dispositif mural ≈ prise enlevée (repère METHODE 0,35 h)",
    notes=["Écrire dans les notes l'alternative jugement (Estimation_2) Détail A-03 h/unité 0,4 (relue dans la feuille Détail) "
           "et dire pourquoi elle n'est pas retenue."])
add('SD-R', desc='Sortie data relocalisée', u='U', art='3.22', portee='RELOCALISER 3',
    lib='famille SORTIE DATA, portée RELOCALISER',
    regle=("Aucun libellé « RELO DATA » → analogue Dupuis « RELO PRISE » (repère 1,5 h) ; repli jugement (Estimation_2) A-05 "
           "(h/unité 1) non retenu."),
    retenu=[(RP, 'U', 1)], ecartes=[],
    analogue="aucun libellé « RELO DATA » ; sortie data ≈ prise relocalisée (repère METHODE 1,5 h)",
    notes=["Écrire dans les notes l'alternative jugement (Estimation_2) Détail A-05 h/unité (relue dans la feuille Détail)."])
add('TV-I', desc='Sortie TV (câblodistribution) neuve', u='U', art='3.33', portee='absente du relevé (CONSERVER 4 seulement)',
    precaution=True,
    lib='« SORTIE DE CÂBLODISTRIBUTION AU MUR » (famille SORTIE TV)',
    regle='Règle 1 : repère METHODE « sortie TV 15 $ ».',
    retenu=[('SORTIE TV', 'U', 1)], ecartes=['TV', 'BOITIER TV', 'ENS BOITIER TV ENCASTRE'],
    notes=["« BOITIER TV » (0 $ / 0 h) est écarté : temps nul pour un vrai travail."])
add('TV-E', desc='Sortie TV enlevée', u='U', art='3.22', portee='absente du relevé (CONSERVER 4 seulement)',
    precaution=True, lib='aucune (portée absente)',
    regle='Aucun libellé direct → analogue « ENLEVER PRISE » (harmonisation).',
    retenu=[(EP, 'U', 1)], ecartes=[],
    analogue="aucun libellé « ENLEVER TV » ; sortie TV murale ≈ prise enlevée (repère METHODE 0,35 h)", notes=[])
add('TV-R', desc='Sortie TV relocalisée', u='U', art='3.22', portee='absente du relevé (CONSERVER 4 seulement)',
    precaution=True, lib='aucune (portée absente)',
    regle='Aucun libellé direct → analogue « RELO PRISE » (harmonisation).',
    retenu=[(RP, 'U', 1)], ecartes=[],
    analogue="aucun libellé « RELO TV » ; sortie TV murale ≈ prise relocalisée (repère METHODE 1,5 h)", notes=[])

# ---- Détecteur de mouvement ------------------------------------------------------------------
add('DM-I', desc='Détecteur de mouvement neuf', u='U', art='3.35', portee='absente du relevé', precaution=True,
    lib='« DETECTEUR DE MOUVEMENT » (famille DETECTEUR MOUVEMENT, commande)',
    regle='Pas de repère : règle 2 (même objet : égalité) puis règle 3 : plus grand nb_projets → « DETECTEUR MOUVEMENT ».',
    retenu=[('DETECTEUR MOUVEMENT', 'U', 1)],
    ecartes=['DETECTEUR DE MOUVEMENT', 'DETECTEUR MOUVEMENT :', 'INT MOUVEMENT'],
    notes=["Le libellé retenu a p = 0 dans le catalogue lui-même (aucun lot fournisseur ne couvre ce détecteur : LOT-DET = 2 "
           "détecteurs de fumée) : p = valeur du catalogue, PAS un « p = 0 forcé »."])
add('DM-E', desc='Détecteur de mouvement enlevé', u='U', art='3.22', portee='ENLEVER 1',
    lib='famille DETECTEUR MOUVEMENT, portée ENLEVER',
    regle='Aucun libellé direct (cherche ENLEV, ENL, DEMANTEL avec DETECT) → analogue « ENLEVER PRISE » (harmonisation).',
    retenu=[(EP, 'U', 1)], ecartes=['STATION ENL', 'EQUIPEMENT A ENLEVER'],
    analogue="aucun libellé « ENLEVER DETECTEUR » ; dispositif mural/plafond léger ≈ prise enlevée (repère METHODE 0,35 h)",
    notes=["Alternatives à nommer en note : « STATION ENL » (0,5 h, dispositif d'alarme) et « EQUIPEMENT A ENLEVER » (0,5 h, générique)."])
add('DM-R', desc='Détecteur de mouvement relocalisé', u='U', art='3.22', portee='absente du relevé', precaution=True,
    lib='aucune (portée absente)',
    regle='Aucun libellé « RELO DETECTEUR MOUVEMENT » → analogue (même action, objet voisin : détecteur) « RELO DETECTEUR A FUME ».',
    retenu=[('RELO DETECTEUR A FUME', 'U', 1)], ecartes=[RP, 'RELO DETECTEUR FUME'],
    analogue="aucun libellé « RELO DETECTEUR MOUVEMENT » ; objet voisin = détecteur (installation 0,5 h comme le détecteur de fumée)",
    notes=["Écrire l'alternative « RELO PRISE » (1,5 h) en note."])

# ---- Contrôle d'accès ------------------------------------------------------------------------
add('LC-I', desc='Lecteur de carte neuf', u='U', art='3.33', portee='INSTALLER 2 (CONSERVER 3)',
    lib='« LECTEUR DE CARTE » (famille LECTEUR CARTE, intrusion)',
    regle=("Règle 1 : repère METHODE « lecteur de carte 15 $ » (les deux libellés ont p = 15) ; règle 2 égalité ; règle 3 : plus grand "
           "nb_projets → « LECTEUR DE CARTE »."),
    retenu=[('LECTEUR DE CARTE', 'U', 1)], ecartes=['LECTEUR CARTE', 'GARDE LECTEUR'], notes=[])
add('LC-E', desc='Lecteur de carte enlevé', u='U', art='3.22', portee='absente du relevé', precaution=True,
    lib='aucune (portée absente)',
    regle=("Aucun libellé « LECTEUR ENL » → analogue Dupuis du MÊME projet et de la même famille (contrôle d'accès : "
           "« LECTEUR RELO », « GACHE RELO », « CONTAC PORTE RELO » sont de S-1659) : « CONTACT DE PORTE ENL » (0 $ / 0,5 h)."),
    retenu=[(CPE, 'U', 1)], ecartes=['OPERATEUR PORTE ENL', 'IC ENL', 'STATION ENL', EP],
    analogue="aucun libellé « LECTEUR ENL » ; famille ENL du projet S-1659 (dispositifs d'accès/alarme enlevés, 0,5 h)",
    notes=["« OPERATEUR PORTE ENL », « IC ENL », « STATION ENL » ont les mêmes valeurs (0 $ / 0,5 h) : choix du libellé sans effet sur p et h."])
add('LC-R', desc='Lecteur de carte relocalisé', u='U', art='3.22', portee='absente du relevé', precaution=True,
    lib='aucune (portée absente)',
    regle='Libellé direct : « LECTEUR RELO » (règle 2 : même objet, même action).',
    retenu=[('LECTEUR RELO', 'U', 1)], ecartes=[],
    notes=["p = 15 (valeur du catalogue pour une relocalisation) : RELOCALISER → prix selon le catalogue."])
add('GA-I', desc='Gâche électrique neuve', u='U', art='3.33', portee='absente du relevé (CONSERVER 3 seulement)',
    precaution=True,
    lib='« GÂCHE ÉLECTRIQUE » (famille GACHE, intrusion)',
    regle='Règle 1 : repère METHODE « gâche 15 $ » → « GACHE » (« GACHE ELECTRIQUE » = 10 $ ne l\'égale pas).',
    retenu=[('GACHE', 'U', 1)], ecartes=['GACHE ELECTRIQUE', 'BOUTON GACHE'], notes=[])
add('GA-E', desc='Gâche électrique enlevée', u='U', art='3.22', portee='absente du relevé (CONSERVER 3 seulement)',
    precaution=True, lib='aucune (portée absente)',
    regle='Aucun libellé « GACHE ENL » → même analogue que LC-E : « CONTACT DE PORTE ENL » (harmonisation).',
    retenu=[(CPE, 'U', 1)], ecartes=['OPERATEUR PORTE ENL', EP],
    analogue="aucun libellé « GACHE ENL » ; famille ENL du projet S-1659 (dispositifs d'accès enlevés, 0,5 h)", notes=[])
add('GA-R', desc='Gâche électrique relocalisée', u='U', art='3.22', portee='absente du relevé (CONSERVER 3 seulement)',
    precaution=True, lib='aucune (portée absente)',
    regle='Libellé direct : « GACHE RELO » (règle 2 : même objet, même action).',
    retenu=[('GACHE RELO', 'U', 1)], ecartes=[],
    notes=["p = 15 (valeur du catalogue pour une relocalisation)."])

# ---- Boîtes de jonction ---------------------------------------------------------------------
add('BJ-I', desc='Boîte de jonction neuve', u='U', art='3.31', portee='INSTALLER 3 (CONSERVER 5)',
    lib='« BOITE DE JONCTION » (famille BOITE JONCTION, services, légende E-001)',
    regle=("Aucun libellé « BOITE DE JONCTION » ; pas de repère. Règle 2 : les candidats carrés/octogonaux décrivent une boîte ; "
           "la feuille Matériel Lumen chiffre les « JB postes » en boîte CARRÉE 4 po (IBE52151K) → boîte carrée ; règle 3 : "
           "plus grand nb_projets → « BOITE CARRE 2-1/8PO KO 1 » (nb_projets 22). Repli Lumen IBE52151K NON utilisé : Dupuis a un analogue."),
    retenu=[('BOITE CARRE 2-1/8PO KO 1', 'U', 1)],
    ecartes=['BOITE OCTOG 1-1/2PO KO 1', 'BOITE D 8X8X4PO CEMA1', 'BOITE CARREES 4 PO', 'BOITE CARRE 1-1/2PO KO 1'],
    notes=["« BOITE OCTOG 1-1/2PO KO 1 » = boîte d'éclairage (Lumen IBE54151L « JB éclairage ») ; « BOITE D 8X8X4PO CEMA1 » = "
           "boîte de tirage CEMA 1 plus grosse. Dire pourquoi la boîte carrée est retenue.",
           "Écrire en note le prix Lumen IBE52151K (5,2196 $, relu dans la feuille Matériel Lumen) comme point de comparaison seulement."])
add('BJ-E', desc='Boîte de jonction enlevée', u='U', art='3.22', portee='ENLEVER 2',
    lib='famille BOITE JONCTION, portée ENLEVER',
    regle='Aucun libellé direct → analogue « ENLEVER PRISE » (boîte + dispositif mural ; harmonisation).',
    retenu=[(EP, 'U', 1)], ecartes=['EQUIPEMENT A ENLEVER'],
    analogue="aucun libellé « ENLEVER BOITE » ; boîte murale ≈ prise enlevée (repère METHODE 0,35 h)",
    notes=["Écrire l'alternative jugement (Estimation_2) Détail A-03 (« boîtes mobilier », h/unité relu dans la feuille Détail) "
           "et « EQUIPEMENT A ENLEVER » (0,5 h) en note."])
add('BJ-R', desc='Boîte de jonction relocalisée', u='U', art='3.22', portee='absente du relevé', precaution=True,
    lib='aucune (portée absente)',
    regle='Aucun libellé direct → analogue « RELO PRISE » (harmonisation).',
    retenu=[(RP, 'U', 1)], ecartes=['BOITIER LUMONEUX RELO'],
    analogue="aucun libellé « RELO BOITE » ; boîte murale ≈ prise relocalisée (repère METHODE 1,5 h)",
    notes=["« BOITIER LUMONEUX RELO » (15 $ / 1 h) est un boîtier lumineux d'un autre projet : objet différent, écarté."])

# ---- Monuments de plancher -------------------------------------------------------------------
add('MP-I', desc='Monument de plancher neuf (poke-through)', u='U', art='3.34', portee='INSTALLER 3 (CONSERVER 1)',
    lib='« MONUMENT PLANCHER SURFACE, TYPE HUBBELL S1PT / POKE THROUGH » (famille MONUMENT PLANCHER, services)',
    regle=("Règle 1 : repère METHODE « monument 250 $ » → « MONUMENT PLANCHER » et « MONUMENT PLANCHER 1TE » ont tous deux p = 250 ; "
           "règle 2 égalité ; règle 3 égalité (nb_projets 1 et 1) ; règle 4 : date_dernier le plus récent → « MONUMENT PLANCHER 1TE » "
           "(p = 250 et h = 1 sont identiques pour les deux : le choix n'a aucun effet numérique, le dire en note)."),
    retenu=[('MONUMENT PLANCHER 1TE', 'U', 1)],
    ecartes=['MONUMENT PLANCHER', 'MONUMENT PLANCHER SU', 'MONUMENT PLANCHER EN', 'MONUMENT PLANCHER PR'],
    notes=["GROSSE LIGNE. « MONUMENT PLANCHER SU » (SU = surface ?) décrit peut-être mieux le type du plan mais p = 118,75 ≠ 250 : "
           "écarté par la règle 1 (à dire).",
           "NE PAS utiliser le prix Lumen du poke-through HUBS1R6PTDEHBLK (1 461,22 $/u, feuille Matériel Lumen, plan : S1R6PTFIT) : le "
           "repère Dupuis 250 $ prévaut ; NOTER l'écart entre 250 $ et 1 461,22 $ en note."])
add('MP-E', desc='Monument de plancher enlevé', u='U', art='3.22', portee='ENLEVER 3',
    lib='famille MONUMENT PLANCHER, portée ENLEVER',
    regle='Aucun libellé direct → analogue « ENLEVER PRISE » (monument = sortie de plancher alimentation/data ; harmonisation).',
    retenu=[(EP, 'U', 1)], ecartes=['EQUIPEMENT A ENLEVER'],
    analogue="aucun libellé « ENLEVER MONUMENT » ; monument = prise/data en boîtier de plancher ≈ prise enlevée (repère METHODE 0,35 h)",
    notes=["Alternatives en note : « EQUIPEMENT A ENLEVER » (0,5 h, générique) et jugement (Estimation_2) Détail A-03 (« câbles sortant du "
           "plancher », h/unité relu) — dire pourquoi l'analogue Dupuis prime."])
add('MP-R', desc='Monument de plancher relocalisé', u='U', art='3.22', portee='absente du relevé', precaution=True,
    lib='aucune (portée absente)',
    regle='Aucun libellé direct → analogue « RELO PRISE » (harmonisation).',
    retenu=[(RP, 'U', 1)], ecartes=[],
    analogue="aucun libellé « RELO MONUMENT » ; ≈ prise relocalisée (repère METHODE 1,5 h)", notes=[])

# ---- Boîtier C -------------------------------------------------------------------------------
add('BC-I', desc='Boîtier « C » neuf (hors légende)', u='U', art='3.36', portee='absente du relevé (ENLEVER 2, CONSERVER 2)',
    precaution=True,
    lib='« BOITIER « C » (hors légende — R-006 TEST-E201) » (famille BOITIER C, alarme)',
    regle=("Aucun libellé direct (cherche BOITIER, BOITE, CONTACT, ALIMENT). Objet NON défini par la légende. Indice : dans la feuille "
           "Marques de releve.xlsx, les BOITIER C (E101, E201) sont posés à quelques points de distance d'un lecteur de carte et d'une gâche "
           "(mêmes portes) → dispositif d'accès de porte ; HYPOTHÈSE DE TRAVAIL, non prouvée : « C » = contact de porte. Analogue : "
           "« CONTACT PORTE » (15 $, convention Dupuis du dispositif d'accès posé, comme lecteur et gâche à 15 $). Règle 3 égalité "
           "(CONTACT DE PORTE nb 3 = CONTACT PORTE nb 3), règle 4 : date → « CONTACT PORTE »."),
    retenu=[('CONTACT PORTE', 'U', 1)],
    ecartes=['CONTACT DE PORTE', 'BOITE ALMENTATION', 'BOITIER ALIMENTATION'],
    analogue="« BOITIER C » non défini par la légende ; hypothèse contact de porte (voisin du lecteur et de la gâche)",
    notes=["Écrire clairement en note que l'identité de « BOITIER C » est une hypothèse, avec les coordonnées Marques utilisées comme indice."])
add('BC-E', desc='Boîtier « C » enlevé (hors légende)', u='U', art='3.22', portee='ENLEVER 2 (CONSERVER 2)',
    lib='famille BOITIER C, portée ENLEVER (E201)',
    regle='Aucun libellé « ENLEVER BOITIER » → analogue du même projet S-1659 pour un dispositif de porte : « CONTACT DE PORTE ENL » (harmonisation avec LC-E, GA-E).',
    retenu=[(CPE, 'U', 1)], ecartes=['OPERATEUR PORTE ENL', 'STATION ENL', EP],
    analogue="« BOITIER C » ≈ contact de porte (hypothèse) ; famille ENL du projet S-1659 (0,5 h)",
    notes=["Attention : BC-E EST relevé (2) — ce n'est pas une correspondance de précaution : ne PAS écrire la phrase de précaution dans src."])
add('BC-R', desc='Boîtier « C » relocalisé (hors légende)', u='U', art='3.22', portee='absente du relevé', precaution=True,
    lib='aucune (portée absente)',
    regle='Libellé voisin direct : « CONTAC PORTE RELO » (hypothèse contact de porte ; même projet S-1659 que LECTEUR RELO / GACHE RELO).',
    retenu=[('CONTAC PORTE RELO', 'U', 1)], ecartes=['LECTEUR RELO', 'GACHE RELO', 'BOUTON DE PORTE RELO'],
    analogue="« BOITIER C » ≈ contact de porte (hypothèse)",
    notes=["p = 15 (valeur du catalogue pour une relocalisation)."])

# ---- Hors plan (feuille Détail) ---------------------------------------------------------------
add('D-09', desc='Barrière anti-vol : 2 boîtes de jonction + raccord panneau de contrôle (PU-1 23)', u='LOT', art='3.31',
    portee='hors plan — Détail D-09 : 1 lot, 6 h estimées', horsplan=True,
    lib='Détail D-09 « Barrière anti-vol : 2 boîtes de jonction + raccord panneau de contrôle (PU-1 23) » (E-104, 1 lot, 6 h estimées)',
    regle=("Composition d'analogues Dupuis (un src composé écrit chaque libellé et l'opération) : 2 × boîte de jonction (même libellé que BJ-I : "
           "« BOITE CARRE 2-1/8PO KO 1 ») + 1 × raccordement d'équipement (« RACCORD DIRECT », nb_projets 5). p = 2×p(boîte) + p(raccord), "
           "h = 2×h(boîte) + h(raccord) — recalculer par script, arrondir à 4 décimales."),
    retenu=[('BOITE CARRE 2-1/8PO KO 1', 'U', 2), ('RACCORD DIRECT', 'U', 1)],
    ecartes=['RACCORD PARTITION', 'RACCORD RCFF'],
    notes=["Le jugement (Estimation_2) du Détail est 6 h pour le lot : l'écrire en note comme alternative non retenue (un analogue Dupuis "
           "vaut mieux que le jugement) et dire que le conduit/filage entre les boîtes n'est pas compris dans cette ligne.",
           "DOUBLE COMPTE PROBABLE avec BJ-I (voir doubles_comptes) : ne pas le résoudre, le signaler."])
add('D-10', desc='Bornes de prêts / fontaine hall — JB dans mur adjacent', u='U', art='3.31',
    portee='hors plan — Détail D-10 : 1 u, 2 h estimées', horsplan=True,
    lib='Détail D-10 « Bornes de prêts / fontaine hall (P2-63, note 2) — JB dans mur adjacent » (E-104, 1 u, 2 h estimées)',
    regle=("Le libellé du Détail ne décrit qu'une boîte de jonction (JB) : 1 × même libellé que BJ-I (« BOITE CARRE 2-1/8PO KO 1 »). "
           "Aucun raccordement n'est dit : ne pas en inventer."),
    retenu=[('BOITE CARRE 2-1/8PO KO 1', 'U', 1)], ecartes=['RACCORD DIRECT'],
    notes=["Alternative à écrire en note : boîte + « RACCORD DIRECT » (si un raccordement des bornes était à la charge de DR) et jugement "
           "(Estimation_2) 2 h/u du Détail — non retenus faute de texte qui les justifie.",
           "DOUBLE COMPTE PROBABLE avec BJ-I (voir doubles_comptes) : le signaler."])
add('D-11', desc="Bouton d'appel — boîte + conduit vide (système fourni par d'autres)", u='U', art='3.33',
    portee='hors plan — Détail D-11 : 1 u, 1 h estimée', horsplan=True,
    lib="Détail D-11 « Bouton d'appel — boîte + conduit vide (système fourni par d'autres) » (E-104, 1 u, 1 h estimée ; note : Aide au lecteur 116)",
    regle=("Règle 2 (même objet) : « DECLENCHEUR APPEL » est le seul libellé « appel » ; convention Dupuis des dispositifs posés par DR et fournis par d'autres : "
           "15 $ + 0,35–0,5 h (BOUTON HANDICAPE, BOUTON OUVERTURE, OPERATEUR PORTE, CONTACT DE PORTE, LECTEUR DE CARTE, GACHE…)."),
    retenu=[('DECLENCHEUR APPEL', 'U', 1)],
    ecartes=['BOUTON HANDICAPE', 'BOUTON OUVERTURE', 'BOTON HANDICAPE'],
    notes=["Les trois candidats ont p = 15 ; seul h change (0,35 contre 0,5) : dire que la règle 2 (mot « appel ») départage, la règle 3 "
           "(nb_projets 2 contre 1) donnerait « BOUTON HANDICAPE ».",
           "Le conduit vide de la ligne n'a pas de longueur dans le kit : NE PAS l'inventer ; écrire en note « conduit vide non chiffré dans "
           "cette ligne (longueur absente du kit) »."])
add('E-03', desc='Boîte de plancher refaite (salle 208, ancien mobilier)', u='U', art='3.34',
    portee='hors plan — Détail E-03 : 2 u, 2,5 h/u estimées (« à confirmer »)', horsplan=True,
    lib='Détail E-03 « Boîte de plancher refaite (salle 208, ancien mobilier — note 1 E-102) » (E-102/E-105, 2 u, 2,5 h/u estimées)',
    regle=("Analogue Dupuis : boîte de plancher ≈ monument de plancher → même libellé que MP-I (« MONUMENT PLANCHER 1TE », repère 250 $) ; "
           "un analogue Dupuis prime sur le jugement (Estimation_2) 2,5 h/u."),
    retenu=[('MONUMENT PLANCHER 1TE', 'U', 1)],
    ecartes=['MONUMENT PLANCHER', 'MONUMENT PLANCHER PR', 'MONUMENT PLANCHER SU'],
    notes=["Écrire l'alternative jugement (Estimation_2) 2,5 h/u en note.",
           "DOUBLES COMPTES PROBABLES avec MP-E / MP-I (même salle, mêmes monuments, voir doubles_comptes) : les signaler."])
add('E-06', desc="Bouton d'appel (2) + bouton de panique (1) — boîte + conduit vide", u='U', art='3.33',
    portee='hors plan — Détail E-06 : 3 u, 1 h/u estimée', horsplan=True,
    lib="Détail E-06 « Bouton d'appel (2) + bouton de panique (1) — boîte + conduit vide » (E-105, 3 u, 1 h/u estimée)",
    regle='Même arbitrage que D-11 (harmonisation obligatoire) : « DECLENCHEUR APPEL » (un bouton de panique est un déclencheur d\'appel).',
    retenu=[('DECLENCHEUR APPEL', 'U', 1)],
    ecartes=['BOUTON HANDICAPE', 'BOUTON OUVERTURE'],
    notes=["Mêmes notes que D-11 (conduit vide non chiffré, longueur absente du kit)."])

# ----------------------------------------------------------------------------------------------
# Politique d'analogues harmonisée (commune aux 3 releveurs)
# ----------------------------------------------------------------------------------------------
POLITIQUE = f"""## POLITIQUE D'ANALOGUES (harmonisée entre les 3 releveurs B1 — à appliquer telle quelle)
Quand le catalogue n'a aucun libellé direct pour une portée (enlever / relocaliser), les trois releveurs B1 utilisent LE MÊME analogue
Dupuis (les valeurs ci-dessous sont lues dans le CSV par le chef de lot — RELIS-LES toi-même avec `ligne()`) :
- Démontage (-E) d'un dispositif mural/boîte (prise, USB, DDFT, data, TV, thermostat, boîte de jonction, monument, détecteur de mouvement) :
  {cand('ENLEVER PRISE')}   ← repère METHODE « prise enlevée 0,35 h »
- Relocalisation (-R) du même type de dispositif : {cand('RELO PRISE')}   ← repère METHODE « relocalisation de prise 1,5 h »
- Démontage (-E) d'un dispositif de contrôle d'accès (lecteur de carte, gâche, boîtier C) : {cand('CONTACT DE PORTE ENL')}
  (famille « ENL » du projet S-1659, la même qui contient « LECTEUR RELO », « GACHE RELO » ; valeurs identiques pour
  {cand('OPERATEUR PORTE ENL')} ; {cand('IC ENL')} ; {cand('STATION ENL')})
- Relocalisation (-R) d'un détecteur de mouvement : {cand('RELO DETECTEUR A FUME')}
- Libellé direct pour INT-R : {cand('RELO INT')}
Alternatives à NOMMER en notes quand tu les écartes : {cand('PRISES A DEMANTELER')} ; {cand('EQUIPEMENT A ENLEVER')} ;
jugement (Estimation_2) Détail A-03 (démantèlement services RDC, h/unité), A-04 (2e), A-05 (relocalisation services) — relis ces h/unité dans la feuille Détail.
Ordre de repli (rappel) : analogue Dupuis > prix régulier Lumen (matériel) + jugement (Estimation_2) (temps). Aucun code de ton lot ne devrait exiger Lumen
ou le jugement ; si tu en utilises un, dis pourquoi en note."""

# ----------------------------------------------------------------------------------------------
# Sous-lots
# ----------------------------------------------------------------------------------------------
LOTS = {
    1: dict(
        titre='PRISES, INTERRUPTEURS, THERMOSTATS',
        codes=['PC-I', 'PC-E', 'PC-R', 'PU-I', 'PU-E', 'PU-R', 'PG-I', 'PG-E', 'PG-R',
               'INT-I', 'INT-E', 'INT-R', 'TH-I', 'TH-E', 'TH-R'],
        enjeu=("Les plus grosses lignes de matériel du dossier pour les prises (PC-I 25, PU-I 20, PG-I 22) sont dans ton sous-lot : "
               "une erreur de libellé ou une médiane glissée ici passe telle quelle dans le matériel et les heures."),
        doubles=[
            ('D-06', 'PC-I', "Détail D-06 « Prise double murale/colonne NEUVE » (8 u) recompte des prises doubles neuves relevées sur plan"),
            ('D-02', 'PU-I', "Détail D-02 « Table c/a boîte d'électrification : 2 prises doubles + 2 prises USB » (5 u) recompte des USB relevées"),
            ('D-07', 'PG-I', "Détail D-07 « Prise DDFT 15A fontaine (P2-61) » (1 u) recompte une DDFT relevée"),
            ('D-01', 'PC-I', "Détail D-01 « Poste de travail intégré mobilier : … 1 prise double 15A + 1 prise double 20A Decora… » (18 postes)"),
            ('LEV16252W/LEV80401NW (Lumen)', 'PC-I', "les prises et plaques Lumen ne s'ajoutent pas au prix d'assemblage Dupuis"),
        ]),
    2: dict(
        titre='TÉLÉCOM, DÉTECTEUR DE MOUVEMENT, CONTRÔLE D\'ACCÈS',
        codes=['SD-I', 'SD-E', 'SD-R', 'TV-I', 'TV-E', 'TV-R', 'DM-I', 'DM-E', 'DM-R',
               'LC-I', 'LC-E', 'LC-R', 'GA-I', 'GA-E', 'GA-R'],
        enjeu=("SD-I (65 sorties data) est la plus grosse ligne de ce sous-lot : le choix entre « TEL/DATA 3/4 » et « TEL/DATA » change "
               "le matériel et les heures de 65 unités ; SD-E (17) et SD-R (3) n'ont aucun libellé direct."),
        doubles=[
            ('D-08', 'SD-I', "Détail D-08 « Sortie data murale/colonne : boîte + conduit 3/4\" vers entreplafond + corde de tirage » (10 u)"),
            ('D-04', 'SD-I', "Détail D-04 « Écran sur mur/colonne — boîte courant + données » (2 u)"),
            ('D-05', 'SD-I', "Détail D-05 « Kiosque TV (P-2 6) — prise + data » (1 u)"),
            ('D-01', 'SD-I', "Détail D-01 « … boîte data 2 RJ45 (plaque seulement) … » (18 postes) et E-01/E-05 (data 2 RJ45)"),
        ]),
    3: dict(
        titre='BOÎTES, MONUMENTS DE PLANCHER, BOÎTIER C, LIGNES HORS PLAN',
        codes=['BJ-I', 'BJ-E', 'BJ-R', 'MP-I', 'MP-E', 'MP-R', 'BC-I', 'BC-E', 'BC-R',
               'D-09', 'D-10', 'D-11', 'E-03', 'E-06'],
        enjeu=("MP-I (monument, 3 u × 250 $) est une grosse ligne de matériel ; BJ, MP-E, BC et les 5 lignes hors plan n'ont aucun libellé "
               "direct : c'est le sous-lot où l'on arbitre le plus, et où les doubles comptes plan/Détail sont les plus probables."),
        doubles=[
            ('D-09', 'BJ-I', "Détail D-09 recompte « 2 boîtes de jonction » (E-104) ; le relevé a 3 BOITE JONCTION INSTALLER, toutes sur E104 (voir Marques)"),
            ('D-10', 'BJ-I', "Détail D-10 recompte « JB dans mur adjacent » (E-104) ; 2 (D-09) + 1 (D-10) = 3 = BJ-I du relevé ?"),
            ('D-01', 'BJ-I', "Détail D-01 (boîte de jonction par poste), D-03 (« JB dans mur »), E-04 (« JB + prise ») comptent aussi des JB"),
            ('E-03', 'MP-E', "Détail E-03 (boîte de plancher refaite, salle 208) vs MP-E (3 monuments enlevés sur E102)"),
            ('E-03', 'MP-I', "Détail E-03 vs MP-I (3 monuments installés sur E105) ; Détail E-02 (monument Hubbell S1R6PTFIT, 2 u) aussi"),
        ]),
}

assert sorted(c for lot in LOTS.values() for c in lot['codes']) == sorted(SPEC), \
    sorted(set(SPEC) ^ {c for lot in LOTS.values() for c in lot['codes']})
assert len(SPEC) == 44, len(SPEC)


def bloc_code(code):
    s = SPEC[code]
    en_tete = (f"### {code} — {s['desc']}\n"
               f"- portée relevée : {s['portee']} — u = `{s['u']}` — art = `{s['art']}`\n"
               f"- libellé du relevé / de la feuille Détail : {s['lib']}\n"
               f"- règle appliquée par le chef de lot : {s['regle']}")
    retenu = []
    for desc, um, mult in s['retenu']:
        pref = f"{mult} × " if mult != 1 else ''
        retenu.append(f"  - {pref}{cand(desc, um)}")
    txt = en_tete + "\n- RETENU (arbitrage du chef de lot — à RELIRE dans le CSV ; si tu n'es pas d'accord, écris ton choix et la raison dans `notes`) :\n"
    txt += '\n'.join(retenu)
    if len(s['retenu']) > 1 or s['retenu'][0][2] != 1:
        p = round(sum(float(ligne(d, u)['prix_a_utiliser']) * m for d, u, m in s['retenu']), 4)
        h = round(sum(float(ligne(d, u)['temps_a_utiliser']) * m for d, u, m in s['retenu']), 4)
        txt += f"\n  - composition attendue : p = {p} ; h = {h} (à recalculer toi-même par script)"
    if s.get('analogue'):
        txt += f"\n- à dire dans `src` : « ; analogue : {s['analogue']} »"
    if s.get('precaution'):
        txt += f"\n- à dire dans `src` : « ; {PREC} »"
    if s['ecartes']:
        txt += "\n- ÉCARTÉS à écrire dans `notes` (libellé exact, p, h, nb_projets, date) :"
        for d in s['ecartes']:
            um = 'U'
            txt += f"\n  - {cand(d, um)}"
    for n in s['notes']:
        txt += f"\n- NOTE : {n}"
    return txt


SQUELETTE = '''```python
import csv, json, re
CAT = '/home/claude/entrainement/S-1902/swarm-2/catalogue-prix-temps-dupuis.csv'
rows = list(csv.DictReader(open(CAT, encoding='utf-8-sig'), delimiter=';'))
assert len(rows) == 2068, len(rows)
def ligne(desc, um=None):
    t = [r for r in rows if r['description'] == desc and (um is None or r['um'] == um)]
    assert len(t) == 1, (desc, len(t))
    return t[0]
def src_d(r):          # src Dupuis EXACT, construit depuis la ligne (aucune frappe à la main)
    return (f"catalogue Dupuis « {r['description']} » um={r['um']} (dernier {r['date_dernier']}, "
            f"{r['projet_dernier']}, nb_projets {r['nb_projets']})")
def note_ecarte(desc, um='U'):   # note d'un candidat écarté : libellé exact, p, h, nb_projets, date
    r = ligne(desc, um)
    return (f"écarté « {r['description']} » um={r['um']} p={r['prix_a_utiliser']} h={r['temps_a_utiliser']} "
            f"nb_projets={r['nb_projets']} dernier {r['date_dernier']}")
def mk(code, desc, u, art, lib, um='U', suite=''):   # ligne simple (un seul libellé Dupuis)
    r = ligne(lib, um)
    return {"code": code, "desc": desc, "q": None, "u": u,
            "p": float(r['prix_a_utiliser']), "h": float(r['temps_a_utiliser']),
            "art": art, "src": src_d(r) + suite}
# ligne composée (ex. D-09) : p = round(2*p1 + p2, 4), h idem ; src = « 2 × <src_d(r1)> + 1 × <src_d(r2)> »
```'''

CONSIGNE_FIN = """## Ce que tu produis (et rien d'autre)
- Un SEUL fichier : `/home/claude/entrainement/S-1902/swarm-2/lots/releveur-B1-{m}.json` (format « Format JSON » ci-dessus ; `"niveau": "releveur"`,
  `"nom": "B1-{m}"`, `"modele_demande": "haiku"`, `"effort_demande": "xhigh"`), avec EXACTEMENT les {n} lignes de tes codes (une par code, dans l'ordre
  de ta liste), `q` = `null` partout, `p` et `h` en nombres, `notes` (liste de textes) et `doubles_comptes` (liste ; vide si rien). `desc` = l'intitulé qui suit
  le code dans le titre « ### CODE — intitulé » de chaque bloc ci-dessus ; `u` et `art` = ceux écrits dans le bloc du code.
- N'écris AUCUN autre fichier (ni script, ni brouillon) : exécute ton code Python en ligne (`python3 - <<'EOF' … EOF`). Ne lis pas les autres
  fichiers de `lots/` ni de `prompts/` : tu n'en as pas besoin et ils ne t'aident pas à relire le catalogue.
- Contenu minimal de `notes` : (1) une entrée par code de ton lot disant le libellé retenu, la règle appliquée (1, 2, 3 ou 4 ; ou « analogue »)
  et les candidats écartés avec libellé exact, p, h, nb_projets, date (utilise `note_ecarte`) ; (2) tes désaccords éventuels avec l'arbitrage du chef de
  lot (choix + raison) ; (3) ce que tu as cherché sans trouver (motifs de recherche) ; (4) le rappel « taux 85 $/h et facteur de prix de vente 1,244 :
  non appliqués (METHODE.md §5/§7) » ; (5) le nom du modèle que tu es (« Claude Haiku », tel que ton contexte le dit).
- Avant d'écrire : relis CHAQUE ligne Dupuis avec `ligne(desc, um)` et vérifie `p == float(prix_a_utiliser)` et `h == float(temps_a_utiliser)` (somme
  pondérée pour une ligne composée) ; vérifie que `src` reproduit le libellé exact ; vérifie 0 doublon de code, `q is None` partout, ENLEVER → p = 0.
- Après avoir écrit le fichier : `python3 -c "import json;d=json.load(open('/home/claude/entrainement/S-1902/swarm-2/lots/releveur-B1-{m}.json'));print(len(d['lignes']), sorted(l['code'] for l in d['lignes']))"`
  doit afficher {n} et exactement tes codes. Puis réponds en UNE ligne (nom du fichier écrit + nombre de lignes) et ARRÊTE-TOI : tu ne lances
  personne, tu n'écris pas de prompt, tu ne consolides rien."""


def prompt(m):
    lot = LOTS[m]
    n = len(lot['codes'])
    codes = ' '.join(lot['codes'])
    fj = FORMAT_JSON.replace('"nom": "B1-2"', f'"nom": "B1-{m}"').replace('"effort_demande": "high"', '"effort_demande": "xhigh"')
    fj = fj.replace('## Format JSON (ARCHITECTURE.md §5) — releveurs et chefs de lot (exemple : adapter niveau, nom, effort)',
                    '## Format JSON (ARCHITECTURE.md §5) — releveur (l\'exemple ci-dessous est illustratif : ton fichier ne contient QUE tes codes)')
    assert f'"nom": "B1-{m}"' in fj and '"effort_demande": "xhigh"' in fj
    out = []
    out.append('effort: xhigh\nmodele: haiku\n')
    out.append(f"# Releveur B1-{m} — {lot['titre']} : prix et temps « méthode Dupuis » (essaim 2, chiffrage à l'aveugle S-1902)\n")
    out.append(f"""Tu es le releveur B1-{m}, modèle Claude Haiku, feuille de l'arbre d'une équipe hiérarchique d'estimation électrique chez
DR Électrique. Ton supérieur est le chef de lot B1 (Claude Sonnet 5.5), sous le directeur B (Claude Opus 5.5), sous le chef de l'essaim
(Claude Fable 5.1). Tu ne délègues à personne : tu fais tout toi-même, tu écris UN fichier JSON, tu le vérifies et tu t'arrêtes.
Dossier S-1902 : Bibliothèque Georgette-Lepage, Brossard — appel d'offres SP-GTER-26-0080.

Mission du lot B (prix et temps) : pour chaque code, le PRIX unitaire `p` et le TEMPS unitaire `h` « méthode Dupuis » (colonnes `prix_a_utiliser` /
`temps_a_utiliser` du catalogue = dernière valeur de M. Dupuis, JAMAIS la médiane), l'article du bordereau `art` et la source exacte `src`. Les
quantités sont la mission d'une autre équipe : `q` reste `null` partout.

Ton sous-lot (B1-{m}) : {n} codes, ni plus ni moins : {codes}.
Pourquoi tu es sur ce sous-lot avec le plus grand soin : {lot['enjeu']}
""")
    out.append("```\n" + REGLES + "\n```\n")
    out.append("```\n" + MECA + "\n```\n")
    out.append(f"""## Dossier de travail
`/home/claude/entrainement/S-1902/swarm-2/` — tu y travailles uniquement (chemins absolus conseillés, `python3`). Tu n'écris QUE ton fichier
`lots/releveur-B1-{m}.json`. Tu n'as pas besoin des fichiers de l'équipe A (quantités).

## Première chose à faire
Lis `CONSIGNES.md` et `METHODE.md` (courts), `rapport-releve.md` (tableau « famille | total | portées »), `reserves.md` (R-002, R-006, R-007, Q14), puis ouvre
le catalogue (code ci-dessous), la feuille `Détail` d'Estimation_2 (lignes D-01…D-11, E-01…E-06 et A-03…A-05 pour le contexte), la feuille `Matériel Lumen`
et `releve.xlsx` (feuilles `Par libellé` et `Marques`). Pour CHAQUE code, interroge toi-même le catalogue (`cherche`, `ligne`) : relis les candidats cités
plus bas ET cherche d'autres variantes par sous-chaînes courtes — ne conclus jamais « absent » après une seule recherche. Le chef de lot a déjà arbitré
chaque code (bloc « RETENU ») : tu dois le CONFIRMER ou le CONTREDIRE par la lecture du fichier, jamais le recopier sans relire.
""")
    out.append(KIT + "\n")
    out.append(PRIX + "\n")
    out.append(NOMEN + "\n")
    out.append(FORMAT_SRC + "\n")
    out.append(fj + "\n")
    out.append(VERIF + "\n")
    out.append(POLITIQUE + "\n")
    out.append(f"## Tes {n} codes — portée relevée, libellés candidats et arbitrage du chef de lot\n"
               "Les valeurs `p`, `h`, `nb_projets`, date et projet ci-dessous ont été lues dans le CSV par le chef de lot ; relis-les toi-même "
               "(`ligne(desc, um)`) avant d'écrire. Les portées viennent du tableau de `rapport-releve.md` ; « absente du relevé » = correspondance de précaution "
               f"(la phrase « {PREC} » va dans `src`).\n")
    out.append('\n\n'.join(bloc_code(c) for c in lot['codes']) + "\n")
    out.append("## Doubles comptes à examiner (à écrire dans `doubles_comptes`, règle « le plan gagne ; un objet physique n'est payé qu'une fois »)\n"
               "Tu ne tranches pas les quantités (équipe A) : tu SIGNALES, avec `codes` et `regle`, ceux de ces couples que tu juges réels après lecture de la feuille "
               "Détail et de `releve.xlsx` (et tu écris ceux que tu vois en plus). Un couple jugé non réel va en note avec la raison.\n"
               + '\n'.join(f"- [{a}, {b}] : {t}" for a, b, t in lot['doubles']) + "\n")
    out.append("## Squelette Python conseillé (tu peux l'adapter ; il élimine les fautes de frappe dans `p`, `h` et `src`)\n" + SQUELETTE + "\n")
    out.append(CONSIGNE_FIN.format(m=m, n=n))
    return '\n'.join(out).rstrip('\n') + '\n'


if __name__ == '__main__':
    for m in (1, 2, 3):
        texte = prompt(m)
        with open(SORTIE.format(m=m), 'w', encoding='utf-8') as f:
            f.write(texte)
        print(SORTIE.format(m=m), len(texte.split('\n')), 'lignes', len(texte), 'caractères')
