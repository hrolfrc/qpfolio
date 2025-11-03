import numpy as np
from qpfolio.personal_indexing import (
    personal_index_optimizer,
    personal_index_optimizer_esg,
)

def main():
    np.random.seed(2)
    n = 8
    R = np.random.randn(n, n)
    Sigma = 0.08 * np.eye(n) + 0.01 * (R + R.T) / 2.0
    w_bench = np.ones(n) / n

    # Baseline
    base = personal_index_optimizer(Sigma, w_bench, max_weight=0.5)

    # ESG: 1-row exposure tagging asset 0; target ~0 with penalty
    exposures = np.zeros((1, n))
    exposures[0, 0] = 1.0
    targets = np.zeros(1)
    penalties = np.array([10.0])

    esg = personal_index_optimizer_esg(
        Sigma,
        w_bench,
        exposures=exposures,
        targets=targets,
        penalties=penalties,
        max_weight=0.5,
    )

    print("Baseline w0:", round(float(base.x[0]), 6))
    print("ESG w0:", round(float(esg.x[0]), 6))
    print("Δ w0 (ESG - base):", round(float(esg.x[0] - base.x[0]), 6))

if __name__ == "__main__":
    main()
