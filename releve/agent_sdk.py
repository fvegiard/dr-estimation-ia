# /// script
# requires-python = ">=3.12"
# dependencies = ["claude-agent-sdk==0.2.154"]
# ///
"""Étape 2 : l'agent de relevé, lancé par le **Claude Agent SDK officiel** (PyPI `claude-agent-sdk` 0.2.154, publié le 2026-09-17),
authentifié par la connexion claude.ai (abonnement Max) déjà faite avec `claude auth login` dans WSL — aucune clé API.

Preuve d'authentification (2026-09-17, `_tmp/sdk_smoke.py`) : `ANTHROPIC_API_KEY` et `CLAUDE_CODE_OAUTH_TOKEN` absents, `query()` répond,
`ResultMessage.total_cost_usd` = 0.0326 $, session 2a08bde1-…  Le SDK lance le CLI Claude Code (`docs/code.claude.com_docs_en_agent-sdk_python.md`
L.825 `cli_path`, L.827 `add_dirs` → `--add-dir`, L.845 `setting_sources`), qui lit les identifiants OAuth du profil
(`docs/code.claude.com_docs_en_authentication.md` L.248-259 : `claude setup-token` → `CLAUDE_CODE_OAUTH_TOKEN` pour un poste sans
connexion interactive ; « This token authenticates with your Claude subscription and requires a Pro, Max, … plan »).

Usage : uv run releve/agent_sdk.py WORKDIR RESULTAT_JSON [--model opus] [--max-turns 800] [--budget-usd 0]
Écrit RESULTAT_JSON (mêmes champs que `claude -p --output-format json` : subtype, is_error, num_turns, total_cost_usd, usage, session_id, result)
et WORKDIR/agent-journal.log (chaque outil appelé, horodaté). Code de sortie 0 si subtype == success.
"""
from __future__ import annotations
import os, sys, json, asyncio, datetime, argparse
from claude_agent_sdk import query, ClaudeAgentOptions, ResultMessage, AssistantMessage, TextBlock, ToolUseBlock

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ALLOWED = ["Read", "Write", "Edit", "Glob", "Grep", "Bash(uv run releve/*)", "Bash(ls *)", "Bash(wc *)", "Bash(head *)", "Bash(sort *)", "Bash(cut *)", "Bash(cat *)"]

async def run(workdir, out_json, model, max_turns, budget):
    log = open(os.path.join(workdir, "agent-journal.log"), "a", encoding="utf-8")
    def j(msg):
        log.write(f"{datetime.datetime.now():%H:%M:%S} {msg}\n"); log.flush()
    opts = ClaudeAgentOptions(
        cwd=REPO, add_dirs=[workdir], setting_sources=["project"],      # charge .claude/skills/releve-planexpert du dépôt
        allowed_tools=ALLOWED, permission_mode="acceptEdits",
        model=model, max_turns=max_turns, max_budget_usd=(budget or None),
        mcp_servers={}, stderr=lambda s: j("stderr: " + s.rstrip()),
    )
    res, text = None, []
    j(f"début  modèle={model} max_turns={max_turns} workdir={workdir}")
    async for m in query(prompt=f"/releve-planexpert {workdir}", options=opts):
        if isinstance(m, AssistantMessage):
            for b in m.content:
                if isinstance(b, ToolUseBlock):
                    j(f"outil {b.name} {json.dumps(b.input, ensure_ascii=False)[:200]}")
                elif isinstance(b, TextBlock) and b.text.strip():
                    text.append(b.text); j("texte " + b.text.strip()[:200].replace("\n", " "))
        elif isinstance(m, ResultMessage):
            res = m
    if res is None:
        data = {"subtype": "aucun ResultMessage", "is_error": True, "result": "\n".join(text[-3:])}
    else:
        data = {"subtype": res.subtype, "is_error": res.is_error, "num_turns": res.num_turns, "session_id": res.session_id,
                "duration_ms": res.duration_ms, "duration_api_ms": res.duration_api_ms, "total_cost_usd": res.total_cost_usd,
                "usage": getattr(res, "usage", None), "stop_reason": getattr(res, "stop_reason", None),
                "result": getattr(res, "result", None) or "\n".join(text[-3:]), "lanceur": "claude-agent-sdk 0.2.154 (OAuth claude.ai)"}
    j(f"fin  subtype={data.get('subtype')} tours={data.get('num_turns')} coût={data.get('total_cost_usd')}")
    json.dump(data, open(out_json, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    print(json.dumps({k: data.get(k) for k in ("subtype", "num_turns", "total_cost_usd", "session_id")}))
    return 0 if data.get("subtype") == "success" else 1

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("workdir"); ap.add_argument("out_json")
    ap.add_argument("--model", default=os.environ.get("RELEVE_MODEL", "opus")); ap.add_argument("--max-turns", type=int, default=int(os.environ.get("RELEVE_MAX_TURNS", "800")))
    ap.add_argument("--budget-usd", type=float, default=float(os.environ.get("RELEVE_BUDGET_USD", "0")))
    a = ap.parse_args()
    sys.exit(asyncio.run(run(os.path.abspath(a.workdir), a.out_json, a.model, a.max_turns, a.budget_usd)))

if __name__ == "__main__":
    main()
