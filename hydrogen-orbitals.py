"""
Hydrogen Orbitals Viewer

Author: Marcelo Falcão de Oliveira
Affiliation: University of São Paulo (USP)
             São Carlos School of Engineering (EESC)
             Materials Engineering Department (SMM)
Contact: marcelo.falcao@usp.br

Description:
This Python script show 3D views for the solutions of Schrödinger's equation for hydrogen:
- 3D wave function
- 3D probability density
- Clipping planes of the 3D probability density
- 3D contours of the probability density (>90%)
- Dot density plot for the 3D proability density 

License:
MIT License (https://opensource.org/licenses/MIT)

Purpose:
The script is designed to teach the solution of the Schrödinger's equation for hydrogen. 
It is fully commented to enhance understanding.

Packages needed:
argparse, vtk, numpy, sympy, pyvista

Usage:
$ python hydrogen_orbitals.py <n> <l> <m>
- <n>: Quantum number n (n >= 1)
- <l>: Quantum number l (0 <= l < n)
- <m>: Quantum number m (-l <= m <= l)
- Use 'python hydrogen_orbitals.py -h' for help.

Date: July 2023
Version: 1.1

Note:
The script is based on the example script of the pyvista package: atomic-orbitals.py
It was also improved with the assistance of ChatGPT-3.5.
"""

import argparse                     # Importing the argparse module for command-line argument parsing
import sys                          # Importing the sys module for interacting with the Python interpreter
import vtk                          # Importing the VTK (Visualization Toolkit) module for 3D computer graphics
import numpy as np                  # Importing the NumPy library for numerical operations
import pyvista as pv                # Importing the PyVista library for 3D visualization and analysis
from sympy.abc import phi, r, theta # Importing specific symbols (phi, r, theta) from the sympy.abc module
from sympy import latex             # Importing the latex function from the sympy module for LaTeX formatting
            

def parse_arguments():
    """
    Parse command-line arguments for the script.
        Returns:
        argparse.Namespace: An object containing parsed command-line arguments.
    """
    # Create an argument parser with a description
    parser = argparse.ArgumentParser(description='Hydrogen Orbitals Viewer.')
    
    # Add command-line arguments for principal, azimuthal, and magnetic quantum numbers
    parser.add_argument('n', metavar='n', type=int, help='Principal quantum number n (n >= 1)')
    parser.add_argument('l', metavar='l', type=int, help='Azimuthal quantum number l (l < n)')
    parser.add_argument('m', metavar='m', type=int, help='Magnetic quantum number m (-l <= m <= l)')
    
    # Parse the command-line arguments and return the result
    return parser.parse_args()

def load_hydrogen_orbital(n=1, l=0, m=0):
    """
    Generate the algebraic wave function for a hydrogen orbital using sympy.
    Args:
        n (int): Principal quantum number (default: 1, valid range: 1 to 6).
        l (int): Azimuthal quantum number (default: 0, valid range: 0 to n-1).
        m (int): Magnetic quantum number (default: 0, valid range: -l to l).
    Returns:
        sympy expression: Algebraic wave function for the specified hydrogen orbital.
    """
    from sympy.abc import phi, r, theta         # Symbols used in the function
    from sympy.physics.hydrogen import Psi_nlm  # Import the hydrogen algebraic wave function from sympy 
    
    # Ensure input quantum numbers are within valid ranges
    if n < 1 or n > 6:
        raise ValueError('`n` must be at least 1 and at most 6')            # Note: n greater than 6 generates orbitals hard to view
    if l not in range(n):
        raise ValueError(f'`l` must be one of: {list(range(n))}')           # Note: l must be smaller than n
    if m not in range(-l, l + 1):
        raise ValueError(f'`m` must be one of: {list(range(-l, l + 1))}')   # Note: m must be between -l and l
    
    # Return the desired algebraic wave function for hydrogen (1) with r, phi, and theta as variables
    psi = Psi_nlm(n, l, m, r, phi, theta, 1)
    
    return psi

