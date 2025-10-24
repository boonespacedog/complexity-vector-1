"""
📄 File: generate_figures.py
Purpose: Generate 3 publication-quality figures for No-Go Scalar Impossibility Theorem
Created: October 24, 2025
Used by: Standalone figure generation for paper submission

Figure Generation for No-Go Scalar Impossibility Theorem Toy Example

Creates 3 publication-quality figures demonstrating Theorem 1.

Paper: Sudoma, O. (2025). Scalar Impossibility in Multi-Pillar Complexity Measures.
DOI: 10.5281/zenodo.17436068

Usage:
    python generate_figures.py

Outputs:
    figures/pillar_evolution.png (10×6 inches, 300 DPI)
    figures/disk_annulus_transformation.png (12×5 inches, 300 DPI)
    figures/contradiction_diagram.png (8×8 inches, 300 DPI)

Requirements:
    numpy, matplotlib, scipy
    five_step_cycle.py (imports all morphisms and complexity measures)

Mathematical Spec: docs/TOY_EXAMPLE_MATHEMATICAL_FORMALISM.md
Critical Review: docs/CRITICAL_REVIEW_NOGO_IMPLEMENTATION.md (recommendations)
"""

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import time
import os

# Import all functions from five_step_cycle
from five_step_cycle import (
    # System state
    SystemState,
    initial_state,

    # Morphisms
    morphism_1_circuit_compilation,
    morphism_2_syndrome_encoding,
    morphism_3_arnold_cat,
    morphism_4_disk_to_annulus,
    morphism_5_closing_isomorphism,

    # Complexity measures
    compute_C_alg,
    compute_C_info,
    compute_C_dyn,
    compute_C_geom,

    # Geometric functions
    sample_disk,
    T_a,
    central_void_score,
    bits_to_points,

    # Parameters
    A_PARAM,
    DELTA_ALG,
    DELTA_INFO,
    DELTA_DYN,
    DELTA_GEOM,
)


# === CONFIG ===
# 🛠️ File Paths
OUTPUT_DIR = "/Users/mac/Desktop/egg-paper/complexity-vector-1/figures"
FIG1_PATH = os.path.join(OUTPUT_DIR, "pillar_evolution.png")
FIG2_PATH = os.path.join(OUTPUT_DIR, "disk_annulus_transformation.png")
FIG3_PATH = os.path.join(OUTPUT_DIR, "contradiction_diagram.png")

# 🧪 Figure Parameters
DPI = 300  # Publication quality
FIG1_SIZE = (10, 6)  # Pillar evolution
FIG2_SIZE = (12, 5)  # Disk/annulus
FIG3_SIZE = (8, 8)   # Contradiction

# Colorblind-friendly palette (Tol palette)
COLORS = {
    'C_alg': '#0077BB',   # Blue
    'C_info': '#33BB00',  # Green
    'C_dyn': '#EE3377',   # Red
    'C_geom': '#9933CC',  # Purple
    'delta': '#CC3311',   # Dark red for annotations
    'void': '#FFD700',    # Gold for void region
}

# Font sizes
FONT_TITLE = 14
FONT_LABEL = 12
FONT_TICK = 10
FONT_ANNOTATION = 9

# 🧠 Notes
# - All parameters from mathematical formalism
# - Colorblind-friendly colors (Tol palette)
# - 300 DPI for publication quality
# - 1s pause after each savefig (rate limiting)


def ensure_output_dir():
    """
    🧠 Function: ensure_output_dir
    Role: Create figures directory if it doesn't exist
    Inputs: None
    Returns: None (side effect: directory created)
    Notes: Required before saving figures
    """
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    print(f"✓ Output directory ready: {OUTPUT_DIR}")


