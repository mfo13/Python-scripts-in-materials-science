"""
2D Schrodinger's equation simulation without the potential term

Author: Marcelo Falcão de Oliveira
Affiliation: University of São Paulo (USP)
             São Carlos School of Engineering (EESC)
             Materials Engineering Department (SMM)
Contact: marcelo.falcao@usp.br

Description:
It illustrates the solution of the Schrodinger's equation in 2D with the 
FDM method and Crank-Nicolson scheme without the potential term. 
The user can choose among 3 classical boundary conditions.

License:
MIT License (https://opensource.org/licenses/MIT)

Purpose:
Educational tool for demonstrating the FDM solution of 2D Schrodinger's equation.

Packages needed:
argparse, matplotlib, numpy

Usage:
$ python 2D_wave.py --lbc <arg1> --rbc <arg2> --ubc <arg3> --bbc <arg4>
Optional arguments:
- <arg1> left boundary conditions, a value among 'd', 'n', 'p' (default: d)
- <arg2> right boundary conditions, same as above
- <arg3> upper boundary conditions, same as above
- <arg4> bottom boundary conditions, same as above
- Use 'python 2D_Schrodinger_0V.py -h' for help.

p.s. d-Dirichlet, n-Neumann, p-periodic

Date: February/2024
Version: 1.0
"""

import argparse                                 # Module for parsing command-line arguments
import numpy as np                              # Library for numerical computations
import matplotlib.pyplot as plt                 # Module for plotting
import matplotlib.colors as mcolors             # Color handling in plots
from matplotlib.animation import FuncAnimation  # Animation functionality in plots

