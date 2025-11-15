# Beta-Convergence Analysis of Country Growth with Python and R

## Overview

This project analyzes **β-convergence** in economic growth between emerging and developed countries using GDP per capita data from 2004 to 2024. β-convergence examines whether poorer economies tend to grow faster than richer ones, potentially reducing income disparities over time.

> **Note:** The data is not scaled as we are working with homogeneous GDP per capita growth rates.

## Theoretical Framework

### What is β-Convergence?

β-Convergence is an economic concept that tests whether economies with lower initial income levels tend to grow faster than their richer counterparts. In this analysis, we examine growth rate patterns across different economic periods by regressing later period growth rates against earlier periods.

#### Interpretation of β Coefficients:

* **β < 0**: Indicates convergence (poorer economies growing faster)
* **β > 0**: Indicates divergence (richer economies maintaining growth advantage)

#### Policy Relevance:

This analysis helps policymakers assess whether economic disparities between countries are narrowing over time and understand how global events influence growth patterns.

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
│   ├── clean_wdi.csv        # Original data
│   └── wdi_data.csv         # Clean and processed data
├── visualizations/
│   ├── R_outputs/           # Plots in python
│   └── python_outputs/      # Regressions in R
├── .gitignore
├── LICENSE
├── README.md
├── main.ipynb               # Main training
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
library(car)
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

1. **Stability (2014-2018)** vs. **Recuperation (2009-2013)**
2. **Recent (2019-2024)** vs. **Pre-Crisis (2004-2008)**
3. **Recuperation (2009-2013)** vs. **Pre-Crisis (2004-2008)**

*Each visualization includes regression lines and β coefficients*

## Regression Analysis

### Single-Variable Models

#### Regression 1: Stability vs. Recuperation

```r
sreg1 <- lm(Stability_Growth..2014.2018._y ~ Recuperation_Growth..2009.2013._y, data=wdi)
summary(sreg1)
coeftest(sreg1, vcov = vcovHC(sreg1, type="HC1"))
```

#### Regression 2: Recent vs. Pre-Crisis

```r
sreg2 <- lm(Recent_Growth..2019.2024._y ~ Pre_Crisis_Growth..2004.2008._y, data=wdi)
summary(sreg2)
coeftest(sreg2, vcov = vcovHC(sreg2, type="HC1"))
```

#### Regression 3: Recuperation vs. Pre-Crisis

```r
sreg3 <- lm(Recuperation_Growth..2009.2013._y ~ Pre_Crisis_Growth..2004.2008._y, data=wdi)
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
multimodel <- glm(Developed ~ Pre_Crisis_Growth..2004.2008._y +
                   Recuperation_Growth..2009.2013._y,
                 data = wdi)
summary(multimodel)
car::vif(multimodel)
coeftest(multimodel, vcov = vcovHC(multimodel, type="HC1"))
```

#### Model Parameters

* **Sample**: 30 countries
* **Dependent Variable**: `Developedᵢ ∈ {1, 0}` where:
  - `1` = Developed economy
  - `0` = Emerging economy
* **Independent Variables**:
  * `PreCrisisGrowthᵢ`: Average GDP growth (2004-2008)
  * `RecuperationGrowthᵢ`: Average GDP growth (2009-2013)
* **Error Term**: `uᵢ`, `∀` `𝔼[uᵢ|Xᵢ] = 0`

### Multicollinearity Assessment

* All regressions now use regular and robust standard errors to correct for potential heteroscedasticity and better significance levels
* **VIF Score**: 3.4757
* **Interpretation**: Moderate correlation between predictors
* **Conclusion**: Acceptable level, no harmful multicollinearity detected

## Key Findings

### Emerging Economies

* **Pattern**: Clear and growing divergence across all periods
* **Evidence**: Positive β coefficients (0.38, 0.23)
* **Interpretation**: No convergence observed; faster-growing economies maintain momentum

### Developed Economies

* **Early Periods**: Weak convergence (β = -0.14, -0.30)
* **Recent Periods**: Shift toward divergence (positive β)
* **Trend**: Transition from mild convergence to emerging divergence

## Limitations

* **Small sample**: Only 30 countries, so statistical power is limited.  
* **Cross-sectional data**: No panel structure; unobserved heterogeneity may bias results.  
* **LPM limitations**: Binary dependent variable; probabilities can fall outside [0,1].  

## Conclusion

The analysis reveals distinct growth patterns between emerging and developed economies, with emerging markets showing persistent divergence while developed economies transition from weak convergence to divergence in recent years. These findings provide valuable insights for economic policy formulation and international development strategies.