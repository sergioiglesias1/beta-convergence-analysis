# Beta-Convergence Analysis of Country Growth with Python and R

![Python >= 3.13](https://img.shields.io/badge/Python-%3E%3D3.13-blue?logo=python&logoColor=white)
![R >= 4.5.1](https://img.shields.io/badge/R-%3E%3D4.5.1-276DC3?logo=r&logoColor=white)
![scikit-learn](https://img.shields.io/badge/scikit--learn-F7931E?logo=scikit-learn&logoColor=white)

This project analyzes **β-convergence** in economic growth between emerging and developed countries using GDP per capita data from 2004 to 2024. β-convergence examines whether poorer economies tend to grow faster than richer ones, potentially reducing income disparities over time.

---

## Project Overview

β-convergence is estimated using **cross-sectional regressions** of average GDP per capita growth rates across four periods:

- Pre-Crisis (2004–2008)  
- Recuperation (2009–2013)  
- Stability (2014–2018)  
- Recent (2019–2024)

The workflow combines Python for visualization and data handling with R for econometric inference.

#### Interpretation of β Coefficients:

* **β < 0**: Indicates convergence <=> Poorer economies growing faster
* **β > 0**: Indicates divergence <=> Richer economies maintaining growth advantage

## Methodology

- **Data source**: World Development Indicators (WDI)  
- **Sample**: 58 countries (Emerging vs Developed)  
- **Approach**:
  - Period-average GDP per capita growth
  - OLS β-convergence regressions
  - Robust standard errors (HC1)
  - Linear Probability Model for development status
## Dataset Description

### Source

World Development Indicators (WDI) - 2004-2024

[Official Data Source](https://databank.worldbank.org/reports.aspx?source=2&series=NY.GDP.PCAP.KD.ZG&country=#)

### Structure

* **Country Code**: Unique identifier (e.g., USA, CHL, IND)
* **Group**: Economic classification ('Emerging' or 'Developed')
* **Period Growth Rates**:

  * **Pre-Crisis** (2004-2008)
  * **Recuperation** (2009-2013)
  * **Stability** (2014-2018)
  * **Recent** (2019-2024)

## File Structure

```
.
├── data/
│   ├── clean_data.csv        
│   └── gdp_data.csv         
├── visualizations/
│   ├── R_outputs/           
│   └── python_outputs/      
├── .gitignore
├── ETL.ipynb               
├── install_r_packages.R
├── LICENSE
├── main.py               
├── plots.py
├── README.md
├── regressions.R
└── requirements.txt
```

## Methodology

### Analytical Tools

#### Python Libraries:

```python
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import LinearRegression
```

#### R Libraries:

```r
library(sandwich)
library(lmtest)
```

### Data Processing

1. Import and clean WDI dataset
2. Calculate average growth rates for each period
3. Classify countries into Emerging/Developed groups
4. Remove empty rows and standardize column names

## Visualizations

### 1. Correlation Matrix Heatmap

* **Tool**: Python/Seaborn
* **Purpose**: Explore relationships between growth periods
* **Output**: Inter-period correlation overview

### 2. Beta-Convergence Analysis Plots

**Tool**: Python/Matplotlib

**Three Key Comparisons**:

1. Stability (2014-2018) vs. Recuperation (2009-2013)
2. Recent (2019-2024) vs. Pre-Crisis (2004-2008)
3. Recuperation (2009-2013) vs. Pre-Crisis (2004-2008)

*Each visualization includes regression lines and β coefficients*

## Regression Analysis

### Single-Variable Models

#### Regression 1: Stability vs. Recuperation

```r
sreg1 <- lm(Stability..2014.2018. ~ Recuperation..2009.2013., data=df_wdi)
summary(sreg1)
coeftest(sreg1, vcov = vcovHC(sreg1, type="HC1"))
```

#### Regression 2: Recent vs. Pre-Crisis

```r
sreg2 <- lm(Recent..2019.2024. ~ Pre_Crisis..2004.2008., data=df_wdi)
summary(sreg2)
coeftest(sreg2, vcov = vcovHC(sreg2, type="HC1"))
```

#### Regression 3: Recuperation vs. Pre-Crisis

```r
sreg3 <- lm(Recuperation..2009.2013. ~ Pre_Crisis..2004.2008., data=df_wdi)
summary(sreg3)
coeftest(sreg3, vcov = vcovHC(sreg3, type="HC1"))
```

### Multivariate Regression Model

#### Theoretical Specification

The model is specified as:

```math
Developed_i = β_0 + β_1 * PreCrisisGrowth_i + β_2 * RecuperationGrowth_i + u_i
```

#### R Implementation

```r
mreg <- glm(developed ~ Pre_Crisis..2004.2008. + 
                    Recuperation..2009.2013.,
                  data=df_wdi)
summary(mreg)
vif(mreg)
coeftest(mreg, vcov = vcovHC(mreg, type="HC1")) 
```

#### Model Parameters

* **Sample**: 58 countries
* **Dependent Variable**: `Developedᵢ ∈ {1, 0}` where:
  - `1` = Developed economy
  - `0` = Emerging economy
* **Independent Variables**:
  * `PreCrisisGrowthᵢ`: Average GDP growth (2004-2008)
  * `RecuperationGrowthᵢ`: Average GDP growth (2009-2013)
* **Error Term**: `uᵢ`, `∀` `𝔼[uᵢ|Xᵢ] = 0`

---

## Key Findings

### Emerging Economies
- Persistent **divergence**
- Positive β coefficients across all periods
- Faster-growing economies maintain their advantage

### Developed Economies
- Weak convergence in early periods
- Shift toward divergence in recent years
- No evidence of long-run income equalization

---

## Conclusion
The analysis reveals distinct growth patterns between emerging and developed economies, with emerging markets showing persistent divergence while developed economies transition from weak convergence to divergence in recent years. These findings provide valuable insights for economic policy formulation and international development strategies.
