// Synthèse reproductible des preuves MCP et des livrables réellement présents.
import { createHash } from 'node:crypto';
import { readFile, readdir, mkdir, writeFile } from 'node:fs/promises';
import { resolve, relative } from 'node:path';
import { fileURLToPath } from 'node:url';
import { contenuReponse, preuveReussie } from './executer_campagne_25.mjs';

const racine = resolve(fileURLToPath(new URL('..', import.meta.url)));
const invariants = {
  'P01-BOURASSA-E-002.json': '137efcfc282b97fbc28136fe066478bb771a97302214b900160ca52cbe98aa25',
  'P01-BOURASSA-E-002-rpc.json': '0c017dd79a1c03d3cbcfb672b2c315cf77fbb0dc6be04ebd97b1da8d126d3cca',
  'P02-BOURASSA-E-101.json': 'cc468457a7d91ac9763605e33c4a544afd1debae64337391a1f4fc09f35116f0',
  'P02-BOURASSA-E-101-rpc.json': 'dbd69fbcd365081c40d7516a59a44c5fea5b592aff49e03e2516e51c45e1fa08',
};

async function lireOptionnel(chemin) {
  try { return await readFile(chemin); }
  catch (erreur) {
    if (erreur.code === 'ENOENT') return null;
    throw erreur;
  }
}

function sha256(contenu) {
  return createHash('sha256').update(contenu).digest('hex');
}

