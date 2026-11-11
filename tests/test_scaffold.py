"""Structure checks, not functionality or model-accuracy tests."""
from pathlib import Path


def test_expected_project_paths_exist():
    root = Path(__file__).resolve().parents[1]
    assert (root / "src" / "url_analyzer.py").is_file()
    assert (root / "src" / "phishing_rules.py").is_file()
    assert (root / "docs" / "INTERFACES.md").is_file()
