
from src.phishing_rules import detect_rule_signals

def test_urgent_phishing_message():
    text = "URGENT! Verify your password immediately."
    results = detect_rule_signals(text)
    types = [item["type"] for item in results]

    assert "urgency" in types
    assert "credential_request" in types

def test_normal_message():
    text = "Hi! Our meeting starts at 3 PM tomorrow."
    results = detect_rule_signals(text)
    assert results == []

def test_financial_pressure():
    text = "Payment required. Transfer money immediately."
    results = detect_rule_signals(text)
    types = [item["type"] for item in results]

    assert "financial_pressure" in types

def test_invalid_input():
    import pytest

    with pytest.raises(TypeError):
        detect_rule_signals(None)
