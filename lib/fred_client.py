import os

from dotenv import load_dotenv
import pandas as pd
import requests


class FredClient:
    BASE_URL = "https://api.stlouisfed.org/fred"

    DEFAULT_SERIES = {
        "gdp": "GDP",
        "real_gdp": "GDPC1",
        "cpi": "CPIAUCSL",
        "inflation_expectation": "T10YIE",
        "fed_funds_rate": "FEDFUNDS",
        "unemployment": "UNRATE",
        "m2_money_supply": "M2SL",
        "recession": "USREC",
        "treasury_2y": "DGS2",
        "treasury_10y": "DGS10",
        "treasury_30y": "DGS30",
        "baa_corporate_yield": "BAA",
        "high_yield_spread": "BAMLH0A0HYM2",
    }

    def __init__(self, api_key=None):
        load_dotenv()
        self.api_key = api_key or os.getenv("FRED_API_KEY")
        if not self.api_key:
            raise ValueError("Missing FRED API key. Set FRED_API_KEY or pass api_key")

    def get_series(
        self,
        series_id,
        start=None,
        end=None,
        frequency=None,
        aggregation_method=None,
    ):
        params = {
            "series_id": series_id,
            "api_key": self.api_key,
            "file_type": "json",
        }

        if start:
            params["observation_start"] = start
        if end:
            params["observation_end"] = end
        if frequency:
            params["frequency"] = frequency
        if aggregation_method:
            params["aggregation_method"] = aggregation_method

        url = f"{self.BASE_URL}/series/observations"
        response = requests.get(url, params=params, timeout=30)
        response.raise_for_status()

        data = response.json()["observations"]

        df = pd.DataFrame(data)
        df["date"] = pd.to_datetime(df["date"])
        df["value"] = pd.to_numeric(df["value"], errors="coerce")

        return df[["date", "value"]].dropna().set_index("date")

    def get(self, name, **kwargs):
        series_id = self.DEFAULT_SERIES.get(name)

        if not series_id:
            raise ValueError(
                f"Unknown name: {name}. Use one of {list(self.DEFAULT_SERIES.keys())}"
            )

        return self.get_series(series_id, **kwargs)

    def get_many(self, names, start=None, end=None):
        frames = []

        for name in names:
            df = self.get(name, start=start, end=end)
            df = df.rename(columns={"value": name})
            frames.append(df)

        return pd.concat(frames, axis=1)