export async function consolider(base, depot = racine) {
  const cheminRelatif = chemin => relative(depot, chemin).replaceAll('\\', '/');
  async function artefact(chemin) {
    const contenu = await lireOptionnel(chemin);
    return { chemin: cheminRelatif(chemin), present: contenu !== null,
      sha256: contenu === null ? null : sha256(contenu),
      octets: contenu?.length ?? null };
  }
  async function images(dossier) {
    let fichiers;
    try { fichiers = await readdir(dossier); }
    catch (erreur) {
      if (erreur.code === 'ENOENT') return [];
      throw erreur;
    }
    return Promise.all(fichiers.filter(nom => nom.endsWith('.png')).sort()
      .map(nom => artefact(resolve(dossier, nom))));
  }
  const manifestChemin = resolve(base, 'manifest.json');
  const manifestOctets = await readFile(manifestChemin);
  const manifeste = JSON.parse(manifestOctets);
  const cas = [];
  for (const entree of manifeste.cas) {
    const preuveChemin = resolve(base, 'preuves', `${entree.id}.json`);
    const preuveOctets = await lireOptionnel(preuveChemin);
    const preuve = preuveOctets === null ? null : JSON.parse(preuveOctets);
    const contenu = preuve ? contenuReponse(preuve.reponse) : null;
    const preuveInfo = { chemin: cheminRelatif(preuveChemin), present: preuve !== null,
      sha256: preuveOctets === null ? null : sha256(preuveOctets) };
    const rpc = await artefact(resolve(base, 'preuves', `${entree.id}-rpc.json`));
    for (const [nom, info] of [[`${entree.id}.json`, preuveInfo], [`${entree.id}-rpc.json`, rpc]]) {
      if (invariants[nom] && info.sha256 !== invariants[nom]) {
        throw new Error(`Preuve initiale modifiée ou absente : ${nom}; attendu ${invariants[nom]}, observé ${info.sha256}`);
      }
    }
    const sortie = resolve(base, entree.id, 'sortie');
    const rapportChemin = resolve(sortie, `${entree.id}-rendu-rapport.json`);
    const rapportOctets = await lireOptionnel(rapportChemin);
    const rapport = rapportOctets === null ? null : JSON.parse(rapportOctets);
    const extrait = await artefact(entree.extrait);
    extrait.sha256_manifeste = entree.extrait_sha256;
    extrait.conforme_manifeste = extrait.sha256 === entree.extrait_sha256;
    const inconnues = contenu?.a_etiqueter?.inconnues ?? [];
    const ambigues = contenu?.a_etiqueter?.ambigues ?? [];
    const bom = await Promise.all((contenu?.bom_fichiers ?? [])
      .map(nom => artefact(resolve(sortie, 'png', nom))));
    const erreurs = [
      ...(contenu?.erreurs ?? []),
      ...(preuve?.erreur ? [preuve.erreur] : []),
      ...(preuve?.erreur_outil || preuve?.reponse?.isError ? ['Erreur outil MCP'] : []),
      ...(preuve && preuve.fermeture?.code !== 0 ? ['Fermeture du processus non réussie'] : []),
      ...(!extrait.conforme_manifeste ? ['Extrait absent ou empreinte différente du manifeste'] : []),
    ];
    cas.push({
      id: entree.id, plan: entree.projet, feuille: entree.feuille,
      source: { chemin: entree.source, page: entree.page_source,
        sha256_manifeste: entree.source_sha256, controle: 'empreinte initiale du manifeste' },
      extrait, preuve: preuveInfo, rpc,
      preuves_initiales_preservees: invariants[`${entree.id}.json`] ? true : null,
      debut: preuve?.debut ?? null, duree_s: preuve?.duree_s ?? null,
      fermeture: preuve?.fermeture ?? null,
      produit: contenu?.produit ?? null,
      succes_technique: preuve ? preuveReussie(preuve) : false,
      statut: !preuve ? 'EN_ATTENTE' : preuveReussie(preuve) ? 'PRODUIT_A_VERIFIER' : 'BLOQUE',
      raison: contenu?.raison ?? null, erreurs,
      inconnues: { signatures: inconnues.length,
        occurrences: inconnues.reduce((total, sig) => total + (sig.n_plans ?? 0), 0) },
      ambigues: { signatures: ambigues.length },
      reperes: rapport?.reperes ?? contenu?.reperes ?? null,
      feuilles: rapport?.sheets ?? contenu?.feuilles ?? [],
      rapport_rendu: await artefact(rapportChemin),
      conformite_rendu: rapport?.conformite ?? null,
      pages: rapport?.pages ?? contenu?.pages ?? null,
      quantites: contenu?.quantites ? {
        represente: contenu.quantites.represente, total: contenu.quantites.total,
        lignes: contenu.quantites.lignes,
      } : null,
      bom, quantites_csv: await artefact(resolve(sortie, 'quantites.csv')),
      releve_pdf: await artefact(resolve(sortie, `${entree.id}-RELEVE.pdf`)),
      zip: await artefact(resolve(sortie, `${entree.id}-LIVRABLES-PNG.zip`)),
      planches_controle: await images(resolve(sortie, 'controle')),
      planches_signatures: await images(resolve(sortie, 'signatures')),
      score_visuel: null,
    });
  }
  return {
    genere_le: new Date().toISOString(),
    manifeste: { chemin: cheminRelatif(manifestChemin), sha256: sha256(manifestOctets) },
    bibliotheque: { ...await artefact(resolve(base, 'bibliotheque-blocs.csv')),
      sha256_manifeste: manifeste.bibliotheque_sha256 },
    limites: [
      'Une production MCP réussie ne constitue pas une acceptation visuelle ou métier.',
      'Les scores visuels restent à établir par inspection directe des images.',
      'Les empreintes des sources originales sont celles du manifeste; les extraits et livrables sont relus.',
    ],
    bilan: {
      plans: cas.length, preuves: cas.filter(c => c.preuve.present).length,
      produits: cas.filter(c => c.succes_technique).length,
      bloques: cas.filter(c => c.statut === 'BLOQUE').length,
      en_attente: cas.filter(c => c.statut === 'EN_ATTENTE').length,
      reperes: cas.reduce((total, c) => total + (c.reperes ?? 0), 0),
    },
    cas,
  };
}

if (process.argv[1] && resolve(process.argv[1]) === fileURLToPath(import.meta.url)) {
  const base = resolve(racine, 'travail-mcp/campagne-25-plans');
  const resultat = await consolider(base);
  const sortie = resolve(racine, 'docs/assurance-empirique-25-plans');
  await mkdir(sortie, { recursive: true });
  await writeFile(resolve(sortie, 'resultats.json'), `${JSON.stringify(resultat, null, 2)}\n`);
  console.log(JSON.stringify(resultat.bilan));
}
