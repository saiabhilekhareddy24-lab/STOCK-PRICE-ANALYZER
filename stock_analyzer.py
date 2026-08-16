import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt


class StockPriceAnalyzer:

    def __init__(self, ticker, period="1mo"):
        self.ticker = ticker.upper()
        self.period = period
        self.data = None

    def fetch_data(self):
        """Download historical stock data."""
        self.data = yf.download(
            self.ticker,
            period=self.period,
            auto_adjust=False,
            progress=False
        )

        if self.data.empty:
            raise ValueError(
                f"No data found for ticker: {self.ticker}"
            )

        # Handle possible MultiIndex columns
        if isinstance(self.data.columns, pd.MultiIndex):
            self.data.columns = self.data.columns.get_level_values(0)

        return self.data

    def calculate_statistics(self):
        """Calculate basic stock statistics."""

        if self.data is None or self.data.empty:
            raise ValueError("Please fetch stock data first.")

        close_prices = self.data["Close"]

        statistics = {
            "Highest Price": float(close_prices.max()),
            "Lowest Price": float(close_prices.min()),
            "Average Price": float(close_prices.mean()),
            "Latest Price": float(close_prices.iloc[-1])
        }

        return statistics

    def calculate_daily_change(self):
        """Calculate daily percentage change."""

        if self.data is None or self.data.empty:
            raise ValueError("Please fetch stock data first.")

        self.data["Daily Change (%)"] = (
            self.data["Close"].pct_change() * 100
        )

        return self.data["Daily Change (%)"]

    def plot_price(self):
        """Display stock closing price chart."""

        if self.data is None or self.data.empty:
            raise ValueError("Please fetch stock data first.")

        plt.figure(figsize=(10, 5))

        plt.plot(
            self.data.index,
            self.data["Close"],
            color="blue",
            linewidth=2
        )

        plt.title(
            f"{self.ticker} Stock Price Analysis"
        )

        plt.xlabel("Date")
        plt.ylabel("Closing Price")
        plt.grid(True)

        plt.tight_layout()
        plt.show()

    def display_report(self):
        """Display analysis report."""

        statistics = self.calculate_statistics()

        print("\n======================================")
        print("       STOCK PRICE ANALYZER")
        print("======================================")

        print(f"Stock Symbol     : {self.ticker}")
        print(f"Analysis Period  : {self.period}")

        print("--------------------------------------")
        print(
            f"Highest Price    : "
            f"{statistics['Highest Price']:.2f}"
        )

        print(
            f"Lowest Price     : "
            f"{statistics['Lowest Price']:.2f}"
        )

        print(
            f"Average Price    : "
            f"{statistics['Average Price']:.2f}"
        )

        print(
            f"Latest Price     : "
            f"{statistics['Latest Price']:.2f}"
        )

        print("======================================\n")


def main():

    print("Stock Price Analyzer")
    print("--------------------")

    ticker = input(
        "Enter stock symbol (example: AAPL): "
    ).strip()

    period = input(
        "Enter analysis period (example: 1mo, 3mo, 6mo, 1y): "
    ).strip()

    if not period:
        period = "1mo"

    try:

        analyzer = StockPriceAnalyzer(
            ticker,
            period
        )

        print("\nDownloading stock data...")

        analyzer.fetch_data()

        print("Data downloaded successfully.")

        analyzer.display_report()

        analyzer.calculate_daily_change()

        analyzer.plot_price()

    except Exception as error:

        print(
            f"\nError: {error}"
        )


if __name__ == "__main__":
    main()
