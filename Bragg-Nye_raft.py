"""
Simulation of the classical bubble raft experiment created by 
Sir Lawrence Bragg and John Nye in 1947 

Author: Marcelo Falcão de Oliveira
Affiliation: University of São Paulo (USP)
             São Carlos School of Engineering (EESC)
             Materials Engineering Department (SMM)
Contact: marcelo.falcao@usp.br

Description:
It ilustrates the dislocations' motions and interactions in a "crystalline" bubble raft. 
Many phenomena can be observed like discolation birth, slip, anyhilation, 
interaction with vacancies, grain contours and other dislocations, climbing and bouncing back. 
Other phenomena can also be observed like grain growth and cracking.

License:
MIT License (https://opensource.org/licenses/MIT)

Purpose:
Educational tool for demonstrating the classical Bragg-Nye bubble raft experiment.

Packages needed:
numpy, scipy, argparse, matplotlib

Usage:

$python Bragg-Nye_raft.py [-h] [-g {one-by-one,all-at-once}] [--n-target N_TARGET] 
                            [--relax-steps RELAX_STEPS] [--compress-velocity COMPRESS_VELOCITY]

Options:
  -h, --help            show help message and exit
  -g {one-by-one,all-at-once}, --bubble-generation {one-by-one,all-at-once}
                        How bubbles are created (default: one-by-one)
  --n-target N_TARGET   How many bubbles (defaults: 550 for one-by-one, 4000 for all-at-once)
  --relax-steps RELAX_STEPS
                        Relaxation steps after bubble generation and after box opening (default: 1000).
  --compress-velocity COMPRESS_VELOCITY
                        Wall velocity in A units per step (default: 0.01)


Date: July, 2026
Version: 1.0

Note:
The script was entirely developed after many interactions with the AI (Claude, Anthropic, 2026).

"""

""" Packages """
import numpy as np
from scipy.spatial import cKDTree
import argparse
import matplotlib.pyplot as plt
import matplotlib.animation as animation

"""---------------------------------------------------------------------------------
FIRST BLOCK - physics engine

Lennard-Jones potential with a tanh-based sigmoid saturation on the force magnitude, 
preventing excessively large forces at close range. 
Vectorized grid-based neighbor search
with a cached Verlet list (skin margin) to avoid rebuilding neighbors every step.
Verlet velocity integrator with internal friction. Velocity rescaling
for temperature control.
Bond-orientational order parameter (psi6) to identify dislocations and
grain boundaries.

-----------------------------------------------------------------------------------"""
A = 1.0                        # lattice parameter
N_EXP = 12                     # repulsive exponent
M_EXP = 6                      # atractive exponent

# C = (n/(n-m)) * (n/m)^(m/(n-m))  -- guarantees that EPS is the well depth
_LJ_C = (N_EXP / (N_EXP - M_EXP)) * (N_EXP / M_EXP) ** (M_EXP / (N_EXP - M_EXP))
# sigma = A / (n/m)^(1/(n-m))      -- guarantees that the minimum r = A
SIGMA = A / (N_EXP / M_EXP) ** (1.0 / (N_EXP - M_EXP))

EPS = 5.0                      # well depth
CUTOFF = 1.5 * A               # cutoff radius for interaction calculations
MASS = 1.0                     # bubble mass (reduced units)

F_MAX = 110.0                  # limiting force for tanh-sigmoid saturation


def compute_forces_from_pairs(pos, pairs, eps=EPS, sigma=SIGMA, cutoff=CUTOFF,
                               n_exp=N_EXP, m_exp=M_EXP, f_max=F_MAX):
    forces = np.zeros_like(pos)
    if len(pairs) == 0:
        return forces

    d = pos[pairs[:, 0]] - pos[pairs[:, 1]]
    r = np.linalg.norm(d, axis=1)

    within = r <= cutoff
    if not np.any(within):
        return forces
    pairs, d, r = pairs[within], d[within], r[within]
    r = np.clip(r, 1e-3, None)

    if np.isscalar(sigma):
        sigma_pair = sigma
    else:
        sigma = np.asarray(sigma)
        sigma_pair = 0.5 * (sigma[pairs[:, 0]] + sigma[pairs[:, 1]])

    sr_m = (sigma_pair / r) ** m_exp
    sr_n = (sigma_pair / r) ** n_exp
    fmag = (_LJ_C * eps / r) * (n_exp * sr_n - m_exp * sr_m)
    fmag = f_max * np.tanh(fmag / f_max)
    fvec = (fmag / r)[:, None] * d

    np.add.at(forces, pairs[:, 0], fvec)
    np.add.at(forces, pairs[:, 1], -fvec)
    return forces


