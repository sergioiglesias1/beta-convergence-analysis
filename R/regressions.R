library(sandwich)
library(lmtest)
library(car)

root <- getwd()
if (basename(root) == "R") root <- dirname(root)

data_path <- file.path(root, "data", "processed", "clean_data.csv")
tables_dir <- file.path(root, "results", "tables")
logs_dir <- file.path(root, "results", "logs")

if (!file.exists(data_path)) {
  stop(paste0(data_path, " not found. Run src/fetch_data.py and src/etl.py first."))
}

dir.create(tables_dir, recursive = TRUE, showWarnings = FALSE)
dir.create(logs_dir, recursive = TRUE, showWarnings = FALSE)

log_path <- file.path(logs_dir, "regressions_output.txt")
sink(log_path, split = TRUE)
on.exit(sink(), add = TRUE)

df <- read.csv(data_path, stringsAsFactors = FALSE)
df$developed <- as.integer(df$group == "Developed")

periods <- list(
  list(key = "pre_crisis", label = "Pre-Crisis (2004-2008)", horizon = 4),
  list(key = "recuperation", label = "Recuperation (2008-2013)", horizon = 5),
  list(key = "stability", label = "Stability (2013-2018)", horizon = 5),
  list(key = "recent", label = "Recent (2018-2024)", horizon = 6),
  list(key = "full", label = "Full sample (2004-2024)", horizon = 20)
)

# lambda = -log(1 + beta*T)/T
# NA for beta >= 0 (divergence)

implied_speed <- function(beta_pct, horizon) {
  beta <- beta_pct / 100
  arg <- 1 + beta * horizon
  if (is.na(beta) || beta >= 0 || arg <= 0) {
    return(c(lambda = NA_real_, half_life = NA_real_))
  }
  lambda <- -log(arg) / horizon
  c(lambda = lambda, half_life = log(2) / lambda)
}

robust <- function(model) coeftest(model, vcov. = vcovHC(model, type = "HC1"))

section <- function(title) {
  cat("\n", title, "\n", sep = "")
}

rows <- list()

for (p in periods) {
  df$growth <- df[[paste0("growth_", p$key)]]
  df$log_y0 <- df[[paste0("log_y0_", p$key)]]

  section(paste0("PERIOD: ", p$label, "  (T = ", p$horizon, " years)"))

  uncond <- lm(growth ~ log_y0, data = df)

  cat("\nUnconditional: growth ~ log(y0)\n")
  print(summary(uncond))
  
  cat("\nHC1 robust standard errors:\n")
  print(robust(uncond))

  beta <- coef(uncond)[["log_y0"]]
  speed <- implied_speed(beta, p$horizon)
  robust_se <- sqrt(diag(vcovHC(uncond, type = "HC1")))[["log_y0"]]
  
  cat(sprintf(
    "\nbeta = %.4f (HC1 se = %.4f) | lambda = %s | half-life = %s\n",
    beta, robust_se,
    ifelse(is.na(speed[["lambda"]]), "n.a. (divergence)",
           sprintf("%.2f%%/yr", 100 * speed[["lambda"]])),
    ifelse(is.na(speed[["half_life"]]), "n.a.",
           sprintf("%.0f yrs", speed[["half_life"]]))
  ))

  cond <- lm(
    growth ~ log_y0 + developed, data = df
  )
  
  cat("\nConditional: growth ~ log(y0) + developed\n")
  print(robust(cond))
  
  cat("\nVariance inflation factors:\n")
  print(vif(cond))

  beta_cond <- coef(cond)[["log_y0"]]
  speed_cond <- implied_speed(beta_cond, p$horizon)

  # A significant interaction means separate convergence clubs.
  clubs <- lm(
    growth ~ log_y0 * developed, data = df
  )
  
  cat("\nConvergence clubs: growth ~ log(y0) * developed\n")
  print(robust(clubs))
  interaction_p <- coeftest(clubs, vcov. = vcovHC(clubs, type = "HC1"))[
    "log_y0:developed", "Pr(>|t|)"]

  cat("\nDiagnostics\n")
  bp <- bptest(uncond)
  print(bp)
  cat("\nRESET test for functional form:\n")
  print(resettest(uncond, power = 2:3, type = "fitted"))

  cooks <- cooks.distance(uncond)
  threshold <- 4 / nobs(uncond)
  top <- head(sort(cooks, decreasing = TRUE), 5)

  cat(sprintf("\nCook's distance (threshold 4/n = %.4f), 5 most influential:\n",
              threshold))
  
  print(data.frame(country = df$country_name[as.integer(names(top))],
                   cooks_d = round(as.numeric(top), 4)),
        row.names = FALSE)

  keep <- cooks <= threshold
  beta_trimmed <- coef(lm(growth ~ log_y0, data = df[keep, ]))[["log_y0"]]
  
  cat(sprintf(
    "beta excluding %d influential observations: %.4f (full sample: %.4f)\n",
    sum(!keep), beta_trimmed, beta
  ))

  rows[[p$key]] <- data.frame(
    period = p$label,
    horizon = p$horizon,
    n = nobs(uncond),
    beta_uncond = beta,
    se_hc1 = robust_se,
    p_value = robust(uncond)["log_y0", "Pr(>|t|)"],
    r_squared = summary(uncond)$r.squared,
    lambda_pct = 100 * speed[["lambda"]],
    half_life = speed[["half_life"]],
    beta_cond = beta_cond,
    lambda_cond_pct = 100 * speed_cond[["lambda"]],
    beta_trimmed = beta_trimmed,
    bp_p_value = bp$p.value,
    club_interaction_p = interaction_p,
    stringsAsFactors = FALSE
  )
}

summary_table <- do.call(rbind, rows)
rownames(summary_table) <- NULL

section("SUMMARY: unconditional and conditional beta by period")
print(format(summary_table, digits = 3), row.names = FALSE)

out_path <- file.path(tables_dir, "regression_summary.csv")
write.csv(summary_table, out_path, row.names = FALSE)

cat("\nWrote", out_path, "\n")
cat("Wrote", log_path, "\n")

sink()
