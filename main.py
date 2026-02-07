# Import packages
import pandas as pd
from plots import plot_beta_convergence

try:
    clean_data = pd.read_csv(r"data/clean_data.csv")
except FileNotFoundError:
    print("File not found. Please run the ETL.ipynb file first to generate the clean data file.")

# First plot
plot_beta_convergence(
    clean_data, 
    'Stability (2014-2018)', 'Recuperation (2009-2013)',
    'Stability Growth (%)', 'Recuperation Growth (%)',
    'β-Convergence: Stability (2014-2018) vs. Recuperation (2009-2013)'
)

# Second plot
plot_beta_convergence(
    clean_data, 
    'Recent (2019-2024)', 'Pre_Crisis (2004-2008)',
    'Recent Growth (%)', 'Pre-Crisis Growth (%)',
    'β-Convergence: Recent (2019-2024) vs. Pre-Crisis (2004-2008)'
)

# Third plot
plot_beta_convergence(
    clean_data, 
    'Recuperation (2009-2013)', 'Pre_Crisis (2004-2008)',
    'Recuperation Growth (%)', 'Pre-Crisis Growth (%)',
    'β-Convergence: Recuperation (2009-2013) vs. Pre-Crisis (2004-2008)'
)
