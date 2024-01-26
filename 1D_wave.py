"""
1D Wave Simulation

Author: Marcelo Falcão de Oliveira
Affiliation: University of São Paulo (USP)
             São Carlos School of Engineering (EESC)
             Materials Engineering Department (SMM)
Contact: marcelo.falcao@usp.br

Description:
It ilustrates the solution of the wave equation in 1D with the
FDM method. The user can choose among 4 classical boundary conditions 
as well as the presence or not of a 'dielectric layer' in the
trajectory.

License:
MIT License (https://opensource.org/licenses/MIT)

Purpose:
Educational tool for demonstrating the FDM solution of 1D wave equation.

Packages needed:
argparse, matplotlib, numpy

Usage:
$ python 1D_wave.py --lbc <arg1> --rbc <arg2> --dl <arg3>
Optional arguments:
- <arg1> left boundary condition, a value among 'd', 'n', 'p' and 'pab' (default: n)
- <arg2> right boundary condition, same as above (default: pab)
- <arg3> 'y' or 'n' for a dielectric layer in the wave path (default: y)
- Use 'python 1D_wave.py -h' for help.

p.s. d-Dirichlet, n-Neumann, p-periodic and pab-Perfect Absorbing Boundary

Date: January/2024
Version: 1.0

Note: Some comments were improved with ChatGPT-3.5.
"""

import argparse                             # Module for parsing command-line arguments
import numpy as np                          # Numerical operations using arrays
import matplotlib.pyplot as plt             # Plotting library
import matplotlib.animation as animation    # Animation functionality


class WaveSimulation:
    def __init__(self, lbc, rbc, dl):
        """
        Initialize the WaveSimulation object with given boundary conditions.
        Parameters:
        - lbc (str): Left boundary condition ('d', 'n', 'p', 'pab').
        - rbc (str): Right boundary condition ('d', 'n', 'p', 'pab').
        - dl (str): 'y' if there is a dielectric layer, 'n' otherwise.

        To understand how matrices, vectors and boundary conditions work refer to the lecture documentation. 
        """
        self.lbc = lbc  # Left boundary condition ('d', 'n', 'p', 'pab')
        self.rbc = rbc  # Right boundary condition ('d', 'n', 'p', 'pab')
        self.dl = dl    # Dielectric layer indicator ('y' if present, 'n' otherwise)

        self.ylabel = None  # left side y label  (boundary condition)
        self.y2label = None # right side y label
        
        """
        Set up the simulation parameters and matrices.
        """
        self.x = np.arange(0, 200, 1)                           # number of grid points
        self.m = 11*np.exp(-(self.x-50)**2/2/5**2)              # Initial pulse wave
        self.c = 1                                              # wave velocity
        self.dx = 1                                             # grid spacing
        self.dt = self.dx/self.c/np.sqrt(2)                     # time step size
        self.lamb = self.c*self.dt/self.dx                      # lambda, Courant's number
        self.lamb2 = self.lamb**2                               # square of lambda
        self.diag = np.full(len(self.m), 2-2*self.lamb2)        # main diagonal of lambda matrix
        self.up_low_diag = np.full(len(self.m) - 1, self.lamb2) # upper and lower main diagonals
        # Definition of the standard tridiagonal lambda matrix
        self.L = np.diag(self.up_low_diag, -1) + np.diag(self.diag, 0) + np.diag(self.up_low_diag, 1)

        # if we are simulating a "dieletric layer"
        if self.dl == 'y':
            dl_lamb2 = (self.lamb*0.7)**2       # dieletric layer's squared lambda (30% off in velocity)

            # we fill the lambda matrix tridiagonal with the lambda from the dieletric layer
            # located in the third quarter of the x axis
            for i in range(int(len(self.m)/2),int(len(self.m)*3/4)):
                self.L[i,i] = 2-2*dl_lamb2
                self.L[i-1,i] = dl_lamb2
                self.L[i+1,i] = dl_lamb2
           
        # periodic boundary condition (if one side is 'p' then both are set 'p')
        if self.lbc == 'p' or self.rbc == 'p':
            self.m[len(self.m)-1] = self.m[0]                               # left
            self.L[0,len(self.m)-2] = self.L[len(self.m)-1,1] = self.lamb2  # right
            self.lbc = self.rbc = 'p'                                       # both are set 'p'
            self.ylabel = 'Periodic Boundary'                               # left y label
            self.y2label = self.ylabel                                      # right y label

        # Dirichlet boundary condition
        if self.lbc == 'd':                             # left
            self.L[0,0] = 2
            self.L[0,1] = 0
            self.ylabel = 'Dirichlet Boundary'          # left y label
        if self.rbc == 'd':                             # right
            self.L[len(self.m)-1,len(self.m)-1] = 2
            self.L[len(self.m)-1,len(self.m)-2] = 0
            self.y2label = 'Dirichlet Boundary'         # right y label
            
        # Neumann boundary condition
        if self.lbc == 'n':                                     # left
            self.L[0,1] = 2*self.lamb2
            self.ylabel = 'Neumann Boundary'                    # left y label
        if self.rbc == 'n':                                     # right
            self.L[len(self.m)-1,len(self.m)-2] = 2*self.lamb2  
            self.y2label = 'Neumann Boundary'                   # right y label

        # Perfect Absorbing Boundary (PAB)
        if self.lbc == 'pab':                                                   # left
            self.L[0,0] = (2-2*self.lamb2)/(1+self.lamb)
            self.L[0,1] = 2*self.lamb2/(1+self.lamb)
            self.ylabel = 'Perfect Absorbing Boundary'                          # left y label
        if self.rbc == 'pab':                                                   # right
            self.L[len(self.m)-1,len(self.m)-1] = (2-2*self.lamb2)/(1+self.lamb)
            self.L[len(self.m)-1,len(self.m)-2] = 2*self.lamb2/(1+self.lamb)
            self.y2label = 'Perfect Absorbing Boundary'                         # right y label
           
        self.m_old = self.m                         # store the previous values
        self.m = 1/2*np.matmul(self.L, self.m_old)  # calculates the first (special) time step (du/dt=0)
        
    def step(self):
        """
        Perform one simulation step.
        """
        m_temp = self.m                                                 # store the initial values
        if self.rbc == 'pab':                                           # if PAB then the vector of the previous values must be modified
            self.m_old[len(self.m)-1] *= (1-self.lamb)/(1+self.lamb)    # left side
        if self.lbc == 'pab':                                           # the same as above (right side)
            self.m_old[0] *= (1-self.lamb)/(1+self.lamb)
        self.m = np.matmul(self.L, m_temp) - self.m_old                 # calculation of the next values
        self.m_old = m_temp                                             # the initial values are now the old ones

    def animate(self, frame):
        """
        Update the animation for each frame.
        Parameters:
        - frame (int): Frame number.
        """
        self.step()             # make a timestep
        line.set_ydata(self.m)  # refresh the line values
        return line,            # return the new line for plotting

