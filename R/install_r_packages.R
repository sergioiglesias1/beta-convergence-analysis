required <- c("sandwich", "lmtest", "car")
missing <- setdiff(required, rownames(installed.packages()))

if (length(missing) == 0) {
  cat("All required packages are already installed.\n")
} else {
  cat("Installing:", paste(missing, collapse = ", "), "\n")
  install.packages(missing, repos = "https://cloud.r-project.org")
}
