import sympy as sp
import numpy as np
import pandas as pd
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt

def polynomial_obtain(n) :
    # Load the CSV file
    dfn = pd.read_csv(r'./data/'+str(n)+'/displacement_data.csv')

    # Load the dataset
    x = dfn['x'].values
    y = dfn['y'].values
    u_x = dfn['u_x'].values
    u_y = dfn['u_y'].values

    # Split the dataset into 60% training and 40% testing
    X = np.column_stack((x, y))
    X_train, X_test, u_x_train, u_x_test, u_y_train, u_y_test = train_test_split(X, u_x, u_y, test_size=0.4, random_state=42)

    # Prepare polynomial features (degree 3 for simplicity)
    poly = PolynomialFeatures(degree=3)
    X_train_poly = poly.fit_transform(X_train)
    X_test_poly = poly.transform(X_test)

    # Fit the polynomial regression model for u_y
    model_y = LinearRegression()
    model_y.fit(X_train_poly, u_y_train)

    # Fit the polynomial regression model for u_x
    model_x = LinearRegression()
    model_x.fit(X_train_poly, u_x_train)

    # Make predictions on the test set
    u_y_pred = model_y.predict(X_test_poly)
    u_x_pred = model_x.predict(X_test_poly)

    # Evaluate the models
    mse_y = mean_squared_error(u_y_test, u_y_pred)
    r2_y = r2_score(u_y_test, u_y_pred)
    mse_x = mean_squared_error(u_x_test, u_x_pred)
    r2_x = r2_score(u_x_test, u_x_pred)
    print(f"u_y - Mean Squared Error (MSE): {mse_y:.5e}, R-squared (R2 Score): {r2_y:.5f}")
    print(f"u_x - Mean Squared Error (MSE): {mse_x:.5e}, R-squared (R2 Score): {r2_x:.5f}")

    # Plot the predictions vs actual values for u_y
    plt.figure(figsize=(10, 6))
    plt.scatter(range(len(u_y_test)), u_y_test, color='blue',
    label='Actual u_y', alpha=0.6)
    plt.scatter(range(len(u_y_pred)), u_y_pred, color='red',
    label='Predicted u_y', alpha=0.6)
    plt.title("Comparison of Actual and Predicted Values for u_y" + ", n = " + str(n))
    plt.xlabel("Sample Index")
    plt.ylabel("u_y")
    plt.legend()
    plt.show()

    # Plot the predictions vs actual values for u_x
    plt.figure(figsize=(10, 6))
    plt.scatter(range(len(u_x_test)), u_x_test, color='green', label='Actual u_x', alpha=0.6)
    plt.scatter(range(len(u_x_pred)), u_x_pred, color='orange', label='Predicted u_x', alpha=0.6)

    plt.title("Comparison of Actual and Predicted Values for u_x" + ", n = " + str(n))
    plt.xlabel("Sample Index")
    plt.ylabel("u_x")
    plt.legend()
    plt.show()

    # Display the polynomial equations
    # For u_y
    coefficients_y = model_y.coef_
    intercept_y = model_y.intercept_
    features = poly.get_feature_names_out(input_features=['x', 'y'])
    equation_y = f"{intercept_y:.5f}"
    for coef, feature in zip(coefficients_y, features):
        equation_y += f" + ({coef:.5e})*{feature}"
    print("\nPolynomial Equation for u_y:")
    print(f"u_y = {equation_y}")

    # For u_x
    coefficients_x = model_x.coef_
    intercept_x = model_x.intercept_
    equation_x = f"{intercept_x:.5f}"
    for coef, feature in zip(coefficients_x, features):
        equation_x += f" + ({coef:.5e})*{feature}"
    print("\nPolynomial Equation for u_x:")
    print(f"u_x = {equation_x}")

    equation_x = equation_x.replace("^", "**").replace("x y", "x * y").replace("x**2 y", "x**2 * y").replace("x y**2", "x * y**2")
    equation_y = equation_y.replace("^", "**").replace("x y", "x * y").replace("x**2 y", "x**2 * y").replace("x y**2", "x * y**2")
    return (equation_x, equation_y)

if __name__ == "__main__":
    print("This file contains polynomial regression function")