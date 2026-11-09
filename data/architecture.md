# ScamShield AI — Initial Technical Architecture (Proposal)

**Status: Proposed.** No described module is claimed as implemented. Review this architecture with the team before locking interfaces.

## Goal and boundaries

Analyze suspicious text, messages, email excerpts, and URLs to surface *observable* scam/phishing indicators and recommended safe actions. Do not claim reliable AI-authorship detection. Start with text and URLs; local QR-code decoding is optional.

## Pipeline

```text
Streamlit UI (app.py)
      |
Input validation and normalization (src/input_processing.py)
      |
      +--> Rule indicators (src/phishing_rules.py)
      +--> Baseline text classifier (src/text_classifier.py)
      +--> Static URL parsing (src/url_analyzer.py)
      |         [NO automatic network fetch / navigation]
      +--> [optional] QR decode (src/qr_decoder.py)
      |
Risk aggregation + uncertainty flags (src/risk_engine.py)
      |
Evidence-grounded explanation (src/explanation_engine.py)
      |
Translation/templates (src/translations.py)
      |
Risk label + cited indicators + safe next actions + limitations
```

## Proposed interfaces

```python
def normalize_input(text: str) -> str: ...

def detect_rule_signals(text: str) -> list[dict]: ...

def analyze_urls(text: str) -> list[dict]: ...

def classify_text(text: str) -> dict: ...

def assess_risk(classifier_result: dict, url_evidence: list[dict], rule_evidence: list[dict]) -> dict: ...

def generate_explanation(assessment: dict, language: str = "en") -> dict: ...
```

Example *illustrative schema* (not a real model output):

```json
{
  "risk_level": "elevated",
  "score": null,
  "score_type": "not_calibrated",
  "indicators": [{"type": "credential_request", "evidence": "verify your password", "severity": "high"}],
  "uncertainty": ["Sender identity not verified"],
  "recommended_actions": ["Verify through a known official channel"],
  "analysis_status": "completed"
}
```

## Model and evidence strategy

1. Implement a deterministic rule baseline with unit tests.
2. Train a TF-IDF + Logistic Regression baseline on an appropriately labeled dataset, preserving a held-out test set.
3. Consider evidence fusion only after component outputs and uncertainty semantics are well-defined.
4. Explainations must identify evidence *actually produced* by analyzers; LLM rewording, if used, may not introduce unsupported indicators.
5. Do not call uncalibrated scores a percent chance of phishing.
6. Use three user-facing states such as `elevated`, `verify`, and `no_major_indicators`; the third must not imply safety.

## Safety properties

- Treat all inputs as hostile text; escape user-controlled strings in the UI.
- Never follow links automatically; statically parse URLs and flag deceptive structures cautiously.
- If optional remote threat intelligence is added, explicitly restrict outbound requests and disclose third-party processing.
- QR decoding must not navigate to the decoded destination.
- Bound input/upload sizes; validate URL schemes and file types.
- Prevent accidental storage or transmission of private submitted content.
- Keep secrets out of Git; use sample/example data safely.

## Evaluation contract

- Define labels carefully; spam datasets cannot alone validate phishing classification.
- Report precision, recall, F1, false-positive rate, confusion matrix, dataset provenance, and class balance.
- Test urgent-but-legitimate, suspicious-but-unconfirmed, multilingual, and invalid-input cases.
- Separate held-out performance from synthetic demonstrations.
- Log and disclose relevant failure modes, including false reassurance and false alarms.

## Delivery sequence (proposed)

- **Nov 9:** Agree interfaces, data, and responsibilities; documentation/setup.
- **Nov 10:** Implement deterministic rules, baseline classifier, basic UI.
- **Nov 11:** Integrate the end-to-end workflow.
- **Nov 12:** Benchmark, safety tests, language review, and failure analysis.
- **Nov 13:** Freeze demo and rehearse.
- **Nov 14:** Showcase; report only observed results.

## Open decisions (team vote/discussion)

- Named responsibility owners and reviewers.
- Language coverage beyond English and Traditional Chinese.
- Source and licensing of evaluation datasets.
- Whether to implement QR decoding in the MVP.
- Deployment choice, privacy posture, and external AI services.
