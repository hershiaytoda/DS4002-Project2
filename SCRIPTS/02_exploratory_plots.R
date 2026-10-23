# Step 2: reproduce the two exploratory figures required by MI3.
# Run from the repository root: Rscript SCRIPTS/02_exploratory_plots.R
# Input: DATA/cleaned_quarterly.csv, produced by 01_preprocess_data.py.
# Outputs: OUTPUT/01_quarterly_trends.png and OUTPUT/02_hpi_growth_distribution.png.
# Uses base R only. These figures describe the data; they do not test hypotheses.

data <- read.csv("DATA/cleaned_quarterly.csv", na.strings = "")
dates <- as.Date(data$quarter_start)
dir.create("OUTPUT", showWarnings = FALSE)

# Separate panels preserve each variable's units and its actual coverage.
# Missing periods stay as gaps rather than being interpolated.
variables <- c("hpi", "mortgage_rate_pct", "unemployment_rate_pct", "active_listings")
labels <- c("Charlottesville metro HPI (1995 Q1 = 100)",
            "U.S. mortgage rate (%)", "Charlottesville city unemployment (%)",
            "Charlottesville metro active listings (quarterly mean)")
colors <- c("#235789", "#A54F19", "#6B4C9A", "#24745A")
png("OUTPUT/01_quarterly_trends.png", width = 1800, height = 1500, res = 180)
par(mfrow = c(4, 1), mar = c(2.8, 4.5, 2.6, 1.2), oma = c(1, 0, 2, 0))
for (i in seq_along(variables)) {
  plot(dates, data[[variables[i]]], type = "l", col = colors[i], lwd = 2,
       xlab = "", ylab = "", main = labels[i], las = 1)
  grid(nx = NA, ny = NULL, col = "#E5E7EB")
  lines(dates, data[[variables[i]]], col = colors[i], lwd = 2)
}
mtext("Quarterly housing-market and economic indicators", outer = TRUE, cex = 1.2)
invisible(dev.off())

# The planned regression outcome is annual HPI growth, not the index level.
growth <- data$hpi_yoy_pct[!is.na(data$hpi_yoy_pct)]
png("OUTPUT/02_hpi_growth_distribution.png", width = 1600, height = 1050, res = 180)
par(mar = c(5, 5, 4, 1.5))
hist(growth, breaks = "FD", col = "#235789", border = "white",
     main = "Distribution of year-over-year Charlottesville HPI growth",
     xlab = "Year-over-year HPI growth (%)", ylab = "Number of quarters", las = 1)
abline(v = 0, col = "#A54F19", lty = 2, lwd = 1.5)
invisible(dev.off())
cat("Saved two exploratory plots in OUTPUT/.\n")
