import numpy as np
import time
import math
import copy
import pprint as pp
import operator
import sys
from itertools import chain
from collections import defaultdict
start = time.time()


############## VARIABLES ##############

# file dei dati:
#se non gli metto niente prendo il file inserito qua
if len(sys.argv) == 1:
	file = 'pedibus_30.dat'
#se inserisco un file dat dal terminale prende quello

else: file = sys.argv[1]

############## FUNCTION DECLARATION ##############
#Parsa il file, occhio che ritorna 5 valori, costs e' una matrice con tutti i costi
def parse_dat_file(dat_file):
	file_dat = np.genfromtxt(dat_file, delimiter='\n', dtype=None)

	cast = 0

	if "data;" in file_dat[0]:
		cast = 0
	else: cast = 1


	n = int(file_dat[1-cast][11:]) #parse param n: dimension of array

	ALPHA = float(file_dat[3-cast][15:]) #parse param alpha
	value = 5-cast
	file_dat = file_dat[value:]

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

def is_reachable(center_node, other_node):
	d1 = costs[center_node][0]
	d2 = costs[other_node][0]

	if costs[center_node][other_node]+d2<=d1*ALPHA:
		return True
	else: 
		return False

def concat(path):
	key = "";
	for i in range (0,len(path)):
		key=key+"-"+str(path[i])
	return key

#calcola il pericolo di un path
def compute_danger(my_path):
	path_danger = 0
	for i in range(0, len(my_path)-1):
		path_danger = path_danger + danger[my_path[i+1]][my_path[i]]

	return path_danger

def init_reachables(center_node):
	node_list = {};
	#init reachability
	for i in range (1,n+1):
		if i!=center_node and is_reachable(center_node, i):
			node_list[str(i)] = node_dist(center_node,i)
			#validated_paths[concat([center_node,i])] = [center_node,i]
	return node_list

def init_reachable_by(node):
	reachable_by = {};
	#init reachability
	for i in range (1,n+1):
		if i!=node and str(node) in reachables[i]:
			reachable_by[i] = node_dist(node,i)
			#validated_paths[concat([center_node,i])] = [center_node,i]
	return reachable_by

def check_path(old_path,new_node):
	path_temp = copy.copy(old_path)
	path_temp.append(new_node)
	#controlla se old_path + new node validato
	if(concat(path_temp) in validated_paths):
		return True, path_temp

	#TODO migliora
	if(concat(old_path) in validated_paths):
		dist = validated_paths[concat(old_path)]
		dist = dist + costs[old_path[-1]][new_node]

		if(dist<costs[new_node][0]*ALPHA):
			validated_paths[concat(path_temp)] = dist
			return True, path_temp


	return False, old_path

def explore_path(prec_path,my_node,index):
	if(not is_reachable_by[my_node]):
		basic_solution.append(prec_path)
		return prec_path
	
	check_node = is_reachable_by[my_node][index][0]
	if check_node in nodi_disponibili:
		prec_node = check_node

	else: 
		index+=1
		if(index<len(is_reachable_by[my_node])):
			return explore_path(prec_path,my_node,index)
		else:
			basic_solution.append(prec_path)
			return prec_path

	bool_path, prec_path = check_path(prec_path, prec_node)
	if(bool_path):
		nodi_disponibili.remove(prec_node)
		zero_sorted_paths.remove((prec_node,costs[prec_node][0]))

		#esplora piu profondo
		return explore_path(prec_path,prec_node,0)
	
	else:
		#esplora altro ramo
		index+=1
		if(index<len(is_reachable_by[my_node])):
			return explore_path(prec_path,my_node,index)
		else:
			basic_solution.append(prec_path)
			return prec_path

def reverse_solution(solution):
	for pat in solution:
		pat.reverse()

def print_solution_vertical(solution):
	sol = {};
	
	for i in range (1,(n+1)):
		sol[i] = 0

	for path in solution:
		for j in range(0,(len(path)-1)):
			sol[path[j]]=path[j+1]

	for k in range (1,n+1):
		print k," ",sol[k]

def print_solution_to_file(solution):
	sol = {};
	output_name = "pedibus_" + str(n) + ".sol"

	file = open(output_name, "w")
	
	for i in range (1,(n+1)):
		sol[i] = 0

	for path in solution:
		for j in range(0,(len(path)-1)):
			sol[path[j]]=path[j+1]

	for k in range (1,n+1):
		print >>file, k,sol[k]

def compute_danger_sol(my_sol):
	total_danger = 0
	for s_path in my_sol:
		total_danger = total_danger + compute_danger(s_path)

	return total_danger

def compute_challenge_value(leaves,danger):
	beta = 0.1
	if(n>10 and n <= 100):
		beta = 0.01
	if(n>100 and n <= 1000):
		beta = 0.001
	if (n > 1000):
		beta = 0.0001
	return round(leaves+(danger*beta),4)

def iterate_last_node(my_risk, my_node, index):
	#calcolo il rischio (nodo preso - ultimo nodo degli altri patthini)
	val = 0
	isNewPath = False
	for pat in sol_cpy:
	
		test_danger = danger[my_node][pat[-1]]
		best_local_risk = my_risk


		#print "\n\nrisky da comparare : ", my_risk, test_danger
		#se danger e' zero vuol dire che sto calcolando il danger con me stesso
		if test_danger != 0:
			#guardo se e' minore del path precedente
			if test_danger < my_risk:
				if test_danger < best_local_risk:
					#se va bene vedo se il path e' valido
					bool_path, pat = check_path(pat, my_node)
					#print "\ncontorllo il check path ", bool_path, pat

					#se path e' valido lo modifico in sol_cpy
					if bool_path:
						best_local_risk = test_danger
						best_index = val
						isNewPath = True

		if isNewPath == True:
			if val == (len(sol_cpy)-1):
				sol_cpy[index].remove(my_node)
				sol_cpy[best_index].append(my_node)
				return sol_cpy

		val = val + 1
		#print "sono l'indice sbarazzino: ", val
