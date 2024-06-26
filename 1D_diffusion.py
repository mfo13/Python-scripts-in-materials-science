"""
Interactive 1D Diffusion Animation

Author: Marcelo Falcão de Oliveira
Affiliation: University of São Paulo (USP)
             São Carlos School of Engineering (EESC)
             Materials Engineering Department (SMM)
Contact: marcelo.falcao@usp.br

Description:
It ilustrates the solution of the transient diffusion equation in 1D
(2nd Fick's law), for example, trhough a wall or plate. The user can interact
with the animation plot by setting vertex positions, selecting boundary
conditions (Dirichlet, Neumann dC/dx=0 or periodic), setting initial
profiles and controlling de diffusion velocity.

License:
MIT License (https://opensource.org/licenses/MIT)

Purpose:
Educational tool for demonstrating 1D transient diffusion.

Packages needed:
matplotlib, numpy

Usage:
$ python 1D_diffusion.py
- Instructions are provided in the first plot

Date: January, 2024
Version: 2.0

Note:
Many improvement attempts were performed with ChatGPT-3.5 without success.
So this script remains "human like".
"""

howtouse = '''
INSTRUCTIONS

1. **Set Concentration:**
   - Click and drag points to adjust concentration values (y).
2. **Toggle Points:**
   - Press 't' to hide/show points for dragging.
3. **Change Boundary Conditions:**
   - Press 'b' to cycle among Dirichlet, Neumann (dC/dx=0), 
     or periodic.
4. **Toggle Diffusion On/Off:**
   - Press 'd' to start/stop diffusion run.
    (Figure interactivity holds with running diffusion.) 
5. **Timestep Size:**
    - Press '+' to double the timestep.
    - Press '-' to reduce the timestep by half.
6. **Reset Initial Profile:**
   - Press 'r' to cycle among resetting initial profiles.
7. **Toggle Help Message:**
   - Press 'h' to hide or show this help message.
'''

import numpy as np                                   # numpy is needed for matrix functions, it makes the code fast
from matplotlib.backend_bases import MouseButton     # needed for mouse interactivity with matplotlib objects
from matplotlib.path import Path                     # needed to build paths that can be decorated
from matplotlib.patches import PathPatch             # needed to build patches, i.e., filling areas
import matplotlib.pyplot as plt                      # pyplot is used for general plotting
import matplotlib.animation as animation             # matplotlib animation functions

def pattern(_id):
    """
    Here we define some resetting profiles for the initial concentration curve
    """

    # pattern 0
    # full of zeros
    pat = np.zeros(n)
    
    # pattern 1
    # half zeros half ones, we concatenate an array of ones and another of zeros
    if _id == 1:
        pat = np.concatenate((np.full(int(n/2-1),1),[0.5],np.full(int(n/2+1),0)))

    # pattern 2
    # alternating 1/3 of zeros or ones, we concatenate 3 arrays
    if _id == 2:
        b0 = np.full(int(n/3),0)
        pat = np.concatenate((b0,[0.5],np.full(int(n/3),1),[0.5],b0))

    # pattern 3
    # alternating 1/4 of zeros or ones, we concatenate 6 arrays
    if _id == 3:
        b0 = np.full(int(n/8),0)
        b1 = np.full(int(n/4),1)
        pat = np.concatenate((b0,b1,b0,[0],b0,b1,b0))

    # pattern 4
    # full of ones
    if _id == 4:
        pat = np.full(n,1)

    return pat

