import numpy as np
from .types import ProblemSpec


def build_mvo_problem(mu: np.ndarray, Sigma: np.ndarray, r_target: float, long_only: bool = True) -> ProblemSpec:
    """Min-variance subject to target return and full investment."""
    n = Sigma.shape[0]
    Q = Sigma.copy()
    c = np.zeros(n)

    # Equality: sum w = 1
    A_eq = np.ones((1, n))
    b_eq = np.array([1.0])

    # Inequalities: -mu^T w <= -r_target  (i.e., mu^T w >= r_target)
    A_ineq = -mu.reshape(1, -1)
    b_ineq = np.array([-r_target])

    bounds = [(0.0, 1.0) if long_only else (-1.0, 1.0) for _ in range(n)]
    return ProblemSpec(Q=Q, c=c, A_eq=A_eq, b_eq=b_eq, A_ineq=A_ineq, b_ineq=b_ineq, bounds=bounds)


def build_mdp_problem(sigmas: np.ndarray, Sigma: np.ndarray, long_only: bool = True) -> ProblemSpec:
    """MDP via variance-min with normalization w^T sigma = 1."""
    n = Sigma.shape[0]
    Q = Sigma.copy()
    c = np.zeros(n)

    A_eq = sigmas.reshape(1, -1)
    b_eq = np.array([1.0])

    A_ineq = None
    b_ineq = None

    bounds = [(0.0, 1.0) if long_only else (-1.0, 1.0) for _ in range(n)]
    return ProblemSpec(Q=Q, c=c, A_eq=A_eq, b_eq=b_eq, A_ineq=A_ineq, b_ineq=b_ineq, bounds=bounds)


def build_dro_lite_problem(mu: np.ndarray, Sigma: np.ndarray, r_target: float, gamma: float = 0.0,
                           long_only: bool = True) -> ProblemSpec:
    """Moment-robust MVO: inflate covariance by gamma*diag(Sigma)."""
    Sigma_robust = Sigma + gamma * np.diag(np.diag(Sigma))
    return build_mvo_problem(mu, Sigma_robust, r_target, long_only=long_only)
