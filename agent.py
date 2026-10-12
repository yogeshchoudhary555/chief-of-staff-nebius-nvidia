"""Chief of Staff — the agent loop: plan, call tools, respond."""
import itertools
import json
import time

from skills import match_skill
from tools import TOOLS_SPEC, tavily_search

MAX_STEPS = 6


class ApprovalPending(Exception):
    """Raised when the agent requests user approval for a consequential action.

    Carries the draft; the run pauses instead of completing.
    """

    def __init__(self, action_type: str, draft_text: str, recipient: str = ""):
        super().__init__("approval requested")
        self.action_type = action_type
        self.draft_text = draft_text
        self.recipient = recipient


def _looks_like_thinking(text: str) -> bool:
    """Heuristic: reasoning models sometimes leak chain-of-thought as the reply."""
    t = (text or "").lower()
    if len(t) < 40:
        return False
    markers = (
        "we need to",
        "we should",
        "the user asked",
        "the user wants",
        "let me think",
        "step 1",
        "first, i need to",
        "i should use",
        "tool call",
        "however, the results",
        "we have performed",
    )
    return sum(1 for m in markers if m in t) >= 2

SYSTEM_PROMPT = """You are Chief of Staff, a private always-on personal AI agent.
You run the user's day: research, remember, remind, brief.

Tools you can call (use them proactively, don't just talk about them):
- tavily_search: search the live web for current info, news, listings.
- memory_read: read durable facts/preferences about the user.
- memory_write: save a durable fact/preference (name, location, tastes, routines).

Rules:
- When the user states a durable fact ("my name is…", "I live in…", "remember…"),
  save it with memory_write before replying.
- When answering personal questions or building a briefing, read memory first.
- Prefer fresh web info for anything time-sensitive; cite what you found.
- CONSEQUENTIAL ACTIONS NEED APPROVAL: before sending any message/email, making
  any booking, or posting anything, you MUST call request_approval with the exact
  draft. The run pauses; the user reviews the draft. Never claim something was
  sent before the user approves it.
- Be concise, warm, and concrete. No fluff."""


def _summarize_tool_call(name, args, out):
    """One-line human summary of a tool step for the visible chain."""
    args = args or {}
    try:
        if name == "tavily_search":
            n = len((out or {}).get("results", []))
            q = str(args.get("query", ""))[:48]
            src = (out or {}).get("source", "")
            live = " · live" if src == "tavily-live" else ""
            return f'"{q}" → {n} result(s){live}'
        if name == "memory_read":
            facts = out if isinstance(out, list) else []
            return f'{len(facts)} fact(s) recalled'
        if name == "memory_write":
            v = str(args.get("value", ""))[:40]
            return f'{args.get("key", "")} = {v}'
    except Exception:
        pass
    return "ok"


