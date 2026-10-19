# Charlottesville Housing Market Factors

Study which changes in mortgage rates, unemployment, and active listings are
associated with year-over-year Charlottesville house-price growth. Start with
**DATA/cleaned_quarterly.csv** for the combined analysis. The three `hpi_vs_*.csv`
files are simpler views for individual comparisons, generated from the same data.

## 1. Software and platform

Preprocessing: Python 3.12 and pandas 3.0.1, tested on Windows.
Exploratory plots: R 4.6.1, using base R (no add-on packages).
Install the Python dependency with `python -m pip install -r requirements.txt`.

## 2. Repository contents

```text
DATA/
  Raw_Combined_ FRED_Data.csv   Original data; unchanged
  cleaned_quarterly.csv        Aligned levels and annual changes; 172 quarters
  hpi_vs_mortgage.csv          HPI and mortgage rates
  hpi_vs_unemployment.csv      HPI and city unemployment
  hpi_vs_listings.csv          HPI and active listings
  README.md                    Cleaning, dictionary, sources, and analysis plan
SCRIPTS/
  preprocess_data.py           Step 1: clean and align the data
  02_exploratory_plots.R       Step 2: reproduce the two exploratory plots
  test_preprocess_data.py      Checks for alignment and missing-data errors
OUTPUT/
  quarterly_trends.png         Four series shown in their original units
  hpi_growth_distribution.png  Distribution of the planned outcome
requirements.txt               Python dependency
LICENSE.md                     MIT license for code
.gitignore                     Excludes temporary files and Python caches
```

## 3. Reproduce the current work

1. Open a terminal in this repository and install the dependency above.
2. Run `python SCRIPTS/preprocess_data.py` to rebuild the combined and three pairwise CSVs.
3. Run `python -m unittest discover -s SCRIPTS -p "test_*.py"` to check it.
4. Run `Rscript SCRIPTS/02_exploratory_plots.R` to rebuild both plots.

Keep `DATA/Raw_Combined_ FRED_Data.csv`: it is the original input and is not
downloaded by these scripts. The four generated CSVs and both PNGs can be deleted
and recreated by steps 2 and 4, in that order. No compilation is needed; rerunning
the scripts also overwrites existing generated files.

MI3 still needs the planned analysis: Haero selects lags and fits the two MI2
regressions; Hershi evaluates the results and diagnostics. They should add their
scripts, outputs, dependencies, and run instructions here when finished. The
[DATA guide](DATA/README.md) explains the handoff and remaining MI3 requirements.
