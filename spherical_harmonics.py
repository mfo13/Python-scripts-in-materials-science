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

July 2023

'''

howtouse = '''
# How to use
#
# $ python spherical_harmonics.py <arg1> <arg2>
#
# <arg1> must be an integer equal or greater than 0 
# <arg2> must be an integer and -<arg1> <= <arg2> <= <arg1>

'''

import sys, matplotlib.pyplot as plt 		# sys is needed for input arguments form command line, matplot.pyplot is used for plotting
from matplotlib import cm, colors 			# cm and colors from matplotlib are used for coloring the surface and the scalebar
import numpy as np							   # numpy is needed for some numerical functions
from scipy.special import sph_harm			# scipy give us the sph_harm which is the spherical harmonics function
from sympy import Ynm, latex, simplify          # sympy functions, Ynm is the spherical harmonics in algebraic format, latex is for latex display and simplify is for simplification
from sympy.abc import theta, phi                # thet and phi sybols from sympy

# check the user input and get it if correct, otherwise quite with a help message
try:
   m, l = int(sys.argv[2]), int(sys.argv[1]) # input harmonic numbers by the user in the command line
except:
    sys.exit(howtouse)
if l<0 or np.abs(m)>l: sys.exit(howtouse)

nphi = np.linspace(0, np.pi, 90)			# array with 90 phi angles in radians
ntheta = np.linspace(0, 2*np.pi, 90)		# array with 30 theta angles in radians
nphi, ntheta = np.meshgrid(nphi, ntheta)	# the angles builds a grid or mesh

# this is the spherical harmonics, we take real part if m>=0 otherwise we take the imaginary part, thus we have orthogonality
sph = sph_harm(m, l, ntheta, nphi).imag if m<0 else sph_harm(m, l, ntheta, nphi).real

maxsph = sph.max()                           # maximum possible displacement
minsph = -maxsph                             # minimum possible displacement
surfcolors = (sph - minsph)/(maxsph-minsph)	# the surface color array is proportional to the amplitude but normalized according to the lower and upper limits
r = sph + 7												# we add the average radius of the sphere (in this case 7) to the amplitude
   
# Now we transform spherical coordinates to cartesian coordinates
x = r * np.sin(nphi) * np.cos(ntheta)
y = r * np.sin(nphi) * np.sin(ntheta)
z = r * np.cos(nphi)

fig = plt.figure(figsize=(6,6))				   # definition of figure with 6 by 6 inches
fig.patch.set_facecolor('black')             # figure background color
ax = fig.add_subplot(111, projection='3d')	# we add a plot in the figure specifing 3D rendering
ax.patch.set_facecolor('black')              # plot area backgrond color

# we make the plot of the surface positons and also apply the colors; rstride and cstride are set to take all the points; we also don't want shades when the user rotates the sphere
surf = ax.plot_surface(x, y, z,  rstride=1, cstride=1, facecolors=cm.viridis(surfcolors), shade=False)
surf.set(edgecolor='black', linewidth=0.1)   # plot a thin black wireframe on the surface

ax.set_axis_off()	# turns off the axis, we don't want to see them

# x, y and z limits in the plot
ax.set_xlim([-7.0, 7.0])
ax.set_ylim([-7.0, 7.0])
ax.set_zlim([-7.0, 7.0])

ax.set_aspect('equal')					   # apect ratio of the axis in the screen so we can see a sphere and not a distorted elipsoid
ax.patch.set_facecolor('black')        # plot area backgrond color
mcm = cm.ScalarMappable(cmap=cm.viridis)	# color map to use in our surface
mcm.set_array([minsph, maxsph])	         # array of the colors according to the min and max possible values of surface displacement


cbar = plt.colorbar(mcm, ax=ax, location='right', fraction=0.15, shrink=0.5)	# definition of our scalebar
cbar.ax.yaxis.set_tick_params(color='white')                               # colorbar tick color
plt.setp(plt.getp(cbar.ax.axes, 'yticklabels'), color='white')             # colorbar tick text color
plt.subplots_adjust(left=0, bottom=0, right=1, top=1, wspace=0, hspace=0)	# we adjust the position of our plot in the fig window
plt.rcParams['text.usetex']=True                                           # sets latex to display our text
# display the equation text in the plot area
ax.set_title('$Y_{('+str(l)+','+str(m)+')}='+latex(simplify(Ynm(l, m, theta, phi).expand(func=True)))+'$', fontsize=14, color='white')

plt.show()	# finally we show our plot window