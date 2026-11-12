"""Static URL inspection for ScamShield.

Finds links in untrusted text and reports structural warning signs as
evidence. This module NEVER opens, fetches, resolves, follows or executes a
submitted URL: it uses only string parsing from the standard library
(``re``, ``urllib.parse``, ``ipaddress``). No DNS lookups, no HTTP requests,
no reputation services.

Contract (see docs/INTERFACES.md)::

    analyze_urls(text: str) -> list[dict]

Each result::

    {
        "url": str,               # the link exactly as written in the text
        "hostname": str | None,   # destination host a browser would contact
        "indicators": [           # structural observations, NOT verdicts
            {"type": str, "evidence": str, "severity": "low"|"medium"|"high"}
        ],
        "status": "analyzed" | "invalid",
        "reason": str,            # only when status == "invalid"
    }

What an indicator means
-----------------------
An indicator is a heuristic: a structural pattern that phishing links often
use. It is never proof that a link is malicious, and the absence of
indicators is never proof that a link is safe. In particular, HTTPS only
means the connection is encrypted; it says nothing about who runs the site,
so HTTPS never produces a "safe" signal here.

Input limits and errors
-----------------------
- ``text`` must be a ``str``; anything else raises ``TypeError``.
- ``text`` longer than ``MAX_TEXT_LENGTH`` characters raises ``ValueError``.
  Callers should enforce their own input limit before calling.
- At most ``MAX_URLS`` distinct links are analyzed. If more are present, one
  extra ``invalid`` result with reason ``"url_limit_reached"`` is appended
  so downstream code knows the analysis was incomplete.
- A link longer than ``MAX_URL_LENGTH`` characters is not parsed and is
  returned as ``invalid`` with reason ``"url_too_long"``.
- Malformed or unsupported links never raise; they are returned as
  ``invalid`` with a machine-readable ``reason``:
  ``unsupported_scheme``, ``missing_host``, ``invalid_port``,
  ``invalid_hostname``, ``unparseable``, ``url_too_long``.

Known limitations
-----------------
- Only ``http://``, ``https://`` and ``www.`` links are analyzed. Bare
  domains such as ``example.com/login`` (no scheme, no ``www.``) are not
  detected, because they cannot be told apart from file names or ordinary
  text without a public-suffix list.
- Extraction stops at whitespace, CJK punctuation and CJK ideographs, so a
  link written directly against Chinese text (no space) is still found.
  Consequently, hostnames written in Chinese characters are not extracted;
  their Punycode (``xn--``) form is.
- Domain boundaries are guessed without the Public Suffix List, so the
  subdomain-count and embedded-domain checks are approximate.
- Python's ``idna`` codec implements IDNA 2003. Browsers use UTS #46 /
  IDNA 2008, so a small number of unusual Unicode hostnames may be
  normalised differently or rejected here.
- Parsing follows browser (WHATWG) behaviour for the tricks covered by the
  tests (``@`` user-info, backslashes, percent-encoded hosts, numeric IPs),
  but browsers and ``urllib`` can still disagree on other edge cases. Any
  ambiguity is reported, not silently resolved.
- Homoglyphs (``paypa1.com``), brand look-alikes, redirects, URL shorteners
  and the reputation or age of a domain are NOT checked.
"""

from __future__ import annotations

import ipaddress
import re
from urllib.parse import unquote, urlsplit

__all__ = [
    "analyze_urls",
    "extract_urls",
    "INDICATOR_DESCRIPTIONS",
    "MAX_TEXT_LENGTH",
    "MAX_URLS",
    "MAX_URL_LENGTH",
]

MAX_TEXT_LENGTH = 100_000
MAX_URLS = 20
MAX_URL_LENGTH = 2_048
LONG_URL_THRESHOLD = 120
MAX_HOST_LABELS = 4  # e.g. a.b.example.com is fine; one more level is flagged

SUPPORTED_SCHEMES = {"http", "https"}
DEFAULT_PORTS = {80, 443}

# Common generic/country second-level labels. Seeing one of these deep inside
# a hostname (``paypal.com.login.example``) suggests a domain name is being
# imitated inside a subdomain.
_TLD_LIKE_LABELS = {
    "com", "net", "org", "edu", "gov", "mil", "int", "info", "biz", "co", "io",
}

