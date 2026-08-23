#!/usr/bin/env Rscript

# Fast native-R smoke test for Chapters 6, 7, and 11. This deliberately fits
# each estimator instead of checking only whether namespaces load.

required <- c(
  "grf", "DiagrammeR", "did", "fixest", "lmtest", "sandwich"
)
missing <- required[!vapply(required, requireNamespace, logical(1), quietly = TRUE)]
if (length(missing)) {
  stop("Missing native-R package(s): ", paste(missing, collapse = ", "))
}

for (package in required) {
  cat(package, as.character(utils::packageVersion(package)), "\n")
}

set.seed(5280)
n <- 120
W <- matrix(stats::rnorm(n * 4), nrow = n)
D <- stats::rbinom(n, 1, stats::plogis(0.3 * W[, 1]))
Y <- W[, 2] + pmax(W[, 1], 0) * D + stats::rnorm(n)

forest <- grf::causal_forest(
  W, Y, D,
  num.trees = 100,
  num.threads = 1,
  seed = 5280
)
forest.prediction <- predict(forest, W[1:5, , drop = FALSE],
                             num.threads = 1)$predictions
stopifnot(length(forest.prediction) == 5L,
          all(is.finite(forest.prediction)))
tree.widget <- plot(grf::get_tree(forest, 1))
stopifnot(inherits(tree.widget, "htmlwidget"))

ids <- 1:120
cohort <- rep(c(0, 3, 4), each = 40)
unit.effect <- stats::rnorm(length(ids))
panel <- merge(
  expand.grid(id = ids, t = 1:5),
  data.frame(id = ids, G = cohort, alpha = unit.effect),
  by = "id",
  sort = TRUE
)
panel$D <- as.integer(panel$G > 0 & panel$t >= panel$G)
panel$Y <- panel$alpha + 0.2 * panel$t +
  panel$D * (1 + 0.25 * (panel$t - panel$G)) +
  stats::rnorm(nrow(panel))

att <- did::att_gt(
  yname = "Y", tname = "t", idname = "id", gname = "G",
  xformla = ~1, data = panel, panel = TRUE,
  control_group = "notyettreated", est_method = "dr",
  base_period = "universal", bstrap = FALSE, cores = 1
)
stopifnot(length(att$att) > 0L, all(is.finite(att$att)))

fixest::setFixest_nthreads(1)
panel$G_sunab <- ifelse(panel$G == 0, 1000, panel$G)
sunab.fit <- fixest::feols(
  Y ~ sunab(G_sunab, t, ref.p = -1) | id + t,
  data = panel,
  cluster = ~id,
  nthreads = 1
)
stopifnot(length(stats::coef(sunab.fit)) > 0L,
          all(is.finite(stats::coef(sunab.fit))))

ols.fit <- stats::lm(Y ~ D + W[, 1])
ols.robust <- lmtest::coeftest(
  ols.fit,
  vcov. = sandwich::vcovHC(ols.fit, type = "HC0")
)
stopifnot(all(is.finite(ols.robust)))

cat("Native Codespaces runtime smoke test: PASS\n")
