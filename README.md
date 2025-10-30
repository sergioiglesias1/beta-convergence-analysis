# Beta-Convergence Analysis of Country Growth with Python and R

## Overview
This project analyzes β-convergence in economic growth between emerging and developed countries using GDP per capita data from 2004 to 2024. β-convergence examines whether poorer economies tend to grow faster than richer ones.
**There is an important detail here, which is that the data is not scaled since we are working with the same types of data (GDP per capita)**.

## What is β-Convergence and Why is it Important?
β-Convergence is an economic concept that examines whether economies with lower initial growth rates tend to grow faster than those with higher initial rates. In this analysis, we regress GDP per capita growth rates in later periods against earlier periods:

- **β < 0**: Indicates convergence (poorer economies growing faster)
- **β > 0**: Indicates divergence (richer economies continuing to grow faster)

This analysis helps policymakers assess whether economic disparities between countries are narrowing over time and how global events are affecting growth patterns.

## Dataset Description
The dataset contains GDP per capita growth data from World Development Indicators (WDI) between 2004-2024:
- **Country Code**: Unique identifier for each country (e.g., USA, CHL, IND)
- **Group**: Classification as 'Emerging' or 'Developed'
- **Period Growth Rates**: Calculated for four time periods:
  - Pre-Crisis (2004-2008)
  - Recuperation (2009-2013)
  - Stability (2014-2018)
  - Recent (2019-2024)
    
This repository has the data already in a csv, to access the official website feel free to investigate through this link: https://databank.worldbank.org/reports.aspx?source=2&series=NY.GDP.PCAP.KD.ZG&country=#

## Analytical Framework

### Python Components
- Data preprocessing and cleaning
- Correlation matrix visualization (Seaborn)
- Beta-convergence plots with regression lines (Matplotlib)
- Initial coefficient calculations

### R Components  
- Multicollinearity detection via VIF analysis
- Statistical significance testing of β coefficients
- Comprehensive regression diagnostics

### Libraries Used
```python
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import LinearRegression
```

```r
library(car)
```

## Data Processing
- Import and clean WDI dataset
- Calculate average growth rates for each period
- Classify countries into Emerging and Developed groups
- Remove empty rows and clean column names

## Visualization Structure

The project includes a comprehensive visualization approach:

### Correlation Matrix Heatmap (Python/Seaborn)
- First visualization showing relationships between growth periods
- Provides overview of inter-period correlations

### Three Main Beta-Convergence Plots (Python/Matplotlib)
- **Stability (2014-2018) vs. Recuperation (2009-2013)**
- **Recent (2019-2024) vs. Pre-Crisis (2004-2008)**
- **Recuperation (2009-2013) vs. Pre-Crisis (2004-2008)**
- Each plot displays regression lines and the β coefficients

## Output findings

### Emerging Economies
- Show clear and growing divergence across all periods
- Positive β coefficients (0.38, 0.23) indicate no convergence
- Faster-growing economies continue to grow rapidly

### Developed Economies
- Transition from weak convergence to moderate divergence
- Slightly negative β in early periods (-0.14, -0.30) indicating mild convergence
- Shift to positive β in recent periods suggesting emerging divergence
