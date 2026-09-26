"""Rule-based analysis for early-stage freelance project briefs."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import UTC, datetime
import re


TECHNOLOGY_SIGNALS: dict[str, tuple[str, ...]] = {
    "Backend API": ("api", "backend", "fastapi", "django", "flask", "endpoint"),
    "Data": ("data", "dashboard", "analytics", "report", "csv", "sql"),
    "AI / LLM": ("ai", "llm", "openai", "chatbot", "rag", "automation"),
    "Database": ("database", "postgres", "postgresql", "mysql", "sqlite"),
    "Frontend": ("frontend", "react", "website", "web app", "ui", "dashboard"),
    "Deployment": ("deploy", "docker", "cloud", "aws", "server", "hosting"),
}

RISK_SIGNALS: dict[str, str] = {
    "urgent": "Timeline may be unrealistic; confirm the delivery date and scope.",
    "asap": "Timeline may be unrealistic; confirm the delivery date and scope.",
    "secure": "Security requirements are mentioned; clarify authentication, permissions, and data handling.",
    "payment": "Payment workflow is in scope; clarify provider, currencies, and compliance needs.",
    "real-time": "Real-time behavior is requested; clarify expected latency and concurrent users.",
    "scrape": "Data collection may have legal or technical limits; confirm source permissions and rate limits.",
}

BASE_QUESTIONS = (
    "Who are the end users and what is the main success metric?",
    "What is the must-have scope for the first version?",
    "What deadline and budget range should guide the delivery plan?",
)


@dataclass(frozen=True)
class BriefAnalysis:
    """Structured result returned from a project-brief analysis."""

    client: str
    summary: str
    technologies: list[str]
    risks: list[str]
    discovery_questions: list[str]
    created_at: str

    def to_dict(self) -> dict[str, object]:
        """Return a JSON-serializable representation."""
        return asdict(self)


def analyze_brief(client: str, brief: str) -> BriefAnalysis:
    """Analyze a client brief using transparent keyword-based rules.

    This deliberately uses simple, inspectable rules. In a later version, an
    OpenAI-powered layer can improve summaries and follow-up questions without
    hiding the application's core workflow.
    """
    cleaned_client = client.strip()
    cleaned_brief = " ".join(brief.split())

    if not cleaned_client:
        raise ValueError("Client name cannot be empty.")
    if not cleaned_brief:
        raise ValueError("Project brief cannot be empty.")

    lowered_brief = cleaned_brief.casefold()
    technologies = [
        category
        for category, keywords in TECHNOLOGY_SIGNALS.items()
        if any(_contains_keyword(lowered_brief, keyword) for keyword in keywords)
    ]
    if not technologies:
        technologies = ["General Python application"]

    risks = list(
        dict.fromkeys(
            message
            for keyword, message in RISK_SIGNALS.items()
            if _contains_keyword(lowered_brief, keyword)
        )
    )
    if not risks:
        risks = ["No obvious delivery risks detected; confirm scope before estimating."]

    questions = list(BASE_QUESTIONS)
    if "ai" in lowered_brief or "openai" in lowered_brief or "chatbot" in lowered_brief:
        questions.append("What data may the AI access, and how should sensitive data be protected?")
    if "api" in lowered_brief:
        questions.append("Which external systems or API integrations are required?")

    return BriefAnalysis(
        client=cleaned_client,
        summary=_summarize(cleaned_brief),
        technologies=technologies,
        risks=risks,
        discovery_questions=questions,
        created_at=datetime.now(UTC).isoformat(),
    )


def _contains_keyword(text: str, keyword: str) -> bool:
    """Match a keyword as a whole word where possible."""
    return bool(re.search(rf"(?<!\w){re.escape(keyword)}(?!\w)", text))


def _summarize(brief: str, max_length: int = 180) -> str:
    """Keep a concise first-sentence-style preview of the client brief."""
    if len(brief) <= max_length:
        return brief
    return f"{brief[:max_length].rsplit(' ', 1)[0]}…"
