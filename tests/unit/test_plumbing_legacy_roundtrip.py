# tests/unit/test_plumbing_legacy_roundtrip.py
import numpy as np
import pytest

osqp = pytest.importorskip("osqp", reason="OSQP not installed; skipping legacy roundtrip test.")

from qpfolio.core.types import ProblemSpec
from qpfolio.solvers.mathopt_osqp import MathOptOSQP

def test_spec_legacy_roundtrip_solve_simple():
    # Min 0.5 x^T I x + (-e1)^T x  (i.e., linear tilt toward asset 0)
    # s.t. sum(x)=1, x >= 0
    n = 4
    Q = np.eye(n)
    c = np.zeros(n)
    c[0] = -1.0  # encourage x0 to be larger

    # Equality: sum(x) = 1
    A_eq = np.ones((1, n))
    b_eq = np.array([1.0])

    # No explicit A_ineq; rely on bounds only
    bounds = [(0.0, None)] * n

    spec = ProblemSpec(Q=Q, c=c, A_eq=A_eq, b_eq=b_eq, bounds=bounds)
    sol = MathOptOSQP(verbose=False).solve(spec)

    assert sol.status.startswith("solv") or sol.status.startswith("opt")
    np.testing.assert_allclose(sol.x.sum(), 1.0, rtol=1e-6, atol=1e-6)
    # With the linear tilt, x0 should be dominant (but not necessarily 1.0 due to quadratic)
    assert sol.x[0] >= max(sol.x[1:])
