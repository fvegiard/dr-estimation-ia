import assert from 'node:assert/strict';
import test from 'node:test';
import { mkdtemp, mkdir, writeFile, rm } from 'node:fs/promises';
import { tmpdir } from 'node:os';
import { resolve } from 'node:path';
import { createHash } from 'node:crypto';
import { consolider } from '../outils/consolider_campagne_25.mjs';

async function fixture(t) {
  const base = await mkdtemp(resolve(tmpdir(), 'consolider-campagne-'));
  t.after(() => rm(base, { recursive: true, force: true }));
  await mkdir(resolve(base, 'preuves'));
  await writeFile(resolve(base, 'extrait.pdf'), 'fixture source');
  await writeFile(resolve(base, 'bibliotheque-blocs.csv'), 'fixture bibliotheque');
  await writeFile(resolve(base, 'manifest.json'), JSON.stringify({
    cas: [{ id: 'P99-TEST-E001', projet: 'TEST', feuille: 'E001',
      extrait: resolve(base, 'extrait.pdf'),
      extrait_sha256: createHash('sha256').update('fixture source').digest('hex') }],
  }));
  return base;
}

test('une campagne partielle distingue absence de preuve et absence de repères', async t => {
  const base = await fixture(t);
  const resultat = await consolider(base, base);
  assert.equal(resultat.bilan.en_attente, 1);
  assert.equal(resultat.cas[0].reperes, null);
  assert.equal(resultat.cas[0].produit, null);
  assert.equal(resultat.cas[0].extrait.conforme_manifeste, true);
  assert.deepEqual(resultat.cas[0].planches_controle, []);
});

test('une production false reste bloquée malgré exit0 et conserve les inconnues', async t => {
  const base = await fixture(t);
  await writeFile(resolve(base, 'preuves/P99-TEST-E001.json'), JSON.stringify({
    fermeture: { code: 0, signal: null },
    reponse: { structuredContent: { produit: false, raison: 'relevé non prêt',
      erreurs: ['aucune occurrence'], a_etiqueter: { inconnues: [{ n_plans: 7 }, { n_plans: 3 }] } } },
  }));
  const resultat = await consolider(base, base);
  assert.equal(resultat.bilan.bloques, 1);
  assert.equal(resultat.cas[0].succes_technique, false);
  assert.equal(resultat.cas[0].inconnues.occurrences, 10);
  assert.equal(resultat.cas[0].inconnues.signatures, 2);
  assert.deepEqual(resultat.cas[0].erreurs, ['aucune occurrence']);
  assert.match(resultat.cas[0].preuve.sha256, /^[a-f0-9]{64}$/);
});

test('les preuves JSON corrompues échouent explicitement', async t => {
  const base = await fixture(t);
  await writeFile(resolve(base, 'preuves/P99-TEST-E001.json'), '{invalide');
  await assert.rejects(consolider(base, base), SyntaxError);
});

test('le rendu et les artefacts produits sont relus, sans inventer de score visuel', async t => {
  const base = await fixture(t);
  const sortie = resolve(base, 'P99-TEST-E001/sortie');
  await mkdir(resolve(sortie, 'controle'), { recursive: true });
  await mkdir(resolve(sortie, 'png'));
  await writeFile(resolve(sortie, 'controle/E001-planche-01.png'), 'image de controle');
  await writeFile(resolve(sortie, 'png/BOM.csv'), 'quantite\n3\n');
  await writeFile(resolve(sortie, 'P99-TEST-E001-rendu-rapport.json'), JSON.stringify({
    reperes: 3, sheets: [{ sheet: 'E001', reperes: 3, box_in_free_space: true, box: [1, 2, 3, 4] }],
  }));
  await writeFile(resolve(base, 'preuves/P99-TEST-E001.json'), JSON.stringify({
    fermeture: { code: 0, signal: null },
    reponse: { structuredContent: { produit: true, bom_fichiers: ['BOM.csv'] } },
  }));
  const resultat = await consolider(base, base);
  assert.equal(resultat.bilan.produits, 1);
  assert.equal(resultat.bilan.reperes, 3);
  assert.equal(resultat.cas[0].score_visuel, null);
  assert.equal(resultat.cas[0].feuilles[0].box_in_free_space, true);
  assert.equal(resultat.cas[0].bom[0].present, true);
  assert.equal(resultat.cas[0].planches_controle.length, 1);
  assert.match(resultat.cas[0].planches_controle[0].sha256, /^[a-f0-9]{64}$/);
});