def create_pillar_evolution():
    """
    🧠 Function: create_pillar_evolution
    Role: Generate Figure 1 - 4-pillar complexity evolution across 5-step cycle
    Inputs: None (uses five_step_cycle functions)
    Returns: None (saves figure to disk)

    Paper reference: Theorem 1, visual summary
    Shows: Each morphism raises its target pillar, φ returns to X_0

    Figure content:
    - X-axis: Cycle steps 0-5 (X₀ → f_alg → f_info → f_dyn → f_geom → φ)
    - Y-axis: Complexity value [0, 1]
    - 4 lines: C_alg (blue), C_info (green), C_dyn (red), C_geom (purple)
    - Annotations: δ_alg, δ_info, δ_dyn, δ_geom arrows showing increases
    - Final step: Show return to initial values (φ closing)

    Size: 10×6 inches, 300 DPI
    """
    print("\n" + "="*60)
    print("Generating Figure 1: Pillar Evolution")
    print("="*60)

    # Run 5-step cycle
    print("Running 5-step cycle...")
    X_0 = initial_state()
    X_1 = morphism_1_circuit_compilation(X_0)
    X_2 = morphism_2_syndrome_encoding(X_1)
    X_3 = morphism_3_arnold_cat(X_2)

    # X_4 requires point cloud generation
    n_points = 10000
    points_disk = bits_to_points(X_3.C, n_points)
    points_annulus = T_a(points_disk, a=A_PARAM)
    X_4 = SystemState(X_3.C.copy(), X_3.Q.copy(), X_3.morphisms_applied.copy())
    X_4.morphisms_applied.add('f_geom')
    X_4._points = points_annulus

    X_0_return = morphism_5_closing_isomorphism(X_4)

    states = [X_0, X_1, X_2, X_3, X_4, X_0_return]
    labels = ["X₀\n(Initial)", "X₁\n(f_alg)", "X₂\n(f_info)",
              "X₃\n(f_dyn)", "X₄\n(f_geom)", "X₀'\n(φ closing)"]

    # Compute all pillar values
    print("Computing complexity pillars...")
    C_alg_values = [compute_C_alg(X) for X in states]
    C_info_values = [compute_C_info(X) for X in states]
    C_dyn_values = [compute_C_dyn(X) for X in states]
    C_geom_values = [compute_C_geom(X, a=A_PARAM) for X in states]

    steps = np.arange(len(states))

    # Create figure
    print("Creating plot...")
    fig, ax = plt.subplots(figsize=FIG1_SIZE, dpi=DPI)

    # Plot lines
    ax.plot(steps, C_alg_values, 'o-', linewidth=2.5, markersize=8,
            color=COLORS['C_alg'], label='$C_{\\mathrm{alg}}$ (Algorithmic)')
    ax.plot(steps, C_info_values, 's-', linewidth=2.5, markersize=8,
            color=COLORS['C_info'], label='$C_{\\mathrm{info}}$ (Information)')
    ax.plot(steps, C_dyn_values, '^-', linewidth=2.5, markersize=8,
            color=COLORS['C_dyn'], label='$C_{\\mathrm{dyn}}$ (Dynamical)')
    ax.plot(steps, C_geom_values, 'D-', linewidth=2.5, markersize=8,
            color=COLORS['C_geom'], label='$C_{\\mathrm{geom}}$ (Geometric)')

    # Annotate increases with arrows
    annotations = [
        (0.5, C_alg_values[1], f'δ_alg = {C_alg_values[1] - C_alg_values[0]:.2f}', COLORS['C_alg']),
        (1.5, C_info_values[2], f'δ_info = {C_info_values[2] - C_info_values[1]:.2f}', COLORS['C_info']),
        (2.5, C_dyn_values[3], f'δ_dyn = {C_dyn_values[3] - C_dyn_values[2]:.2f}', COLORS['C_dyn']),
        (3.5, C_geom_values[4], f'δ_geom = {C_geom_values[4] - C_geom_values[3]:.2f}', COLORS['C_geom']),
    ]

    for x, y, text, color in annotations:
        ax.annotate(text, xy=(x, y), xytext=(x, y + 0.15),
                   arrowprops=dict(arrowstyle='->', color=COLORS['delta'], lw=1.5),
                   fontsize=FONT_ANNOTATION, color=COLORS['delta'],
                   ha='center', bbox=dict(boxstyle='round,pad=0.3',
                                         facecolor='white', edgecolor=color, alpha=0.8))

    # Highlight return to X_0
    ax.annotate('Return to X₀', xy=(5, C_alg_values[5]), xytext=(5, 0.7),
               arrowprops=dict(arrowstyle='->', color='black', lw=2, linestyle='--'),
               fontsize=FONT_ANNOTATION + 1, ha='center',
               bbox=dict(boxstyle='round,pad=0.4', facecolor='yellow',
                        edgecolor='black', alpha=0.7))

    # Styling
    ax.set_xlabel('Cycle Step', fontsize=FONT_LABEL, fontweight='bold')
    ax.set_ylabel('Complexity Value', fontsize=FONT_LABEL, fontweight='bold')
    ax.set_title('Four-Pillar Complexity Evolution Through 5-Step Cycle',
                fontsize=FONT_TITLE, fontweight='bold', pad=15)
    ax.set_xticks(steps)
    ax.set_xticklabels(labels, fontsize=FONT_TICK)
    ax.set_ylim(-0.05, 1.15)
    ax.grid(True, alpha=0.3, linestyle='--')
    ax.legend(loc='upper left', fontsize=FONT_TICK, framealpha=0.9)

    plt.tight_layout()

    # Save
    print(f"Saving to {FIG1_PATH}...")
    plt.savefig(FIG1_PATH, dpi=DPI, bbox_inches='tight')
    print(f"✓ Figure 1 saved: {FIG1_PATH}")
    plt.close()

    # Compute total accumulation
    total_increase = sum([
        max(0, C_alg_values[1] - C_alg_values[0]),
        max(0, C_info_values[2] - C_info_values[1]),
        max(0, C_dyn_values[3] - C_dyn_values[2]),
        max(0, C_geom_values[4] - C_geom_values[3]),
    ])
    print(f"Total accumulation Σδ = {total_increase:.3f}")
    print(f"Expected minimum: {DELTA_ALG + DELTA_INFO + DELTA_DYN + DELTA_GEOM:.3f}")

    # Rate limiting: MANDATORY 1s pause after savefig
    print("Pausing 1 second (rate limiting)...")
    time.sleep(1)
    print("✓ Pause complete\n")


