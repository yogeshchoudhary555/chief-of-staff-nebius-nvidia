# Demo script — judging video (≤ 3 minutes)

**Setup before recording:** `pip install -r requirements.txt && python app.py`
→ open http://localhost:8000. **Record with LIVE keys** (NEBIUS_API_KEY +
TAVILY_API_KEY via the vault provider — no mock mode). Judges may never run
the app; the video IS the submission. On-screen badge (top-right, whole
video): `Nemotron-3-Nano · Nebius Token Factory · LIVE`.

---

## 0:00–0:20 — The hook: the painful loop (20s)
Show the UI. Say: *"Every morning I lose 40 minutes to the same loop —
research the web, remember what matters, write the briefing. This is Chief of
Staff — a private personal AI that does it before I wake up. Persistent
memory, reusable skills, live web research — running on NVIDIA Nemotron,
served by Nebius Token Factory."*
(Lead with the loop + track fit, not architecture.)

## 0:20–1:00 — Moment 1: live research + dealer message (40s)
Click the **🏠 Hunt** button (deterministic pipeline: memory → live Tavily →
Nemotron draft → approval gate).
- Show the step chain: `1. memory_read — 0 fact(s) · 2. tavily_search — 5 result(s) · live · 3. nemotron_draft · 4. request_approval — waiting for your OK`.
- Say: *"Live web search via Tavily — real listings, right now. Without Tavily this answer is impossible — the model can't know today's rentals."* (one spoken
  Tavily line: required for the $3,000 Best Use of Tavily prize)
- Scroll the listing summary + drafted message.

## 1:00–1:20 — UPGRADE 1 · The trust beat: it never sends without your OK (20s)
- The drafted message sits in a **pending-approval state** — show it waiting.
- Say: *"And it never sends anything without my OK. A personal AI that acts
  on your life has to be stoppable — that's the whole point of keeping your
  data under your control."*
- Click **Approve** (or leave pending — either way the gate is visible).

## 1:20–2:10 — UPGRADE 2 · Memory that compounds, not just stores (50s)
- First, click **Briefing** tab → show a GENERIC briefing (no memory yet).
- Say: *"Watch what changes once it knows me."*
- Type: **"remember my name is Yogesh and I prefer morning briefings at 8am"**
  → show `tools: memory_write` confirmation.
- **Restart the app on camera** (`Ctrl+C`, `python app.py` — sqlite persists).
- Type: **"what do you remember about me?"** → recalls facts; open the Memory
  tab (timestamps visible).
- Click **Briefing** again → now personalized (name + 8am framing).
- Say: *"Same briefing, twice. The second one is better because it remembered
  — memory that compounds, not a chat trick."*

## 2:10–2:50 — Moment 3: the always-on payoff (40s)
- Say: *"Every morning it reads what it knows about me, checks fresh news via
  Tavily, and tells me what to focus on — before I wake up."*
- Show the personalized briefing rendering (`tools: memory_read, tavily_search`).

## 2:50–3:00 — Close: one line on the sponsor tech (10s, REQUIRED audio)
*"Chief of Staff: private, always-on, yours. All reasoning on NVIDIA
Nemotron-3-Nano via Nebius Token Factory — no model hosting, no data leaving
my control. Built for the Personal AI track."*
Show the repo + `GET /api/health` returning the live provider status.

---

## Backup lines (if a judge asks)
- **Why Nemotron?** Fast, cheap, tool-calling + JSON reliable — ideal for an
  agentic loop; served serverless so there's no model hosting.
- **Privacy?** Memory is a local sqlite file; keys live only in the vault.
- **What would you add next?** Voice input, scheduled briefings (cron), and a
  reminders tool backed by the same memory store.

## Recording checklist (from winning-patterns.md)
- [ ] LIVE keys (no mock badge anywhere in the video)
- [ ] On-screen badge: Nemotron-3-Nano · Nebius Token Factory · LIVE
- [ ] Spoken Tavily line in Moment 1 + visible tavily_search badge
- [ ] Spoken Nemotron + Token Factory line in the close (required audio)
- [ ] 1080p, no terminal scroll marathons, total ≤ 3:00
