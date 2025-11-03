# tests/test_personal_indexing.py
import numpy as np

from qpfolio.personal_indexing import personal_index_optimizer, personal_index_optimizer_esg, personal_index_optimizer_taxaware


def _make_psd_cov(n: int, seed: int = 0) -> np.ndarray:
    rng = np.random.default_rng(seed)
    A = rng.normal(size=(n, n))
    Sigma = A @ A.T  # PSD
    # normalize to reasonable variances
    d = np.sqrt(np.diag(Sigma))
    Dinv = np.diag(1.0 / np.maximum(d, 1e-8))
    Sigma = Dinv @ Sigma @ Dinv
    # scale to ~[0.02, 0.10] variances
    return 0.06 * Sigma + 0.02 * np.eye(n)


def test_personal_index_basic_feasibility():
    n = 5
    Sigma = _make_psd_cov(n, seed=1)
    w_bench = np.ones(n) / n

    sol = personal_index_optimizer(Sigma, w_bench, max_weight=0.5)
    w = sol.x

    assert np.isfinite(w).all()
    assert np.isclose(w.sum(), 1.0, atol=5e-6)
    assert (w >= -1e-12).all()  # numerical slack
    assert (w <= 0.5 + 1e-12).all()


def test_personal_index_exclusions():
    n = 6
    Sigma = _make_psd_cov(n, seed=2)
    w_bench = np.ones(n) / n
    exclude = [1, 4]

    sol = personal_index_optimizer(Sigma, w_bench, max_weight=0.6, exclude=exclude)
    w = sol.x

    assert np.isclose(w.sum(), 1.0, atol=5e-6)
    assert np.isclose(w[1], 0.0, atol=5e-8)
    assert np.isclose(w[4], 0.0, atol=5e-8)
    assert (w >= -1e-12).all()
    assert (w <= 0.6 + 1e-12).all()


def test_esg_penalty_reduces_targeted_exposure():
    """
    Build a single-row exposure vector that tags asset 0 (e.g., 'energy').
    Set target exposure ~0 and apply a penalty; asset 0's weight should drop
    relative to the baseline tracking solution.
    """
    n = 8
    Sigma = _make_psd_cov(n, seed=3)
    w_bench = np.ones(n) / n

    # Baseline (no ESG penalty)
    base = personal_index_optimizer(Sigma, w_bench, max_weight=0.5)
    w_base = base.x

    # ESG exposure: emphasize reducing asset 0 exposure
    E = np.zeros((1, n))
    E[0, 0] = 1.0
    t = np.array([0.0])

    esg = personal_index_optimizer_esg(
        Sigma,
        w_bench,
        exposure_matrix=E,
        exposure_targets=t,
        exposure_penalty=5.0,  # reasonably strong penalty
        max_weight=0.5,
    )
    w_esg = esg.x

    # Feasibility
    assert np.isclose(w_esg.sum(), 1.0, atol=5e-6)
    assert (w_esg >= -1e-12).all()
    assert (w_esg <= 0.5 + 1e-12).all()

    # Exposure on asset 0 should drop vs baseline
    assert w_esg[0] <= w_base[0] + 1e-9  # allow tiny numerical slack
    # And the penalty shouldn't explode weights elsewhere
    assert np.all(np.isfinite(w_esg))


def test_taxaware_penalty_prefers_previous_weights():
    """
    With a high turnover penalty, the optimizer should stay closer to w_prev
    than the baseline tracking solution.
    """
    n = 7
    Sigma = _make_psd_cov(n, seed=4)
    w_bench = np.ones(n) / n

    # Previous portfolio: concentrated in asset 2
    w_prev = np.zeros(n)
    w_prev[2] = 1.0

    # Baseline (no turnover penalty)
    base = personal_index_optimizer(Sigma, w_bench, max_weight=0.7)
    w_base = base.x

    # Tax/turnover-aware (L2 penalty)
    tax_weights = np.linspace(1.0, 2.0, n)  # emphasize later assets slightly
    tax = personal_index_optimizer_taxaware(
        Sigma,
        w_bench,
        w_prev=w_prev,
        tax_weights=tax_weights,
        turnover_penalty=10.0,  # strong
        max_weight=0.7,
    )
    w_tax = tax.x

    # Feasibility
    assert np.isclose(w_tax.sum(), 1.0, atol=5e-6)
    assert (w_tax >= -1e-12).all()
    assert (w_tax <= 0.7 + 1e-12).all()

    # Should be closer to previous weights than the baseline solution
    dist_base = np.linalg.norm(w_base - w_prev)
    dist_tax = np.linalg.norm(w_tax - w_prev)
    assert dist_tax <= dist_base + 1e-9
