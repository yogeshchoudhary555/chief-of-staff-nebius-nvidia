# Chief of Staff — your always-on personal AI

Entry for the **Nebius × NVIDIA Global AI Hackathon** — **Personal AI track**.
An always-on, private personal agent that runs your day: it researches the live
web, remembers your facts across sessions, invokes reusable prompt-skills, and
generates a morning briefing.

## How it meets the hackathon requirements

- **Runs on Nebius Token Factory** — NVIDIA Nemotron via the OpenAI-compatible
  endpoint `https://api.tokenfactory.nebius.com/v1` (model
  `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, overridable via `NEMOTRON_MODEL`).
  This satisfies the "≥1 NVIDIA open model on Nebius" requirement.
- **Personal AI track** — private memory, daily briefing, proactive tool use.
- **Offline demo mode** — a mock LLM backend simulates the full tool-calling
  loop so judges can run the UI with zero keys.

## How we used NVIDIA Nemotron

Every line of agent reasoning runs on **NVIDIA Nemotron-3-Nano-30B-A3B**
(`nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`). The model drives the full agentic
loop in `agent.py`: it plans which tools to call, issues OpenAI-style function
calls (`tavily_search`, `memory_read`, `memory_write`, `request_approval`),
reads the tool observations, and composes the final user-facing reply. Nemotron
was chosen because its tool-calling is reliable enough for a multi-step loop
and it is fast/cheap enough to keep an always-on assistant economical. The demo
video shows the model ID in the UI badge and names it in the voiceover.

## Where Nebius Token Factory accelerated our workflow

- **Zero model hosting.** Token Factory's OpenAI-compatible serverless endpoint
  meant no GPU provisioning, no inference server to babysit — the agent calls
  `https://api.tokenfactory.nebius.com/v1/chat/completions` exactly like an
  OpenAI client (`llm.py`), so the whole build focused on agent behavior, not
  infrastructure. Idea to working agentic loop in a single day.
- **Instant model swap.** The namespaced model ID in one env var
  (`NEMOTRON_MODEL`) let us evaluate Nemotron variants from the Token Factory
  playground and drop the winner straight into the app with no code changes.
- **Live demo confidence.** Because inference is serverless and always warm,
  the ≤3-minute judging video was recorded against the LIVE endpoint (badge:
  `Nemotron-3-Nano · Nebius Token Factory · LIVE`) — no canned outputs.

## How we used Tavily (Best Use of Tavily)

The `tavily_search` tool (`tools.py`) fires a live Tavily search inside the
agent loop — e.g. the rental-hunt skill pulls current listings the model could
never know from training data. Without Tavily the pipeline collapses: no live
listings, no dealer draft, no briefing news. The demo video shows the live
search badge and names Tavily in the voiceover.

## Quickstart

```bash
cd nebius-nvidia-2026
pip install -r requirements.txt
cp .env.example .env        # optional; app runs without keys in demo mode
python app.py
# open http://localhost:8000
```

To go live: put `NEBIUS_API_KEY` (from https://dev.nebius.com/builders) and
`TAVILY_API_KEY` (from https://tavily.com) in `.env`. With no keys the app
automatically uses the offline mock backend — same UI, same tool loop.

## What it does

| Feature | How |
|---|---|
| Agent loop with tool calling | `agent.py` — plans, calls tools, responds (max 6 steps) |
| Web research | `tavily_search` tool (Tavily API) |
| Persistent memory | `memory.py` — sqlite at `data/memory.db`, survives restarts |
| Skills system | `skills/*.md` — reusable prompt-skills, auto-activated by keywords or `/skill <name>` |
| Morning briefing | Briefing panel auto-generates from memory + fresh news |
| Pluggable LLM | `llm.py` — `NebiusProvider` (Nemotron) / `MockProvider` (offline) |

## API

- `GET /` — single-page UI (chat + briefing + memory + skills)
- `POST /api/chat` — `{message, history}` → `{reply, tools_used, skill}`
- `GET /api/briefing` — morning briefing
- `GET /api/memory` — all remembered facts
- `POST /api/memory` — `{key, value}` save a fact
- `GET /api/skills` — loaded skills
- `GET /api/health` — active provider + key presence (booleans only, never values)

## Project structure

```
app.py            FastAPI app + single-page UI
agent.py          ChiefOfStaff agent loop
llm.py            Provider abstraction (Nebius Nemotron / mock)
tools.py          tavily_search + OpenAI function specs
memory.py         sqlite persistent memory
skills.py         markdown skill loader
config.py         env-var config (no secrets in code)
skills/           morning-briefing.md, rental-hunt.md
demo-script.md    ≤3-min judging video outline
```

## Notes

- Model IDs on Nebius are namespaced and case-sensitive — confirm the exact
  string in the Token Factory playground if the default 404s.
- Nemotron reasoning models may return answers in `reasoning_content`;
  `llm.py` falls back to it automatically.

## License

Apache-2.0 — see `LICENSE`.
