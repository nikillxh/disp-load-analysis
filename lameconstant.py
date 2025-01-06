import sympy as sp
import numpy as np
import pandas as pd
from scipy.optimize import minimize
from sklearn.model_selection import train_test_split

def lame_constants(n, u_x, u_y):
    # Define symbols
    df = pd.read_csv(r'./data/'+str(n)+'/displacement_data.csv')
    rd = pd.read_csv(r'./data/'+str(n)+'/reaction_data.csv')

    x, y = sp.symbols('x y')
    lambda_lame, mu_lame = sp.symbols('lambda mu')

    u_x = eval(u_x)
    u_y = eval(u_y)

    # Compute first derivatives
    dux_dx = sp.diff(u_x, x)
    duy_dy = sp.diff(u_y, y)

    # Compute second derivatives
    d2ux_dx2 = sp.diff(u_x, x, 2)
    d2ux_dy2 = sp.diff(u_x, y, 2)
    d2uy_dx2 = sp.diff(u_y, x, 2)
    d2uy_dy2 = sp.diff(u_y, y, 2)
    d2ux_dxdy = sp.diff(u_x, x, y)
    d2uy_dxdy = sp.diff(u_y, x, y)

    # Laplacians of u_x and u_y
    laplacian_ux = d2ux_dx2 + d2ux_dy2
    laplacian_uy = d2uy_dy2 + d2uy_dx2

    # Residuals based on Navier's equation
    residual_ux = (lambda_lame + 2*mu_lame)*d2ux_dx2 + mu_lame*(d2ux_dy2) + (lambda_lame + mu_lame)*d2uy_dxdy
    residual_uy = (lambda_lame + 2*mu_lame)*d2uy_dy2 + mu_lame*(d2uy_dx2) + (lambda_lame + mu_lame)*d2ux_dxdy

    # Constraint equation for y = 0
    constraint_eq1 = lambda_lame * (dux_dx + duy_dy) + 2 * mu_lame * dux_dx + rd['Value'].values[0]
    constraint_eq2 = lambda_lame * (dux_dx + duy_dy) + 2 * mu_lame * dux_dx + rd['Value'].values[2]

    # Convert residuals and constraint to numerical functions
    residual_ux_func = sp.lambdify((x, y, lambda_lame, mu_lame), residual_ux)
    residual_uy_func = sp.lambdify((x, y, lambda_lame, mu_lame), residual_uy)
    constraint_func1 = sp.lambdify((x, y, lambda_lame, mu_lame), constraint_eq1)
    constraint_func2 = sp.lambdify((x, y, lambda_lame, mu_lame), constraint_eq2)

    # Function to calculate the total cost
    def calculate_cost(df, lambda_val, mu_val, penalty_scale=1e2): 
        total_cost = 0
        x_vals, y_vals = df['x'].values, df['y'].values

        # Compute residuals for u_x and u_y at all points
        res_ux_vals = residual_ux_func(x_vals, y_vals, lambda_val, mu_val)
        res_uy_vals = residual_uy_func(x_vals, y_vals, lambda_val, mu_val)

        # Add squared residuals to cost
        total_cost += np.sum(res_ux_vals**2 + res_uy_vals**2)

        # Compute constraint violations only when x = 1 and y = 1 respectively
        constraint1_violations = constraint_func1(x_vals[x_vals == 1], y_vals[x_vals == 1], lambda_val, mu_val)
        constraint2_violations = constraint_func2(x_vals[y_vals == 1], y_vals[y_vals == 1], lambda_val, mu_val)

        # Add penalties for constraint violations
        penalty_factor = 1e2 # Adjusted penalty scale
        total_cost += penalty_factor * (np.sum(np.abs(constraint1_violations)**2) + np.sum(np.abs(constraint2_violations)**2))
        return total_cost

    # Cost function wrapper for scipy optimizer
    def cost_function(params, df):
        lambda_val, mu_val = params
        return calculate_cost(df, lambda_val, mu_val)

    # Split data: 60% for training, 40% for testing
    df_train, df_test = train_test_split(df, test_size=0.4, random_state=42)

    # Initial guess for lambda and mu
    initial_guess = [1e10, 1e10]

    # Define bounds for lambda and mu (both are positive)
    bounds = [(1e8, 1e12), (1e8, 1e12)] # Ensures positivity

    # Optimize using Nelder-Mead method with bounds on the training data
    result = minimize(cost_function, initial_guess, args=(df_train,),
    method='Nelder-Mead', bounds=bounds)

    # Extract optimized values
    lambda_optimized, mu_optimized = result.x

    # Print optimized values
    print(f"Optimized Lamé's constants (Training Data):")
    print(f"Lambda (λ) = {lambda_optimized:.2e}")
    print(f"Mu (μ) = {mu_optimized:.2e}")

    # Evaluate the cost on the test set
    test_cost = calculate_cost(df_test, lambda_optimized, mu_optimized)
    print(f"Cost on Test Data: {test_cost:.2e}")

    return (lambda_optimized, mu_optimized)

if __name__ == "__main__":
    print("This file contains lame constants optimization")