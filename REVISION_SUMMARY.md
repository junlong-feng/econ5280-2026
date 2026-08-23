# Website revision summary

This repository is a companion website only. It does not contain the lecture-note prose, LaTeX source, PDF output, or PDF workflow.

## Content retained

The website retains all 33 R examples from the completed lecture-note project. Their code is preserved byte for byte; only each fence is changed to `{webr}` or `{r}` to select its runtime. Every example has one short heading and one short description.

The examples previously placed in the matrix and probability appendices are grouped with Chapters 2 and 3 so the site remains an 11-chapter companion:

| Chapter | R examples | Runtime |
|---|---:|---|
| 1. Introduction | 1 | Quarto Live/WebR |
| 2. Matrix Algebra | 4 | Quarto Live/WebR |
| 3. Probability | 3 | Quarto Live/WebR |
| 4. Statistics and Regression | 5 | Quarto Live/WebR |
| 5. Randomized Controlled Trials | 5 | Quarto Live/WebR |
| 6. Causal Forest | 2 | GitHub Codespaces |
| 7. Doubly Robust Learning | 2 | GitHub Codespaces |
| 8. Regression Discontinuity | 2 | Quarto Live/WebR |
| 9. Instrumental Variables and LATE | 1 | Quarto Live/WebR |
| 10. Neural Networks | 3 | Quarto Live/WebR |
| 11. Difference-in-Differences and Event Studies | 5 | GitHub Codespaces |

## Verification

`examples_manifest.json` records the source path and SHA-256 hash of every retained R block. `python3 scripts/check_site.py` verifies the title, page inventory, example count, hashes, runtime fences, description length, data copies, and absence of `.tex` and `.pdf` files before every GitHub Pages deployment.