def create_disk_annulus_figure():
    """
    🧠 Function: create_disk_annulus_figure
    Role: Generate Figure 2 - Disk→Annulus transformation visualization
    Inputs: None (uses five_step_cycle functions)
    Returns: None (saves figure to disk)

    Paper reference: Appendix A.4, Morphism f_geom
    Shows: Geometric complexity increase via T_a map

    Figure content:
    - Left panel: 10,000 points in unit disk (before T_a)
    - Right panel: Same points in annulus [a,1] (after T_a)
    - Color: Points by radial distance
    - Annotations: a=0.68 inner radius, void region highlighted
    - Overlay: C_geom values (Disk: ~0.001, Annulus: ~1.000)

    Size: 12×5 inches, 300 DPI
    """
    print("\n" + "="*60)
    print("Generating Figure 2: Disk→Annulus Transformation")
    print("="*60)

    # Generate point clouds
    print("Generating point clouds...")
    n_points = 10000
    points_disk = sample_disk(n_points, seed=42)
    points_annulus = T_a(points_disk, a=A_PARAM)

    # Compute C_geom for both
    c_geom_disk = central_void_score(points_disk, a=A_PARAM)
    c_geom_annulus = central_void_score(points_annulus, a=A_PARAM)

    print(f"C_geom(Disk) = {c_geom_disk:.3f}")
    print(f"C_geom(Annulus) = {c_geom_annulus:.3f}")
    print(f"Increase: δ_geom = {c_geom_annulus - c_geom_disk:.3f}")

    # Create figure with 2 subplots
    print("Creating plot...")
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=FIG2_SIZE, dpi=DPI)

    # Compute radial distances for coloring
    r_disk = np.linalg.norm(points_disk, axis=1)
    r_annulus = np.linalg.norm(points_annulus, axis=1)

    # Left panel: Disk
    scatter1 = ax1.scatter(points_disk[:, 0], points_disk[:, 1],
                          c=r_disk, cmap='viridis', s=1, alpha=0.3)
    ax1.set_aspect('equal')
    ax1.set_xlim(-1.1, 1.1)
    ax1.set_ylim(-1.1, 1.1)
    ax1.set_xlabel('x', fontsize=FONT_LABEL)
    ax1.set_ylabel('y', fontsize=FONT_LABEL)
    ax1.set_title('Unit Disk (Before $T_a$)', fontsize=FONT_TITLE, fontweight='bold')
    ax1.grid(True, alpha=0.3)

    # Add unit circle
    theta = np.linspace(0, 2*np.pi, 100)
    ax1.plot(np.cos(theta), np.sin(theta), 'k--', linewidth=1.5, label='$r=1$')

    # Annotate C_geom
    ax1.text(0.05, 0.95, f'$C_{{\\mathrm{{geom}}}} = {c_geom_disk:.3f}$',
            transform=ax1.transAxes, fontsize=FONT_ANNOTATION + 2,
            verticalalignment='top',
            bbox=dict(boxstyle='round,pad=0.5', facecolor='white',
                     edgecolor='black', alpha=0.9))

    # Right panel: Annulus
    scatter2 = ax2.scatter(points_annulus[:, 0], points_annulus[:, 1],
                          c=r_annulus, cmap='viridis', s=1, alpha=0.3)
    ax2.set_aspect('equal')
    ax2.set_xlim(-1.1, 1.1)
    ax2.set_ylim(-1.1, 1.1)
    ax2.set_xlabel('x', fontsize=FONT_LABEL)
    ax2.set_ylabel('y', fontsize=FONT_LABEL)
    ax2.set_title(f'Annulus $[a,1]$ (After $T_a$)', fontsize=FONT_TITLE, fontweight='bold')
    ax2.grid(True, alpha=0.3)

    # Add circles: inner (a) and outer (1)
    ax2.plot(A_PARAM * np.cos(theta), A_PARAM * np.sin(theta),
            'r-', linewidth=2, label=f'$r={A_PARAM}$ (inner)')
    ax2.plot(np.cos(theta), np.sin(theta), 'k--', linewidth=1.5, label='$r=1$ (outer)')

    # Highlight void region
    void_circle = plt.Circle((0, 0), A_PARAM, color=COLORS['void'],
                            alpha=0.15, zorder=0, label='Central void')
    ax2.add_patch(void_circle)

    # Annotate C_geom
    ax2.text(0.05, 0.95, f'$C_{{\\mathrm{{geom}}}} = {c_geom_annulus:.3f}$',
            transform=ax2.transAxes, fontsize=FONT_ANNOTATION + 2,
            verticalalignment='top',
            bbox=dict(boxstyle='round,pad=0.5', facecolor='white',
                     edgecolor='black', alpha=0.9))

    # Legends
    ax1.legend(loc='lower right', fontsize=FONT_TICK-1)
    ax2.legend(loc='lower right', fontsize=FONT_TICK-1)

    # Colorbars
    cbar1 = plt.colorbar(scatter1, ax=ax1, label='Radial distance $r$',
                        shrink=0.7, pad=0.05)
    cbar2 = plt.colorbar(scatter2, ax=ax2, label='Radial distance $r$',
                        shrink=0.7, pad=0.05)

    # Overall title
    fig.suptitle('Geometric Complexity Increase via Area-Preserving Map $T_a$',
                fontsize=FONT_TITLE + 1, fontweight='bold', y=0.98)

    plt.tight_layout(rect=[0, 0, 1, 0.96])

    # Save
    print(f"Saving to {FIG2_PATH}...")
    plt.savefig(FIG2_PATH, dpi=DPI, bbox_inches='tight')
    print(f"✓ Figure 2 saved: {FIG2_PATH}")
    plt.close()

    # Rate limiting: MANDATORY 1s pause after savefig
    print("Pausing 1 second (rate limiting)...")
    time.sleep(1)
    print("✓ Pause complete\n")


