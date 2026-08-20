import sys
import pandas as pd

from etl import PERIODS
from paths import CLEAN_DATA, SIGMA_DATA
from plots import (plot_beta_convergence, plot_correlation_matrix,
                   plot_sigma_convergence)


def load(path):
    if not path.exists():
        sys.exit(f"{path} not found. Run `python src/fetch_data.py` "
                 f"and `python src/etl.py` first.")
    return pd.read_csv(path)


def main():
    data = load(CLEAN_DATA)
    dispersion = load(SIGMA_DATA)

    for (key, label, base, end) in PERIODS:
        path = plot_beta_convergence(data, key, label, end - base, f"beta_{key}.png")
        print(f"Wrote {path.name}")

    print(f"Wrote {plot_sigma_convergence(dispersion, 'sigma_convergence.png').name}")
    print(f"Wrote {plot_correlation_matrix(data, 'correlation_matrix.png').name}")


if __name__ == "__main__":
    main()
