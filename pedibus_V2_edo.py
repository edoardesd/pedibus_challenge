import numpy as np
import time
import math
import copy
import pprint as pp
import operator
import threading
from itertools import chain
from collections import defaultdict
start = time.time()


############# THREAD #################
class SolverThread (threading.Thread):
    def __init__(self, nodeDisp, zeroSort, threadCount):
        threading.Thread.__init__(self)
        self.nodeDisp = nodeDisp
        self.zeroSort = zeroSort
        self.threadCount = threadCount
        self.threadSolution = []
        self.threadLeaves = n 
        self.currentPath = []
        self.currNode = threadCount


    def run(self):	
        #self.threadSolution=solve_thread_run(self.clusters,self.first_path, self.threadCount)
        
		test(self.currentPath, self.currNode, self.threadSolution, self.nodeDisp, self.zeroSort, self.threadCount)      
		threadLock.acquire()
		if len(threadSolution) <= BEST_LEAVES:
			BEST_LEAVES = len(threadSolution)
			BEST_SOL = threadSolution
		threadLock.release()


def test(currentPath,currNode, threadSolution, nodeDisp, zeroSort, threadCount):
	tIndex = threadCount
	while (len(zeroSort) > 0 and len(threadSolution)<=BEST_LEAVES):
		currentPath = [0]
		#prendi il piu vicino V a zero
		currNode = zeroSort[tIndex][0]
		tIndex = 0
		#creo current_path = [0,V]
		currentPath.append(currNode)
		validated_paths[concat(currentPath)] = costs[currNode][0]
		#rimuovo V dai nodi_disponibili
		nodeDisp.remove(currNode)
		zeroSort.remove((currNode,costs[currNode][0]))


		explore_thread(currentPath,currNode,0, threadSolution, nodeDisp, zeroSort)


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
		path_danger = path_danger + danger[my_path[i]][my_path[i+1]]

	return path_danger


### METODI NUOVI ###

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

def explore_thread(prec_path,my_node,index, threadSolution, nodeDisp, zeroSort):
	if(not is_reachable_by[my_node]):
		threadSolution.append(prec_path)
		return prec_path
	
	check_node = is_reachable_by[my_node][index][0]
	if check_node in nodeDisp:
		prec_node = check_node

	else: 
		index+=1
		if(index<len(is_reachable_by[my_node])):
			return explore_thread(prec_path,my_node,index, threadSolution, nodeDisp, zeroSort)
		else:
			threadSolution.append(prec_path)
			return prec_path

	bool_path, prec_path = check_path(prec_path, prec_node)
	if(bool_path):
		nodi_disponibili.remove(prec_node)
		zeroSort.remove((prec_node,costs[prec_node][0]))

		#esplora piu profondo
		return explore_thread(prec_path,prec_node,0, threadSolution, nodeDisp, zeroSort)
	
	else:
		#esplora altro ramo
		index+=1
		if(index<len(is_reachable_by[my_node])):
			return explore_path(prec_path,my_node,index, threadSolution, nodeDisp, zeroSort)
		else:
			threadSolution.append(prec_path)
			return prec_path


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


def print_solution_vertical(solution):
	sol = {};
	for i in range (1,(n+1)):
		sol[i] = 0;

	for path in solution:
		for j in range(0,(len(path)-1)):
			sol[path[j]]=path[j+1]

	for k in range (1,n+1):
		print k," ",sol[k]


def compute_danger_sol(my_sol):
	total_danger = 0
	for s_path in my_sol:
		total_danger = total_danger + compute_danger(s_path)

	return total_danger
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

file = 'res/pedibus_10.dat'


############## BODY ##############
n, ALPHA, node, danger, costs = parse_dat_file(file)

BEST_LEAVES = n
BEST_RISK = 9999
BEST_SOL = []


MAX_THREADS = 300
threadLock = threading.Lock()
threads = []

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

	print zero_sorted_paths
	#creo current_path = [0,V]
	current_path.append(current_node)

	validated_paths[concat(current_path)] = costs[current_node][0]
	#rimuovo V dai nodi_disponibili
	nodi_disponibili.remove(current_node)
	zero_sorted_paths.remove((current_node,costs[current_node][0]))


	explore_path(current_path,current_node,0)

BEST_SOL = basic_solution
####################






# for i in range (1, n+1):
# 	for sol in basic_solution:
# 		sol.reverse()

# 	if (len(basic_solution)<BEST_LEAVES):
# 		BEST_SOL = copy.deepcopy(basic_solution)
# 		BEST_LEAVES = len(BEST_SOL)
# 	BEST_RISK = compute_danger_sol(basic_solution)
# 	print "SOL:", BEST_SOL, "LEAVES ", BEST_LEAVES, " Risk: ", BEST_RISK
	
# 	node_after = i
# 	for i in range (1,n+1):
# 		nodi_disponibili.append(i)

# 	basic_solution = []
# 	zero_sorted_paths = sorted(zero_paths.items(), key=operator.itemgetter(1))
# 	while (len(zero_sorted_paths) > 0 and len(basic_solution)<=BEST_LEAVES):
# 		current_path = [0]
# 		#prendi il piu vicino V a zero
# 		current_node = zero_sorted_paths[0][0]
# 		node_after = 0
# 		#creo current_path = [0,V]
# 		current_path.append(current_node)

# 		validated_paths[concat(current_path)] = costs[current_node][0]
# 		#rimuovo V dai nodi_disponibili
# 		nodi_disponibili.remove(current_node)
# 		zero_sorted_paths.remove((current_node,costs[current_node][0]))


# 	explore_path(current_path,current_node,0)




for i in range (1,n+1):
	nodi_disponibili.append(i)

zero_sorted_paths = sorted(zero_paths.items(), key=operator.itemgetter(1))


#per ogni nodo 
print_solution_vertical(basic_solution)

#time
time_final = time.time()-start
print 'TOTAL time:', round(time_final,3), 'seconds.\n\n'




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
