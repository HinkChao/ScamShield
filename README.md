# 🛡️ ScamShield AI

### An Explainable, Multilingual Defense Against Scams and Phishing

**Hackathon:** Fall 2026 Collaborative Hackathon  
**Challenge:** Problem 4 — ScamShield AI  
**Project Status:** Early Development  
**Final Showcase:** November 14, 2026

## 🌍 About the Project

ScamShield AI is a collaborative cybersecurity and artificial intelligence project designed to help people identify suspicious digital communications, understand potential risks, and make safer decisions.

The system focuses on phishing and scams delivered through messages, emails, suspicious URLs, and potentially QR codes.

Unlike traditional phishing detectors that only return a warning, ScamShield AI aims to explain **why content may be suspicious** and recommend practical safety actions.

## 🎯 Project Objectives

1. Detect potential phishing and scam patterns using AI and transparent security rules.
2. Explain warning signs through evidence-based risk assessments.
3. Support multilingual users, initially focusing on English and Traditional Chinese.
4. Provide accessible, actionable recommendations.
5. Evaluate detection performance, usability, and system limitations.

## ✨ Planned MVP Features

- Text and email content analysis
- ML-based phishing classification
- Static URL inspection without opening submitted links
- Explainable warning signs
- Risk assessment with uncertainty handling
- English and Traditional Chinese explanations
- Safe-action recommendations

**Optional:** QR-code decoding, additional languages, and campus reporting support.

## 🏗️ Proposed Technology Stack

| Component | Technology |
|---|---|
| Programming Language | Python |
| Web Application | Streamlit |
| Machine Learning | scikit-learn |
| Text Features | TF-IDF |
| URL Analysis | Python URL parsing libraries |
| QR Decoding | OpenCV (optional) |
| Testing | pytest |
| Version Control | GitHub |

## 📁 Repository Structure

```text
ScamShield/
├── app.py
├── requirements.txt
├── src/
│   ├── input_processing.py
│   ├── text_classifier.py
│   ├── phishing_rules.py
│   ├── url_analyzer.py
│   ├── risk_engine.py
│   ├── explanation_engine.py
│   ├── translations.py
│   └── qr_decoder.py
├── scripts/
├── tests/
├── data/
├── models/
├── demo/
└── docs/
```

The existing files are placeholders. Implementation is being developed collaboratively.

## 🤝 Team Collaboration

ScamShield AI operates through **shared responsibility and collaborative decision-making without a designated team leader**.

Project responsibilities will be distributed based on team interests, skills, availability, and the ongoing role-selection discussion.

Repository ownership is an administrative function and does not imply leadership over the project.

Contributors should develop substantial changes on separate branches and propose integration through pull requests.

## 🔐 Security and Responsible AI

- Never automatically open suspicious URLs.
- Treat submitted content as untrusted data.
- Protect user privacy and avoid unnecessary data collection.
- Ground explanations in observable evidence.
- Communicate model uncertainty and limitations.
- Never guarantee that analyzed content is safe.

## 🧪 Evaluation Plan

The team plans to compare a rule-based baseline against an ML-based classifier.

Evaluation will include precision, recall, F1-score, false-positive analysis, representative failure cases, and multilingual testing where feasible.

Results will be documented after implementation and testing.

## 📅 Development Timeline

| Date | Target |
|---|---|
| November 9 | Project setup and scope |
| November 10 | Initial detection components |
| November 11 | Integration |
| November 12 | Evaluation and testing |
| November 13 | Finalization and rehearsal |
| November 14 | Hackathon showcase |

## 📌 Current Status

The project is in its initial setup stage.

Planned features are not yet implemented or validated.

## 📄 License

A project license will be selected through team discussion before public reuse or redistribution.
