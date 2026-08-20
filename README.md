# Beta-Convergence of GDP per capita, 2004-2024

![Python >= 3.11](https://img.shields.io/badge/Python-%3E%3D3.11-blue?logo=python&logoColor=white)
![R >= 4.5](https://img.shields.io/badge/R-%3E%3D4.5-276DC3?logo=r&logoColor=white)
![statsmodels](https://img.shields.io/badge/statsmodels-8CAAE6)
![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)

Cross-country test of **β-convergence**: do poorer economies grow faster than
richer ones, so that income gaps close over time? Estimated on 153 economies
with World Bank data for 2004-2024, using Python for the data pipeline and
figures and R for inference.

---

## Specification

β-convergence, following Barro & Sala-i-Martin (1992), regresses the
annualised growth rate of GDP per capita over a period on the **log of income
at the start of that period**:

$$\frac{1}{T}\ln\left(\frac{y_{iT}}{y_{i0}}\right) = \alpha + \beta \ln(y_{i0}) + u_i$$

- **β < 0** → convergence: economies that started poorer grew faster.
- **β > 0** → divergence.

The regressor is the **income level** in the base year. Regressing growth in
one period on growth in an earlier period is a different exercise — it measures
persistence of growth, or mean reversion in growth rates — and its sign says
nothing about whether poor countries are catching up. That distinction drives
the whole design of this repository.

From β the standard summary statistics follow:

$$\beta = -\frac{1 - e^{-\lambda T}}{T} \quad\Longrightarrow\quad \lambda = -\frac{\ln(1 + \beta T)}{T}, \qquad t_{1/2} = \frac{\ln 2}{\lambda}$$

where λ is the annual speed of convergence and $t_{1/2}$ the half-life of a
deviation from steady state. The canonical benchmark in the literature is
λ ≈ 2% per year.

Three models are estimated for every period:

| Model | Specification | Question |
|---|---|---|
| Unconditional | `growth ~ log(y0)` | Do all economies converge to a common income level? |
| Conditional | `growth ~ log(y0) + developed` | Do they converge once steady states are allowed to differ? |
| Convergence clubs | `growth ~ log(y0) * developed` | Do the two groups converge at *different speeds*? |

Alongside β, **σ-convergence** — the cross-sectional standard deviation of
log GDP per capita — is reported. β-convergence is necessary but not
sufficient for the income distribution to actually narrow, so the two answer
different questions.

---

## Data

| Item | Value |
|---|---|
| Source | World Bank, World Development Indicators (API v2) |
| Indicators | `NY.GDP.PCAP.KD` (level, constant 2015 US$), `NY.GDP.PCAP.KD.ZG` (growth), `SP.POP.TOTL` |
| Coverage | 2004-2024 |
| Sample | 153 economies (50 high income, 103 other) |

**Sample selection** is a rule, not a hand-picked list: every World Bank member
economy that (i) is not a regional or income aggregate, (ii) has a World Bank
income classification, (iii) has at least 1,000,000 inhabitants in 2024, and
(iv) reports GDP per capita in every year the periods require. Six economies are
dropped for incomplete series. The population floor keeps micro-states and
offshore financial centres from dominating a cross-section of this size.

`Developed` = World Bank high-income group; `Emerging` = everything else. Using
a published classification rather than a personal list means the sample cannot
be tuned to the result.

**Periods.** Each period is defined by its base year and end year, and growth
runs from the level at the base year to the level at the end year:

| Period | Base → End | T |
|---|---|---|
| Pre-Crisis | 2004 → 2008 | 4 |
| Recuperation | 2008 → 2013 | 5 |
| Stability | 2013 → 2018 | 5 |
| Recent | 2018 → 2024 | 6 |
| Full sample | 2004 → 2024 | 20 |

Growth is the **log-annualised** rate, `(1/T)·ln(y_T/y_0)`, not the arithmetic
mean of annual growth rates. Averaging annual rates overstates growth for
volatile series, which biases the comparison towards emerging economies
precisely where the analysis is most sensitive.

---

## Results

Unconditional β with HC1 standard errors, n = 153:

| Period | T | β | HC1 s.e. | p | R² | λ | Half-life |
|---|---|---|---|---|---|---|---|
| Pre-Crisis (2004-2008) | 4 | −0.334 | 0.148 | 0.026 | 0.024 | 0.34%/yr | 206 yrs |
| Recuperation (2008-2013) | 5 | −0.789 | 0.138 | <0.001 | 0.195 | 0.81%/yr | 86 yrs |
| Stability (2013-2018) | 5 | −0.213 | 0.125 | 0.089 | 0.013 | 0.21%/yr | 324 yrs |
| Recent (2018-2024) | 6 | +0.095 | 0.124 | 0.445 | 0.003 | — | — |
| **Full sample (2004-2024)** | 20 | **−0.354** | 0.083 | <0.001 | 0.082 | 0.37%/yr | 189 yrs |

Conditional β (controlling for development status) and the club interaction:

| Period | β conditional | λ conditional | Club interaction p |
|---|---|---|---|
| Pre-Crisis | −0.261 | 0.26%/yr | <0.001 |
| Recuperation | −0.577 | 0.59%/yr | 0.778 |
| Stability | −0.648 | 0.66%/yr | 0.200 |
| Recent | −0.039 | 0.04%/yr | 0.035 |
| Full sample | −0.568 | 0.60%/yr | 0.001 |

σ-convergence, standard deviation of log GDP per capita:

| Year | All | Developed | Emerging |
|---|---|---|---|
| 2004 | 1.507 | 0.725 | 0.953 |
| 2008 | 1.492 | 0.643 | 0.981 |
| 2013 | 1.438 | 0.629 | 0.962 |
| 2018 | 1.429 | 0.599 | 0.948 |
| 2024 | 1.445 | 0.575 | 0.970 |

### Reading of the results

1. **Over the full 2004-2024 window there is unconditional β-convergence, but
   it is slow.** β = −0.354 (p < 0.001) implies λ = 0.37% per year and a
   half-life of roughly 189 years — an order of magnitude below the canonical
   2%. Statistically significant, economically almost irrelevant on a policy
   horizon.
2. **Conditioning on development status roughly doubles the speed**
   (λ = 0.60%/yr over the full sample). This is the standard result: economies
   converge towards their own steady state, not towards a common one.
3. **The interaction with `developed` is significant over the full sample
   (p = 0.001)**, so the two groups do not share one convergence process —
   evidence of convergence *clubs* rather than global catch-up.
4. **The result is driven by one sub-period.** Convergence is strong in
   2008-2013 (λ = 0.81%/yr, R² = 0.19), weak in 2013-2018, and absent in
   2018-2024, where β turns positive and insignificant. Much of the "catch-up"
   in the full-sample estimate is the post-2008 window, when advanced economies
   contracted, rather than sustained convergence.
5. **σ-convergence is much weaker than β-convergence.** Overall dispersion falls
   only from 1.507 to 1.445 across twenty years, and rises again after 2018.
   Within the developed group dispersion falls steadily (0.725 → 0.575); within
   the emerging group it is flat. The distribution is not meaningfully
   narrowing.

---

## Diagnostics and robustness

Everything below is reported in `results/regressions_output.txt`.

- **HC1 robust standard errors** throughout. Breusch-Pagan rejects
  homoskedasticity only in the 2018-2024 period (p = 0.047) and is borderline
  over the full sample (p = 0.071), so robust errors are a precaution here
  rather than a rescue — reported either way, since growth variance plainly
  differs across income groups.
- **RESET test** for functional form on every unconditional regression.
- **Influence.** With n = 153, Cook's distance above 4/n is reported and each
  regression is refit without those observations. Over the full sample β moves
  from −0.354 to −0.360 when the 8 most influential economies are excluded, so
  the headline result does not rest on outliers.
- **VIF** for the conditional model.

## Known limitations

- **Galton's fallacy / regression to the mean.** Measurement error in $y_{i0}$
  biases β downwards even without genuine convergence, because the regressor
  appears (with opposite sign) on both sides of the equation. A negative β from
  a single cross-section is weaker evidence than it looks.
- **Selection on survivors.** The sample is economies that exist today and
  report continuous data, which excludes the worst growth outcomes.
- **COVID-19.** The 2018-2024 period contains the 2020 collapse and the 2021
  rebound. The positive β there should not be read as a structural break.
- **Steady states are proxied by one dummy.** A proper conditional test would
  control for investment, human capital and institutions; `developed` is a
  coarse stand-in.
- **Cross-section, not panel.** Panel estimation with country fixed effects
  would address unobserved heterogeneity, at the cost of the well-known Nickell
  bias in dynamic panels.

A linear probability model of development status on past growth was present in
an earlier version of this project and has been removed: it regressed an outcome
determined over more than a century on growth in a five-year window, so the
causality ran backwards and the coefficients were not interpretable.

---

## Reproducing the analysis

```bash
pip install -r requirements.txt
Rscript install_r_packages.R

python fetch_data.py     # download raw indicators from the World Bank API
python etl.py            # build data/clean_data.csv and data/sigma_convergence.csv
python main.py           # write figures to visualizations/python_outputs/
Rscript regressions.R    # estimate, test, write results/
```

Every step is reproducible from the API: no manual download from the DataBank
web interface is involved.

## Project structure

```
.
├── data/
│   ├── raw/                      # downloaded indicators (fetch_data.py)
│   ├── clean_data.csv            # analysis cross-section (etl.py)
│   └── sigma_convergence.csv     # dispersion of log GDP pc by year
├── results/
│   ├── regression_summary.csv    # one row per period
│   └── regressions_output.txt    # full console log of regressions.R
├── visualizations/
│   └── python_outputs/           # beta_*.png, sigma_convergence.png...
├── ETL.ipynb                     # exploratory notebook
├── fetch_data.py                 # World Bank API download
├── etl.py                        # sample selection and variable construction
├── plots.py                      # figure functions
├── main.py                       # regenerates every figure
├── regressions.R                 # OLS, HC1, diagnostics, convergence speeds
├── install_r_packages.R
├── requirements.txt
└── LICENSE
```

## Tooling

Python (`pandas`, `numpy`, `matplotlib`, `seaborn`, `statsmodels`) handles the
pipeline and the figures; R (`sandwich`, `lmtest`, `car`) handles inference.
The full-sample estimate is computed in both and agrees to four decimals, which
is the point of keeping the two paths.

## References

- Barro, R. J. & Sala-i-Martin, X. (1992). *Convergence*. Journal of Political Economy, 100(2), 223-251.
- Quah, D. (1993). *Galton's Fallacy and Tests of the Convergence Hypothesis*. Scandinavian Journal of Economics, 95(4), 427-443.
- Sala-i-Martin, X. (1996). *The Classical Approach to Convergence Analysis*. Economic Journal, 106(437), 1019-1036.

## License

MIT. See [LICENSE](LICENSE).
