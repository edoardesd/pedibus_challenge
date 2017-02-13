#DIMENSION
param n;

#SETS
# contiene tutti i nodi
set V:= 0..n;
#contiene tutti i nodi eccetto 0
set S:= 1..n;


#PARAMS 
param alpha;
param coordX{V};
param coordY{V};
param d{V,V};


### VARIABLES ###

#x[i,j] = 1 se seleziono l'arco da i a j 
var x{V,V} binary;


#y[i] nodo successivo ad i (verso la root)
var y{V} binary;

#depth[i] profondità del nodo i
var depth{V} integer >= 0;

#matrice delle distanze
var distance{V,V} >= 0;




### OBJECTIVE ###


#minimizza le distanze
minimize distances: sum{ i in V , j in V} x[i,j]*distance[i,j];


### CONSTRAINS ###

#SPANNING TREE
#ogni nodo ha 1 e un solo arco in uscita
subject to nodeConnection{ h in S}:
	(sum{i in V} x[h,i]) = 1;

#il numero totale di archi è n
subject to numberOfEdges: 
	sum{s in S, v in V} x[s,v] = n;

#non ci sono auto anelli
subject to noAutoAnelli {h in V}: 
	x[h,h]=0;

#almeno un arco arriva alla root
subject to ArchiInScuola:
	sum{h in S}x[h,0] >= 1;

#non ci sono cicli
subject to noCicli {h in S,k in S}:
	x[h,k]+x[k,h]<=1;

#END SPANNING TREE




#NEXT NODE

subject to nextNode {h in S}:
	y[h]=sum{k in V} x[h,k]*k;

#END NEXT NODE



/*
subject to L1distance{h in S}:
	L1[h] = (sum {i in V} x[i,h]*L2[i]);

subject to L2distance{h in S}:
	L2[h] = (sum {i in V} x[h,i]*L1[i]) + (sum{ j in V} x[h,j]*distance[h,j]);


subject to PathLenght{h in S}:
	L2[h] <= alpha * distance[h,0];
*/

#END PATH LENGHT



#DISTANCES
subject to distanceValues { h in V, k in V}:
distance[h,k] = sqrt(abs(coordX[h]-coordX[k])^2 + abs(coordY[h]-coordY[k])^2);

#END DISTANCES




/*

*/




/*

subject to noArchiOutScuola {h in V}:
	x[0,h]=0;


/*

subject to almenoUnArcoInScuola:
	sum{h in S} x[h,0]>0;

subject to scuolaNoFoglia:
	z[0]=0;

subject to almenoUnaFoglia:
	sum{h in S} z[h]>=1;

subject to nextNode { h in V diff {0}}:
	y[h]=sum {j in V} x[h,j]*j;

subject to isFoglia { h in V diff {0}}:
	z[h]= 1 - (sum {j in V} x[j,h]);

subject to distanceValues { h in S, k in V}:
distance[h,k] = sqrt(abs(coordX[h]-coordX[k])^2 + abs(coordY[h]-coordY[k])^2);
*/
/*
subject to alphaConstrain {h in S}: 
	;
*/