def compute_forces(pos, eps=EPS, sigma=SIGMA, cutoff=CUTOFF, n_exp=N_EXP, m_exp=M_EXP, f_max=F_MAX):
    tree = cKDTree(pos)
    pairs = tree.query_pairs(r=cutoff, output_type="ndarray")
    return compute_forces_from_pairs(pos, pairs, eps=eps, sigma=sigma, cutoff=cutoff,
                                      n_exp=n_exp, m_exp=m_exp, f_max=f_max)


def build_neighbor_pairs_grid(pos, r_search):
    n = len(pos)
    if n < 2:
        return np.zeros((0, 2), dtype=int)

    box_min = pos.min(axis=0)
    cell_size = r_search
    ix = np.floor((pos[:, 0] - box_min[0]) / cell_size).astype(int)
    iy = np.floor((pos[:, 1] - box_min[1]) / cell_size).astype(int)
    ny_cells = int(iy.max()) + 1
    cell_id = ix * ny_cells + iy

    order = np.argsort(cell_id, kind="stable")
    sorted_cell_id = cell_id[order]
    unique_ids, start_idx = np.unique(sorted_cell_id, return_index=True)
    end_idx = np.append(start_idx[1:], n)
    cell_range = {int(cid): (int(s), int(e)) for cid, s, e in zip(unique_ids, start_idx, end_idx)}

    pairs_i, pairs_j = [], []
    for cid, (s, e) in cell_range.items():
        idx_here = order[s:e]
        cx, cy = divmod(cid, ny_cells)

        if len(idx_here) > 1:
            ii, jj = np.triu_indices(len(idx_here), k=1)
            pairs_i.append(idx_here[ii])
            pairs_j.append(idx_here[jj])

        for dx in (-1, 0, 1):
            for dy in (-1, 0, 1):
                if dx == 0 and dy == 0:
                    continue
                ncx, ncy = cx + dx, cy + dy
                if ncx < 0 or ncy < 0 or ncy >= ny_cells:
                    continue
                ncid = ncx * ny_cells + ncy
                if ncid <= cid or ncid not in cell_range:
                    continue
                ns, ne = cell_range[ncid]
                idx_other = order[ns:ne]
                ii, jj = np.meshgrid(idx_here, idx_other, indexing="ij")
                pairs_i.append(ii.ravel())
                pairs_j.append(jj.ravel())

    if not pairs_i:
        return np.zeros((0, 2), dtype=int)
    return np.stack([np.concatenate(pairs_i), np.concatenate(pairs_j)], axis=1)


def build_verlet_list(pos, cutoff=CUTOFF, skin=0.25 * A):
    r_verlet = cutoff + skin
    candidates = build_neighbor_pairs_grid(pos, r_verlet)
    if len(candidates) == 0:
        return candidates
    d = pos[candidates[:, 0]] - pos[candidates[:, 1]]
    r = np.linalg.norm(d, axis=1)
    return candidates[r <= r_verlet]


def verlet_step(pos, vel, forces, dt, mass=MASS, fixed_mask=None,
                 eps=EPS, sigma=SIGMA, cutoff=CUTOFF, gamma=0.0, f_max=F_MAX,
                 force_fn=None):
    if force_fn is None:
        force_fn = lambda p: compute_forces(p, eps=eps, sigma=sigma, cutoff=cutoff, f_max=f_max)

    if fixed_mask is None:
        fixed_mask = np.zeros(len(pos), dtype=bool)
    free = ~fixed_mask

    accel = forces / mass - gamma * vel / mass
    new_pos = pos.copy()
    new_pos[free] = pos[free] + vel[free] * dt + 0.5 * accel[free] * dt ** 2

    new_forces = force_fn(new_pos)

    new_vel = vel.copy()
    v_meio = vel[free] + 0.5 * dt * accel[free]
    denom = 1.0 + 0.5 * dt * gamma / mass
    new_vel[free] = (v_meio + 0.5 * dt * new_forces[free] / mass) / denom

    return new_pos, new_vel, new_forces


