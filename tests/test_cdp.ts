import assert from 'node:assert/strict';
import test from 'node:test';
import { createServer } from 'node:net';
import { portLibre } from '../outils/cdp.ts';

test('CDP : jamais 9222; port occupé → le suivant libre', async () => {
  const p = await portLibre();
  assert.ok(p >= 9223);
  const occupe = createServer();
  await new Promise<void>(r => occupe.listen(p, '127.0.0.1', r));
  try { assert.ok(await portLibre(p) > p); }
  finally { await new Promise<void>(r => occupe.close(() => r())); }
});
