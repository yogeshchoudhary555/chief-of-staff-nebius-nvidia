# Winner Deep Research — Nebius × NVIDIA Global AI Hackathon
Researched 2026-10-12 via Devpost pages, winner announcements, winner repos, judge lists.
Goal: concrete patterns behind $20,000 Grand Prize wins, not generic advice.

## The rules that actually govern this hackathon (verified from the page)
- **Pass/fail gate first:** does the project genuinely fit its track AND actually use
  Nebius Token Factory/AI Cloud + ≥1 NVIDIA open model? Everything else is scored after.
- **4 judging criteria** (appear equally weighted): Technological Implementation /
  Design / Potential Impact / Quality of the Idea.
- **Required:** ≤3-min public YouTube demo video showing "how you used Nebius Token
  Factory and NVIDIA Nemotron"; working demo URL; public repo with open-source
  license visible at top + README with setup instructions; README must "highlight
  how you've used NVIDIA Nemotron, where Token Factory accelerated your workflow,
  and any other Nebius Tools or Services used"; product feedback on Token Factory/models.
- **Prize stacking:** one Overall Award OR one Track Award, PLUS one Bonus Award.
  → We can target Grand Prize + Best Use of Tavily ($3,000) simultaneously.
- **Judges (23):** NVIDIA engineers (Nancy Agarwal, Abhinav Balasubramanian, Lakshmi
  Rameish, Surbhi Jha, Selena Williams, Sayali Kandarkar...), Nebius Token Factory
  PMM/DevRel (Dylan Bristot, Rob Spectre, Daniel Myers, Jacquie Capur, AbdulMajed
  Raja...), Tavily FDEs (Evan Rimer, Ricky Johnson, Lakshya Prakash Agarwal).
- **Personal AI track** wording: "always-on, private assistant... persistent memory,
  reusable skills, access to the tools and information you choose... data under your
  control." Our Chief-of-Staff concept matches this verbatim.
- Deadline: Oct 30, 2026, 22:30 IST. 21,616 participants registered at time of check.

## Named winners used as proof
1. **GDELT Open Intelligence Agent** (Qasim Khan) — 1st place, ArangoDB + NVIDIA
   hackathon ($15,000). NL queries → AQL/NetworkX scripts → interactive graph viz.
   ReWOO plan-and-execute agent; dynamic per-task tool selection; human-in-the-loop
   for update/delete; memory across turns; Streamlit UI. Featured on ArangoDB blog,
   promoted by NVIDIA. https://devpost.com/software/gdelt-open-intelligence-agent
2. **Nomi** — Grand Prize, "Agentic AI Unleashed" AWS & NVIDIA hackathon. Multi-sensor
   network system for seniors (physical sensing + agents). Won on specific real
   audience + impact.
3. **Skyrchitect** — 2nd place, same hackathon. Nemotron-nano autonomously designs
   production-ready cloud architectures, generates infra code, calculates costs —
   seconds from idea to deployable output.
4. **basket** (omorros/basket) — 1st place "Best Use of Tavily", Multiagents
   Hackathon London 2026. Orchestrator + 5 specialist agents: Date-Finder (Tavily),
   Retrieval (Tavily), Classifier, Aggregator/Detector, Publisher of cited alerts.
   https://github.com/omorros/basket
5. **8kEdu** — Best Use of NVIDIA Nemotron, AITX × NVIDIA Claw Agents Hack Austin.
   Agent turns YouTube lectures into continuously evolving interactive learning.
6. **MasteryWrite** — Best Use of NemoClaw/OpenShell, same event. Autonomous essay
   assessment that explains its reasoning and improves its own graders over time.
7. **RoundOne.dev** — built FOR this hackathon. Its own video chapters:
   "0:00 Building got cheap. Judging didn't." / "The first minute is the why.
   The rest is a tour of the app."
8. **pawnote** — live competitor, targets Best Apps & Agents + Best Use of Tavily +
   Toronto City Winner; attended Builders & Brews Toronto (city awards reward IRL attendance).

