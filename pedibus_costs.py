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
#Parsa il file, occhio che ritorna 5 valori, costs e' una matrice con tutti i costi
def parse_dat_file(dat_file):
	file_dat = np.genfromtxt(file, delimiter='\n', dtype=None)

	n = int(file_dat[1][11:]) #parse param n: dimension of array

	ALPHA = float(file_dat[3][15:]) #parse param alpha
	file_dat = file_dat[5:]

	raw_x = []
	raw_y = [] 
	raw_d = []
	costs = []
	#start split coord x in vector raw_x and idem for y
	for row in file_dat:
		if "coordX" in row:
			isX = True
			isY = False
			isD = False
		if "coordY" in row:
			isX = False
			isY = True
			isD = False
		if "d [*,*]" in row:
			isY = False
			isD = True

		if isX:
			raw_x.append(" ".join(row.split()))

		if isY:
			raw_y.append(" ".join(row.split()))

		if isD: 
			raw_d.append(" ".join(row.split()))


	
	#delete initial words and final semicolumn
	raw_x.pop(0)
	raw_x.pop(len(raw_x)-1)
	raw_y.pop(0)
	raw_y.pop(len(raw_y)-1)
	raw_d.pop(0)
	raw_d.pop(0)
	raw_d.pop(len(raw_d)-1)

	raw_d =' '.join(raw_d)
	raw_d = raw_d.split(' ')

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

	#transfer raw_d in a matrix
	row = []
	danger = []
	for i in range (0, len(raw_d)+1):
		if (i%(n+2)) != 0:
			row.append(float(raw_d[i]))
		else:
			if i != 0:
				danger.append(row)
			row = []
	
	costs = [costs[:] for costs in [[0] * (n + 1)] * (n + 1)]

	for i in range(0, (n+1)):
		for j in range(0, (n+1)):
			costs[i][j] = float("{0:.4f}".format(math.sqrt((coord_x[i]-coord_x[j])**2 + (coord_y[i]-coord_y[j])**2)))


	#possibile ottimizzare le fusione in un unico dizionario, anche piu sopra
	#merge the two dictionaries
	coord = defaultdict(list)
	for k, v in chain(coord_x.items(), coord_y.items()):
    		coord[k].append(v)
	
	return n, ALPHA, coord, danger, costs

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

def validate_path(path):
	max_lenght = costs[path[0]][path[len(path)-1]]*ALPHA
	lenght = 0
	i = 0;
	while i < len(path)-1:
		lenght = lenght+costs[path[i]][path[i+1]]
		if lenght>max_lenght:
			return False;
		i=i+1
	if(len(path)>2):
		#check sub-path
		sub_path = path[1:len(path)]
		path_len = len(sub_path);

		#check cluster di path[1]
		first_node = sub_path[0]
		first_node_cluster = clusters[first_node]
		actual_depth = len(first_node_cluster) 

		if(actual_depth < path_len-1 or (sub_path not in clusters[first_node][len(sub_path)-2])):
			return False
		#return validate_path(path[1:len(path)])
	return True;

def is_reachable(center_node, other_node):
	d1 = costs[center_node][0]
	d2 = costs[other_node][0]

	if costs[center_node][other_node] + d2 <= d1*ALPHA:
		return True
	else: 
		return False



def compareLists(l1, l2):
	for i in range (len(array)):
		if array[i] == element:
			return True
	return False


def clusterize(center_node, depth):
	paths = []

	node_cluster = clusters[center_node]
	actual_depth = len(node_cluster) 

	#se il cluster is completo, esci
	if(center_node in complete_clusters):
		print "salto nodo ", center_node
		return paths

	#se il cluster precedente non esiste, tronca ed esci
	if(actual_depth <= depth-1):
		print "tronco cluster per nodo", center_node
		complete_clusters.append(center_node)
		cluster_depth[center_node] = actual_depth
		return paths

	for i in range (0, len(clusters[center_node][depth-1])):
		old_path = clusters[center_node][depth-1][i]

		for j in range (0, len(reachables[center_node])):
			new_node = reachables[center_node][j]
			if new_node not in old_path:
				#inserisco new_node in old_path in seconda posizione 
				new_path = copy.copy(old_path)
				new_path.insert(1,new_node)		
				if(validate_path(new_path)):
					paths.append(new_path)

	return paths


def init_reachables(center_node):
	node_list = [];
	#init reachability
	for i in range (1,n):
		if i != center_node and is_reachable(center_node, i):
			node_list.append(i)
	return node_list


