// Client JSON-RPC réel : chaque cas passe par un processus MCP stdio isolé.
import { spawn } from 'node:child_process';
import { createInterface } from 'node:readline';
import { readFile, writeFile, mkdir, rename, open, unlink } from 'node:fs/promises';
import { resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

const racine = resolve(fileURLToPath(new URL('..', import.meta.url)));
const base = resolve(racine, 'travail-mcp/campagne-25-plans');
const python = resolve(racine, '.venv/Scripts/python.exe');

export function contenuReponse(reponse) {
  if (reponse?.structuredContent) return reponse.structuredContent;
  const texte = reponse?.content?.filter(c => c.type === 'text').map(c => c.text).join('\n');
  return texte ? JSON.parse(texte) : null;
}

export function preuveReussie(preuve) {
  if (preuve.erreur || preuve.erreur_outil || preuve.reponse?.isError ||
      preuve.fermeture?.code !== 0 || preuve.fermeture?.signal) return false;
  return contenuReponse(preuve.reponse)?.produit === true;
}

export function selectionner(cas, selection) {
  const inconnus = selection.filter(id => !cas.some(c => c.id === id || c.id.split('-')[0] === id));
  if (inconnus.length) throw new Error(`Sélection inconnue : ${inconnus.join(', ')}`);
  return cas.filter(c => !selection.length || selection.includes(c.id) ||
    selection.includes(c.id.split('-')[0]));
}

async function lirePreuve(chemin) {
  try { return JSON.parse(await readFile(chemin, 'utf8')); }
  catch (erreur) {
    if (erreur.code === 'ENOENT') return null;
    throw new Error(`Preuve illisible, conservée sans modification : ${chemin}`, { cause: erreur });
  }
}

async function traiter(cas) {
  const debut = Date.now();
  const enfant = spawn(python, ['-m', 'serveur_mcp'], {
    cwd: racine, shell: false, windowsHide: true,
    env: { ...process.env, PYTHONUTF8: '1', PYTHONIOENCODING: 'utf-8',
      ESTIMATEUR_BASE: base, ESTIMATEUR_BIBLIOTHEQUE: resolve(base, 'bibliotheque-blocs.csv') },
    stdio: ['pipe', 'pipe', 'pipe'],
  });
  let identifiant = 0;
  let stderr = '';
  const attente = new Map();
  const echanges = [];
  const lignes = createInterface({ input: enfant.stdout });
  enfant.stderr.setEncoding('utf8');
  enfant.stderr.on('data', chunk => { stderr += chunk; });
  enfant.stdin.on('error', erreur => { rejeter(erreur); });
  function rejeter(erreur) {
    for (const a of attente.values()) { clearTimeout(a.timer); a.reject(erreur); }
    attente.clear();
  }
  const fermeture = new Promise((resolveExit, rejectExit) => {
    enfant.once('error', erreur => { rejeter(erreur); rejectExit(erreur); });
    enfant.once('close', (code, signal) => {
      rejeter(new Error(`Serveur fermé prématurément : ${code}, ${signal}`));
      resolveExit({ code, signal });
    });
  });
  // Évite une promesse rejetée non observée pendant un appel RPC.
  fermeture.catch(erreur => { stderr += `Erreur de processus : ${erreur.stack}\n`; });
  lignes.on('line', ligne => {
    let message;
    try { message = JSON.parse(ligne); }
    catch (erreur) { rejeter(new Error(`Sortie MCP non JSON : ${ligne}`, { cause: erreur })); return; }
    echanges.push({ reception: message });
    const a = attente.get(message.id);
    if (!a) return;
    clearTimeout(a.timer);
    attente.delete(message.id);
    if (message.error) a.reject(new Error(JSON.stringify(message.error)));
    else a.resolve(message.result);
  });
  function envoyer(message) {
    echanges.push({ envoi: message });
    enfant.stdin.write(`${JSON.stringify(message)}\n`);
  }
  function demander(method, params) {
    const id = ++identifiant;
    return new Promise((resolveRpc, reject) => {
      const timer = setTimeout(() => {
        attente.delete(id);
        reject(new Error(`Délai dépassé pour ${method}`));
      }, 30 * 60 * 1000);
      attente.set(id, { resolve: resolveRpc, reject, timer });
      envoyer({ jsonrpc: '2.0', id, method, params });
    });
  }
  const preuve = { id: cas.id, debut: new Date(debut).toISOString() };
  try {
    preuve.initialisation = await demander('initialize', {
      protocolVersion: '2025-06-18', capabilities: {},
      clientInfo: { name: 'assurance-25-plans', version: '1.0' },
    });
    if (preuve.initialisation.serverInfo?.name !== 'expert-estimateur')
      throw new Error('Identité du serveur inattendue');
    envoyer({ jsonrpc: '2.0', method: 'notifications/initialized' });
    const retour = await demander('tools/call', {
      name: 'relever_automatique', arguments: { dossier: cas.id, chemin_source: cas.extrait },
    });
    preuve.reponse = retour;
    preuve.erreur_outil = Boolean(retour.isError);
    preuve.produit = contenuReponse(retour)?.produit === true;
    if (!preuve.produit) preuve.echec_production = 'Le serveur ne confirme pas produit:true';
    enfant.stdin.end();
    const delaiFermeture = setTimeout(() => {
      preuve.erreur = 'Le serveur ne ferme pas après la fin de son entrée (30 secondes)';
      enfant.kill();
    }, 30_000);
    try { preuve.fermeture = await fermeture; }
    finally { clearTimeout(delaiFermeture); }
  } catch (erreur) {
    preuve.erreur = String(erreur.stack ?? erreur);
    enfant.kill();
    try { preuve.fermeture = await fermeture; }
    catch (erreurFermeture) {
      preuve.fermeture = { code: null, signal: null, erreur: String(erreurFermeture) };
    }
  } finally {
    lignes.close();
    preuve.duree_s = (Date.now() - debut) / 1000;
    preuve.stderr = stderr;
    await writeFile(resolve(base, 'preuves', `${cas.id}.json`),
      `${JSON.stringify(preuve, null, 2)}\n`, { flag: 'wx' });
    await writeFile(resolve(base, 'preuves', `${cas.id}-rpc.json`),
      `${JSON.stringify(echanges, null, 2)}\n`, { flag: 'wx' });
  }
  const contenu = preuve.reponse?.structuredContent ??
    preuve.reponse?.content?.filter(c => c.type === 'text').map(c => c.text).join('\n');
  console.log(JSON.stringify({ id: cas.id, duree_s: preuve.duree_s,
    fermeture: preuve.fermeture, erreur: preuve.erreur, erreur_outil: preuve.erreur_outil,
    resultat: typeof contenu === 'string' ? contenu.slice(0, 500) :
      JSON.stringify(contenu)?.slice(0, 500) }));
  return preuve;
}

async function main() {
  const argumentsCli = process.argv.slice(2);
  const reprendreEchecs = argumentsCli.includes('--reprendre-echecs');
  const selection = argumentsCli.filter(arg => arg !== '--reprendre-echecs');
  const manifeste = JSON.parse(await readFile(resolve(base, 'manifest.json'), 'utf8'));
  const casSelectionnes = selectionner(manifeste.cas, selection);
  if (!casSelectionnes.length) throw new Error('Aucun cas à exécuter');
  await mkdir(resolve(base, 'preuves'), { recursive: true });
  const resultats = [];
  for (const cas of casSelectionnes) {
    const cheminVerrou = resolve(base, 'preuves', `${cas.id}.lock`);
    const verrou = await open(cheminVerrou, 'wx');
    try {
      await verrou.writeFile(`${JSON.stringify({ pid: process.pid, debut: new Date().toISOString() })}\n`);
      const chemin = resolve(base, 'preuves', `${cas.id}.json`);
      const existante = await lirePreuve(chemin);
      if (existante && (preuveReussie(existante) || !reprendreEchecs)) {
        console.log(JSON.stringify({ id: cas.id, conserve: true,
          succes: preuveReussie(existante), raison: 'Preuve existante conservée' }));
        resultats.push(existante);
        continue;
      }
      if (existante) {
        const archive = resolve(base, 'preuves', 'historique',
          `${cas.id}-${new Date().toISOString().replaceAll(':', '-')}`);
        await mkdir(archive, { recursive: true });
        await rename(chemin, resolve(archive, `${cas.id}.json`));
        try {
          await rename(resolve(base, 'preuves', `${cas.id}-rpc.json`),
            resolve(archive, `${cas.id}-rpc.json`));
        } catch (erreur) {
          if (erreur.code !== 'ENOENT') throw erreur;
          console.error(`${cas.id} : ancien journal RPC absent; preuve archivée dans ${archive}`);
        }
        console.log(JSON.stringify({ id: cas.id, reprise_echec: true, archive }));
      }
      console.log(JSON.stringify({ id: cas.id, demarrage: new Date().toISOString() }));
      resultats.push(await traiter(cas));
    } finally {
      await verrou.close();
      await unlink(cheminVerrou);
    }
  }
  process.exitCode = resultats.every(preuveReussie) ? 0 : 1;
}

if (process.argv[1] && resolve(process.argv[1]) === fileURLToPath(import.meta.url)) {
  await main();
}
