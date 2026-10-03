"""
Simulation of Directional Solidification in a Binary Alloy (Microscopic CA / Phase Diagram Driven)

Author: Marcelo Falcão de Oliveira
Affiliation: University of São Paulo (USP)
             São Carlos School of Engineering (EESC)
             Materials Engineering Department (SMM)
Contact: marcelo.falcao@usp.br

Description: 
2D Cellular Automata (CA) model simulating directional solidification and 
dendritic growth in a binary alloy. The model explicitly couples interface 
kinetic supercooling with micro-scale solute diffusion in the liquid (solute 
rejection/segregation based on partition coefficient k) and 1D macro thermal 
conduction with latent heat release. Real-time visualization tracks microstructural 
evolution, local solid/liquid composition, thermal profile, and Constitutional 
Supercooling (T_real vs T_liquidus). 

License: MIT License (https://opensource.org/licenses/MIT)
Purpose: Educational tool for materials science & solidification simulation.
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
    description="Microscopic Solidification Simulation with Phase Diagram Driven CA.",
    formatter_class=argparse.RawTextHelpFormatter
)
parser.add_argument("--c0", type=float, default=0.1, help="Nominal alloy concentration (fraction).")
parser.add_argument("--k", type=float, default=0.15, help="Partition coefficient (c_S / c_L).")
parser.add_argument("--mL", type=float, default=500.0, help="Liquidus line slope |m_L| (K/fraction).")
parser.add_argument("--DL", type=float, default=3.0, help="Solute diffusivity in liquid.")
parser.add_argument("--alpha_1D", type=float, default=50.0, help="1D Thermal diffusivity in mold/metal.")
parser.add_argument("--L_eff", type=float, default=0.1, help="Effective latent heat release coefficient.")
parser.add_argument("--K_base", type=float, default=50.0, help="Interface kinetics coefficient.")
parser.add_argument("--G_initial", type=float, default=1.5, help="Initial thermal gradient dT/dx (K/grid length).")
parser.add_argument("--superheat", type=float, default=2.5, help="Initial liquid superheat above T_liquidus_0 (K).")
parser.add_argument("--noise_level", type=float, default=0.25, help="Thermal/kinetic fluctuation amplitude.")
parser.add_argument("--aniso_strength", type=float, default=0.5, help="Anisotropy strength delta.")
parser.add_argument("--fs_min", type=float, default=0.001, help="Minimum fs to render in microstructure plot.")

args = parser.parse_args()

# --- 2. Parameters ---
Nx, Ny = 300, 300          # Grid size
dt = 0.005                 # Time step
dx = 1.0                   # Spatial step

c0 = args.c0
k = args.k
mL = args.mL
DL = args.DL
alpha_1D = args.alpha_1D
L_eff = args.L_eff
K_base = args.K_base
G_initial = args.G_initial
superheat = args.superheat
noise_level = args.noise_level
aniso_strength = args.aniso_strength
fs_min = args.fs_min

T_m = 0.0                  # Pure solvent melting point

# Derived physical temperature values
T_liquidus_0 = T_m - mL * c0
T_initial = T_liquidus_0 + superheat
T_wall = T_liquidus_0 - G_initial * Nx

# --- 3. Pure Physical Kernel via Numba ---
@njit(parallel=True, fastmath=True)
def step_simulation_binary(fs, cL, cS, T, dt, dx, alpha_1D, DL, L_eff, K_base, k, mL, T_m, noise_level, aniso_strength, T_wall):
    Nx, Ny = fs.shape
    fs_new = fs.copy()
    cL_new = cL.copy()
    cS_new = cS.copy()
    T_new = T.copy()
    
    dfs_mean_x = np.zeros(Nx, dtype=np.float64)

    w_ortho = 1.0
    w_diag = 0.70710678118
    w_total = 4.0 * w_ortho + 4.0 * w_diag

    # 1. Solidification Kinetics
    for i in prange(1, Nx - 1):
        sum_dfs_col = 0.0
        T_local = T[i]

        cL_eq = (T_m - T_local) / mL
        cS_eq = k * cL_eq

        for j in range(Ny):
            fs_curr = fs[i, j]

            if fs_curr < 1.0:
                j_up = j + 1 if j < Ny - 1 else 0
                j_dn = j - 1 if j > 0 else Ny - 1

                n_weight = (
                    (fs[i-1, j_dn] > 0.5) * w_diag  + (fs[i-1, j] > 0.5) * w_ortho + (fs[i-1, j_up] > 0.5) * w_diag +
                    (fs[i,   j_dn] > 0.5) * w_ortho +                                (fs[i,   j_up] > 0.5) * w_ortho +
                    (fs[i+1, j_dn] > 0.5) * w_diag  + (fs[i+1, j] > 0.5) * w_ortho + (fs[i+1, j_up] > 0.5) * w_diag
                )

                if n_weight > 0.0:
                    dx_fs = (
                        (fs[i+1, j_up] + 2.0 * fs[i+1, j] + fs[i+1, j_dn]) -
                        (fs[i-1, j_up] + 2.0 * fs[i-1, j] + fs[i-1, j_dn])
                    ) * 0.125

                    dy_fs = (
                        (fs[i+1, j_up] + 2.0 * fs[i, j_up] + fs[i-1, j_up]) -
                        (fs[i+1, j_dn] + 2.0 * fs[i, j_dn] + fs[i-1, j_dn])
                    ) * 0.125

                    theta = np.arctan2(dy_fs, dx_fs) if (abs(dx_fs) > 1e-6 or abs(dy_fs) > 1e-6) else 0.0

                    aniso_factor = max(0.0, 1.0 + aniso_strength * np.cos(4.0 * theta))
                    noise = 1.0 + noise_level * (np.random.random() - 0.5)
                    
                    T_liquidus_local = T_m - mL * cL[i, j]
                    delta_T = T_liquidus_local - T_local
                    
                    if delta_T > 0.0:
                        dfs = K_base * aniso_factor * noise * delta_T * (n_weight / w_total) * dt
                        fs_val = min(1.0, fs_curr + dfs)
                        actual_dfs = fs_val - fs_curr

                        if actual_dfs > 0.0:
                            fs_new[i, j] = fs_val
                            cS_new[i, j] = (fs_curr * cS[i, j] + actual_dfs * cS_eq) / fs_val
                            
                            c_rejected = actual_dfs * (cL_eq - cS_eq)
                            cL_new[i, j] = min(1.0, cL_new[i, j] + c_rejected)
                            sum_dfs_col += actual_dfs

        dfs_mean_x[i] = sum_dfs_col / Ny

    # 2. Solute Diffusion in Liquid
    eps_fl = 0.01

    for i in prange(1, Nx - 1):
        for j in range(Ny):
            fs_c = fs[i, j]

            if fs_c < 1.0:
                j_up = j + 1 if j < Ny - 1 else 0
                j_dn = j - 1 if j > 0 else Ny - 1

                fl_c = 1.0 - fs_c
                fl_right = 1.0 - fs[i+1, j]
                fl_left  = 1.0 - fs[i-1, j]
                fl_up    = 1.0 - fs[i, j_up]
                fl_dn    = 1.0 - fs[i, j_dn]

                f_face_r = 0.5 * (fl_c + fl_right)
                f_face_l = 0.5 * (fl_c + fl_left)
                f_face_u = 0.5 * (fl_c + fl_up)
                f_face_d = 0.5 * (fl_c + fl_dn)

                flux_r = f_face_r * (cL[i+1, j] - cL[i, j])
                flux_l = f_face_l * (cL[i-1, j] - cL[i, j])
                flux_u = f_face_u * (cL[i, j_up] - cL[i, j])
                flux_d = f_face_d * (cL[i, j_dn] - cL[i, j])

                net_flux = flux_r + flux_l + flux_u + flux_d
                fl_effective = max(fl_c, eps_fl)

                cL_updated = cL_new[i, j] + (DL * dt / (dx * dx)) * (net_flux / fl_effective)
                cL_new[i, j] = min(1.0, max(0.0, cL_updated))

    # Solute Boundary Conditions
    for j in range(Ny):
        cL_new[0, j] = cL_new[1, j]
        cL_new[Nx-1, j] = cL_new[Nx-2, j]

    # 3. Thermal Diffusion Loop
    for i in range(1, Nx - 1):
        lap_T = (T[i+1] + T[i-1] - 2.0 * T[i]) / (dx * dx)
        T_new[i] += alpha_1D * lap_T * dt + L_eff * dfs_mean_x[i]

    T_new[0] = T_wall
    T_new[Nx-1] = T_new[Nx-2]

    return fs_new, cL_new, cS_new, T_new


# --- 4. Field Initialization ---
fs = np.zeros((Nx, Ny), dtype=np.float64)
cL = np.full((Nx, Ny), c0, dtype=np.float64)
cS = np.zeros((Nx, Ny), dtype=np.float64)

fs[0:3, :] = 1.0
cL[0:3, :] = k * c0
cS[0:3, :] = k * c0

x_coords = np.arange(Nx, dtype=np.float64)
T = T_liquidus_0 + G_initial * (x_coords - 3.0)
T[0] = T_wall

# --- 5. Matplotlib Figure Setup ---
fig, (ax1, ax3) = plt.subplots(1, 2, figsize=(14, 5))

# Left Panel
ax1.set_facecolor('white')
ax1.set_xlim(0, Nx)
ax1.set_ylim(0, Ny)
ax1.axis('off')

cS_masked = np.ma.masked_where(fs < fs_min, cS)
im_solid = ax1.imshow(
    cS_masked.T, cmap='viridis', origin='lower',
    extent=[0, Nx, 0, Ny], vmin=k*c0, vmax=k*c0*1.5, zorder=1, aspect='auto'
)
cbar_s = fig.colorbar(im_solid, ax=ax1, fraction=0.046, pad=0.04, location='left')
cbar_s.set_label(r"Solid Concentration $c_S$", rotation=90)

ax1_T = ax1.twinx()
T_min_plot = np.min(T)
T_max_plot = np.max(T)
T_margin = max(1.0, (T_max_plot - T_min_plot) * 0.05)
ax1_T.set_ylim(T_min_plot - T_margin, T_max_plot + T_margin)
ax1_T.axis('off')

x_coords_plot = np.arange(Nx)

# Original simple mean calculation for T_liquidus line
cL_mean_x = np.mean(cL, axis=1)
T_liq_profile = T_m - mL * cL_mean_x

line_T, = ax1_T.plot(x_coords_plot, T, 'k-', linewidth=2, label=r"$T_{real}$", zorder=10)
line_Tliq, = ax1_T.plot(x_coords_plot, T_liq_profile, 'r--', linewidth=2, label=r"$T_{liquidus}$", zorder=10)

lines = [line_T, line_Tliq]
labels = [l.get_label() for l in lines]
ax1.legend(lines, labels, loc='lower right', framealpha=0.8, facecolor='white')

# Right Panel
ax3.axis('off')
im_c = ax3.imshow(cL.T, cmap='viridis', origin='lower', extent=[0, Nx, 0, Ny], vmin=c0, vmax=c0*1.5, aspect='auto')
cbar_c = fig.colorbar(im_c, ax=ax3, fraction=0.046, pad=0.04)
cbar_c.set_label(r"Liquid Concentration $c_L$", rotation=270, labelpad=15)

# --- 6. Animation Loop ---
title_y_position = 0.99
global_step = 0

def update(frame):
    global fs, cL, cS, T, global_step

    sub_steps = 150
    for _ in range(sub_steps):
        fs, cL, cS, T = step_simulation_binary(
            fs, cL, cS, T, dt, dx, alpha_1D, DL, L_eff, K_base, k, mL, T_m, noise_level, aniso_strength, T_wall
        )

    global_step += sub_steps

    cS_masked = np.ma.masked_where(fs < fs_min, cS)
    im_solid.set_data(cS_masked.T)
    
    # Original simple calculation during animation
    cL_mean_x = np.mean(cL, axis=1)
    T_liq_profile = T_m - mL * cL_mean_x

    line_T.set_ydata(T)
    line_Tliq.set_ydata(T_liq_profile)

    im_c.set_data(cL.T)
    
    cS_max_curr = np.max(cS)
    cL_max_curr = np.max(cL)
    
    im_solid.set_clim(vmin=k * c0, vmax=max(k * c0 + 1e-5, cS_max_curr))
    im_c.set_clim(vmin=c0, vmax=max(c0 + 1e-5, cL_max_curr))
    
    mean_fs = np.mean(fs)
    if mean_fs >= 0.99:
        ani.event_source.stop()
        ax1.set_title(f"SOLIDIFICATION COMPLETE - Step {global_step}", y=title_y_position, color='red', fontweight='bold')
        ax3.set_title(f"Final Solute Field - Step {global_step}", y=title_y_position, color='red', fontweight='bold')
    else:
        ax1.set_title(f"Solid Concentration ($c_S$) & Temp - Step {global_step}", y=title_y_position)
        ax3.set_title(f"Liquid Solute Field ($c_L$) - Step {global_step}", y=title_y_position)

    return im_solid, line_T, line_Tliq, im_c

# Warm-up call
fs, cL, cS, T = step_simulation_binary(fs, cL, cS, T, dt, dx, alpha_1D, DL, L_eff, K_base, k, mL, T_m, noise_level, aniso_strength, T_wall)

ani = animation.FuncAnimation(fig, update, frames=400, interval=10, blit=False)
plt.tight_layout(rect=[0, 0, 1, 0.95])
plt.show()