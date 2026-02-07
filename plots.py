import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

def plot_beta_convergence(
    data, 
    x_col, 
    y_col, 
    x_label, 
    y_label, 
    title
):

    plt.figure(figsize=(10, 6))
    colors = {'Emerging': 'blue', 'Developed': 'orange'}
    groups = ['Emerging', 'Developed']

    for group in groups:
        sett = data[data['Group'] == group]
        X = sett[[x_col]]
        y = sett[y_col]

        model = LinearRegression(
            fit_intercept=True,
        ).fit(X, y)

        plt.scatter(X, y, label=f'{group} data', color=colors[group], alpha=0.5)
        plt.plot(X, model.predict(X), linestyle='-', color=colors[group], 
                 label=f'{group} (β = {model.coef_[0]:.2f})')

    plt.title(title, fontsize=16, pad=15)
    plt.xlabel(x_label, fontsize=12)
    plt.ylabel(y_label, fontsize=12)
    plt.legend()
    plt.grid(alpha=0.4)
    plt.tight_layout()
    plt.show()
