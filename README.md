# Finance Project

Small Python helper for pulling economic data from the FRED API.

Official FRED API docs:
https://fred.stlouisfed.org/docs/api/fred/series_observations.html

## Setup

Install dependencies:

```bash
pip install -r requirements.txt
```

Create a `.env` file in the project root:

```bash
FRED_API_KEY=your_api_key_here
```

## Basic Usage

```python
from lib import FredClient

fred = FredClient()

fred.get("gdp").tail()
```

You can also request a FRED series directly by its official series ID:

```python
fred.get_series("GDP").tail()
```

## `get_series` Parameters

```python
fred.get_series(
    series_id,
    start=None,
    end=None,
    frequency=None,
    aggregation_method=None,
)
```

`series_id` is the official FRED series code.

Examples:

```python
"GDP"       # Gross Domestic Product
"GDPC1"     # Real GDP
"CPIAUCSL"  # CPI
"UNRATE"    # Unemployment rate
"FEDFUNDS"  # Federal funds rate
"DGS10"     # 10-year Treasury rate
```

`start` and `end` filter the observation date range. Use `YYYY-MM-DD` strings.

```python
fred.get_series("GDP", start="2015-01-01", end="2024-12-31")
```

`frequency` aggregates data 

Common values:

```python
"d"   # daily
"w"   # weekly
"bw"  # biweekly
"m"   # monthly
"q"   # quarterly
"sa"  # semiannual
"a"   # annual
```

More specific weekly and biweekly values:

```python
"wem"   # weekly ending Monday
"wetu"  # weekly ending Tuesday
"wew"   # weekly ending Wednesday
"weth"  # weekly ending Thursday
"wef"   # weekly ending Friday
"wesa"  # weekly ending Saturday
"wesu"  # weekly ending Sunday
"bwew"  # biweekly ending Wednesday
"bwem"  # biweekly ending Monday
```

`aggregation_method` controls how values are combined when `frequency` is used.

```python
"avg"  # average
"sum"  # sum
"eop"  # end of period
```

`aggregation_method` only matters when `frequency` is set.

## Examples

Get unemployment data for a date range:

```python
fred.get_series(
    "UNRATE",
    start="2020-01-01",
    end="2024-12-31",
).tail()
```

Get daily 10-year Treasury rates aggregated to monthly averages:

```python
fred.get_series(
    "DGS10",
    start="2023-01-01",
    end="2024-12-31",
    frequency="m",
    aggregation_method="avg",
).tail()
```

Get daily 10-year Treasury rates aggregated to quarterly end-of-period values:

```python
fred.get_series(
    "DGS10",
    start="2023-01-01",
    end="2024-12-31",
    frequency="q",
    aggregation_method="eop",
).tail()
```

## Shortcut Series Names

The client includes these shortcut names:

```python
fred.get("gdp")
fred.get("real_gdp")
fred.get("cpi")
fred.get("inflation_expectation")
fred.get("fed_funds_rate")
fred.get("unemployment")
fred.get("m2_money_supply")
fred.get("recession")
fred.get("treasury_2y")
fred.get("treasury_10y")
fred.get("treasury_30y")
fred.get("baa_corporate_yield")
fred.get("high_yield_spread")
```

You can pass the same date and aggregation options to shortcuts:

```python
fred.get(
    "treasury_10y",
    start="2023-01-01",
    end="2024-12-31",
    frequency="m",
    aggregation_method="avg",
).tail()
```

You can also load multiple shortcut series into one DataFrame:

```python
fred.get_many(
    ["gdp", "unemployment", "fed_funds_rate"],
    start="2020-01-01",
    end="2024-12-31",
).tail()
```

## Notes

`frequency` can aggregate higher-frequency data down, such as daily data to monthly or quarterly. It cannot convert lower-frequency data into higher-frequency data.
