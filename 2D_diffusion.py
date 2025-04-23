"""
2D Diffusion of R, G, B in BMP Images

Author: Marcelo Falcão de Oliveira
Affiliation: University of São Paulo (USP)
             São Carlos School of Engineering (EESC)
             Materials Engineering Department (SMM)
Contact: marcelo.falcao@usp.br

Description:
This Python script simulates the 2D diffusion of color channels (R, G, B) in BMP images.
It is designed for teaching purposes, providing insights into the diffusion process.

License:
MIT License (https://opensource.org/licenses/MIT)

Purpose:
Educational tool for demonstrating 2D color diffusion processes.

Packages needed:
argparse, sys, matplotlib, numpy

Usage:
$ python 2D_diffusion.py <arg1> <arg2>
- <arg1> bmp image (prefer images not larger than 500 px at the edge)
- <arg2> bondary condition, can be neumann, dirichlet or periodic. (neumann is the default)
- <arg3> R diffusivity (default 1)
- <arg4> G diffusivity (default 1)
- <arg5> B diffusivity (default 1)
- Use 'python 2D_diffusion.py -h' for help.

Date: September, 2023
Version: 1.1

Note:
This script was improved with the assistance of ChatGPT-3.5.
"""
import argparse                                 # For parsing command-line arguments
import sys                                      # For system-specific parameters and functions
import numpy as np                              # For numerical operations on arrays
import matplotlib.pyplot as plt                 # For creating plots
from matplotlib import image                    # For reading and displaying images
from matplotlib.animation import FuncAnimation  # For creating animated plots

def parse_arguments():
    """
    Parse command-line arguments for the 2D diffusion script.
    Returns:
        argparse.Namespace: An object containing parsed command-line arguments.
    """
    parser = argparse.ArgumentParser(description='2D diffusion of R, G, B in BMP images.')
    parser.add_argument('image_path', metavar='image_path', type=str, help='Path to the BMP image file')
    parser.add_argument('boundary_condition', metavar='boundary_condition', type=str, nargs='?',
                        choices=['neumann', 'dirichlet', 'periodic'],
                        help='Boundary condition for the diffusion')
    parser.add_argument('Dr', metavar='Dr', type=float, nargs='?', default=1.0,
                        help='Red color diffusivity (default: 1.0)')
    parser.add_argument('Dg', metavar='Dg', type=float, nargs='?', default=1.0,
                        help='Green color diffusivity (default: 1.0)')
    parser.add_argument('Db', metavar='Db', type=float, nargs='?', default=1.0,
                        help='Blue color diffusivity (default: 1.0)')
    return parser.parse_args()

def load_image(image_path):
    """
    Load and convert an image to a floating-point matrix.
    Args:
        image_path (str): Path to the BMP image file.
    Returns:
        numpy.ndarray: A floating-point matrix representing the image.
    Raises:
        SystemExit: Exits the script if an error occurs during image loading.
    """
    try:
        img = image.imread(image_path)
        return np.float_(img)
    except Exception as e:
        sys.exit(f"Error loading the image: {e}")

def initialize_variables(image_matrix, Dr, Dg, Db):
    """
    Initialize variables for a 2D diffusion simulation.
    Args:
        image_matrix (numpy.ndarray): Matrix representing the image.
        Dr (float): Red color diffusivity.
        Dg (float): Green color diffusivity.
        Db (float): Blue color diffusivity.
    Returns:
        tuple: A tuple containing initialized variables:
            - m (numpy.ndarray): Copy of the image matrix.
            - D (numpy.ndarray): Array of diffusivities for R, G, B.
            - dt (float): Time step for the simulation.
            - bottom (int): Index of the bottom row of the image matrix.
            - right (int): Index of the rightmost column of the image matrix.
    """
    m = image_matrix.copy()
    D = np.array([Dr, Dg, Db])  # diffusivities for R, G, B
    dt = 1 / np.max(D) / 4.
    bottom, right = m.shape[0] - 1, m.shape[1] - 1
    return m, D, dt, bottom, right

