import numpy as np
import time
import math
import pprint as pp
from itertools import chain
from collections import defaultdict
start = time.time()

############## FUNCTION DECLARATION ##############
def parse_dat_file(dat_file):
	file_dat = np.genfromtxt(file, delimiter='\n', dtype=None)

	n = int(file_dat[1][11:]) #parse param n: dimension of array

	alpha = float(file_dat[3][15:]) #parse param alpha
	file_dat = file_dat[5:]

	raw_x = []
	raw_y = [] 

	#start split coord x in vector raw_x and idem for y
	for row in file_dat:
		if "coordX" in row:
			isX = True
			isY = False
		if "coordY" in row:
			isX = False
			isY = True
		if "d [*,*]" in row:
			isY = False

		if isX:
			raw_x.append(" ".join(row.split()))

		if isY:
			raw_y.append(" ".join(row.split()))


	#delete initial words and final semicolumn
	raw_x.pop(0)
	raw_x.pop(len(raw_x)-1)
	raw_y.pop(0)
	raw_y.pop(len(raw_y)-1)

	raw_x =' '.join(raw_x)
	raw_x = raw_x.split(' ')
	raw_y =' '.join(raw_y)
	raw_y = raw_y.split(' ')

	#transfer vector raw_x in a dictionary. key=index, value=coordX
	i=0
	for column in raw_x:
		if i%2 == 0:
			even = int(column)
		if i%2 != 0:
			coord_x[even] = int(column)

		i = i+1

	#transfer vector raw_y in a dictionary. key=index, value=coordY
	i=0
	for column in raw_y:
		if i%2 == 0:
			even = int(column)
		if i%2 != 0:
			coord_y[even] = int(column)

		i = i+1


	#possibile ottimizzare le fusione in un unico dizionario, anche piu sopra
	#merge the two dictionaries
	coord = defaultdict(list)
	for k, v in chain(coord_x.items(), coord_y.items()):
    		coord[k].append(v)
	
	return n, alpha, coord

def node_dist(index_1, index_2):
	sub_x = math.pow((node[index_1][0] - node[index_2][0]), 2)
	sub_y = math.pow((node[index_1][1] - node[index_2][1]), 2)
	return math.sqrt(sub_x + sub_y)

def compute_distance():
	for key1, value1 in node.items():
		distance.clear()
		for key2, value2 in node.items():
			if key1 != key2:
				distance[key2] = node_dist(key1, key2)
				neighbor[key1] = distance.copy()

	return neighbor

############## VARIABLES ##############

#initialize dictionary for bus stop coordinates
coord_x = {}
coord_y = {}
neighbor = {}
distance = {}

file = 'res/pedibus_10.dat'

############## BODY ##############
n, alpha, node = parse_dat_file(file)




pp.pprint(compute_distance())

#print parameters for check
print "\nn: ",n, "\n" "alpha: ", alpha, "\n", "nodes:", node

#time
print '\nIt took', time.time()-start, 'seconds.'