import polynomial as pf
import lameconstant as lc
import distribution as dt

lambda_mu = []
lst = []

for n in range(1, 6, 1):
    print('\nn = ', n)
    (u_x, u_y) = pf.polynomial_obtain(n)
    (lambda_val, mu_val) = lc.lame_constants(n, u_x, u_y)
    lambda_mu.append((1, float(lambda_val), float(mu_val)))
    lst.append((n, u_x, u_y))

print(lambda_mu, "\nSimilar Values")
[dt.distribution_plot(n, u_x, u_y, lambda_val, mu_val) for (n, u_x, u_y) in lst]
