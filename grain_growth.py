"""
Simulation of grain growth by Monte Carlo Cellular Automata with Dynamic Zener Pinning Toggle

Author: Marcelo Falcão de Oliveira
Affiliation: University of São Paulo (USP)
             São Carlos School of Engineering (EESC)
             Materials Engineering Department (SMM)
Contact: marcelo.falcao@usp.br

Description:
Simulates grain growth kinetics with Arrhenius temperature dependence. Includes an
interactive GUI toggle button to dynamically add/dissolve mobile Zener pinning particles (-1)
scattered along grain boundaries.

License: MIT License (https://opensource.org/licenses/MIT)
Purpose: Educational tool for materials science & grain growth simulation.
Packages needed: argparse, numpy, matplotlib

Acknowledgements:
Developed after many interactions with Gemini AI (Google).

August 2026
"""

help_message = "\
Grain Growth with Dynamic Zener Pinning \n\
\n\
Keyboard commands: \n\
space -> pause/play \n\
r -> reset \n\
z -> toggle Zener pinning \n\
"

import argparse
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.widgets import Button, Slider
from matplotlib.colors import LinearSegmentedColormap

# ==========================================
# SIMULATION CONFIGURATION (defaults)
# ==========================================
GRID_SIZE = 500
SEEDS = 2000
INITIAL_STEPS = 500
STEPS_PER_FRAME = 2

# Particle parameters (Zener Pinning)
PARTICLE_FRACTION = 0.10  # fraction of boundary pixels converted to particles
PARTICLE_MOBILITY = 0.05 # fraction of matrix mobility (D_particle << D_matrix)

# Activation energy
Q_ENERGY = 3200.0

# Global state trackers
particles_enabled = False
particles_added = False

# ==========================================
# FUNCTIONS
# ==========================================

def initialize_grains(grid_size, num_seeds):
    """
    Initializes the grid with unique random seeds (IDs from 1 to num_seeds)
    without replacement, ensuring exact seed count without collisions.
    """
    grid = np.zeros((grid_size, grid_size), dtype=int)
    
    # Select unique flat indices across the grid to avoid seed collisions
    total_pixels = grid_size * grid_size
    chosen_indices = np.random.choice(total_pixels, size=num_seeds, replace=False)
    
    # Assign grain IDs sequentially to the selected unique locations
    grid.flat[chosen_indices] = np.arange(1, num_seeds + 1)

    return grid

def get_neighbors(grid):
    """
    Returns an 8-neighbor 3D numpy array of shape (8, N, N) with periodic 
    boundary conditions using np.pad with wrap mode. Centralizes padded slicing.
    """
    padded = np.pad(grid, pad_width=1, mode='wrap')
    return np.stack([
        padded[:-2, 1:-1],  # 0: Top
        padded[2:,  1:-1],  # 1: Bottom
        padded[1:-1, :-2],  # 2: Left
        padded[1:-1, 2:],   # 3: Right
        padded[:-2, :-2],   # 4: Top-Left
        padded[:-2, 2:],    # 5: Top-Right
        padded[2:,  :-2],   # 6: Bottom-Left
        padded[2:,  2:]     # 7: Bottom-Right
    ])

def calculate_local_energy(grid):
    """
    Calculates boundary energy E for each cell (number of mismatching neighbors, 0 to 8)
    by stacking neighbor slices and performing a vectorized sum along axis 0.
    """
    neighbors_stack = get_neighbors(grid)
    
    # Broadcast comparison (grid vs all 8 slices) and sum True flags along axis 0
    return np.sum(grid != neighbors_stack, axis=0)

def scatter_particles_on_boundaries(grid, fraction):
    """
    Scatters particles (ID = -1) ONLY along grain boundaries (where local energy > 0).
    Simulates preferential boundary precipitation.
    """
    # Calculate local energy directly using the optimized 2D padded slicing
    boundary_energy = calculate_local_energy(grid)
    
    # Identify indices corresponding to grain boundaries
    boundary_indices = np.flatnonzero(boundary_energy > 0)
    
    num_particles = int(len(boundary_indices) * fraction)
    #print("Initial particles scattered:", num_particles) # debug
    if num_particles > 0:
        chosen_indices = np.random.choice(boundary_indices, size=num_particles, replace=False)
        grid.flat[chosen_indices] = -1
        
    return grid