def apply_boundary_condition(bc, m0, m, D, dt, bottom, right):
    """
    Apply boundary conditions in a 2D diffusion simulation.
    Args:
        bc (str): Boundary condition, can be 'neumann' or 'periodic'.
        m0 (numpy.ndarray): Matrix representing the previous state.
        m (numpy.ndarray): Matrix representing the current state.
        D (numpy.ndarray): Array of diffusivities for R, G, B.
        dt (float): Time step for the simulation.
        bottom (int): Index of the bottom row of the image matrix.
        right (int): Index of the rightmost column of the image matrix.
    Returns:
        numpy.ndarray: Matrix representing the updated state after applying boundary conditions.
    
    Notice: Use of numpy slicing and broadcasting instead of nested for loops
    """
    if bc == 'neumann':
        # Neumann bondary condition, dC/dx = dC/dy = 0
        # FTCS discretization scheme
        # left border
        m[1:-1, 0] = m0[1:-1, 0] + D * dt * ( # cells's previous values
                m0[2:, 0] + m0[:-2, 0]        # up and down points
              + 2*m0[1:-1, 1]                 # right points
              - 4*m0[1:-1, 0])                # central points
        # top border
        m[0, 1:-1] = m0[0, 1:-1] + D * dt * ( # cells's previous values
                2*m0[1, 1:-1]                 # down points
              + m0[0, 2:] + m0[0, :-2]        # left and right points
              - 4*m0[0, 1:-1])                # central points
        # right border
        m[1:-1, right] = m0[1:-1, right] + D * dt * ( # cells' previous values
                m0[2:, right] + m0[:-2, right]        # up and down points
              + 2*m0[1:-1, right-1]                   # left points
              - 4*m0[1:-1, right])                    # central points
        # bottom border
        m[bottom, 1:-1] = m0[bottom, 1:-1] + D * dt * ( # cells' previous values
                2*m0[bottom-1, 1:-1]                    # up points
              + m0[bottom, 2:] + m0[bottom, :-2]        # left and right points
              - 4*m0[bottom, 1:-1])                     # central points
        # 4 corners
        m[0, 0] = m0[0, 0] + D * dt * ( # up left point previous value
                2*m0[1, 0]              # down point
              + 2*m0[0, 1]              # right point
              - 4*m0[0, 0])             # central point
        m[0, right] = m0[0, right] + D * dt * ( # up right point previous value
                2*m0[1, right]                  # down point
              + 2*m0[0, right-1]                # left point
              - 4*m0[0, right])                 # central point
        m[bottom, 0] = m0[bottom, 0] + D * dt * (   # bottom left point previous value
                2*m0[bottom-1, 0]                   # up point
              + 2*m0[bottom, 1]                     # right point
              - 4*m0[bottom, 0])                    # central point
        m[bottom, right] = m0[bottom, right] + D * dt * (   # bottom right point previous value
                2*m0[bottom-1, right]                       # up point
              + 2*m0[bottom, right-1]                       # left point
              - 4*m0[bottom, right])                        # central point
    elif bc == 'periodic':
        # Periodic bondary condition (pbc)
        # FTCS discretization scheme
        # left border
        m[1:-1, 0] = m0[1:-1, 0] + D * dt * ( # cells's previous values
                m0[2:, 0] + m0[:-2, 0]        # up and down points
              + m0[1:-1, 1] + m0[1:-1, right] # left and right points
              - 4*m0[1:-1, 0])                # central points
        # top border
        m[0, 1:-1] = m0[0, 1:-1] + D * dt * (   # cells's previous values
                m0[1, 1:-1] + m0[bottom, 1:-1]  # up and down points
              + m0[0, 2:] + m0[0, :-2]          # left and right points
              - 4*m0[0, 1:-1])                  # central points
        # right border
        m[1:-1, right] = m0[1:-1, right] + D * dt * ( # cells' previous values
                m0[2:, right] + m0[:-2, right]        # up and down points
              + m0[1:-1, right-1] + m0[1:-1, 0]       # left and right points
              - 4*m0[1:-1, right])                    # central points
        # bottom border
        m[bottom, 1:-1] = m0[bottom, 1:-1] + D * dt * ( # cells' previous values
                m0[bottom-1, 1:-1] + m0[0, 1:-1]        # up and down points
              + m0[bottom, 2:] + m0[bottom, :-2]        # left and right points
              - 4*m0[bottom, 1:-1])                     # central points
        # 4 corners
        m[0, 0] = m0[0, 0] + D * dt * (     # up left point previous value
                m0[1, 0] + m0[bottom, 0]    # down and up points
              + m0[0, 1] + m0[0, right]     # right and left points
              - 4*m0[0, 0])                 # central point
        m[0, right] = m0[0, right] + D * dt * (     # up right point previous value
                m0[1, right] + m0[bottom, right]    # down and up points
              + m0[0, right-1] + m0[0, 0]           # left and right points
              - 4*m0[0, right])                     # central point
        m[bottom, 0] = m0[bottom, 0] + D * dt * (   # bottom left point previous value
                m0[bottom-1, 0] + m0[0, 0]          # up and down points
              + m0[bottom, 1] + m0[bottom, right]   # right and left points
              - 4*m0[bottom, 0])                    # central point
        m[bottom, right] = m0[bottom, right] + D * dt * (   # bottom right point previous value
                m0[bottom-1, right] + m0[0, right]          # up and down points
              + m0[bottom, right-1] + m0[bottom, 0]         # left and right points
              - 4*m0[bottom, right])                        # central point
    return m

