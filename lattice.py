"""
Bravais Lattices, conventional, primitive and Wigner-Seitz 

Author: Marcelo Falcão de Oliveira
Affiliation: University of São Paulo (USP)
             São Carlos School of Engineering (EESC)
             Materials Engineering Department (SMM)
Contact: marcelo.falcao@usp.br

Description:
It shows 3D plots, in any browser, Bravais Lattices conventional cells and
optionally the primitive and/or Wigner-Seitz cells. Additionally the user
can also choose hcp and diamond lattices. 

License:
MIT License (https://opensource.org/licenses/MIT)

Purpose:
Educational tool for visualizing 3D Bravais lattice cells.

Packages needed:
argparse, plotly, numpy, scipy, spglib, ase 

Usage:
$ python lattice.py --lattice <arg1> --primitive --ws
Optional arguments:
- <arg1> lattice abbreviations (many possibla from usula notitions, default bcc)
- primitive and ws are optionals to show, respectively, primitive or Wigner-Seitz cells 
- Use 'python lattice.py -h' for help.

This script was produce with the help of ChatGPT

Version: 1.0 March/2026
"""
# importe usefull libraries
import plotly.graph_objects as go
import numpy as np
import argparse
import spglib
import sys
from ase import Atoms
from scipy.spatial import Voronoi, ConvexHull

# ==========================================================
# Sphere utility (to plot spheres)
# ==========================================================
def add_sphere(fig, center, radius=0.05, resolution=20, color='orange'):
    u = np.linspace(0, 2*np.pi, resolution)
    v = np.linspace(0, np.pi, resolution)

    x = radius * np.outer(np.cos(u), np.sin(v)) + center[0]
    y = radius * np.outer(np.sin(u), np.sin(v)) + center[1]
    z = radius * np.outer(np.ones(np.size(u)), np.cos(v)) + center[2]

    fig.add_trace(go.Surface(
        x=x, y=y, z=z,
        showscale=False,
        opacity=1.0,
        colorscale=[[0, color], [1, color]]
    ))

# ==========================================================
# Plot the conventinal unit cell
# ==========================================================
def plot_conventional_cell(fig, atoms):
    # get the cell matrix
    cell = atoms.get_cell()
    # define the spheres radius proportionaly to the smallest cell edge
    parametros = atoms.cell.cellpar()
    raio = np.min([np.abs(parametros[0]), np.abs(parametros[1]), np.abs(parametros[2])])/20

    # get the coordinates of all atomic positions in the cell by shiftting the basis
    frac = atoms.get_scaled_positions()
    visual_positions = []
    for f in frac:
        shifts = [[0,0,0]]
        for i in range(3):
            if np.isclose(f[i], 0):
                new_shifts = []
                for s in shifts:
                    s_copy = s.copy()
                    s_copy[i] = 1
                    new_shifts.append(s_copy)
                shifts.extend(new_shifts)
        
        for s in shifts:
            new_frac = f + s
            cart = new_frac @ cell
            visual_positions.append(cart)

    positions = np.array(visual_positions)
    
    # get the vertices of the cell
    a1, a2, a3 = cell
    vertices = [
        [0,0,0],
        a1,
        a2,
        a3,
        a1 + a2,
        a1 + a3,
        a2 + a3,
        a1 + a2 + a3
    ]
    
    # Vertices connectivity for the edges
    edges = [
        (0,1),(0,2),(0,3),
        (1,4),(1,5),
        (2,4),(2,6),
        (3,5),(3,6),
        (4,7),(5,7),(6,7)
    ]
    
    # plot spheres on lattice points
    for p in positions:
        add_sphere(fig, p, radius=raio, resolution=24)
    
    # Plot the edges
    for e in edges:
        fig.add_trace(go.Scatter3d(
            x=[vertices[e[0]][0], vertices[e[1]][0]],
            y=[vertices[e[0]][1], vertices[e[1]][1]],
            z=[vertices[e[0]][2], vertices[e[1]][2]],
            mode='lines',
            line=dict(color='black', width=2),
            showlegend=False
        ))
    
    # update the figure layout
    fig.update_layout(
        scene=dict(
            xaxis=dict(visible=False),
            yaxis=dict(visible=False),
            zaxis=dict(visible=False),
            aspectmode='data'
        ),
        margin=dict(l=0, r=0, b=0, t=0)
    )
    
