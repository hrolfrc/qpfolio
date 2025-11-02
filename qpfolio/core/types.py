from dataclasses import dataclass
from typing import Optional, Tuple, Sequence
import numpy as np

ArrayLike = np.ndarray

@dataclass
class ProblemSpec:
    Q: ArrayLike                      # (n,n) PSD
    c: Optional[ArrayLike] = None     # (n,)
    A_eq: Optional[ArrayLike] = None  # (m_eq,n)
    b_eq: Optional[ArrayLike] = None  # (m_eq,)
    A_ineq: Optional[ArrayLike] = None  # (m_ineq,n)
    b_ineq: Optional[ArrayLike] = None  # (m_ineq,)
    bounds: Optional[Sequence[Tuple[float, float]]] = None  # per-variable (lo, hi)

@dataclass
class Solution:
    x: ArrayLike
    obj_value: float
    status: str
    info: dict
