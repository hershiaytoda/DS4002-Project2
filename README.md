# DS-4002-Project 2

This repository contains Project 2 for Group 4 in DS 4002.

This project examines whether changes in mortgage rates, unemployment, and active listings are associated with year-over-year Charlottesville house-price growth.  We started with **DATA/cleaned_quarterly.csv** for the combined analysis. The three `hpi_vs_*.csv`files are simpler views for individual comparisons, generated from the same data.

## Section 1: Software and platform

Preprocessing: Python 3.12 and pandas 3.0.1, tested on Windows.
Exploratory plots: R 4.6.1, using base R (no add-on packages).
Install the Python dependency with `python -m pip install -r requirements.txt`.

## Section 2: A Map of our documentation

```text
DS4002-Project2/
├── DATA/
│   ├── original_fred/              Individual source CSVs (see Step 1)
│   ├── Raw_Combined_ FRED_Data.csv  Raw input to preprocessing; unchanged
│   ├── cleaned_quarterly.csv       Combined levels and annual changes; 172 quarters
│   ├── hpi_vs_mortgage.csv         HPI and mortgage rates; 172 quarters
│   ├── hpi_vs_unemployment.csv     HPI and city unemployment; 146 quarters
│   ├── hpi_vs_listings.csv         HPI and active listings; 40 quarters
│   └── README.md                  Cleaning, data dictionary, sources, and analysis plan
├── OUTPUT/
│   ├── EVALUATION_TABLES/
│   │   ├── 01_crisis_period_shifts.csv      Coefficient shifts when crisis periods are dummied out or dropped
│   │   ├── 02_diagnostics.csv               Residual diagnostics: autocorrelation, heteroskedasticity, normality
│   │   ├── 03_equal_strength_tests.csv      Wald tests comparing predictor strengths
│   │   ├── 04_final_model_summary.csv       Final model sample sizes and fit statistics
│   │   ├── 05_final_model_summary.png       Image of the final model summary table
│   │   ├── 06_final_results_table.csv       Final coefficients, confidence intervals, p-values, and VIF
│   │   ├── 07_flagged_quarters.csv          Quarters flagged as influential by two or more checks
│   │   ├── 08_influence_measures.csv        Cook's D, studentized residuals, leverage, and DFBETAS per quarter
│   │   ├── 09_outlier_sensitivity.csv       Coefficients under baseline, crisis-dummy, and crisis-dropped models
│   │   ├── 10_robustness_checks.csv         Results under alternative Newey-West lags and a no-listings model
│   │   └── 11_robustness_p_values.csv       P-values for each robustness specification
│   ├── 01_quarterly_trends.png          Initial plots of the four series in original units
│   ├── 02_hpi_growth_distribution.png   Initial histogram of annual HPI growth
│   ├── 03_coverage_table.csv            Variable coverage and missing-value counts
│   ├── 04_timeseries_yoy.png            Annual-change time-series panels
│   ├── 05_summary_stats.csv             Summary statistics by analysis window
│   ├── 06_histograms_yoy.png            Annual-change distributions
│   ├── 07_correlation_heatmaps.png      Correlations by analysis window
│   ├── 08_lag_correlations.png          Exploratory correlations at lags 0–4
│   ├── 09_seasonality_boxplots.png      Seasonal patterns by calendar quarter
│   ├── 10_quarter_scorecard.png         Descriptive seasonal rankings
│   ├── 11_lag_correlations.csv          Modeling lag correlations and selections
│   ├── 12_lag_stability.csv             Lag-selection stability results
│   ├── 13_results_table.csv             Coefficients, uncertainty, p-values, and VIF
│   ├── 14_model_summary.csv             Model sample sizes and fit statistics
│   ├── 15_long_run_model_summary.txt    Long-run regression summary
│   ├── 16_recent_model_summary.txt      Recent regression summary
│   ├── 17_long_run_fitted_residuals.csv Long-run fitted values and residuals
│   ├── 18_recent_fitted_residuals.csv   Recent fitted values and residuals
│   ├── 19_actual_vs_fitted.png          Actual vs. fitted HPI growth for both models
│   ├── 20_coefficient_plot.png          Standardized coefficients with 95% confidence intervals
│   ├── 21_lag_stability.png             How often each lag won in the bootstrap resamples
│   ├── 22_mortgage_vs_hpi_growth.png    Mortgage-rate changes vs. HPI growth
│   ├── 23_influential_quarters.png      Cook's distance, with influential quarters labeled
│   └── 24_outlier_sensitivity.png       Coefficient changes with crisis dummies or crisis quarters dropped
├── SCRIPTS/
│   ├── 01_preprocess_data.py            Clean, align, and export quarterly data
│   ├── 02_exploratory_plots.R           Generate the two initial descriptive plots
│   ├── 03_variable_and_lag_analysis.Rmd Expanded EDA, lags, and seasonality
│   ├── 04_regression_models.ipynb       Select lags, fit models, and export results
│   └── 05_model_evaluation.ipynb        Diagnostics, robustness, outlier analysis, final tables
├── LICENSE.md                       MIT license for code
├── requirements.txt                 Python preprocessing dependency (pandas)
├── .gitignore                       Temporary files and Python caches
└── README.md                        Project overview and reproduction instructions
```

