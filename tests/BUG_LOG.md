# ScamShield Bug Log & Issue Tracker

| Bug ID | Component | Description | Steps to Reproduce | Expected Result | Actual Result | Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 001 | `risk_engine` | Risk scoring under-classifies explicit text-based phishing if no URL is present. | Run `pytest tests/test_demonstration_cases.py`. Observe failures in `test_explicit_credential_phishing` and `test_message_without_a_url`. | Risk level evaluates to `elevated` or `high` based purely on text signals. | Risk level defaults to `caution`. | Open |