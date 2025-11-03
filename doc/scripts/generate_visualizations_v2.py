#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from dataclasses import asdict, dataclass
from datetime import datetime, UTC
from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

from qpfolio.simulation.gbm import simulate_prices_and_returns
from qpfolio.core.estimates import sample_mean_cov
from qpfolio.core.frontier import compute_frontier
from qpfolio.core.metrics import frontier_to_frame
from qpfolio.core.visualize import (
    plot_frontier,
    plot_frontier_with_cml,
    plot_weights_along_frontier,
    plot_risk_contributions,
    plot_corr_heatmap,
)
from qpfolio.solvers.mathopt_osqp import MathOptOSQP


OUTDIR = Path("../_static/artifacts/v2")



@dataclass(frozen=True)
class RunConfig:
    n_assets: int = 5
    mus: tuple[float, ...] = (0.08, 0.10, 0.11, 0.09, 0.12)   # annual drifts for GBM
    sigmas: tuple[float, ...] = (0.20, 0.25, 0.22, 0.18, 0.28) # annual vols for GBM
    T: float = 1.0
    steps_per_year: int = 252
    s0: float = 100.0
    rf: float = 0.02  # risk-free rate for CML


def _ensure_outdir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def _targets_from_mu(mu_annual: np.ndarray, k: int = 21) -> np.ndarray:
    lo = float(mu_annual.min() * 0.9)
    hi = float(mu_annual.max() * 1.05)
    if np.isclose(lo, hi):
        hi = lo + 1e-3
    return np.linspace(lo, hi, k)


def _compute_mdp_point(Sigma: np.ndarray, mu: np.ndarray) -> dict:
    """
    Closed-form Most Diversified Portfolio (long-only ignored in closed form):
    w* ∝ Σ^{-1} σ, then rescale to sum to 1.
    """
    # vol vector
    sigma = np.sqrt(np.clip(np.diag(Sigma), 1e-12, None))
    # pseudo-inverse for stability
    Sinv = np.linalg.pinv(Sigma)
    raw = Sinv @ sigma
    raw = np.clip(raw, 0.0, None)  # enforce nonnegativity softly
    if raw.sum() <= 0:
        # fallback: equal weights
        w = np.full_like(raw, 1.0 / raw.size)
    else:
        w = raw / raw.sum()
    risk = float(np.sqrt(max(w @ Sigma @ w, 0.0)))
    ret = float(w @ mu)
    return {"w": w, "risk": risk, "ret": ret}


def _plot_comparison(mvo_pts, dro_pts, mdp_point: dict, outdir: Path) -> None:
    fig, ax = plt.subplots(figsize=(7.5, 5.5))
    # MVO frontier
    risks_mvo = [p[0] for p in mvo_pts]
    rets_mvo = [p[1] for p in mvo_pts]
    ax.plot(risks_mvo, rets_mvo, marker="o", linewidth=1.5, label="MVO")

    # DRO frontier
    risks_dro = [p[0] for p in dro_pts]
    rets_dro = [p[1] for p in dro_pts]
    ax.plot(risks_dro, rets_dro, marker="o", linewidth=1.5, label="DRO (Σ+γI)")

    # MDP point
    ax.scatter([mdp_point["risk"]], [mdp_point["ret"]], marker="D", s=70, label="MDP (point)")

    ax.set_xlabel("Risk (stdev)")
    ax.set_ylabel("Expected Return")
    ax.set_title("Method Comparison: MVO vs DRO Frontier + MDP Point")
    ax.grid(True, alpha=0.3)
    ax.legend(loc="best")
    fig.tight_layout()
    fig.savefig(outdir / "comparison_frontiers.png", dpi=150)
    plt.close(fig)


def _save_metadata(cfg: RunConfig, seed: int, mu: np.ndarray, Sigma: np.ndarray, gamma: float, outdir: Path) -> None:
    meta = {
        "generated_at_utc": datetime.now(UTC).isoformat(timespec="seconds"),
        "seed": seed,
        "config": asdict(cfg),
        "gamma": gamma,
        "mu_annual": mu.tolist(),
        "Sigma_annual": Sigma.tolist(),
        "artifacts": sorted([p.name for p in outdir.glob("*.*")]),
        "notes": "v2: compares MVO and DRO frontiers; MDP shown as single point (closed-form).",
    }
    with open(outdir / "metadata.json", "w", encoding="utf-8") as f:
        json.dump(meta, f, indent=2)