def remove_particles_from_grid(grid):
    """
    Dissolves particles (-1) by replacing them with the first valid neighboring
    grain ID (> 0) using fully vectorized 3D array indexing (zero Python loops).
    """
    particle_mask = (grid == -1)
    if not np.any(particle_mask):
        return grid

    new_grid = grid.copy()

    neighbors_stack = get_neighbors(grid)

    # Mask of valid grain IDs (> 0) across all 8 neighbors
    valid_mask = (neighbors_stack > 0)

    # Find the index of the first valid grain ID along axis 0
    first_valid_idx = np.argmax(valid_mask, axis=0)

    # Extract the grain ID corresponding to the first valid neighbor
    # Advanced 3D indexing replaces all particle sites in a single operation
    rows, cols = np.indices(grid.shape)
    selected_grains = neighbors_stack[first_valid_idx, rows, cols]

    # Assign selected grain IDs only to particle locations
    new_grid[particle_mask] = selected_grains[particle_mask]

    return new_grid

def calculate_mobility_probability(T, Q=Q_ENERGY, R=8.314):
    """Calculates jump probability based on Arrhenius kinetics."""
    return np.exp(-Q / (R * T))

def particle_swap_step(grid, mobility_prob):
    """
    Handles mobile particle (-1) dragging and Zener pinning using fully vectorized
    NumPy operations with sparse coordinate indexing for energy updates.
    Ensures strict 1-to-1 pixel conservation without Python loops or global grid copies.
    """
    N = grid.shape[0]
    particle_mask = (grid == -1)
        
    if not np.any(particle_mask):
        return grid

    neighbors_stack = get_neighbors(grid)

    # --- FRONT 1: Fast Multi-Grain Boundary Detection ---
    valid_grain_mask = (neighbors_stack > 0)
    grain_count = np.sum(valid_grain_mask, axis=0)
    
    masked_grains = np.where(valid_grain_mask, neighbors_stack, -1)
    max_grain = np.max(masked_grains, axis=0)
    
    masked_grains_for_min = np.where(valid_grain_mask, neighbors_stack, np.inf)
    min_grain = np.min(masked_grains_for_min, axis=0)

    has_multiple_grains = (grain_count >= 2) & (max_grain != min_grain)
    # ----------------------------------------------------

    active_particles = particle_mask & has_multiple_grains
    random_draw = np.random.rand(N, N)
    active_particles &= (random_draw < (mobility_prob * args.particle_mobility))

    if not np.any(active_particles):
        return grid

    new_grid = grid.copy()

    # Random movement directions for active particles
    candidate_dir = np.random.randint(0, 8, size=(N, N))

    # Offsets for standard 8-neighbor directions (0 to 7)
    shifts = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]

    # Process each direction in vectorized batching
    for k in range(8):
        swap_candidates = active_particles & (candidate_dir == k)
        if not np.any(swap_candidates):
            continue

        neigh_k = neighbors_stack[k]
        valid_swap = swap_candidates & (neigh_k > 0)

        if np.any(valid_swap):
            # --- FRONT 2 OPTIMIZATION: Sparse Local Delta E Evaluation ---
            # Get flat indices of candidate active particles (A) and target grain sites (B)
            flat_indices_A = np.flatnonzero(valid_swap)
            
            shift_r, shift_c = shifts[k]
            # Convert flat indices to 2D coordinates (rows, cols)
            rows_A, cols_A = np.unravel_index(flat_indices_A, (N, N))
            
            # Target B coordinates under periodic boundary conditions
            rows_B = (rows_A + shift_r) % N
            cols_B = (cols_A + shift_c) % N
            flat_indices_B = np.ravel_multi_index((rows_B, cols_B), (N, N))

            # Current IDs at site A (-1) and site B (grain_id)
            grain_ids_B = new_grid.flat[flat_indices_B]

            # Extract 8 neighbors specifically for candidates A and B from stack
            # Shape of stack_A / stack_B: (8, num_candidates)
            stack_A = neighbors_stack[:, rows_A, cols_A]
            stack_B = neighbors_stack[:, rows_B, cols_B]

            # Calculate initial local boundary energy at sites A and B
            # Energy = number of neighbors with a different ID
            E_A_init = np.sum(stack_A != -1, axis=0)
            E_B_init = np.sum(stack_B != grain_ids_B, axis=0)

            # Proposed local energy after swapping values (A gets grain_id, B gets -1)
            E_A_prop = np.sum(stack_A != grain_ids_B, axis=0)
            E_B_prop = np.sum(stack_B != -1, axis=0)

            delta_E_local = (E_A_prop + E_B_prop) - (E_A_init + E_B_init)

            # Filter candidates where energy decreases (delta_E < 0)
            accept_sparse = (delta_E_local < 0)
            
            if np.any(accept_sparse):
                # Map accepted sparse choices back to boolean mask for execution
                accept_mask = np.zeros((N, N), dtype=bool)
                accept_mask.flat[flat_indices_A[accept_sparse]] = True

                # Target must currently hold a valid grain (> 0)
                target_is_grain = np.roll(np.roll(new_grid > 0, -shift_r, axis=0), -shift_c, axis=1)
                safe_swap = accept_mask & target_is_grain

                if np.any(safe_swap):
                    # Execute 2-way vectorized swap preserving 1-to-1 particle count
                    new_grid[safe_swap] = neigh_k[safe_swap]
                    
                    target_mask = np.roll(np.roll(safe_swap, shift_r, axis=0), shift_c, axis=1)
                    new_grid[target_mask] = -1
            # -------------------------------------------------------------

    return new_grid

