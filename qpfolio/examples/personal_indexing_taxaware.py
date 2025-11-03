import numpy as np
from qpfolio.personal_indexing import personal_index_optimizer, personal_index_optimizer_taxaware

def main():
    np.random.seed(3)
    n = 7
    R = np.random.randn(n, n)
    Sigma = 0.08 * np.eye(n) + 0.01 * (R + R.T) / 2.0
    w_bench = np.ones(n) / n

    w_prev = np.zeros(n)
    w_prev[2] = 1.0
    tax_weights = np.linspace(1.0, 2.0, n)

    base = personal_index_optimizer(Sigma, w_bench, max_weight=0.7)
    tax = personal_index_optimizer_taxaware(
        Sigma, w_bench,
        w_prev=w_prev,
        tax_weights=tax_weights,
        turnover_penalty=10.0,
        max_weight=0.7,
    )

    print("Baseline weights:", np.round(base.x, 6))
    print("Tax-aware weights:", np.round(tax.x, 6))
    print("||tax - prev||:", np.linalg.norm(tax.x - w_prev))
    print("||base - prev||:", np.linalg.norm(base.x - w_prev))

if __name__ == "__main__":
    main()
