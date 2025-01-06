import sympy as sp
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def distribution_plot(n, u_x, u_y, lambda_val, mu_val):
    # Load the data from CSV
    df = pd.read_csv(r'./data/'+str(n)+'/displacement_data.csv')

    # Extract x and y coordinates from the dataframe
    x_points = df['x'].values
    y_points = df['y'].values

    # Define symbols
    x, y = sp.symbols('x y')
    lambda_lame, mu_lame = sp.symbols('lambda mu')

    u_x = eval(u_x)
    u_y = eval(u_y)

    # Compute first derivatives
    dux_dx = sp.diff(u_x, x)
    duy_dy = sp.diff(u_y, y)
    dux_dy = sp.diff(u_x, y)
    duy_dx = sp.diff(u_y, x)

    # Define stress components
    sigma_xx = lambda_lame * (dux_dx + duy_dy) + 2 * mu_lame * dux_dx
    sigma_yy = lambda_lame * (dux_dx + duy_dy) + 2 * mu_lame * duy_dy
    sigma_xy = mu_lame * (dux_dy + duy_dx)

    # Lambdify the expressions for faster evaluation
    sigma_xx_func = sp.lambdify((x, y, lambda_lame, mu_lame), sigma_xx, modules="numpy")
    sigma_yy_func = sp.lambdify((x, y, lambda_lame, mu_lame), sigma_yy, modules="numpy")
    sigma_xy_func = sp.lambdify((x, y, lambda_lame, mu_lame), sigma_xy, modules="numpy")

    # Evaluate the stress components for each point in the dataset
    sigma_xx_values = sigma_xx_func(x_points, y_points, lambda_val, mu_val)
    sigma_yy_values = sigma_yy_func(x_points, y_points, lambda_val, mu_val)
    sigma_xy_values = sigma_xy_func(x_points, y_points, lambda_val, mu_val)

    # Create scatter plots for the stress components
    fig, axes = plt.subplots(1, 3, figsize=(18, 6))

    # Scatter plot for sigma_xx
    scatter1 = axes[0].scatter(x_points, y_points, c=sigma_xx_values, cmap='twilight', s=10)
    axes[0].set_title(r'$\sigma_{xx}$ (Variation of $\sigma_{xx}$)'+ ", n = " + str(n))
    axes[0].set_xlabel('x')
    axes[0].set_ylabel('y')
    cbar = fig.colorbar(scatter1, ax=axes[0])
    scatter1.set_clim(0, 9 * 1e6)

    # Scatter plot for sigma_yy
    scatter2 = axes[1].scatter(x_points, y_points, c=sigma_yy_values, cmap='twilight', s=10)
    axes[1].set_title(r'$\sigma_{yy}$ (Variation of $\sigma_{yy}$)'+ ", n = " + str(n))
    axes[1].set_xlabel('x')
    axes[1].set_ylabel('y')
    cbar = fig.colorbar(scatter2, ax=axes[1])
    scatter2.set_clim(0, 9 * 1e6)

    # Scatter plot for sigma_xy
    scatter3 = axes[2].scatter(x_points, y_points, c=sigma_xy_values, cmap='twilight', s=10)
    axes[2].set_title(r'$\sigma_{xy}$ (Variation of $\sigma_{xy}$)'+ ", n = " + str(n))
    axes[2].set_xlabel('x')
    axes[2].set_ylabel('y')
    cbar = fig.colorbar(scatter3, ax=axes[2])
    scatter3.set_clim(0, 3.6 * 1e4)

    # Display the plots
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    print("This file plots distribution")