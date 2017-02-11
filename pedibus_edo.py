import numpy as np
import time
import math
import pprint as pp
import itertools
import operator
from itertools import chain
from collections import defaultdict
start = time.time()

############## FUNCTION DECLARATION ##############
def parse_dat_file(dat_file):
	file_dat = np.genfromtxt(file, delimiter='\n', dtype=None)

	n = int(file_dat[1][11:]) #parse param n: dimension of array

	ALPHA = float(file_dat[3][15:]) #parse param alpha
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
	
	return n, ALPHA, coord

#calcola distanza euclidea tra due nodi
def node_dist(index_1, index_2):
	sub_x = math.pow((node[index_1][0] - node[index_2][0]), 2)
	sub_y = math.pow((node[index_1][1] - node[index_2][1]), 2)
	return math.sqrt(sub_x + sub_y)

#crea dizionario con distanza di un nodo ad ogni altro nodo
def compute_distance():
	for key1, value1 in node.items():
		distance.clear()
		for key2, value2 in node.items():
			if key1 != key2:
				distance[key2] = node_dist(key1, key2)
				neighbor[key1] = distance.copy()

	return neighbor

#popola l'albero della soluzione con la soluzione base
def create_starting_solution():
	for i in range(1,n+1):
			tree[i].append(i)
			tree[i].append(0)

	return tree

#eliminare il nodo myNode
def delete_node(myNode):
	for i in range (1, len(tree)+1):
		if myNode in tree[i]: 
			tree[i].remove(myNode)

def remove_zero_path(myDict):
	for i in range(1, len(myDict)+1):
		if len(myDict[i]) == 1:
			elim = i

	del myDict[elim]
	return myDict
############## VARIABLES ##############

#initialize dictionary for bus stop coordinates
coord_x = {} #per coordinate x quando parso il dat
coord_y = {} #per coordinate y quando parso il dat
neighbor = {} #ogni nodo con gli altri per distanza
distance = {} #distanza da un nodo ad un altro, per poi metterla in neighbor
tree = defaultdict(list) #lista soluzioni

file = 'res/pedibus_10.dat'

############## BODY ##############
n, ALPHA, node = parse_dat_file(file)

#print parameters for check
print "n: ",n, "\n" "ALPHA: ", ALPHA, "\n\n"

neighbor = compute_distance()

tree = create_starting_solution()
sorted_x = sorted(neighbor[0].items(), key=operator.itemgetter(1)) #ordinare per vicinanza i nodi rispetto al nodo zero (tra quadre)

pp.pprint(tree)

sorted_x = sorted(neighbor[1].items(), key=operator.itemgetter(1))
candidate_list = sorted_x[0] #candidate list: contiene in 0 il nodo e in 1 la distanza [nodo, distanza]
candidate_node = candidate_list[0]
candidate_dist = candidate_list[1]
print candidate_node
print neighbor[1][0], "\n"

if candidate_node + neighbor[1][0] < ALPHA*neighbor[candidate_node][0]:
	for i in range (1, n+1):
		if 1 in tree[i]:
			print candidate_node
			delete_node(candidate_node)
			tree[i].insert(0, candidate_node) #update path: inserisce candidate_node nella posizione 0 (primo della lista)
			print "ok, dovrei updatare path"
else: print "nada"

remove_zero_path(tree)
pp.pprint(tree)

print "\nSolution has", len(tree),"leaves"


#time
print '\nIt took', time.time()-start, 'seconds.'