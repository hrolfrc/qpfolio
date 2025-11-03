# tests/unit/test_plumbing_triplet_roundtrip.py
import numpy as np
import pytest

osqp = pytest.importorskip("osqp", reason="OSQP not installed; skipping triplet roundtrip test.")

from qpfolio.core.types import ProblemSpec
from qpfolio.solvers.mathopt_osqp import MathOptOSQP


def test_spec_triplet_roundtrip_solve_simple():
    # Min 0.5 x^T I x  s.t. sum(x)=1, x >= 0
    n = 3
    Q = np.eye(n)
    c = np.zeros(n)

    # Equality: sum(x) = 1  -> 1 <= [1 1 1] x <= 1
    Aeq = np.ones((1, n))
    l = np.array([1.0])
    u = np.array([1.0])

    # Bounds: x_i in [0, +inf)
    bounds = [(0.0, None)] * n

    spec = ProblemSpec(Q=Q, c=c, A=Aeq, l=l, u=u, bounds=bounds)
    sol = MathOptOSQP(verbose=False).solve(spec)

    assert sol.status.startswith("solv") or sol.status.startswith("opt")
    # Symmetry suggests x ~ [1/3, 1/3, 1/3]
    np.testing.assert_allclose(sol.x.sum(), 1.0, rtol=1e-6, atol=1e-6)
    np.testing.assert_allclose(sol.x, np.ones(n) / n, rtol=1e-3, atol=1e-3)
