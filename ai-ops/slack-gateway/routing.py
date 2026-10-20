from __future__ import annotations

import hashlib
import json
import re
from dataclasses import dataclass, asdict

ROUTER_VERSION = "2026-10-19.1"

CHANNELS = {
    "optimize": "C0C9AQ2FK3P",
    "vt_decks": "C0C8YU5RDDM",
    "decisions": "C0C8YU5RG5D",
    "parallel_agents": "C0C8ZJ4FTAT",
    "feedback_pipeline": "C0C9913PWH3",
    "drive_organization": "C0C9AL4D293",
    "teaching_hub": "C0C9E488BAN",
    "class_reports": "C0C9E489T6E",
    "writing_flow": "C0C9FGVK1DY",
    "work_que": "C0C9FD9QJ4W",
    "kathy": "C0C9C47UKU5",
    "exceptions": "C0C9BJ57N13",
    "decomission": "C0C9BJ4S9HT",
    "teaching_reflection": "C0C9EMYK6MC",
    "needs_rerouting": "C0C9QPBHDE1",
    "system_review": "C0C9J0NU6LC",
    "lesson_preflight": "C0CA8LQ417A",
    "higher_ed": "C0C9L06CVU4",
    "research_roam": "C0C9B0N3WUV",
}

CHANNEL_NAMES = {v: k.replace("_", "-") for k, v in CHANNELS.items()}
CHANNEL_NAMES[CHANNELS["optimize"]] = "optimize-me"

KINDS = {"thought", "task", "decision", "accomplishment", "question"}
AREAS = {"ai_ops", "school", "writing", "higher_ed", "research_roam", "personal_admin"}

@dataclass(frozen=True)
class RouteDecision:
    kind: str
    area: str
    destination_id: str
    summary: str
    provider: str
    model: str | None
    confidence: float
    deterministic: bool

    def asdict(self):
        return asdict(self)


def normalized(text: str) -> str:
    return re.sub(r"\s+", " ", text.strip())


def cache_key(text: str, provider: str, model: str | None) -> str:
    body = json.dumps({"v": ROUTER_VERSION, "text": normalized(text), "provider": provider, "model": model}, sort_keys=True)
    return hashlib.sha256(body.encode()).hexdigest()


def provider_override(text: str) -> tuple[str | None, str]:
    value = text.strip()
    patterns = [
        ("openai", r"^(?:\[openai\]|openai:|@openai\s+)\s*"),
        ("claude", r"^(?:\[claude\]|claude:|@claude\s+)\s*"),
    ]
    for provider, pattern in patterns:
        match = re.match(pattern, value, flags=re.I)
        if match:
            return provider, value[match.end():].strip()
    return None, value


def _without_addressees(text: str) -> str:
    # Slack addresses are metadata before the request, not part of its wording.
    return re.sub(r"^(?:\s*<@[A-Z0-9]+(?:\|[^>]+)?>[\s,:]*)+", "", text, flags=re.I)


def _kind(text: str) -> tuple[str, float]:
    text = _without_addressees(text)
    lower = text.lower()
    # Requests mentioning a completed/failed item are still requests.
    if re.search(r"^(?:please\s+)?(?:task|todo|to-do|need to|remember to|add to|fix|repair|implement|audit|reconcile|verify|update|route|send|file|queue)\b", lower) or re.search(r"\bi need (?:you|us|to)\b", lower):
        return "task", 0.90
    if "?" in text or re.match(r"^(what|why|how|when|where|which|who|can|should|does|do)\b", lower):
        return "question", 0.84
    if re.search(r"\b(done|finished|completed|accomplished|shipped|fixed|resolved)\b", lower):
        return "accomplishment", 0.94
    if re.search(r"\b(decision|decided|chose|we will)\b|^rule:", lower):
        return "decision", 0.92
    if re.match(r"^(?:blocked|failure|error|exception|retirement candidate|human action)\s*:", lower):
        return "thought", 0.86
    if re.search(r"\b(?:kathy|katherine)\s+(?:needs to|must)\s+(?:approve|choose|decide|sign in|log in)\b", lower):
        return "task", 0.90
    if re.search(r"\b(idea|thought|reflection|notice|noticed|noticing|wondering|i think)\b", lower):
        return "thought", 0.82
    return "thought", 0.45


