"""Step 1: clean the FRED snapshot and export combined/pairwise quarterly data.

Run from any directory: python SCRIPTS/preprocess_data.py
Input: DATA/Raw_Combined_ FRED_Data.csv (never modified).
Output: DATA/cleaned_quarterly.csv (172 quarters in the supplied snapshot).
Also exports hpi_vs_mortgage.csv, hpi_vs_unemployment.csv, hpi_vs_listings.csv
beside the combined output. These are column selections, not separate cleanings.
Requires pandas. Blank values remain missing; no model is fitted here.
"""

from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
SOURCES = {
    "hpi": ("observation_date_ATHPI", "all_transactions HPI", "Q"),
    "mortgage_rate_pct": ("observation_date_mortgage", "mortgage", "W"),
    "unemployment_rate_pct": (
        "observation_date_unemployment", "Unemployment_rate", "M"
    ),
    "active_listings": (
        "observation_date_listing count", "HPI_Listing Count", "M"
    ),
}
PREDICTORS = {
    "mortgage": ("mortgage_rate_pct", "mortgage_rate_yoy_pp"),
    "unemployment": ("unemployment_rate_pct", "unemployment_rate_yoy_pp"),
    "listings": ("active_listings", "active_listings_yoy_pct"),
}


def read_sources(path: Path) -> tuple[dict, dict]:
    """Read each date/value pair independently and reject ambiguous observations."""
    raw = pd.read_csv(path, dtype=str, keep_default_na=False)
    missing_tokens = {"", ".", "NA", "N/A", "NaN", "nan", "null"}
    series, audit = {}, {"raw_rows": len(raw), "series": {}}
    for name, (date_col, value_col, frequency) in SOURCES.items():
        pair = raw[[date_col, value_col]].apply(lambda col: col.str.strip())
        pair = pair.loc[~pair.isin(missing_tokens).all(axis=1)]
        dates = pd.to_datetime(pair[date_col], format="%Y-%m-%d", errors="raise")
        if dates.isna().any():
            raise ValueError(f"{name}: value without an observation date")
        values = pd.to_numeric(pair[value_col].mask(pair[value_col].isin(missing_tokens)), errors="raise")
        frame = pd.DataFrame({"date": dates, "value": values})
        exact_duplicates = int(frame.duplicated().sum())
        frame = frame.drop_duplicates().sort_values("date").reset_index(drop=True)
        if frame.date.duplicated().any():
            raise ValueError(f"{name}: conflicting values on the same date")
        valid = frame.value.dropna()
        if valid.isin([float("inf"), float("-inf")]).any() or (valid < 0).any():
            raise ValueError(f"{name}: nonfinite or negative level")
        if name == "hpi" and (valid <= 0).any():
            raise ValueError("HPI must be positive for percentage changes")
        if name.endswith("_pct") and (valid > 100).any():
            raise ValueError(f"{name}: rate exceeds 100 percent")
        if name == "active_listings" and (valid % 1 != 0).any():
            raise ValueError("Listing counts must be whole numbers before averaging")
        if frequency in {"M", "Q"}:
            periods = frame.date.dt.to_period(frequency)
            if periods.duplicated().any():
                raise ValueError(f"{name}: more than one observation per {frequency}")
            if not (frame.date == periods.dt.start_time).all():
                raise ValueError(f"{name}: expected period-start observation dates")
            expected = pd.period_range(periods.min(), periods.max(), freq=frequency)
            absent_periods = expected.difference(pd.PeriodIndex(periods)).astype(str).tolist()
        else:
            absent_periods = []
            # Holiday releases can move by a day or two. Longer gaps need review.
            if frame.date.diff().dt.days.dropna().gt(9).any():
                raise ValueError(f"{name}: weekly gap greater than 9 days; inspect source")
        audit["series"][name] = {
            "dated_observations": len(frame),
            "nonmissing_values": int(frame.value.notna().sum()),
            "first_date": frame.date.min().strftime("%Y-%m-%d"),
            "last_date": frame.date.max().strftime("%Y-%m-%d"),
            "missing_value_dates": frame.loc[frame.value.isna(), "date"].dt.strftime("%Y-%m-%d").tolist(),
            "absent_periods": absent_periods,
            "exact_duplicates_removed": exact_duplicates,
        }
        series[name] = frame
    return series, audit


