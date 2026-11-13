"""Tests for static URL inspection (src/url_analyzer.py)."""
import socket
import urllib.request

import pytest

from src import url_analyzer
from src.url_analyzer import (
    INDICATOR_DESCRIPTIONS,
    MAX_TEXT_LENGTH,
    MAX_URLS,
    analyze_urls,
    extract_urls,
)
from src.risk_engine import assess_risk


def types_of(result):
    return {item["type"] for item in result["indicators"]}


def only(text):
    results = analyze_urls(text)
    assert len(results) == 1, results
    return results[0]


# --- No-link and invalid input ------------------------------------------------

def test_no_link_input_returns_empty_list():
    assert analyze_urls("Hi! Our meeting starts at 3 PM tomorrow.") == []
    assert analyze_urls("") == []


def test_times_and_prose_with_colons_are_not_links():
    assert analyze_urls("Meet at 10:30. JavaScript: the good parts.") == []


def test_non_string_raises_type_error():
    with pytest.raises(TypeError):
        analyze_urls(None)


def test_oversized_text_raises_value_error():
    with pytest.raises(ValueError):
        analyze_urls("a" * (MAX_TEXT_LENGTH + 1))


# --- Ordinary URLs ------------------------------------------------------------

def test_ordinary_https_url_has_no_indicators():
    result = only("See https://www.example.com/news for details.")
    assert result["status"] == "analyzed"
    assert result["url"] == "https://www.example.com/news"
    assert result["hostname"] == "www.example.com"
    assert result["indicators"] == []


def test_https_is_never_reported_as_a_safety_signal():
    result = only("https://example.com")
    for item in result["indicators"]:
        assert "safe" not in item["type"]
    assert "secure" not in " ".join(types_of(result))


def test_trailing_punctuation_is_not_part_of_url():
    assert extract_urls("Go to https://example.com/login.") == [
        "https://example.com/login"
    ]
    assert extract_urls("(see https://example.com/a)") == [
        "https://example.com/a"
    ]


def test_balanced_parentheses_are_kept():
    url = "https://en.wikipedia.org/wiki/Foo_(bar)"
    assert extract_urls(f"Read {url}.") == [url]


def test_url_next_to_chinese_text_is_extracted():
    text = "請立即點擊https://example.com/verify驗證您的帳戶。"
    assert extract_urls(text) == ["https://example.com/verify"]


def test_www_link_without_scheme():
    result = only("Visit www.example.com/login today")
    assert result["hostname"] == "www.example.com"
    assert "insecure_http" not in types_of(result)


def test_email_address_is_not_a_link():
    assert analyze_urls("Contact help@www.example.com") == []


def test_hostname_is_lowercased():
    assert only("https://WWW.Example.COM/")["hostname"] == "www.example.com"


# --- Deceptive syntax ---------------------------------------------------------

def test_userinfo_trick_reports_real_destination():
    result = only("Login: https://example.com@attacker.example/login")
    assert result["status"] == "analyzed"
    assert result["hostname"] == "attacker.example"
    assert "userinfo_in_url" in types_of(result)
    item = next(i for i in result["indicators"] if i["type"] == "userinfo_in_url")
    assert item["severity"] == "high"
    assert "attacker.example" in item["evidence"]


def test_userinfo_with_multiple_at_signs_uses_last():
    result = only("http://bank.com@login@attacker.example/")
    assert result["hostname"] == "attacker.example"


def test_backslash_trick_matches_browser_destination():
    result = only(r"https://attacker.example\@bank.example/")
    assert result["hostname"] == "attacker.example"
    assert "backslash_in_url" in types_of(result)


def test_percent_encoded_hostname_is_decoded_and_flagged():
    result = only("https://%61ttacker.example/")
    assert result["hostname"] == "attacker.example"
    assert "encoded_hostname" in types_of(result)


def test_insecure_http_is_low_severity():
    result = only("http://example.com/")
    item = next(i for i in result["indicators"] if i["type"] == "insecure_http")
    assert item["severity"] == "low"


def test_punycode_hostname():
    result = only("https://xn--pple-43d.com/")
    assert "punycode_hostname" in types_of(result)


def test_unicode_hostname():
    # Cyrillic "а" imitating Latin "a"
    result = only("https://аpple.com/")
    assert "unicode_hostname" in types_of(result)
    item = next(i for i in result["indicators"] if i["type"] == "unicode_hostname")
    assert "xn--" in item["evidence"]


def test_embedded_domain_in_subdomain():
    result = only("https://paypal.com.account-verify.example/")
    assert "embedded_domain_name" in types_of(result)


@pytest.mark.parametrize("url", [
    "https://www.example.com.au/",
    "https://www.bbc.co.uk/",
    "https://www.ntu.edu.tw/",
])
def test_country_domains_are_not_embedded_domains(url):
    assert "embedded_domain_name" not in types_of(only(url))


def test_excessive_subdomains():
    result = only("https://a.b.c.d.example.org/")
    assert "excessive_subdomains" in types_of(result)


def test_long_url():
    url = "https://example.com/" + "a" * 150
    result = only(url)
    assert "long_url" in types_of(result)


# --- Ports --------------------------------------------------------------------

def test_unusual_port_is_flagged():
    result = only("https://example.com:8443/login")
    assert result["hostname"] == "example.com"
    assert "non_standard_port" in types_of(result)


