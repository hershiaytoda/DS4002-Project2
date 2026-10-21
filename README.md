# DS-4002-Project 2

This repository contains Project 2 for Group 4 in DS 4002.

This project examines whether changes in mortgage rates, unemployment, and active listings are associated with year-over-year Charlottesville house-price growth.  We started with **DATA/cleaned_quarterly.csv** for the combined analysis. The three `hpi_vs_*.csv`files are simpler views for individual comparisons, generated from the same data.

## Section 1: Software and platform

Preprocessing: Python 3.12 and pandas 3.0.1, tested on Windows.
Exploratory plots: R 4.6.1, using base R (no add-on packages).
Install the Python dependency with `python -m pip install -r requirements.txt`.

## Section 2: A Map of our documentation

```text
DS-4002-Project-1/
│
├── DATA/
│   ├── Raw_Combined_ FRED_Data.csv   Original data; unchanged
│   ├── cleaned_quarterly.csv        Aligned levels and annual changes; 172 quarters
│   ├── hpi_vs_mortgage.csv          HPI and mortgage rates
│   ├── hpi_vs_unemployment.csv      HPI and city unemployment
│   ├── hpi_vs_listings.csv          HPI and active listings
│   └── README.md                    Cleaning, dictionary, sources, and analysis plan
│
├── OUTPUT/
│   ├── []
│   ├── []
│   ├── []
│   ├── []
│   ├── []
│   ├── []
│   ├── []
│   ├── []
│   ├── []
│   ├── []
│   ├── []
│   ├── []
│   ├── []
│   └── []
│
├── SCRIPTS/
│   ├── 01_preprocess_data.py           Step 1: clean and align the data
│   ├── 02_exploratory_plots.R       Step 2: reproduce the two exploratory plots
│   ├── test_preprocess_data.py      Checks for alignment and missing-data errors
│   ├── []
│   ├── []
│   └── []
├── LICENSE.md                     MIT license for code
├── requirements.txt               Python dependency
├── .gitignore                     Excludes temporary files and Python caches
└── README.md
```

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

**Use the raw combined CSV:** `[DATA/Raw_Combined_ FRED_Data.csv]`

This is the file our preprocessing script reads, so start from it to reproduce our results exactly. It contains all four FRED series side by side, each with its own date column, all downloaded from FRED on **[download date]**. Each series has a different frequency and start date, so values in the same row do **not** refer to the same time period. The preprocessing script in Step 2 aligns them by date. See the data dictionary in Section 2 for a description of every column.

**Original FRED files (for reference):** the individual CSV files we downloaded from FRED are also saved in `[DATA/original_fred/]`. They contain the same data as the combined file, in the original format FRED provides. You don't need them to reproduce our results, but they let you confirm where every value came from.

| Variable | FRED series ID | Frequency | Original file |
|---|---|---|---|
| House price index (outcome) | [ATNHPIUS51540A](https://fred.stlouisfed.org/series/ATNHPIUS51540A) | Quarterly | `[DATA/original_fred/All-transactions_House_Price_Index_ATNHPIUS51540A.csv]` |
| Unemployment rate | [VACHAR0URN](https://fred.stlouisfed.org/series/VACHAR0URN) | Monthly | `[DATA/original_fred/Unemployment_Rate_VACHAR0URN.csv]` |
| 30-year mortgage rate | [MORTGAGE30US](https://fred.stlouisfed.org/series/MORTGAGE30US) | Weekly | `[DATA/original_fred/30YR_Fixed_Rate_Mortgage_Avg_US_MORTGAGE30US.csv]` |
| Active listing count | [ACTLISCOU16820](https://fred.stlouisfed.org/series/ACTLISCOU16820) | Monthly | `[DATA/original_fred/Housing_Inventory_Active_Listing_Count_ACTLISCOU16820.csv]` |

**Note:** do not download fresh copies from FRED to reproduce our results. FRED revises past values and adds new observations over time, so newly downloaded data may differ slightly from ours. The series links above are provided for reference only.
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

### Step 4: Select the time lag for each predictor

**Run:** `[SCRIPTS/03_lag_selection.ipynb]`

For each dataset separately, and for each predictor, this notebook calculates the Pearson correlation between house price growth and the predictor at lags of 0, 1, 2, 3, and 4 quarters. The lag with the **largest absolute correlation** is selected for that predictor. All five correlations are saved, not only the selected one.

**Output:** `[OUTPUT/lag_correlations.csv]`, a table of all correlations with the selected lag marked for each predictor and dataset.

---

### Step 5: Fit the regression models

**Run:** `[SCRIPTS/04_regression_models.ipynb]`

For each dataset, this notebook:
1. **Standardizes the predictors** (subtracts the mean and divides by the standard deviation, calculated within that dataset). Each predictor is used at the lag selected in Step 4. The outcome, house price growth, is left in percent units.
2. **Drops rows** with missing values created by lagging.
3. **Fits an ordinary least squares (OLS) multiple regression** with an intercept, using Newey-West standard errors with a maximum lag of 4 quarters. In `statsmodels`, this is:
```python
   import statsmodels.api as sm
   model = sm.OLS(y, sm.add_constant(X)).fit(cov_type="HAC", cov_kwds={"maxlags": 4})
```
   Here `y` is year-over-year house price growth, and `X` contains the standardized, lagged predictors.

**Output:** `[OUTPUT/long_run_model_summary.txt]` and `[OUTPUT/recent_model_summary.txt]`.

---

### Step 6: Evaluate the models and create results figures

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

### Step 7: Compare your results with ours

Our final results are in `[OUTPUT/]` and summarized in our final presentation. If you used the data files from Option A, your coefficients, p-values, and R² values should match ours to at least 3 decimal places. If they don't, check the following:
- **Did you download fresh FRED data?** Revised values cause small differences; use the files in `DATA/` instead.
- **Were the cells run out of order?** Restart the notebook kernel and choose "Run All."
- **Are rates being converted to percent changes?** Unemployment and mortgage rates must use percentage-point differences, not percent changes.
- **Are the quarters correct?** Confirm the quarterly averages use calendar quarters and the mean of available months, not the sum.