def wfc(n=1, l=0, m=0):
    """
    Generate a 3D grid of numerical data representing the hydrogen orbital wave function.
    Args:
        n (int): Principal quantum number (default: 1, valid range: 1 to 6).
        l (int): Azimuthal quantum number (default: 0, valid range: 0 to n-1).
        m (int): Magnetic quantum number (default: 0, valid range: -l to l).
    Returns:
        pyvista.ImageData: 3D grid containing the numerical values of the wave function.
    """
    from sympy import lambdify          # lambdify converts functions to expressions that can be numerically evaluated
    from sympy.abc import phi, r, theta # Import the sympy symbols used in the functions

    psi = lambdify((r, phi, theta), load_hydrogen_orbital(n, l, m), 'numpy')    # Convert the sympy algebraic function to a numpy expression for numerical evaluation  
    org = 2 * (n**2 + n)                                                        # Half of the simulation box size, approximately close to the tail of the radial function (in Hartree unit)
    dim = 100                                                                   # Number of points in one dimension of the simulation box
    sp = (org * 2) / (dim - 1)                                                  # Spacing of points in the simulation box
    
    # Build the 3D grid of the image data
    grid = pv.ImageData(
        dimensions=(dim, dim, dim),
        spacing=(sp, sp, sp),
        origin=(-org, -org, -org),
    )

    r, theta, phi = pv.cartesian_to_spherical(grid.x, grid.y, grid.z)   # Convert Cartesian coordinates to spherical coordinates in the grid box
    wfc = psi(r, phi, theta).reshape(grid.dimensions)                   # Reshape the wave function according to the grid dimensions in spherical coordinates
    
    # Make a 1D array of the wfc data and store it in the grid
    if m < 0:
        grid['wfc'] = np.imag(wfc.ravel())  # Take the imaginary part when m < 0 since we want the real orbitals
    elif m > 0:
        grid['wfc'] = np.real(wfc.ravel())  # Take the real part when m > 0 since we want the real orbitals
    else:
        grid['wfc'] = wfc.ravel()           # If m = 0, there is no imaginary part
        
    return grid

def prob_dens(n=1, l=0, m=0):
    """
    Generate a 3D grid of numerical data representing the probability density from the hydrogen orbital wave function.
    Args:
        n (int): Principal quantum number (default: 1, valid range: 1 to 6).
        l (int): Azimuthal quantum number (default: 0, valid range: 0 to n-1).
        m (int): Magnetic quantum number (default: 0, valid range: -l to l).
    Returns:
        pyvista.ImageData: 3D grid containing the numerical values of the probability density.
    """
    from sympy import lambdify          # lambdify converts functions to expressions that can be numerically evaluated
    from sympy import Abs, re, im       # Abs, re, and im are used to get, respectively, the absolute, the real, and the imaginary part of a function
    from sympy.abc import phi, r, theta # Import the sympy symbols used in the functions

    psi = load_hydrogen_orbital(n, l, m)     # Load the desired wave function
    
    # Calculate the probability density
    if m < 0:
        dens = Abs(im(psi))     # Take the imaginary part for the absolute value when m < 0 since we want the real orbitals
    elif m > 0:
        dens = Abs(re(psi))     # Take the real part for the absolute value when m > 0 since we want the real orbitals
    else:
        dens = Abs(psi)         # If m = 0, there is no imaginary part
    
    # Multiply the absolute value by r if l = 0 since it is a uniform radial distribution (we want the radial probability density in such a case)
    if l == 0:
        dens *= r
    
    dens *= dens                                        # Square the absolute value (actual probability density)
    cloud = lambdify((r, phi, theta), dens, 'numpy')    # Convert the sympy algebraic function to a numpy expression for numerical evaluation
    org = 1.7 * (n**2 + n) + 4                          # Half of the simulation box size, approximately close to the tail of the radial function (in Hartree unit)
    dim = 100                                           # Number of points in one dimension of the simulation box
    sp = (org * 2) / (dim - 1)                          # Spacing of points in the simulation box
    
    # Build the 3D grid of the image data
    grid = pv.ImageData(
        dimensions=(dim, dim, dim),
        spacing=(sp, sp, sp),
        origin=(-org, -org, -org),
    )

    r, theta, phi = pv.cartesian_to_spherical(grid.x, grid.y, grid.z)   # Convert Cartesian coordinates to spherical coordinates in the grid box
    prob_c = cloud(r, phi, theta).reshape(grid.dimensions)              # Reshape the probability density function according to the grid dimensions in spherical coordinates
    grid['probability density'] = prob_c.ravel()                        # Get the probability density numbers (1D array) and store in the grid
    
    return grid

