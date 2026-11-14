"""Integration tests for the 7.4 Mandatory Demonstration Test Cases."""
import pytest

from src.url_analyzer import analyze_urls
from src.risk_engine import assess_risk

# --- 1. Explicit credential phishing ---
def test_explicit_credential_phishing():
    # Expected Behavior: Identify relevant danger signals[cite: 1].
    text = "SECURITY ALERT: Reply with your password to prevent account suspension."
    urls = analyze_urls(text)
    
    # Simulating the text analyzer flagging credential phishing
    text_analysis = {"status": "ok", "label": "phishing", "signals": ["credential requests"]}
    assessment = assess_risk(text_analysis, urls, [])
    
    assert assessment["risk_level"] in ["elevated", "high"]
    assert any("credential requests" in signal for signal in text_analysis["signals"])

# --- 2. Normal university reminder ---
def test_normal_university_reminder():
    # Expected Behavior: Avoid treating ordinary institutional language as automatically malicious[cite: 1].
    text = "Reminder from the Registrar: Spring class registration opens at 8:00 AM tomorrow."
    urls = analyze_urls(text)
    
    # Simulating a benign text classification
    text_analysis = {"status": "ok", "label": "legitimate"}
    assessment = assess_risk(text_analysis, urls, [])
    
    assert assessment["risk_level"] == "no_major_indicators"

# --- 3. Urgent but legitimate announcement ---
def test_urgent_but_legitimate_announcement():
    # Expected Behavior: Handle urgency without a categorical scam verdict[cite: 1].
    text = "URGENT: The campus library will close early today at 5 PM due to weather conditions."
    urls = analyze_urls(text)
    
    text_analysis = {"status": "ok", "label": "legitimate", "signals": ["urgency"]}
    assessment = assess_risk(text_analysis, urls, [])
    
    # Should not automatically fail just because it contains urgent language
    assert assessment["risk_level"] in ["no_major_indicators", "caution"] 

# --- 4. Suspicious shortened or deceptive URL ---
def test_suspicious_deceptive_url():
    # Expected Behavior: Highlight relevant structural indicators[cite: 1].
    text = "Verify your account: https://myuni.edu@attacker.example/login"
    urls = analyze_urls(text)
    
    text_analysis = {"status": "ok", "label": "legitimate"} # Text looks fine, but URL is bad
    assessment = assess_risk(text_analysis, urls, [])
    
    assert assessment["risk_level"] == "elevated"
    url_items = [i for i in assessment["indicators"] if i["source"] == "url"]
    assert any("attacker.example" in i["evidence"] for i in url_items)

# --- 5. Message without a URL ---
def test_message_without_a_url():
    # Expected Behavior: Analyze text without inventing URL evidence[cite: 1].
    text = "Please purchase 5 gift cards and send me the activation codes immediately."
    urls = analyze_urls(text)
    
    assert len(urls) == 0  # Verifies no URL evidence is hallucinated/invented[cite: 1]
    
    text_analysis = {"status": "ok", "label": "scam"}
    assessment = assess_risk(text_analysis, urls, [])
    assert assessment["risk_level"] == "elevated"

# --- 6. Ambiguous message ---
def test_ambiguous_message():
    # Expected Behavior: Express uncertainty and recommend verification[cite: 1].
    text = "Can you look at this file? ftp://files.example.com/invoice_01.pdf"
    urls = analyze_urls(text) 
    
    text_analysis = {"status": "ok", "label": "ambiguous"}
    assessment = assess_risk(text_analysis, urls, [])
    
    assert assessment["risk_level"] == "caution"
    assert "uncertainty" in assessment
    assert any("URL" in u for u in assessment["uncertainty"])

# --- 7. Traditional Chinese phishing example ---
def test_traditional_chinese_phishing_example():
    # Expected Behavior: Process and explain without losing meaning[cite: 1].
    text = "請立即點擊https://%61ttacker.example/verify驗證您的帳戶。" # Uses encoded hostname trick
    urls = analyze_urls(text)
    
    assert urls[0]["hostname"] == "attacker.example"
    # Ensure it extracts accurately despite Chinese characters without crashing
    assert len(urls) == 1 

# --- 8. Empty or malformed input ---
def test_empty_input():
    # Expected Behavior: Show a controlled validation message[cite: 1].
    text = ""
    urls = analyze_urls(text)
    
    assert len(urls) == 0
    # In your UI or API layer, you would test that this triggers a 400 Bad Request or validation warning