# Plain-language descriptions for the explanation engine to reuse.
INDICATOR_DESCRIPTIONS = {
    "userinfo_in_url": (
        "Text before '@' in a link is ignored by browsers; the link goes to "
        "the host after the '@'."
    ),
    "backslash_in_url": (
        "The link contains a backslash, which browsers treat as '/' and "
        "which can disguise the real destination."
    ),
    "ip_address_host": (
        "The link points to a raw IP address instead of a domain name."
    ),
    "obfuscated_ip_host": (
        "The link hides an IP address in an unusual numeric form."
    ),
    "encoded_hostname": (
        "The link's hostname is percent-encoded, which hides the real "
        "destination."
    ),
    "punycode_hostname": (
        "The hostname uses Punycode (xn--), which can disguise look-alike "
        "characters."
    ),
    "unicode_hostname": (
        "The hostname contains non-ASCII characters that may imitate a "
        "familiar domain."
    ),
    "embedded_domain_name": (
        "A domain-like name appears inside a subdomain, which can make the "
        "link look like it belongs to a different site."
    ),
    "excessive_subdomains": (
        "The hostname has many subdomain levels."
    ),
    "insecure_http": (
        "The link uses unencrypted HTTP. (HTTPS would not prove the site "
        "is safe either.)"
    ),
    "non_standard_port": (
        "The link uses an unusual network port."
    ),
    "long_url": (
        "The link is unusually long, which can hide its real destination."
    ),
}

# --- Extraction ------------------------------------------------------------

# Characters that end a link: whitespace, quotes/angle brackets, CJK
# punctuation, full-width punctuation and CJK ideographs.
_STOP = (
    r"\s<>\"'`"
    r"　-〿"   # CJK symbols and punctuation (。、「」 etc.)
    r"㐀-䶿一-鿿"  # CJK ideographs
    r"！-／：-＠［-｀｛-･"  # full-width punct
)
_URL_RE = re.compile(
    rf"""
    # ASCII-only look-behind instead of \b: CJK characters count as word
    # characters, so \b would miss links written right after Chinese text.
    (?<![a-z0-9+.\-@])
    (?:
        [a-z][a-z0-9+.\-]*://[^{_STOP}]*    # scheme://...
      | (?:javascript|vbscript):[^{_STOP}]+ # script pseudo-URLs
      | data:[a-z]+/[^{_STOP}]*             # data: URIs
      | www\.[^{_STOP}]+                    # www.example.com without scheme
    )
    """,
    re.IGNORECASE | re.VERBOSE,
)
_TRAILING = ".,;:!?'\")]}>*"
_PAIRS = {")": "(", "]": "[", "}": "{"}


def _strip_trailing(candidate: str) -> str:
    """Remove sentence punctuation that is not part of the link."""
    while candidate and candidate[-1] in _TRAILING:
        last = candidate[-1]
        opener = _PAIRS.get(last)
        # Keep a closing bracket that balances one inside the URL,
        # e.g. https://en.wikipedia.org/wiki/Foo_(bar)
        if opener and candidate.count(opener) >= candidate.count(last):
            break
        candidate = candidate[:-1]
    return candidate


def extract_urls(text: str) -> list[str]:
    """Return distinct link candidates in order of first appearance."""
    if not isinstance(text, str):
        raise TypeError("text must be a string")
    seen: set[str] = set()
    urls: list[str] = []
    for match in _URL_RE.finditer(text):
        candidate = _strip_trailing(match.group(0))
        if candidate and candidate not in seen:
            seen.add(candidate)
            urls.append(candidate)
    return urls


# --- Analysis ----------------------------------------------------------------

def _invalid(url: str, reason: str) -> dict:
    return {
        "url": url,
        "hostname": None,
        "indicators": [],
        "status": "invalid",
        "reason": reason,
    }


def _indicator(kind: str, evidence: str, severity: str) -> dict:
    return {"type": kind, "evidence": evidence, "severity": severity}


_NUMERIC_LABEL = re.compile(r"^(?:0x[0-9a-f]*|[0-9]+)$")
_HOST_LABEL = re.compile(r"^[a-z0-9_](?:[a-z0-9_\-]{0,61}[a-z0-9_])?$")


def _classify_ip(host: str) -> str | None:
    """Return 'standard' or 'obfuscated' if the host is an IP address."""
    try:
        ipaddress.ip_address(host)
        return "standard"
    except ValueError:
        pass
    labels = host.split(".")
    # Browsers read hosts like 3232235777, 0x7f.1 or 0177.0.0.1 as IPv4.
    if 1 <= len(labels) <= 4 and all(_NUMERIC_LABEL.match(p) for p in labels):
        return "obfuscated"
    return None


