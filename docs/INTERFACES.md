# Proposed component interfaces — review before implementation

These are **contracts to align modules**, not claims that implementations exist. Collaborators should agree on return shapes before building dependent components.

## Text rules
```python
def detect_rule_signals(text: str) -> list[dict]: ...
```
Each item: `{ "type": str, "evidence": str, "severity": "low" | "medium" | "high" }`. Evidence must be a direct substring or clearly identified structural observation. Existing implementation is proposed in PR #4.

## Static URL inspection
```python
def analyze_urls(text: str) -> list[dict]: ...
```
Each item: `{ "url": str, "hostname": str | None, "indicators": list[dict], "status": "analyzed" | "invalid" }`. **Never fetch or navigate to submitted URLs.** Malformed inputs must fail safely. Treat every URL risk signal as a heuristic, not proof of maliciousness.

## ML inference
```python
def classify_text(text: str) -> dict: ...
```
Return `{ "label": "phishing" | "legitimate" | "unknown", "score": float | None, "model_id": str, "status": "ok" | "unavailable" }`. Keep dataset label semantics explicit (spam is not necessarily phishing). Unless calibrated, score is a model score, not the probability the message is fraudulent.

## Risk assessment
```python
def assess_risk(classifier_result: dict, url_evidence: list[dict], rule_evidence: list[dict]) -> dict: ...
```
Return `{ "risk_level": "elevated" | "caution" | "no_major_indicators", "indicators": list[dict], "uncertainty": list[str], "recommended_actions": list[str], "analysis_status": str }`. An absence of detected indicators must never be described as guaranteed safe.

## Explanation and translation
```python
def generate_explanation(assessment: dict, language: str = "en") -> dict: ...
```
Must communicate only evidence in `assessment`, preserve uncertainty, and separate translation quality from multilingual detection performance. Target initial languages: English, Traditional Chinese.

## Integration acceptance
1. Each module has unit tests, including empty/malformed inputs.
2. `python -m pytest -q` passes on the integration branch.
3. The Streamlit app handles unavailable ML or malformed URLs without crashing.
4. A message containing a deceptive URL must show the actual parsed hostname and appropriate limitations.
5. One realistic ambiguous case is explained without a confident fabricated verdict.