def generate(cfg: RunConfig, seed: int, gamma: float) -> None:
    _ensure_outdir(OUTDIR)

    # 1) Simulate GBM → returns
    prices, log_ret = simulate_prices_and_returns(
        mus=np.array(cfg.mus, dtype=float),
        sigmas=np.array(cfg.sigmas, dtype=float),
        T=cfg.T,
        steps_per_year=cfg.steps_per_year,
        s0=np.full(len(cfg.mus), cfg.s0, dtype=float),
        seed=seed,
    )

    # 2) Estimates (annualized) for optimization
    mu_hat, Sigma_hat = sample_mean_cov(log_ret.values, freq=cfg.steps_per_year)

    # 3) Frontiers
    targets = _targets_from_mu(mu_hat, k=21)
    solver = MathOptOSQP()

    # MVO
    mvo_pts = compute_frontier(mu_hat, Sigma_hat, targets, solver=solver)
    df_mvo = frontier_to_frame(mvo_pts, asset_labels=[f"A{i+1}" for i in range(len(mu_hat))])
    df_mvo.to_csv(OUTDIR / "mvo_frontier.csv", index=True)

    # DRO: Σ' = Σ + γ I
    Sigma_dro = Sigma_hat + gamma * np.eye(Sigma_hat.shape[0], dtype=float)
    dro_pts = compute_frontier(mu_hat, Sigma_dro, targets, solver=solver)
    df_dro = frontier_to_frame(dro_pts, asset_labels=[f"A{i+1}" for i in range(len(mu_hat))])
    df_dro.to_csv(OUTDIR / "dro_frontier.csv", index=True)

    # 4) Visuals per method
    # MVO suite
    fig, ax = plt.subplots(figsize=(7, 5))
    plot_frontier_with_cml(mvo_pts, rf=cfg.rf, ax=ax)
    fig.tight_layout(); fig.savefig(OUTDIR / "mvo_frontier.png", dpi=150); plt.close(fig)

    fig, ax = plt.subplots(figsize=(8, 5))
    w_cols = [c for c in df_mvo.columns if c.startswith("w_")]
    plot_weights_along_frontier(df_mvo[w_cols], labels=list(df_mvo[w_cols].columns), ax=ax)
    fig.tight_layout(); fig.savefig(OUTDIR / "mvo_weights.png", dpi=150); plt.close(fig)

    mid = len(df_mvo) // 2
    w_mid = df_mvo.loc[df_mvo.index[mid], w_cols].to_numpy()
    fig, ax = plt.subplots(figsize=(7, 4))
    plot_risk_contributions(w_mid, Sigma_hat, labels=list(df_mvo[w_cols].columns), ax=ax)
    fig.tight_layout(); fig.savefig(OUTDIR / "mvo_risk.png", dpi=150); plt.close(fig)

    # Correlation heatmap (from Σ)
    fig, ax = plt.subplots(figsize=(5.5, 5))
    plot_corr_heatmap(Sigma_hat, labels=[f"A{i+1}" for i in range(len(mu_hat))], ax=ax)
    fig.tight_layout(); fig.savefig(OUTDIR / "corr.png", dpi=150); plt.close(fig)

    # DRO: show frontier only (weights/RC optional)
    fig, ax = plt.subplots(figsize=(7, 5))
    plot_frontier(dro_pts, ax=ax)
    ax.set_title("DRO Efficient Frontier (Σ + γI)")
    fig.tight_layout(); fig.savefig(OUTDIR / "dro_frontier.png", dpi=150); plt.close(fig)

    # 5) MDP point (closed-form)
    mdp = _compute_mdp_point(Sigma_hat, mu_hat)
    # also render it alone for clarity
    fig, ax = plt.subplots(figsize=(5.5, 4.2))
    ax.scatter([mdp["risk"]], [mdp["ret"]], marker="D", s=70)
    ax.set_xlabel("Risk (stdev)"); ax.set_ylabel("Expected Return")
    ax.set_title("MDP (closed-form point)")
    ax.grid(True, alpha=0.3)
    fig.tight_layout(); fig.savefig(OUTDIR / "mdp_point.png", dpi=150); plt.close(fig)

    # 6) Combined comparison
    _plot_comparison(mvo_pts, dro_pts, mdp, OUTDIR)

    # 7) Save metadata
    _save_metadata(cfg, seed, mu_hat, Sigma_hat, gamma, OUTDIR)


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Generate v2 comparison artifacts (MVO, DRO, MDP) for qpfolio docs.")
    p.add_argument("--seed", type=int, default=42, help="RNG seed for reproducibility")
    p.add_argument("--gamma", type=float, default=0.15, help="DRO inflation parameter (Σ' = Σ + γ I)")
    return p.parse_args()


def main() -> None:
    args = parse_args()
    cfg = RunConfig()
    generate(cfg, seed=args.seed, gamma=args.gamma)


if __name__ == "__main__":
    main()
