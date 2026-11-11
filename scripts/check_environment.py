"""Quick structural checks; not a full application validation."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
NEEDED = [
    "app.py", "src/phishing_rules.py", "src/url_analyzer.py",
    "src/risk_engine.py", "tests/test_rules.py", "tests/test_urls.py",
    "docs/TEAM_START_HERE.md", "docs/INTERFACES.md",
]

def main() -> None:
    missing = [path for path in NEEDED if not (ROOT / path).is_file()]
    if missing:
        raise SystemExit("Missing project paths: " + ", ".join(missing))
    print("Repository structure: OK (implementation may still be incomplete)")

if __name__ == "__main__":
    main()