def rescale_velocities(vel, fixed_mask, target_ke_per_particle, mass=MASS):
    free = ~fixed_mask
    n_free = free.sum()
    if n_free == 0:
        return vel

    current_ke = 0.5 * mass * np.sum(vel[free] ** 2)
    target_ke = target_ke_per_particle * n_free

    new_vel = vel.copy()
    if current_ke > 1e-12:
        scale = np.sqrt(target_ke / current_ke)
        new_vel[free] = vel[free] * scale
    return new_vel


BOND_CUTOFF = 1.3 * A  # separates first layer (r~A) from second neighbours (r~1.73*A)


def compute_psi6(pos, pairs, bond_cutoff=BOND_CUTOFF):
    """
    6-fold orientational order parameter, |psi6|, for each
    particle — the classic measure of "how hexagonal" the local
    neighborhood is in a 2D triangular lattice. Close to 1 = perfectly
    hexagonal environment; drops near dislocations and grain boundaries.

        psi6(j) = (1/N_j) * sum_k exp(i * 6 * theta_jk)

    where the sum is over the FIRST-SHELL neighbors k of j, and
    theta_jk is the angle of the j-k bond.

    Reuses already calculated pairs (e.g., the Verlet list used
    for force calculations) instead of rebuilding the neighborhood
    from scratch — it simply filters by actual distance <= bond_cutoff,
    which is tighter than the force cutoff (capturing only the 1st
    shell, not everyone within the potential's range).

    Implementation detail: for a pair (i,j), the bond angle
    viewed from i is theta, and viewed from j is theta+pi. Since
    exp(i*6*(theta+pi)) == exp(i*6*theta) (6*pi is a multiple of 2*pi),
    the same complex contribution enters the sum for both sides of
    the pair — there is no need to calculate the angle twice.

    """
    n = len(pos)
    if len(pairs) == 0:
        return np.zeros(n)

    d = pos[pairs[:, 0]] - pos[pairs[:, 1]]
    r = np.linalg.norm(d, axis=1)
    mask = r <= bond_cutoff
    if not np.any(mask):
        return np.zeros(n)
    pairs_b, d_b = pairs[mask], d[mask]

    theta = np.arctan2(d_b[:, 1], d_b[:, 0])
    contrib = np.exp(1j * 6 * theta)

    psi6_sum = np.zeros(n, dtype=complex)
    counts = np.zeros(n, dtype=int)
    np.add.at(psi6_sum, pairs_b[:, 0], contrib)
    np.add.at(psi6_sum, pairs_b[:, 1], contrib)
    np.add.at(counts, pairs_b[:, 0], 1)
    np.add.at(counts, pairs_b[:, 1], 1)

    psi6 = np.zeros(n)
    has_neighbors = counts > 0
    psi6[has_neighbors] = np.abs(psi6_sum[has_neighbors] / counts[has_neighbors])
    return psi6

"""-----------------------------------

SECOND BLOCK - bubble raft simulator

--------------------------------------"""

DT = 0.02                           # time step (dimensionless)
STEPS_PER_FRAME = 4                 # calculated steps between each frame redraw
N_RESCALE = 20                      # steps between velocity rescaling
TARGET_KE_PER_PARTICLE = 0.02       # target kinetic energy (temperature)
GAMMA_FRICTION = 2.0                # internal friction factor

VERLET_SKIN = 0.5 * A               # skin distance above cutoff to build Verlet's list
VERLET_REBUILD_INTERVAL = 200       # steps before rebuilds the Verlet's list for one-by-one

BUBBLE_RADIUS = 0.5 * A             # visual bubble radius

WALL_SPACING = A / 3                # distance between point in the walls
WALL_PAD = A / 3                    # distance between walls and box frame

_rng = np.random.default_rng(42)

N_TARGET_DEFAULT = 550              # default number of bubbles for one-by-one
SPAWN_INTERVAL = 15                 # steps between spawn of new bubble

BIRTH_JITTER = 0.0005 * A           # jitter to oscilate point of birth around the calculated centroid

TRIANGLE_TOLERANCE = 0.20           # tollerance regarding the sides of an equilateral triangle
MAX_TRIANGLE_ATTEMPTS = 50          # mas attempts to find an acceptable triangle of 3 neighbors

