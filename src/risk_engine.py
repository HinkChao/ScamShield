
"""Combine observed warning signs into a cautious risk assessment."""

VALID_SEVERITIES = {"low", "medium", "high"}


def assess_risk(classifier_result, url_evidence, rule_evidence):
    indicators = []
    seen = set()
    uncertainty = []

    # Collect observed rule indicators.
    for item in rule_evidence or []:
        if not isinstance(item, dict):
            continue

        kind = item.get("type")
        evidence = item.get("evidence")
        severity = item.get("severity")

        if not kind or not evidence or severity not in VALID_SEVERITIES:
            continue

        key = (str(kind), str(evidence).lower())
        if key in seen:
            continue
        seen.add(key)

        indicators.append({
            "type": str(kind),
            "evidence": str(evidence),
            "severity": severity,
            "source": "rules"
        })

    # Collect URL indicators from the agreed URL schema.
    for url_result in url_evidence or []:
        if not isinstance(url_result, dict):
            continue

        if url_result.get("status") != "analyzed":
            uncertainty.append("A URL could not be fully analyzed.")
            continue

        for item in url_result.get("indicators", []):
            if not isinstance(item, dict):
                continue

            kind = item.get("type")
            evidence = item.get("evidence")
            severity = item.get("severity")

            if not kind or not evidence or severity not in VALID_SEVERITIES:
                continue

            key = (str(kind), str(evidence).lower())
            if key in seen:
                continue
            seen.add(key)

            indicators.append({
                "type": str(kind),
                "evidence": str(evidence),
                "severity": severity,
                "source": "url"
            })

    # ML is optional. Never interpret an unavailable model as safe.
    ml_available = (
        isinstance(classifier_result, dict)
        and classifier_result.get("status") == "ok"
    )

    if not ml_available:
        uncertainty.append("ML classification is unavailable.")
    else:
        label = classifier_result.get("label")

        if label == "phishing":
            indicators.append({
                "type": "ml_phishing_signal",
                "evidence": "The text classifier flagged this message.",
                "severity": "medium",
                "source": "ml"
            })
            uncertainty.append(
                "The ML prediction is not proof of fraud."
            )
        elif label not in ("legitimate",):
            uncertainty.append("ML classification was inconclusive.")

    if url_evidence is None:
        uncertainty.append("URL analysis is unavailable.")

    if rule_evidence is None:
        uncertainty.append("Rule analysis is unavailable.")

    # Simple, transparent decision policy.
    independent_types = {item["type"] for item in indicators}
    has_high = any(
        item["severity"] == "high" for item in indicators
    )

    if has_high or len(independent_types) >= 2:
        level = "elevated"
    elif indicators or uncertainty:
        level = "caution"
    else:
        level = "no_major_indicators"

    if level == "elevated":
        actions = [
            "Do not share passwords or verification codes.",
            "Verify the request using an independently found official channel."
        ]
    elif level == "caution":
        actions = [
            "Verify the sender and context before acting.",
            "Avoid opening unfamiliar links or sharing sensitive information."
        ]
    else:
        actions = [
            "No major indicators were identified by the supplied checks.",
            "This does not guarantee the message is safe."
        ]

    return {
        "risk_level": level,
        "indicators": indicators,
        "uncertainty": uncertainty,
        "recommended_actions": actions,
        "analysis_status": "completed_with_limitations" if uncertainty else "completed"
    }