def _area_destination(text: str, kind: str) -> tuple[str, str, float]:
    text = _without_addressees(text)
    lower = text.lower()
    # Only explicit routing directives override topic lanes, not incidental mentions.
    directive = re.match(r"^(?:please\s+)?(?:route|send|file|queue)\s+(?:(?:this|it)\s+)?(?:to|in)\s+(?:<#([A-Z0-9]+)(?:\|[^>]+)?>|#([a-z-]+))(?=\s|:|$)", text, re.I)
    if directive:
        destination = directive.group(1) or next((cid for cid, name in CHANNEL_NAMES.items() if name == directive.group(2).lower()), None)
        if destination in CHANNEL_NAMES:
            return "ai_ops", destination, 0.96
    if re.match(r"^human action\s*:", lower) or re.search(r"\b(?:kathy|katherine)\s+(?:needs to|must)\s+(?:approve|choose|decide|sign in|log in)\b", lower):
        return "personal_admin", CHANNELS["kathy"], 0.94
    if re.match(r"^(?:blocked|failure|error|exception)\s*:", lower):
        return "ai_ops", CHANNELS["exceptions"], 0.94
    if re.match(r"^retirement candidate\s*:", lower):
        return "ai_ops", CHANNELS["decomission"], 0.94
    if kind == "decision":
        return "ai_ops", CHANNELS["decisions"], 0.88

    if re.search(r"\b(wilmu|wilmington|oli\s*710[26]|710[26]|dip|doctoral|graduate paper|higher[- ]ed|professor|adjunct)\b", lower):
        return "higher_ed", CHANNELS["higher_ed"], 0.96

    if re.search(r"\b(roam|literature|annotated lit|literature review|citation|zotero|research source|source note)\b", lower):
        return "research_roam", CHANNELS["research_roam"], 0.94

    if re.search(r"\b(answerable teaching|manuscript|chapter|substack|book|writing voice|reflection ledger|authorial agency)\b", lower):
        return "writing", CHANNELS["writing_flow"], 0.94

    school = re.search(r"\b(school|biology|forensics|anatomy|student|lesson|schoology|infinite campus|\bic\b|agenda|grade|grading|worksheet|deck|feedback|print|roster)\b", lower)
    if school:
        if kind == "thought" and re.search(r"\b(reflection|noticed|noticing|notice)\b", lower):
            return "school", CHANNELS["teaching_reflection"], 0.93
        if re.search(r"\b(vt|variation theory|critical aspect|deck)\b", lower):
            return "school", CHANNELS["vt_decks"], 0.95
        if re.search(r"\b(feedback|revision|itracker)\b", lower):
            return "school", CHANNELS["feedback_pipeline"], 0.95
        if re.search(r"\b(preflight|lesson|print|lab setup|materials|grocery)\b", lower):
            return "school", CHANNELS["lesson_preflight"], 0.93
        if re.search(r"\b(report|grade|roster|student)\b", lower):
            return "school", CHANNELS["class_reports"], 0.88
        if re.search(r"\b(drive|folder|file|link)\b", lower):
            return "school", CHANNELS["drive_organization"], 0.88
        return "school", CHANNELS["teaching_hub"], 0.84

    if re.search(r"\b(parallel|coordinate|claude|chatgpt|codex|agent)\b", lower) and re.search(r"\b(agent|coordinate|parallel|talk to|handoff)\b", lower):
        return "ai_ops", CHANNELS["parallel_agents"], 0.91

    if re.search(r"\b(api|router|cache|github|cloud run|google cloud|account|subscription|automation|workflow|system|optimi[sz]e|slack)\b", lower):
        return "ai_ops", CHANNELS["work_que" if kind == "task" else "system_review"], 0.90

    if re.search(r"\b(email|calendar|todoist|grocer|order|appointment|bill|admin|home)\b", lower):
        return "personal_admin", CHANNELS["work_que" if kind == "task" else "optimize"], 0.78

    return "ai_ops", CHANNELS["optimize"], 0.40


def deterministic_route(text: str) -> RouteDecision | None:
    override, clean = provider_override(text)
    kind, kind_conf = _kind(clean)
    area, destination, area_conf = _area_destination(clean, kind)
    confidence = min(kind_conf, area_conf)
    if override:
        return None
    if confidence < 0.78:
        # Unclear messages go to #needs-rerouting for Katherine, not to a paid model.
        # A model is called only when the message asks for one ([openai]/[claude]).
        destination = CHANNELS["needs_rerouting"]
        if kind_conf < 0.78:
            kind = "thought"
    summary = normalized(clean)
    if len(summary) > 500:
        summary = summary[:497].rstrip() + "..."
    return RouteDecision(kind, area, destination, summary, "deterministic", None, confidence, True)


def default_provider_for(text: str) -> tuple[str, str]:
    override, clean = provider_override(text)
    if override == "openai":
        return "openai", "gpt-6-luna"
    if override == "claude":
        return "claude", "claude-haiku-5-5"
    lower = clean.lower()
    # Writing/scholar/research ambiguity defaults to Claude; operational ambiguity to OpenAI.
    if re.search(r"\b(book|chapter|substack|writing|wilm|710[26]|dip|doctoral|research|roam|literature)\b", lower):
        return "claude", "claude-haiku-5-5"
    return "openai", "gpt-6-luna"


def validate_model_decision(value: dict, *, provider: str, model: str) -> RouteDecision:
    if not isinstance(value, dict):
        raise ValueError("classification must be object")
    kind = value.get("kind")
    area = value.get("area")
    destination = value.get("destination")
    summary = normalized(str(value.get("summary", "")))
    if kind not in KINDS or area not in AREAS:
        raise ValueError("unsupported classification")
    by_name = {name: cid for cid, name in CHANNEL_NAMES.items()}
    if destination not in by_name:
        raise ValueError("unsupported destination")
    if not summary or len(summary) > 500:
        raise ValueError("invalid summary")
    return RouteDecision(kind, area, by_name[destination], summary, provider, model, 0.75, False)


def classifier_prompt(text: str) -> str:
    _, clean = provider_override(text)
    destinations = ", ".join(sorted(CHANNEL_NAMES.values()))
    return (
        "Classify this Slack intake message. Return JSON only with keys kind, area, destination, summary. "
        f"kind must be one of {sorted(KINDS)}. area must be one of {sorted(AREAS)}. "
        f"destination must be one of: {destinations}. "
        "Use decisions for durable cross-domain decisions; higher-ed for Wilmington/doctoral/graduate work; "
        "research-roam for literature/Roam; writing-flow for Answerable Teaching/book/Substack; school channels for school work; "
        "work-que for planned technical or delegated admin work; system-review for AI system observations/questions; "
        "parallel-agents only for multi-agent coordination; exceptions for actual failures/blockers; "
        "decomission for retirement candidates; teaching-reflection for teaching observations. "
        "Use kathy only for an explicit human action/decision that agents cannot resolve, never ordinary troubleshooting. "
        "Honor an explicit routing directive to a supported channel, but do not treat incidental channel mentions as directives. "
        "summary must preserve the user's actual intent in <=60 words and must not invent work completed.\n\n"
        f"MESSAGE:\n{clean}"
    )