def timestep(m0, m, D, dt, bc, bottom, right):
    """
    Apply a time step of the FTCS scheme to update the matrix.
    Args:
        m0 (numpy.ndarray): Matrix representing the previous state.
        m (numpy.ndarray): Matrix representing the current state.
        D (numpy.ndarray): Array of diffusivities for R, G, B channels.
        dt (float): Time step.
        bc (str): Boundary condition ('neumann' or 'periodic' or 'dirichlet').
        bottom (int): Index of the bottom row.
        right (int): Index of the rightmost column.
    Returns:
        Tuple[numpy.ndarray, numpy.ndarray]: Updated matrices for the previous and current states.

    Notice: Use of numpy slicing and broadcasting instead of nested for loops
    """
    m[1:-1, 1:-1] = m0[1:-1, 1:-1] + D * dt * (       # cells's previous values
            m0[2:, 1:-1] + m0[:-2, 1:-1]              # up and down points
          + m0[1:-1, 2:] + m0[1:-1, :-2]              # left and right points
          - 4*m0[1:-1, 1:-1])                         # central point
    
    # p.s.: for Dirichlet bondary condition we do nothing since the cells at the borders don't change
    if bc != 'dirichlet':
        m = apply_boundary_condition(bc, m0, m, D, dt, bottom, right)
    m0 = m.copy()
    return m0, m

def animate(i, ax, m0, m, titulo, D, dt, bc, bottom, right):
    """
    Update and plot the diffusion animation for a given time step.
    Args:
        i (int): Current time step.
        ax (matplotlib.axes._axes.Axes): Matplotlib axes for plotting.
        m0 (numpy.ndarray): Matrix representing the previous state.
        m (numpy.ndarray): Matrix representing the current state.
        titulo (str): Title for the plot.
        D (numpy.ndarray): Array of diffusivities for R, G, B channels.
        dt (float): Time step.
        bc (str): Boundary condition ('neumann' or 'periodic' or 'dirichlet').
        bottom (int): Index of the bottom row.
        right (int): Index of the rightmost column.
    Returns:
        matplotlib.axes._axes.Axes: Updated matplotlib axes.
    """
    ax.clear()
    m0, m = timestep(m0, m, D, dt, bc, bottom, right)
    ax.imshow(np.int_(np.round(m)))
    ax.set_axis_off()
    ax.set_title(f"{titulo} - timestep: {i}")
    return ax

# Execute the main code only if this script is run directly, not when imported as a module
if __name__ == "__main__":
    # Parse command line arguments
    args = parse_arguments()

    # Load the image matrix
    image_matrix = load_image(args.image_path)

    # Initialize variables for diffusion
    m, D, dt, bottom, right = initialize_variables(image_matrix, args.Dr, args.Dg, args.Db)

    # Set boundary condition and title
    bc = args.boundary_condition
    if bc not in ['neumann', 'dirichlet', 'periodic']: bc = 'neumann'   # default bc
    titulo = '2D diffusion'

    # Create the initial plot
    fig, ax = plt.subplots()
    ax.imshow(np.int_(np.round(m)))
    ax.set_axis_off()
    ax.set_title(f"{titulo} - timestep: 0")

    # Create the animation
    anim = FuncAnimation(fig, animate, frames=1000, fargs=(ax, m, m, titulo, D, dt, bc, bottom, right), interval=20)

    # Show the animation
    plt.show()
