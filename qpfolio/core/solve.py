from .types import ProblemSpec, Solution
from . import types
import numpy as np


def solve_qp(problem: ProblemSpec, solver: "Solver") -> Solution:
    """Dispatch to a concrete solver adapter."""
    return solver.solve(problem)


def assert_psd(matrix: np.ndarray, tol: float = 1e-10) -> None:
    """Basic PSD check with eigenvalue floor."""
    ev = np.linalg.eigvalsh(matrix)
    if ev.min() < -tol:
        raise ValueError("Matrix is not PSD within tolerance.")