class PathInteractor:
    """
    Main core of the script for plot interactivity and animation.
    It is a very extensive modification of the original class 
    PathInteractor code from matplotlib examples found in
    https://matplotlib.org/stable/gallery/event_handling/path_editor.html#path-editor
    """
    showverts = True    # variable to control whether vertices (points) are shown or not
    epsilon = 13        # max pixel distance to count as a vertex hit
    _ind = None         # variable for identification of the active vertex for user's editing
    bc = 'Dirichlet'    # initial boundary condition
    timestepfactor = 1  # initial timestep multiplier
    helpshow = True     # variable to control toggle of help message
    pattern_id = 4      # last pattern id for curve resetting
    
    def __init__(self, figure, pathpatch, mesh):
        """
        This is the initialization function of the class
        """
        self.canvas = figure.canvas                         # pass figure canvas to an internal class variable
        self.ax = pathpatch.axes                            # pass patchpatch axes to an internal class variable
        self.pathpatch = pathpatch                          # pass the pathpatch to an internal class variable
        self.pathpatch.set_animated(True)                   # makes the pathpatch animated
        self.ax2 = mesh                                     # pass the pcolormesh to an internal class variable
        self.vertices = self.pathpatch.get_path().vertices  # internal variable for the path vertices
        self.vertices = self.vertices[1:-1]                     # trim out the path borders (they are used only for the patch)
        shape = colormesh.get_coordinates().shape               # get colormesh grid matrix shape
        self.mat = mesh.get_array().reshape(shape[2],shape[1])  # reshape the colormesh array values to an internal class variable
        
        x, y = zip(*self.vertices)  # gets x and y coordinates of the pathpatch and arrange them in vectors
   
        # we build a line (not visible) with markers on the path for user's editing, it is also animated
        self.line, = self.ax.plot(
            x, y, marker='s', markersize='7', markerfacecolor='r', linewidth=0, animated=True)

        # plot title with initial bondary condition
        self.ax.set_title('1D Diffusion Animation - Boundary Condition: Dirichlet')
        # we add the help message into the plot
        self.helpbox = self.ax.text(-0.9,0.1, howtouse, color='blue', fontsize=10.5, wrap=True)
        
        self.canvas.mpl_connect('draw_event', self.on_draw)                      # detects drawing event and executes on_draw function
        self.canvas.mpl_connect('button_press_event', self.on_button_press)      # detects mouse button press and executes on_button_press function
        self.canvas.mpl_connect('key_press_event', self.on_key_press)            # detects keybord press and executes on_key_press fucntion
        self.canvas.mpl_connect('button_release_event', self.on_button_release)  # detects mouse button release and executes on_button_release function
        self.canvas.mpl_connect('motion_notify_event', self.on_mouse_move)       # detects mouse movement and executes on_mouse_move function

        self.keepdiffusing = False  # variable to toggle on/off the animation (diffusion)

        # we define the animation, infinite loop (frames=None) and 10 ms bettween frames
        self.anim = animation.FuncAnimation(figure, self.animate, frames=None, interval=10)

        plt.show() # now we can show our plot
       
    def animate(self, frame):
        """
        Animates our plot, perform a diffusion step and refresh the canvas
        """
        # perform a diffusion step only if diffusion is on
        if self.keepdiffusing:
            self.vertices = self.timestep(self.vertices) # apply the diffusion step
        
        self.canvas.blit(self.ax.bbox)  # refresh canvas with fast rendering over the background

    def get_ind_under_point(self, event):
        """
        Return the index of the point closest to the event position or *None*
        if no point is within ``self.epsilon`` to the event position.
        """
        xy = self.vertices                                  # get vertices
        xyt = self.pathpatch.get_transform().transform(xy)  # get vertices coordinates in the screen
        xt, yt = xyt[:, 0], xyt[:, 1]                       # split x and y coordinates in two vectors
        d = np.sqrt((xt - event.x)**2 + (yt - event.y)**2)  # calculates the distance between the click event and the vertices
        ind = d.argmin()                                    # get the id of the vertex with the minor distance
        return ind if d[ind] < self.epsilon else None       # if the distance is shorter than epsilon returns the vertex' id

    def on_draw(self, event):
        """
        This function is activated everytime a drawing event occurs; blit, for example.   
        """
        self.line.set_data(zip(*self.vertices))                    # update marker's (vertices) positions
        self.ax.draw_artist(self.pathpatch)                        # draw the path and the patch
        self.ax.draw_artist(self.line)                             # draw the interactive markers (line)
        self.mat[:,:] = self.vertices[:,1]                         # updates the matrix of the colormesh
        self.ax2.set_array(self.mat)
        
    def on_button_press(self, event):
        """
        Function to handle mouse button press
        """
        if (event.inaxes is None                        # it works only if the mouse is inside axes or left mouse button
                or event.button != MouseButton.LEFT     # and vertices are visible
                or not self.showverts):
            return
        self._ind = self.get_ind_under_point(event)     # gets the vertex identification if close enough the mouse click

    def on_button_release(self, event):
        """
        Function to handle mouse button release
        """
        if (event.button != MouseButton.LEFT            # it works only if left mouse button
                or not self.showverts):                 # and vertices are visible
            return
        self._ind = None                                # since the mouse was released no vertex is active

    def on_key_press(self, event):
        """
        Function to handle keyboard pressing
        """
        # check if the mouse is inside the plot or do nothing
        if not event.inaxes:
            return

        # show or hide vertices as well as toggle path user's interaction
        if event.key == 't':
            self.showverts = not self.showverts   # flip showverts condition
            self.line.set_visible(self.showverts) # set markers (line) visibility
            # if vertices are hidden none is avaliable for editing
            if not self.showverts:                
                self._ind = None
            
        # cycle among boundary conditions
        if event.key == 'b':
            if self.bc == 'Dirichlet':  # from Dirichlet to Neumann
                self.bc = 'Neumann'     
            elif self.bc == 'Neumann':  # from Neumann to periodic
                self.bc = 'Periodic'
            else: 
                self.bc = 'Dirichlet'   # back to Dirichlet
            # apply the periodic condition if set
            if self.bc == 'Periodic':
                self.vertices[n-1][1] = self.vertices[0][1]
            # change the boundary conditon in the title
            self.ax.set_title('1D Diffusion Animation - Boundary Condition: ' + self.bc)
                                    
        # toggle diffusion on/off
        if event.key == 'd':
            self.keepdiffusing = not self.keepdiffusing     # flip keepdiffusing condition
            
        # cycle the resetting path curve according to the patterns
        if event.key == 'r':
            if self.pattern_id == 0:
                self.pattern_id = 1
            elif self.pattern_id == 1:
                self.pattern_id = 2
            elif self.pattern_id == 2:
                self.pattern_id = 3
            elif self.pattern_id == 3:
                self.pattern_id = 4
            elif self.pattern_id == 4:
                self.pattern_id = 0
            self.vertices[:,1] = pattern(self.pattern_id)   # pass the concentration pattern to the path
            if not self.showverts:                          # make the markers (line) visible
                 self.showverts = True
                 self.line.set_visible(True)
            self.timestepfactor = 1                         # set the timestep multiplier back to 1
             
        if event.key == '+':                # double the timestep multiplier
            self.timestepfactor *= 2

        if event.key == '-':                # half the timestep multiplier
            self.timestepfactor *= 0.5

        # toggle help visibility
        if event.key == 'h':
            self.helpshow = not self.helpshow           # flip helpshow condition
            self.helpbox.set_visible(self.helpshow)     # apply the condition     
            
    def on_mouse_move(self, event):
        """
        Function to handle mouse movements.
        """
        if (self._ind is None                           # it works only if the mouse is inside axes or left mouse button
                or event.inaxes is None                 # and vertices are visible
                or event.button != MouseButton.LEFT
                or not self.showverts):
            return

        y = event.ydata                                     # allow moving only along y between 0 and 1
        if event.ydata > 1: y = 1
        if event.ydata < 0: y = 0
        self.vertices[self._ind][1] = y                     # move only the active vertex
        if self.bc == 'Periodic' and self._ind == 0:        # if bc is periodic the extremes are the same
            self.vertices[n-1][1] = self.vertices[0][1]
        if self.bc == 'Periodic' and self._ind == (n-1):    # if bc is periodic the extremes are the same
            self.vertices[0][1] = self.vertices[n-1][1]
            
    def timestep(self, m):
        """
        This function applies the Crank-Nicolson scheme for solving the 2nd Fick's law equation.
        Notice how we can avoid nested for loops by using numpy matrix functions.
        To understand the matricial solution refer to the lecture documentation.
        """
        m0 = m[:,1].copy()                  # make a copy (column) of the initial vector of values
        dt = 1/1000*self.timestepfactor     # time step size which is also the lambda of the C-N scheme 
       
        Lidiag = np.full(len(m), 1+dt)                                      # main diagonal of lambda matrix for implicit terms
        Lioffdiag = np.full(len(m)-1, -dt/2)                                # off diagonals of lambda matrix for implicit terms
        Li =  np.diag(Lioffdiag,-1)+np.diag(Lidiag,0)+np.diag(Lioffdiag,1)  # lambda tridiagonal matrix for implicit terms
        
        Lediag = np.full(len(m), 1-dt)                                      # main diagonal of lambda matrix for explicit terms
        Leoffdiag = np.full(len(m)-1, dt/2)                                 # off diagonals of lambda matrix for explicit terms
        Le =  np.diag(Leoffdiag,-1)+np.diag(Lediag,0)+np.diag(Leoffdiag,1)  # lambda tridiagonal matrix for explicit terms

        # Apply the boundary condition
        if self.bc == 'Dirichlet':
            Li[0,0] = Li[len(m)-1,len(m)-1] = 1     # main diagonal extremes
            Le[0,0] = Le[len(m)-1,len(m)-1] = 1 
            Li[0,1] = Li[len(m)-1,len(m)-2] = 0     # off diagonal extremes
            Le[0,1] = Le[len(m)-1,len(m)-2] = 0
        if self.bc == 'Neumann': 
            Li[0,1] = Li[len(m)-1,len(m)-2] = -dt   # off diagonal extremes
            Le[0,1] = Le[len(m)-1,len(m)-2] = dt
        if self.bc == 'Periodic': 
            Li[0,len(m)-2,] = Li[len(m)-1,1] = -dt/2 # off anti-diagonal extremes
            Le[0,len(m)-2,] = Le[len(m)-1,1] = dt/2

        m[:,1] = np.matmul(np.linalg.inv(Li),np.matmul(Le,m0))  # solves the matricial equation: m = Li^(-1).Le.m0

        return m                                                # returns the calculated matrix

