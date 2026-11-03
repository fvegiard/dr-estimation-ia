// Chromium sans tête avec port de débogage CDP sur le premier port libre à partir de 9223 (jamais 9222).
// Usage : node outils/cdp.ts   → affiche le port et l'URL WebSocket, Chromium reste ouvert (Ctrl+C pour fermer).
import { spawn } from 'node:child_process';
import { createServer } from 'node:net';
import { fileURLToPath } from 'node:url';
import { resolve } from 'node:path';

export function portLibre(depart = 9223, hote = '127.0.0.1'): Promise<number> {
  return new Promise((ok, echec) => {
    const s = createServer();
    s.once('error', (e: NodeJS.ErrnoException) => (e.code === 'EADDRINUSE' || e.code === 'EACCES') && depart < 65535
      ? portLibre(depart + 1, hote).then(ok, echec) : echec(e));
    s.listen(depart, hote, () => s.close(() => ok(depart)));
  });
}

if (process.argv[1] && resolve(process.argv[1]) === fileURLToPath(import.meta.url)) {
  const port = await portLibre();
  const chrome = process.env.CHROME_PATH ?? '/opt/pw-browsers/chromium';
  const enfant = spawn(chrome, ['--headless', '--no-sandbox', `--remote-debugging-port=${port}`,
    '--remote-debugging-address=127.0.0.1', 'about:blank'], { stdio: 'ignore' });
  enfant.once('error', (e: Error) => { console.error(`Chromium introuvable (${chrome}) : ${e.message}`); process.exit(1); });
  for (let i = 0; i < 50; i++) {
    try {
      const v = await (await fetch(`http://127.0.0.1:${port}/json/version`)).json() as
        { webSocketDebuggerUrl: string; Browser: string };
      console.log(JSON.stringify({ port, ws: v.webSocketDebuggerUrl, navigateur: v.Browser }));
      break;
    } catch { await new Promise(r => setTimeout(r, 200)); }
  }
}