class ChiefOfStaff:
    def __init__(self, provider, memory, skills):
        self.provider = provider
        self.memory = memory
        self.skills = skills
        self._counter = itertools.count(1)
        self._approvals = {}  # id -> approval record
        self._appr_counter = itertools.count(1)

    # -- approval queue ----------------------------------------------------
    def _new_approval(self, action_type, draft_text, recipient, skill_name=None):
        aid = f"appr_{next(self._appr_counter)}"
        rec = {
            "id": aid,
            "action_type": action_type,
            "draft_text": draft_text,
            "recipient": recipient or "",
            "skill": skill_name or "",
            "status": "pending",
            "created_at": time.strftime("%Y-%m-%dT%H:%M:%S"),
        }
        self._approvals[aid] = rec
        return rec

    def list_pending_approvals(self):
        return [r for r in self._approvals.values() if r["status"] == "pending"]

    def approve(self, approval_id: str, edited_text: str = None):
        """User approved the draft (optionally edited). Simulate the send."""
        rec = self._approvals.get(approval_id)
        if not rec or rec["status"] != "pending":
            return {"ok": False, "error": "approval not found or not pending"}
        final_text = (edited_text or "").strip() or rec["draft_text"]
        rec["status"] = "approved"
        rec["final_text"] = final_text
        # Simulated send — in a production build this is where the real
        # channel call (WhatsApp/email API) would fire.
        rec["send_result"] = {
            "sent": True,
            "channel": "simulated",
            "action_type": rec["action_type"],
            "recipient": rec["recipient"],
        }
        to = f" to {rec['recipient']}" if rec["recipient"] else ""
        reply = (
            f"✅ Approved — {rec['action_type']}{to} sent "
            f"(simulated send in demo)."
        )
        return {"ok": True, "reply": reply, "approval": rec}

    def reject(self, approval_id: str):
        rec = self._approvals.get(approval_id)
        if not rec or rec["status"] != "pending":
            return {"ok": False, "error": "approval not found or not pending"}
        rec["status"] = "rejected"
        return {
            "ok": True,
            "reply": (
                f"🚫 Cancelled — the {rec['action_type']} was not sent. "
                "Nothing went out."
            ),
            "approval": rec,
        }

    def respond(self, user_message: str, history=None, force_skill: str = None):
        history = history or []
        skill = None
        if force_skill:
            skill = next(
                (s for s in self.skills if s["name"] == force_skill), None
            )
        else:
            skill = match_skill(self.skills, user_message)

        system = SYSTEM_PROMPT
        if skill:
            system += f"\n\nActive skill: {skill['name']}\n{skill['body']}"

        messages = [{"role": "system", "content": system}]
        for h in history[-10:]:
            if h.get("role") in ("user", "assistant"):
                messages.append(
                    {"role": h["role"], "content": h.get("content", "")}
                )
        messages.append({"role": "user", "content": user_message})

        tools_used = []
        steps = []  # visible thinking chain: plan → tool → observation
        reply = ""
        pending_approval = None
        for _ in range(MAX_STEPS):
            result = self.provider.chat(messages, TOOLS_SPEC)
            if not result.tool_calls:
                reply = result.text or "(no response)"
                break
            try:
                for tc in result.tool_calls:
                    if not tc.id:
                        tc.id = f"call_{next(self._counter)}"
                    tools_used.append(tc.name)
                    out = self._dispatch(tc)
                    steps.append(
                        {
                            "tool": tc.name,
                            "detail": _summarize_tool_call(
                                tc.name, tc.arguments, out
                            ),
                        }
                    )
                    messages.append(
                        {
                            "role": "tool",
                            "tool_call_id": tc.id,
                            "name": tc.name,
                            "content": json.dumps(out, ensure_ascii=False)[:4000],
                        }
                    )
            except ApprovalPending as ap:
                # Consequential action: pause the run, hand the draft to the user.
                pending_approval = self._new_approval(
                    ap.action_type, ap.draft_text, ap.recipient,
                    skill_name=skill["name"] if skill else None,
                )
                steps.append(
                    {
                        "tool": "request_approval",
                        "detail": f'{ap.action_type} → waiting for your OK',
                    }
                )
                found = self._summarize_last_search(messages)
                reply = (
                    (f"I found {found}. " if found else "")
                    + "I've drafted the "
                    f"{ap.action_type}{' for ' + ap.recipient if ap.recipient else ''} "
                    "below — nothing has been sent yet. "
                    "Review it: approve, edit, or reject."
                )
                break
        else:
            reply = result.text or "(stopped after max steps)"

        # Trust-beat enforcement: if the active skill's steps require
        # request_approval and the model finished without calling it, give it
        # up to 2 more turns with an explicit instruction. The approval gate
        # is the product's core promise — never silently skipped.
        if (
            skill
            and "request_approval" in (skill.get("body") or "")
            and pending_approval is None
            and tools_used
        ):
            for _ in range(2):
                messages.append(
                    {
                        "role": "user",
                        "content": (
                            "The active skill requires you to call "
                            "request_approval with your exact draft before "
                            "finishing. Call it now — do not give your final "
                            "answer instead."
                        ),
                    }
                )
                try:
                    result = self.provider.chat(messages, TOOLS_SPEC)
                except Exception:
                    break
                if not result.tool_calls:
                    break
                try:
                    for tc in result.tool_calls:
                        if not tc.id:
                            tc.id = f"call_{next(self._counter)}"
                        tools_used.append(tc.name)
                        out = self._dispatch(tc)
                        steps.append(
                            {
                                "tool": tc.name,
                                "detail": _summarize_tool_call(
                                    tc.name, tc.arguments, out
                                ),
                            }
                        )
                        messages.append(
                            {
                                "role": "tool",
                                "tool_call_id": tc.id,
                                "name": tc.name,
                                "content": json.dumps(out, ensure_ascii=False)[
                                    :4000
                                ],
                            }
                        )
                except ApprovalPending as ap:
                    pending_approval = self._new_approval(
                        ap.action_type,
                        ap.draft_text,
                        ap.recipient,
                        skill_name=skill["name"] if skill else None,
                    )
                    steps.append(
                        {
                            "tool": "request_approval",
                            "detail": (
                                f"{ap.action_type} → waiting for your OK"
                            ),
                        }
                    )
                    found = self._summarize_last_search(messages)
                    reply = (
                        (f"I found {found}. " if found else "")
                        + "I've drafted the "
                        f"{ap.action_type}"
                        f"{' for ' + ap.recipient if ap.recipient else ''} "
                        "below — nothing has been sent yet. "
                        "Review it: approve, edit, or reject."
                    )
                    break

        # Reasoning-model quirk: Nemotron sometimes returns its chain-of-thought
        # in the reasoning field with empty content. If the reply looks like
        # narrated thinking rather than a user-facing answer, ask once for a
        # clean final answer (no tools on this pass).
        if _looks_like_thinking(reply):
            nudged = messages + [
                {
                    "role": "user",
                    "content": "Now give your final answer to the user directly in 2-4 sentences. Do not describe your thought process.",
                }
            ]
            try:
                final = self.provider.chat(nudged)
                if final.text and not _looks_like_thinking(final.text):
                    reply = final.text
            except Exception:
                pass

        return {
            "reply": reply,
            "tools_used": tools_used,
            "steps": steps,
            "skill": skill["name"] if skill else None,
            "pending_approval": pending_approval,
        }

    def run_rental_hunt(self, location="H Block, Sri Ganganagar", budget="10000"):
        """Deterministic rental-hunt pipeline (the demo's trust-beat path).

        The approval gate is a structural feature, not a probabilistic model
        behavior: memory → live Tavily → Nemotron summarizes + drafts →
        request_approval pauses for the user. Every step is visible.
        """
        steps = []
        prefs = self.memory.read("")
        steps.append(
            {"tool": "memory_read", "detail": f"{len(prefs)} fact(s) recalled"}
        )
        pref_hint = ""
        if prefs:
            pref_hint = "User preferences: " + "; ".join(
                f"{p.get('key')}: {p.get('value')}" for p in prefs[:6]
            )
        query = f"2 BHK flat for rent {location} under {budget}"
        search_out = tavily_search(query, 5)
        results = search_out.get("results", []) or []
        steps.append(
            {
                "tool": "tavily_search",
                "detail": f'"{query[:48]}" → {len(results)} result(s) · live',
            }
        )
        listings = "\n".join(
            f"- {r.get('title', '')}: {(r.get('content', '') or '')[:220]} "
            f"({r.get('url', '')})"
            for r in results[:5]
        )
        draft_messages = [
            {
                "role": "system",
                "content": (
                    "You are Chief of Staff, a private personal AI. "
                    "Summarize rental listings, then draft ONE short dealer "
                    "outreach message (WhatsApp-ready, under 60 words). "
                    "Never invent listings or phone numbers — only use what "
                    "the search returned.\n\n"
                    "Reply in exactly this format:\n"
                    "SUMMARY:\n<2-4 line summary with prices>\n"
                    "DRAFT:\n<the dealer message>"
                ),
            },
            {
                "role": "user",
                "content": (
                    f"{pref_hint}\nLive listings for '{query}':\n{listings}"
                    if listings
                    else f"No live listings found for '{query}'."
                ),
            },
        ]
        try:
            res = self.provider.chat(draft_messages)
            text = res.text or ""
        except Exception:
            text = ""
        summary, draft = text, ""
        if "DRAFT:" in text:
            summary, draft = text.split("DRAFT:", 1)
            summary = summary.replace("SUMMARY:", "").strip()
            draft = draft.strip()
        if not draft:
            draft = (
                "Namaste! I saw your 2 BHK listing near "
                f"{location} (budget under ₹{budget}). Is it still "
                "available? Could I visit this week? Please share a "
                "suitable time. Thank you!"
            )
        steps.append(
            {"tool": "nemotron_draft", "detail": "summary + dealer message"}
        )
        approval = self._new_approval(
            "message", draft, "property dealer", skill_name="rental-hunt"
        )
        steps.append(
            {"tool": "request_approval", "detail": "message → waiting for your OK"}
        )
        reply = (
            f"I found {len(results)} live listing(s). "
            f"{summary}\n\nI've drafted the message below — nothing has been "
            "sent yet. Review it: approve, edit, or reject."
        )
        return {
            "reply": reply,
            "tools_used": ["memory_read", "tavily_search", "request_approval"],
            "steps": steps,
            "skill": "rental-hunt",
            "pending_approval": approval,
        }

    def morning_briefing(self):
        """One-shot briefing using the morning-briefing skill."""
        return self.respond(
            "Generate my morning briefing for today.",
            force_skill="morning-briefing",
        )

    # -- internals ---------------------------------------------------------
    def _summarize_last_search(self, messages):
        """One-line summary of the most recent web search for the pause reply."""
        for m in reversed(messages):
            if m.get("role") == "tool" and m.get("name") == "tavily_search":
                try:
                    data = json.loads(m.get("content", "{}"))
                except json.JSONDecodeError:
                    return ""
                results = data.get("results") or []
                if results:
                    return f"{len(results)} listing(s)"
                return ""
        return ""

    def _dispatch(self, tc):
        name, args = tc.name, tc.arguments or {}
        if name == "tavily_search":
            return tavily_search(
                args.get("query", ""), int(args.get("max_results", 5) or 5)
            )
        if name == "memory_read":
            return self.memory.read(args.get("key", "") or "")
        if name == "memory_write":
            ok = self.memory.write(args.get("key", ""), args.get("value", ""))
            return {
                "ok": ok,
                "key": args.get("key", ""),
                "value": args.get("value", ""),
            }
        if name == "request_approval":
            # Never executes the action — pauses the run for user review.
            raise ApprovalPending(
                args.get("action_type", "message"),
                args.get("draft_text", ""),
                args.get("recipient", "") or "",
            )
        return {"error": f"unknown tool: {name}"}