# ==========================================================
# Plot the primitive unit cell
# ==========================================================
def plot_primitive_cell(fig, atoms):
    
    # get the primitive
    # we can't use find_primitive here because we want no_idealize 
    # in order to keep the coordinate system for non orthogonal cells
    result = spglib.standardize_cell(
        (atoms.get_cell(),
         atoms.get_scaled_positions(),
         atoms.get_atomic_numbers()),
         to_primitive=True,
         no_idealize=True
    )

    # vertices of the primitive
    cell = np.array(result[0])
    a1, a2, a3 = cell
    
    primitive_points = np.array([
        np.zeros(3),
        a1, a2, a3,
        a1 + a2,
        a1 + a3,
        a2 + a3,
        a1 + a2 + a3
    ])
    
    # faces of the primitive
    primitive_faces = [
        (0,1,4,2),(0,1,5,3),(0,2,6,3),
        (7,4,2,6),(7,5,1,4),(7,6,3,5)
    ]
    
    i_list, j_list, k_list = [], [], []
    
    for face in primitive_faces:
        q = list(face)
        i_list.extend([q[0], q[0]])
        j_list.extend([q[1], q[2]])
        k_list.extend([q[2], q[3]])
          
    # plot the faces
    fig.add_trace(go.Mesh3d(
        x=primitive_points[:,0],
        y=primitive_points[:,1],
        z=primitive_points[:,2],
        i=i_list, j=j_list, k=k_list,
        opacity=0.7,
        color='cyan',
        flatshading=True,
        lighting=dict(ambient=1.0, diffuse=0.0, specular=0.0),
        showscale=False
    ))
    
    # edges of the primitive (allways the same for any primitive)
    primitive_edges = [
        (0,1),(0,2),(0,3),
        (1,4),(1,5),
        (2,4),(2,6),
        (3,5),(3,6),
        (4,7),(5,7),(6,7)
    ]
    
    # plot the edges
    for e in primitive_edges:
        fig.add_trace(go.Scatter3d(
            x=[primitive_points[e[0],0], primitive_points[e[1],0]],
            y=[primitive_points[e[0],1], primitive_points[e[1],1]],
            z=[primitive_points[e[0],2], primitive_points[e[1],2]],
            mode='lines',
            line=dict(width=4, color='blue'),
            showlegend=False
        ))

    # plot atoms of the primitive outside the conventinal cell
    conv_cell = np.array(atoms.get_cell())
    inv_conv = np.linalg.inv(conv_cell)
    scaled = primitive_points @ inv_conv # to verify wich vertices are inside the conventional
    tol = 1e-8
    inside = np.all((scaled >= 0 - tol) & (scaled <= 1 + tol), axis=1)
    outside = primitive_points[~inside]
    parametros = conventional.cell.cellpar()
    raio = np.min([np.abs(parametros[0]), np.abs(parametros[1]), np.abs(parametros[2])])/20
    for p in outside:
        add_sphere(fig, p, radius=raio, color='red')
    
    # update the figure layout
    fig.update_layout(
        scene=dict(
            xaxis=dict(visible=False),
            yaxis=dict(visible=False),
            zaxis=dict(visible=False),
            aspectmode='data'
        ),
        margin=dict(l=0, r=0, b=0, t=0)
    )

