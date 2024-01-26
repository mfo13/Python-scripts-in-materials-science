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

Date: July, 2023
Version: 1.1

Note:
This script was improved with the assistance of ChatGPT-3.5.
"""

import argparse                                # Module for parsing command-line arguments
import matplotlib.pyplot as plt                # Module for creating plots and visualizations
from matplotlib import cm, colors              # Modules for handling color maps and colors
import numpy as np                             # Module for numerical operations with arrays
from scipy.special import sph_harm             # Module for spherical harmonics functions
from matplotlib.animation import FuncAnimation # Module for creating animated plots
from sympy import Ynm, latex, simplify         # Modules for symbolic mathematics (used for LaTeX representation of mathematical expressions)
from sympy.abc import theta, phi               # Symbolic variables used in the script

def parse_arguments():
    """
    Parses command-line arguments using argparse.

    Returns:
        argparse.Namespace: Parsed arguments.
    """
    parser = argparse.ArgumentParser(description="Generate an animation of spherical harmonics.")
    parser.add_argument("l", type=int, help="Degree of the spherical harmonics (must be >= 0, default: 0).", metavar="l", default=0)
    parser.add_argument("m", type=int, help="Order of the spherical harmonics (-l <= m <= l, default: 0).", metavar="m", default=0)

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
   global surf                                    # Update the global variable 'surf' to manage the 3D surface plot
   t = 2 * np.pi / nframes * i                     # Calculate the angle 't' based on the frame index 'i'
   r = sph * np.cos(t)                             # Compute the radial distance 'r' using spherical harmonics and cosine modulation
   surfcolors = (r - minsph) / (maxsph - minsph)   # Map the radial values 'r' to colors using normalization
   r += 4                                          # Increase the radial distance 'r' to enhance the visualization

   # Calculate the cartesian coordinates based on spherical coordinates
   x = r * np.sin(nphi) * np.cos(ntheta)
   y = r * np.sin(nphi) * np.sin(ntheta)
   z = r * np.cos(nphi)

   # Remove the previous surface plot
   surf.remove()
   # Plot the new surface
   surf = ax.plot_surface(x, y, z, rstride=1, cstride=1, facecolors=cm.viridis(surfcolors), shade=False)
   surf.set(edgecolor='black', linewidth=0.1)

# Execute the main code only if this script is run directly, not when imported as a module
if __name__ == "__main__":
   # Parse command-line arguments
   args = parse_arguments()
   l, m = args.l, args.m

   # Generate spherical coordinates grid
   nphi = np.linspace(0, np.pi, 30)
   ntheta = np.linspace(0, 2*np.pi, 30)
   nphi, ntheta = np.meshgrid(nphi, ntheta)

   # Create a figure and 3D axis
   fig = plt.figure(figsize=(6, 6))
   fig.patch.set_facecolor('black')
   ax = fig.add_subplot(111, projection='3d')
   ax.patch.set_facecolor('black')

   # Initialize the surface plot
   surf = ax.plot_surface(np.array([[]]), np.array([[]]), np.array([[]]))

   # Compute spherical harmonics
   sph = sph_harm(m, l, ntheta, nphi).imag if m < 0 else sph_harm(m, l, ntheta, nphi).real

   # Determine the range of spherical harmonics values
   maxsph = sph.max()
   minsph = -maxsph

   # Set axis limits
   ax.set_xlim([-4.0, 4.0])
   ax.set_ylim([-4.0, 4.0])
   ax.set_zlim([-4.0, 4.0])

   # Customize axis appearance
   ax.set_axis_off()
   ax.set_aspect('equal')
   mcm = cm.ScalarMappable(cmap=cm.viridis)
   mcm.set_array([minsph, maxsph])
   cbar = plt.colorbar(mcm, ax=ax, location='right', fraction=0.15, shrink=0.5)
   cbar.ax.yaxis.set_tick_params(color='white')
   plt.setp(plt.getp(cbar.ax.axes, 'yticklabels'), color='white')
   plt.subplots_adjust(left=0, bottom=0, right=1, top=1, wspace=0, hspace=0)
   plt.rcParams['text.usetex'] = True

   # Set the title with the symbolic expression for spherical harmonics
   ax.set_title('$Y_{('+str(l)+','+str(m)+')}='+latex(simplify(Ynm(l, m, theta, phi).expand(func=True)))+'$', fontsize=14, color='white')

   # Number of animation frames
   nframes = 36
   # Create the animation
   anim = FuncAnimation(fig, animate, frames=nframes, interval=1000/nframes)

   # Uncomment the lines below if you want to save mp4 or gif movies
   # anim.save('sph_harm_'+str(l)+'_'+str(m)+'.mp4')
   # anim.save('sph_harm_'+str(l)+'_'+str(m)+'.gif')

   # Display the animation
   plt.show()