def ca_growth_step(grid, mobility_prob):
    """
    Cellular Automata step handling space filling, particle swaps, and grain growth.
    Fully vectorized and performance-optimized.
    """
    global particles_added, particles_enabled
    N = grid.shape[0]
    new_grid = grid.copy()
    neighbors = get_neighbors(grid)

    # 1. Initial Growth Phase (filling unassigned space '0')
    unassigned = (grid == 0)
    if np.any(unassigned):
        for neigh in neighbors:
            expansion_mask = unassigned & (neigh > 0)
            new_grid[expansion_mask] = neigh[expansion_mask]
            unassigned = (new_grid == 0)
        return new_grid

    # 2. Scatter particles if Zener pinning option is enabled
    if particles_enabled and not particles_added:
        new_grid = scatter_particles_on_boundaries(new_grid, args.particle_fraction)
        particles_added = True
        return new_grid

    # 3. Particle Swap/Drag Step (if particles exist)
    if particles_enabled and particles_added:
        new_grid = particle_swap_step(new_grid, mobility_prob)

    # 4. Curvature-Driven Grain Boundary Migration (Optimized)
    neighbors_arr = np.array(get_neighbors(new_grid))  # Shape: (8, N, N)
    
    # Fast sum of the current energy
    current_energy = np.sum(neighbors_arr != new_grid, axis=0)
    
    # Only contours (>0) with active probability
    active_mask = (current_energy > 0) & (new_grid > 0) & (np.random.rand(N, N) < mobility_prob)

    if not np.any(active_mask):
        return new_grid

    # Selection of candidate neighbours without using np.indices (take_along_axis)
    candidate_dir = np.random.randint(0, 8, size=(N, N))
    candidate_grid = np.take_along_axis(neighbors_arr, candidate_dir[None, ...], axis=0)[0]

    # Filters valid candidates (avoids propagate -1 or swap null ID)
    valid_candidates = active_mask & (candidate_grid > 0)

    if not np.any(valid_candidates):
        return new_grid

    # Calculates delta_E only for valid pixels (Sparse Evaluation)
    # 2D subarray extraction (8, num_valid)
    valid_neighbors = neighbors_arr[:, valid_candidates]
    valid_proposed = candidate_grid[valid_candidates]
    
    E_init = current_energy[valid_candidates]
    E_prop = np.sum(valid_neighbors != valid_proposed, axis=0)
    
    delta_E = E_prop - E_init

    # Implementation of valid swaps
    accept_indices = valid_candidates.copy()
    accept_indices[valid_candidates] = (delta_E <= 0)
    
    new_grid[accept_indices] = candidate_grid[accept_indices]

    return new_grid