def create_contradiction_diagram():
    """
    🧠 Function: create_contradiction_diagram
    Role: Generate Figure 3 - Visualization of impossibility contradiction
    Inputs: None (uses five_step_cycle functions)
    Returns: None (saves figure to disk)

    Paper reference: Theorem 1 proof visualization
    Shows: 4D cycle with impossible equality C*(X₄) = C*(X₀)

    Figure content:
    - 3D projection of 4D pillar space (use first 3 pillars for visualization)
    - Points X₀, X₁, X₂, X₃, X₄ connected by arrows
    - Arrow from X₄ back to X₀ (φ closing isomorphism)
    - Color gradient: Shows "distance" accumulation
    - Text: "Σδ = 2.628 > 0" and "φ: X₄ ≅ X₀"

    Size: 8×8 inches, 300 DPI
    """
    print("\n" + "="*60)
    print("Generating Figure 3: Contradiction Diagram")
    print("="*60)

    # Run 5-step cycle
    print("Running 5-step cycle...")
    X_0 = initial_state()
    X_1 = morphism_1_circuit_compilation(X_0)
    X_2 = morphism_2_syndrome_encoding(X_1)
    X_3 = morphism_3_arnold_cat(X_2)

    # X_4 requires point cloud
    n_points = 10000
    points_disk = bits_to_points(X_3.C, n_points)
    points_annulus = T_a(points_disk, a=A_PARAM)
    X_4 = SystemState(X_3.C.copy(), X_3.Q.copy(), X_3.morphisms_applied.copy())
    X_4.morphisms_applied.add('f_geom')
    X_4._points = points_annulus

    X_0_return = morphism_5_closing_isomorphism(X_4)

    states = [X_0, X_1, X_2, X_3, X_4, X_0_return]
    labels = ["$X_0$", "$X_1$", "$X_2$", "$X_3$", "$X_4$", "$X_0'$"]

    # Compute pillar values
    print("Computing complexity vectors...")
    pillar_vectors = []
    for X in states:
        c_alg = compute_C_alg(X)
        c_info = compute_C_info(X)
        c_dyn = compute_C_dyn(X)
        c_geom = compute_C_geom(X, a=A_PARAM)
        pillar_vectors.append([c_alg, c_info, c_dyn, c_geom])

    pillar_vectors = np.array(pillar_vectors)

    # Use first 3 pillars for 3D visualization
    # (4D visualization requires projection, use C_alg, C_info, C_dyn)
    X_coords = pillar_vectors[:, 0]  # C_alg
    Y_coords = pillar_vectors[:, 1]  # C_info
    Z_coords = pillar_vectors[:, 2]  # C_dyn

    # Compute total accumulation
    total_increase = sum([
        max(0, pillar_vectors[1][0] - pillar_vectors[0][0]),
        max(0, pillar_vectors[2][1] - pillar_vectors[1][1]),
        max(0, pillar_vectors[3][2] - pillar_vectors[2][2]),
        max(0, pillar_vectors[4][3] - pillar_vectors[3][3]),
    ])

    print(f"Total accumulation Σδ = {total_increase:.3f}")

    # Create 3D plot
    print("Creating 3D plot...")
    fig = plt.figure(figsize=FIG3_SIZE, dpi=DPI)
    ax = fig.add_subplot(111, projection='3d')

    # Plot path with arrows
    for i in range(len(states) - 1):
        if i < len(states) - 2:
            # Forward morphisms (colored by step)
            color = plt.cm.viridis(i / 4)
            ax.plot([X_coords[i], X_coords[i+1]],
                   [Y_coords[i], Y_coords[i+1]],
                   [Z_coords[i], Z_coords[i+1]],
                   'o-', color=color, linewidth=2.5, markersize=10,
                   label=f'Step {i}→{i+1}')
        else:
            # Closing isomorphism (dashed red)
            ax.plot([X_coords[i], X_coords[i+1]],
                   [Y_coords[i], Y_coords[i+1]],
                   [Z_coords[i], Z_coords[i+1]],
                   'o--', color='red', linewidth=3, markersize=10,
                   label='φ (closing)')

    # Annotate points
    for i, label in enumerate(labels[:-1]):  # Skip X_0' (same as X_0)
        ax.text(X_coords[i], Y_coords[i], Z_coords[i],
               f'  {label}', fontsize=FONT_ANNOTATION + 2,
               fontweight='bold')

    # Add contradiction text box
    textstr = (f'Contradiction:\n'
              f'Σδ = {total_increase:.3f} > 0\n'
              f'φ: $X_4 \\cong X_0$\n'
              f'⇒ $C^*(X_0) = C^*(X_4)$\n'
              f'     $\\geq C^*(X_0) + {total_increase:.2f}$\n'
              f'⇒ 0 ≥ {total_increase:.2f}  ✗')

    ax.text2D(0.02, 0.98, textstr, transform=ax.transAxes,
             fontsize=FONT_ANNOTATION + 1, verticalalignment='top',
             bbox=dict(boxstyle='round,pad=0.8', facecolor='yellow',
                      edgecolor='red', alpha=0.9, linewidth=2))

    # Styling
    ax.set_xlabel('$C_{\\mathrm{alg}}$ (Algorithmic)', fontsize=FONT_LABEL,
                 fontweight='bold', labelpad=10)
    ax.set_ylabel('$C_{\\mathrm{info}}$ (Information)', fontsize=FONT_LABEL,
                 fontweight='bold', labelpad=10)
    ax.set_zlabel('$C_{\\mathrm{dyn}}$ (Dynamical)', fontsize=FONT_LABEL,
                 fontweight='bold', labelpad=10)
    ax.set_title('Impossibility via Cycle Contradiction\n(4D Complexity Space, 3D Projection)',
                fontsize=FONT_TITLE, fontweight='bold', pad=20)

    # Legend (hide to avoid clutter, contradiction is self-explanatory)
    # ax.legend(loc='upper left', fontsize=FONT_TICK-2, framealpha=0.8)

    # Grid
    ax.grid(True, alpha=0.3)

    # View angle
    ax.view_init(elev=20, azim=45)

    plt.tight_layout()

    # Save
    print(f"Saving to {FIG3_PATH}...")
    plt.savefig(FIG3_PATH, dpi=DPI, bbox_inches='tight')
    print(f"✓ Figure 3 saved: {FIG3_PATH}")
    plt.close()

    # Rate limiting: MANDATORY 1s pause after savefig
    print("Pausing 1 second (rate limiting)...")
    time.sleep(1)
    print("✓ Pause complete\n")


