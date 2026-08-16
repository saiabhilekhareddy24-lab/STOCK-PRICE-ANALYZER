import unittest
import pandas as pd

from stock_analyzer import StockPriceAnalyzer


class TestStockPriceAnalyzer(unittest.TestCase):

    def setUp(self):

        self.analyzer = StockPriceAnalyzer(
            "TEST",
            "1mo"
        )

        dates = pd.date_range(
            start="2026-01-01",
            periods=5
        )

        self.analyzer.data = pd.DataFrame(
            {
                "Open": [
                    100,
                    105,
                    110,
                    108,
                    115
                ],

                "High": [
                    105,
                    110,
                    115,
                    112,
                    120
                ],

                "Low": [
                    95,
                    100,
                    105,
                    103,
                    110
                ],

                "Close": [
                    102,
                    108,
                    112,
                    110,
                    118
                ],

                "Volume": [
                    1000,
                    1200,
                    1500,
                    1300,
                    1600
                ]
            },
            index=dates
        )

    def test_highest_price(self):

        statistics = self.analyzer.calculate_statistics()

        self.assertEqual(
            statistics["Highest Price"],
            118
        )

    def test_lowest_price(self):

        statistics = self.analyzer.calculate_statistics()

        self.assertEqual(
            statistics["Lowest Price"],
            102
        )

    def test_average_price(self):

        statistics = self.analyzer.calculate_statistics()

        expected_average = (
            102 + 108 + 112 + 110 + 118
        ) / 5

        self.assertEqual(
            statistics["Average Price"],
            expected_average
        )

    def test_latest_price(self):

        statistics = self.analyzer.calculate_statistics()

        self.assertEqual(
            statistics["Latest Price"],
            118
        )

    def test_daily_change(self):

        changes = self.analyzer.calculate_daily_change()

        self.assertTrue(
            pd.isna(changes.iloc[0])
        )

        self.assertAlmostEqual(
            changes.iloc[1],
            5.88235294,
            places=4
        )

    def test_empty_data(self):

        empty_analyzer = StockPriceAnalyzer("TEST")

        empty_analyzer.data = pd.DataFrame()

        with self.assertRaises(ValueError):
            empty_analyzer.calculate_statistics()


if __name__ == "__main__":
    unittest.main(verbosity=2)