def plot_orbital(orbital, cpos='iso', clip_plane='x', eq=''):
    """
    Plot the probability density of a given orbital using PyVista, with an optional clipping plane.
    Args:
        orbital (pyvista.ImageData): 3D grid containing the numerical values of the probability density.
        cpos (str): Camera position preset (default: 'iso').
        clip_plane (str): Axis for the clipping plane (default: 'x').
        eq (str): Equation text to display on the plot (default: '').
    Returns:
        pyvista.Plotter: PyVista plotter object for visualization.
    """
    pl = pv.Plotter()   # Initialize the PyVista plotter
    
    # Define scalar bar title based on the azimuthal quantum number (l)
    scalar_bar_title = '$\|\psi\|^2r^2$' if int(sys.argv[2]) == 0 else '$\|\psi\|^2$'  # For l=0, include r^2 in the scalar bar title
    
    # Add a volume to the plotter with the desired grid (orbital) and set additional details below
    vol = pl.add_volume(
        orbital,  # Input grid
        cmap='rainbow',  # Color map for the probability density; rainbow map has consistent brightness from red to blue
        scalar_bar_args={'title': scalar_bar_title, 'use_opacity': False}  # Set the title of the scalar bar and disable opacity
    )
    
    vol.prop.interpolation_type = 'linear'  # Interpolation of the scalar values in between points
    
    # Place the desired clipping plane
    pl.add_volume_clip_plane(
        vol,
        normal=clip_plane,  # Axis cut by the clipping plane
        normal_rotation=False,  # Avoid rotation of the clipping plane by the user; only translation is possible
    )
    
    pl.add_text(eq, font_size=14)   # Add the text of the equation to the plot window
    pl.camera_position = cpos       # Define the position of the viewer (camera)
    pl.show_axes()                  # Make the x, y, and z axes visible
    
    return pl.show()                # Return the show of the plot window