N_BUBBLES_DEFAULT = 4000            # default number of bubbles for all-at-once
MIN_SEPARATION = 0.05 * A           # minimum distance for spawn a new bubble
AREA_FACTOR = 1.0                          # final occupancy factor regarding a perfect lattice
VERLET_REBUILD_INTERVAL_ALL_AT_ONCE = 5    # steps before rebuilds the Verlet's list for all-at-once

RELAX_STEPS = 1000                         # default relaxation steps
COMPRESS_VELOCITY_DEFAULT = 0.01 * A       # velocity of the moving wall in units of A per step
VERLET_REBUILD_INTERVAL_COMPRESSION = 10   # steps before rebuilds the Verlet's list for compression


def box_side(n_target, area_factor=1.0):
    hex_area_per_bubble = (np.sqrt(3) / 2) * A ** 2
    box_area = n_target * hex_area_per_bubble * area_factor
    return np.sqrt(box_area)

def build_walls(box_side, spacing=WALL_SPACING, pad=WALL_PAD):
    lo, hi = -pad, box_side + pad
    bottom, top, left, right = [], [], [], []
    x = lo
    while x <= hi + 1e-9:
        bottom.append((x, lo))
        top.append((x, hi))
        x += spacing
    y = lo + spacing
    while y <= hi - spacing + 1e-9:
        left.append((lo, y))
        right.append((hi, y))
        y += spacing
    return {
        "bottom": np.array(bottom), "top": np.array(top),
        "left": np.array(left), "right": np.array(right),
    }

WALL_SIDE_ORDER = ("bottom", "top", "left", "right")

def walls_dict_to_array(walls):
    return np.vstack([walls[name] for name in WALL_SIDE_ORDER])

def wall_side_ranges(walls):
    ranges = {}
    start = 0
    for name in WALL_SIDE_ORDER:
        n = len(walls[name])
        ranges[name] = (start, start + n)
        start += n
    return ranges

def radius_to_marker_size(radius_data_units, ax, fig):
    ax_width_inches = fig.get_size_inches()[0] * ax.get_position().width
    data_range_x = ax.get_xlim()[1] - ax.get_xlim()[0]
    points_per_data_unit = ax_width_inches * 72 / data_range_x
    diameter_points = 2 * radius_data_units * points_per_data_unit
    return diameter_points ** 2


def make_state(wall_pos, mobile_pos=None, rebuild_interval=VERLET_REBUILD_INTERVAL,
               wall_side_ranges_dict=None):
    mobile_pos = np.zeros((0, 2)) if mobile_pos is None else mobile_pos
    n_wall = len(wall_pos)
    pos_all = np.vstack([wall_pos, mobile_pos]) if len(mobile_pos) else wall_pos.copy()
    vel_all = np.zeros_like(pos_all)
    fixed_mask = np.zeros(len(pos_all), dtype=bool)
    fixed_mask[:n_wall] = True
    return {
        "pos": pos_all, "vel": vel_all, "fixed_mask": fixed_mask, "n_wall": n_wall,
        "verlet_pairs": np.zeros((0, 2), dtype=int), "steps_since_rebuild": 10**9,
        "step_count": 0, "rebuild_interval": rebuild_interval,
        "wall_sides": wall_side_ranges_dict or {},
    }


def physics_substep(state):
    if len(state["pos"]) > state["n_wall"]:
        if state["steps_since_rebuild"] >= state["rebuild_interval"]:
            state["verlet_pairs"] = build_verlet_list(state["pos"], cutoff=CUTOFF, skin=VERLET_SKIN)
            state["steps_since_rebuild"] = 0
        pairs = state["verlet_pairs"]

        def force_fn(p, pairs=pairs):
            return compute_forces_from_pairs(p, pairs, sigma=SIGMA)

        forces = force_fn(state["pos"])
        state["pos"], state["vel"], _ = verlet_step(
            state["pos"], state["vel"], forces, DT,
            fixed_mask=state["fixed_mask"], gamma=GAMMA_FRICTION, force_fn=force_fn)
        state["steps_since_rebuild"] += 1

    state["step_count"] += 1

    if len(state["pos"]) > state["n_wall"] and state["step_count"] % N_RESCALE == 0:
        state["vel"] = rescale_velocities(state["vel"], state["fixed_mask"], TARGET_KE_PER_PARTICLE)


