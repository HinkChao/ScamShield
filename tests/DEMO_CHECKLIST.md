# ScamShield: Final Demonstration Checklist

## Phase 1: Pre-Flight Checks (Before taking the stage)
- [ ] Pull the latest `main` branch to the presentation laptop (`git pull`).
- [ ] Run `pytest tests/test_demonstration_cases.py` to verify the risk engine bug is resolved and all tests pass.
- [ ] Launch the local ScamShield UI.
- [ ] Open a blank text file containing all 9 test payloads for quick copy-pasting (prevents live-typing errors).

## Phase 2: Live Pitch (The 9 Mandatory Cases)

**1. Explicit credential phishing**
*   **Action:** Paste: *"SECURITY ALERT: Reply with your password to prevent account suspension."*
*   **Speaking Track:** Highlight the system's immediate detection of explicit danger signals.

**2. Normal university reminder**
*   **Action:** Paste: *"Reminder from the Registrar: Spring class registration opens at 8:00 AM tomorrow."*
*   **Speaking Track:** Emphasize that the risk engine does not overreact to ordinary institutional language.

**3. Urgent but legitimate announcement**
*   **Action:** Paste: *"URGENT: The campus library will close early today at 5 PM due to weather conditions."*
*   **Speaking Track:** Demonstrate how the model isolates urgency from malicious intent, avoiding a categorical scam verdict.

**4. Suspicious shortened or deceptive URL**
*   **Action:** Paste: *"Verify your account: https://myuni.edu@attacker.example/login"*
*   **Speaking Track:** Point to the UI highlighting the structural indicator (the deceptive `@` routing).

**5. Message without a URL**
*   **Action:** Paste: *"Please purchase 5 gift cards and send me the activation codes immediately."*
*   **Speaking Track:** Show that the text analyzer correctly flags the scam without inventing or hallucinating URL evidence.

**6. Ambiguous message**
*   **Action:** Paste: *"Can you look at this file? ftp://files.example.com/invoice_01.pdf"*
*   **Speaking Track:** Highlight the "Caution" state, expressing uncertainty and recommending user verification.

**7. Traditional Chinese phishing example**
*   **Action:** Paste: *"請立即點擊https://%61ttacker.example/verify驗證您的帳戶。"*
*   **Speaking Track:** Prove the multi-lingual NLP processes the threat natively without losing meaning.

**8. Empty or malformed input**
*   **Action:** Submit a completely blank input box.
*   **Speaking Track:** Show the controlled validation message that prevents a pipeline crash.

**9. Optional malicious-looking QR**
*   **Action:** Upload the test QR code image file.
*   **Speaking Track:** Demonstrate the sandboxed decoding process that reads the payload without executing the destination link.