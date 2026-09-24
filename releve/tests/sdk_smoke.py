# /// script
# requires-python = ">=3.12"
# dependencies = ["claude-agent-sdk==0.2.154"]
# ///
import asyncio, json, os
from pathlib import Path
from claude_agent_sdk import query, ClaudeAgentOptions, ResultMessage, AssistantMessage, TextBlock

REPO = Path(__file__).resolve().parents[2]

async def main():
    opts = ClaudeAgentOptions(model="haiku", max_turns=1, cwd=str(REPO),
                              setting_sources=["project"], mcp_servers={}, strict_mcp_config=True, tools=[], allowed_tools=[])
    async for m in query(prompt="Réponds exactement: OK-SDK", options=opts):
        if isinstance(m, AssistantMessage):
            for b in m.content:
                if isinstance(b, TextBlock): print("TEXT:", b.text)
        if isinstance(m, ResultMessage):
            print(json.dumps({"subtype": m.subtype, "is_error": m.is_error, "cost": m.total_cost_usd, "session": m.session_id, "turns": m.num_turns}))
print("ANTHROPIC_API_KEY set:", bool(os.environ.get("ANTHROPIC_API_KEY")), "OAUTH_TOKEN set:", bool(os.environ.get("CLAUDE_CODE_OAUTH_TOKEN")))
asyncio.run(main())