# Execute the main code only if this script is run directly, not when imported as a module
if __name__ == "__main__":

    # Parse command line arguments
    args = parse_arguments()

    # Set PyVista global theme settings
    pv.global_theme.background = 'black'    # Set the plotter background color
    pv.global_theme.font.color = 'white'    # Set the plotter font color
    pv.global_theme.font.family = 'courier' # Set the plotter font type

    # Convert the algebraic sympy function of the orbital to LaTeX format
    expr = latex(load_hydrogen_orbital(args.n, args.l, args.m))

    # Create LaTeX expressions for the wave function and probability density
    expr_wfc = f'$\psi_{{({args.n},{args.l},{args.m})}}={expr}$'
    expr_prob = f'$\|\psi_{{({args.n},{args.l},{args.m})}}\|^2r^2=\|{expr}\|^2r^2$' if args.l == 0 else f'$\|\psi_{{({args.n},{args.l},{args.m})}}\|^2=\|{expr}\|^2$'

    # Plot block 1: 3D Wave Function
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    grid = wfc(args.n, args.l, args.m)      # Get the wave function evaluation grid
    pl = pv.Plotter()                       # Initialize the PyVista plotter

    # Add a volume to the plotter with the desired grid (orbital) and set additional details below
    vol = pl.add_volume(
        grid,
        cmap='twilight' if args.n > 1 else 'pink',    # Define the color map
        opacity=[1, 0, 1] if args.n > 1 else 'linear',  # Define the opacity
        scalar_bar_args={'title': '$\psi$', 'use_opacity': False}  # Set the title of the scalar bar and disable opacity 
    )
    vol.prop.interpolation_type = 'linear'  # Interpolation of the scalar values in between points

    # Insert a clipping plane for better view when n>1, l is even, and m=0
    if args.n > 1 and args.l % 2 == 0 and args.m == 0:
        pl.add_volume_clip_plane(
            vol,
            normal='-x',                # x-axis cut by the clipping plane
            normal_rotation=False,      # Avoid rotation of the clipping plane by the user; only translation is possible
        )

    pl.add_text(expr_wfc, font_size=14)     # Add the text of the equation to the plot window
    pl.show_axes()                          # Make x, y, and z axes visible
    pl.show()                               # Show the plot window

    
    # Plot block 2: 3D Orbital Probability Density
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    grid = prob_dens(args.n, args.l, args.m)    # Get the probability density function evaluation grid
    pl = pv.Plotter()                           # Initialize the PyVista plotter

    # Define the title for the scalar bar
    title_bar = '$\|\psi\|^2r^2$' if args.l == 0 else '$\|\psi\|^2$'

    # Add a volume to the plotter with the desired grid (orbital) and set additional details below
    vol = pl.add_volume(
        grid,
        cmap='rainbow',  # Define the color map for the probability density
        scalar_bar_args={'title': title_bar, 'use_opacity': False}  # Set the title of the scalar bar and disable opacity
    )
    vol.prop.interpolation_type = 'linear'  # Interpolation of the scalar values in between points

    pl.add_text(expr_prob, font_size=14)  # Add the text of the equation to the plot window
    pl.show_axes()  # Make x, y, and z axes visible
    pl.show()   # Show the plot window

    # Plot block 3: Clipping Planes of the 3D Probability Density 
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #clip plane at x=0 
    plot_orbital(grid, clip_plane='-x', eq=expr_prob)
    # clip plane at y=0
    plot_orbital(grid, clip_plane='-y', eq=expr_prob)
    # clip plane at z=0
    plot_orbital(grid, clip_plane='-z', eq=expr_prob)

    # Plot block 4: Orbital Contours as an Isosurface
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    grid = prob_dens(args.n, args.l, args.m)            # Get the probability density function evaluation grid
    perc = 0.1 - args.n * 0.015                         # Cut percent from 10% to 1% according to quantum number n
    eval_at = grid['probability density'].max() * perc  # Cut set regarding the maximum value 

    # Make the contour
    contours = grid.contour(
        [eval_at],                  # Contour values (just one here)
        method='marching_cubes'     # VTK filter to create the contour
    )
    contours = contours.interpolate(grid)   # Interpolate the countour with the grid

    # Plot the contour
    contours.plot(
        smooth_shading=True,    # Contour rounded edges
        show_scalar_bar=False,  # No scalar bar
        color='blue'            # Contour color
    )

    # Plot block 5: Orbital Probability Density with a Density Plot of Points
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    grid = prob_dens(args.n, args.l, args.m)                                # Get the probability density function evaluation grid
    prob = grid['probability density'] / grid['probability density'].sum()  # Normalize the probability densities by their whole sum
    indices = np.random.choice(grid.n_points, 10000, p=prob)                # Take points randomly but weighted by the probability density (10,000 points)

    # Add a small amount of noise to the coordinates to fade out the grid appearance
    points = grid.points[indices]
    points += np.random.random(points.shape) - 0.5
    
    point_cloud = pv.PolyData(points)   # Create a point cloud

    # Plot the points
    point_cloud.plot(
        style='points_gaussian',        # Gaussian-like representation
        render_points_as_spheres=False, # Points as points
        point_size=1,                   # Point size
        emissive=False,                 # Not emissive points (matte)
        show_scalar_bar=False,          # No scalar bar
        cpos='xz',                      # Point of view (camera position)
        color=[0, 200, 255]             # Point color
    )