def parse_arguments():
    """
    Parse command-line arguments.
    Returns:
    - args: Parsed command-line arguments.
    """
    parser = argparse.ArgumentParser(description='1D Wave Simulation')
    parser.add_argument('--lbc', type=str.lower, default='n', nargs='?', metavar='Left Boundary Condition', choices=['d', 'n', 'p', 'pab'], help='Left Boundary Condition')
    parser.add_argument('--rbc', type=str.lower, default='pab', nargs='?', metavar='Right Boundary Condition', choices=['d', 'n', 'p', 'pab'], help='Right Boundary Condition')
    parser.add_argument('--dl', type=str.lower, default='y', nargs='?', metavar='Dielectric layer in the path?', choices=['y', 'n'], help='Dielectric layer in the path or not?')
    return parser.parse_args()

# Execute the main code only if this script is run directly, not when imported as a module
if __name__ == "__main__":
    
    args = parse_arguments()                                # get the command line arguments

    wave_sim = WaveSimulation(args.lbc, args.rbc, args.dl)  # create the simulation object with the input arguments

    fig, ax = plt.subplots()            # create the plot figure
    fig.suptitle('1D Wave Equation')    # figure title
    ax.set_xlim(0, len(wave_sim.m))     # x axis limits
    ax.set_xticks([])                   # no ticks in x
    ax.set_ylim(-10, 10)                # y axis limits
    ax.set_yticks([])                   # no ticks in y
    secy = ax.secondary_yaxis('right')  # secondary y axis
    secy.set_yticks([])                 # no ticks in the secondary y axis
    ax.set_ylabel(wave_sim.ylabel)      # define the y label
    secy.set_ylabel(wave_sim.y2label)   # define the secondary y label

    line, = ax.plot(wave_sim.x, wave_sim.m) # plot the initial line

    # If the dielectric layer is on, plot vertical lines at the interfaces
    if args.dl == 'y':
        fig.suptitle('1D Wave simulation with a "Dielectric layer"')
        line2, = ax.plot([100,100],[-10,10], color='orange', linewidth='1', linestyle='--')
        line3, = ax.plot([150,150],[-10,10], color='orange', linewidth='1', linestyle='--')
    else:
        fig.suptitle('1D Wave simulation')

    # define the animation
    ani = animation.FuncAnimation(fig, wave_sim.animate, interval=10, blit=True, save_count=1000)
    
    #ani.save('1D_wave.mp4')    # Uncomment this line if you want to save a mp4 movie

    plt.show()                  # finally shows the plot