The script prefixes indicate the analysis sequence; the reproduction instructions
below also include setup and data acquisition. See Step 3 for the expanded EDA's
current path settings and differences between generated and committed filenames.

## Section 3: Instructions for Reproducing Our Results

These steps reproduce every result in this project, from the raw FRED data to the final regression tables and figures. Follow them in order. Each step says which file to run, what it does, and what it should produce, so you can check your work as you go.

> **Before you start:** file and folder names below match the structure described in Section 2. Text in `[brackets]` is a placeholder; replace it with your group's actual file names and values before publishing.

---

### Step 0: Set up your environment

1. Install **Python 3.10 or newer** and **Jupyter Notebook** (or use Google Colab or VS Code with the Jupyter extension).
2. Clone this repository and move into it:
```bash
   git clone [https://github.com/your-group/your-repo.git]
   cd [your-repo]
```
3. Install the required packages:
```bash
   pip install -r requirements.txt
```
   If `requirements.txt` is missing, install them directly:
```bash
   pip install pandas numpy statsmodels matplotlib seaborn
```
   Our results were produced with `[pandas 2.x, numpy 1.x, statsmodels 0.14.x, matplotlib 3.x, seaborn 0.13.x]`. Other versions should work, but small numerical differences are possible.

---

### Step 1: Get the data

Use the included [raw combined CSV](<DATA/Raw_Combined_ FRED_Data.csv>) as the input to `SCRIPTS/01_preprocess_data.py`. No additional download is required.

The file contains 2,898 rows with four independent date/value pairs. Each series has its own frequency and start date, so values on the same raw row do **not** necessarily describe the same time period. Step 2 aligns the observations by calendar quarter. See [DATA/README.md](DATA/README.md) for the raw and cleaned column dictionaries, missing-data rules, and source references.

The individual source CSVs are also included in `DATA/original_fred/` for reference. The preprocessing script reads the combined file, rather than these individual files.

| Variable | FRED series ID in the source CSV | Frequency | Included source file |
|---|---|---|---|
| Charlottesville metro house price index (outcome) | `ATNHPIUS16820Q` | Quarterly | [HPI CSV](DATA/original_fred/All-transactions_House_Price_Index_ATNHPIUS51540A.csv) |
| Charlottesville city unemployment rate | `VACHAR0URN` | Monthly | [Unemployment CSV](DATA/original_fred/Unemployment_Rate_VACHAR0URN.csv) |
| U.S. 30-year fixed mortgage rate | `MORTGAGE30US` | Weekly | [Mortgage CSV](DATA/original_fred/30YR_Fixed_Rate_Mortgage_Avg_US_MORTGAGE30US.csv) |
| Charlottesville metro active listing count | `ACTLISCOU16820` | Monthly | [Listings CSV](DATA/original_fred/Housing_Inventory_Active_Listing_Count_ACTLISCOU16820.csv) |

**HPI filename note:** the included HPI file is named with `ATNHPIUS51540A`, but its column header identifies the quarterly metro series `ATNHPIUS16820Q`. The table above follows the file contents; keep the existing filename when locating the supplied file.

Use the supplied snapshot to reproduce the committed results. Newly downloaded FRED data may contain revisions or additional observations. The repository's data documentation records source access dates, but does not establish a single download date for the combined file.

