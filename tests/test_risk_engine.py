
from src.risk_engine import assess_risk
from src.explanation_engine import generate_explanation


def test_suspicious_message():
    rules = [
        {
            "type": "urgency",
            "evidence": "urgent",
            "severity": "medium"
        },
        {
            "type": "credential_request",
            "evidence": "verify your password",
            "severity": "high"
        }
    ]

    result = assess_risk(None, [], rules)

    assert result["risk_level"] == "elevated"
    assert len(result["indicators"]) == 2

    explanation = generate_explanation(result)
    assert len(explanation["explanations"]) == 2


def test_ordinary_message_with_unavailable_ml():
    result = assess_risk(None, [], [])

    assert result["risk_level"] == "caution"
    assert result["uncertainty"]


def test_no_major_indicators_when_checks_complete():
    ml = {"status": "ok", "label": "legitimate"}

    result = assess_risk(ml, [], [])

    assert result["risk_level"] == "no_major_indicators"


def test_duplicate_evidence():
    finding = {
        "type": "urgency",
        "evidence": "urgent",
        "severity": "medium"
    }

    result = assess_risk(None, [], [finding, finding])

    assert len(result["indicators"]) == 1


def test_invalid_url_evidence():
    urls = [{"status": "invalid", "indicators": []}]

    result = assess_risk(None, urls, [])

    assert result["risk_level"] == "caution"
    assert any("URL" in u for u in result["uncertainty"])