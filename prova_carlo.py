import math
import pprint as pp

#variabili
NODES = 11
ALPHA = 1.46
nodes = [(46,31),(34,19),(55,54),(46,16),(57,42),(27,16),(13,40),(2,8),(51,35),(48,51),(43,35)]
root = nodes[0]


#matrice distance
distance = [[0 for x in range(NODES)] for y in range(NODES)]
#clusters
neighbor = [[0 for x in range(NODES)] for y in range(NODES)]
#vettore foglie: "1" se il corrispondente nodo e' una foglia
leaves = [0 for x in range(NODES)]
#vettore coda dei nodi: "1" vuol dire che deve essere preso
queue = [1 for x in range(NODES)]



#calcolo distanza
def node_dist(index_1, index_2):
	sub_x = math.pow((nodes[index_1][0] - nodes[index_2][0]), 2)
	sub_y = math.pow((nodes[index_1][1] - nodes[index_2][1]), 2)
	return math.sqrt(sub_x + sub_y)


#matrice delle distanze
for i in range(0,len(nodes)):
	for j in range(0,len(nodes)):
		distance[i][j] = node_dist(i,j)
#print(distance)

#ritorna la distanza minima di un nodo. Non considero root
def min_dist(node):
	minimum = 99999999999999999999999999999999
	for i in range(1,len(nodes)):
		if (distance[node][i] < minimum) and (i!=node):
			minimum = distance[node][i]
	return minimum
print("mimium di 7 is :" , min_dist(7))


'''
per ogni nodo guardo quali altri nodi rispettano la condizione alpha rispetto a lui:
	"1" se posso prendere quel nodo
	"r" root (confronto inutile)
	"self" se stesso (confronto inutile)
'''
def alpha_condition():
	for i in range(0,len(nodes)):
		for j in range(0,len(nodes)):
			neighbor[i][0] = 'root'

			if ((distance[i][j] + distance[j][0])  < ALPHA*distance[i][0]):
				neighbor[i][j] = 1
			else:
				neighbor[i][j] = 0

			if (i==j):
				neighbor[i][j] = ("self"+str(j))

alpha_condition()
print("clusters:")
print(neighbor)

def not_in_queue(index):
	queue[index] = 0
#numero di foglie iniziale: se la somma di neighbor[i] e' 0, i non puo' essere collegato a niente. E' quindi una foglia
def initial_leaves():
	LEAVES = 0
	for i in range(1,len(neighbor)):
		cont = 0
		for j in range(1,len(neighbor)):
			if neighbor[i][j]==1:
				cont = cont + 1
		if cont == 0:
			#aumento contatore foglie LEAVES
			LEAVES = LEAVES + 1
			#setto valore queue a 0. Non lo devo piu' prendere
			not_in_queue(i)
			#setto valore leaves a 1. E' una foglia
			leaves[i] = 1
			
	print("STARTING: we have "+str(LEAVES)+" leaves")		


initial_leaves()
#sono vettori di 11 elementi. In futuro il primo non va considerato in quanto root. Quindi non ci interessa ai fini di LEAVES e QUEUE
print("leaves vector:")
print(leaves)
print("nodes in queue:")
print(queue)


