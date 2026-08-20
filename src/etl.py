# Build the analysis cross-section from the raw World Bank files.

import numpy as np
import pandas as pd

from paths import CLEAN_DATA, PROCESSED_DIR, RAW_DIR, SIGMA_DATA

MIN_POPULATION = 1_000_000
POPULATION_YEAR = 2024

# Aggregates and unclassified economies carry the literal code "NA".
INCOME_GROUP_CODES = ("HIC", "UMC", "LMC", "LIC")

# key, label, base year, end year
PERIODS = [
    ("pre_crisis", "Pre-Crisis (2004-2008)", 2004, 2008),
    ("recuperation", "Recuperation (2008-2013)", 2008, 2013),
    ("stability", "Stability (2013-2018)", 2013, 2018),
    ("recent", "Recent (2018-2024)", 2018, 2024),
    ("full", "Full sample (2004-2024)", 2004, 2024),
]


def load_raw():
    missing = [name for name in ("gdp_pc_level", "population", "country_metadata")
               if not (RAW_DIR / f"{name}.csv").exists()]
    if missing:
        raise FileNotFoundError(
            f"Missing raw files: {missing}. Run `python src/fetch_data.py` first."
        )
    levels = pd.read_csv(RAW_DIR / "gdp_pc_level.csv")
    population = pd.read_csv(RAW_DIR / "population.csv")
    # keep_default_na=False, or the "NA" aggregate code is read as missing.
    metadata = pd.read_csv(RAW_DIR / "country_metadata.csv", keep_default_na=False)
    return levels, population, metadata


def wide_levels(levels):
    wide = levels.pivot_table(
        index="country_code", columns="year", values="value", aggfunc="first"
    )
    wide.columns = [f"gdp_pc_{year}" for year in wide.columns]
    return wide.reset_index()


def build_dataset():
    levels, population, metadata = load_raw()

    countries = metadata[metadata["income_group_id"].isin(INCOME_GROUP_CODES)][
        ["country_code", "country_name", "region", "income_group", "income_group_id"]
    ]
    data = countries.merge(wide_levels(levels), on="country_code", how="inner")

    pop = population[population["year"] == POPULATION_YEAR][["country_code", "value"]]
    data = data.merge(pop.rename(columns={"value": "population"}),
                      on="country_code", how="left")
    data = data[data["population"] >= MIN_POPULATION].copy()
    data["group"] = np.where(data["income_group_id"] == "HIC", "Developed", "Emerging")

    required = [f"gdp_pc_{year}" for year in
                sorted({y for _, _, base, end in PERIODS for y in (base, end)})]
    before = len(data)
    data = data.dropna(subset=required)
    dropped = before - len(data)

    for key, _, base, end in PERIODS:
        horizon = end - base
        y0, yt = data[f"gdp_pc_{base}"], data[f"gdp_pc_{end}"]
        data[f"log_y0_{key}"] = np.log(y0)
        # Log-annualised growth in % per year, not the mean of annual rates:
        # averaging annual rates overstates growth for volatile series.
        data[f"growth_{key}"] = 100.0 * np.log(yt / y0) / horizon

    data["developed"] = (data["group"] == "Developed").astype(int)

    columns = (
        ["country_code", "country_name", "region", "income_group", "group",
         "developed", "population"]
        + [f"log_y0_{key}" for key, *_ in PERIODS]
        + [f"growth_{key}" for key, *_ in PERIODS]
        + [f"gdp_pc_{year}" for year in range(2004, 2025)
           if f"gdp_pc_{year}" in data.columns]
    )
    data = data[columns].sort_values("country_name").reset_index(drop=True)
    data.attrs["dropped_incomplete"] = dropped
    return data


def sigma_convergence(data, years=range(2004, 2025)):
    # Dispersion of log income: beta-convergence is necessary but not
    # sufficient for the distribution to actually narrow.
    rows = []
    for year in years:
        column = f"gdp_pc_{year}"
        if column not in data.columns:
            continue
        rows.append({"year": year, "group": "All",
                     "sd_log_gdp_pc": np.log(data[column]).std(ddof=1)})
        for group, chunk in data.groupby("group"):
            rows.append({"year": year, "group": group,
                         "sd_log_gdp_pc": np.log(chunk[column]).std(ddof=1)})
    return pd.DataFrame(rows)


def main():
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    data = build_dataset()
    data.to_csv(CLEAN_DATA, index=False)
    sigma_convergence(data).to_csv(SIGMA_DATA, index=False)

    print(f"Wrote {CLEAN_DATA.name}: {len(data)} countries "
          f"{data['group'].value_counts().to_dict()}")
    print(f"Dropped for incomplete GDP per capita series: "
          f"{data.attrs['dropped_incomplete']}")
    print(f"Wrote {SIGMA_DATA.name}")


if __name__ == "__main__":
    main()
