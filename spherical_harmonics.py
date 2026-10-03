'''
Spherical Harmonics py

Author: Marcelo Falcão de Oliveira
Affiliation: University of São Paulo 
             São Carlos School of Engineering
             Materials Engineering Department
e-mail: marcelo.falcao@usp.br

This python script is intended for teaching porposes.
You can use, copy to others or modify as you wish but at your own risk.
If you find it usefull for your work, please cite the source.

Since the basic idea is for teaching the the script is, as much as possible, fully commented.

Packages needed:
numpy, scipy, sympy, matplotlib (this last one is the main core)

July 2023 (2026 update for scipy compatibility)
'''

howtouse = '''
# How to use
#
# $ python spherical_harmonics.py <arg1> <arg2>
#
# <arg1> must be an integer equal or greater than 0 
# <arg2> must be an integer and -<arg1> <= <arg2> <= <arg1>

'''

import sys, matplotlib.pyplot as plt        # sys is needed for input arguments from command line, matplotlib.pyplot is used for plotting
from matplotlib import cm, colors           # cm and colors from matplotlib are used for coloring the surface and the scalebar
import numpy as np                          # numpy is needed for some numerical functions
from sympy import Ynm, latex, simplify      # sympy functions: Ynm is spherical harmonics in algebraic format, latex is for LaTeX rendering, simplify is for symbolic simplification
from sympy.abc import theta, phi            # theta and phi symbols from sympy

# Import sph_harm_y for newer SciPy versions, or fall back to sph_harm for older versions
try:
    from scipy.special import sph_harm_y
    def get_sph_harm(m, l, ntheta, nphi):
        # sph_harm_y arguments: degree (l), order (m), polar angle [0, pi], azimuthal angle [0, 2pi]
        return sph_harm_y(l, m, nphi, ntheta)
except ImportError:
    from scipy.special import sph_harm
    def get_sph_harm(m, l, ntheta, nphi):
        # legacy sph_harm arguments: order (m), degree (l), azimuthal angle [0, 2pi], polar angle [0, pi]
        return sph_harm(m, l, ntheta, nphi)

# Check the user input; if no arguments are given in IDE execution, use defaults (l=3, m=2) instead of exiting
if len(sys.argv) == 3:
    try:
        l, m = int(sys.argv[1]), int(sys.argv[2])
    except ValueError:
        sys.exit(howtouse)
elif len(sys.argv) == 1:
    l, m = 3, 2  # Default harmonic values when executed directly without CLI arguments
else:
    sys.exit(howtouse)

if l < 0 or np.abs(m) > l:
    sys.exit(howtouse)

nphi = np.linspace(0, np.pi, 90)            # array with 90 polar angles (phi) in radians
ntheta = np.linspace(0, 2*np.pi, 90)        # array with 90 azimuthal angles (theta) in radians
nphi, ntheta = np.meshgrid(nphi, ntheta)    # the angles build a grid or mesh

# compute spherical harmonics using the compatibility function; take imaginary part if m<0, real part otherwise for real spherical harmonics
harm_val = get_sph_harm(m, l, ntheta, nphi)
sph = harm_val.imag if m < 0 else harm_val.real

maxsph = sph.max()                          # maximum possible displacement
minsph = -maxsph                            # minimum possible displacement
surfcolors = (sph - minsph)/(maxsph-minsph) # normalized surface color array bounded between 0 and 1
r = sph + 7                                 # add average radius of the sphere (7) to the amplitude
   
# transform spherical coordinates to cartesian coordinates
x = r * np.sin(nphi) * np.cos(ntheta)
y = r * np.sin(nphi) * np.sin(ntheta)
z = r * np.cos(nphi)

fig = plt.figure(figsize=(6,6))             # definition of figure with 6 by 6 inches
fig.patch.set_facecolor('black')            # figure background color
ax = fig.add_subplot(111, projection='3d')  # add a 3D subplot to the figure
ax.patch.set_facecolor('black')             # plot area background color

# plot the surface positions and apply colors; rstride/cstride set to 1 for full resolution; shade=False avoids unwanted lighting shading when rotating
surf = ax.plot_surface(x, y, z, rstride=1, cstride=1, facecolors=cm.viridis(surfcolors), shade=False)
surf.set(edgecolor='black', linewidth=0.1)   # plot a thin black wireframe on the surface

ax.set_axis_off()   # turn off axis display

# set x, y and z limits in the plot
ax.set_xlim([-7.0, 7.0])
ax.set_ylim([-7.0, 7.0])
ax.set_zlim([-7.0, 7.0])

ax.set_aspect('equal')                     # set equal aspect ratio so the sphere is not distorted into an ellipsoid
mcm = cm.ScalarMappable(cmap=cm.viridis)    # color map for the surface
mcm.set_array([minsph, maxsph])             # array bounds for color mapping based on min and max displacement

cbar = plt.colorbar(mcm, ax=ax, location='right', fraction=0.15, shrink=0.5)    # definition of scalebar
cbar.ax.yaxis.set_tick_params(color='white')                               # colorbar tick marks color
plt.setp(plt.getp(cbar.ax.axes, 'yticklabels'), color='white')             # colorbar tick labels text color
plt.subplots_adjust(left=0, bottom=0, right=1, top=1, wspace=0, hspace=0)   # adjust plot position in figure window

# display the symbolic equation in the plot title using Matplotlib's built-in mathtext engine
ax.set_title('$Y_{('+str(l)+','+str(m)+')}='+latex(simplify(Ynm(l, m, theta, phi).expand(func=True)))+'$', fontsize=14, color='white')

plt.show()  # display plot window