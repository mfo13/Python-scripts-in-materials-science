
#!/usr/bin/env python

'''
Voronoi relaxation in 2D with periodic boundary conditions

Author: Marcelo Falcão de Oliveira
Affiliation: University of São Paulo 
             São Carlos School of Engineering
             Materials Engineering Department
e-mail: marcelo.falcao@usp.br

This python script is intended for teaching porposes.
You can use, copy to others or modify as you wish but at your own risk.
If you find it usefull for your work, please cite the source.

Packages needed:
numpy, matplotlib, scipy

August 2023

'''

howtouse = '''
# How to use:
# python voromaxent2d.py argv1 argv2 argv3 argv4 argv5
# - argv1: x unit cell size (integer)
# - argv2: y unit cell size (integer)
# - argv3: number of points per unit cell
'''

import sys
import numpy as np
import random as rnd
import matplotlib.pyplot as plt
from scipy.spatial import Voronoi, voronoi_plot_2d
import matplotlib.animation as animation

# pbc images
def pbc(base_,entrada_):
	saida_=[i for i in entrada_]
	for x in [-base_[0],np.array([0,0]),base_[0]]:
		for y in [-base_[1],np.array([0,0]),base_[1]]:
			if not (sum(x)==0 and sum(y)==0):
				soma=entrada_+x+y
				saida_.extend([i for i in soma])
	return saida_

# bring points to the central unit cell
def wrap(base_,entrada_):
	for i in range(len(entrada_)):
		if entrada_[i][0]<0: entrada_[i][0]+=base_[0][0]
		if entrada_[i][0]>=base_[0][0]: entrada_[i][0]-=base_[0][0]
		if entrada_[i][1]<0: entrada_[i][1]+=base_[1][1]
		if entrada_[i][1]>=base_[1][1]: entrada_[i][1]-=base_[1][1]
	return entrada_

# centralizes the points in the unit cell
def centra(base_,pontos_):
	centro=np.mean(pontos_,axis=0)
	dif=centro-np.mean(base_,axis=0)
	pontos_=pontos_-dif
	return pontos_

# rotates the group of points to align the largest distance with the unit cell diagonal
def gira(base_,pontos_):
	# find the most distant point from the center
	dif=pontos_-np.mean(base_,axis=0) # origin in the center of the unit cell
	norms=np.linalg.norm(dif,axis=1)
	imax=np.where(norms==np.max(norms))
	# sin of the angle between the direction of the distant point and the unit cell diagonal
	sent=np.dot(dif[imax[0][0]],np.array([base_[0][0],base_[1][1]]))/np.linalg.norm(dif[imax[0][0]])/np.linalg.norm(np.array([base_[0][0],base_[1][1]]))
	# rotation matrix
	if (1-sent**2)>=0:
		rmat=np.array([[sent,-np.sqrt(1-sent**2)],[np.sqrt(1-sent**2),sent]])
		pontos_=np.transpose(np.matmul(rmat,np.transpose(dif)))
		# centralization
		pontos_=pontos_+np.mean(base_,axis=0)
	return pontos_

# Voronoi relaxation and frame refresh
def optvoro(i):
	global ax, pontos, nframes, anim
	soma=0
	pontos=centra(base,pontos) # centralization
	vor=Voronoi(pbc(base,pontos))
	# relaxation
	for j in range(len(pontos)-1): # reference point
		medio=np.mean(vor.vertices[vor.regions[vor.point_region[j]]],axis=0)
		soma+=np.linalg.norm(pontos[j]-medio)
		pontos[j]=medio
	# refresh
	ax.clear()
	voronoi_plot_2d(vor, ax, show_vertices=False,line_colors='orange',clear=True)
	ax.plot([0,0,base[0][0],base[0][0],0],[0,base[1][1],base[1][1],0,0],color='green')
	# bottom dashed line
	ax.plot([-base[0][0]/2,1.5*base[0][0]],[0,0],color='green',ls=':')
	# upper dashed line
	ax.plot([-base[0][0]/2,1.5*base[0][0]],[base[1][1],base[1][1]],color='green',ls=':')
	# left dashed line
	ax.plot([0,0],[-base[1][1]/2,1.5*base[1][1]],color='green',ls=':')
	# right dashed line
	ax.plot([base[0][0],base[0][0]],[-base[1][1]/2,1.5*base[1][1]],color='green',ls=':')
	# axis sizes
	ax.axis([-base[0][0]/2,1.5*base[0][0],-base[1][1]/2,1.5*base[1][1]])
	nframes+=1
	ax.set_title('step: '+str(nframes))
	if soma<prec: anim.pause()


####################
# Main

prec=5e-2

# load user input
if len(sys.argv)<3 or 'h' in sys.argv or '-h' in sys.argv or 'help' in sys.argv or '-help' in sys.argv:
	sys.exit(howtouse)

# set base and number of points
base=np.array([[int(sys.argv[1]),0],[0,int(sys.argv[2])]])
numero_de_pontos=int(sys.argv[3])

# get base ratio
ratio=base[0][0]/base[1][1]

# definition of figure
fig, ax = plt.subplots(figsize=(6*ratio,6))

# randomize the initial points
pontosini=[]
for i in range(numero_de_pontos):
	pontosini.append(np.random.uniform(sum(base)))

# Initializaton
pontosini=centra(base,pontosini)
pontosini=gira(base,pontosini)
nframes=-1
pontos=pontosini

# animation function
anim = animation.FuncAnimation(fig, optvoro, interval=100)

plt.show()

# uncomment the lines bellow if you want to save a mp4 movie
# size=nframes
# nframes=-1
# pontos=pontosini
# anim = animation.FuncAnimation(fig, optvoro, interval=100, frames=size)
# anim.save('voronoi_relax_'+sys.argv[1]+'_'+sys.argv[2]+'_'+sys.argv[3]+'.mp4')