def test_default_port_is_not_flagged():
    assert "non_standard_port" not in types_of(only("https://example.com:443/"))


@pytest.mark.parametrize("url", [
    "https://example.com:abc/",
    "https://example.com:99999/",
])
def test_malformed_port_is_invalid(url):
    result = only(url)
    assert result["status"] == "invalid"
    assert result["reason"] == "invalid_port"
    assert result["hostname"] is None


# --- IP hosts -----------------------------------------------------------------

@pytest.mark.parametrize("url,host", [
    ("http://192.168.10.5/login", "192.168.10.5"),
    ("http://[2001:db8::1]/", "2001:db8::1"),
])
def test_ip_address_host(url, host):
    result = only(url)
    assert result["hostname"] == host
    assert "ip_address_host" in types_of(result)


@pytest.mark.parametrize("url", [
    "http://3232235777/",
    "http://0x7f.1/",
])
def test_obfuscated_ip_host(url):
    assert "obfuscated_ip_host" in types_of(only(url))


# --- Malformed and unsupported ------------------------------------------------

@pytest.mark.parametrize("text,reason", [
    ("ftp://files.example.com/a", "unsupported_scheme"),
    ("javascript:alert(1)", "unsupported_scheme"),
    ("data:text/html,<b>hi</b>", "unsupported_scheme"),
    ("https:///nohost", "missing_host"),
    ("http://", "missing_host"),
    ("https://exa_mple..com/", "invalid_hostname"),
    ("https://[not-an-ip]/", "unparseable"),
])
def test_malformed_or_unsupported_urls_are_invalid(text, reason):
    result = only(text)
    assert result["status"] == "invalid"
    assert result["reason"] == reason
    assert result["indicators"] == []


def test_overlong_url_is_invalid():
    result = only("https://example.com/" + "a" * 3000)
    assert result["reason"] == "url_too_long"


# --- Duplicates and limits ----------------------------------------------------

def test_duplicate_urls_reported_once():
    text = "https://example.com/a and again https://example.com/a!"
    assert [r["url"] for r in analyze_urls(text)] == ["https://example.com/a"]


def test_multiple_urls_keep_order():
    text = "first http://a.example then https://b.example"
    assert [r["hostname"] for r in analyze_urls(text)] == ["a.example", "b.example"]


def test_url_limit_marks_analysis_incomplete():
    text = " ".join(f"https://h{i}.example/" for i in range(MAX_URLS + 5))
    results = analyze_urls(text)
    assert len(results) == MAX_URLS + 1
    assert results[-1]["status"] == "invalid"
    assert results[-1]["reason"] == "url_limit_reached"


# --- Contract and safety ------------------------------------------------------

def test_every_result_matches_interface_contract():
    text = (
        "https://example.com@attacker.example http://1.2.3.4:8080/x "
        "ftp://x.example https://example.com:abc/"
    )
    for result in analyze_urls(text):
        assert set(result) >= {"url", "hostname", "indicators", "status"}
        assert result["status"] in {"analyzed", "invalid"}
        for item in result["indicators"]:
            assert set(item) == {"type", "evidence", "severity"}
            assert item["severity"] in {"low", "medium", "high"}
            assert item["evidence"]
            assert item["type"] in INDICATOR_DESCRIPTIONS


def test_no_network_access(monkeypatch):
    def blocked(*args, **kwargs):
        raise AssertionError("url_analyzer attempted network access")

    monkeypatch.setattr(socket, "socket", blocked)
    monkeypatch.setattr(socket, "create_connection", blocked)
    monkeypatch.setattr(socket, "getaddrinfo", blocked)
    monkeypatch.setattr(urllib.request, "urlopen", blocked)

    analyze_urls(
        "https://example.com@attacker.example http://3232235777 "
        "https://xn--pple-43d.com www.example.com"
    )


def test_module_imports_no_network_libraries():
    source = open(url_analyzer.__file__, encoding="utf-8").read()
    for forbidden in ("requests", "urlopen", "socket", "http.client", "tldextract"):
        assert forbidden not in source.split('"""', 2)[-1], forbidden


# --- Risk Engine integration --------------------------------------------------

def test_deceptive_url_raises_risk_and_keeps_hostname():
    urls = analyze_urls("Verify now: https://myuni.edu@attacker.example/login")
    assessment = assess_risk(None, urls, [])
    assert assessment["risk_level"] == "elevated"
    url_items = [i for i in assessment["indicators"] if i["source"] == "url"]
    assert any("attacker.example" in i["evidence"] for i in url_items)


def test_invalid_url_becomes_uncertainty_not_verdict():
    urls = analyze_urls("Open ftp://files.example.com/a")
    assessment = assess_risk({"status": "ok", "label": "legitimate"}, urls, [])
    assert assessment["risk_level"] == "caution"
    assert any("URL" in u for u in assessment["uncertainty"])


def test_clean_https_link_does_not_claim_safety():
    urls = analyze_urls("Schedule: https://www.example.com/calendar")
    assessment = assess_risk({"status": "ok", "label": "legitimate"}, urls, [])
    assert assessment["risk_level"] == "no_major_indicators"
    assert any("not guarantee" in a for a in assessment["recommended_actions"])