# ==========================================
# INTERACTIVE ANIMATION & GUI SETUP
# ==========================================

def parse_args():
    parser = argparse.ArgumentParser(
        description = help_message,
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument("-s", "--seeds", type=int, default=SEEDS, help="Number of initial grains (default: %(default)s)")
    parser.add_argument("-f", "--particle-fraction", type=float, default=PARTICLE_FRACTION, help="Particle fraction in the contours (default: %(default)s)")
    parser.add_argument("-m", "--particle-mobility", type=float, default=PARTICLE_MOBILITY, help="Particle mobility (default: %(default)s)")
    return parser.parse_args()

args = parse_args()

# INITIALIZATION
# ----------------
T_MIN = - Q_ENERGY / 8.314 / np.log(0.1)
T_MAX = - Q_ENERGY / 8.314 / np.log(0.8)
T_INIT = (T_MAX + T_MIN) / 2
current_T = T_INIT
mobility_prob = calculate_mobility_probability(T=current_T, Q=Q_ENERGY)
is_running = True
current_frame = 0
grid = initialize_grains(GRID_SIZE, args.seeds)
history_mcs = []
history_grains = []
    
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 7))
plt.subplots_adjust(left=0.04, right=0.96, top=0.92, bottom=0.14, wspace=0.15)

title_text = fig.suptitle(
    f"Grain Growth Simulation (T = {current_T:.0f} K / {current_T-273.15:.0f} °C)",
    fontsize=14, fontweight='bold', y=0.99
)

# Custom continuous colormap for grains
grain_colors = ["#eefa48", "#fbd75d", "#f9b96a", "#f59a6f", "#ee7a75", "#df5c82", 
                "#c84098", "#9e37ac", "#653baa", "#313a8c", "#1A3A6B", "#304c67", 
                "#474220", "#4E2A18", "#622125", "#7a1e4b", "#7c387c", "#7457a0", 
                "#6b72bb", "#628dc8", "#5da8c9", "#61c1c4", "#80d8b7", "#a9eca0", "#d5ff76"]

custom_gradient = LinearSegmentedColormap.from_list("zener_cmap", grain_colors)
custom_gradient.set_under('#ffffff') # particle color

# Added animated=True for blit optimization and fast nearest interpolation
img = ax1.imshow(grid, cmap=custom_gradient, interpolation='none', vmin=1, vmax=args.seeds, animated=True)
ax1.set_title("Microstructure Evolution", fontsize=12)
ax1.axis('off')

# Kinetic curve panel (Added animated=True)
line, = ax2.plot([], [], color='firebrick', lw=2, animated=True)
ax2.set_xlim(0, INITIAL_STEPS)
ax2.set_ylim(0, args.seeds + 10)
ax2.set_xlabel("Monte Carlo Steps (MCS)", fontsize=11)
ax2.set_ylabel("Remaining Active Grains N(t)", fontsize=11)
ax2.set_title("Grain Annihilation Curve", fontsize=12)
ax2.grid(True, linestyle='--', alpha=0.6)

