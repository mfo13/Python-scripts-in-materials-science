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

how_to_use = "\
Grain Growth with Dynamic Zener Pinning \n\
\n\
How to use: \n\
$ python grain_growth.py \n\
\n\
For help message: \n\
$ python grain_growth.py -h [--help] \n\
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
# SIMULATION CONFIGURATION
# ==========================================
GRID_SIZE = 500
SEEDS = 2000
INITIAL_STEPS = 500
STEPS_PER_FRAME = 2

# Particle parameters (Zener Pinning)
PARTICLE_FRACTION = 0.20  # fraction of boundary pixels converted to particles
PARTICLE_MOBILITY = 0.01  # fraction of matrix mobility (D_particle << D_matrix)

# Activation energy
Q_ENERGY = 3200.0

# Temperatures
T_MIN = -Q_ENERGY / 8.314 / np.log(0.1)
T_MAX = -Q_ENERGY / 8.314 / np.log(0.8)
T_INIT = (T_MAX + T_MIN) / 2

# Global state trackers
particles_enabled = False
particles_added = False

# ==========================================
# FUNCTIONS
# ==========================================

def initialize_grains(grid_size, num_seeds):
    """Initializes the grid with random seeds (IDs from 1 to num_seeds)."""
    grid = np.zeros((grid_size, grid_size), dtype=int)
    for i in range(1, num_seeds + 1):
        x, y = np.random.randint(0, grid_size, size=2)
        grid[x, y] = i

    return grid

def get_neighbors(grid):
    """Returns 8 Moore neighbors with periodic boundary conditions."""
    top    = np.roll(grid, -1, axis=0)
    bottom = np.roll(grid,  1, axis=0)
    left   = np.roll(grid, -1, axis=1)
    right  = np.roll(grid,  1, axis=1)
    top_left     = np.roll(top, -1, axis=1)
    top_right    = np.roll(top,  1, axis=1)
    bottom_left  = np.roll(bottom, -1, axis=1)
    bottom_right = np.roll(bottom,  1, axis=1)

    return [top, bottom, left, right, top_left, top_right, bottom_left, bottom_right]

def calculate_local_energy(grid, neighbors):
    """Calculates boundary energy E for each cell (number of mismatching neighbors)."""
    energy = np.zeros_like(grid, dtype=int)
    for neigh in neighbors:
        energy += (grid != neigh)

    return energy

def scatter_particles_on_boundaries(grid, fraction):
    """
    Scatters particles (ID = -1) ONLY along grain boundaries (where local energy > 0).
    Simulates preferential boundary precipitation.
    """
    neighbors = get_neighbors(grid)
    boundary_energy = calculate_local_energy(grid, neighbors)
    
    boundary_mask = (boundary_energy > 0)
    boundary_indices = np.flatnonzero(boundary_mask)
    
    num_particles = int(len(boundary_indices) * fraction)
    if num_particles > 0:
        chosen_indices = np.random.choice(boundary_indices, size=num_particles, replace=False)
        grid.flat[chosen_indices] = -1
        
    return grid

def remove_particles_from_grid(grid):
    """
    Dissolves particles (-1) by replacing them with the most frequent neighboring grain ID.
    Simulates dissolution of second-phase particles back into the matrix.
    """
    particle_mask = (grid == -1)
    if not np.any(particle_mask):
        return grid

    new_grid = grid.copy()
    neighbors = get_neighbors(grid)

    # For each particle pixel, pick a valid neighboring grain (> 0)
    for neigh in neighbors:
        valid_neigh = particle_mask & (neigh > 0)
        new_grid[valid_neigh] = neigh[valid_neigh]
        particle_mask = (new_grid == -1)
        if not np.any(particle_mask):
            break

    return new_grid

def calculate_mobility_probability(T, Q=Q_ENERGY, R=8.314):
    """Calculates jump probability based on Arrhenius kinetics."""
    return np.exp(-Q / (R * T))