# ==========================================================
# Plot the Wigner-Seitz (Voronoi) cell
# # ========================================================
def plot_ws_cell(fig, atoms):
    
    cell = np.array(atoms.get_cell())
    a1, a2, a3 = cell

    # expand the lattice around the original unit cell 
    shifts = [-1, 0, 1]
    lattice_points = []
    scaled_positions = atoms.get_scaled_positions()
    shifts = [-1, 0, 1]
    lattice_points = []
    for i in shifts:
        for j in shifts:
            for k in shifts:
                T = i*a1 + j*a2 + k*a3

                for sp in scaled_positions:
                    cart = sp[0]*a1 + sp[1]*a2 + sp[2]*a3
                    lattice_points.append(T + cart)

    lattice_points = np.array(lattice_points)

    # Voronoi 3D
    vor = Voronoi(lattice_points)

    # find the index of the central point and its voronoi region
    center_index = np.where(
        np.all(np.isclose(lattice_points, [0,0,0]), axis=1)
    )[0][0]
    region_index = vor.point_region[center_index]
    region = vor.regions[region_index]

    if -1 in region:
        print("Infinite region detected — enlarge the lattice expansion.")
        return

    vertices = vor.vertices[region]
    hull = ConvexHull(vertices)

    # find the faces ant their vertices
    faces = []
    for eq in hull.equations:
        normal = eq[:3]
        d = eq[3]
        # vertices that belong to the plane
        idx = [
            i for i, v in enumerate(vertices)
            if np.isclose(np.dot(normal, v) + d, 0, atol=1e-8)
        ]
        if len(idx) < 3:
            continue

        # order the vertices in the plane
        pts = vertices[idx]

        center = pts.mean(axis=0)

        # ortonormal base in the plane
        n = normal / np.linalg.norm(normal)
        ref = pts[0] - center
        ref /= np.linalg.norm(ref)
        u = ref
        v = np.cross(n, u)

        # polar angles
        angles = []
        for p in pts:
            vec = p - center
            x = np.dot(vec, u)
            y = np.dot(vec, v)
            angles.append(np.arctan2(y, x))

        order = np.argsort(angles)
        ordered_idx = [idx[i] for i in order]

        faces.append(ordered_idx)

    # remove duplicates
    unique_faces = []
    for f in faces:
        s = sorted(f)
        if s not in [sorted(g) for g in unique_faces]:
            unique_faces.append(f)

    # triangulation of the faces
    i_list, j_list, k_list = [], [], []
    for face in unique_faces:
        for t in range(1, len(face)-1):
            i_list.append(face[0])
            j_list.append(face[t])
            k_list.append(face[t+1])
    
    # plot the faces
    fig.add_trace(go.Mesh3d(
        x=vertices[:,0],
        y=vertices[:,1],
        z=vertices[:,2],
        i=i_list,
        j=j_list,
        k=k_list,
        opacity=0.7,
        color='magenta',
        flatshading=True,
        lighting=dict(ambient=1.0, diffuse=0.0, specular=0.0),
        showscale=False
    ))

    # find the edges
    edges = set()
    for face in unique_faces:
        for a, b in zip(face, face[1:] + [face[0]]):
            edges.add(tuple(sorted((a, b))))
    
    # plot the edges
    for e in edges:
        fig.add_trace(go.Scatter3d(
            x=[vertices[e[0],0], vertices[e[1],0]],
            y=[vertices[e[0],1], vertices[e[1],1]],
            z=[vertices[e[0],2], vertices[e[1],2]],
            mode='lines',
            line=dict(width=4, color="red"),
            showlegend=False
        ))

        