def init_cluster(center_node):
	clusterZero = {};
	node_list = [];
	#node_list = center_node + node_list
	node_list.append([center_node,0]);
	clusterZero[0] = node_list;
	cluster_depth[center_node] = MAX_DEPTH-1;
	return clusterZero;
"""
def init_risk(center_node):
	riskZero = {};
	risk_lisk = [];
"""


def generate_cluster(depth):
	#create cluster 
	# DEPTH
	for i in range (1,n+1):
		node_list = clusterize(i, depth);
		if(len(node_list)>0):
			clusters[i][depth]=node_list;



def solve_tree():
	i=MAX_DEPTH-1;

	while i>=0:
		#per ogni cluster
		for j in range (1,n):
			#cerca il cluster di profondita i
			#se eiste
			if(cluster_depth[j]>i):
				#assegna array dei path
				pathList = clusters[j][i]
				#se esiste
				if(pathList):
					#seleziona la prima occorrenza
					path = pathList[0]
					
					solution.append(path);
					print "\n\nSelect path --->",path
					#rimuovi tutti i path che contengono i nodi del path scelto
					for node in path:
						if(node!=0):
							print "remove all ", node, " occurrencies"
							removeAllOccurrences(node)
#			

		print "\nClusters - SOLVE ITERATION ",MAX_DEPTH-i
		#pp.pprint(clusters)
		i=i-1



def removeAllOccurrences(node):
	for x in range (1,(n+1)):
		cluster=clusters[x];

		for y in range (0,MAX_DEPTH):

			clusters[node][y] = []

			if(cluster_depth[x]>y):
				pathList=cluster[y];
				pathListCopy=copy.copy(pathList)
			
				for path in pathListCopy:
					if node in path:
						pathList.remove(path)

#calcola il pericolo di un path
def compute_danger(my_path):
	path_danger = 0
	for i in range(0, len(my_path)-1):
		path_danger = path_danger + danger[my_path[i]][my_path[i+1]]

	return path_danger


#tra un vettori di path ritorna quello con meno dangerous
def min_dangerous(paths):
	min_danger = 9999
	min_danger_path = []
	for pat in paths:
		if compute_danger(pat) < min_danger:  
			min_danger = compute_danger(pat)
			min_danger_path = pat
	return min_danger_path

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

#contiene per ogni nodo la profondita massima del cluster
cluster_depth = {}

#contiene i nodi per i quali i cluster sono completi
complete_clusters = []

solution = [];

#initialize dictionary for bus stop coordinates
coord_x = {} #per coordinate x quando parso il dat
coord_y = {} #per coordinate y quando parso il dat
neighbor = {} #ogni nodo con gli altri per distanza
distance = {} #distanza da un nodo ad un altro, per poi metterla in neighbor
danger = []
tree = defaultdict(list) #lista soluzioni

file = 'res/pedibus_30.dat'


############## BODY ##############
n, ALPHA, node, danger, costs = parse_dat_file(file)

#MAD-DEPTH -> limite di profondita con cui vendono generati i cluster per ogni nodo
#puo andare da 1 a n, se troppo alto crasha il programma
MAX_DEPTH = 6

#print parameters for check
print "n: ", n, "\n" "ALPHA: ", ALPHA, "\n\n"
#pp.pprint(danger)


#neighbor = node_distance()


#INITIALIZIATION
for i in range (1,n+1):
	reachables[i]=init_reachables(i)
	clusters[i] = init_cluster(i)
	#risks[i] = init_risk()


#CLUSTER GENERATION
for i in range (1,MAX_DEPTH):
	print "\nCALCOLO CLUSTER LEVEL : ",i;
	generate_cluster(i)
	print "Fatto.\n";

time_clustering = time.time()-start

print "\nREACHABLES:"
pp.pprint(reachables)
print "\nCLUSTER DEPTHS:"
pp.pprint(cluster_depth)
print "\nCLUSTERS before solving:"
pp.pprint(clusters)


#SOLUTION
solve_tree()
print "\nSOLUTION PATHS:"
print solution

print "\nSOLUTION NEXT NODES:"
print_solution()

time_final = time.time()-start

#time
print '\n------------------------------------------------------'
print '\nClustering time:', round(time_clustering,3), 'seconds.'
print 'Solving time:', round(time_final-time_clustering,3), 'seconds.'
print 'TOTAL time:', round(time_final,3), 'seconds.\n\n'