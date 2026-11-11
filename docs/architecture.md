# ScamShield AI — Technical Architecture

**Version:** 1.0  
**Status:** Proposed architecture — pending team review  
**Hackathon:** Fall 2026 Collaborative Hackathon  
**Challenge:** Problem 4 — ScamShield AI

## 1. System Overview

ScamShield AI is a multilingual, explainable phishing and scam detection application.

The system combines machine learning, rule-based security analysis, and evidence-grounded explanations to help users understand suspicious digital communications and make safer decisions.

### Core Workflow

```text
User submits message, email text, or URL
                  |
                  v
       Input Validation
                  |
                  v
     Text & URL Extraction
                  |
                  v
  +-------------------------------+
  |      Detection Modules        |
  |                               |
  |  1. Text ML Classifier        |
  |  2. Phishing Rule Engine      |
  |  3. Static URL Analyzer       |
  +-------------------------------+
                  |
                  v
        Risk Assessment
                  |
                  v
     Explanation Generation
                  |
                  v
     Multilingual Presentation
                  |
                  v
  Risk Indicators + Safe Actions
```

QR-code decoding is an optional enhancement.

## 2. Technology Stack

| Component | Proposed Technology |
|---|---|
| Programming Language | Python 3.11+ |
| Web Interface | Streamlit |
| ML Framework | scikit-learn |
| Text Representation | TF-IDF |
| Baseline Classifier | Logistic Regression |
| URL Analysis | urllib.parse, ipaddress, tldextract |
| QR Decoding | OpenCV (optional) |
| Testing | pytest |
| Data Processing | pandas |
| Version Control | GitHub |

The team may revise this stack after discussing development feasibility.

## 3. Application Components

### 3.1 Input Processing

**File:** `src/input_processing.py`

Responsibilities:

- Receive and validate user-submitted text.
- Handle empty and oversized inputs.
- Normalize text while preserving meaningful evidence.
- Extract URL candidates.
- Avoid executing or automatically opening submitted content.

### 3.2 Text Classification

**File:** `src/text_classifier.py`

Responsibilities:

- Load a trained classification pipeline.
- Predict phishing-related labels.
- Return machine-readable outputs.
- Report when the model is unavailable.

Initial proposed baseline:

TF-IDF + Logistic Regression.

A multilingual or LLM-based model may be evaluated as an enhancement.

The system must not claim to reliably identify whether text was written by AI.

### 3.3 Phishing Rule Engine

**File:** `src/phishing_rules.py`

Responsibilities:

- Identify urgency and time-pressure language.
- Detect credential or sensitive-information requests.
- Recognize possible impersonation cues.
- Identify suspicious calls to action.
- Return evidence excerpts.

Rule matches are warning indicators, not proof of malicious intent.

### 3.4 URL Security Analysis

**File:** `src/url_analyzer.py`

Responsibilities:

- Extract and parse URLs.
- Identify suspicious domain structures.
- Detect IP-address hosts and deceptive URL syntax.
- Examine excessive subdomains and unusual URL patterns.
- Avoid automatically visiting submitted destinations.

A suspicious-looking URL is not necessarily malicious.

### 3.5 Risk Engine

**File:** `src/risk_engine.py`

Responsibilities:

- Combine machine learning outputs with security indicators.
- Handle missing or conflicting evidence.
- Determine an appropriate warning level.
- Communicate uncertainty.

Proposed risk categories:

- Elevated risk
- Caution / verification required
- No major indicators detected

A numerical score must not be described as a calibrated probability of fraud unless calibration has been evaluated.

### 3.6 Explanation Engine

**File:** `src/explanation_engine.py`

Responsibilities:

- Convert structured evidence into understandable explanations.
- Highlight specific suspicious features.
- Provide appropriate safety recommendations.
- Avoid inventing unsupported claims.

If an LLM is used, explanations must remain grounded in the actual detection evidence.

### 3.7 Multilingual Support

**File:** `src/translations.py`

Initial target languages:

- English
- Traditional Chinese

Additional languages may include Bahasa Indonesia or others supported by the team.

Translation quality and phishing-detection accuracy must be evaluated separately.

