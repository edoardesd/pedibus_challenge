sorted_x = sorted(neighbor[1].items(), key=operator.itemgetter(1)) #ordinare per vicinanza i nodi rispetto al nodo 1 (tra quadre)
candidate_list = sorted_x[0] #candidate list: contiene in 0 il nodo e in 1 la distanza [nodo, distanza]
candidate_node = candidate_list[0]
candidate_dist = candidate_list[1]
print candidate_node, candidate_dist
print neighbor[1][0], "\n"

print tree[1]
new_path_test = [4, 6, 7, 0] 
if check_alpha(new_path_test, candidate_node) == True:
	for i in tree:
		if 1 in tree[i]:
			print candidate_node
			delete_node(candidate_node)
			tree[i].insert(0, candidate_node) #update path: inserisce candidate_node nella posizione 0 (primo della lista)
			print "ok, dovrei updatare path"
else: print "nada"

remove_zero_path(tree)
pp.pprint(tree)