def main():
    """
    🧠 Function: main
    Role: Execute all figure generation with rate limiting
    Inputs: None
    Returns: None (saves all 3 figures)

    Execution sequence:
    1. Create output directory
    2. Generate Figure 1 (pillar evolution) + 1s pause
    3. Generate Figure 2 (disk/annulus) + 1s pause
    4. Generate Figure 3 (contradiction) + 1s pause
    5. Report completion

    Notes:
    - MANDATORY 1-second pause after each savefig
    - Total execution time: ~10-15 seconds
    - All figures saved to figures/ directory
    """
    print("""
╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                              ║
║           FIGURE GENERATION FOR NO-GO SCALAR IMPOSSIBILITY THEOREM          ║
║                                                                              ║
║  Paper: Sudoma, O. (2025). Scalar Impossibility in Multi-Pillar Complexity  ║
║  DOI: 10.5281/zenodo.17436068                                               ║
║                                                                              ║
║  Generates 3 publication-quality figures (300 DPI):                         ║
║  1. Pillar evolution across 5-step cycle                                    ║
║  2. Disk→annulus transformation showing geometric complexity increase       ║
║  3. 4D contradiction diagram (3D projection)                                ║
║                                                                              ║
║  MANDATORY RATE LIMITING: 1s pause after each figure save                   ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
    """)

    # Create output directory
    ensure_output_dir()

    # Generate all figures with mandatory pauses
    start_time = time.time()

    create_pillar_evolution()       # Figure 1 + 1s pause
    create_disk_annulus_figure()    # Figure 2 + 1s pause
    create_contradiction_diagram()  # Figure 3 + 1s pause

    elapsed_time = time.time() - start_time

    # Summary
    print("\n" + "="*60)
    print("FIGURE GENERATION COMPLETE")
    print("="*60)
    print(f"\n✓ All 3 figures generated successfully")
    print(f"✓ Output directory: {OUTPUT_DIR}")
    print(f"✓ Total time: {elapsed_time:.1f} seconds")
    print(f"✓ Rate limiting enforced: 3 × 1s pauses = 3s")
    print(f"\nFiles created:")
    print(f"  1. {FIG1_PATH}")
    print(f"  2. {FIG2_PATH}")
    print(f"  3. {FIG3_PATH}")
    print(f"\nFigure specifications:")
    print(f"  - Resolution: {DPI} DPI (publication quality)")
    print(f"  - Format: PNG")
    print(f"  - Colorblind-friendly: Yes (Tol palette)")
    print(f"  - Font sizes: {FONT_TICK}-{FONT_TITLE} pt")
    print("\nReady for inclusion in paper!")
    print("="*60)


if __name__ == "__main__":
    main()
