"""
Spherical Harmonics Animation

Author: Marcelo Falcão de Oliveira
Affiliation: University of São Paulo (USP)
             São Carlos School of Engineering (EESC)
             Materials Engineering Department (SMM)
Contact: marcelo.falcao@usp.br

Description:
This Python script generates an animation of spherical harmonics for teaching purposes.
It visualizes the vibration modes of a spherical membrane based on user-specified harmonic numbers.

License:
MIT License (https://opensource.org/licenses/MIT)

Purpose:
Educational tool for demonstrating spherical harmonics and vibrational principles.

Packages needed:
argparse, numpy, scipy, sympy, matplotlib

Usage:
$ python spherical_harmonics_anim.py <arg1> <arg2>
- <arg1> must be an integer equal or greater than 0
- <arg2> must be an integer equal or greater than 0
- Use 'python spherical_harmonics_anim.py -h' for help.

Date: July, 2023 (Updated 2026 for SciPy compatibility)
Version: 1.2
"""

import argparse
import matplotlib.pyplot as plt
from matplotlib import cm, colors
import numpy as np
from matplotlib.animation import FuncAnimation
from sympy import Ynm, latex, simplify
from sympy.abc import theta, phi

# Compatibility trials
try:
    from scipy.special import sph_harm_y
    def get_sph_harm(m, l, ntheta, nphi):
        # sph_harm_y input: (l, m, polar [0, pi], azimute [0, 2pi])
        return sph_harm_y(l, m, nphi, ntheta)
except ImportError:
    from scipy.special import sph_harm
    def get_sph_harm(m, l, ntheta, nphi):
        # old sph_harm input: (m, l, azimute [0, 2pi], polar [0, pi])
        return sph_harm(m, l, ntheta, nphi)

def parse_arguments():
    """
    Parses command-line arguments using argparse.

    Returns:
        argparse.Namespace: Parsed arguments.
    """
    parser = argparse.ArgumentParser(description="Generate an animation of spherical harmonics.")
    parser.add_argument("l", type=int, nargs='?', help="Degree of the spherical harmonics (must be >= 0, default: 3).", metavar="l", default=3)
    parser.add_argument("m", type=int, nargs='?', help="Order of the spherical harmonics (-l <= m <= l, default: 2).", metavar="m", default=2)

    try:
        args = parser.parse_args()
        if args.l < 0 or np.abs(args.m) > args.l:
            raise argparse.ArgumentTypeError("Invalid harmonic numbers. l must be >= 0 and -l <= m <= l.")
        return args
    except argparse.ArgumentTypeError as e:
        parser.error(str(e))

def animate(i):
    """
    Animates the spherical harmonics.

    Args:
        i (int): Frame index.
    """
    global surf
    t = 2 * np.pi / nframes * i
    r = sph * np.cos(t)
    surfcolors = (r - minsph) / (maxsph - minsph)
    r += 4

    x = r * np.sin(nphi) * np.cos(ntheta)
    y = r * np.sin(nphi) * np.sin(ntheta)
    z = r * np.cos(nphi)

    surf.remove()
    surf = ax.plot_surface(x, y, z, rstride=1, cstride=1, facecolors=cm.viridis(surfcolors), shade=False)
    surf.set(edgecolor='black', linewidth=0.1)

if __name__ == "__main__":
    args = parse_arguments()
    l, m = args.l, args.m

    # Grid de coordenadas esféricas
    nphi = np.linspace(0, np.pi, 30)       # Ângulo polar [0, pi]
    ntheta = np.linspace(0, 2*np.pi, 30)   # Ângulo azimutal [0, 2pi]
    nphi, ntheta = np.meshgrid(nphi, ntheta)

    fig = plt.figure(figsize=(6, 6))
    fig.patch.set_facecolor('black')
    ax = fig.add_subplot(111, projection='3d')
    ax.patch.set_facecolor('black')

    surf = ax.plot_surface(np.array([[]]), np.array([[]]), np.array([[]]))

    # Calculation according to the compatible version
    harm_val = get_sph_harm(m, l, ntheta, nphi)
    sph = harm_val.imag if m < 0 else harm_val.real

    maxsph = sph.max()
    minsph = -maxsph

    ax.set_xlim([-4.0, 4.0])
    ax.set_ylim([-4.0, 4.0])
    ax.set_zlim([-4.0, 4.0])

    ax.set_axis_off()
    ax.set_aspect('equal')
    mcm = cm.ScalarMappable(cmap=cm.viridis)
    mcm.set_array([minsph, maxsph])
    cbar = plt.colorbar(mcm, ax=ax, location='right', fraction=0.15, shrink=0.5)
    cbar.ax.yaxis.set_tick_params(color='white')
    plt.setp(plt.getp(cbar.ax.axes, 'yticklabels'), color='white')
    plt.subplots_adjust(left=0, bottom=0, right=1, top=1, wspace=0, hspace=0)
    
    # Latex usage
    plt.rcParams['text.usetex'] = True

    ax.set_title('$Y_{('+str(l)+','+str(m)+')}='+latex(simplify(Ynm(l, m, theta, phi).expand(func=True)))+'$', fontsize=14, color='white')

    nframes = 36
    anim = FuncAnimation(fig, animate, frames=nframes, interval=1000/nframes)

    plt.show()