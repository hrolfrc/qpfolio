import numpy as np
from qpfolio.personal_indexing import personal_index_optimizer

def main():
    np.random.seed(1)
    n = 5
    # Simple PSD-ish covariance: diagonal + small random symmetric
    R = np.random.randn(n, n)
    Sigma = 0.08 * np.eye(n) + 0.01 * (R + R.T) / 2.0
    w_bench = np.ones(n) / n

    sol = personal_index_optimizer(Sigma, w_bench, max_weight=0.5)
    print("Status:", sol.status)
    print("Objective:", round(float(sol.obj), 8))
    print("Weights:", np.round(sol.x, 6))
    print("Sum:", sol.x.sum())

if __name__ == "__main__":
    main()