if __name__ == "__main__":
    
    # Parse the input arguments
    parser = argparse.ArgumentParser(
        description="Plot conventional unit cell and optionally primitive and/or Wigner-Seitz cells."
    )
    parser.add_argument(
        "--primitive",
        action="store_true",
        help="Also plot the primitive cell."
    )
    parser.add_argument(
        "--ws",
        action="store_true",
        help="Also plot Wigner-Seitz cell."
    )
    # possible lattice abbreviations
    sc_ab = ["sc", "SC", "cP", "CUB"]               # simple cubic
    bcc_ab = ["bcc", "BCC", "cI"]                   # body-centered cubic
    fcc_ab = ["fcc", "FCC", "cF", "ccp"]            # face-centered cubic
    st_ab = ["st", "ST", "tP", "TET"]               # simple tetragonal
    bct_ab = ["bct", "BCT", "tI"]                   # body-centered tetragonal
    oP_ab = ["so", "SO", "oP", "orc", "ORC"]        # simple orthorhombic
    oS_ab = ["os", "oS", "orcc", "ORCC", "oC"]      # base-centered orthorhombic
    bco_ab = ["bco", "BCO", "orci", "ORCI", "oI"]   # body-centered orthorhombic
    fco_ab = ["fco", "FCO", "orcf", "ORCF", "oF"]   # face-centered orthorhombic
    mP_ab = ["sm", "SM", "mcl", "MCL", "mP"]        # simple monoclinic
    bcm_ab = ["bcm", "BCM", "mclc", "MCLC", "mS"]   # base-centered monoclinic
    tri_ab = ["tri", "TRI", "T", "aP", "tricl"]     # triclinic
    hex_ab = ["hex", "HEX", "sh", "SH", "hP"]       # hexagonal
    rhl_ab = ["rhl", "RHL", "hR"]                   # rhombohedral
    hcp_ab = ["hcp", "HCP", "cph", "hP2"]           # hexagonal close packed
    dc_ab = ["diam", "DIAM", "dc", "DC", "A4", "cF8"] # diamond
    parser.add_argument(
        "--lattice",
        type=str,
        default="bcc",
        choices=sc_ab+bcc_ab+fcc_ab+st_ab+bct_ab+oP_ab+oS_ab+bco_ab+fco_ab+mP_ab+bcm_ab+tri_ab+hex_ab+rhl_ab+hcp_ab+dc_ab,
        help="Choose a Bravais lattice, hexagonal close packed or diamond."
    )
    args = parser.parse_args()
    if len(sys.argv) == 1:
        print()
        print(parser.print_help())

    # import standard structures from ASE package
    from ase.lattice.cubic import SimpleCubic, BodyCenteredCubic, FaceCenteredCubic, Diamond
    from ase.lattice.tetragonal import SimpleTetragonal, CenteredTetragonal
    from ase.lattice.orthorhombic import SimpleOrthorhombic, BaseCenteredOrthorhombic, FaceCenteredOrthorhombic, BodyCenteredOrthorhombic
    from ase.lattice.monoclinic import SimpleMonoclinic, BaseCenteredMonoclinic
    from ase.lattice.triclinic import Triclinic
    from ase.lattice.hexagonal import Hexagonal, HexagonalClosedPacked

    # define the chosen conventional unit cell
    if args.lattice in sc_ab:
        conventional = SimpleCubic(latticeconstant=1, symbol="Fe")
        texto = "Simple&nbsp;Cubic"
        texto2 = "a=b=c&nbsp;&nbsp;&#945;=&#946;=&#947;=90<sup>o</sup>"
    elif args.lattice in bcc_ab:
        conventional = BodyCenteredCubic(symbol="Fe")
        texto = "Body-Centered&nbsp;Cubic"
        texto2 = "a=b=c&nbsp;&nbsp;&#945;=&#946;=&#947;=90<sup>o</sup>"
    elif args.lattice in fcc_ab:
        conventional = FaceCenteredCubic(latticeconstant=1, symbol="Fe")
        texto = "Face-Centered&nbsp;Cubic"
        texto2 = "a=b=c&nbsp;&nbsp;&#945;=&#946;=&#947;=90<sup>o</sup>"
    elif args.lattice in st_ab:
        conventional = SimpleTetragonal(latticeconstant=(1,1.5), symbol="Fe")
        texto = "Simple&nbsp;Tetragonal"
        texto2 = "a=b&#8800;c&nbsp;&nbsp;&#945;=&#946;=&#947;=90<sup>o</sup>"
    elif args.lattice in bct_ab:
        conventional = CenteredTetragonal(latticeconstant=(1,1.5), symbol="Fe")
        texto = "Body-Centered&nbsp;Tetragonal"
        texto2 = "a=b&#8800;c&nbsp;&nbsp;&#945;=&#946;=&#947;=90<sup>o</sup>"
    elif args.lattice in oP_ab:
        conventional = SimpleOrthorhombic(latticeconstant=(1,1.5,2), symbol="Fe")
        texto = "Simple&nbsp;Orthorhombic"
        texto2 = "a&#8800;b&#8800;c&nbsp;&nbsp;&#945;=&#946;=&#947;=90<sup>o</sup>"
    elif args.lattice in oS_ab:
        conventional = BaseCenteredOrthorhombic(latticeconstant=(1,1.5,2), symbol="Fe")
        texto = "Base-Centered&nbsp;Orthorhombic"
        texto2 = "a&#8800;b&#8800;c&nbsp;&nbsp;&#945;=&#946;=&#947;=90<sup>o</sup>"
    elif args.lattice in bco_ab:
        conventional = BodyCenteredOrthorhombic(latticeconstant=(1,1.5,2), symbol="Fe")
        texto = "Body-Centered&nbsp;Orthorhombic"
        texto2 = "a&#8800;b&#8800;c&nbsp;&nbsp;&#945;=&#946;=&#947;=90<sup>o</sup>"
    elif args.lattice in fco_ab:
        conventional = FaceCenteredOrthorhombic(latticeconstant=(1,1.5,2), symbol="Fe")
        texto = "Face-Centered&nbsp;Orthorhombic"
        texto2 = "a&#8800;b&#8800;c&nbsp;&nbsp;&#945;=&#946;=&#947;=90<sup>o</sup>"
    elif args.lattice in mP_ab:
        conventional = SimpleMonoclinic(latticeconstant=(1,1.5,2,75), symbol="Fe")
        # trick to keep the same coordinate system, not necessary for orthogonal cells
        conventional = spglib.find_primitive((conventional.get_cell(), conventional.get_scaled_positions(), conventional.get_atomic_numbers()))
        conventional = Atoms(cell=conventional[0], scaled_positions=[[0,0,0]], symbols=[26])
        texto = "Simple&nbsp;Monoclinic"
        texto2 = "a&#8800;b&#8800;c&nbsp;&nbsp;&#945;=&#947;=90<sup>o</sup>&#8800;&#946;"
    elif args.lattice in bcm_ab:
        conventional = BaseCenteredMonoclinic(latticeconstant=(1,1.5,2,75), symbol="Fe")
        # trick to keep the same coordinate system, not necessary for orthogonal cells
        conventional = spglib.find_primitive((conventional.get_cell(), conventional.get_scaled_positions(), conventional.get_atomic_numbers()))
        conventional = Atoms(cell=conventional[0], scaled_positions=[[0,0,0],[0.5,0.5,0]], symbols=[26,26])
        texto = "Base-Centered&nbsp;Monoclinic"
        texto2 = "a&#8800;b&#8800;c&nbsp;&nbsp;&#945;=&#947;=90<sup>o</sup>&#8800;&#946;"
    elif args.lattice in tri_ab:
        conventional = Triclinic(latticeconstant=(1,1.5,2,50,60,75), symbol="Fe")
        # trick to keep the same coordinate system, not necessary for orthogonal cells
        conventional = spglib.find_primitive((conventional.get_cell(), conventional.get_scaled_positions(), conventional.get_atomic_numbers()))
        conventional = Atoms(cell=conventional[0], scaled_positions=[[0,0,0]], symbols=[26])
        texto = "Triclinic"
        texto2 = "a&#8800;b&#8800;c&nbsp;&nbsp;&#945;&#8800;&#946;&#8800;&#947;&#8800;90<sup>o</sup>"
    elif args.lattice in hex_ab:
        conventional = Hexagonal(latticeconstant=(1,1.5), symbol="Fe")
        texto = "Hexagonal"
        texto2 = "a=b&#8800;c&nbsp;&nbsp;&#945;=&#946;=90<sup>o</sup>&nbsp;&nbsp;&#947;=120<sup>o</sup>"
    elif args.lattice in rhl_ab:
        # rhombohedral is a triclinic with equal angles (different from 90 and 60) and with equal edges
        conventional = Triclinic(latticeconstant=(1,1,1,75,75,75), symbol="Fe")
        # trick to keep the same coordinate system, not necessary for orthogonal cells
        conventional = spglib.find_primitive((conventional.get_cell(), conventional.get_scaled_positions(), conventional.get_atomic_numbers()))
        conventional = Atoms(cell=conventional[0], scaled_positions=[[0,0,0]], symbols=[26])
        texto = "Rhombohedral (Trigonal)"
        texto2 = "a=b=c&nbsp;&nbsp;&#945;=&#946;=&#947;&#8800;90<sup>o</sup>&#8800;60<sup>o</sup>"
    elif args.lattice in hcp_ab:
        conventional = HexagonalClosedPacked(latticeconstant=(1,np.sqrt(8/3)), symbol="Fe")
        texto = "Hexagonal&nbsp;Close&nbsp;Packed"
        texto2 = "a=b&#8800;c&nbsp;&nbsp;&#945;=&#946;=90<sup>o</sup>&nbsp;&nbsp;&#947;=120<sup>o</sup>"
    elif args.lattice in dc_ab:
        conventional = Diamond(latticeconstant=(1), symbol="Fe")
        texto = "Diamond"
        texto2 = "a=b=c&nbsp;&nbsp;&#945;=&#946;=&#947;=90<sup>o</sup>"      

    # initialize the plot
    fig = go.Figure()

    # plot the conventional unit cell
    plot_conventional_cell(fig, conventional)

    # Title and subtitle
    fig.add_annotation(
        xref="paper",
        yref="paper",
        x=0.5,       # 0 = esquerda, 1 = direita
        y=0.99,       # 0 = baixo, 1 = topo
        text=texto,
        showarrow=False,
        font=dict(size=25, color="darkgray"),
        font_family="Arial",
        xanchor="center"
        )
    fig.add_annotation(
        xref="paper",
        yref="paper",
        x=0.5,       # 0 = esquerda, 1 = direita
        y=0.95,       # 0 = baixo, 1 = topo
        text=texto2,
        showarrow=False,
        font=dict(size=18, color="darkgray"),
        font_family="DeJaVu Sans",
        xanchor="center"
        )
   
    # if chosen plot the primitive and the Wiger-Seitz (Voronoi) cells
    if args.primitive:
        plot_primitive_cell(fig, conventional)
    if args.ws:
        plot_ws_cell(fig, conventional)
  
    # set initial camera view
    camera = dict(
        eye=dict(x=1.3, y=1.6, z=1),
        projection=dict(type = 'perspective') # default; another option: orthographic
    )
    fig.update_layout(scene_camera=camera)

    # show the figure
    fig.show()