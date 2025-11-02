# Project Governance

## Overview
QPFolio is currently in **early-stage development (v0.1.x)** and maintained by a single primary developer.  
At this stage, all design, architectural, and release decisions are made by the maintainer to ensure conceptual and technical consistency across the project.

This document describes the current governance model and the plan for transitioning to a more open and collaborative structure once the project matures.

---

## Current Governance Model

### 1. Maintainer-Led Development
All aspects of the project — including roadmap direction, code contributions, and release management — are currently overseen by the **Project Maintainer**:

> **Maintainer:** Rolf Carlson  
> **Role:** Project founder and lead developer  
> **Responsibility:** Architecture, code, documentation, and release management.

The maintainer holds final authority over:
- Acceptance of code and documentation changes.
- Release timing and versioning.
- Design and implementation priorities.
- Licensing and external dependency review.

### 2. External Participation
While QPFolio is not yet open for active development or contribution, feedback and bug reports are welcome through GitHub Issues.  
These will be reviewed and considered for inclusion in future releases, depending on project priorities and stability requirements.

---

## Future Governance (Post–v1.0.0)

When the project reaches a stable public release, governance is expected to evolve toward a **“core maintainer + contributor”** model with the following structure:

### Maintainers
- Oversee overall direction and ensure code quality.
- Approve major features, APIs, and backward-incompatible changes.
- Coordinate release cycles and dependency management.

### Contributors
- Submit pull requests and issue reports.
- Participate in code reviews and discussions.
- Propose new features or documentation improvements.

### Decision Process
- Technical decisions will favor consensus when possible.
- In cases of disagreement, the lead maintainer will have final say to ensure continuity.
- Significant changes (APIs, architecture, or dependencies) will be logged in `CHANGELOG.md` and discussed publicly.

---

## Versioning and Release Policy
QPFolio follows **Semantic Versioning (SemVer 2.0.0)**:
- `MAJOR`: Breaking changes or major design shifts.
- `MINOR`: Backward-compatible feature additions.
- `PATCH`: Bug fixes or minor adjustments.

All releases are signed and tagged in Git with corresponding changelog updates.

---

## Guiding Principles
- **Clarity over consensus:** Early development benefits from clear direction.
- **Reproducibility over speed:** Each release must be stable and testable.
- **Transparency over secrecy:** Design rationale and decisions are documented whenever possible.

---

## Contact
For inquiries related to governance, releases, or long-term planning, please reach out via the maintainer contact listed in `pyproject.toml` or on the project’s GitHub profile.

---

**Summary:**  
> QPFolio is currently governed by a single maintainer for focus and cohesion.  
> As the project matures, a structured and transparent community governance model will emerge to support growth and collaboration.