def add_particle_to_verlet_list(verlet_pairs, pos_all, new_idx, cutoff, skin):
    d = np.linalg.norm(pos_all - pos_all[new_idx], axis=1)
    r_verlet = cutoff + skin
    mask = (d <= r_verlet) & (d > 0)
    others = np.where(mask)[0]
    if len(others) == 0:
        return verlet_pairs
    new_pairs = np.stack([np.full(len(others), new_idx), others], axis=1)
    return np.vstack([verlet_pairs, new_pairs]) if len(verlet_pairs) else new_pairs


def remove_wall_sides(state, side_names):
    remove_ranges = [state["wall_sides"][name] for name in side_names]
    keep_mask = np.ones(len(state["pos"]), dtype=bool)
    for start, end in remove_ranges:
        keep_mask[start:end] = False

    new_wall_sides = {}
    removed_so_far = 0
    for name in WALL_SIDE_ORDER:
        start, end = state["wall_sides"][name]
        if name in side_names:
            removed_so_far += (end - start)
            continue
        n = end - start
        new_start = start - removed_so_far
        new_wall_sides[name] = (new_start, new_start + n)

    n_removed_total = sum(end - start for start, end in remove_ranges)

    state["pos"] = state["pos"][keep_mask]
    state["vel"] = state["vel"][keep_mask]
    state["fixed_mask"] = state["fixed_mask"][keep_mask]
    state["n_wall"] -= n_removed_total
    state["wall_sides"] = new_wall_sides

    state["verlet_pairs"] = np.zeros((0, 2), dtype=int)
    state["steps_since_rebuild"] = 10**9


def move_wall_side(state, side_name, dx, dy):
    start, end = state["wall_sides"][side_name]
    state["pos"][start:end, 0] += dx
    state["pos"][start:end, 1] += dy


def spawn_bubble(state, birth_point, rng):
    jittered_point = birth_point + rng.normal(scale=BIRTH_JITTER, size=2)
    state["pos"] = np.vstack([state["pos"], jittered_point])
    state["vel"] = np.vstack([state["vel"], np.zeros((1, 2))])
    state["fixed_mask"] = np.append(state["fixed_mask"], False)
    new_idx = len(state["pos"]) - 1
    state["verlet_pairs"] = add_particle_to_verlet_list(
        state["verlet_pairs"], state["pos"], new_idx, CUTOFF, VERLET_SKIN)


def next_birth_point(mobile_pos, rng, tol=TRIANGLE_TOLERANCE, max_attempts=MAX_TRIANGLE_ATTEMPTS):
    n = len(mobile_pos)
    tree = cKDTree(mobile_pos)
    k_c = min(7, n)

    pos_a = pos_b = pos_c = None
    for _ in range(max_attempts):
        idx_a = rng.integers(0, n)
        pos_a = mobile_pos[idx_a]

        k_b = min(2, n)
        _, idx_b_cand = tree.query(pos_a, k=k_b)
        idx_b_cand = np.atleast_1d(idx_b_cand)
        idx_b_opcoes = idx_b_cand[idx_b_cand != idx_a]
        if len(idx_b_opcoes) == 0:
            continue
        idx_b = idx_b_opcoes[0]
        pos_b = mobile_pos[idx_b]

        _, idx_near_a = tree.query(pos_a, k=k_c)
        _, idx_near_b = tree.query(pos_b, k=k_c)
        candidatos = np.unique(np.concatenate([np.atleast_1d(idx_near_a), np.atleast_1d(idx_near_b)]))
        candidatos = candidatos[(candidatos != idx_a) & (candidatos != idx_b)]
        if len(candidatos) == 0:
            continue

        d_a = np.linalg.norm(mobile_pos[candidatos] - pos_a, axis=1)
        d_b = np.linalg.norm(mobile_pos[candidatos] - pos_b, axis=1)
        metrica = np.sqrt(d_a**2 + d_b**2)
        pos_c = mobile_pos[candidatos[np.argmin(metrica)]]

        lados = np.array([
            np.linalg.norm(pos_a - pos_b),
            np.linalg.norm(pos_b - pos_c),
            np.linalg.norm(pos_a - pos_c),
        ])
        media = lados.mean()
        if media > 0 and np.all(np.abs(lados - media) <= tol * media):
            return np.array([pos_a, pos_b, pos_c]).mean(axis=0)

    return np.array([pos_a, pos_b, pos_c]).mean(axis=0)


