import assert from 'node:assert/strict';
import test from 'node:test';
import { contenuReponse, preuveReussie, selectionner } from '../outils/executer_campagne_25.mjs';

function preuve(produit) {
  return {
    reponse: { content: [{ type: 'text', text: JSON.stringify({ produit }) }], isError: false },
    fermeture: { code: 0, signal: null },
  };
}

test('une fermeture réussie ne valide jamais un relevé non produit', () => {
  assert.equal(preuveReussie(preuve(false)), false);
  assert.equal(preuveReussie(preuve(true)), true);
  assert.equal(preuveReussie(preuve('true')), false);
});

test('les erreurs du processus et de l’outil bloquent le succès', () => {
  assert.equal(preuveReussie({ ...preuve(true), erreur: 'délai dépassé' }), false);
  assert.equal(preuveReussie({ ...preuve(true), erreur_outil: true }), false);
  assert.equal(preuveReussie({ ...preuve(true), fermeture: { code: 1 } }), false);
  assert.equal(preuveReussie({ ...preuve(true), fermeture: { code: 0, signal: 'SIGTERM' } }), false);
  const erreur = preuve(true);
  erreur.reponse.isError = true;
  assert.equal(preuveReussie(erreur), false);
});

test('les réponses structurées sont reconnues et les JSON invalides signalés', () => {
  assert.equal(preuveReussie({
    reponse: { structuredContent: { produit: true } }, fermeture: { code: 0 },
  }), true);
  assert.equal(contenuReponse(undefined), null);
  assert.throws(() => contenuReponse({ content: [{ type: 'text', text: '{ invalide' }] }), SyntaxError);
});

test('sélection complète ou courte sans doublons; identifiant inconnu refusé', () => {
  const cas = [{ id: 'P01-BOURASSA-E-002' }, { id: 'P02-BOURASSA-E-101' }];
  assert.deepEqual(selectionner(cas, []), cas);
  assert.deepEqual(selectionner(cas, ['P01']), [cas[0]]);
  assert.deepEqual(selectionner(cas, [cas[1].id, 'P02']), [cas[1]]);
  assert.throws(() => selectionner(cas, ['P99']), /Sélection inconnue/);
});
