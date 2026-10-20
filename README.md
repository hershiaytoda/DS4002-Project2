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
│   ├── preprocess_data.py           Step 1: clean and align the data
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

**Run:** `[SCRIPTS/preprocess_data.ipynb]`, all cells from top to bottom.

This notebook does the following, in order:

1. **Loads** the raw combined CSV file (DATA/Raw_Combined_ FRED_Data.csv) and converts each date column to a date format.
2. **Renames** columns to `hpi`, `unemployment`, `mortgage_rate`, and `active_listings`.
3. **Converts everything to quarterly values.** For each calendar quarter (Q1 = Jan–Mar, Q2 = Apr–Jun, Q3 = Jul–Sep, Q4 = Oct–Dec), it takes the **mean of all available observations** in that quarter. Weekly mortgage rates are assigned to a quarter by their observation date. The house price index is already quarterly and is not changed.
   - Missing values are **not** filled in or estimated. For example, the unemployment value for October 2025 is missing in FRED, so the 2025 Q4 average uses only November and December.
4. **Calculates year-over-year changes** by comparing each quarter with the same quarter one year (4 quarters) earlier:
   - `hpi` and `active_listings`: percent change = (this quarter − same quarter last year) ÷ same quarter last year × 100
   - `unemployment` and `mortgage_rate`: percentage-point change = this quarter − same quarter last year
5. **Creates lagged versions** of each predictor, shifted back 0, 1, 2, 3, and 4 quarters (e.g., `mortgage_rate_lag2` holds the mortgage rate change from two quarters earlier).
6. **Builds two datasets**, keeping only quarters where every variable used by that model has a value:
   - **Long-run dataset (1990–2025):** `hpi`, `unemployment`, `mortgage_rate`
   - **Recent dataset (2016–2025):** `hpi`, `unemployment`, `mortgage_rate`, `active_listings`

**Output:** `[DATA/long_run.csv]` and `[DATA/recent.csv]`.

**Check:** the long-run dataset should have about **[N]** rows and start in **[1991 Q1]**. The recent dataset should have about **[N]** rows and start in **[2017 Q3]**. The first year of each series is lost to the year-over-year calculation, which is why neither starts at the raw data's first quarter.

---

### Step 3: Exploratory analysis

**Run:** `[SCRIPTS/02_exploratory_analysis.ipynb]`

This notebook makes:
- **Figure 1**, a time-series plot of all four variables, standardized so they share one scale.
- **Figure 2**, a histogram of the house price index.
- A correlation heatmap of the year-over-year changes.

**Output:** figures saved to `[OUTPUT/figures/]`.

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
