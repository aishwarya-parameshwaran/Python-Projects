import getopt,sys
import heapq
from collections import deque
graph = {}
weightedGraph = {}
neighbors = []
	
def createGraph(nodes):
	graph.clear()
	for i in range(len(nodes)):
		graph[nodes[i]] = []
	#print graph
	
def addNeighbor(source,destination):
	graph[source].append(destination)
	#print graph

def addNeighborWeighted(source, destination, weight, offtimes):
	temp = []
	temp.append(weight)
	temp.append(destination)
	temp.append(offtimes)
	graph[source].append(temp)

def getNeighbors(source):
	neighbors = graph[source]
	return neighbors
#a = ['A','B','C']
#createGraph(a)
#addNeighbor('A','B')
#getNeighbors('A')

def evaluateAlgorithm(rawInput):
	if rawInput[0] == 'BFS':
		algorithm = 1
	elif rawInput[0] == 'DFS':
		algorithm = 2
	elif rawInput[0] == 'UCS':
		algorithm = 3
	return algorithm
	
def seperateCases():
	filename = sys.argv[2]
	file = open(filename,'r')
	filestr = file.read()
	cases = int(filestr[0])
	filelist = filestr.rsplit('\n\n')
	filelist[0] = filelist[0][2:]
	i = 1
#	print filelist
	while i < len(filelist):
#		print filelist[i][0]
		if filelist[i][0].isdigit():
			
			filelist[i-1:i+1] = ['\n'.join(filelist[i-1:i+1])]
		i = i+1
	#print filelist
	return filelist



	
def seperateParts(inputString):
	inputList = inputString.rsplit('\n')
	return inputList


def getNodes(inputList):
	nodes = []	
	source = inputList[1]
	destination = inputList[2].split(' ')
	midNodes = inputList[3].split(' ')
	nodes.append(source)
	for i in range(len(destination)):
		nodes.append(destination[i])
	for i in range(len(midNodes)):
		nodes.append(midNodes[i])
	return nodes
	
def setPath(inputList):
	paths = 0
	index = 0
	for i in range(len(inputList)):
		if inputList[i].isdigit():
			index = i
			paths = int(inputList[i])
			break
	#print paths
		
	for i in range(paths):
		input = inputList[index+i+1].split(' ')
		source = input[0]
		dest = input[1]
		addNeighbor(source,dest)
		
def setPathWithCost(inputList):
	
	paths = 0
	index = 0
	for i in range(len(inputList)):
		if inputList[i].isdigit():
			index = i
			paths = int(inputList[i])
			break
#	print paths
		
	for i in range(paths):
		input = inputList[index+i+1].split(' ')
		source = input[0]
		dest = input[1]
		cost = input[2]
		offtimecount = int(input[3])
		length = 4 + offtimecount
		offtimes = input[4:length]
#		print source
		addNeighborWeighted(source,dest,cost,offtimes)
		

			
queue = deque()		
parent = deque()
explored = []


def BFS(source,destination,startTime):
	temp1 = []
	temp = []
	queue.clear()
	temp.append(source)
	queue.append(temp)
	current = []
	explored = []
	destination.sort()
	while True:
		if len(queue) == 0:
			return 'None'
		current = queue.popleft()
		temp1 = list(current)
	#	print current
		currentNode = current[-1]
	#	print currentNode
		explored.append(current)
	#	print explored
		currentNeighbors = getNeighbors(currentNode)
		if len(currentNeighbors) == 0:
			continue
	#	print currentNeighbors
		currentNeighbors.sort()
		for i in range(len(destination)):
				if destination[i] in currentNeighbors:
					temp = current
					temp.append(destination[i])
					explored.append(temp)
					pathcost = len(explored[-1])
					result = destination[i] + ' ' + str((pathcost + int(startTime) - 1)%24)
				#	print explored
					return result
		
		currentNeighbors.sort()
		length = len(currentNeighbors)
		
		for i in currentNeighbors:
			for j in range(len(explored)):
				if i == explored[j][-1]:
					if i in currentNeighbors:
						currentNeighbors.remove(i)
				
		for i in currentNeighbors:
			for j in queue:
				if i == j[-1]:
					print i
					if i in currentNeighbors:
						currentNeighbors.remove(i)
		if len(currentNeighbors) == 0:
			continue
		
		currentNeighbors.sort()
		length = len(currentNeighbors)
		for i in range(length):
			temp1 = list(current)
			temp1.append(currentNeighbors[i])
			queue.append(temp1)
			print queue
			
def DFS(source,destination,startTime):
	temp1 = []
	temp = []
	queue.clear()
	temp.append(source)
	queue.append(temp)
	current = []
	explored = []
	while True:
		if len(queue) == 0:
			return 'None'
		current = queue.popleft()
		temp1 = list(current)
	#	print current
		currentNode = current[-1]
	#	print currentNode
		if currentNode in explored:
			continue
			
		if currentNode in destination:
			result = currentNode + ' ' + str((len(current) + int(startTime) - 1)%24)
			return result
	#	print currentNode
		explored.append(currentNode)
	#	print explored
		currentNeighbors = getNeighbors(currentNode)
	#	print currentNeighbors
		if len(currentNeighbors) == 0:
			continue
	#	print currentNeighbors
	#	for i in range(len(destination)):
	#			if destination[i] in currentNeighbors:
	#				temp = current
	#				temp.append(destination[i])
	#				explored.append(temp)
	#				pathcost = len(explored[-1])
	#				result = destination[i] + ' ' + str(pathcost + int(startTime) - 1)
		#			print explored
	#				return result
		for i in currentNeighbors:
			for j in queue:
				if i == j[-1]:
			#		print 'In'
					if i in currentNeighbors:
						currentNeighbors.remove(i)
	#	print explored			
		
		for i in currentNeighbors:
			if i in explored:
		#		print 'In here'
				
				currentNeighbors.remove(i)
		if len(currentNeighbors) == 0:
			continue
		
		currentNeighbors.sort()
		length = len(currentNeighbors)
		for i in range(length):
			temp1 = list(current)
			temp1.append(currentNeighbors[-1-i])
			queue.appendleft(temp1)
		#	print queue			
		
			
		
