"""
2D Schrodinger's equation simulation

Author: Marcelo Falcão de Oliveira
Affiliation: University of São Paulo (USP)
             São Carlos School of Engineering (EESC)
             Materials Engineering Department (SMM)
Contact: marcelo.falcao@usp.br

Description:
It ilustrates the solution of the Schrodinger's equation in 2D with the
FDM method and Crank-Nicolson scheme with large sparse matrices.
The user can choose among 3 classical boundary conditions. 

License:
MIT License (https://opensource.org/licenses/MIT)

Purpose:
Educational tool for demonstrating the FDM solution of 2D Schrodinger's equation.

Packages needed:
argparse, matplotlib, numpy, scipy

Usage:
$ python 2D_Schrodinger.py --lbc <arg1> --rbc <arg2> --ubc <arg1> --bbc <arg2>
Optional arguments:
- <arg1> left boundary condition, a value among 'd', 'n', 'p' (default: d)
- <arg2> right boundary condition, same as above
- <arg3> upper boundary condition, same as above
- <arg4> bottom boundary condition, same as above
- Use 'python 2D_Schrodinger.py -h' for help.

p.s. d-Dirichlet, n-Neumann, p-periodic

Date: February/2024
Version: 1.0
"""

# Import the argparse module for parsing command-line arguments
import argparse
# Import NumPy library
import numpy as np
# Import specific function from scipy to build diagonal sparse matrices
from scipy.sparse import spdiags
# Import specific functions from scipy.sparse.linalg module to fast solve matrix equation
from scipy.sparse.linalg import factorized, LinearOperator, aslinearoperator
# Import pyplot module from matplotlib library
import matplotlib.pyplot as plt
# Import specific module from matplotlib.colors
import matplotlib.colors as mcolors
# Import specific class from matplotlib.animation
from matplotlib.animation import FuncAnimation

