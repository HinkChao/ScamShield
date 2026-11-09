# Contributing to ScamShield AI

This is a jointly developed hackathon project. **There is no designated team leader.** Repository administrative permissions are technical access controls, not authority over project decisions. Functional responsibilities are provisional until the Discord role vote is complete.

## Working agreements

- Discuss significant architectural, product, safety, or dataset changes before implementation.
- Keep work traceable in GitHub Issues and pull requests; do not preassign ownership while voting is underway.
- Each issue should state its acceptance criteria, dependencies, and tests. A person taking a task owns its completion, not the team.
- Aim for at least one peer review before merge. Review each other's work respectfully regardless of discipline or experience.
- Prefer consensus for scope decisions; record unresolved choices and a documented fallback instead of letting an administrator silently decide.
- Credit actual contributions in `docs/contributions.md` when the team agrees on a format.

## Branches and commits

Base branches on the current `main`; examples:

- `docs/architecture-review`
- `feature/url-static-checks`
- `feature/text-baseline`
- `test/ambiguous-cases`
- `fix/input-validation`

Keep pull requests focused. Use informative commit titles (e.g., `docs: define evidence schema`). Avoid pushing directly to `main` when a feature branch is feasible. Do not force-push shared branches without coordination.

## Pull request checklist

- [ ] Purpose and scope are described.
- [ ] Existing files/changes from teammates are preserved.
- [ ] Tests or manual verification steps are described.
- [ ] Safety and privacy implications have been considered.
- [ ] New dependencies and datasets have provenance and license notes.
- [ ] No credentials, identifying private data, or live malicious links have been added.
- [ ] User-facing risk explanations do not assert facts the system cannot verify.

## Review expectations

- Prefer questions and reproducible evidence over ungrounded criticism.
- Treat disagreement as a technical discussion; document tradeoffs.
- A merge is not proof of an individual's project leadership.
- If the demo deadline approaches, prioritize the tested end-to-end workflow over unintegrated enhancements.

## Reporting problems

Use GitHub Issues for bugs, integration blockers, model failures, and evaluation gaps. For vulnerabilities, avoid publishing exploitable details or private examples in a public issue; coordinate privately with repository maintainers first.
