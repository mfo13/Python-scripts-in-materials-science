#!/usr/bin/env python

# makeBZpath.py
# This python script automatically produces a list of explicit or implicit k (or q) points along a Brillouin zone (BZ) path.
# Such a list can be directly used in the input files of pw.x, ph.x or matdyn.x binaries of Quantum-Espresso (QE).
# The script parses the crystal structure found in the input file used with pw.x, or in a cif file or in many other crystal file formats.
# The crystal structure is automatically detected and the suggested BZ path is produced with the approximate number of points requested by the user.
# Both path versions can be generated, with implicit as well as explicit points.
#
# You can use or distribut this script as you wish, without any garantee and under your entire responsability.
#
# If you improve this script, please, send me your improved version.
#
# Marcelo Falcão de Oliveira - University of São Paulo (marcelo.falcao@usp.br)
# Jan-Nov 2022

# Required packages: 
# ASE: https://pypi.org/project/ase/ or https://anaconda.org/conda-forge/ase
# seekpath: https://pypi.org/project/seekpath/ or https://anaconda.org/conda-forge/seekpath

howtouse = '''
# How to use
#
# $ python makeBZpath.py <input_filename> <arg1> <arg2> <arg3>
#
# - input_filename: is the input file in many formats (quantum-espresso, cif and many others, see https://wiki.fysik.dtu.dk/ase/ase/io/io.html#module-ase.io)
# - arg1: must be "implicit" or "explicit" depending on the desired BZ path format, i.e., implicit or explicit points 
# - arg2: is a natural number expressing the number of points you want in your BZ path. The output will be an approximation
# - arg3: is optional, a natural number of the "weight" regarding your points in the explicit BZ path
'''

# Output:
#              
# Imput file: >input_filename<
# Crystal with inversion symetry: >boolean<
# Extended Bravais lattice: >lattice designation code<
# Conventional lattice vectors:
# >matrix of lattice vectors if present<
# Primitive lattice vectors:
# >matrix of primitive lattice vectors<
#
# ### Number of main k or q points with an implicit BZ path, just copy and paste in your input file ###
#
# >number of k (or q) points<
# >list of main k or q points with weight (number of implicit points) with a comment (! k-point label)<
#
# or
#
# ### Number of k or q points and explicit BZ path, just copy and paste in your input file ###
#
# >number of k or q explicit points<
# >list of k or q points with weight (if requested) with a comment (!) when applicable: k-point label at the points of high symmetry (k-point path)<

# Details of the main packages needed:
#
# ASE (Atomic Simulation Environment) is a python library with the aim of setting up, steering, and analyzing atomistic simulations; developed by
# Ask Hjorth Larsen et al., The Atomic Simulation Environment—A Python library for working with atoms, J. Phys.: Condens. Matter 29, 273002 (2017)
# PyPI: https://pypi.org/project/ase/
# GitHub: https://github.com/rosswhitfield/ase
# Anaconda: https://anaconda.org/conda-forge/ase 
#
# SeeK-path is a python module to obtain band paths in the Brillouin zone of crystal structures; developed by
# - Y. Hinuma, G. Pizzi, Y. Kumagai, F. Oba, I. Tanaka, Band structure diagram paths based on crystallography, Comp. Mat. Sci. 128, 140 (2017)
# Its essential library is spglib, developed by
# - A. Togo, I. Tanaka, Spglib: a software library for crystal symmetry search, arXiv:1808.01590 (2018)
# PyPI: https://pypi.org/project/seekpath/
# GitHub: https://github.com/giovannipizzi/seekpath
# Anaconda: https://anaconda.org/conda-forge/seekpath

import sys
import numpy
import re
import ase.io
import seekpath

#######################################################
#           Main Script
#######################################################

if len(sys.argv)<3 or 'h' in sys.argv or '-h' in sys.argv or 'help' in sys.argv or '-help' in sys.argv:
    sys.exit(howtouse)

