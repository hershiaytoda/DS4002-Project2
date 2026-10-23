# DS-4002-Project 2

Project 2 for Group 4 in DS 4002 examines whether changes in mortgage rates,
unemployment, and active listings are associated with year-over-year
Charlottesville house-price growth.

## Section 1: Software and platform

The project uses Python for preprocessing, regression, and evaluation, and R for
exploratory analysis. Preprocessing was reported as tested on Windows with Python
3.12 and pandas 3.0.1. The repository uses relative paths and can also be opened
from macOS or Linux; a full run on every platform has not been verified.

- Python 3.10 or newer, with pandas(2.2.3), NumPy(2.1.3), statsmodels(0.15.0), matplotlib(3.10,0), IPython(7.34.0),
  and Jupyter Notebook. Install with `python -m pip install -r requirements.txt`.
- R and RStudio: script 02 uses base R; script 03 needs ggplot2(4.0,2), dplyr(1.1.4),
  lubridate(1.9.4), tidyr(1.3.2), readr(2.2.0), scales(1.4.0), and purrr(1.2.1). Run its R chunks in RStudio.

Dependency versions are not fully pinned. The evaluation notebook records its
Python package versions when run.

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
│   │   ├── 06_final_results_table.csv       Final coefficients, confidence intervals, p-values, ranks, and VIF
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
├── requirements.txt                 Python analysis and notebook dependencies
├── .gitignore                       Temporary files and Python caches
└── README.md                        Project overview and reproduction instructions
```

Rerunning the expanded EDA also writes `OUTPUT/eda_lag_correlations.csv`.
Evaluation also creates a final-results table image, an outlier-sensitivity pivot,
and an environment record in `OUTPUT/EVALUATION_TABLES/`, plus
`evaluation_results.zip` at the repository root. These supplementary files are
not all included in the committed snapshot.

## Section 3: Instructions for Reproducing Our Results

Run these steps in order. Use the supplied data snapshot to reproduce the saved
results; fresh downloads may contain revisions or additional observations.

### Step 0: Set up

Install Python, R, and RStudio, then run:

```bash
git clone https://github.com/hershiaytoda/DS4002-Project2.git
cd DS4002-Project2
python -m pip install -r requirements.txt
```

Install the expanded EDA packages from the R console:

```r
install.packages(c("ggplot2", "dplyr", "lubridate", "tidyr", "readr", "scales", "purrr"))
```

### Step 1: Use the included data

No download is needed. Preprocessing reads
[the raw combined CSV](<DATA/Raw_Combined_ FRED_Data.csv>), which contains 2,898
rows with four independent date/value pairs. Observations on the same raw row do
not necessarily describe the same date. The individual FRED CSVs are included in
`DATA/original_fred/` for reference.

See [the data README](DATA/README.md) for source references, units, cleaning rules,
ethics, and data dictionaries. The HPI source filename contains `ATNHPIUS51540A`,
but its header identifies the quarterly metro series `ATNHPIUS16820Q`; the
analysis follows the supplied file contents. Unemployment covers Charlottesville
city, HPI/listings cover the metro area, and mortgage rates are national.

### Step 2: Preprocess

From the repository root:

```bash
python SCRIPTS/01_preprocess_data.py
```

The script validates each date/value pair separately, aligns observations to
calendar quarters, and calculates year-over-year changes before trimming to HPI
coverage. Mortgage rates use weekly means; unemployment and listings use monthly
means. Incomplete quarters remain missing, including 2025 Q4 unemployment.
Missing values are not filled and crisis observations are retained.

HPI/listings changes are percentages over four quarters. Mortgage/unemployment
changes are percentage-point differences over four quarters.

| Output in DATA | Quarters | Coverage |
|---|---:|---|
| cleaned_quarterly.csv | 172 | 1983 Q3-2026 Q2 |
| hpi_vs_mortgage.csv | 172 | 1983 Q3-2026 Q2 |
| hpi_vs_unemployment.csv | 146 | 1990 Q1-2026 Q2 |
| hpi_vs_listings.csv | 40 | 2016 Q3-2026 Q2 |

These counts include missing values and are not regression sample sizes.

### Step 3: Exploratory analysis

From the repository root:

```bash
Rscript SCRIPTS/02_exploratory_plots.R
```

This writes `OUTPUT/01_quarterly_trends.png` and
`OUTPUT/02_hpi_growth_distribution.png`.

Open `SCRIPTS/03_variable_and_lag_analysis.Rmd` in RStudio, set the working
directory to the repository root, and run its R chunks from top to bottom.
It reads `DATA/cleaned_quarterly.csv` and writes directly to `OUTPUT/`.
Outputs 03-10 contain coverage, annual-change plots, summary statistics,
histograms, correlations, lag plots, seasonality, and a descriptive scorecard.
Its extra `eda_lag_correlations.csv` is separate from the model lag-selection table.

### Step 4: Fit models

Open `SCRIPTS/04_regression_models.ipynb` in Jupyter and choose
**Kernel > Restart & Run All**. Start Jupyter from the repository root with
`python -m notebook`. The notebook finds DATA from either the root or SCRIPTS.

The notebook compares predictor lags 0-4 on a common sample for each predictor,
selects the largest absolute correlation, and checks selection stability using
2,000 block-bootstrap resamples (seed 0, block length 8). It then creates lags
before dropping missing rows, standardizes predictors on each final sample, and
fits OLS with Newey-West errors (maximum lag 4) and two-sided t-tests.

**Study-period note:** the documented MI2 plan ended in 2025. The committed
analysis uses available data through 2026 Q2 instead. The defaults reproduce
these committed results; this departure from the plan should be disclosed when
presenting the study.

| Check | Long-run model | Recent model |
|---|---|---|
| Sample | 1991 Q2-2026 Q2; 140 quarters | 2018 Q3-2026 Q2; 31 quarters |
| Selected lags | Mortgage 0; unemployment 1 | Mortgage 0; unemployment 1; listings 4 |
| R² / adjusted R² | 0.133 / 0.121 | 0.692 / 0.658 |

Outputs 11-18 in OUTPUT contain lag correlations, bootstrap stability,
coefficients and uncertainty, VIF, model summaries, and fitted values/residuals.
The seed is fixed; runtime depends on your computer.

### Step 5: Evaluate models

Open `SCRIPTS/05_model_evaluation.ipynb` and choose
**Kernel > Restart & Run All**. It reads the numbered Step 4 outputs directly;
no renaming or manual folder changes are needed. Running in the local clone is
the simplest way to use your current files. In Colab, the notebook clones the
GitHub repository if needed, so it uses the version published there.

It refits the models and checks coefficients against the saved results, creates
figures 19-24, and writes diagnostics and final tables to
`OUTPUT/EVALUATION_TABLES/`. Checks include residual autocorrelation,
heteroskedasticity, normality, alternative Newey-West settings, a same-sample
model without listings, predictor-strength tests, influential quarters, and
crisis-period sensitivity. The final cell creates `evaluation_results.zip`.

### Step 6: Check and interpret results

Check the sample sizes and fit values above, and check that the evaluation
reports matching refit coefficients. Use the supplied snapshot when comparing
numeric results; package versions may cause small differences.

Results describe associations. Lag selection uses the same data as estimation,
so significance tests are exploratory. Residual autocorrelation remains substantial,
and the recent model has only 31 quarters. Compare model specifications on the
same quarters when assessing the added contribution of listings; the two main
models' R² values use different periods.

## References

Data sources and the Newey-West method are cited in IEEE-style numbered
references at the end of [DATA/README.md](DATA/README.md).