# Update frame function
def update(frame):
    global grid, current_frame, is_running

    if not is_running:
        return img, line

    for _ in range(STEPS_PER_FRAME):
        current_frame += 1
        grid = ca_growth_step(grid, mobility_prob)

    # Sample history data periodically instead of every single step
    if current_frame % 2 == 0:
        # Fast grain count using np.bincount instead of np.unique
        positive_mask = grid[grid > 0]
        active_grains = np.count_nonzero(np.bincount(positive_mask.ravel())) if positive_mask.size > 0 else 0
        
        history_mcs.append(current_frame)
        history_grains.append(active_grains)

        # Redraw background only when expanding axis limit
        if current_frame >= ax2.get_xlim()[1]:
            ax2.set_xlim(0, current_frame + 200)
            ax2.figure.canvas.draw_idle()

        img.set_array(grid)
        line.set_data(history_mcs, history_grains)

        #if particles_added:
        #    print("Current particle count:", np.sum(grid == -1)) # debug

    return img, line

# Controls Layout
ax_pause   = plt.axes([0.10, 0.03, 0.08, 0.045])
ax_reset   = plt.axes([0.19, 0.03, 0.08, 0.045])
ax_zener   = plt.axes([0.28, 0.03, 0.12, 0.045])
ax_slider  = plt.axes([0.55, 0.035, 0.35, 0.03])

btn_pause = Button(ax_pause, 'Pause', color='lightgray', hovercolor='0.9')
btn_reset = Button(ax_reset, 'Reset', color='lightgray', hovercolor='0.9')
btn_zener = Button(ax_zener, 'Zener: OFF', color='lightgray', hovercolor='0.9')
slider_T  = Slider(ax_slider, 'Temp (K)', T_MIN, T_MAX, valinit=T_INIT, valfmt='%1.0f K')

# Controls functions
def toggle_pause(event=None):
    global is_running
    is_running = not is_running
    btn_pause.label.set_text("Play" if not is_running else "Pause")
    fig.canvas.draw_idle()

def reset_simulation(event=None):
    global grid, current_frame, history_mcs, history_grains, particles_added, particles_enabled
    current_frame = 0
    particles_added = False
    particles_enabled = False
    btn_zener.label.set_text("Zener: OFF")
    btn_zener.color = 'lightgray'
    
    # Clear data arrays
    history_mcs.clear()
    history_grains.clear()
    
    # Reset grid and line data
    grid = initialize_grains(GRID_SIZE, args.seeds)
    line.set_data([], [])
    img.set_array(grid)
    
    # Reset X axis limits
    ax2.set_xlim(0, INITIAL_STEPS)
    
    # Force immediate full redraw to flush blitting background cache
    fig.canvas.draw()

def toggle_zener(event=None):
    global particles_enabled, particles_added, grid
    particles_enabled = not particles_enabled
    
    if particles_enabled:
        btn_zener.label.set_text("Zener: ON")
        btn_zener.color = 'lightgreen'
    else:
        btn_zener.label.set_text("Zener: OFF")
        btn_zener.color = 'lightgray'
        # Dissolve particles back into grain matrix when turning Zener OFF
        grid = remove_particles_from_grid(grid)
        particles_added = False
        img.set_array(grid)

    fig.canvas.draw_idle()

def update_temperature(val):
    global current_T, mobility_prob
    current_T = slider_T.val
    mobility_prob = calculate_mobility_probability(T=current_T, Q=Q_ENERGY)
    title_text.set_text(f"Grain Growth Simulation (T = {current_T:.0f} K / {current_T-273.15:.0f} °C)")
    fig.canvas.draw_idle()

def on_key_press(event):
    if event.key == ' ':       # space bar to pause/play
        toggle_pause()
    elif event.key == 'r':     # r key to reset
        reset_simulation()
    elif event.key == 'z':     # z key to toggle Zener pinning
        toggle_zener()

# Keyboard and canvas controls
btn_pause.on_clicked(toggle_pause)
btn_reset.on_clicked(reset_simulation)
btn_zener.on_clicked(toggle_zener)
slider_T.on_changed(update_temperature)
fig.canvas.mpl_connect('key_press_event', on_key_press)

# Animation execution (blit enabled and interval optimized)
anim = animation.FuncAnimation(
    fig,
    update,
    interval=1,
    blit=True,
    repeat=True,
    cache_frame_data=False
)

plt.show()