# reads the cell parameters, atomic positions and atomic species
try:
    entra = ase.io.read(sys.argv[1])
    cell = entra.get_cell()
    positions = entra.get_scaled_positions()
    numbers = entra.get_atomic_numbers()
except:
    sys.exit('\nInput file parsing error or input file not found.\n')

# imput for the seekpath functions
structure=[cell,positions,numbers]

# check if the user wants implicit or explicit output
if sys.argv[2]!='implicit' and sys.argv[2]!='explicit':
    sys.exit("\nYou must choose an implicit or explicit BZ path.\n")

# used for crytal identification and BZ path with implicit points
path = seekpath.get_path(structure,False)

# primary output
print (" ")
print ("Imput file: " + sys.argv[1])
print ("Crystal with inversion symetry: " + str(path.get('has_inversion_symmetry')))
print ("Extended Bravais lattice: " + path.get('bravais_lattice_extended'))
print ("Conventional lattice vectors:")
print (path.get('cont_lattice'))
print ("Primitive lattice vectors:")
print (path.get('primitive_lattice'))

# large step just to run get_explicit_k_path in order to get the minimum possible number of points (k-points path)
step = 100 
result = seekpath.get_explicit_k_path(structure,False,step)
# number of k-points (minus 1 in order to get the path length)
last = len(result.get('explicit_kpoints_rel')) - 1
length = result.get('explicit_kpoints_linearcoord')[last]
# total points requested by the user
try:
    totalpoints = int(sys.argv[3])
    if totalpoints <= 0: sys.error()
except:
    sys.exit('\nYou must choose the number of points for the BZ path with a positive integer.\n')

# path step size in order to generate an approximate number of requested q points  
step = length / totalpoints
result = seekpath.get_explicit_k_path(structure,False,step)

# refresh the total of points
totalpoints = (len(result.get('explicit_kpoints_rel')))

# main output
if sys.argv[2]=='implicit':
    print(" ")
    print ("### Number of k (or q) points with an implicit BZ path, just copy and paste in your input file ###")
    print(" ")
    pts = 2
    # get the number of main points
    for i in range(1,len(path.get('path'))):
        if path.get('path')[i-1][1]==path.get('path')[i][0]:
            pts += 1
        else:
            pts += 2
    print (str(pts))
    # print the main points, weights and labels
    w = 0
    seg = 0
    pend =  False
    for i in range(0,totalpoints):
        if result.get('explicit_kpoints_labels')[i]==path.get('path')[seg][1]:
            for k in path.get('point_coords')[path.get('path')[seg][0]]:
                print("{:1.10f}".format(k), end=" ")
            print (str(w)+' !'+path.get('path')[seg][0])
            w = 0
            if seg==(len(path.get('path'))-1):
                pend = True
            else:
                if path.get('path')[seg][1]!=path.get('path')[seg+1][0]:
                    pend = True
                    w = -1
            if pend:
                pend = False
                for k in path.get('point_coords')[path.get('path')[seg][1]]:
                    print("{:1.10f}".format(k), end=" ")
                print ('1 !'+path.get('path')[seg][1])
            seg += 1
        w += 1
    print (" ")

if sys.argv[2]=="explicit":
    print (" ")
    print ("### Number of k (or q) points and explicit BZ path, just copy and paste in your input file ###")
    print (" ")
    print (totalpoints)
    # check if the user wants weight and print, otherwise nothing
    if len(sys.argv)==5:
        try:
            weight = str(int(sys.argv[4]))
        except:
            sys.exit('\nThe optional weight must be an integer.\n')
    else:
        weight = ""
    for i in range(0,totalpoints):
        # check if the point is a special k-point and prints its label as a comment
        label = weight + re.sub(r'(\S+)',r' !\1', result.get('explicit_kpoints_labels')[i])
        for k in result.get('explicit_kpoints_rel')[i]:
            print("{:1.10f}".format(k), end=" ")
        print (label)
    print (" ")