# Scalar Impossibility in Multi-Pillar Complexity Measures

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.17436068.svg)](https://doi.org/10.5281/zenodo.17436068)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**Author**: Oksana Sudoma
**Status**: Preprint Submission (October 25, 2025)
**DOI**: https://doi.org/10.5281/zenodo.17436068

## Overview

This repository contains a mathematical impossibility theorem proving that **no single scalar quantity can universally represent complexity** across systems exhibiting multiple independent complexity pillars. The work demonstrates fundamental limitations in complexity science through rigorous mathematical construction.

The theorem shows that any attempt to create a universal complexity scalar inevitably leads to:
1. Loss of information about individual complexity dimensions
2. Inability to distinguish qualitatively different system states
3. Violation of basic ordering properties required for meaningful comparison

## Main Result

**Theorem 1 (No-Go for Universal Complexity Scalar)**: There exists no continuous function `C: ℝⁿ → ℝ` that can consistently order all multi-pillar complexity states while preserving:
- Monotonicity with respect to each pillar
- Injectivity (distinct states map to distinct values)
- Continuity (smooth response to parameter changes)

The proof constructs an explicit 5-step cycle in complexity space where any scalar assignment leads to logical contradiction.

## Paper

**PDF**: `paper/no_go_complexity_scalar_sudoma_2025.pdf` (29 pages)
**LaTeX source**: `paper/no_go_complexity_scalar_sudoma_2025.tex`
**Bibliography**: `paper/nogocomplexity_v5.bib`

**Key Sections**:
- Section 2: Mathematical framework and four complexity pillars
- Section 3: Constructive proof of impossibility theorem
- Section 4: Implications for complexity science
- Appendix A: Computational verification protocol

## Code

**Toy Example**: `code/five_step_cycle.py` (1770 lines, implemented)
- Demonstrates the 5-step cycle from Theorem 1
- Computes all 4 complexity pillars numerically
- Shows contradiction when attempting scalar assignment
- Based on formal specification in `docs/TOY_EXAMPLE_MATHEMATICAL_FORMALISM.md`

**Requirements**:
```bash
pip install -r requirements.txt
# Dependencies: numpy>=1.20, scipy>=1.6, matplotlib>=3.3
```

**Usage**:
```bash
# Run main demonstration
cd code/
python3 five_step_cycle.py

# Generate figures (300 DPI, publication quality)
python3 generate_figures.py
```

**Expected output**:
- 4 oracle tests (all should pass)
- 5-step cycle evolution table
- Pillar increase summary
- Logical contradiction demonstration

**Figures generated** (via `generate_figures.py`):
- `figures/pillar_evolution.png` - 4-pillar complexity evolution across cycle
- `figures/disk_annulus_transformation.png` - Geometric complexity increase visualization
- `figures/contradiction_diagram.png` - 3D projection of 4D complexity space path

See `outputs/DEMONSTRATION_RESULTS.md` for detailed results and analysis.

## Documentation

**Mathematical Formalism**: `docs/TOY_EXAMPLE_MATHEMATICAL_FORMALISM.md`
- Complete formal specification of toy system
- Explicit calculation of all complexity measures
- Step-by-step derivation of contradiction

**Amendment History**: `docs/NOGO_V8_TO_V9_FINAL_AMENDMENTS.md`
- Evolution from v8 to v9 (final version)
- Technical corrections and clarifications

**Review Reports**: `docs/feedback/`
- Fact-check validation reports
- Beta reader feedback
- Revision history

## Citation

```bibtex
@article{Sudoma2025NoGo,
  title={Scalar Impossibility in Multi-Pillar Complexity Measures: A No-Go Theorem},
  author={Sudoma, Oksana},
  year={2025},
  month={10},
  note={Pending Submission},
  doi={10.5281/zenodo.17436068},
  url={https://doi.org/10.5281/zenodo.17436068}
}
```

## Abstract

Complexity science often seeks single scalar measures to quantify system complexity. We prove this approach is fundamentally impossible for systems exhibiting multiple independent complexity pillars (structural, dynamical, thermodynamic, computational). Through constructive proof, we demonstrate that any attempt to compress multi-dimensional complexity into a scalar inevitably loses critical information and produces logical contradictions. This no-go theorem has implications for complexity theory, systems science, and quantitative approaches to emergence.

## License

**Code**: MIT License (see `LICENSE`)
**Paper**: CC BY 4.0 (Creative Commons Attribution 4.0 International)

You are free to:
- Share and adapt the code (MIT)
- Share and adapt the paper with attribution (CC BY 4.0)

## Contact

**Oksana Sudoma**
Email: boonespacedog@gmail.com
GitHub: [@boonespacedog](https://github.com/boonespacedog)

## Acknowledgments

Mathematical formalism developed with AI assistance (Claude, Anthropic). All theoretical insights, hypothesis formulation, and scientific claims are the sole responsibility of the author.
