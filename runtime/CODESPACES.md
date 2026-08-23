# Native R in GitHub Codespaces

Chapters 6, 7, and 11 run in one persistent Codespace. The classroom computer needs only a browser and a GitHub login.

## Create and test it once

1. Open the `econ5280-2026` repository on GitHub.
2. Choose **Code > Codespaces > Create codespace on main**.
3. Use the two-core machine if GitHub asks for a machine type.
4. Wait for the container build and automatic smoke test to finish.
5. In the terminal, run `Rscript scripts/test_native_runtime.R` once more. Its final line should be `Native Codespaces runtime smoke test: PASS`.

Create this environment before the semester and resume the same Codespace later.

## Before class

1. In GitHub **Settings > Codespaces**, set the default idle timeout to about 150 minutes.
2. Open **Code > Codespaces** in the repository and resume the existing Codespace.
3. If the repository changed, run `git pull --ff-only` in the terminal.
4. Open the required source file:
   - `chapters/chapter06_causal_forest.qmd`
   - `chapters/chapter07_doubly_robust.qmd`
   - `chapters/chapter11_did.qmd`
5. Use **R: Create R terminal** from the command palette.
6. Click **Run Cell** above each `{r}` block in order.

Stop the Codespace after class from <https://github.com/codespaces>. Stopping preserves the installed environment; deleting it does not.

If `.devcontainer/devcontainer.json` changes, pull the commit and run **Codespaces: Rebuild Container** from the command palette. Ordinary changes to descriptions or R examples need no rebuild.
