#!/usr/bin/env node
// ralph-loop.mjs — Ralph loop driving the official claude-code CLI (npm @anthropic-ai/claude-code)
// in autonomous full-agentic mode, with an adversarial quality gate as backpressure.
// Semantics follow the official ralph-wiggum plugin (anthropics/claude-code): --max-iterations, --completion-promise.
// Dev inspection: DEV_INSPECT=1 node ralph-loop.mjs ... (re-execs with --inspect) | CLI debug: --verbose, --debug-file <path>
import { spawn, spawnSync } from 'node:child_process';
import { readFileSync, writeFileSync, appendFileSync, mkdirSync } from 'node:fs';
import { resolve, dirname } from 'node:path';

if (process.env.DEV_INSPECT === '1' && !process.execArgv.some(a => a.startsWith('--inspect'))) {
  const r = spawnSync(process.execPath, ['--inspect', ...process.argv.slice(1)], { stdio: 'inherit', env: { ...process.env, DEV_INSPECT: '0' } });
  process.exit(r.status ?? 1);
}
function parseArgs(argv) { const o = {}; for (let i = 0; i < argv.length; i++) { const a = argv[i]; if (!a.startsWith('--')) continue; const k = a.slice(2); const n = argv[i + 1]; if (n === undefined || n.startsWith('--')) o[k] = true; else { o[k] = n; i++; } } return o; }
const args = parseArgs(process.argv.slice(2));
const CWD = resolve(args.cwd || process.cwd());
const MAX = Number(args['max-iterations'] || 3);
const PROMISE = String(args['completion-promise'] || 'CONFORME_CLOSEABLE');
const STATUS = args.status ? resolve(args.status) : resolve(CWD, 'ralph-status.json');
const LOG = args.log ? resolve(args.log) : resolve(CWD, 'ralph.log');
const GATE_ONLY = !!args['gate-only'];
if (!args.gate) die('missing --gate <file>');
if (!GATE_ONLY && !args.prompt) die('missing --prompt <file> (or use --gate-only)');

const GATE_SCHEMA = { type: 'object', properties: {
  verdict: { type: 'string' }, conforme_closeable: { type: 'boolean' },
  closeable_gaps: { type: 'array', items: { type: 'object', properties: { id: { type: 'string' }, desc: { type: 'string' }, fix: { type: 'string' } }, required: ['id', 'desc', 'fix'] } },
  blocked_gaps: { type: 'array', items: { type: 'object', properties: { id: { type: 'string' }, desc: { type: 'string' }, reason: { type: 'string' } }, required: ['id', 'desc', 'reason'] } },
  evidence: { type: 'string' } }, required: ['verdict', 'conforme_closeable', 'closeable_gaps', 'blocked_gaps'] };

function ts() { return new Date().toISOString(); }
function log(msg) { const line = `[${ts()}] ${msg}`; console.log(line); try { appendFileSync(LOG, line + '\n'); } catch {} }
function die(msg) { console.error('ralph-loop: ' + msg); process.exit(64); }
let state = { iteration: 0, maxIter: MAX, phase: 'init', verdict: null, conforme_closeable: false, closeable: [], blocked: [], steps: [], updatedAt: ts() };
function status(patch) { state = { ...state, ...patch, updatedAt: ts() }; try { mkdirSync(dirname(STATUS), { recursive: true }); writeFileSync(STATUS, JSON.stringify(state, null, 2)); } catch (e) { log('status write failed: ' + e.message); } }
function step(label, st, note) { state.steps.push({ label, status: st, note }); }

const CLAUDE_BIN = process.env.CLAUDE_BIN || (process.platform === 'win32' ? 'claude.exe' : 'claude');
function runClaude(prompt, { schema, model } = {}) {
  const argv = ['-p', prompt, '--dangerously-skip-permissions', '--output-format', 'json'];
  if (schema) argv.push('--json-schema', JSON.stringify(schema));
  if (model) argv.push('--model', String(model));
  if (args.verbose) argv.push('--verbose');
  if (args['debug-file']) argv.push('--debug-file', resolve(args['debug-file']));
  return new Promise((res, rej) => {
    const child = spawn(CLAUDE_BIN, argv, { cwd: CWD, stdio: ['ignore', 'pipe', 'pipe'], env: process.env });
    let out = '', err = '';
    child.stdout.on('data', d => out += d); child.stderr.on('data', d => err += d);
    child.on('error', rej);
    child.on('close', code => {
      if (code !== 0) return rej(new Error(`claude exited ${code}: ${err.slice(-800)}`));
      let obj = null; try { obj = JSON.parse(out); } catch { return res({ raw: out, json: null }); }
      let json = obj.structured_output ?? null;
      if (!json && typeof obj.result === 'string') { try { json = JSON.parse(obj.result); } catch {} }
      res({ raw: out, meta: { cost_usd: obj.total_cost_usd, turns: obj.num_turns, duration_ms: obj.duration_ms }, json });
    });
  });
}

