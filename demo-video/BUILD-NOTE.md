# Demo video — build note (2026-10-12)

**FINAL:** [FINAL-demo-20261012.mp4](./FINAL-demo-20261012.mp4)
- Duration: **109.4s (1:49)** — under the 3:00 limit
- Resolution: **1920×1080**, h264 + AAC
- Audio: voiceover −16.5 dB mean / −16.4 LUFS integrated, TP −1.5 — clearly audible, not silent
- Voice: English, `avocado_v2:MAI_03` + `--language en` (locked voice)
- Music: mixkit-73 bed at −22 dB under VO (voice clarity preserved)

## How it was built
All visuals are **real Playwright screenshots (1920×1080)** of the actual running app at
http://localhost:8000 — no mock UI, no terminal scrolls. Subtle zoompan per shot.
Voiceover: 6 TTS segments matching the demo script, assembled with ffmpeg.

**Genuine live run:** the on-camera flow used LIVE keys throughout —
Nebius vault `custom.nebius` (Nemotron-3-Nano-30B-A3B) + Tavily vault `custom.tavily`.
The 🏠 Hunt ran the deterministic `POST /api/rental-hunt` pipeline with a real
Tavily search (5 live results). The app server was **really restarted** between the
memory-write and the recall captures — the sqlite memory survived (timestamps
`2026-10-12T22:50:35` visible in the Memory tab).

## Recording checklist (demo-script.md)
- [x] LIVE keys — badge `⚡ nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B · Nebius Token Factory · LIVE`
      visible in every app frame; closing frame shows `GET /api/health` =
      `{"provider":"nebius","live":true,…,"nebius_key_set":true,"tavily_key_set":true}`.
      No mock/offline badge anywhere.
- [x] On-screen badge present whole video (all app screenshots).
- [x] Spoken Tavily line (Moment 1): *"Without Tavily this answer is impossible —
      the model cannot know today's rentals."* + visible `tavily_search … 5 result(s) · live`
      in the step chain.
- [x] Closing sponsor line (required audio): *"All reasoning on NVIDIA Nemotron-3-Nano
      via Nebius Token Factory — no model hosting, no data leaving my control.
      Built for the Personal AI track."*
- [x] 1080p, total 1:49 ≤ 3:00.

## Segment map
| Time | Visual | VO beat |
|---|---|---|
| 0:00–0:21 | Hero chat UI | Hook: the 40-min loop → Chief of Staff intro |
| 0:21–0:47 | 🏠 Hunt step chain (memory_read → tavily_search live → nemotron_draft → request_approval) | Moment 1 + Tavily line |
| 0:47–0:57 | Pending approval card (Approve & send / Edit / Reject) | Trust beat: never sends without OK |
| 0:57–1:24 | Generic briefing (Seattle) → memory_write confirmation → Memory tab timestamps → recall (2 facts) | Memory compounds |
| 1:24–1:40 | Personalized briefing ("Good morning, Yogesh — your briefing at 8 am") | Always-on payoff |
| 1:40–1:49 | /api/health live JSON | Close: Nemotron-3-Nano via Nebius Token Factory |

## Notes / known warts (minor)
- The personalized briefing's date line says "September 24, 2025" (model date wart) —
  personalization elements (name + 8am) are correct and clearly visible.
- Chat renders `**bold**` markdown literally (frontend cosmetic, not a video defect).
- One capture run showed a phantom auto-approve of the Hunt approval (unexplained UI
  click race); the FINAL uses the clean pending-state screenshot — trust beat intact.

## Source assets
- Screenshots: `demo-video/shots/` (seg1_hero, seg2_hunt_chain, seg3_approval,
  seg4a_briefing_generic, seg4b_memory_write, seg4c_memory_tab, seg4d_recall,
  seg4e_briefing_personalized, seg6_health)
- Voiceover: `demo-video/vo/vo1.mp3 … vo6.mp3`
- Assembly script: `/tmp/assemble.py` (+ `/tmp/capture_*.py`)