def UCS(source, destination, startTime):
	queue = deque()	
	queue.clear()
	unsorted = deque()
	explored = []
	current = []
	offtime = []
	temp = []
	start = int(startTime)
	temp.append(start)
	index = 0
	temp.append(index)
	temp.append([source])
	queue.append(temp)
	index = 0
	while True:
	#	print open
		if len(queue) == 0:
			return 'None'
		
		current = queue.popleft()
	#	print current
		currentNode = current[2][-1]
					
	#	print currentNode
		explored.append(currentNode)
	#	for i in range(len(current[2])):
	#		offtime[i] = current[2][i].split('-')
	#	print offtime	
		if currentNode in destination:
			result = currentNode + ' ' + str(current[0]%24)
			return result
			
		currentNeighbors = graph[currentNode]
	#	print currentNeighbors
		
		for i in range(len(currentNeighbors)):
			offtime = []
			for j in range(len(currentNeighbors[i][2])):
				offtime.append(currentNeighbors[i][2][j].split('-'))
			temp = []
			temp1 = list(current[2])
			cost = current[0] 
			starttime = int(cost%24)
		#	print starttime
			cost = current[0] + int(currentNeighbors[i][0])
		#	print cost
			if currentNeighbors[i][1] in explored:
				continue
			frontierCheck = ''
			checkIf = 0
			
		#	print 'Time'+str(time)
		#	print offtime
			
	#		if(len(offtime) == 0):
	#			flag = 0
	#		else:	
			flag = 0
			for j in range(len(offtime)):
				
		#		print offtime[j]
				upperbound = int(offtime[j][1])
				lowerbound = int(offtime[j][0])
				if starttime >= lowerbound and starttime <= upperbound:
					flag = 1
				#	print 'Inrange'
					break
				else:
				#	print 'In range'
					flag = 0
					continue
		#	print flag
			if flag == 1:
				continue
			elif flag == 0:
				for check in range(len(queue)):
					frontierCheck = queue[check][2][-1]
				#	print frontierCheck
					if currentNeighbors[i][1] == frontierCheck:
						if cost < queue[check][0]:
							del queue[check]
							temp.append(cost)
							index = index + 1
							temp.append(index)
							temp1.append(currentNeighbors[i][1])
							temp.append(temp1)
							queue.append(temp)
							unsorted = sorted(queue)
							queue = deque(unsorted)
							checkIf = 1
						#	print queue
							break
						elif cost >= queue[check][0]:
							checkIf = 1
							break
			temp2 = []
			test = 0
		#	print 'Check'
		#	print checkIf
			if checkIf == 1:
				continue
			else:
				for x in range(len(queue)):
					if cost == queue[x][0] and queue[x][2][-1] > currentNeighbors[i][1]:
					#	print 'Same cost'
						temp2 = queue[x]
						queue.remove(temp2)
					#	print queue
						temp.append(cost)
						index = index + 1
						temp.append(index)
						temp1.append(currentNeighbors[i][1])
						temp.append(temp1)
						queue.append(temp)
					#	print queue
						index = index + 1
						temp2[1] = index
						queue.append(temp2)
						unsorted = sorted(queue)
						queue = deque(unsorted)
						test = 1
						break
						
				if test == 0:
					
					temp.append(cost)
					index = index + 1
					temp.append(index)
					temp1.append(currentNeighbors[i][1])
					temp.append(temp1)
					queue.append(temp)
					unsorted = sorted(queue)
					queue = deque(unsorted)
						
				
		#	print queue	
		
		
		
def main():
		file = open('output.txt','w')
		
		
		testcases = seperateCases()
		for i in range(len(testcases)):
			algorithm = 0
			testParts = seperateParts(testcases[i])
			testParts = filter(None, testParts)
		#	print testParts
			nodes = getNodes(testParts)
			createGraph(nodes)
			algorithm = evaluateAlgorithm(testParts)
			if algorithm == 1:
				#testParts.remove()
				setPath(testParts)
				source = testParts[1]
				destination = testParts[2].split(' ')
			#	print testParts
				startTime = testParts[len(testParts)-1]
				for j in range(len(destination)):
					if source == destination[j]:
						result = 'Source and destination same. Invalid test case.'
						break
				else:
					result = BFS(source, destination, startTime)
				file.write(result+'\n')
				
			elif algorithm == 2:
				setPath(testParts)
				source = testParts[1]
				destination = testParts[2].split(' ')
			#	print testParts
				startTime = testParts[len(testParts)-1]
				for j in range(len(destination)):
					if source == destination[j]:
						result = 'Source and destination same. Invalid test case.'
						break
				else:
					result = DFS(source, destination, startTime)
				file.write(result+'\n')
			
			elif algorithm == 3:
				setPathWithCost(testParts)
				source = testParts[1]
				destination = testParts[2].split(' ')
			#	print testParts
				startTime = testParts[len(testParts)-1]
				if source in destination:
					result = 'Source and destination same. Invalid test case.'
					break
				else:
					result = UCS(source, destination, startTime)
				file.write(result+'\n')	
				
				
main()
	
		
