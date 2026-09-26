from brief_analyzer.analyzer import analyze_brief


def test_detects_relevant_work_areas() -> None:
    analysis = analyze_brief(
        "Acme",
        "Build a FastAPI backend with PostgreSQL and an OpenAI-powered chatbot.",
    )

    assert "Backend API" in analysis.technologies
    assert "Database" in analysis.technologies
    assert "AI / LLM" in analysis.technologies


def test_adds_ai_discovery_question() -> None:
    analysis = analyze_brief("Acme", "We need an AI assistant for support.")

    assert any("What data may the AI access" in question for question in analysis.discovery_questions)


def test_rejects_empty_client() -> None:
    try:
        analyze_brief("   ", "Build a dashboard")
    except ValueError as error:
        assert str(error) == "Client name cannot be empty."
    else:
        raise AssertionError("Expected an empty client name to be rejected.")


def test_shortens_long_summary() -> None:
    analysis = analyze_brief("Acme", "word " * 60)

    assert len(analysis.summary) <= 181
    assert analysis.summary.endswith("…")