class AnimatedPcolormesh:
    '''
    Class for calculation and animation of the plots
    '''
    def __init__(self, side_points, args):
        '''
        Initialize the WaveSimulation object with given boundary conditions.
        side_points - number of grid points in one direction
        args - arguments for the boundary conditions

        To understand how matrices, vectors and boundary conditions work refer to the lecture documentation. 
        '''
        # Initial setups
        #----------------
        self.args = args                                                     # gets the arguments passed by the user        
        self.X, self.Y = np.meshgrid(side_points, side_points)               # creates the 2D coordinate grid according to the number of points in x and y
        self.m = np.ndarray((len(self.X), len(self.Y)), dtype='complex')     # creates the 2D matrix of complex values for the wave function
        self.V = np.zeros(self.m.shape, dtype='complex')                     # we create the potential matrix full of zeros

        self.dx = 2/len(self.X)                                 # grid spacing
        self.dt = self.dx**2*2                                  # time step size
        self.lamb = 1j*self.dt/2/self.dx**2                     # lambda 
        self.nu = 1j*self.dt                                    # nu

        # Initial wave function ('particle' size and momentum), change as you want
        #---------------------------------------------------------------------------
        # It is a Gaussian pulse (first part) together with some momentum (second part)
        # high energy particle
        self.m = np.exp(-((self.Y)**2+(self.X+0.6)**2)**2/0.1**2)*np.exp(1j*80*((self.X+0.6)/2))
        # low energy particle
        #self.m = np.exp(-((self.Y)**2+(self.X+0.6)**2)**2/0.1**2)*np.exp(1j*15*((self.X+0.6)/2))

        # Diffraction grid fill it as you want
        #---------------------------------------
        # we create here 5 round "transparent" potential wells of our diffraction grid
        # along 2 parallel walls
        gridpot = 5e2
        radius = 0.1
        for i in range(self.X.shape[0]):
            for j in range(self.X.shape[1]):
                if np.sqrt((self.X[i,j]+1/6)**2+(self.Y[i,j])**2) < radius:
                    self.V[i,j] = gridpot
                if np.sqrt((self.X[i,j]+1/6)**2+(self.Y[i,j]-1/3)**2) < radius:
                    self.V[i,j] = gridpot
                if np.sqrt((self.X[i,j]+1/6)**2+(self.Y[i,j]+1/3)**2) < radius:
                    self.V[i,j] = gridpot
                if np.sqrt((self.X[i,j]-1/6)**2+(self.Y[i,j]+1/6)**2) < radius:
                    self.V[i,j] = gridpot
                if np.sqrt((self.X[i,j]-1/6)**2+(self.Y[i,j]-1/6)**2) < radius:
                    self.V[i,j] = gridpot
                if np.sqrt((self.X[i,j]-1/6)**2+(self.Y[i,j]+1/2)**2) < radius:
                    self.V[i,j] = gridpot
                if np.sqrt((self.X[i,j]-1/6)**2+(self.Y[i,j]-1/2)**2) < radius:
                    self.V[i,j] = gridpot

        # absorbing potential layers
        # to partially cancel the waves at the simulation box bondaries
        cut = 0.9
        mult = 2e5
        power = 2
        for i in range(self.X.shape[0]):
            for j in range(self.X.shape[1]):
                # left
                if self.X[i,j] < -cut:
                    sigma = (-self.X[i,j]-cut)**power
                    self.V[i,j] = mult*(1-np.exp(1j*sigma))
                # right
                # if self.X[i,j] > cut:
                #     sigma = (self.X[i,j]-cut)**power
                #     self.V[i,j] = mult*(1-np.exp(1j*sigma))
                # bottom
                if self.Y[i,j] < -cut:
                    sigma = (-self.Y[i,j]-cut)**power
                    self.V[i,j] = mult*(1-np.exp(1j*sigma))
                # up
                if self.Y[i,j] > cut:
                    sigma = (self.Y[i,j]-cut)**power
                    self.V[i,j] = mult*(1-np.exp(1j*sigma))

        # # parabolic well
        # raio = np.sqrt((self.X)**2+(self.Y)**2)-0.5        
        # self.m = np.exp(-(raio**2/0.1**2))
        # for i in range(len(self.m)):
        #     for j in range(len(self.m)):
        #         self.V[i,j] = 1000*np.sqrt(self.X[i,j]**2+self.Y[i,j]**2)**2

        # # standing waves (deactivate the potential matrix)
        # self.m = np.exp(1j*self.X*np.pi/2).real*np.exp(1j*self.Y*np.pi/2).real
        # self.m = np.exp(1j*self.X*np.pi).imag*np.exp(1j*self.Y*np.pi).imag
        # self.m = np.exp(1j*self.X*3/2*np.pi).real*np.exp(1j*self.Y*3/2*np.pi).real
        #---------------------------------------------------------------------------

        # Figure and plot setups
        #-----------------------
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
        self.bbclabel = 'Dirichlet'                     # label for bottom bondary condition
        self.ubclabel = 'Dirichlet'                     # label for upper bondary condition
        self.rbclabel = 'Dirichlet'                     # label for right bondary condition
        self.lbclabel = 'Dirichlet'                     # label for left bondary condition
        
        # Matrices construction
        ########################            
        L = np.full(self.m.shape, 1+self.lamb) + self.nu/2*self.V       # matrix of Ls
        R = np.full(self.m.shape, 1-self.lamb) - self.nu/2*self.V       # matrix of Rs

        # Assembly of L and R blocks
        subupL = np.full(len(self.m), -self.lamb/2) # upper off diagonal blocks for Ls  
        subbotL = subupL.copy()
        subupL[-1] = 0                              # block division for up off diagonal for Ls
        subbotL[-1] = 0                             # block division for bottom off diagonal for Ls
        subupR = np.full(len(self.m), self.lamb/2)  # upper off diagonal blocks for Rs
        subbotR = subupR.copy() 
        subupR[-1] = 0                              # block division for up off diagonal for Rs
        subbotR[-1] = 0                             # block division for bottom off diagonal for Rs

        yupdiagE = np.tile(np.full(len(self.m), -self.lamb/2), len(self.m)-1)  # y off diagonals for E 
        ybotdiagE = yupdiagE.copy()              
        yupdiagD = np.tile(np.full(len(self.m), self.lamb/2), len(self.m)-1)   # y off diagonals for D
        ybotdiagD = yupdiagD.copy()

        # Set all boundary conditions before setting the sparse matrices
        # Dirichlet don't need any change
        # Neumann
        if self.args.lbc == 'n' and self.args.rbc != 'p':                
            subupL[0] *= 2                                      # all left side of off diagonal blocks are double for Neumann
            subupR[0] *= 2
            self.lbclabel = 'Neumann'
        if self.args.rbc == 'n' and self.args.lbc != 'p':                
            subbotL[-2] *= 2                                    # all right side of off diagonal blocks are double for Neumann
            subbotR[-2] *= 2
            self.rbclabel = 'Neumann'
        if self.args.ubc == 'n' and self.args.bbc != 'p':
            yupdiagE[:len(self.m)] *= 2                         # the first block of y diagonal is double for Neumann
            yupdiagD[:len(self.m)] *= 2
            self.ubclabel = 'Neumann'
        if self.args.bbc == 'n' and self.args.ubc != 'p':
            ybotdiagE[-len(self.m):] *= 2                       # the last block of y diagonal is double for Neumann
            ybotdiagD[-len(self.m):] *= 2
            self.bbclabel = 'Neumann'

        diagE = L.reshape(1,-1)                 # put all diagonal blocks in a straight array
        diagD = R.reshape(1,-1)

        # Assembly of E and D matrices
        self.E = spdiags(diagE,0)                           # main diagonal of matrix E
        self.E.setdiag(np.tile(subupL,len(self.m)),1)       # up off diagonal
        self.E.setdiag(np.tile(subbotL,len(self.m)),-1)     # down off diagonal
        self.E.setdiag(yupdiagE,len(self.m))                # up off diagonal for y direction
        self.E.setdiag(ybotdiagE,-len(self.m))              # down off diagonal for y direction

        self.D = spdiags(diagD,0)                           # same as above but for matrix D
        self.D.setdiag(np.tile(subupR,len(self.m)),1)
        self.D.setdiag(np.tile(subbotR,len(self.m)),-1)
        self.D.setdiag(yupdiagD,len(self.m))
        self.D.setdiag(ybotdiagD,-len(self.m))

        # Periodic boundary conditions are set in the assembled E and D matrices
        # for periodic along x we need to create the extra terms for each main diagonal blocks
        if self.args.lbc == 'p' or self.args.rbc == 'p':
            pd = np.array([0+0j]).repeat(len(self.m))               
            pd[0] = -self.lamb/2
            pdfull = np.tile(pd,len(self.m))
            self.E.setdiag(pdfull, len(self.m)-1)
            self.E.setdiag(pdfull, -(len(self.m)-1))
            pdfull *= -1 
            self.D.setdiag(pdfull, len(self.m)-1)
            self.D.setdiag(pdfull, -(len(self.m)-1))
            self.lbclabel = 'Periodic'
            self.rbclabel = 'Periodic'
        # for periodic along y we need to create two extra blocks containing lambda diagonals
        if self.args.ubc == 'p' or self.args.bbc == 'p':
            pd = np.full(len(self.m),-self.lamb/2)
            self.E.setdiag(pd,(len(self.m)-1)*len(self.m))
            pd *= -1
            self.D.setdiag(pd,(len(self.m)-1)*len(self.m))
            pd = np.flip(pd)
            self.D.setdiag(pd,-(len(self.m)-1)*len(self.m))
            pd *= -1
            self.E.setdiag(pd,-(len(self.m)-1)*len(self.m))
            self.ubclabel = 'Periodic'
            self.bbclabel = 'Periodic'

        self.E = self.E.tocsc()               # we convert the sparse E matrix into csc format
        self.solver = factorized(self.E)      # we prefactorize E to solve the steps more fast 
        self.D = self.D.tocsr()               # we convert the sparse D matrix into csr format
        self.mult = aslinearoperator(self.D)  # we convert D into a linear operator for fast multiplication

        # these lines are just to debug matrices building
        # print(self.E.size, self.D.size)
        # if len(self.m) < 8:
        #     for i in range(len(self.m)):
        #         for j in range(len(self.m)):
        #             print(str(i)+' '+str(j))
        #             print(self.E.toarray()[i*len(self.m):(i+1)*len(self.m),j*len(self.m):(j+1)*len(self.m)])
        #             print('---')
        #             print(self.D.toarray()[i*len(self.m):(i+1)*len(self.m),j*len(self.m):(j+1)*len(self.m)])

        # Final plot area settings
        # ------------------------
        self.ax[0].set_xlabel(self.bbclabel, loc='right', fontsize=8)     # set bottom label for bc
        self.ax[0].set_ylabel(self.lbclabel, loc='bottom', fontsize=8)    # set left label for bc
        self.secx.set_xlabel(self.ubclabel, loc='left', fontsize=8)       # set upper label for bc
        self.secy.set_ylabel(self.rbclabel, loc='top', fontsize=8)        # set right label for bc

    def update(self, frame):
        '''
        Function to solve the Schrodinger's equation, update the matrix and the colormeshes
        '''
        # solve the matricial equation, Ynew = (E^-1)*D*Yold
        self.m = self.solver(self.mult.matvec(self.m.reshape(-1,1)))
        
        temparr = self.m.real.ravel()                   # gets the wave real part
        self.pcmr.set_array(temparr)                    # updates the plot colormesh array

        # uncomment these lines if you want continuous colormap limits updating for plot 0
        #maxabs = max(np.abs(temparr))
        #self.pcmr.set_clim(vmin=-maxabs, vmax=maxabs)

        temparr = self.m.imag.ravel()                   # gets the wave real part
        self.pcmi.set_array(temparr)                    # updates the plot colormesh array

        # uncomment these lines if you want continuous colormap limits updating for plot 1
        #maxabs = max(np.abs(temparr))
        #self.pcmi.set_clim(vmin=-maxabs, vmax=maxabs)

        temparr = (np.conjugate(self.m)*self.m).real.ravel()    # recalculates the probability density
        self.pcmd.set_array(temparr)                            # updates the plot colormesh array

        # uncomment these lines if you want continuous colormap limits updating for plot 2
        #maxabs = max(temparr)
        #self.pcmd.set_clim(vmax=maxabs)

        return self.pcmr, self.pcmi, self.pcmd                  # returns the updated colormeshes

    def animate(self):
        '''
        Function to animate the plots
        '''
        animation = FuncAnimation(self.fig, self.update, frames=None, interval=1, blit=True, save_count=300)

        # uncomment this line if you want to save a mp4 movie
        #animation.save('Snell_45.mp4', fps=60)

        plt.show()      # show the figure