############## VARIABLES ##############


# contiene per ogni nodo i nodi raggiungibili
zero_paths = {}
zero_sorted_paths = []
reachables = {}
is_reachable_by = {}

nodi_disponibili = [];

validated_paths = {}

basic_solution = []

#initialize dictionary for bus stop coordinates
coord_x = {} #per coordinate x quando parso il dat
coord_y = {} #per coordinate y quando parso il dat
danger = []
tree = defaultdict(list) #lista soluzioni



############## BODY ##############
n, ALPHA, node, danger, costs = parse_dat_file(file)

BEST_LEAVES = n
BEST_RISK = 9999
BEST_SOL = []


#print parameters for check
print "n: ", n, "\n" "ALPHA: ", ALPHA, "\n\n"
#pp.pprint(danger)


#INIZIALIZZA REACHABLES // ZERO PATHS // NODI DISP
for i in range (1,n+1):
	reachables[i]=init_reachables(i)
	zero_paths[i] = costs[i][0]
	nodi_disponibili.append(i)

#INIZIALIZZA ZERO PATHS
zero_sorted_paths = sorted(zero_paths.items(), key=operator.itemgetter(1))

#INIZIALIZZA IS_REACHABLE_BY
for i in range (1,n+1):
	x = init_reachable_by(i)
	is_reachable_by[i] = sorted(x.items(), key=operator.itemgetter(1))


#local_solution = []
#nodi_disp = [1...n]

while (len(zero_sorted_paths) > 0 and len(basic_solution)<=BEST_LEAVES):
	current_path = [0]
	#prendi il piu vicino V a zero
	current_node = zero_sorted_paths[0][0]

	#creo current_path = [0,V]
	current_path.append(current_node)

	validated_paths[concat(current_path)] = costs[current_node][0]
	#rimuovo V dai nodi_disponibili
	nodi_disponibili.remove(current_node)
	zero_sorted_paths.remove((current_node,costs[current_node][0]))


	explore_path(current_path,current_node,0)



BEST_SOL = copy.deepcopy(basic_solution)
BEST_LEAVES = len(basic_solution)
BEST_RISK = compute_danger_sol(basic_solution)


# ESPLORA SOLUZIONI ALTERNATIVE DA 0 E CONFRONTA

for i in range (1,n):

 	selected_node = i
 	#reset nodi disp
 	nodi_disponibili = []
 	zero_sorted_paths = []

 	for j in range (1,n+1):
 		nodi_disponibili.append(j)

 	#reset basic solution
	basic_solution = []
	#reset zero sorted
	zero_sorted_paths = sorted(zero_paths.items(), key=operator.itemgetter(1))

 	while (len(zero_sorted_paths) > 0 and len(basic_solution)<=BEST_LEAVES):
 		current_path = [0]
 		#prendi l'i-esimo nodo piu vicino a zero
 		current_node = zero_sorted_paths[selected_node][0]
 		selected_node = 0
 		#creo current_path = [0,V]
 		current_path.append(current_node)

 		validated_paths[concat(current_path)] = costs[current_node][0]
 		#rimuovo V dai nodi_disponibili
 		nodi_disponibili.remove(current_node)
 		zero_sorted_paths.remove((current_node,costs[current_node][0]))

 		explore_path(current_path,current_node,0)

 	# UPDATE BEST IF NEEDED
 	new_leaves = len(basic_solution)
 	new_risk = compute_danger_sol(basic_solution)
 	if(new_leaves<BEST_LEAVES or (new_leaves==BEST_LEAVES and new_risk<BEST_RISK)):
 		BEST_SOL = basic_solution
 		BEST_LEAVES = new_leaves
 		BEST_RISK = new_risk



#creo copia soluzioni
sol_cpy = copy.deepcopy(BEST_SOL)

for i in range(0, len(sol_cpy)):
	#prendo l'ultimo nodo della prima soluzione
	last_node = sol_cpy[i][-1]
	penultim = sol_cpy[i][-2]

	#print "nodi in gioco", last_node, penultim
	#prendo il rischio (nodo preso-penultimo nodo)
	last_risk = danger[last_node][penultim]

	iterate_last_node(last_risk, last_node, i)


BEST_SOL = sol_cpy

print "\n\n----------------------------------------------------\n"

print "BEST SOLUTION:"
print BEST_SOL

BEST_RISK = compute_danger_sol(BEST_SOL)
BEST_LEAVES = len(BEST_SOL)

print "\nLEAVES:",BEST_LEAVES
print "DANGER:",BEST_RISK
print "CHALLENGE VALUE:",compute_challenge_value(BEST_LEAVES,BEST_RISK),"\n"
#per ogni nodo 
#reverse_solution(BEST_SOL)
#print_solution_vertical(BEST_SOL)

print "----------------------------------------------------"

#time
time_final = time.time()-start
print 'TOTAL time:', round(time_final,3), 'seconds.\n\n'
reverse_solution(BEST_SOL)
print_solution_vertical(BEST_SOL)

print 'SOLUTION SAVED IN FILE: pedibus_' + str(n) + ".sol\n"
print_solution_to_file(BEST_SOL)


############# COME FUNZIA #############
#per ogni nodo che contiene V si prende il piu vicino U
#controllo U-V-0
	#se path ok:
		#aggiorno current_path
		#rimuovo U dai nodi_disponibili
	#se path non ok: 


#per ogni nodo che contiene U prendo il piu vicino K
#controllo K-U-V-0
	#se si
#rimuovo U dai nodi_disponibili
