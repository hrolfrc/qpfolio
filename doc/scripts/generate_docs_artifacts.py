#!/usr/bin/env python3
"""
Generate documentation artifacts (plots + CSV) with REAL qpfolio runs.
- Uses qpfolio core + solver adapter (MathOpt+OSQP) for genuine optimization.
- Deterministic by seed.
- Saves provenance to metadata.json.
"""
from __future__ import annotations

import json
from datetime import datetime, UTC
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

from qpfolio.core.data import simulate_mvn_returns
from qpfolio.core.estimates import sample_mean_cov
from qpfolio.core.frontier import compute_frontier
from qpfolio.core.metrics import frontier_to_frame
from qpfolio.core.metrics import risk_contributions
from qpfolio.solvers.mathopt_osqp import MathOptOSQP  # ensure this is the real adapter

OUTDIR = Path("_static/artifacts/v0")


def main():
    OUTDIR.mkdir(parents=True, exist_ok=True)

    # ---- Parameters (documented in metadata)
    n_assets = 6
    n_days = 252
    seed = 42
    targets = np.linspace(0.06, 0.14, 9).tolist()
    asset_labels = [f"A{i + 1}" for i in range(n_assets)]

    # ---- Simulate -> estimate
    R, mu, Sigma = simulate_mvn_returns(n_assets=n_assets, n_periods=n_days, seed=seed)
    mu_est, Sigma_est = sample_mean_cov(R)

    # ---- Solve frontier (REAL solve via MathOpt+OSQP)
    solver = MathOptOSQP()
    points = compute_frontier(mu_est, Sigma_est, targets, solver=solver)

    # ---- Frontier frame (for CSV & stacked weights)
    df = frontier_to_frame(points, asset_labels=asset_labels)
    df.to_csv(OUTDIR / "frontier.csv", index=True)

    # ---- Plot: frontier
    fig, ax = plt.subplots()
    xs = [p[0] for p in points]
    ys = [p[1] for p in points]
    ax.plot(xs, ys, marker="o", linewidth=1.5)
    ax.set_xlabel("Risk (stdev)")
    ax.set_ylabel("Expected Return")
    ax.set_title("Efficient Frontier")
    ax.grid(True)
    fig.tight_layout()
    fig.savefig(OUTDIR / "frontier.png", dpi=150)
    plt.close(fig)

    # ---- Plot: weights along frontier (stacked area)
    weight_cols = [c for c in df.columns if c.startswith("w_")]
    W = df[weight_cols].to_numpy()  # shape (k, n)
    x = np.arange(W.shape[0])
    fig, ax = plt.subplots()
    ax.stackplot(x, W.T, labels=[c[2:] for c in weight_cols])  # strip "w_"
    ax.set_xlabel("Frontier Index")
    ax.set_ylabel("Weight")
    ax.set_ylim(0.0, 1.0)
    ax.set_title("Weights Along the Frontier")
    ax.legend(loc="upper right", ncols=3)
    fig.tight_layout()
    fig.savefig(OUTDIR / "weights.png", dpi=150)
    plt.close(fig)

    # ---- Plot: risk contributions for the mid frontier point
    mid = len(points) // 2
    w_mid = points[mid][2].x
    rc = risk_contributions(w_mid, Sigma_est)
    frac = rc["trc_frac"]
    fig, ax = plt.subplots()
    ax.bar(np.arange(n_assets), frac)
    ax.set_xticks(np.arange(n_assets), asset_labels, rotation=0)
    ax.set_ylabel("Risk Contribution (fraction of σ)")
    ax.set_title("Total Risk Contributions (mid frontier)")
    ax.grid(True, axis="y", alpha=0.3)
    fig.tight_layout()
    fig.savefig(OUTDIR / "risk_contrib.png", dpi=150)
    plt.close(fig)

    # ---- Provenance metadata for audit
    meta = {
        "generated_at_utc": datetime.now(UTC).isoformat(timespec="seconds"),
        "git_commit": _git_hash_safely(),
        "params": {
            "n_assets": n_assets,
            "n_days": n_days,
            "seed": seed,
            "targets": targets,
        },
        "notes": "Artifacts generated with REAL qpfolio solver and simulation.",
    }
    (OUTDIR / "metadata.json").write_text(json.dumps(meta, indent=2))


def _git_hash_safely() -> str:
    try:
        import subprocess
        return subprocess.check_output(["git", "rev-parse", "HEAD"], text=True).strip()
    except Exception:
        return "unknown"


if __name__ == "__main__":
    main()
