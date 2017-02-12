import time
start = time.time() #faccio partire il tempo 

############## IMPORT LIBRARIES ##############
from itertools import chain
from collections import defaultdict

import numpy as np
import pprint as pp
import math
import itertools
import operator


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
def node_distance():
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

#rimuovere nodi solo con 0
def remove_zero_path(my_dict):
	bool_elim = False
	for i in range(1, len(my_dict)+1):
		if len(my_dict[i]) == 1:
			bool_elim = True
			elim = i

	if bool_elim:
		del my_dict[elim]
	return my_dict

#controlla alpha condition, new_path e' in path con anche il nuovo nodo, new_node e' il nuovo nodo
def check_alpha(new_path, new_node):

	dist_tot = 0 #inizializzo distanza totale a zero
	times_alpha = ALPHA*neighbor[new_node][0] #alpha + distanza di new_node da 0
	
	for i in range (len(new_path)-1):
		dist_tot = dist_tot + node_dist(new_path[i], new_path[i+1])
	
	print "\nDistanza totale path: ", dist_tot # dist_tot distanza da il nodo mio agli altri
	
	if dist_tot <= times_alpha:
		print "Condizione alpha soddisfatta, il path col nuovo nodo va bene"
		return True
	
	else:
		print "Condizione alpha NON soddisfatta, path da scartare"
		return False

#creo cluster: creo un dizionario.
#le key sono i nodi, i value sono una lista con i nodi all'interno del raggio alpha*distanza da root
def create_cluster():
	print "Inizio a creare cluster!"
	single_cluster = []
	for key in node.items(): #scandisco tutti i nodi
		if key[0] != 0: #salto il nodo 0
			alpha_range = ALPHA*neighbor[key[0]][0]
			node_sorted = sorted(neighbor[key[0]].items(), key=operator.itemgetter(1)) #ordinare per vicinanza i nodi rispetto al nodo tra quadre
			del single_cluster[:]
			for j in range (len(node_sorted)):
				if node_sorted[j][0] != 0: #il nodo 0 (scuola) non deve essere nel cluster
					if node_sorted[j][1] <= alpha_range:
						single_cluster.append(node_sorted[j][0])
		
			cluster[key[0]] = list(single_cluster) #copia il cluster attuale nel dizionario di cluster

	return cluster

#ritorna il cluster piu' grande. Ritorna lunghezza, valori cluster e id cluster. magari si puo' far ritornare meno roba
def getMaxCluster(my_cluster):



    return max((len(v), v, k) for k, v in my_cluster.iteritems())

#instanzia una lista con tutti i nodi non presi nella soluzione
def initialize_queue():
	for i in range(1, n+1):
		queue.append(i)

	return queue
############## VARIABLES ##############

#initialize dictionary for bus stop coordinates
coord_x = {} #per coordinate x quando parso il dat
coord_y = {} #per coordinate y quando parso il dat
neighbor = {} #ogni nodo con gli altri per distanza
distance = {} #distanza da un nodo ad un altro, per poi metterla in neighbor
cluster = {} #cluster di ogni nodo (i nodi all'interno del raggio alpha*distanza da root)
queue = [] #nodi non ancora assegnati

tree = defaultdict(list) #lista soluzioni

file = 'res/pedibus_10.dat'

############## BODY ##############
n, ALPHA, node = parse_dat_file(file)

#print parameters for check
print "n: ",n, "\n" "ALPHA: ", ALPHA, "\n\n"

neighbor = node_distance() 

cluster = create_cluster()
queue = initialize_queue()



#pp.pprint(cluster)

print getMaxCluster(cluster)



############## END BODY ##############
#time
print '\nIt took', time.time()-start, 'seconds.'