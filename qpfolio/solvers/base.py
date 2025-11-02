from abc import ABC, abstractmethod
from typing import Protocol
from qpfolio.core.types import ProblemSpec, Solution


class Solver(ABC):
    @abstractmethod
    def solve(self, problem: ProblemSpec) -> Solution:
        """Solve a QP and return Solution."""
        raise NotImplementedError


class HasSolve(Protocol):
    def solve(self, problem: ProblemSpec) -> Solution: ...
