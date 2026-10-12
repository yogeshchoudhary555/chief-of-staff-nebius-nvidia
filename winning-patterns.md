# What wins AI-agent hackathons on Devpost — research 2026-10-12

Sources: UC Berkeley AI Hackathon 2025 grand-prize winners (ChipChat, Cameron);
CockroachDB × AWS "Build with Agentic Memory" winners recap (judge-written);
LifeOS build spec (direct Personal-AI-track competitor, this hackathon);
Pawnote hackathon README (entrant checklist, this hackathon).
Key rule facts verified from official Devpost page + competitor specs.

## The judging reality (this hackathon)

- 4 criteria, EQUALLY weighted: Technological Implementation, Design,
  Potential Impact, Quality of the Idea. Tie-break order: Implementation first.
- Stage 1 is pass/fail: does the project GENUINELY attempt the track's stated
  goal? Framing in the Devpost description must LEAD with track fit
  (always-on, private, persistent memory, skills) — not with the dashboard.
- **"Judges may judge only from the description, images, and video — they are
  not required to test the app."** The video + Devpost page ARE the submission.
- Prize stacking: one Overall award OR one Track award, PLUS one Bonus award.
  Realistic ceiling = Personal AI Track win + Best Use of Tavily ($3,000), or
  Overall placing + Tavily. The Tavily bonus needs only a functional runtime
  API call — $3,000 contested by far fewer entrants than the overall prizes.
- Sponsor tech must be LOAD-BEARING, not decorative: "Remove them and there is
  no project." Our inference runs on Nemotron via Token Factory — say so,
  show so.

## Top 5 winning patterns

### 1. A visceral, specific problem + personal story (all grand-prize winners)
ChipChat: "we struggled with circuits as undergrads" → prompt-to-manufacturing
pipeline. Cameron: "cameras stop at step one of observe-interpret-act."
Anchor (1st, memory hackathon): "the 3am page" — the agent resolves the THIRD
incident faster than the first. Winners never pitch "an agent framework";
they pitch one painful loop they close end-to-end.
→ DO: open with the loop — "every morning I lose 40 minutes to research +
briefing; Chief of Staff does it before I wake up." Real user (Yogesh), real
workflow, real artifact (the dealer message).

### 2. Memory shown as COMPOUNDING value, not storage (Anchor, Unsay)
Anchor won because memory made the agent BETTER over time (3rd incident fixed
faster than 1st). Unsay (2nd) won on memory INVALIDATION — "I was wrong,
here's the update" as a feature. Nobody wins for "it remembers your name."
→ DO: show memory changing an outcome — the briefing AFTER learning the
preference is visibly better than before. DON'T: do a bare "restart and
recall" party trick and stop there.

### 3. Design is scored equal to implementation (unusual — exploit it)
"Design counts as much as implementation... a technically brilliant project
with a rough interface scores no better than a well-built one that looks
finished." Winners' UIs look like products: clean panels, visible tool badges,
readable typography.
→ DO: make the UI look finished — tool-call badges, memory tab with
timestamps, briefing tab. Record at 1080p, no terminal scrolling marathons.

### 4. A trust/governance "wow" beat in the video (LifeOS time-beats)
The sharpest competitor scripts a 1:25–2:00 beat: agent reaches an unapproved
domain → user denies from phone → timeline logs the block. For Personal AI,
control IS the differentiator (track brief: "keeping your data under your
control").
→ DO: add a 20-second beat where the agent drafts the dealer message and
WAITS for approval — "it never sends without your OK." Show the pending state
on camera. This is our cheapest Quality-of-Idea upgrade.

### 5. Cheap wins most entrants skip (stack them)
- Best Use of Tavily: one functional runtime call. FEWER contestants than
  overall prizes. Our rental-hunt moment already does this — make the Tavily
  call VISIBLE (badge + one spoken line).
- Most Valuable Feedback ($100 × 10): required submission field anyway — write
  it from a running log during the build, not on the last day. Specificity is
  visible.
- README must explicitly state: where Nemotron is used, where Token Factory
  accelerated the workflow, other Nebius services used. Judges skim for this.
- Video must have AUDIO explaining Token Factory + NVIDIA model usage (stated
  in an entrant checklist). Never submit a silent screen-capture.

## DO / DON'T list for our entry

DO:
- Lead the Devpost description with track fit: always-on, private, persistent
  memory, reusable skills, daily workflows — first paragraph.
- Record the video with LIVE keys (Nemotron + Tavily), not mock mode; show a
  small on-screen badge "Nemotron-3-Nano · Nebius Token Factory · live".
- Show tool badges on every agent action (tavily_search, memory_write,
  memory_read) — judges skim for sponsor-tech usage.
- End the video with ONE line on Nemotron + Token Factory (required audio).
- Include the approval-gate beat (pattern 4) and the compounding-memory beat
  (pattern 2).
- Write the feedback section from build notes as you go.
- Keep the repo public from day one with Apache-2.0/MIT at the top level.

DON'T:
- Don't open with architecture diagrams — open with the painful loop (pattern 1).
- Don't let the video exceed 3:00 (hard rule) or go silent on sponsor tech.
- Don't demo in mock mode and "promise" live mode — judges may never run it.
- Don't narrate chain-of-thought — answers must be user-facing (already fixed
  in agent.py).
- Don't add decorative sponsor mentions — every NVIDIA/Nebius component must
  be load-bearing in the demo.
- Don't skip the prior-work disclosure if any code predates the submission
  period (rules require it).

## Grand Prize vs Track Winner — what separates them
Grand winners nail ALL four criteria with a visceral problem + flawless
end-to-end demo + personal story, and their sponsor tech is irreplaceable.
Track winners win on undeniable track fit + sponsor-tech depth. Our path:
make Personal AI fit undeniable, make Nemotron/Token Factory load-bearing,
and let the video carry the judging (it may be ALL the judges see).
