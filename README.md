# Displacement-controlled Loading Analysis

## Report and 
[Report on Analysis of Stress Distribution](./REPORT.md)
[Problem Statement](./Problem_Statement.pdf)

## Overview
This project analyzes displacement-controlled loading of materials using data-driven approaches. The workflow involves three main steps:
1. **Polynomial Regression:** Generate polynomial equations for displacement components (`u_x` and `u_y`) using `polynomial.py`.
2. **Optimization:** Calculate Lamé constants (`λ` and `μ`) and minimize the cost function using `lameconstant.py`.
3. **Stress Visualization:** Plot stress variation (`σ_xx`, `σ_yy`, `σ_xy`) for the material using `distribution.py`.

## File Descriptions

1. `polynomial.py`
    - **Purpose:** Perform polynomial regression on displacement data to model `u_x` and `u_y`.
    - **Key Outputs:**
        - Polynomial equations for `u_x` and `u_y`.
        - Prediction vs. Actual plots for displacement components.


2. `lameconstant.py`
    - **Purpose:** Optimize Lamé constants (`λ` and `μ`) based on Navier’s equations and boundary constraints.
    - **Key Outputs:**
        - Optimized Lamé constants.
        - Cost function value for training and test datasets.

3. `distribution.py`
    - **Purpose:** Visualize stress variations (`σ_xx`, `σ_yy`, `σ_xy`) across the material.
    - **Key Outputs:**
        - Scatter plots for stress components at various points.

4. `main.py`
    - **Purpose:** Integrates the workflow for all five datasets in the `data/` directory.
    - **Steps:**
        1. Call `polynomial_obtain` to compute `u_x` and `u_y`.
        2. Optimize Lamé constants using `lame_constants`.
        3. Plot stress distributions for each dataset.


## How to Run

1. **Ensure Dependencies Are Installed:**
   ```bash
   pip install -r requirements.txt
    ```
2. **Place Data in the data/ Directory:**

    Each subfolder (e.g., 1, 2, ...) should contain:
    - displacement_data.csv
    - reaction_data.csv

3. **Run the Main Script:**
    ```bash
   python main.py
    ```

## Outputs

1. Polynomial Regression:
    - Equations for u_x and u_y.
    - Prediction vs. Actual plots.

2. Lamé Constants Optimization:
    - Optimized values of λ and μ.

3. Stress Distribution:
    - Scatter plots for σ_xx, σ_yy, and σ_xy.
