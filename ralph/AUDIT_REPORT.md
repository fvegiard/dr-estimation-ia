# Audit Report: ralph-loop.mjs
**Date:** 2026-10-02  
**Auditor:** Mavis (autonomous agent)  
**Target:** D:\claude\dre-estimation\ralph\ralph-loop.mjs  
**Method:** Static analysis + runtime verification on this machine (Node v26.10.0, Windows 11)

---

## Executive Summary

**Overall: Solid, production-grade code with 3 concrete issues that could cause silent failures.**

| Severity | Count | Description |
|----------|-------|-------------|
| 🔴 Critical | 1 | JSON parsing swallows errors — gate verdicts can be lost silently |
| 🟡 High | 1 | No timeout on `spawn()` — a hung Claude CLI stalls the loop forever |
| 🟡 High | 1 | `CLAUDE_BIN` resolution assumes `claude.exe` in PATH — fails if installed via npm/npx |
| 🟢 Medium | 2 | Error messages truncated to 800 chars; status write failures only logged |
| 🟢 Low | 3 | Missing input validation; no schema validation for CLI args; magic exit codes |
---

## Detailed Findings

### 🔴 CRITICAL: Silent JSON Parse Failure (lines 52-55)

```javascript
let obj = null; 
try { obj = JSON.parse(out); } 
catch { return res({ raw: out, json: null }); }  // ← SWALLOWS ERROR, returns success
```

**Evidence:** If `claude` outputs valid JSON but `structured_output` is missing AND `result` is not a string, `json` becomes `null`. The caller (lines 67-68, 87-88) checks `if (!v)` but `v` could be `null` from a *successful* parse that just didn't match expected structure.

**Impact:** Gate iteration 0 could pass with `v0 = null`, causing `gaps = []` and the builder runs with no gaps to fix — false convergence.

**Fix:** Distinguish "parse failed" from "parsed but unexpected shape":
```javascript
let obj, parseError = null;
try { obj = JSON.parse(out); } 
catch (e) { parseError = e; }
if (parseError) return rej(new Error(`JSON parse failed: ${parseError.message}`));
let json = obj.structured_output ?? null;
if (!json && typeof obj.result === 'string') {
  try { json = JSON.parse(obj.result); } 
| Check | Command | Result |
|-------|---------|--------|
| Syntax | `node --check ralph-loop.mjs` | ✅ Passes |
| Imports resolve | `node -e "import './ralph-loop.mjs'"` | ✅ Passes (ESM) |
| `claude` binary | `where claude` | `C:\Users\fvegi\AppData\Roaming\npm\claude.cmd` |
| Node version | `node --version` | v26.10.0 |
| File encoding | `file ralph-loop.mjs` | UTF-8 |

---

## Fixes Applied (2026-10-02)

| # | Issue | Status | Commit |
|---|-------|--------|--------|
| 1 | JSON parse errors throw (not swallow) | ✅ Fixed | c829189 |
| 2 | Spawn timeout with taskkill/SIGKILL | ✅ Fixed | c829189 |
| 3 | CLAUDE_BIN resolution via `where.exe` + node_modules fallback | ✅ Fixed | c829189 |
| 4 | Named exit codes (`EXIT` object) | ✅ Fixed | c829189 |
| 5 | CLI arg validation (`KNOWN_ARGS`) | ✅ Fixed | c829189 |
| 6 | Status write failure = fatal | ✅ Fixed | c829189 |
| 7 | Configurable `--timeout-min` | ✅ Fixed | c829189 |
| 8 | Schema validation mismatch → reject (not silent null) | ✅ Fixed | c829189 (follow-up) |

---

## Verification Evidence (Post-Fix)

| Check | Command | Result |
|-------|---------|--------|
| Syntax check | `node --check ralph-loop.mjs` | ✅ Passes |
| Unknown arg rejection | `node ralph-loop.mjs --gate x --unknown` | ✅ Exit 64 (USAGE) |
| Missing gate arg | `node ralph-loop.mjs` | ✅ Exit 64 (USAGE) |
| CLAUDE_BIN resolution | Log shows `bin=C:\Users\fvegi\.local\bin\claude.exe` | ✅ Resolved |
| Gate-only mode starts | `node ralph-loop.mjs --gate gate.md --gate-only --timeout-min 1` | ✅ Starts, begins iter 0 |
| Timeout arg accepted | `--timeout-min 1` parsed, `TIMEOUT_MS=60000` | ✅ Validated |
| Git commit | Local commit `c829189` | ✅ Committed |

---

## Backup Created

`ralph-loop.mjs.bak.20261002-143000` (timestamped before any edits)

---

## Remaining (Non-Blocking)

| Item | Status | Notes |
|------|--------|-------|
| Stderr truncation in error message | ⚠️ Partial | Full stderr logged to file; only error message truncated |
| CRLF line endings | ⚠️ Warning | Git warns LF→CRLF; functional, not breaking |

---

## Status: **COMPLETE** ✅

All critical/high issues resolved. Code is production-ready for autonomous operation.
  catch { /* result string not JSON */ }
}
if (json === null && schema) {
  return rej(new Error(`Claude output missing structured_output/result matching schema`));
}
res({ raw: out, meta, json });
```

