"""
Drum Harmonics Animation

Author: Marcelo Falcão de Oliveira
Affiliation: University of São Paulo (USP)
             São Carlos School of Engineering (EESC)
             Materials Engineering Department (SMM)
Contact: marcelo.falcao@usp.br

Description:
This Python script generates an animation of drum harmonics for teaching purposes.
It visualizes the vibration modes of a drum membrane based on user-specified harmonic numbers.

License:
MIT License (https://opensource.org/licenses/MIT)

Purpose:
Educational tool for demonstrating drum vibrations and harmonic principles.

Packages needed:
argparse, numpy, scipy, matplotlib

Usage:
$ python drum_harmonics_anim.py <arg1> <arg2>
- <arg1> must be an integer equal or greater than 0
- <arg2> must be an integer equal or greater than 1
- Use 'python drum_harmonics_anim.py -h' for help.

Date: July, 2023
Version: 1.1

Note:
This script was improved with the assistance of ChatGPT-3.5.
"""

import argparse                                 # Module for handling command-line arguments
import numpy as np                              # Numerical computing library
import matplotlib.pyplot as plt                 # Plotting library
from matplotlib import cm, colors               # Colormap and color utilities
from scipy.special import jn, jn_zeros          # Bessel functions and their zeros
from matplotlib.animation import FuncAnimation  # Animation module for Matplotlib

# function to initialize the plot
def initialize_plot(m, n):
    # Create a grid of polar coordinates
    theta = np.linspace(0, 2*np.pi, 30)
    r = np.linspace(0, 1, 30)
    r, theta = np.meshgrid(r, theta)
    
    # Initialize the 3D plot
    fig = plt.figure(figsize=(6, 6), facecolor='black')
    ax = fig.add_subplot(111, projection='3d', facecolor='black')
    
    # Calculate Bessel function zeros and drum membrane shape
    k = jn_zeros(m, n)[n-1]
    z = (np.sin(m * theta) + np.cos(m * theta)) * jn(m, k * r)
    maxz, minz = z.max(), -z.max()
    
    # Set plot limits and axis properties
    ax.set_xlim([-.7, .7])
    ax.set_ylim([-.7, .7])
    ax.set_zlim([-1.4, 1.4])
    ax.set_axis_off()
    
    # Create a color map for the surface plot
    mc = cm.ScalarMappable(norm=colors.Normalize(minz, maxz), cmap=cm.viridis)
    
    # Add a colorbar to the plot
    cbar = plt.colorbar(mc, ax=ax, location='right', fraction=0.15, shrink=0.5)
    cbar.ax.yaxis.set_tick_params(color='white')
    plt.setp(plt.getp(cbar.ax.axes, 'yticklabels'), color='white')
    
    # Display the vibration frequency formula as the plot title
    text = f'$\\nu_{{({m},{n})}}=\\frac{{{k:.3f}}}{{2\\pi}}\\sqrt{{\\frac{{N^*_{{rr}}}}{{\\rho{{h}}}}}}$'
    ax.set_title(text, fontsize=14, color='white')
    
    return fig, ax, r, theta, z, mc, minz, maxz

# function to animate the surface
def animate(i, ax, r, theta, z, mc, minz, maxz):
    # Calculate the membrane shape for the current animation step
    t = 2 * np.pi / nframes * i
    zz = z * np.cos(t)
    surfcolors = (zz - minz) / (maxz - minz)
    
    # Convert polar coordinates to Cartesian coordinates
    x = r * np.cos(theta)
    y = r * np.sin(theta)

    # Remove the previous surface
    for col in ax.collections:
        col.remove()

    # Plot the updated surface with the new membrane shape and colors
    surf = ax.plot_surface(x, y, zz, rstride=1, cstride=1, facecolors=cm.viridis(surfcolors), shade=False)
    surf.set(edgecolor='black', linewidth=0.1)
    
    return surf

# Execute the main code only if this script is run directly, not when imported as a module
if __name__ == "__main__":
    # Parse command-line arguments for harmonic numbers
    parser = argparse.ArgumentParser(description='Drum Harmonics Animation')
    parser.add_argument('m', type=int, help='An integer equal or greater than 0')
    parser.add_argument('n', type=int, help='An integer equal or greater than 1')
    args = parser.parse_args()

    # Extract harmonic numbers from command-line arguments
    m, n = args.m, args.n

    # Initialize the plot and get necessary parameters
    fig, ax, r, theta, z, mc, minz, maxz = initialize_plot(m, n)
    
    # Set the number of frames for the animation
    nframes = 36
    
    # Create the animation
    anim = FuncAnimation(fig, animate, fargs=(ax, r, theta, z, mc, minz, maxz), frames=nframes, interval=100/nframes)
    
    # Uncomment the lines below if you want to save mp4 or gif movies
    # anim.save(f'drum_{m}_{n}.mp4')
    # anim.save(f'drum_{m}_{n}.gif')
    
    # Show the animation plot
    plt.show()
