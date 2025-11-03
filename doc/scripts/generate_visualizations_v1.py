#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from dataclasses import asdict, dataclass
from datetime import datetime, UTC
from pathlib import Path

import matplotlib  # keep all imports at top; set backend before importing pyplot
import numpy as np
import pandas as pd

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

from qpfolio.simulation.gbm import simulate_prices_and_returns
from qpfolio.core.estimates import sample_mean_cov
from qpfolio.core.frontier import compute_frontier
from qpfolio.core.metrics import frontier_to_frame
from qpfolio.core.visualize import (
    plot_frontier_with_cml,
    plot_weights_along_frontier,
    plot_risk_contributions,
    plot_corr_heatmap,
)
from qpfolio.solvers.mathopt_osqp import MathOptOSQP


OUTDIR = Path("../_static/artifacts/v1")
# OUTDIR = Path("_static/artifacts/v1")

@dataclass(frozen=True)
class RunConfig:
    n_assets: int = 5
    mus: tuple[float, ...] = (0.08, 0.10, 0.11, 0.09, 0.12)   # annualized drifts (GBM)
    sigmas: tuple[float, ...] = (0.20, 0.25, 0.22, 0.18, 0.28) # annualized vols (GBM)
    T: float = 1.0
    steps_per_year: int = 252
    s0: float = 100.0
    rf: float = 0.02  # risk-free rate for CML


def _ensure_outdir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def _targets_from_mu(mu_annual: np.ndarray, k: int = 15) -> np.ndarray:
    # A simple, robust range around the empirical mean range
    lo = float(mu_annual.min() * 0.9)
    hi = float(mu_annual.max() * 1.05)
    if np.isclose(lo, hi):
        hi = lo + 1e-3
    return np.linspace(lo, hi, k)


def _plot_prices_and_returns(prices: pd.DataFrame, log_ret: pd.DataFrame, outdir: Path) -> None:
    fig, ax = plt.subplots(figsize=(8, 5))
    prices.plot(ax=ax, legend=False)
    ax.set_title("GBM Price Paths")
    ax.set_xlabel("Time (years)")
    ax.set_ylabel("Price")
    ax.grid(True, alpha=0.3)
    fig.tight_layout()
    fig.savefig(outdir / "gbm_prices.png", dpi=144)
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(8, 5))
    (log_ret * 252).plot(ax=ax, legend=False)  # annualized log-returns for visual scale
    ax.set_title("GBM Log Returns (Annualized)")
    ax.set_xlabel("Time (years)")
    ax.set_ylabel("Log Return")
    ax.grid(True, alpha=0.3)
    fig.tight_layout()
    fig.savefig(outdir / "gbm_returns.png", dpi=144)
    plt.close(fig)


def _plot_mvo_suite(points, df_frontier: pd.DataFrame, Sigma: np.ndarray, labels: list[str], rf: float, outdir: Path) -> None:
    # Frontier + CML
    fig, ax = plt.subplots(figsize=(7, 5))
    plot_frontier_with_cml(points, rf=rf, ax=ax)
    fig.tight_layout()
    fig.savefig(outdir / "mvo_frontier.png", dpi=144)
    plt.close(fig)

    # Weights along frontier (stacked area)
    fig, ax = plt.subplots(figsize=(8, 5))
    w_cols = [c for c in df_frontier.columns if c.startswith("w_")]
    plot_weights_along_frontier(df_frontier[w_cols], labels=labels, ax=ax)
    fig.tight_layout()
    fig.savefig(outdir / "mvo_weights.png", dpi=144)
    plt.close(fig)

    # Risk contributions at mid frontier point
    mid = len(df_frontier) // 2
    w_mid = df_frontier.loc[df_frontier.index[mid], w_cols].to_numpy()
    fig, ax = plt.subplots(figsize=(7, 4))
    plot_risk_contributions(w_mid, Sigma, labels=labels, ax=ax)
    fig.tight_layout()
    fig.savefig(outdir / "mvo_risk.png", dpi=144)
    plt.close(fig)

    # Correlation heatmap from Sigma
    fig, ax = plt.subplots(figsize=(5.5, 5))
    plot_corr_heatmap(Sigma, labels=labels, ax=ax)
    fig.tight_layout()
    fig.savefig(outdir / "corr.png", dpi=144)
    plt.close(fig)


def _save_frontier_csv(df_frontier: pd.DataFrame, outdir: Path) -> None:
    df_frontier.to_csv(outdir / "frontier.csv", index=True)


def _save_metadata(cfg: RunConfig, seed: int, mu: np.ndarray, Sigma: np.ndarray, outdir: Path) -> None:
    meta = {
        "generated_at_utc": datetime.now(UTC).isoformat(timespec="seconds"),
        "seed": seed,
        "config": asdict(cfg),
        "mu_annual": mu.tolist(),
        "Sigma_annual": Sigma.tolist(),
        "artifacts": [
            "mvo_frontier.png",
            "mvo_weights.png",
            "mvo_risk.png",
            "corr.png",
            "gbm_prices.png",
            "gbm_returns.png",
            "frontier.csv",
        ],
        "notes": "Artifacts generated with OSQP-backed MVO on GBM-derived returns.",
    }
    with open(outdir / "metadata.json", "w", encoding="utf-8") as f:
        json.dump(meta, f, indent=2)


def generate(cfg: RunConfig, seed: int) -> None:
    _ensure_outdir(OUTDIR)

    # 1) Simulate GBM prices -> log returns
    prices, log_ret = simulate_prices_and_returns(
        mus=np.array(cfg.mus, dtype=float),
        sigmas=np.array(cfg.sigmas, dtype=float),
        T=cfg.T,
        steps_per_year=cfg.steps_per_year,
        s0=np.full(len(cfg.mus), cfg.s0, dtype=float),
        seed=seed,
    )
    # Visuals for GBM itself
    _plot_prices_and_returns(prices, log_ret, OUTDIR)

    # 2) Estimate annualized mu, Sigma from simulated returns
    mu_hat, Sigma_hat = sample_mean_cov(log_ret.values, freq=cfg.steps_per_year)  # returns annualized estimates

    # 3) Build MVO frontier with OSQP
    targets = _targets_from_mu(mu_hat, k=15)
    solver = MathOptOSQP()
    points = compute_frontier(mu_hat, Sigma_hat, targets, solver=solver)

    # 4) Tabular frontier + weights
    labels = [f"A{i+1}" for i in range(len(mu_hat))]
    df_frontier = frontier_to_frame(points, asset_labels=labels)
    _save_frontier_csv(df_frontier, OUTDIR)

    # 5) Visual suite (frontier, weights, risk contrib, corr heatmap)
    _plot_mvo_suite(points, df_frontier, Sigma_hat, labels, rf=cfg.rf, outdir=OUTDIR)

    # 6) Metadata
    _save_metadata(cfg, seed, mu_hat, Sigma_hat, OUTDIR)


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Generate v1 visualization artifacts for qpfolio docs.")
    p.add_argument("--seed", type=int, default=42, help="RNG seed for reproducibility")
    return p.parse_args()


def main() -> None:
    args = parse_args()
    cfg = RunConfig()
    generate(cfg, seed=args.seed)


if __name__ == "__main__":
    main()