def aggregate(frame: pd.DataFrame, source_frequency: str, frequency: str) -> pd.DataFrame:
    """Arithmetic means, masked when native observations do not cover the period."""
    work = frame.assign(period=frame.date.dt.to_period(frequency))
    grouped = work.groupby("period", sort=True)
    result = grouped.agg(
        mean=("value", "mean"), n_observations=("value", "size"),
        n_values=("value", "count"), first_date=("date", "min"), last_date=("date", "max"),
    )
    if source_frequency in {"M", "Q"}:
        expected = 3 if source_frequency == "M" and frequency == "Q" else 1
        result["complete"] = result.n_values.eq(expected) & result.n_observations.eq(expected)
    else:
        # This is a coverage screen, not a reconstructed official release calendar.
        # 12-14 quarterly observations can be valid because of holiday date shifts.
        minimum = 12 if frequency == "Q" else 3
        result["complete"] = (
            result.n_values.eq(result.n_observations)
            & result.n_values.ge(minimum)
            & (result.first_date - result.index.start_time).dt.days.le(9)
            & (result.index.end_time.normalize() - result.last_date).dt.days.le(9)
        )
    result["value"] = result["mean"].where(result.complete)
    return result


def build_quarterly(series: dict) -> pd.DataFrame:
    """Align levels and calculate annual changes on a continuous quarter calendar."""
    all_quarters = pd.period_range(
        min(frame.date.min() for frame in series.values()).to_period("Q"),
        max(frame.date.max() for frame in series.values()).to_period("Q"), freq="Q",
    )
    master = pd.DataFrame(index=all_quarters)
    for name, (_, _, native_frequency) in SOURCES.items():
        grouped = aggregate(series[name], native_frequency, "Q")
        master[name] = grouped.value

    # A year is four quarters. Never fill missing values before taking changes.
    master["hpi_yoy_pct"] = master.hpi.pct_change(4, fill_method=None) * 100
    for level, transformed in PREDICTORS.values():
        if transformed.endswith("_pp"):
            change = master[level] - master[level].shift(4)
        else:
            previous = master[level].shift(4)
            change = (master[level] / previous.where(previous.ne(0)) - 1) * 100
        master[transformed] = change

    # Retain every HPI quarter, including blanks in predictors. This keeps later
    # shifts by the modeling partner aligned to actual calendar quarters.
    hpi_dates = series["hpi"].date
    master = master.loc[hpi_dates.min().to_period("Q"):hpi_dates.max().to_period("Q")].copy()
    master.index.name = "quarter"
    master.insert(0, "quarter_start", master.index.start_time)
    return master


def export_csv(frame: pd.DataFrame, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    # Explicit labels avoid date_format turning PeriodIndex keys into period-end dates.
    export = frame.copy()
    export.index = export.index.astype(str)
    export.to_csv(path, index=True, na_rep="", date_format="%Y-%m-%d", float_format="%.10g")


def build_pairwise(master: pd.DataFrame) -> dict[str, pd.DataFrame]:
    """Select HPI and one predictor, keeping all quarters within their overlap."""
    pairs = {}
    for name, (level, change) in PREDICTORS.items():
        columns = ["quarter_start", "hpi", level, "hpi_yoy_pct", change]
        observed = master[["hpi", level]].dropna()
        if observed.empty:
            pair = master.iloc[:0][columns]
        else:
            # Trim years before the predictor begins, but retain missing quarters
            # inside the overlap so later lags still represent calendar quarters.
            pair = master.loc[observed.index.min():observed.index.max(), columns]
        pairs[f"hpi_vs_{name}.csv"] = pair
    return pairs


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, default=ROOT / "DATA" / "Raw_Combined_ FRED_Data.csv")
    parser.add_argument("--output", type=Path, default=ROOT / "DATA" / "cleaned_quarterly.csv")
    args = parser.parse_args()
    series, audit = read_sources(args.input)
    master = build_quarterly(series)
    export_csv(master, args.output)
    print(f"Saved {args.output.name}: {len(master)} quarters, {master.index.min()} through {master.index.max()}.")
    for filename, pair in build_pairwise(master).items():
        export_csv(pair, args.output.parent / filename)
        print(f"Saved {filename}: {len(pair)} quarters.")
    for name, detail in audit["series"].items():
        if detail["missing_value_dates"]:
            print(f"Missing {name}: {', '.join(detail['missing_value_dates'])}; not filled.")
    print("Next: use pairwise files for individual comparisons and the combined file for multiple regression.")


if __name__ == "__main__":
    main()
