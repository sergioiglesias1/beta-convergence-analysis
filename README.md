# Beta-Convergence Analysis of Country Growth with Python

## Overview
This project analyzes β-convergence in economic growth between emerging and developed countries using GDP per capita data from 2004 to 2024. β-convergence examines whether poorer economies tend to grow faster than richer ones, potentially "catching up" over time. To see the whole process and output generated please click this link here: https://sergioiglesias1.github.io/myportfolio/project.html

## What is β-Convergence and Why is it Important?
β-Convergence is an economic concept that examines whether economies with lower initial growth rates tend to grow faster than those with higher initial rates. In this analysis, we regress GDP per capita growth rates in later periods against earlier periods:

- **β < 0**: Indicates convergence (poorer economies growing faster)
- **β > 0**: Indicates divergence (richer economies continuing to grow faster)

This analysis helps policymakers assess whether economic disparities between countries are narrowing over time and how global events (financial crises, pandemics) affect growth patterns.

## Dataset Description
The dataset contains GDP per capita growth data from World Development Indicators (WDI) between 2004-2024:

- **Country Code**: Unique identifier for each country (e.g., USA, CHL, IND)
- **Group**: Classification as 'Emerging' or 'Developed'
- **Period Growth Rates**: Calculated for four time periods:
  - Pre-Crisis (2004-2008)
  - Recuperation (2009-2013)
  - Stability (2014-2018)
  - Recent (2019-2024)

## Methodology

### Data Processing
- Import and clean WDI dataset
- Calculate average growth rates for each period
- Classify countries into Emerging and Developed groups
- Remove empty rows and clean column names

### Country Classification
**Emerging Economies**: CHL, POL, ETH, VNM, IND, EGY, IDN, PER, MAR, PHL, NGA, BGD, PAK, MOZ  
**Developed Economies**: USA, CHE, LUX, GBR, KOR, IRL, DEU, ESP, JPN, CAN, AUS, NOR, NLD, DNK, SWE, FIN

### Analytical Approach
- Implement linear regression to calculate β coefficients
- Compute R² values to assess model fit
- Visualize convergence/divergence patterns across different time periods
- Compare results between emerging and developed economies

## Key Findings

### Emerging Economies
- Show clear and growing divergence across all periods
- Positive β coefficients (0.47, 0.54, 0.69) indicate no convergence
- Faster-growing economies continue to grow rapidly

### Developed Economies
- Transition from weak convergence to moderate divergence
- Slightly negative β in early periods (-0.24, -0.13) indicating mild convergence
- Shift to positive β in recent periods suggesting emerging divergence

## Visualization
The project includes three main visualizations comparing growth rates across different periods:

1. **Pre-Crisis (2004-2008) vs. Recent (2019-2024)**
2. **Post-Crisis (2009-2013) vs. Stability (2014-2018)**
3. **Stability (2014-2018) vs. Recent (2019-2014)**

Each plot displays regression lines, β coefficients, and R² values for both country groups.

## Technical Implementation

### Libraries Used
```python
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score