def setup_one_by_one(n_target, area_factor):
    side = box_side(n_target, area_factor)
    walls = build_walls(side)
    wall_pos = walls_dict_to_array(walls)
    state = make_state(wall_pos, rebuild_interval=VERLET_REBUILD_INTERVAL,
                        wall_side_ranges_dict=wall_side_ranges(walls))
    margin = 1.5 * A
    xlim = (-2 * A - margin, side + 2 * A + margin)
    ylim = xlim
    birth_point = np.array([side/2, side/2])
    extra = {"birth_point": birth_point, "n_target": n_target}
    return wall_pos, state, xlim, ylim, extra


def step_one_by_one(state, extra):
    physics_substep(state)
    n_mobile = len(state["pos"]) - state["n_wall"]
    if n_mobile < extra["n_target"] and state["step_count"] % SPAWN_INTERVAL == 0:
        spawn_bubble(state, extra["birth_point"], _rng)
        n_mobile += 1
        if n_mobile >= 3:
            mobile_pos = state["pos"][state["n_wall"]:]
            extra["birth_point"] = next_birth_point(mobile_pos, _rng)


def random_start(n, min_sep, area_factor, rng):
    side = box_side(n, area_factor)
    points = []
    attempts = 0
    max_attempts = 20000
    while len(points) < n and attempts < max_attempts:
        candidate = rng.uniform(0, side, size=2)
        attempts += 1
        if not points:
            points.append(candidate)
            continue
        d = np.linalg.norm(np.array(points) - candidate, axis=1)
        if d.min() >= min_sep:
            points.append(candidate)

    if len(points) < n:
        raise RuntimeError(
            f"Could only place {len(points)}/{n} bubbles without overlap. "
            "Increase area_factor or reduce n_bubbles."
        )
    return np.array(points), side


def setup_all_at_once(n_bubbles, area_factor):
    mobile_pos, side = random_start(n_bubbles, MIN_SEPARATION, area_factor, _rng)
    walls = build_walls(side)
    wall_pos = walls_dict_to_array(walls)
    state = make_state(wall_pos, mobile_pos, rebuild_interval=VERLET_REBUILD_INTERVAL_ALL_AT_ONCE,
                        wall_side_ranges_dict=wall_side_ranges(walls))
    margin = 1.5 * A
    xlim = (-2 * A - margin, side + 2 * A + margin)
    ylim = xlim
    return wall_pos, state, xlim, ylim


def step_all_at_once(state, extra):
    physics_substep(state)


