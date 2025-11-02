# Maintainers

## Overview
This document lists the current maintainers of **QPFolio** and defines how maintenance responsibilities are managed.  
As of version **0.1.x**, QPFolio is maintained by a single lead developer while the project’s architecture, optimization engine, and documentation are being stabilized.

---

## Current Maintainer

| Name | Role | Responsibilities | Contact |
|------|------|------------------|----------|
| **Rolf Carlson** | Founder & Lead Maintainer | Core architecture, mathematical formulations, solver integration, documentation, and release management. | See contact email in `pyproject.toml` or the GitHub repository profile. |

---

## Responsibilities
Maintainers are responsible for ensuring the project remains stable, consistent, and well-documented.  
Their specific duties include:

1. **Technical Oversight**
   - Approve, review, and merge code changes.
   - Maintain build and testing pipelines.
   - Manage dependencies and solver compatibility.

2. **Project Direction**
   - Define the roadmap and release milestones.
   - Evaluate new features for mathematical correctness and practical relevance.
   - Maintain alignment with the long-term goals of reproducibility and clarity.

3. **Quality Assurance**
   - Ensure all code meets style and testing standards.
   - Oversee documentation, changelog, and version tagging.

4. **Security and Compliance**
   - Review third-party dependencies for license and security issues.
   - Coordinate vulnerability response (when active).

---

## Future Maintainers
When QPFolio reaches a stable public release (`v1.0.0`), additional maintainers may be invited to assist with:
- Solver backends and mathematical extensions.
- Documentation and educational examples.
- Continuous integration and infrastructure.

New maintainers will be added to this document following a transparent review and onboarding process defined in `GOVERNANCE.md`.

---

## Maintenance Philosophy
- **Clarity before complexity:** Favor clear, maintainable designs over maximal features.
- **Mathematical rigor:** Preserve correctness and convexity in all optimization formulations.
- **Reproducibility:** Ensure every release is deterministic, testable, and documented.
- **Transparency:** Decisions, releases, and changelogs are open and traceable.

---

**Summary:**  
> QPFolio is presently maintained by a single developer during its foundational stage.  
> As the project matures, maintenance will expand to include collaborators aligned with its principles of clarity, rigor, and reproducibility.
