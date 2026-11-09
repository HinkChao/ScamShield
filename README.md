# ScamShield AI

**An explainable, multilingual defense against scam and phishing messages.**

ScamShield AI is a collaborative prototype for Problem 4 of the Fall 2026 international hackathon. It aims to help people recognize suspicious messages, understand *which observable signs* support a warning, and choose safer next steps. It is **decision support**, not a guarantee of safety or maliciousness.

## Status

**Planning / repository scaffolding.** The current repository contains empty placeholder modules. Working detection, multilingual analysis, evaluation results, and deployments are not yet implemented. This documentation PR initializes shared expectations without claiming functionality that does not exist.

## Proposed MVP

1. Accept pasted message or email text and optionally a URL.
2. Extract and inspect URL structure **without opening the URL**.
3. Run a transparent warning-indicator baseline and a measured text-classification baseline.
4. Return evidence-grounded explanations, uncertainty, and safe next-step guidance.
5. Provide English and Traditional Chinese explanations (evaluate each language separately).
6. Demonstrate legitimate, suspicious, and ambiguous examples and report failures.

**Stretch goals:** local QR decoding; additional languages; user-reviewed reporting templates. Out of scope: full browser protection, malware execution, deepfake detection, and reliable identification of whether content was AI-generated.

## Architecture and coordination

- [Technical architecture](docs/architecture.md)
- [Contribution guidelines](CONTRIBUTING.md)
- Existing planned modules live in `src/`, experiments in `scripts/`, automated checks in `tests/`, and demo cases in `demo/`.
- Proposed work areas: ML, URL/security, application integration, evaluation/QA, UX/multilingual guidance, product research/documentation. **Roles remain open pending the team's vote. No project leader is designated.**

## Running the application

The application has **not been implemented yet**. Once `app.py` and `requirements.txt` are populated, the anticipated command will be `streamlit run app.py`. Do not expect this to work in the current skeleton.

## Safety and data

Do not submit real passwords, tokens, private messages, or personal information to public demonstrations. Do not visit arbitrary submitted URLs from the analysis pipeline. Keep API keys and raw private datasets out of Git history. Use properly licensed datasets and document provenance, splits, and limitations.

## Collaboration

Create a feature branch, open a pull request, and request peer review. GitHub repository ownership does not confer project leadership. Important architecture and scope decisions should be discussed openly.

## Attribution

Document external libraries, pretrained models, datasets, synthetic examples, and AI assistance in the final project materials.