def parse_args():
    parser = argparse.ArgumentParser(
        description="Bragg-Nye bubble raft simulator",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument(
        "-g", "--bubble-generation", choices=["one-by-one", "all-at-once"],
        default="one-by-one",
        help="How bubbles are created")
    parser.add_argument(
        "--n-target", type=int, default=None,
        help="How many bubbles (default: %(default)s if not set -- "
            f"{N_TARGET_DEFAULT} for one-by-one mode, {N_BUBBLES_DEFAULT} for all-at-once mode)")
    parser.add_argument(
        "--relax-steps", type=int, default=None,
        help="Relaxation steps (default: %(default)s if not set -- "
                f"{RELAX_STEPS} relaxation steps.")
    parser.add_argument(
        "--compress-velocity", type=float, default=None,
        help="Wall velocity, in units of A per step "
             f"(default: {COMPRESS_VELOCITY_DEFAULT/A} if not set")
    return parser.parse_args()


def main():
    args = parse_args()

    relax_steps = args.relax_steps or RELAX_STEPS
    compress_velocity = (args.compress_velocity * A) if args.compress_velocity is not None \
        else COMPRESS_VELOCITY_DEFAULT
    protocol = {"phase": "generating", "wall_removed_at": None}
    if args.bubble_generation == "one-by-one":
        n_target = args.n_target or N_TARGET_DEFAULT
        wall_pos, state, xlim, ylim, extra = setup_one_by_one(n_target, AREA_FACTOR)
        step_fn = step_one_by_one
        title_fmt = lambda n_mobile: f"one-by-one — {n_mobile}/{n_target} bubbles"
    else:
        n_target = args.n_target or N_BUBBLES_DEFAULT
        wall_pos, state, xlim, ylim = setup_all_at_once(n_target, AREA_FACTOR)
        extra = {}
        step_fn = step_all_at_once
        title_fmt = lambda n_mobile: f"all-at-once — {n_mobile} bubbles"

    fig, ax = plt.subplots(figsize=(7, 7))
    ax.set_xlim(*xlim)
    ax.set_ylim(*ylim)
    ax.set_aspect("equal")
    ax.set_axis_off()

    wall_scatter = ax.scatter(wall_pos[:, 0], wall_pos[:, 1], s=10, c="#888888",
                               marker="s", linewidths=0)
    n_mobile_inicial = len(state["pos"]) - state["n_wall"]
    mobile_scatter = ax.scatter(
        state["pos"][state["n_wall"]:, 0] if n_mobile_inicial else [],
        state["pos"][state["n_wall"]:, 1] if n_mobile_inicial else [],
        s=10, c=np.ones(n_mobile_inicial), cmap="Spectral", vmin=0, vmax=1,
        edgecolors="black", linewidths=0.4)
    fig.colorbar(mobile_scatter, ax=ax, label=r"$|\psi_6|$ (1 = perfect hexagonal)", shrink=0.8)
    title = ax.set_title(title_fmt(n_mobile_inicial))

    marker_size = {"value": radius_to_marker_size(BUBBLE_RADIUS, ax, fig)}
    wall_scatter.set_sizes(np.full(len(wall_pos), marker_size["value"]))
    if n_mobile_inicial > 0:
        mobile_scatter.set_sizes(np.full(n_mobile_inicial, marker_size["value"]))

    def on_resize(event):
        marker_size["value"] = radius_to_marker_size(BUBBLE_RADIUS, ax, fig)
        wall_scatter.set_sizes(np.full(state["n_wall"], marker_size["value"]))
        n_mobile_agora = len(state["pos"]) - state["n_wall"]
        if n_mobile_agora > 0:
            mobile_scatter.set_sizes(np.full(n_mobile_agora, marker_size["value"]))
        fig.canvas.draw_idle()

    fig.canvas.mpl_connect("resize_event", on_resize)

    def update(frame):
        for _ in range(STEPS_PER_FRAME):
            step_fn(state, extra)

        mobile_pos = state["pos"][state["n_wall"]:]

        if protocol["phase"] == "generating":
            if len(mobile_pos) == n_target:
                protocol["phase"] = "relax before box opening"
                protocol["generated_at"] = state["step_count"]

        elif protocol["phase"] == "relax before box opening":
            if state["step_count"] - protocol["generated_at"] > relax_steps and "top" in state["wall_sides"]:
                remove_wall_sides(state, ["top", "bottom"])
                protocol["phase"] = "relax after box opening"
                protocol["wall_removed_at"] = state["step_count"]

        elif protocol["phase"] == "relax after box opening":
            if state["step_count"] - protocol["wall_removed_at"] > relax_steps:
                protocol["phase"] = "compressing"
                state["rebuild_interval"] = VERLET_REBUILD_INTERVAL_COMPRESSION
                left_x = state["pos"][slice(*state["wall_sides"]["left"]), 0].mean()
                right_x = state["pos"][slice(*state["wall_sides"]["right"]), 0].mean()
                protocol["target_x"] = (left_x + right_x) / 2

        elif protocol["phase"] == "compressing":
            right_x = state["pos"][slice(*state["wall_sides"]["right"]), 0].mean()
            if right_x <= protocol["target_x"]:
                protocol["phase"] = "stop"
            else:
                move_wall_side(state, "right", -compress_velocity, 0.0)

        wall_pos_agora = state["pos"][:state["n_wall"]]
        wall_scatter.set_offsets(wall_pos_agora)
        wall_scatter.set_sizes(np.full(state["n_wall"], marker_size["value"]))

        mobile_scatter.set_offsets(mobile_pos if len(mobile_pos) else np.zeros((0, 2)))
        if len(mobile_pos) > 0:
            mobile_scatter.set_sizes(np.full(len(mobile_pos), marker_size["value"]))

        if len(mobile_pos) > 0:
            psi6 = compute_psi6(state["pos"], state["verlet_pairs"])
            mobile_scatter.set_array(psi6[state["n_wall"]:])

        title.set_text(title_fmt(len(mobile_pos)) + f" (step {state['step_count']}, phase: {protocol['phase']})")
        return mobile_scatter, wall_scatter, title

    anim = animation.FuncAnimation(fig, update, frames=4000, interval=20, blit=False)
    plt.show()


if __name__ == "__main__":
    main()