class AnimatedPcolormesh:
    '''
    Class for calculation and animation of the plots
    '''
    def __init__(self, x, y, args):
        '''
        Initialize the WaveSimulation object with given boundary conditions.
        x - number of grid points in x
        y - number of grid points in y
        args - arguments for the boundary conditions

        To understand how matrices, vectors and boundary conditions work refer to the lecture documentation. 
        '''
        self.args = args                                                # gets the arguments passed by the user        
        self.X, self.Y = np.meshgrid(x, y)                              # creates the 2D coordinate grid according to the number of points in x and y
        self.m = np.ndarray(shape=(len(x),len(y)), dtype='complex')     # creates the 2D matrix of complex values for the wave function

        # Initial wave function ('particle' size and momentum), change as you want
        # It is a Gaussian pulse (first part) together with some momentum (second part)
        # ------------------------------------------------------------------------------
        # High energy (momentum) particle
        self.m = np.exp(-((self.Y)**2+(self.X+0.6)**2)**2/0.1**2)*np.exp(1j*80*((self.X+0.6)/2))
        # Low energy (momentum) particle
        #self.m = np.exp(-((self.Y)**2+(self.X+0.6)**2)**2/0.1**2)*np.exp(1j*10*((self.X+0.6)/2))
        
        # Bouncing particle (comment the grid barrier bellow)
        # call the script with --ybc d
        #self.m = np.exp(-((self.Y)**2+(self.X+0.5)**2)**2/0.1**2)*np.exp(1j*50*((self.X+0.5)/2-self.Y))

        # standing wave (comment the grid barrier bellow)
        #self.m = np.exp(1j*self.X*np.pi).imag*np.exp(1j*self.Y*np.pi).imag
        #---------------------------------------------------------------------------

        self.vi = []                    # positions that will be set to zero for barriers                                                     
        self.vj = []

        # Grid barrier
        # we create here 3 round barriers of our diffraction grid
        # we store the positions of the matrix to make the code faster
        for i in range(self.X.shape[0]):
            for j in range(self.X.shape[1]):
                if np.sqrt((self.X[i,j])**2+(self.Y[i,j])**2) < 0.1:
                    self.vi.append(i)
                    self.vj.append(j)
                if np.sqrt((self.X[i,j])**2+(self.Y[i,j]-0.35)**2) < 0.1:
                    self.vi.append(i)
                    self.vj.append(j)
                if np.sqrt((self.X[i,j])**2+(self.Y[i,j]+0.35)**2) < 0.1:
                    self.vi.append(i)
                    self.vj.append(j)

        # we force all selected positions to be zero (Dirichlet boundary)
        for n in range(len(self.vi)):
            self.m[self.vi[n],self.vj[n]] = 0

        self.fig, self.ax = plt.subplots(1, 3, figsize=(12,4), layout='constrained')    # initialize the figure with 3 plot areas
        self.fig.suptitle('2D Schrodinger\'s equation simulation')                      # figure title

        self.pcmr = self.ax[0].pcolormesh(self.X, self.Y, self.m.real, vmin=-1, vmax=1 , cmap='twilight')   # colormesh of the real wave part in plot area 0

        colors1 = plt.cm.bone_r(np.linspace(0., 1, 128))                            # we take half of the inverted 'bone' colormap
        colors2 = plt.cm.pink(np.linspace(0, 1, 128))                               # we take half of the 'pink' colormap
        colors = np.vstack((colors1, colors2))                                      # we combine the previous half colormaps into one
        mycmap = mcolors.LinearSegmentedColormap.from_list('my_colormap', colors)   # we create a new colormap

        self.pcmi = self.ax[1].pcolormesh(self.X, self.Y, self.m.real, vmin=-1, vmax=1, cmap=mycmap)                            # colormesh of the imaginary part of the wave in plot area 1
        self.pcmd = self.ax[2].pcolormesh(self.X, self.Y, (np.conjugate(self.m)*self.m).real, vmin=0, vmax=1, cmap='viridis')   # colormesh of the probability density in plot area 2
        
        for i in range(len(self.ax)):   # we erase all ticks of all plots
            self.ax[i].set_xticks([])
            self.ax[i].set_yticks([])

        self.ax[0].set_title(r'$\psi_{real}$')          # plot 0 title
        self.ax[1].set_title(r'$\psi_{imag}$')          # plot 1 title
        self.ax[2].set_title(r'$|\psi|^2$')             # plot 2 title
        self.secx = self.ax[0].secondary_xaxis('top')   # secondary x axis for plot 0
        self.secy = self.ax[0].secondary_yaxis('right') # secondary y axis for plot 1
        self.secx.set_xticks([])                        # erase ticks of secondary axis
        self.secy.set_yticks([])
        self.lbclabel = 'Dirichlet boundary'            # label for left bondary condition
        self.rbclabel = 'Dirichlet boundary'            # label for right bondary condition
        self.ubclabel = 'Dirichlet boundary'            # label for upper bondary condition
        self.bbclabel = 'Dirichlet boundary'            # label for bottom bondary condition
                        
        self.dx = self.dy = 1                                  # grid spacing
        self.dt = self.dx**2*2                                 # time step size
        self.lamb = 1j*self.dt/self.dx**2                      # lambda
        
        Ldiag = np.full(len(self.m), np.sqrt(1+2*self.lamb))                  # main diagonal of lambda matrix for implicit terms
        Loffdiag = np.full(len(self.m)-1, -self.lamb/2)                       # upper/lower diagonals of lambda matrix for implicit terms
        self.Lx =  np.diag(Loffdiag,-1)+np.diag(Ldiag,0)+np.diag(Loffdiag,1)  # lambda tridiagonal matrix for x direction for implicit terms
        self.Ly =  np.diag(Loffdiag,-1)+np.diag(Ldiag,0)+np.diag(Loffdiag,1)  # lambda tridiagonal matrix for y direction for implicit terms

        Rdiag = np.full(len(self.m), np.sqrt(1-2*self.lamb))                  # main diagonal of lambda matrix for explicit terms
        Roffdiag = np.full(len(self.m)-1, self.lamb/2)                        # upper/lower diagonals of lambda matrix for explicit terms
        self.Rx =  np.diag(Roffdiag,-1)+np.diag(Rdiag,0)+np.diag(Roffdiag,1)  # lambda tridiagonal matrix of explicit terms for x direction
        self.Ry =  np.diag(Roffdiag,-1)+np.diag(Rdiag,0)+np.diag(Roffdiag,1)  # lambda tridiagonal matrix of explicit terms for y direction
        
        self.bc()       # apply the boundary conditions
            
        self.ax[0].set_xlabel(self.bbclabel, loc='right', fontsize=8)     # set x label bc for plot 0
        self.ax[0].set_ylabel(self.lbclabel, loc='bottom', fontsize=8)    # set y label bc for plot 0
        self.secx.set_xlabel(self.ubclabel, loc='left', fontsize=8)       # set x secondary label for plot 0
        self.secy.set_ylabel(self.rbclabel, loc='top', fontsize=8)        # set y secondary label for plot 0
   
    def bc(self):
        '''
        Function to apply the chosen boundary conditions different from Dirichlet
        '''
        # Neumann
        if self.args.lbc == 'n':
            self.Lx[0,1] *= 2
            self.Rx[0,1] *= 2
            self.lbclabel = 'Neumann boundary'
        if self.args.rbc == 'n':
            self.Lx[len(self.m)-1,len(self.m)-2] *= 2
            self.Rx[len(self.m)-1,len(self.m)-2] *= 2
            self.rbclabel = 'Neumann boundary'
        if self.args.ubc == 'n':
            self.Ly[0,1] *= 2
            self.Ry[0,1] *= 2
            self.ubclabel = 'Neumann boundary'
        if self.args.bbc == 'n':
            self.Ly[len(self.m)-1,len(self.m)-2] *= 2
            self.Ry[len(self.m)-1,len(self.m)-2] *= 2
            self.bbclabel = 'Neumann boundary'
        
        # Periodic
        if self.args.lbc == 'p' or self.args.rbc == 'p':
            self.Lx[0,len(self.m)-1] = -self.lamb/2
            self.Lx[len(self.m)-1,0] = -self.lamb/2
            self.Rx[0,len(self.m)-1] = self.lamb/2
            self.Rx[len(self.m)-1,0] = self.lamb/2
            self.lbclabel = 'Periodic boundary'
            self.rbclabel = 'Periodic boundary'
        if self.args.ubc == 'p' or self.args.bbc == 'p':
            self.Ly[0,len(self.m)-1] = -self.lamb/2
            self.Ly[len(self.m)-1,0] = -self.lamb/2
            self.Ry[0,len(self.m)-1] = self.lamb/2
            self.Ry[len(self.m)-1,0] = self.lamb/2
            self.ubclabel = 'Periodic boundary'
            self.bbclabel = 'Periodic boundary'
    
    def update(self, frame):
        '''
        Function to solve the Schrodinger's equation, update the matrix and the colormeshes
        '''

        # solve the matricial equation, in this case, 
        # Ly.Ynew.Lx = Ry.Yold.Rx
        # thus,
        # Ynew = Ly^-1.(Ry.Yold.Rx).Lx^-1
        # where Ly and Lx are the lambda matrices for implicit terms of x and y directions,
        # Ry and Rx are the matrices for explicit terms, Yold is the old wave matrix and 
        # Ynew is the new wave matrix                                                 
        self.m = np.linalg.inv(self.Ly)@(self.Ry@self.m@self.Rx)@np.linalg.inv(self.Lx)

        # we reimpose the barrier positions (Dirichlet condition)
        for n in range(len(self.vi)):
            self.m[self.vi[n],self.vj[n]] = 0
                                       
        temparr = self.m.real.ravel()                   # gets the wave real part
        self.pcmr.set_array(temparr)                    # updates the plot colormesh array

        # uncomment these lines if you want colormap limits updating for plot 0
        #maxabs = max(np.abs(temparr))
        #self.pcmr.set_clim(vmin=-maxabs, vmax=maxabs)

        temparr = self.m.imag.ravel()                   # gets the wave real part
        self.pcmi.set_array(temparr)                    # updates the plot colormesh array

        # uncomment these lines if you want colormap limits updating for plot 1
        #maxabs = max(np.abs(temparr))
        #self.pcmi.set_clim(vmin=-maxabs, vmax=maxabs)

        temparr = (np.conjugate(self.m)*self.m).real.ravel()    # recalculates the probability density
        self.pcmd.set_array(temparr)                            # updates the plot colormesh array

        # uncomment these lines if you want colormap limits updating for plot 2
        #maxabs = max(temparr)
        #self.pcmd.set_clim(vmax=maxabs)
        
        return self.pcmr, self.pcmi, self.pcmd                  # returns the updated colormeshes

    def animate(self):
        '''
        Function to animate the plots
        '''
        animation = FuncAnimation(self.fig, self.update, frames=None, interval=1, blit=True, save_count=300)

        # uncomment this line if you want to save a mp4 movie
        #animation.save('2D_Schrodinger_0V.mp4', fps=20)

        plt.show()      # show the figure