### 3.8 QR-Code Analysis (Optional)

**File:** `src/qr_decoder.py`

Responsibilities:

- Decode QR content from uploaded images.
- Extract embedded URLs.
- Send the extracted content to the URL analyzer.
- Never automatically open the decoded destination.

## 4. Proposed Module Interfaces

```python
def classify_text(text: str) -> dict:
    """Return model label, score, and availability."""

def detect_rule_signals(text: str) -> list[dict]:
    """Return observed indicators with evidence excerpts."""

def analyze_urls(text: str) -> list[dict]:
    """Inspect extracted URLs without visiting them."""

def assess_risk(
    classifier_result: dict,
    url_evidence: list[dict],
    rule_evidence: list[dict]
) -> dict:
    """Combine evidence and return a risk assessment."""

def generate_explanation(
    assessment: dict,
    language: str = "en"
) -> dict:
    """Generate evidence-grounded explanations and guidance."""
```

These interfaces are proposals and must be finalized before independent component development.

## 5. Example Analysis Output

```json
{
  "risk_level": "elevated",
  "score": null,
  "score_type": "not_calibrated",
  "indicators": [
    {
      "type": "credential_request",
      "evidence": "Verify your password",
      "severity": "high"
    }
  ],
  "uncertainty": [
    "Sender authenticity has not been verified"
  ],
  "recommended_actions": [
    "Do not submit credentials through the link",
    "Verify using a known official channel"
  ],
  "analysis_status": "completed"
}
```

This is an illustrative output contract, not an actual model prediction.

## 6. Data and Model Evaluation

The team should maintain clear definitions for spam, phishing, legitimate communication, and scam-related indicators.

Potential evaluation components:

1. Rule-based baseline.
2. TF-IDF and Logistic Regression classifier.
3. Hybrid evidence-based system.

Recommended metrics:

- Precision
- Recall
- F1-score
- Confusion matrix
- False-positive rate
- Error analysis by language where feasible

Avoid data leakage between training and testing.

A spam dataset must not automatically be treated as a validated phishing dataset.

Synthetic demonstration examples should be distinguished from independently labeled test data.

## 7. Security and Privacy

The system must:

- Treat all submitted text and URLs as untrusted input.
- Never automatically open suspicious links.
- Never execute submitted scripts.
- Validate and limit file uploads.
- Avoid storing private messages unnecessarily.
- Keep API credentials outside the repository.
- Explain any transfer of submitted data to external AI services.
- Avoid displaying unsupported claims of certainty.

## 8. Testing Strategy

**Unit tests**

Test individual modules such as URL parsing, input validation, phishing rules, and risk aggregation.

**Integration tests**

Verify that modules exchange compatible outputs and handle errors.

**Model evaluation**

Test the classifier on appropriately labeled, held-out data.

**Human-centered tests**

Where feasible, assess whether users understand warnings and choose appropriate verification actions.

## 9. Proposed Development Priorities

### Phase 1 — Foundation

- Finalize interfaces.
- Implement input validation.
- Implement basic rule detection.
- Build initial Streamlit interface.

### Phase 2 — Detection

- Train baseline classifier.
- Implement static URL analysis.
- Integrate classifier and rules.

### Phase 3 — Explainability

- Build evidence-grounded explanations.
- Implement safe-action recommendations.
- Add multilingual presentation.

### Phase 4 — Evaluation

- Test representative examples.
- Evaluate detection performance.
- Document false positives and limitations.
- Prepare final demonstration.

## 10. Team Collaboration

This architecture is a shared technical proposal.

There is no designated team leader.

Component responsibilities will be allocated after the team's role-selection discussion.

Major architectural decisions should be discussed collaboratively, documented, and reviewed through GitHub pull requests.

Repository administration does not imply project leadership.

## 11. Current Implementation Status

The repository currently contains initial placeholder files and project documentation.

The architecture described here is proposed and should not be interpreted as completed functionality.

Actual implementation progress must be tracked through code, tests, GitHub Issues, and pull requests.

---

**ScamShield AI — Detect suspicious signals. Explain the evidence. Support safer decisions.**
