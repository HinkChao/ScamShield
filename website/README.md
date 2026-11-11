# ScamShield AI Project Hub

A public static website for the ScamShield hackathon. **GitHub is the single source of truth; Vercel only hosts the website.** This does not replace the Python/Streamlit detection application.

## Repository placement

Add this entire `website/` folder to `HinkChao/ScamShield` on a feature branch. Do not commit directly to `main`. Open a pull request for team review.

## Vercel setup (after merging the PR)

1. In Vercel, select **Add New → Project** and import the `HinkChao/ScamShield` GitHub repository.
2. In project configuration set **Root Directory** to `website`.
3. Set **Framework Preset** to `Other` (static HTML/CSS/JavaScript).
4. Leave the build command blank; the output is the `website` directory itself.
5. Use a preview deployment first. After review, deploy the chosen `main` branch to production.
6. Vercel's Git integration automatically builds previews for PRs and deploys the configured production branch.

Do not put GitHub PATs or secrets in browser JavaScript. The hub fetches publicly accessible GitHub Issues and falls back to direct issue links if API access fails.

## Review checklist
- Verify team consent to publish names.
- Confirm each proposed role and ownership on GitHub.
- Check Issue links and any updated acceptance criteria.
- Confirm the Streamlit demo is functional before adding a live demo URL.
- Keep scam-analysis logic in the existing Python app, not in this site.

## Local preview

From the `website/` directory run:

```bash
python -m http.server 8000
```

Then visit `http://localhost:8000`.
