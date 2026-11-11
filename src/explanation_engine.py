
"""Turn evidence-based assessments into readable explanations."""


def generate_explanation(assessment, language="en"):
    if language != "en":
        raise ValueError(
            "Only English is implemented. Translation review is pending."
        )

    descriptions = {
        "urgency": "The message uses urgent language.",
        "credential_request": "The message requests sensitive credentials.",
        "financial_pressure": "The message uses financial pressure.",
        "ml_phishing_signal": "The text classifier flagged a possible phishing pattern.",
    }

    findings = []

    for item in assessment.get("indicators", []):
        kind = item.get("type", "unknown")
        evidence = item.get("evidence", "")

        description = descriptions.get(
            kind, f"A warning sign was identified: {kind}."
        )

        findings.append({
            "reason": description,
            "evidence": evidence,
            "source": item.get("source", "unknown")
        })

    return {
        "risk_level": assessment.get("risk_level", "caution"),
        "explanations": findings,
        "uncertainty": assessment.get("uncertainty", []),
        "recommended_actions": assessment.get("recommended_actions", []),
        "disclaimer": (
            "This assessment identifies possible warning signs, "
            "not confirmed fraud or guaranteed safety."
        )
    }