def parse_arguments():
    """
    Parse command-line arguments.
    Returns:
    - args: Parsed command-line arguments.
    """
    chois = ['d','n','p']
    parser = argparse.ArgumentParser(description='2D Schrodinger\'s equation simulation')
    parser.add_argument('--rbc', type=str.lower, default='d', nargs='?', metavar='Right Boundary Condition', choices=chois, help='Right Boundary Condition')
    parser.add_argument('--lbc', type=str.lower, default='d', nargs='?', metavar='Left Boundary Condition', choices=chois, help='Left Boundary Condition')
    parser.add_argument('--ubc', type=str.lower, default='d', nargs='?', metavar='Upper Boundary Condition', choices=chois, help='Upper Boundary Condition')
    parser.add_argument('--bbc', type=str.lower, default='d', nargs='?', metavar='Bottom Boundary Condition', choices=chois, help='Bottom Boundary Condition')
    return parser.parse_args()
    
# Execute the main code only if this script is run directly, not when imported as a module
if __name__ == "__main__":
    
    args = parse_arguments()                                      # gets the command line arguments
    
    side_points = np.linspace(-1,1,150)                           # number of grid points in x an y
    animated_plot = AnimatedPcolormesh(side_points, args)         # creates the animation instance
    animated_plot.animate()                                       # start the animation
