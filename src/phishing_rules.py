
import re

PHISHING_PATTERNS = {
    "urgency": [
        r"immediately",
        r"urgent",
        r"within \d+ (minutes?|hours?)",
        r"act now",
        r"account will be suspended",
    ],
    "credential_request": [
        r"verify your password",
        r"enter your password",
        r"confirm your login",
        r"provide your otp",
        r"share your verification code",
    ],
    "financial_pressure": [
        r"transfer money",
        r"payment required",
        r"pay immediately",
        r"unpaid fee",
    ],
}

def detect_rule_signals(text: str) -> list[dict]:
    """Identify observable phishing warning signs."""
    if not isinstance(text, str):
        raise TypeError("Message must be a string")

    findings = []

    for category, patterns in PHISHING_PATTERNS.items():
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)

            if match:
                findings.append({
                    "type": category,
                    "evidence": match.group(0),
                    "severity": (
                        "high" if category == "credential_request"
                        else "medium"
                    )
                })
                break

    return findings