---

### Step 2: Preprocess the data

From the repository root, run:

```bash
python SCRIPTS/01_preprocess_data.py
```

The script reads `DATA/Raw_Combined_ FRED_Data.csv` without changing it and:

1. Reads each series using its own date column, validates dates and numeric values, removes exact duplicates, and rejects conflicting observations.
2. Aligns the series to calendar quarters. HPI stays as observed; mortgage rates use the mean of weekly observations, and unemployment and active listings use the mean of monthly observations. Listings represent average inventory, not a quarterly total.
3. Requires all three monthly values for a quarterly mean. Weekly mortgage coverage requires all values present, at least 12 observations, and observations within nine days of both quarter boundaries; source gaps longer than nine days are rejected. Incomplete quarters stay missing. In particular, missing October 2025 unemployment leaves 2025 Q4 unemployment blank. Missing values are not filled, and COVID-era extremes are retained.
4. Calculates year-over-year changes on the continuous quarterly calendar, before trimming the output to HPI coverage:
   - `hpi_yoy_pct` and `active_listings_yoy_pct`: `100 * (value / value_four_quarters_ago - 1)`.
   - `mortgage_rate_yoy_pp` and `unemployment_rate_yoy_pp`: `value - value_four_quarters_ago`, in percentage points.
5. Exports the combined dataset and three smaller views containing HPI and one predictor, with both levels and annual changes. Missing quarters within each pair's overlap remain in place so later lags represent actual calendar quarters.

**Outputs and checks for the supplied snapshot:**

| File | Rows (quarters) | Coverage |
|---|---:|---|
| `DATA/cleaned_quarterly.csv` | 172 | 1983 Q3–2026 Q2 |
| `DATA/hpi_vs_mortgage.csv` | 172 | 1983 Q3–2026 Q2 |
| `DATA/hpi_vs_unemployment.csv` | 146 | 1990 Q1–2026 Q2 |
| `DATA/hpi_vs_listings.csv` | 40 | 2016 Q3–2026 Q2 |

These counts include rows with missing values; they are not regression sample sizes. Preprocessing does not create lagged predictors or separate long-run/recent model files. Modeling uses `cleaned_quarterly.csv`, creates lags before dropping missing rows, and restricts dates to the planned study windows ending in 2025. See [DATA/README.md](DATA/README.md) for the data dictionary and cleaning details.

### Step 3: Exploratory analysis

**Initial descriptive plots:** from the repository root, run:

```bash
Rscript SCRIPTS/02_exploratory_plots.R
```

This script uses base R and reads `DATA/cleaned_quarterly.csv`. It saves:

- `OUTPUT/quarterly_trends.png`: four time-series panels showing HPI, mortgage rates, unemployment, and active listings in their original units, with missing periods left as gaps.
- `OUTPUT/hpi_growth_distribution.png`: a histogram of year-over-year HPI growth (`hpi_yoy_pct`), with a dashed line at zero growth.

**Expanded EDA:** open `SCRIPTS/03_variable_and_lag_analysis.Rmd` in RStudio and run its R chunks from top to bottom. Install its packages first if needed:

```r
install.packages(c("ggplot2", "dplyr", "lubridate", "tidyr", "readr", "scales", "purrr"))
```

The committed R Markdown file currently reads a personal Desktop path and writes to `eda_output/`. Before running it, set the working directory to the repository root, replace its `read.csv(...)` call with `read.csv("DATA/cleaned_quarterly.csv")`, and change `OUT_DIR` to `"OUTPUT"`. Its `DATA_PATH` variable is currently unused. Run the R chunks in RStudio; the header's command for a `.R` file does not apply to this `.Rmd` file.

The expanded analysis produces a coverage table, year-over-year time-series plots, summary statistics, histograms, correlation heatmaps, correlations at lags 0–4, seasonal boxplots, and a descriptive quarter scorecard. It uses data through 2026 Q2, with long-run annual-change coverage beginning in 1991 Q1 and recent coverage beginning in 2017 Q3. These EDA windows extend beyond the models' planned 2025 endpoint.

