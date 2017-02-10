import numpy as np
import re
import time
start = time.time()

list_test = []

file_dat = np.genfromtxt('res/pedibus_50.dat', delimiter='\n', dtype=None)

n = int(file_dat[1][11:]) #parse param n: dimension of array

alpha = float(file_dat[3][15:]) #parse param alpha
file_dat = file_dat[5:]
coord_x = []
coord_y = []
raw_x = []
raw_y = []


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


raw_x.pop(0)
raw_x.pop(len(raw_x)-1)
raw_y.pop(0)
raw_y.pop(len(raw_y)-1)

raw_x =' '.join(raw_x)
raw_x = raw_x.split(' ')
raw_y =' '.join(raw_y)
raw_y = raw_y.split(' ')

i=0
coord_x = {}
for column in raw_x:
	if i%2 == 0:
		even = int(column)
	if i%2 != 0:
		coord_x[even] = int(column)

	i = i+1
	
i=0
coord_y = {}
for column in raw_y:
	if i%2 == 0:
		even = int(column)
	if i%2 != 0:
		coord_y[even] = int(column)

	i = i+1
	

print "n: ",n, "\n" "alpha: ", alpha, "\n", "coord x:", coord_x, "coord y:", coord_y


print 'It took', time.time()-start, 'seconds.'