(async () => {
  mkdirSync(CWD, { recursive: true });
  log(`ralph-loop start cwd=${CWD} max=${MAX} promise=${PROMISE} gateOnly=${GATE_ONLY} bin=${CLAUDE_BIN}`);
  const gatePrompt = readFileSync(resolve(args.gate), 'utf8');
  let gaps = [];
  if (args['gate-first'] && !GATE_ONLY) {
    status({ iteration: 0, phase: 'gate iter 0 (initial audit)' }); log('iter 0: gate (initial audit)');
    const g0 = await runClaude(gatePrompt, { schema: GATE_SCHEMA, model: args['gate-model'] || 'opus' });
    const v0 = g0.json;
    if (v0) {
      step('Gate iter 0', 'done', `${v0.verdict} · fermables=${v0.closeable_gaps.length} · bloques=${v0.blocked_gaps.length}`);
      status({ verdict: v0.verdict, conforme_closeable: !!v0.conforme_closeable, closeable: v0.closeable_gaps, blocked: v0.blocked_gaps });
      log(`iter 0: verdict=${v0.verdict} fermables=${v0.closeable_gaps.length} bloques=${v0.blocked_gaps.length}`);
      if (v0.conforme_closeable === true || String(v0.verdict || '').includes(PROMISE)) { log('already conforme - stop'); status({ phase: 'done', converged: true }); process.exit(0); }
      gaps = v0.closeable_gaps;
    }
  }
  for (let i = GATE_ONLY ? 0 : 1; i <= MAX; i++) {
    if (!GATE_ONLY) {
      status({ iteration: i, phase: `builder iter ${i}` });
      const base = readFileSync(resolve(args.prompt), 'utf8');
      const prompt = gaps.length ? `${base}\n\nECARTS FERMABLES A TRAITER (du gate precedent):\n${JSON.stringify(gaps, null, 2)}` : base;
      log(`iter ${i}: builder`);
      const b = await runClaude(prompt, { model: args.model });
      step(`Builder iter ${i}`, 'done', b.meta ? `${b.meta.turns} tours · ${b.meta.cost_usd?.toFixed?.(3)} $` : undefined);
    }
    status({ iteration: i, phase: `gate iter ${i}` }); log(`iter ${i}: gate`);
    const g = await runClaude(gatePrompt, { schema: GATE_SCHEMA, model: args['gate-model'] || 'opus' });
    const v = g.json;
    if (!v) { step(`Gate iter ${i}`, 'done', 'verdict non parsable'); status({ phase: 'gate-unparsable' }); log('gate returned no structured verdict; raw tail: ' + g.raw.slice(-300)); process.exit(3); }
    const ok = v.conforme_closeable === true || String(v.verdict || '').includes(PROMISE);
    step(`Gate iter ${i}`, 'done', `${v.verdict} · fermables=${v.closeable_gaps.length} · bloques=${v.blocked_gaps.length}`);
    status({ verdict: v.verdict, conforme_closeable: !!v.conforme_closeable, closeable: v.closeable_gaps, blocked: v.blocked_gaps, phase: ok ? 'done' : `gaps after iter ${i}` });
    log(`iter ${i}: verdict=${v.verdict} fermables=${v.closeable_gaps.length} bloques=${v.blocked_gaps.length}`);
    if (ok) { log(`completion promise reached (${PROMISE}) - stop`); status({ phase: 'done', converged: true }); process.exit(0); }
    gaps = v.closeable_gaps;
    if (GATE_ONLY) { status({ phase: 'done', converged: false }); process.exit(2); }
  }
  log(`max-iterations (${MAX}) reached without promise`); status({ phase: 'max-iterations', converged: false }); process.exit(2);
})().catch(e => { log('fatal: ' + e.message); status({ phase: 'error', error: e.message }); process.exit(1); });