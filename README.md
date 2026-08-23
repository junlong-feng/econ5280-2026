# ECON 5280: Applied Econometrics

This is the website-only repository for the course companion. Each chapter page contains only the numerical examples from the lecture notes and a short description of each example. The repository contains no LaTeX or PDF source.

See `REVISION_SUMMARY.md` for the complete chapter-by-chapter example inventory and verification method.

## Publish with GitHub Pages

1. Create a GitHub repository named `econ5280-2026` and add this folder's contents.
2. Push the `main` branch.
3. On GitHub, open **Settings > Pages** and choose **GitHub Actions** under **Build and deployment**.
4. Open **Actions** and wait for **Publish Applied Econometrics companion** to finish.
5. Open the deployment URL shown in the completed workflow or in **Settings > Pages**.

Every push to `main` validates the example inventory, renders the Quarto site, and deploys it. To rebuild without changing a file, open the workflow and choose **Run workflow**.

## R runtimes

- Quarto Live/WebR runs Chapters 1–5 and 8–10 directly in the browser.
- Native R in GitHub Codespaces runs Chapters 6, 7, and 11 without replacing the original `grf`, `did`, or `fixest` package code.

The classroom computer therefore needs only a web browser. See `runtime/CODESPACES.md` for the one-time Codespaces setup and classroom sequence.

## Edit the site

- Chapter pages: `chapters/*.qmd`
- Navigation and course title: `_quarto.yml`
- Home page: `index.qmd`
- Appearance: `styles.css`

Run `python3 scripts/check_site.py` before committing. If Quarto is installed locally, preview with `quarto preview` or build with `quarto render --no-execute`.
