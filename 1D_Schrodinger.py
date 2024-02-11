"""
1D Schrodinger's Equation Simulation

Author: Marcelo Falcão de Oliveira
Affiliation: University of São Paulo (USP)
             São Carlos School of Engineering (EESC)
             Materials Engineering Department (SMM)
Contact: marcelo.falcao@usp.br

Description:
It ilustrates the solution of the time-dependent Schrodinger's 
equation in 1D by the FDM method and Crank-Nicolson scheme.
The user can choose among 3 classical boundary conditions 
as well as the presence or not of a potential barrier in the
trajectory.

License:
MIT License (https://opensource.org/licenses/MIT)

Purpose:
Educational tool for demonstrating the FDM solution of 1D Schrodinger's equation.

Packages needed:
argparse, matplotlib, numpy

Usage:
$ python 1D_wave_function.py --lbc <arg1> --rbc <arg2> --bar <arg3>
Optional arguments:
- <arg1> left boundary condition, a value among 'd', 'n' and 'p' (default: d)
- <arg2> right boundary condition, same as above (default: d)
- <arg3> 'y' or 'n' for a potential barrier in the wave path (default: y)
- Use 'python 1D_wave_function.py -h' for help.

p.s. d-Dirichlet, n-Neumann, p-periodic

Date: February/2024
Version: 1.0

"""

import argparse                             # Module for parsing command-line arguments
import numpy as np                          # Numerical operations using arrays
import matplotlib.pyplot as plt             # Plotting library
import matplotlib.animation as animation    # Animation functionality


class WaveSimulation:
    def __init__(self, args):
        """
        Initialize the WaveSimulation object with given boundary conditions.
        Parameters:
        - lbc (str): Left boundary condition ('d', 'n', 'p').
        - rbc (str): Right boundary condition ('d', 'n', 'p').
        
        To understand how matrices, vectors and boundary conditions work refer to the lecture documentation. 
        """
        self.args = args  # Left boundary condition ('d', 'n', 'p')
                       
        self.ylabel = None  # left side y label  (boundary condition)
        self.y2label = None # right side y label (boundary condition)
        
        """
        Set up the simulation parameters and matrices.
        """
        self.x = np.linspace(-1, 1, 500)                           # number of grid points
        self.m = np.ndarray(shape=(len(self.x)), dtype='complex')  # grid of complex numbers

        # Initial pulse wave (change as you want)
        self.m = np.exp(-(self.x+0.6)**2/2/0.1**2)*np.exp(1j*20*(self.x+0.6))            
        
        self.dx = (max(self.x)-min(self.x))/len(self.x)            # grid spacing
        self.dt = self.dx**2*10                                    # time step size
        self.lamb = 1j*self.dt/2/self.dx**2                        # lambda 
        self.nu = 1j*self.dt/2                                     # nu

        self.V = np.zeros(len(self.x))                             # potential grid full of zeros  

        # potential barrier if chosen
        if self.args.bar == 'y':
            self.Ve = 0.3           # left position
            self.Vr = 0.5           # right position
            wl = 500                # potential
            # we fill the V grid with wl between Ve and Vr
            for i in range(np.int_((self.Ve+1)*len(self.x)/2),np.int_((self.Vr+1)*len(self.x)/2)):
                self.V[i] = wl
                
        self.Ldiag = np.full(len(self.x),1+self.lamb) + self.nu*self.V                  # main diagonal of L
        self.Rdiag = np.full(len(self.x),1-self.lamb) - self.nu*self.V                  # main diagonal of R
        Loffdiag = np.full(len(self.m)-1, -self.lamb/2)                                 # upper/lower diagonals of L
        self.L =  np.diag(Loffdiag,-1)+np.diag(self.Ldiag,0)+np.diag(Loffdiag,1)        # tridiagonal matrix of L
        Roffdiag = np.full(len(self.m)-1, self.lamb/2)                                  # upper/lower diagonals of lambda matrix for explicit terms
        self.R =  np.diag(Roffdiag,-1)+np.diag(self.Rdiag,0)+np.diag(Roffdiag,1)        # tridiagonal matrix of R

        self.applybc()                                  # apply de bondary conditions

        self.m_old = self.m                             # store the previous values of the grid

        self.pd =  (np.conjugate(self.m)*self.m).real   # calculates the grid of probability densities
     
    def applybc(self):
        '''
        Apply the bondary conditions
        '''
        if self.args.lbc == 'd' and self.args.rbc != 'p':
            self.L[0,0] = 1
            self.L[0,1] = 0
            self.R[0,0] = 1
            self.R[0,1] = 0            
            self.ylabel = 'Dirichlet boundary'
        if self.args.rbc == 'd' and self.args.lbc != 'p':
            self.L[len(self.m)-1,len(self.m)-1] = 1
            self.L[len(self.m)-1,len(self.m)-2] = 0
            self.R[len(self.m)-1,len(self.m)-1] = 1
            self.R[len(self.m)-1,len(self.m)-2] = 0
            self.y2label = 'Dirichlet boundary'
        if self.args.lbc == 'n' and self.args.rbc != 'p':
            self.L[0,1] = -self.lamb
            self.R[0,1] = self.lamb
            self.ylabel = 'Neumann boundary'
        if self.args.rbc == 'n'and self.args.lbc != 'p':
            self.L[len(self.m)-1,len(self.m)-2] = -self.lamb
            self.R[len(self.m)-1,len(self.m)-2] = self.lamb
            self.y2label = 'Neumann boundary'
        if self.args.lbc == 'p' or self.args.rbc == 'p': 
            self.L[0,len(self.m)-2] = -self.lamb/2
            self.L[len(self.m)-1,1] = -self.lamb/2
            self.R[0,len(self.m)-2] = self.lamb/2
            self.R[len(self.m)-1,1] = self.lamb/2
            self.ylabel = 'Periodic boundary'
            self.y2label = 'Periodic boundary'
     
    def step(self):
        """
        Perform one simulation step.
        """
        m_temp = self.m                                                       # store the initial values
        self.m = np.matmul(np.linalg.inv(self.L),np.matmul(self.R,m_temp))  # solves the matricial equation
        self.m_old = m_temp                                                   # the initial values are now the old ones

    def animate(self, frame):
        """
        Update the animation for each frame.
        Parameters:
        - frame (int): Frame number.
        """
        self.step()                                     # make a timestep
        line.set_ydata(self.m.real)                     # refresh the real line values
        line2.set_ydata(self.m.imag)                    # refresh the imaginary line values
        self.pd = (np.conjugate(self.m)*self.m).real    # recalculates the probability densities
        line3.set_ydata(self.pd)                        # refresh the probability density lin/e
        return line, line2, line3,                      # return the new lines for plotting

