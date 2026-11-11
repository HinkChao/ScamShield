# Start here: ScamShield team workflow

**Shared project, no designated team leader.** GitHub owner/admin permissions are administrative, not decision-making authority. Role preferences remain open until the team agrees.

## 1. Join and choose a task
1. Accept an invitation to `HinkChao/ScamShield` using your own GitHub account.
2. Check open pull requests and the task map in [WORK_BOARD.md](WORK_BOARD.md) before starting.
3. After the Discord poll, agree on a task with teammates; create or claim an Issue. **Do not claim someone else's work by surprise.**
4. Each task has a point-of-contact and a reviewer, not a project leader. Anyone may propose changes.

## 2. Work on a feature branch
```bash
git clone https://github.com/HinkChao/ScamShield.git
cd ScamShield
git switch main
git pull --ff-only origin main
git switch -c feature/short-description
```

Choose a unique branch name (examples: `feature/ml-baseline`, `feature/url-analysis`, `test/evaluation`). Don't commit unfinished work directly to `main`.

## 3. Build and test
```bash
python -m pip install -r requirements-dev.txt
python scripts/check_environment.py
python -m pytest -q
```

Some existing modules are placeholders and will become functional through separate PRs. A green setup check is **not** evidence of phishing-detection accuracy.

## 4. Submit your contribution
```bash
git status
git add path/to/your_file.py tests/test_your_file.py
git commit -m "feat: describe the change"
git push -u origin feature/short-description
```
Open a PR from your feature branch into `main`; explain what changed and what was tested. Ask another teammate to review. Avoid merging an untested component simply to meet a deadline.

## 5. Working in Google Colab
Colab is a development environment, **not** GitHub itself. Use a fresh feature branch, write `.py` files inside the cloned repo, test, then push using your own GitHub credentials through a hidden prompt or a trusted credential manager. Never paste a token in the notebook source, output, Discord, or PR.

**Colab runtime resets:** local unsaved/unpushed changes may disappear. Push changes regularly to a feature branch.

## 6. Shared rules
- Agree on interfaces in [INTERFACES.md](INTERFACES.md) before wiring components together.
- Use synthetic test samples. Don't commit real private messages, passwords, tokens, or secret keys.
- No automatic opening/fetching of untrusted user URLs.
- Cite dataset and model sources and licenses.
- Report uncertainty and failure cases, not only successes.
- Preserve attribution to all contributors; repo ownership is not team leadership.

## 7. Initial PRs
- PR #3: documentation and architecture (await review).
- PR #4: rule-based phishing detector and tests (await review).

This setup PR is independent of those changes; review and merge each separately.
