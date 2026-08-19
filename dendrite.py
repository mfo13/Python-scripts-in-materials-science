"""
Simulation of Dendritic Growth by Phase-Field Approximation with Cellular Automata

Author: Marcelo Falcão de Oliveira
Affiliation: University of São Paulo (USP)
              São Carlos School of Engineering (EESC)
              Materials Engineering Department (SMM)
Contact: marcelo.falcao@usp.br

Description:
Simulates dendritic solidification kinetics of a pure undercooled metal using an accelerated 
Cellular Automata / Phase-Field approach with Numba JIT parallelization. Solves heat diffusion 
with Neumann boundary conditions, incorporates 4-fold crystalline anisotropy, Gibbs-Thomson 
curvature effects, and interfacial thermal noise to trigger secondary dendrite branching.

License: MIT License (https://opensource.org/licenses/MIT)
Purpose: Educational tool for materials science & dendritic solidification simulation.
Packages needed: numpy, matplotlib, numba

Acknowledgements:
Developed after many interactions with Gemini AI (Google).

August 2026
"""

import argparse
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from numba import njit, prange

# --- 1. Command-Line Argument Parser Setup ---
parser = argparse.ArgumentParser(
    description="2D Dendritic Solidification Simulation using Cellular Automata / Phase-Field method with Numba JIT.",
    formatter_class=argparse.RawTextHelpFormatter,
    epilog="""
    ==============================================================================
    PRESET COMMAND-LINE EXAMPLES (GROWTH REGIMES)
    ==============================================================================
    Copy and paste the commands below into your terminal to test different regimes:

    1. High and coarse ramification:
       python .\\dendrite.py --anisotropy 0 --K_base 50.0 --noise_level 0.05 --gamma_kappa 0 --alpha 2.5

    2. High and fine ramification:
       python .\\dendrite.py --anisotropy 0.25 --K_base 50.0 --noise_level 0.05 --gamma_kappa 0 --alpha 1.5 --L_eff 2

    3. Fine ramification and high mesh anisotropy:
       python .\\dendrite.py --anisotropy 0 --K_base 50.0 --noise_level 0.05 --gamma_kappa 0 --alpha 1.5 --L_eff 2

    4. Spherulitic-like growth:
       python .\\dendrite.py --anisotropy 0.1 --noise_level 0.05 --gamma_kappa 0.4
    ==============================================================================
    """
)

parser.add_argument(
    "--alpha", type=float, default=1.0,
    help="Thermal diffusivity coefficient (controls how fast heat dissipates)."
)
parser.add_argument(
    "--L_eff", type=float, default=1.2,
    help="Effective latent heat release during phase transformation."
)
parser.add_argument(
    "--K_base", type=float, default=20.0,
    help="Interface kinetics coefficient (controls interface growth speed)."
)
parser.add_argument(
    "--anisotropy", type=float, default=0.3,
    help="Strength of 4-fold crystalline anisotropy."
)
parser.add_argument(
    "--noise_level", type=float, default=0.3,
    help="Thermal noise amplitude at interface (triggers side-branching)."
)
parser.add_argument(
    "--gamma_kappa", type=float, default=0.01,
    help="Curvature penalty coefficient (Gibbs-Thomson capillarity effect)."
)
parser.add_argument(
    "--T_inf", type=float, default=-1.0,
    help="Initial undercooling temperature of the liquid phase."
)

args = parser.parse_args()

# --- 2. Numerical and Physical Parameters ---
N = 500                   # Grid size 500x500
dt = 0.012                # Time step
dx = 0.8                  # Spatial spacing

# Assign parsed values
alpha = args.alpha
L_eff = args.L_eff
K_base = args.K_base
anisotropy = args.anisotropy
noise_level = args.noise_level
gamma_kappa = args.gamma_kappa
T_inf = args.T_inf

T_m = 0.0                 # Melting temperature

# Some suggestions of command lines
# python .\dendrite.py --anisotropy 0 --K_base 50.0 --noise_level 0.05 --gamma_kappa 0 --alpha 1.5
# python .\dendrite.py --anisotropy 0 --K_base 50.0 --noise_level 0.05 --gamma_kappa 0 --alpha 1.5 --L_eff 2
# python .\dendrite.py --anisotropy 0.1 --noise_level 0.05 --gamma_kappa 0.4

