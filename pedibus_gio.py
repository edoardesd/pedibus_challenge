import numpy as np
import time
import math
import copy
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
	sub_x = math.pow(abs(node[index_1][0] - node[index_2][0]), 2)
	sub_y = math.pow(abs(node[index_1][1] - node[index_2][1]), 2)
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

#controlla alpha condition
def check_alpha(my_path, new_node):
	tot_dist = 0 #inizializzo distanza totale a zero
	times_alpha = ALPHA*neighbor[new_node][0] #alpha + distanza di new_node da 0
	print "blblba ",times_alpha, neighbor[new_node][0]
	for i in range (len(my_path)-1):
		tot_dist = tot_dist + node_dist(my_path[i], my_path[i+1])
		print "\nDistanza totale path: ", tot_dist + neighbor[new_node][0] #ATTENZIONEEEEE, distanza da il nodo mio agli altri
	if tot_dist + neighbor[new_node][0] <= times_alpha:
		print "true"
		return True
	else:
		print "false"
		return False


def validate_path(path):
	max_lenght = node_dist(path[0],path[len(path)-1])*ALPHA
	lenght = 0
	i = 0;
	while i < len(path)-1:
		lenght = lenght+node_dist(path[i],path[i+1])	
		if lenght>max_lenght:
			return False;
		i=i+1
	if(len(path)>2):
		return validate_path(path[1:len(path)])
	return True;

def is_reachable(center_node, other_node):
	d1 = node_dist(center_node,0)
	d2 = node_dist(other_node,0)

	if node_dist(center_node,other_node)+d2<=d1*ALPHA:
		return True
	else: 
		return False


def contains(array, element):
	for i in range (len(array)):
		if array[i] == element:
			#print array," CONTAINS ",element,"= TRUE"
			return True
	#print array," CONTAINS ",element,"= FALSE"
	return False

def compareLists(l1, l2):
	for i in range (len(array)):
		if array[i] == element:
			return True
	return False


def clusterize(center_node, depth):
	paths = []
		
	for i in range (0,len(clusters[center_node][depth-1])):
		old_path = clusters[center_node][depth-1][i]

		for j in range (0,len(reachables[center_node])):
			new_node = reachables[center_node][j]
			if(not contains(old_path,new_node)):
				#inserisco new_node in old_path in seconda posizione 
				new_path = copy.copy(old_path);
				new_path.insert(1,new_node);		
				if(validate_path(new_path)):
					paths.append(new_path)

			#TROPPO DISPENDIOSO
			#controllo se il sotto path da new_node a 0 e gia stato validato nell'iterazione precedente
			#sub_path = new_path[1:len(new_path)]
			#for k in range (0,len(clusters[new_node][depth-1])):
			#	p = clusters[new_node][depth-1][k]
			#	if(p==sub_path):
					#se si, verifico il nuovo path
			#		if(validate_path(new_path)):
						#se si inserisco il nuovo path
			#			paths.append(new_path)


	return paths


def init_reachables(center_node):
	node_list = [];
	#init reachability
	for i in range (1,n):
		if i!=center_node and is_reachable(center_node, i):
			node_list.append(i)
	return node_list


def init_cluster(center_node):
	clusterZero = {};
	node_list = [];
	node_list.append([center_node,0]);
	clusterZero[0] = node_list;
	return clusterZero;
"""
def init_risk(center_node):
	riskZero = {};
	risk_lisk = [];
"""


def generate_cluster(depth):
	#create cluster 
	# DEPTH
	for i in range (1,n):
		node_list = clusterize(i, depth);
		clusters[i][depth]=node_list;



def solve_tree():
	i=MAX_DEPTH-1;
	while i>=0:
		for j in range (1,n):
			#trova il path piu lungo
			pathList = clusters[j][i]
			found = False;
			if(pathList):
				#seleziona la prima occorrenza
				path = pathList[0]
				found = True;
				solution.append(path);
				print "\n\nSelect path --->",path
				#rimuovi tutti i path che contengono i nodi del path scelto
				for node in path:
					if(node!=0):
						removeAllOccurrences(node)
			if(found):
				break;

		print "\nClusters - SOLVE ITERATION ",MAX_DEPTH-i
		pp.pprint(clusters)
		i=i-1



def removeAllOccurrences(node):
	for x in range (1,(n)):
		cluster=clusters[x];
		for y in range (0,MAX_DEPTH):
			pathList=cluster[y];
			pathListCopy=copy.copy(pathList)
			for path in pathListCopy:
				if(contains(path,node)):
					found=True;
					pathList.remove(path)


def print_solution():
	sol = {};
	for i in range (1,(n+1)):
		sol[i] = 0;

	for path in solution:
		for j in range(0,(len(path)-1)):
			sol[path[j]]=path[j+1]

	for k in range (1,n+1):
		print k," ",sol[k]

############## VARIABLES ##############

#CLUSTERS contiene un oggetto per ogni nodo X
#all'interno di ogni oggetto c'e un array [i] che contiere i path possibili da X a 0 in [i] spostamenti
#gia ALPHA validati
#
#	X: {0: [0], 					     // elementi raggiungibili
#		1: [[2,0]] 						 // path possibili con 1 spostamento
#		2: [[2,4,0],[2,8,0],[2,9,0]]  	 // path possibili con 2 spostamenti
#		3: [[2,4,8,0] ... ]   			 // path possibili con 3 spostamenti
#		.
#		.
#		n: [...]
#}
clusters = {}
risks = {}

# contiene per ogni nodo i nodi raggiungibili
reachables = {}

solution = [];

#initialize dictionary for bus stop coordinates
coord_x = {} #per coordinate x quando parso il dat
coord_y = {} #per coordinate y quando parso il dat
neighbor = {} #ogni nodo con gli altri per distanza
distance = {} #distanza da un nodo ad un altro, per poi metterla in neighbor
tree = defaultdict(list) #lista soluzioni

file = 'res/pedibus_20.dat'


############## BODY ##############
n, ALPHA, node = parse_dat_file(file)

#MAD-DEPTH -> limite di profondita con cui vendono generati i cluster per ogni nodo
#puo andare da 1 a n, se troppo alto crasha il programma
MAX_DEPTH = 5

#print parameters for check
print "n: ", n, "\n" "ALPHA: ", ALPHA, "\n\n"

neighbor = node_distance()

for i in range (1,n+1):
	reachables[i]=init_reachables(i)
	clusters[i] = init_cluster(i)
	#risks[i] = init_risk()

for i in range (1,MAX_DEPTH):
	print "\nCalcolo CLUSTER LEVEL : ",i;
	generate_cluster(i)
	print "Fatto.\n";


print "\nREACHABLES:"
pp.pprint(reachables)
print "\nCLUSTERS before solving:"
pp.pprint(clusters)

solve_tree()
print "\nSOLUTION PATHS:"
print solution

print "\nSOLUTION NEXT NODES:"
print_solution()

#time
print '\nIt took', time.time()-start, 'seconds.'