## TOP 10 actionable patterns
1. **The video IS the submission.** With 21,616 participants and 23 judges, most
   entries are scored from video + description + repo alone — nobody runs your code.
   RoundOne's own demo: "The first minute is the why. The rest is a tour of the app."
   Hackathon-judges guide: "If the judges can't understand what problem you're solving
   after 30 seconds, you've already lost." → First 30s of our video = one-sentence
   problem + the person it hurts. No logos, no throat-clearing.
2. **Put the sponsor stack on screen, by exact name.** The rules require the video to
   show "how you used Nebius Token Factory and NVIDIA Nemotron" and the README to
   name models + where Token Factory accelerated the workflow. The judges include
   Token Factory's founding PMM and NVIDIA engineers — say "Nemotron-3-Nano on
   Nebius Token Factory" out loud, show the model ID in the UI, and name Tavily when
   a live search fires. This is free scoring on Technological Implementation.
3. **The eligibility gate is pass/fail — prove real API calls, not name-drops.**
   The Amazon hackathon winner's checklist warns: "The MCP SDK must be imported and
   actually called at runtime. Naming it in the README does not count." Our video must
   show a LIVE Token Factory inference call and a LIVE Tavily search (visible request/
   result), not canned output. A judge who suspects mocking fails the entry.
4. **Show the thinking, not just the answer.** Every agent winner exposes the loop:
   GDELT (ReWOO plan → tool selection → execution), MasteryWrite ("explains its
   reasoning"), Skyrchitect (design → code → cost). JacHacks rubric scores "depth of
   agentic behavior: planning, memory, tool use, multi-agent coordination." → Our video
   must show plan → tool calls → observations → final result as a visible chain.
5. **Chain 3–5 visible tool steps; single-shot answers lose.** GDELT: NL → AQL →
   graph analytics → visualization. basket: 5 agents. Winners never do one LLM call →
   answer. Our rental-hunt (briefing → memory recall → Tavily search → candidate
   shortlist → approval gate → send) is exactly this shape — keep every step visible.
6. **Human-in-the-loop is a winning feature.** GDELT listed "Human in the Loop for
   Update/Delete: critical updates require human confirmation" as a build highlight —
   and won 1st place. Our request_approval trust beat (pause → user approves/edits/
   rejects before any send) is a proven winner pattern, not a demo crutch. Show it
   mid-video, not as an afterthought.
7. **Demo memory compounding explicitly.** GDELT listed cross-turn memory as a feature;
   the Personal AI track demands "persistent memory, reusable skills." Don't claim
   memory — PROVE it: morning briefing that references something learned yesterday,
   then a new fact learned today that changes tomorrow's briefing. Before/after in
   one video.
8. **Make Tavily load-bearing, not decorative.** basket won Best Use of Tavily because
   the pipeline collapses without live web data (reformulation date + complaint spikes
   can't come from training data). Tavily's own FDEs are judging. → Our video must say
   and show: "without Tavily, this answer is impossible" — live rental listings the
   model could never know. Bonus stacks with Grand Prize.
9. **Ship a complete product experience, not a POC.** Design criterion: "a complete,
   coherent product experience not just a technical proof of concept." Winners have
   real UIs (GDELT's Streamlit, basket's dashboard, RoundOne's app tour). Our single-page
   UI with Chat/Briefing/Memory/Skills tabs satisfies this — the video must tour it,
   not just a terminal.
10. **Name a specific person with a specific problem at a specific moment.**
    Impact criterion: "a credible, specific case for solving a real problem for a real
    audience... based on what's demonstrated." Nomi won Grand Prize on senior care;
    AskStreets on street-network analysis. "A renter in Sri Ganganagar hunting a 2BHK
    at 9pm" beats "helps everyone." Also: 20 city awards ($500) exist and reward IRL
    Builders & Brews attendance — check for a nearby event.

## Anti-patterns (what loses)
- Canned/mock demo output — fails the eligibility gate on suspicion alone.
- Problem explained after 60s of intro — judges have already moved on.
- Sponsor tools mentioned only in README, never shown working.
- "AI assistant" with one chat call and no visible tools, memory, or approval.
- Repo without license at top, no setup instructions, no model/tool callouts.
- Video over 3 minutes — judges aren't required to watch past 3:00.
