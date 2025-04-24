'''
Drum Harmonics py

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
numpy, scipy, matplotlib (this last one is the main core)

July 2023

'''

howtouse = '''
# How to use
#
# $ python drum_harmonics.py <arg1> <arg2>
#
# <arg1> must be an integer equal or greater than 0 
# <arg2> must be an integer equal or greater than 1

'''

import sys, matplotlib.pyplot as plt            # sys is needed for input arguments form command line, matplot.pyplot is used for plotting
from matplotlib import cm, colors               # cm and colors from matplotlib are used for coloring the surface and the scalebar
import numpy as np                              # numpy is needed for some numerical functions
from scipy.special import jn, jn_zeros          # scipy give us the Bessel functions

# check the user input and get it if correct, otherwise quite with a help message
try:
   m, n = int(sys.argv[1]), int(sys.argv[2]) # input harmonic numbers by the user in the command line
except:
    sys.exit(howtouse)
if m<0 or n<1: sys.exit(howtouse)

theta = np.linspace(0, 2*np.pi, 90)		# array with 30 theta angles in radians
r = np.linspace(0, 1, 30)              # array with 30 points in unit radius
r, theta = np.meshgrid(r, theta)       # the radiu and the angles builds a grid or mesh

k = jn_zeros(m, n)[n-1]                            # take the nth zero of Bessel function Jm
z = (np.sin(m*theta)+np.cos(m*theta)) * jn(m, k*r) # z position of the drum membrane at t=0
maxz = z.max()                                     # max value of our z
minz = -maxz                                       # min value of our z
surfcolors = (z-minz)/(maxz-minz)                  # the surface color array is proportional to the amplitude but normalized according to the lower and upper limits
   
# Now we transform polar coordinates to cartesian coordinates
x = r * np.cos(theta)
y = r * np.sin(theta)

fig = plt.figure(figsize=(6,6))				   # definition of figure with 6 by 6 inches
fig.patch.set_facecolor('black')             # figure background color
ax = fig.add_subplot(111, projection='3d')	# we add a plot in the figure specifing 3D rendering
ax.patch.set_facecolor('black')              # plot area backgrond color

# we make the plot of the surface positons and also apply the colors; rstride and cstride are set to take all the points; we also don't want shades when the user rotates the sphere
surf = ax.plot_surface(x, y, z, rstride=1, cstride=1, facecolors=cm.viridis(surfcolors), shade=False)
surf.set(edgecolor='black', linewidth=0.1)   # plot a thin black wireframe on the surface

ax.set_axis_off()	# turns off the axis, we don't want to see them

# x, y and z limits in the plot
ax.set_xlim([-.7, .7])                                               
ax.set_ylim([-.7, .7])
ax.set_zlim([-1.4, 1.4]) # we make z large to reduce the visual of the amplitudes

ax.set_axis_off()                                # turns off the axis, we don't want to see them
mc = cm.ScalarMappable(cmap=cm.viridis)          # color map to use in our surface
mc.set_array([minz, maxz])                       # array of the colors according to the max and min value of z
cbar = plt.colorbar(mc, ax=ax, location='right', fraction=0.15, shrink=0.5)   # definition of our scalebar
cbar.ax.yaxis.set_tick_params(color='white')                                  # colorbar tick color
plt.setp(plt.getp(cbar.ax.axes, 'yticklabels'), color='white')                # colorbar tick text color
plt.subplots_adjust(left=0, bottom=0, right=1, top=1, wspace=0, hspace=0)     # we adjust the position of our plot in the fig window
plt.rcParams['text.usetex']=True                                              # sets latex to display our text

# plots the vibration frequency (\nu), N*rr is the normal force of the membrane at the periferic circle, \rho is the material density and h is the membrane thickness
text = f'$\\nu_{{({m},{n})}}=\\frac{{{k:.3f}}}{{2\\pi}}\\sqrt{{\\frac{{N^*_{{rr}}}}{{\\rho{{h}}}}}}$'
ax.set_title(text, fontsize=14, color='white')

plt.show()	# finally we show our plot window