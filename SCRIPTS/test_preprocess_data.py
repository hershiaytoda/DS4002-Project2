"""Run: python -m unittest discover -s SCRIPTS -p 'test_*.py'."""

from io import StringIO
import unittest

import pandas as pd

from importlib import import_module

# Numbered script names must be imported through importlib.
preprocess = import_module("01_preprocess_data")
ROOT = preprocess.ROOT
SOURCES = preprocess.SOURCES
aggregate = preprocess.aggregate
build_quarterly = preprocess.build_quarterly
read_sources = preprocess.read_sources


class PreprocessingTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.series, cls.audit = read_sources(ROOT / "DATA" / "Raw_Combined_ FRED_Data.csv")
        cls.master = build_quarterly(cls.series)

    def test_date_based_means_against_raw_filter(self):
        for name in SOURCES:
            frame = self.series[name]
            values = frame.loc[frame.date.between("2020-04-01", "2020-06-30"), "value"]
            self.assertAlmostEqual(self.master.loc["2020Q2", name], sum(values) / len(values))
        self.assertEqual(self.master.loc["2025Q4", "hpi"], 407.5)

    def test_missing_month_invalidates_quarter(self):
        quarter = self.master.loc["2025Q4"]
        self.assertTrue(pd.isna(quarter.unemployment_rate_pct))
        coverage = aggregate(self.series["unemployment_rate_pct"], "M", "Q")
        self.assertEqual(coverage.loc["2025Q4", "n_values"], 2)
        self.assertFalse(coverage.loc["2025Q4", "complete"])
        self.assertEqual(self.audit["series"]["unemployment_rate_pct"]["missing_value_dates"], ["2025-10-01"])

    def test_yoy_units_and_calendar_offsets(self):
        frame = self.master
        self.assertAlmostEqual(frame.loc["2025Q2", "hpi_yoy_pct"],
                               100 * (frame.loc["2025Q2", "hpi"] / frame.loc["2024Q2", "hpi"] - 1))
        self.assertAlmostEqual(frame.loc["2025Q2", "mortgage_rate_yoy_pp"],
                               frame.loc["2025Q2", "mortgage_rate_pct"] - frame.loc["2024Q2", "mortgage_rate_pct"])
        self.assertTrue(pd.isna(frame.loc["2017Q2", "active_listings_yoy_pct"]))
        self.assertFalse(pd.isna(frame.loc["2017Q3", "active_listings_yoy_pct"]))

    def test_calendar_preserved_for_partners_lag_calculation(self):
        frame = self.master
        lag1 = frame.unemployment_rate_yoy_pp.shift(1)
        lag2 = frame.unemployment_rate_yoy_pp.shift(2)
        self.assertTrue(pd.isna(lag1.loc["2026Q1"]))
        self.assertAlmostEqual(lag2.loc["2026Q1"], frame.loc["2025Q3", "unemployment_rate_yoy_pp"])
        self.assertEqual(frame.index.to_list(), pd.period_range("1983Q3", "2026Q2", freq="Q").to_list())

    def test_truncated_weekly_quarter(self):
        frame = pd.DataFrame({"date": pd.date_range("2026-10-01", periods=2, freq="7D"), "value": [7.28, 7.4]})
        result = aggregate(frame, "W", "Q")
        self.assertFalse(result.loc["2026Q4", "complete"])
        self.assertTrue(pd.isna(result.loc["2026Q4", "value"]))

    def test_holiday_boundary_with_twelve_observations(self):
        quarter = aggregate(self.series["mortgage_rate_pct"], "W", "Q").loc["2026Q1"]
        self.assertEqual(quarter.n_values, 12)
        self.assertTrue(quarter.complete)

    def test_absent_month_not_hidden_by_mean(self):
        frame = pd.DataFrame({"date": pd.to_datetime(["2020-01-01", "2020-03-01"]), "value": [2., 4.]})
        self.assertTrue(pd.isna(aggregate(frame, "M", "Q").loc["2020Q1", "value"]))

    def test_conflicting_duplicate_rejected(self):
        raw = pd.read_csv(ROOT / "DATA" / "Raw_Combined_ FRED_Data.csv", dtype=str).fillna("")
        duplicate = {column: "" for column in raw.columns}
        duplicate.update({"observation_date_ATHPI": "1983-07-01", "all_transactions HPI": "999"})
        csv = StringIO(pd.concat([raw, pd.DataFrame([duplicate])], ignore_index=True).to_csv(index=False))
        with self.assertRaisesRegex(ValueError, "conflicting values"):
            read_sources(csv)

    def test_exported_period_keys(self):
        # Protect against CSV date formatting silently changing quarter keys.
        master = pd.read_csv(ROOT / "DATA" / "cleaned_quarterly.csv")
        self.assertEqual(master.quarter.iloc[0], "1983Q3")
        self.assertEqual(master.quarter_start.iloc[0], "1983-07-01")
        self.assertEqual(len(master.columns), 10)


if __name__ == "__main__":
    unittest.main()
