.. _methods:

Methods: Mathematical Formulations
==================================

This section summarizes the optimization problems supported by **qpfolio**.
Throughout, let :math:`\mu \in \mathbb{R}^N` be expected returns, :math:`\Sigma \in \mathbb{R}^{N\times N}` the PSD covariance, and :math:`\mathbf{w}\in\mathbb{R}^N` portfolio weights.

Mean–Variance Optimization (MVO)
--------------------------------
.. math::

   \begin{aligned}
   \min_{\mathbf{w}} \quad & \tfrac{1}{2}\,\mathbf{w}^\top \Sigma \mathbf{w} \\
   \text{s.t.} \quad & \mathbf{w}^\top \mu \ge R_{\text{target}}, \\
                     & \mathbf{w}^\top \mathbf{1} = 1, \\
                     & \mathbf{w} \ge 0 \quad (\text{optional, long-only})
   \end{aligned}

**Purpose.** Minimize variance for a target return.

**Strengths.** Convex, interpretable, efficient.

**Weaknesses.** Sensitive to estimation error (especially :math:`\mu` and off-diagonal :math:`\Sigma`).

Most Diversified Portfolio (MDP)
--------------------------------
Diversification ratio :math:`\mathrm{DR}(\mathbf{w}) = \dfrac{\sum_i w_i \sigma_i}{\sqrt{\mathbf{w}^\top \Sigma \mathbf{w}}}`.

A QP surrogate:

.. math::

   \begin{aligned}
   \min_{\mathbf{w}} \quad & \tfrac{1}{2}\,\mathbf{w}^\top \Sigma \mathbf{w} \\
   \text{s.t.} \quad & \mathbf{w}^\top \sigma = 1, \\
                     & \mathbf{w}^\top \mathbf{1} = 1, \\
                     & \mathbf{w} \ge 0
   \end{aligned}

**Purpose.** Maximize diversification; reduce concentration risk.

**Notes.** Enforces a normalization via :math:`\mathbf{w}^\top \sigma`.

Distributionally Robust Optimization (DRO, moment-based)
--------------------------------------------------------
A simple robustification inflates covariance by a PSD penalty :math:`\Gamma`:

.. math::

   \begin{aligned}
   \min_{\mathbf{w}} \quad & \tfrac{1}{2}\,\mathbf{w}^\top (\Sigma + \Gamma) \mathbf{w} \\
   \text{s.t.} \quad & \mathbf{w}^\top \mu \ge R_{\text{target}}, \\
                     & \mathbf{w}^\top \mathbf{1} = 1, \\
                     & \mathbf{w} \ge 0
   \end{aligned}

**Interpretation.** Model uncertainty enters as additional risk; conservatism increases with :math:`\Gamma`.

Method Selection: Strengths & Weaknesses
----------------------------------------
- **MVO**: highest efficiency under accurate estimates; fragile to noise.
- **MDP**: robust to mean misspecification; focuses on spread of risk.
- **DRO**: trades performance for resilience to distributional shifts.
