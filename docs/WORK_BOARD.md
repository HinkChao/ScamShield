# Work board — provisional, unassigned

**Choose owners only after the Discord poll.** These are task areas and review requests, not leadership titles.

| Priority | Task / proposed issue | Module(s) | Acceptance |
|---|---|---|---|
| P0 | Integrate reviewed project documentation (PR #3) | README, CONTRIBUTING, docs | Approved scope and collaboration rules |
| P0 | Review phishing-rule baseline (PR #4) | `src/phishing_rules.py`, `tests/test_rules.py` | Tests pass; limitations stated |
| P0 | Static URL inspection | `src/url_analyzer.py`, `tests/test_urls.py` | Safe parsing, no navigation, malformed URL tests |
| P0 | Minimal Streamlit user flow | `app.py` | Paste message → computed evidence → action; handles errors |
| P0 | Evidence-grounded risk integration | `src/risk_engine.py`, `src/explanation_engine.py` | Stable output contract and uncertainty |
| P1 | ML baseline and provenance | `src/text_classifier.py`, `scripts/train_model.py` | Held-out evaluation; data/license documented |
| P1 | End-to-end test and quality audit | `tests/test_integration.py`, `scripts/evaluate_model.py` | Reproducible runs and at least one failure case |
| P1 | English / Traditional Chinese UX | `src/translations.py` | Verified messages and readable guidance |
| P1 | Pitch, research and outreach | `docs/pitch.md`, `docs/evaluation.md` | Evidence-based 10-minute story and contributions |
| P2 | Local QR decoding (optional) | `src/qr_decoder.py` | Decode only; never open extracted URL |

## Ready-to-work rules
- Look at open PRs to avoid duplicate implementation.
- Claim one narrowly scoped issue and post planned branch name.
- Identify one collaborator to review. No central lead is required.
- Record dependencies in issue descriptions.
- Post progress and blockers asynchronously on Discord.
- Merge to `main` after peer review and passing tests.