# --- 3. C-Compiled Numerical Kernel via Numba ---
@njit(parallel=True, fastmath=True)
def step_simulation_numba(fs, T, dt, dx, alpha, L_eff, K_base, anisotropy, noise_level, gamma_kappa, T_m):
    N = fs.shape[0]
    fs_new = fs.copy()
    T_new = T.copy()
    
    # 1. Interfacial Growth and Latent Heat Release Update
    for i in prange(1, N - 1):
        for j in range(1, N - 1):
            if fs[i, j] < 1.0:
                # Solid neighbor count (Moore neighborhood)
                neighbors = (
                    0.5 * (fs[i-1, j-1] >= 1.0) + 1.0 * (fs[i-1, j] >= 1.0) + 0.5 * (fs[i-1, j+1] >= 1.0) +
                    1.0 * (fs[i, j-1] >= 1.0)   + 0.0                      + 1.0 * (fs[i, j+1] >= 1.0) +
                    0.5 * (fs[i+1, j-1] >= 1.0) + 1.0 * (fs[i+1, j] >= 1.0) + 0.5 * (fs[i+1, j+1] >= 1.0)
                )
                
                if neighbors > 0.0:
                    # Local solid fraction gradient
                    gx = (fs[i, j+1] - fs[i, j-1]) * 0.5
                    gy = (fs[i+1, j] - fs[i-1, j]) * 0.5
                    
                    angle = np.arctan2(gy, gx)
                    aniso_factor = 1.0 + anisotropy * np.cos(4.0 * angle)
                    
                    # Approximate curvature
                    kappa = (neighbors / 6.0) - 0.5
                    
                    # Local undercooling
                    delta_T = T_m - T[i, j] - gamma_kappa * kappa
                    if delta_T < 0.0:
                        delta_T = 0.0
                    
                    # Pseudo-random fluctuation
                    noise = 1.0 + noise_level * (np.random.random() - 0.5)
                    
                    # Growth rate
                    dfs = K_base * aniso_factor * noise * delta_T * (neighbors / 6.0) * dt
                    
                    fs_val = fs[i, j] + dfs
                    if fs_val > 1.0:
                        fs_val = 1.0
                    
                    actual_dfs = fs_val - fs[i, j]
                    fs_new[i, j] = fs_val
                    T_new[i, j] += L_eff * actual_dfs

    # 2. Thermal Diffusion (5-point Laplacian stencil)
    for i in prange(1, N - 1):
        for j in range(1, N - 1):
            lap_T = (T[i+1, j] + T[i-1, j] + T[i, j+1] + T[i, j-1] - 4.0 * T[i, j]) / (dx * dx)
            T_new[i, j] += alpha * lap_T * dt

    # Neumann Boundary Conditions (dT/dn = 0 at domain edges)
    for i in range(N):
        T_new[i, 0] = T_new[i, 1]           # Left boundary
        T_new[i, N-1] = T_new[i, N-2]       # Right boundary
        T_new[0, i] = T_new[1, i]           # Bottom boundary
        T_new[N-1, i] = T_new[N-2, i]       # Top boundary

    return fs_new, T_new


# --- 4. Field Initialization ---
T = np.full((N, N), T_inf, dtype=np.float64)
fs = np.zeros((N, N), dtype=np.float64)

center = N // 2
fs[center-1:center+2, center-1:center+2] = 1.0
T[center-1:center+2, center-1:center+2] = T_m

# --- 5. Matplotlib Figure Setup ---
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 5))

# Hide axes ticks and boundaries for cleaner visual output
ax1.axis('off')
ax2.axis('off')

im_fs = ax1.imshow(fs, cmap='Blues', origin='lower', vmin=0, vmax=1)
ax1.set_title("Solid Fraction ($f_s$)")
fig.colorbar(im_fs, ax=ax1, fraction=0.046, pad=0.04)

im_T = ax2.imshow(T, cmap='inferno', origin='lower')
ax2.set_title("Thermal Field ($T$)")
cbar_T = fig.colorbar(im_T, ax=ax2, fraction=0.046, pad=0.04)

# --- 6. High-Performance Animation Loop ---
def update(frame):
    global T, fs

    sub_steps = 40
    for _ in range(sub_steps):
        fs, T = step_simulation_numba(
            fs, T, dt, dx, alpha, L_eff, K_base, 
            anisotropy, noise_level, gamma_kappa, T_m
        )

    im_fs.set_data(fs)
    im_T.set_data(T)
    im_T.set_clim(vmin=np.min(T), vmax=np.max(T))
    
    current_step = frame * sub_steps
    ax1.set_title(f"Solid Fraction ($f_s$) - Step {current_step}")
    ax2.set_title(f"Thermal Field ($T$) - Step {current_step}")

    return im_fs, im_T

# Warm-up call to trigger JIT compilation before animation starts
fs, T = step_simulation_numba(fs, T, dt, dx, alpha, L_eff, K_base, anisotropy, noise_level, gamma_kappa, T_m)

ani = animation.FuncAnimation(fig, update, frames=300, interval=10, blit=False)
plt.tight_layout()
plt.show()