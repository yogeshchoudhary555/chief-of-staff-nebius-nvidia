# Best Use of Tavily — prize brief ($3,000, stackable with Grand Prize)

**Official requirement** (hackathon info pack): "Must make a functional, runtime API call to the Tavily Search API as an integral part of the solution (e.g. live search grounding, deep research, web browsing)." Context: Nebius acquired Tavily (Feb 2026) — this is a Nebius-family prize judged by Tavily's own FDEs. They will spot fakes instantly.

## (a) Winning patterns (from actual Tavily-prize winners)

1. **Tavily in 2+ pipeline stages, never one decorative call.** Basket — *Best Use of Tavily Search, 1st place, Multiagents Hackathon London 2026* — ran Tavily in two of five agents: Agent 1 (Date-Finder: finds when a product was reformulated, from a name alone) and Agent 2 (Retrieval: complaint mentions across news + web). Their README states the winning logic: Tavily is "what makes it a real web agent acting on live data, not a script over a static file." **We match this:** Tavily drives both the rental-hunt pipeline AND the morning briefing — show both in the video.
2. **Search → Extract two-step, named on camera.** `search` (advanced depth) for discovery, then `extract` for full clean text of top URLs. One hackathon team noted their Tavily judge "literally wrote the 'Search vs Extract' guide — she will recognize best-practice usage immediately."
3. **Cited output — every claim traceable to a live source.** Basket's publisher emits a sourced alert where each claim links back to its URL. Judges cannot verify "live" unless live sources are visible.
4. **A question the model cannot answer without the live web.** Basket validated a dated, checkable demo target (Reese's cups recipe change, Feb 2026). HackNation's prize definition: "leverages Tavily's APIs in a creative **and impactful** way" — both words matter. Ours: *today's* rental listings in Sri Ganganagar — the model cannot know them; only live search can.
5. **Visible proof of liveness.** Timestamps, a "live" badge on the search step, real URLs rendered in the UI — not flashed, scrolled.

## (b) What the demo video must SHOW and SAY

**SHOW on screen:**
- The step chain with a visible `tavily_search — 5 result(s) · live` badge (already in UI).
- Real listing titles/URLs from the live search — scroll them slowly, don't flash.
- Before/after: briefing WITHOUT Tavily data (generic) vs WITH it (live-grounded).
- Proof the key is live (badge reads LIVE / source "tavily-live", never mock).

**SAY aloud (non-negotiable):**
- Moment 1: *"Live web search via Tavily — real listings, right now. Without Tavily this answer is impossible — the model can't know today's rentals."*
- Name the method: *"Tavily searches the live web, then extracts the full listing text — that's the research pipeline."*

## (c) Red flags to avoid

1. **Mocked or stale results** — the #1 suspicion. Never show cached/hardcoded listings. If the API fails on recording day, re-record; don't fake.
2. **One bolted-on search call** — a single `tavily_search` inside an otherwise static chatbot reads as decoration. Show it in BOTH the rental hunt and the briefing.
3. **Results never displayed** — if the video never shows what Tavily returned, judges assume it's mocked.
4. **No spoken sponsor line** — sponsor prizes are won partly by naming the sponsor's value on camera. The "without Tavily this answer is impossible" line stays.
5. **A fallback that could mask a dead key** — verify Tavily is live immediately before recording; the video must not be able to pass with a dead key.
6. **Missing README section** — rules require "How we used Tavily" in the README (already added — keep it).

*Gap: no public judging-criteria statements found from Evan Rimer or Ricky Johnson — do not quote them.*