def _analyze_one(url: str) -> dict:
    if len(url) > MAX_URL_LENGTH:
        return _invalid(url, "url_too_long")

    lowered = url.lower()
    if lowered.startswith("www."):
        scheme_given = False
        to_parse = "http://" + url
    else:
        scheme_given = True
        to_parse = url
        scheme = lowered.split(":", 1)[0]
        if scheme not in SUPPORTED_SCHEMES:
            return _invalid(url, "unsupported_scheme")

    indicators: list[dict] = []

    # Browsers treat "\" as "/" in http(s) URLs, so "http://evil.example\@bank.com"
    # really goes to evil.example. Normalise the same way before parsing.
    if "\\" in to_parse:
        to_parse = to_parse.replace("\\", "/")
        indicators.append(_indicator(
            "backslash_in_url",
            f"{url} (backslash treated as '/')",
            "high",
        ))

    try:
        parts = urlsplit(to_parse)
        port = parts.port  # raises ValueError on non-numeric / out-of-range
    except ValueError as exc:
        reason = "invalid_port" if "port" in str(exc).lower() else "unparseable"
        return _invalid(url, reason)

    raw_host = parts.hostname
    if not raw_host:
        return _invalid(url, "missing_host")

    if "%" in raw_host:
        decoded = unquote(raw_host).lower()
        indicators.append(_indicator(
            "encoded_hostname",
            f"{parts.netloc.rsplit('@', 1)[-1]} (decodes to {decoded})",
            "medium",
        ))
        raw_host = decoded

    host = raw_host.rstrip(".")
    if not host:
        return _invalid(url, "missing_host")

    if "@" in parts.netloc:
        user_part = parts.netloc.rsplit("@", 1)[0]
        indicators.append(_indicator(
            "userinfo_in_url",
            f"{user_part}@{host} (actual destination: {host})",
            "high",
        ))

    ip_kind = _classify_ip(host)
    if ip_kind == "standard":
        indicators.append(_indicator(
            "ip_address_host", f"{host} (IP address)", "medium"
        ))
    elif ip_kind == "obfuscated":
        indicators.append(_indicator(
            "obfuscated_ip_host", f"{host} (numeric IP form)", "high"
        ))
    else:
        try:
            ascii_host = host.encode("idna").decode("ascii").lower()
        except UnicodeError:
            return _invalid(url, "invalid_hostname")
        labels = ascii_host.split(".")
        if not all(_HOST_LABEL.match(label) for label in labels):
            return _invalid(url, "invalid_hostname")

        if not host.isascii():
            indicators.append(_indicator(
                "unicode_hostname",
                f"{host} (encoded as {ascii_host})",
                "medium",
            ))
        elif any(label.startswith("xn--") for label in labels):
            try:
                shown = ascii_host.encode("ascii").decode("idna")
            except UnicodeError:
                shown = "undecodable"
            indicators.append(_indicator(
                "punycode_hostname",
                f"{ascii_host} (displays as {shown})",
                "medium",
            ))

        # "paypal.com.account-verify.example": a TLD-like label well before
        # the end of the hostname. Allows example.com.au / example.co.uk.
        embedded = [
            label for label in labels[:-2] if label in _TLD_LIKE_LABELS
        ]
        if embedded and len(labels) >= 3:
            indicators.append(_indicator(
                "embedded_domain_name",
                f"{host} (registered part is likely "
                f"{'.'.join(labels[-2:])})",
                "medium",
            ))
        elif len(labels) > MAX_HOST_LABELS:
            indicators.append(_indicator(
                "excessive_subdomains",
                f"{host} ({len(labels)} levels)",
                "low",
            ))

    if scheme_given and parts.scheme.lower() == "http":
        indicators.append(_indicator(
            "insecure_http", f"{url} (unencrypted http://)", "low"
        ))

    if port is not None and port not in DEFAULT_PORTS:
        indicators.append(_indicator(
            "non_standard_port", f"{host}:{port}", "low"
        ))

    if len(url) > LONG_URL_THRESHOLD:
        indicators.append(_indicator(
            "long_url", f"{url[:60]}... ({len(url)} characters)", "low"
        ))

    return {
        "url": url,
        "hostname": host,
        "indicators": indicators,
        "status": "analyzed",
    }


def analyze_urls(text: str) -> list[dict]:
    """Inspect links in ``text`` without visiting them.

    Returns one result per distinct link, in order of appearance, or ``[]``
    when the text contains no links. See the module docstring for the result
    shape, limits and limitations.
    """
    if not isinstance(text, str):
        raise TypeError("text must be a string")
    if len(text) > MAX_TEXT_LENGTH:
        raise ValueError(
            f"text is {len(text)} characters; the limit is {MAX_TEXT_LENGTH}"
        )

    urls = extract_urls(text)
    results = [_analyze_one(url) for url in urls[:MAX_URLS]]
    if len(urls) > MAX_URLS:
        results.append(_invalid(urls[MAX_URLS], "url_limit_reached"))
    return results