Existing expanded EDA outputs are saved in `OUTPUT/` as `01_coverage_table.csv`, `02_timeseries_yoy.png`, `03_summary_stats.csv`, `04_histograms_yoy.png`, `05_correlation_heatmaps.png`, `06_lag_correlations.png`, `07_seasonality_boxplots.png`, and `08_quarter_scorecard.png`.

**Reproduction note:** the current R Markdown code saves the time-series figure as `03_timeseries_yoy.png`, seasonal boxplots as `08_seasonality_boxplots.png`, and scorecard as `09_quarter_scorecard.png`, so these names differ from the committed figures. It also exports `05_lag_correlations.csv`. The expanded EDA's lag table is separate from the modeling output `OUTPUT/lag_correlations.csv`. These figures and correlations describe associations; they do not establish causation.

---

### Step 4: Select time lags and fit the regression models

**Run:** `SCRIPTS/04_regression_models.ipynb`. Open it in Jupyter and choose **Kernel → Restart & Run All**.

The notebook requires `pandas`, `numpy`, and `statsmodels`. It reads `DATA/cleaned_quarterly.csv` from Step 2 and finds the `DATA/` folder automatically, so it can be run from either the main repository folder or the `SCRIPTS/` folder. No settings need to be changed to reproduce our results.

The notebook does the following, in order:

1. **Loads the cleaned data** with one row per calendar quarter, keeping quarters with blank values so that shifting by *k* rows always means *k* calendar quarters. It then defines two models, each using the quarters where all of its variables are available:
   - **Long-run model:** yearly house price growth (`hpi_yoy_pct`) explained by unemployment and mortgage rate changes (`unemployment_rate_yoy_pp`, `mortgage_rate_yoy_pp`)
   - **Recent model:** the same variables plus active listing changes (`active_listings_yoy_pct`)
2. **Selects a time lag for each predictor.** For each model and predictor, it calculates the Pearson correlation between house price growth and the predictor measured 0, 1, 2, 3, and 4 quarters earlier. All five lags are compared on the same set of quarters. The lag with the largest absolute correlation is selected.
3. **Checks how reliable each selected lag is.** Year-over-year changes overlap by 3 of 4 quarters, so correlations at neighboring lags are naturally similar. The notebook resamples the data in blocks of 8 consecutive quarters (a moving block bootstrap, 2,000 resamples, random seed 0) and records how often each lag is selected. A lag selected in at least 70% of resamples is marked as clear; otherwise, its response time should be reported as a range of lags.
4. **Builds each model's dataset.** Each predictor is shifted by its selected lag, quarters with missing values are dropped, and the predictors are standardized (mean 0, standard deviation 1). House price growth is left in percent units.
5. **Fits the regressions.** Each model is an ordinary least squares (OLS) regression with an intercept, using Newey-West standard errors with a maximum lag of 4 quarters and two-sided t-tests at α = 0.05.
6. **Creates results tables** with coefficients, 95% confidence intervals, p-values, predictor rankings by standardized coefficient size, variance inflation factors (VIF), R², and adjusted R², and saves all outputs.

**Outputs** (saved in `OUTPUT/`):

| File | Contents |
|---|---|
| `lag_correlations.csv` | Correlation between price growth and each predictor at lags 0–4, with the selected lag marked |
| `lag_stability.csv` | Percentage of bootstrap resamples in which each lag was selected, and whether the selected lag is clear (≥ 70%) |
| `results_table.csv` | Standardized coefficients, Newey-West standard errors, 95% CIs, p-values, significance, rank, and VIF for each predictor |
| `model_summary.csv` | Sample size, R², adjusted R², and number of significant predictors for each model |
| `long_run_fitted_residuals.csv`, `recent_fitted_residuals.csv` | Actual, fitted, and residual price growth for each quarter (used for residual plots in Step 5) |
| `long_run_model_summary.txt`, `recent_model_summary.txt` | Full `statsmodels` regression output for each model |

**Check:** if you are using our data snapshot, the notebook should produce these values:

| | Long-run model | Recent model |
|---|---|---|
| Regression sample | 1991Q2 – 2026Q2 (140 quarters) | 2018Q3 – 2026Q2 (31 quarters) |
| Selected lags | Mortgage rate: 0, Unemployment: 1 | Mortgage rate: 0, Unemployment: 1, Active listings: 4 |
| R² / Adjusted R² | 0.133 / 0.121 | 0.692 / 0.658 |

