import json
import time
import urllib.error
import urllib.request

import pandas as pd

from paths import RAW_DIR

API = "https://api.worldbank.org/v2"
(START_YEAR, END_YEAR) = (2004, 2024)

INDICATORS = {
    "gdp_pc_level": "NY.GDP.PCAP.KD",
    "gdp_pc_growth": "NY.GDP.PCAP.KD.ZG",
    "population": "SP.POP.TOTL",
}

# the aim is to download the raw indicators from the World Bank API
# NY.GDP.PCAP.KD

def get_json(url, retries=3, backoff=2.0):
    last_error = None
    for attempt in range(retries):
        try:
            with urllib.request.urlopen(url, timeout=60) as response:
                return json.loads(response.read().decode("utf-8"))
        except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as error:
            last_error = error
            if attempt < retries - 1:
                time.sleep(backoff * (attempt + 1))
    raise RuntimeError(f"World Bank API request failed: {url}") from last_error


def fetch_indicator(code):
    url = (
        f"{API}/country/all/indicator/{code}"
        f"?format=json&date={START_YEAR}:{END_YEAR}&per_page=20000"
    )
    payload = get_json(url)
    if len(payload) < 2 or payload[1] is None:
        raise RuntimeError(f"No observations returned for indicator {code}")

    records = [
        {
            "country_code": row["countryiso3code"],
            "country_name": row["country"]["value"],
            "year": int(row["date"]),
            "value": row["value"],
        }
        for row in payload[1]
        if row["countryiso3code"]
    ]
    return pd.DataFrame.from_records(records)


def fetch_country_metadata():
    payload = get_json(f"{API}/country?format=json&per_page=400")
    records = [
        {
            "country_code": row["id"],
            "country_name": row["name"],
            "region": row["region"]["value"],
            "region_id": row["region"]["id"],
            "income_group": row["incomeLevel"]["value"],
            "income_group_id": row["incomeLevel"]["id"],
        }
        for row in payload[1]
    ]
    return pd.DataFrame.from_records(records)


def main():
    RAW_DIR.mkdir(parents=True, exist_ok=True)

    for (name, code) in INDICATORS.items():
        frame = fetch_indicator(code)
        path = RAW_DIR / f"{name}.csv"
        frame.to_csv(path, index=False)
        print(f"{code:<20} -> {path.name}  ({len(frame)} rows, "
              f"{frame['value'].notna().sum()} non-missing)")

    metadata = fetch_country_metadata()
    metadata.to_csv(RAW_DIR / "country_metadata.csv", index=False)
    print(f"{'country metadata':<20} -> country_metadata.csv  ({len(metadata)} rows)")


if __name__ == "__main__":
    main()
