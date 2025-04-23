"""
Hydrogen Radial Wave Function animation

Author: Marcelo Falcão de Oliveira
Affiliation: University of São Paulo (USP)
             São Carlos School of Engineering (EESC)
             Materials Engineering Department (SMM)
Contact: marcelo.falcao@usp.br

Description:
This Python script show animated plots for the solutions of Schrödinger's
equation for hydrogen regarding the radial function and the radial
probability density.

License:
MIT License (https://opensource.org/licenses/MIT)

Purpose:
Educational tool for demonstrating the radial functions and radial
probability densities of hydrogen.

Packages needed:
argparse, matplotlib, numpy, sympy

Usage:
$ python hydrogen_psi_radial_anim.py <arg1> <arg2>
- <arg1> principal quantum number
- <arg2> azimutal quantum number

Date: January/2024
Version: 1.0
"""

import argparse                             # Module for parsing command-line arguments
import numpy as np                          # Numerical operations using arrays
import matplotlib.pyplot as plt             # Plotting library
import matplotlib.animation as animation    # Animation functionality
from sympy.abc import r                     # Importing specific symbol (r) from the sympy.abc module
from sympy.physics.hydrogen import R_nl     # Radial hydrogen function from sympy.
from sympy import lambdify                  # lambdify evaluates functions numerically

class Wave:
    def __init__(self, n, l):
                      
        """
        Set up the function parameters and plot limits
        """
        self.xlim = 2 * (n**2 + n)                  # Approximately close to the tail of the radial function (in Hartree unit)
        self.x = np.linspace(0, self.xlim, 200)     # Distribute points along the line
        psi_R = lambdify(r, R_nl(n,l,r), 'numpy')   # Takes the radial expression and converts into a function
        self.f = psi_R(self.x)                      # Calculates the radial function along the line
        self.wylim = 1.05*max(self.f.real)          # Define the y limit for the radial function
        self.dylim = 1.05*max(self.dens())          # Define the y limit for the denstiy plot
                
    def dens(self):
        """
        Calculates the radial probability density
        """
        dens = (self.f*np.conjugate(self.f))*self.x**2
        return dens
    
    def animate(self, frame):
        """
        Update the animation for each frame.
        """
        f = self.f*np.exp(-(1j)*frame/100*np.pi) # introduces the time part of the wavefunction
        line1.set_ydata(f.real)                  # update the real part of the wavefunction
        line2.set_ydata(f.imag)                  # update the imaginary part of the wave function
        return line1, line2,                     # return the new lines for plotting

def parse_arguments():
    """
    Parse command-line arguments for the script.
        Returns:
        argparse.Namespace: An object containing parsed command-line arguments.
    """
    # Create an argument parser with a description
    parser = argparse.ArgumentParser(description='Hydrogen Radial Function Animation')
    # Add command-line arguments for principal and azimuthal quantum numbers
    parser.add_argument('n', metavar='n', type=int, help='Principal quantum number n (n >= 1)')
    parser.add_argument('l', metavar='l', type=int, help='Azimuthal quantum number l (l < n)')
    # Parse the command-line arguments and return the result
    return parser.parse_args()

# Execute the main code only if this script is run directly, not when imported as a module
if __name__ == "__main__":

    # Parse command line arguments
    args = parse_arguments()
    
    wave_sim = Wave(args.n,args.l)  # create the wave object with the input arguments

    fig, ax = plt.subplots()                    # create the plot figure
    fig.set_size_inches(6,6)                    # adjust figure size
    fig.subplots_adjust(left=0.14, right=0.84)  # adjust figure margins
  
    line1, = ax.plot(wave_sim.x, wave_sim.f.real, color='tab:orange', label='real') # plot the real part
    line2, = ax.plot(wave_sim.x, wave_sim.f.imag, color='tab:blue', label='imag')   # plot the imaginary part

    ax.legend() # add the legend
    
    ax.set_ylim([-wave_sim.wylim,wave_sim.wylim])    # set y limits for the waves
    ax.set_ylabel(f'$R\,_n\,_l\:(real\:and\:imag)$') # set y label (left)
    ax.set_xlim([0,wave_sim.xlim])                   # set x limits
    ax.set_xlabel(f'$r\:(a_0)$')                     # set x label
       
    ax2 = ax.twinx()                                                # set a new axe sharing the x axis
    line3, = ax2.plot(wave_sim.x, wave_sim.dens(), color='green')   # plot the radial probability density

    ax2.set_ylim([-wave_sim.dylim,wave_sim.dylim])                  # set y limits for density plot
    ax2.tick_params(axis='y', labelcolor='green')                   # set y tick label color
    ax2.set_ylabel(f'$\|R\,_n\,_l\|^2\,r^2$', color='green')        # set y label

    # define the animation
    ani = animation.FuncAnimation(fig, wave_sim.animate, interval=10, blit=True, save_count=500)
    
    # Uncomment this line if you want to save a mp4 movie
    #ani.save('hydrogen_psi_radial_'+str(args.n)+'_'+str(args.l)+'.mp4', fps=30)
    
    plt.show()                  # finally shows the plot