The reliability check takes about 10–20 seconds to run. Because the random seed is fixed, it produces the same percentages every time.

### Step 5: Evaluate the models and create results figures

**Run:** `[SCRIPTS/05_evaluation.ipynb]`

For each model, this notebook reports:
- The sample size (number of quarters)
- The selected lag for each predictor
- Coefficient estimates, 95% confidence intervals, and p-values. A two-sided test at α = 0.05 counts as significant.
- R² and adjusted R²
- Variance inflation factors (VIF), using `statsmodels.stats.outliers_influence.variance_inflation_factor`. Values above 5 are flagged.
- A plot of residuals over time
- A ranking of predictors by the absolute value of their standardized coefficients

**Output:** `[OUTPUT/results_table.csv]` and figures in `[OUTPUT/figures/]`.

---

### Step 6: Evaluate the models, test outliers, and create final tables

Run: `SCRIPTS/05_model_evaluation.ipynb`. Open it in Jupyter and choose **Kernel → Restart & Run All**. In Google Colab, use **Runtime → Run all**; in Colab it clones this repository automatically if `DATA/` is not found.

The notebook needs the same packages as Step 4, plus `matplotlib`. It reads `DATA/cleaned_quarterly.csv` and the Step 4 outputs `OUTPUT/11_…` through `OUTPUT/18_…`, so complete Step 4 first. It stops with a clear error message if any of those files is missing. No settings need to be changed.

The notebook does the following, in order:

1. **Refits both models and checks the refit.** It refits each Step 4 model from the saved lag selections and confirms the coefficients match `13_results_table.csv`, so the evaluation is built on the same models.
2. **Plots model fit.** It compares actual and fitted price growth, shows standardized coefficients with 95% confidence intervals, shows how often each lag won in the bootstrap resamples, and plots mortgage-rate changes against price growth.
3. **Runs residual diagnostics.** For each model it tests residual autocorrelation (Durbin-Watson and Ljung-Box), non-constant variance (Breusch-Pagan), and non-normality (Jarque-Bera).
4. **Checks robustness.** It reruns the models with wider Newey-West lags (6 and 8) and with a version that leaves out active listings, using the same quarters. It also runs Wald tests of whether predictors have equal strength.
5. **Finds influential quarters.** For each quarter it computes Cook's distance, studentized residuals, leverage, and DFBETAS. A quarter is flagged when two or more of these checks exceed their thresholds.
6. **Tests sensitivity to crisis periods.** It refits each model three ways: baseline, with dummy variables for the 2007 Q4–2009 Q2 recession and 2020 Q1–2022 Q4 pandemic periods, and with those quarters dropped. It then reports how much each coefficient moves.
7. **Saves the final results tables** and an environment file listing package versions.

**Outputs:**

| Location | Files | Contents |
|---|---|---|
| `OUTPUT/` | `19_actual_vs_fitted.png`, `20_coefficient_plot.png`, `21_lag_stability.png`, `22_mortgage_vs_hpi_growth.png` | Model-fit figures: actual vs. fitted, coefficient plot, lag stability, mortgage vs. price growth |
| `OUTPUT/` | `23_influential_quarters.png`, `24_outlier_sensitivity.png` | Cook's distance with flagged quarters labeled, and coefficient changes under the crisis specifications |
| `OUTPUT/EVALUATION_TABLES/` | `01_…` through `11_…` | Diagnostics, robustness checks, influence measures, flagged quarters, outlier sensitivity, and the final results and model-summary tables |

**Check:** the refit in item 1 should report that it matches Step 4's coefficients. The bootstrap is not rerun here, so the notebook finishes in under a minute.

---

### Step 7: Compare your results with ours

Our final results are in `[OUTPUT/]` and summarized in our final presentation. If you used the data files from Option A, your coefficients, p-values, and R² values should match ours to at least 3 decimal places. If they don't, check the following:
- **Did you download fresh FRED data?** Revised values cause small differences; use the files in `DATA/` instead.
- **Were the cells run out of order?** Restart the notebook kernel and choose "Run All."
- **Are rates being converted to percent changes?** Unemployment and mortgage rates must use percentage-point differences, not percent changes.
- **Are the quarters correct?** Confirm the quarterly averages use calendar quarters and the mean of available months, not the sum.