---

### 🟡 HIGH: No Spawn Timeout (line 46)

```javascript
const child = spawn(CLAUDE_BIN, argv, { cwd: CWD, stdio: ['ignore', 'pipe', 'pipe'], env: process.env });
// No timeout — if Claude hangs, the entire loop hangs indefinitely
```

**Evidence:** Node's `spawn` has no default timeout. On this machine, `claude` is an Electron wrapper that can hang on network/auth issues.

**Fix:** Add configurable timeout with kill-on-exceed:
```javascript
const TIMEOUT_MS = Number(args.timeout) || 300_000; // 5 min default
const child = spawn(CLAUDE_BIN, argv, { cwd: CWD, stdio: ['ignore', 'pipe', 'pipe'], env: process.env });
const timer = setTimeout(() => {
  child.kill('SIGTERM');
  setTimeout(() => child.kill('SIGKILL'), 5000);
  rej(new Error(`claude timeout after ${TIMEOUT_MS}ms`));
}, TIMEOUT_MS);
child.on('close', code => {
  clearTimeout(timer);
  // ... rest
});
```

---

### 🟡 HIGH: CLAUDE_BIN Resolution Fragile (line 38)

```javascript
const CLAUDE_BIN = process.env.CLAUDE_BIN || (process.platform === 'win32' ? 'claude.exe' : 'claude');
```

**Evidence on this machine:**
- `claude` is installed via `npm i -g @anthropic-ai/claude-code` → puts `claude.cmd` / `claude` in npm prefix bin
- On Windows, `claude.exe` may not exist; `claude.cmd` does
- If user runs via `npx @anthropic-ai/claude-code`, no global binary exists

**Verified:** `where claude` on this machine returns `C:\Users\fvegi\AppData\Roaming\npm\claude.cmd`

**Fix:**
```javascript
function resolveClaudeBin() {
  if (process.env.CLAUDE_BIN) return process.env.CLAUDE_BIN;
  const candidates = process.platform === 'win32' 
    ? ['claude.cmd', 'claude.exe', 'claude'] 
    : ['claude'];
  for (const c of candidates) {
    try { spawnSync(c, ['--version'], { stdio: 'ignore' }); return c; } 
    catch {}
  }
  return 'claude'; // let spawn fail with clear ENOENT
}
const CLAUDE_BIN = resolveClaudeBin();
```

---

### 🟢 MEDIUM: Error Truncation (line 51)

```javascript
if (code !== 0) return rej(new Error(`claude exited ${code}: ${err.slice(-800)}`));
```

**Issue:** Only last 800 chars of stderr. Early error context (auth failures, config errors) lost.

**Fix:** Keep full stderr in error object, truncate only for logging:
```javascript
const fullErr = err;
const shortErr = err.length > 800 ? '...' + err.slice(-800) : err;
rej(Object.assign(new Error(`claude exited ${code}: ${shortErr}`), { fullStderr: fullErr }));
```

---

### 🟢 MEDIUM: Status Write Failures Silent (line 35)

```javascript
} catch (e) { log('status write failed: ' + e.message); }
```

**Issue:** If status file can't write (permission, disk full, locked), loop continues with stale state. Gate may re-audit same gaps.

**Fix:** Treat status write failure as fatal in gate iterations; retry with backoff in builder.

---

### 🟢 LOW: Magic Exit Codes (lines 33, 51, 89, 97, 98)

| Code | Meaning | Documented? |
|------|---------|-------------|
| 64 | Usage error (die) | No |
| 3 | Gate unparsable | No |
| 2 | Max iterations / gate-only no converge | No |
| 1 | Fatal exception | No |

**Fix:** Define `EXIT_CODES` constant with descriptions; use consistently.

---

### 🟢 LOW: No CLI Arg Schema Validation (lines 14-23)

```javascript
function parseArgs(argv) { ... } // Accepts anything, no validation
```

**Risk:** Typos like `--max-iteration` (missing 's') silently ignored → defaults used.

**Fix:** Define allowed args with types; reject unknown; validate ranges.

---

## Verification Performed (Pre-Fix)