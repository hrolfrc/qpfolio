"""qpfolio: Quadratic programming portfolio optimization."""

from importlib.metadata import version, PackageNotFoundError

__all__ = ["__version__"]

try:
    __version__ = version("qpfolio")
except PackageNotFoundError:  # pragma: no cover
    __version__ = "0.1.7"