# Execute the main code only if this script is run directly, not when imported as a module
if __name__ == "__main__":

    n = 41                  # number of main vertices in the path

    fig, (ax1, ax2) = plt.subplots(2, sharex=True, height_ratios=[9, 1])  # we define 2 subplots with different heights
    fig.set_figwidth(6)                                                   # figure width
    fig.set_figheight(6)                                                  # figure height
    fig.subplots_adjust(hspace=0.05)                                      # vertical space between subplots

    # define the main vertices in the path between -1 and 1, with zero concentration in all points
    verts = np.array([np.linspace(-1,1,n),np.zeros(n)]).flatten(order='F').reshape(n,2)
    # we add 2 fixed vertices at the path extremities to build a decorative patch from the horizintal axis 
    fullpath = np.concatenate((np.array([[-1,0]]),verts,np.array([[1,0]])),axis=0)
    # we define a path
    path = Path(fullpath)
    # now we define a patch with the path
    patch = PathPatch(
         path, facecolor='lightgreen', edgecolor='blue', linewidth=2)
    # the patch is added to the upper subplot
    ax1.add_patch(patch)
    # we set the x axis limits
    ax1.set_xlim(-1, 1)
    # we set the y axis limits
    ax1.set_ylim(0, 1.01)
    # we set the x axis title at the bottom subplot
    ax2.set_xlabel('Relative position')
    # turn off the y labels in the bottom subplot
    ax2.yaxis.set_tick_params(labelleft=False)
    # turn off the y ticks in the bottom subplot
    ax2.set_yticks([])
    # we set the y axis title
    ax1.set_ylabel('Concentration')

    # we define the X, Y matrices for meshgrid: n x 2
    X, Y = np.meshgrid(np.linspace(-1,1,n), np.array([0,1]))
    # we define the initial values of the mesh points
    mat = (X+Y)*0
    # we add the colormesh to the bottom subplot
    colormesh = ax2.pcolormesh(X, Y, mat, cmap='Purples', vmin=0, vmax=1, shading='gouraud')

    # we call the class for path interaction and animation, passing figure, patch and colormesh
    interactor = PathInteractor(fig, patch, colormesh)
