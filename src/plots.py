import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import statsmodels.api as sm

from paths import FIGURES_DIR

GROUP_COLORS = {"Emerging": "#1f77b4", "Developed": "#ff7f0e", "All": "#444444"}

def save(fig, filename):
    FIGURES_DIR.mkdir(parents=True, exist_ok=True)
    path = FIGURES_DIR / filename
    fig.savefig(path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    return path

def implied_speed(beta_pct, horizon):
    # beta = -(1 - exp(-lambda*T))/T, with beta rescaled from % to a rate.
    # Undefined for beta >= 0, which is divergence.
    beta = beta_pct / 100.0
    argument = 1.0 + beta * horizon
    if beta >= 0 or argument <= 0:
        return float("nan"), float("nan")
    speed = -np.log(argument) / horizon
    return speed, np.log(2.0) / speed


def plot_beta_convergence(data, period_key, period_label, horizon, filename):
    x_col, y_col = f"log_y0_{period_key}", f"growth_{period_key}"
    fig, ax = plt.subplots(figsize=(10, 6))

    for group in ("Emerging", "Developed"):
        chunk = data[data["group"] == group]
        if chunk.empty:
            continue

        x, y = chunk[x_col].to_numpy(), chunk[y_col].to_numpy()
        model = sm.OLS(y, sm.add_constant(x)).fit()

        grid = np.linspace(x.min(), x.max(), 100)
        ax.scatter(x, y, color=GROUP_COLORS[group], alpha=0.55,
                   label=f"{group} (n={len(x)})")
        ax.plot(grid, model.params[0] + model.params[1] * grid,
                color=GROUP_COLORS[group],
                label=f"{group}: beta = {model.params[1]:.3f}")

    pooled = sm.OLS(data[y_col].to_numpy(),
                    sm.add_constant(data[x_col].to_numpy())).fit() # pooled ols (mco agrupado)
    
    grid = np.linspace(data[x_col].min(), data[x_col].max(), 100)
    ax.plot(grid, pooled.params[0] + pooled.params[1] * grid,
            color=GROUP_COLORS["All"], linestyle="--",
            label=f"Pooled: beta = {pooled.params[1]:.3f}")

    (speed, half_life) = implied_speed(pooled.params[1], horizon)
    note = (f"Pooled speed lambda = {speed:.3%}/yr, half-life = {half_life:.0f} yrs"
            if np.isfinite(speed) else "Pooled beta > 0: no convergence")

    ax.axhline(0, color="grey", linewidth=0.8, alpha=0.6)
    ax.set_title(f"Beta-convergence: {period_label}", fontsize=15, pad=12)
    ax.set_xlabel("Log GDP per capita, base year (constant 2015 US$)", fontsize=11)
    ax.set_ylabel("Annualised growth of GDP per capita (%)", fontsize=11)
    ax.annotate(note, xy=(0.02, 0.03), xycoords="axes fraction",
                fontsize=9, color="#333333")
    
    ax.legend(fontsize=9)
    ax.grid(alpha=0.3)
    fig.tight_layout()

    return save(fig, filename)


def plot_sigma_convergence(dispersion, filename):
    fig, ax = plt.subplots(figsize=(10, 6))

    for (group, chunk) in dispersion.groupby("group"):
        chunk = chunk.sort_values("year")
        ax.plot(chunk["year"], chunk["sd_log_gdp_pc"], marker="o", markersize=3,
                color=GROUP_COLORS.get(group), label=group)
        
    ax.set_title("Sigma-convergence: dispersion of log GDP per capita",
                 fontsize=15, pad=12)
    ax.set_xlabel("Year", fontsize=11)
    ax.set_ylabel("Standard deviation of log GDP per capita", fontsize=11)
    ax.legend(fontsize=9)
    ax.grid(alpha=0.3)
    fig.tight_layout()

    return save(fig, filename)


def plot_correlation_matrix(data, filename):
    columns = [c for c in data.columns if c.startswith(("growth_", "log_y0_"))]
    fig, ax = plt.subplots(figsize=(11, 9))

    sns.heatmap(data[columns].corr(), cmap="vlag", vmin=-1, vmax=1, center=0,
                annot=True, fmt=".2f", annot_kws={"size": 7}, square=True,
                cbar_kws={"shrink": 0.8}, ax=ax)

    ax.set_title("Correlation of period growth rates and initial income",
                 fontsize=14, pad=12)

    plt.setp(ax.get_xticklabels(), rotation=45, ha="right", fontsize=8)
    plt.setp(ax.get_yticklabels(), rotation=0, fontsize=8)
    fig.tight_layout()

    return save(fig, filename)