def parse_arguments():
    """
    Parse command-line arguments.
    Returns:
    - args: Parsed command-line arguments.
    """
    parser = argparse.ArgumentParser(description='1D Wave Function Animation')
    parser.add_argument('--lbc', type=str.lower, default='d', nargs='?', metavar='Left Boundary Condition', choices=['d', 'n', 'p'], help='Left Boundary Condition')
    parser.add_argument('--rbc', type=str.lower, default='d', nargs='?', metavar='Right Boundary Condition', choices=['d', 'n', 'p'], help='Right Boundary Condition')
    parser.add_argument('--bar', type=str.lower, default='y', nargs='?', metavar='Potential barrier in the path?', choices=['y', 'n'], help='Potential barrier in the path??')
    return parser.parse_args()

# Execute the main code only if this script is run directly, not when imported as a module
if __name__ == "__main__":
    
    args = parse_arguments()          # get the command line arguments

    wave_sim = WaveSimulation(args)  # create the simulation object with the input arguments

    fig, ax = plt.subplots(1, 2, figsize=(12,4), layout='constrained')  # set up two plot areas
    fig.suptitle('1D Schrodinger\'s Equantion')                         # figure title
    ax[0].set_xlim(-1, 1)                                               # x axis limits for plot 0
    ax[0].set_xticks([])                                                # no ticks in x
    ax[0].set_ylim(-1, 1)                                               # y axis limits
    ax[0].set_yticks([])                                                # no ticks in y
    ax[1].set_xlim(-1, 1)                                               # all the same applies for plot 1
    ax[1].set_xticks([])                   
    ax[1].set_ylim(0, 1)                
    ax[1].set_yticks([])   

    secy = ax[0].secondary_yaxis('right')   # secondary y axis for plot 0
    secy.set_yticks([])                     # no ticks in the secondary y axis
    ax[0].set_ylabel(wave_sim.ylabel)       # define the y label for plot 0
    secy.set_ylabel(wave_sim.y2label)       # define the secondary y label for plot 0

    ax[0].set_title(r'$\psi$')              # title for plot 0
    ax[1].set_title(r'$|\psi|^2$')          # title for plot 1

    x0, = ax[0].plot([-1,1],[0,0], color='lightgray', linestyle='dotted')   # dotted line at y=0 for plot 0
    line, = ax[0].plot(wave_sim.x, wave_sim.m.real, label='real')           # plot the initial real line
    line2, = ax[0].plot(wave_sim.x, wave_sim.m.imag, label='imag')          # plot the initial imaginary line
    line3, = ax[1].plot(wave_sim.x, wave_sim.pd, color='green')             # plot the initial probability density

    ax[0].legend(handles=[line, line2])                                     # add legends for real and imaginary plots

    # If the potential barrier layer is on, plot vertical lines at the interfaces and changes figure title
    if args.bar == 'y':
        fig.suptitle('1D Schrodinger\'s Equation with potential barrier')
        ax[0].plot([wave_sim.Ve,wave_sim.Ve],[-1,1], color='purple', linestyle='dotted')
        ax[0].plot([wave_sim.Vr,wave_sim.Vr],[-1,1], color='purple', linestyle='dotted')
        ax[1].plot([wave_sim.Ve,wave_sim.Ve],[-1,1], color='purple', linestyle='dotted')
        ax[1].plot([wave_sim.Vr,wave_sim.Vr],[-1,1], color='purple', linestyle='dotted') 

    # define the animation
    ani = animation.FuncAnimation(fig, wave_sim.animate, interval=10, blit=True, save_count=1500)
    
    #ani.save('1D_Schrodinger.mp4')    # Uncomment this line if you want to save a mp4 movie

    plt.show()                  # finally shows the plot