def particle_swap_step(grid, mobility_prob):
    """
    Handles mobile particle (-1) dragging and Zener pinning.
    Strict condition: Swaps occur ONLY if particle is at a grain-grain interface
    and if energy strictly decreases (Delta_E < 0).
    """
    N = grid.shape[0]
    neighbors = get_neighbors(grid)
    particle_mask = (grid == -1)

    if not np.any(particle_mask):
        return grid

    has_multiple_grains = np.zeros((N, N), dtype=bool)
    for i in range(8):
        for j in range(i + 1, 8):
            g1 = neighbors[i]
            g2 = neighbors[j]
            has_multiple_grains |= ((g1 > 0) & (g2 > 0) & (g1 != g2))

    active_particles = particle_mask & has_multiple_grains
    
    random_draw = np.random.rand(N, N)
    active_particles &= (random_draw < (mobility_prob * PARTICLE_MOBILITY))

    if not np.any(active_particles):
        return grid

    new_grid = grid.copy()
    candidate_dir = np.random.randint(0, 8, size=(N, N))

    for k in range(8):
        swap_candidates = active_particles & (candidate_dir == k)
        if not np.any(swap_candidates):
            continue

        neigh_k = neighbors[k]
        valid_swap = swap_candidates & (neigh_k > 0)

        if np.any(valid_swap):
            curr_energy = calculate_local_energy(new_grid, neighbors)
            
            temp_grid = new_grid.copy()
            temp_grid[valid_swap] = neigh_k[valid_swap]
            
            prop_energy = calculate_local_energy(temp_grid, get_neighbors(temp_grid))
            delta_E = prop_energy - curr_energy

            accept = valid_swap & (delta_E < 0)
            new_grid[accept] = neigh_k[accept]

    return new_grid

def ca_growth_step(grid, mobility_prob):
    """
    Cellular Automata step handling space filling, particle swaps, and grain growth.
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
        new_grid = scatter_particles_on_boundaries(new_grid, PARTICLE_FRACTION)
        particles_added = True
        return new_grid

    # 3. Particle Swap/Drag Step (if particles exist)
    if particles_enabled and particles_added:
        new_grid = particle_swap_step(new_grid, mobility_prob)

    # 4. Curvature-Driven Grain Boundary Migration
    neighbors = get_neighbors(new_grid)
    current_energy = calculate_local_energy(new_grid, neighbors)
    interface_mask = (current_energy > 0) & (new_grid > 0)

    random_draw = np.random.rand(N, N)
    active_mask = interface_mask & (random_draw < mobility_prob)

    candidate_dir = np.random.randint(0, 8, size=(N, N))
    candidate_grid = np.zeros_like(new_grid)
    for k in range(8):
        candidate_grid[candidate_dir == k] = neighbors[k][candidate_dir == k]

    proposed_energy = calculate_local_energy(candidate_grid, neighbors)
    delta_E = proposed_energy - current_energy

    accept_change = active_mask & (delta_E <= 0) & (candidate_grid > 0)
    new_grid[accept_change] = candidate_grid[accept_change]

    return new_grid

# ==========================================
# INITIALIZATION
# ==========================================
current_T = T_INIT
mobility_prob = calculate_mobility_probability(T=current_T, Q=Q_ENERGY)
is_running = True
current_frame = 0
grid = initialize_grains(GRID_SIZE, SEEDS)
history_mcs = []
history_grains = []

# ==========================================
# INTERACTIVE ANIMATION & GUI SETUP
# ==========================================

# argparse to display help message and how to use
def parse_args():
    parser = argparse.ArgumentParser(
        description=how_to_use,
        formatter_class=argparse.RawTextHelpFormatter
        )
    return parser.parse_args()

parse_args()
    
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

img = ax1.imshow(grid, cmap=custom_gradient, interpolation='hamming', vmin=1, vmax=SEEDS)
ax1.set_title("Microstructure Evolution", fontsize=12)
ax1.axis('off')

# Kinetic curve panel
line, = ax2.plot([], [], color='firebrick', lw=2)
ax2.set_xlim(0, INITIAL_STEPS)
ax2.set_ylim(0, SEEDS + 10)
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

    unique_ids = np.unique(grid)
    active_grains = len(unique_ids[(unique_ids > 0)])

    history_mcs.append(current_frame)
    history_grains.append(active_grains)

    if current_frame >= ax2.get_xlim()[1]:
        ax2.set_xlim(0, current_frame + 200)
        ax2.figure.canvas.draw_idle()

    img.set_array(grid)
    line.set_data(history_mcs, history_grains)

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
    history_mcs.clear()
    history_grains.clear()
    grid = initialize_grains(GRID_SIZE, SEEDS)
    ax2.set_xlim(0, INITIAL_STEPS)
    line.set_data([], [])
    img.set_array(grid)
    fig.canvas.draw_idle()

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

# keyboard and canvas controls
btn_pause.on_clicked(toggle_pause)
btn_reset.on_clicked(reset_simulation)
btn_zener.on_clicked(toggle_zener)
slider_T.on_changed(update_temperature)
fig.canvas.mpl_connect('key_press_event', on_key_press)

# Animation execution
anim = animation.FuncAnimation(
    fig,
    update,
    interval=20,
    blit=False,
    repeat=True,
    cache_frame_data=False
)

plt.show()