def parse_arguments():
    """
    Parse command-line arguments.
    Returns:
    - args: Parsed command-line arguments.
    """
    chois = ['d','n','p']
    parser = argparse.ArgumentParser(description='2D Schrodinger\'s equation simulation')
    parser.add_argument('--lbc', type=str.lower, default='d', nargs='?', metavar='Left Boundary Condition', choices=chois, help='Left Boundary Condition')
    parser.add_argument('--rbc', type=str.lower, default='d', nargs='?', metavar='Right Boundary Condition', choices=chois, help='Right Boundary Condition')
    parser.add_argument('--ubc', type=str.lower, default='d', nargs='?', metavar='Upper Boundary Condition', choices=chois, help='Upper Boundary Condition')
    parser.add_argument('--bbc', type=str.lower, default='d', nargs='?', metavar='Bottom Boundary Condition', choices=chois, help='Bottom Boundary Condition')
    return parser.parse_args()
    
# Execute the main code only if this script is run directly, not when imported as a module
if __name__ == "__main__":
    
    args = parse_arguments()                                      # gets the command line arguments
    
    x_values = np.linspace(-1,1,200)                              # number of grid points in x
    y_values = x_values                                           # same for y
    animated_plot = AnimatedPcolormesh(x_values, y_values, args)  # creates the animation instance
    animated_plot.animate()                                       # start the animation
