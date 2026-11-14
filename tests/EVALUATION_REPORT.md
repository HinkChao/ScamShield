# Test Dataset Evaluation Report

## 1. Overview
This report evaluates the ScamShield risk analysis engine against the 7.4 Mandatory Demonstration Test Cases. 

## 2. False Positives
* **Result:** 0 False Positives.
* **Details:** The system successfully identified normal university reminders and urgent legitimate announcements as safe, correctly avoiding overly aggressive flagging.

## 3. False Negatives (Action Required)
* **Result:** 2 False Negatives identified during initial testing.
* **Details:** `test_explicit_credential_phishing` and `test_message_without_a_url` failed. The `assess_risk` function currently caps the threat score at `caution` if no URL is present, even when the text analyzer flags the input as explicit phishing or a scam. 
* **Resolution:** Bug 001 logged. Awaiting developer patch to adjust risk weighting for text-only threats.