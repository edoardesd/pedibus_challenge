import threading

class myThread(threading.Thread):
	def __init__(self, threadID):
		threading.Thread.__init__(self)
		self.threadID = threadID
	

	def run(self):

		threadLock.acquire()
		print "AUGURI dal thread", self.threadID
		threadLock.release()


threadLock = threading.Lock()

i=0
for i in range (0,25):
	myThread(i).start()