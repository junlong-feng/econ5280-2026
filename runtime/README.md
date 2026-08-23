# Runtime design

The public site uses Quarto Live/WebR wherever the original example and its packages work in a browser. Chapters 6, 7, and 11 use native R in one persistent GitHub Codespace so the original package workflows remain intact.

The GitHub Pages build never executes native R. It displays those `{r}` cells as static code, while the Codespace opens the same `.qmd` files and provides **Run Cell**.

The included dev container installs R, Quarto, and every package needed by the native examples. Its post-create command runs `scripts/test_native_runtime.R` automatically. Full setup and classroom instructions are in `CODESPACES.md`.
