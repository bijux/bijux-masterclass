# Module 01 — Why Reproducibility Fails

*Motivation, mental models, and the problem DVC actually solves*

---

## Purpose of this Module

Professionals often turn to DVC not out of an abstract interest in reproducibility, but because a practical issue has arisen: a result cannot be regenerated, a model's metrics have shifted inexplicably, a colleague obtains different outcomes from identical code, or a report proves indefensible months later.

This module serves three essential objectives:

1. **Highlight the challenges explicitly**: It demonstrates why contemporary machine learning (ML) workflows inherently compromise reproducibility.

2. **Refine conceptual frameworks**: It clarifies why familiar tools such as Git, Jupyter notebooks, and standalone scripts appear adequate but ultimately fall short.

3. **Delineate the scope precisely**: Prior to exploring DVC, it defines the achievable forms of reproducibility, their limitations, and the role of supporting tools.

Upon completion, you should possess a definitive response to: *What problem does DVC address, and what issues does it deliberately exclude?* If this remains ambiguous, subsequent modules may seem disconnected.

**Prerequisites**: Familiarity with basic Git operations and ML workflows is assumed. If needed, review Git fundamentals before proceeding.

---

## 1.1 A Familiar Scenario (Grounded in Practice)

Examine a standard ML workflow, illustrated with simplified elements:

- A dataset resides in `data/raw.csv`.
- A script, `train.py`, processes the data and trains a model (e.g., via scikit-learn or PyTorch).
- Metrics (e.g., accuracy) are output to the console or a file like `metrics.csv`.
- Code and results are committed to Git, perhaps with a README outlining execution steps.

Months later:
- Rerunning `train.py` yields divergent metrics.
- The cause is unclear: perhaps the dataset was subtly altered, preprocessing occurred offline, or library versions changed.
- A team member asserts no modifications were made, yet outcomes differ.

No overt errors occur—no crashes or exceptions. Nonetheless, the outcome is irreproducible.

This reflects not individual error, but the inherent outcome of ML processes lacking formalized dependencies. To illustrate, consider this pseudo-code snippet from `train.py`:

```python
import pandas as pd
import numpy as np  # Version implicitly affects random seeding

data = pd.read_csv('data/raw.csv')  # Assumes unchanged file
np.random.seed(42)  # Seed set, but environment may influence behavior

# Training logic...
```

Such setups invite silent inconsistencies.

---

## 1.2 Repeatability vs. Reproducibility: A Key Differentiation

These terms are frequently conflated, yet they denote distinct concepts.

### Repeatability
> Executing identical code repeatedly within the same environment and machine, yielding consistent results.

This is localized and vulnerable, achievable through minimal interventions such as avoiding system restarts, library updates, or data modifications. Failures often manifest subtly.

### Reproducibility
> Recreating equivalent results over time, across machines, and among individuals via documented artifacts and protocols.

This is broader and resilient, enduring fresh repository clones, varied environments, team transitions, continuous integration (CI) pipelines, and audits.

Most ML processes offer transient repeatability but are structurally irreproducible. DVC prioritizes the latter.

**Key Takeaway**: Distinguishing these fosters precise expectations from tools like DVC.

---

## 1.3 Limitations of Git in ML Contexts

Git excels in many domains but is often inappropriately extended to ML.

### Git's Strengths
- Versioning textual content.
- Capturing deliberate modifications.
- Facilitating branching and merging of source code.
- Enabling granular line-by-line differences.

### Git's Gaps
- Handling voluminous binary files.
- Managing derived outputs.
- Recording runtime contexts.
- Linking causal dependencies among stages.

Git logs alterations, not derivations. This fosters the misconception: "Versioned code implies versioned results." In reality, outcomes hinge on precise data, parameters, sequencing, environments, and randomness—elements Git overlooks.

DVC complements Git by addressing these omissions in data-centric systems.

---

## 1.4 Overlooked Inputs in ML Scripts

Inputs transcend explicit files and arguments, even in straightforward scripts.

### Evident Inputs
- Training datasets.
- Configuration YAML or JSON files.
- Command-line parameters.

### Concealed Inputs (Commonly Overlooked)
- Library versions (e.g., NumPy vs. TensorFlow).
- Hardware-specific behaviors (e.g., BLAS for linear algebra, CUDA for GPU acceleration).
- System settings (e.g., locale, operating system).
- Random seeds.
- Floating-point precision variations.
- Filesystem enumeration order.

These elements impact results tracelessly unless documented. A reproducible framework must address: *What inputs were present, and how did they shape the output?* Few ML initiatives can respond comprehensively.

**Illustration**: A text-based diagram of input layers:

```
Obvious Inputs --> [Data Files | Configs | Flags]
Hidden Inputs  --> [Libs | Hardware | OS | Seeds | FP Impl | FS Order]
Combined       --> Execution --> Output
```

---

## 1.5 ML's Unique Reproducibility Challenges Compared to Software Engineering

Traditional software features explicit inputs, deterministic outputs, and inherently repeatable builds. In contrast, ML involves expansive, mutable inputs; probabilistic outputs; amplified effects from minor changes; and evaluative rather than absolute correctness.

Consequently:
- Unnoticed drifts prevail.
- Troubleshooting is historical.
- Reliability diminishes progressively.

In ML, reproducibility safeguards against inadvertent errors, rendering it indispensable.

---

## 1.6 Boundaries of Reproducibility

Precision in scope is vital.

Reproducibility excludes:
- Uniform floating-point outcomes across hardware.
- Perpetual cloud storage access.
- Data semantic accuracy.
- Conclusion validity.

DVC avoids:
- Data validation.
- Determinism assurance.
- Experimental methodology substitution.
- Comprehensive environment oversight.

It upholds mechanical invariants, not empirical veracity. Misaligned expectations often underlie DVC dissatisfaction.

---

## 1.7 Foundational Principle

Reproducibility inheres not in isolated scripts, but in integrated systems encompassing data, code, execution, storage, personnel, and temporal factors. Implicit elements render it fortuitous.

DVC renders pivotal components explicit, versioned, and verifiable, underpinning the course.

---

## 1.8 Initial Reflective Exercise (Pre-DVC)

Engage earnestly:
1. Select a prior project.
2. Document: data origins, alterations, key parameters, and environment.
3. Evaluate: Could another reproduce it in six months? Could you?

Affirmative uncertainty is typical; this course aims to resolve it.

**Guidance**: Note findings in a journal for later comparison.

---

## 1.9 Course Overview

Subsequent modules establish enforceable invariants:
- **Module 02**: Immutable, content-based data identity.
- **Module 03**: Environments as declared inputs.
- **Module 04**: Pipelines as verifiable directed acyclic graphs (DAGs).
- **Module 05**: Metrics and parameters as interpretive agreements.
- **Module 06**: Experiments as managed variations.
- **Module 07**: Collaborative and CI-driven safeguards.
- **Module 08**: Endurance against scale and incidents.

Each invariant is defined, exemplified, and failure-tested rigorously.

---

## Module 01 — Readiness Checklist

Affirm readiness by confirming:
- [ ] Explanation of Git's inadequacy for reproducibility.
- [ ] Differentiation between repeatability and reproducibility.
- [ ] Identification of at least five hidden inputs in personal workflows.
- [ ] Awareness of DVC's exclusions.
- [ ] Recognition of reproducibility as systemic.

Clarify uncertainties before advancing; foundational precision enables depth.

---

### Transition to Module 02

With the challenge articulated, we introduce DVC's initial assurance: *Data identity stems from content, independent of location, naming, or purpose.* Module 02 codifies this, establishing its foundational role.