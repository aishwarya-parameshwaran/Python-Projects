import getopt,sys
mancala = []
def createMancala(input):
	#print input
	pits = len(input[3])
	#print pits
	mancala_new = [[],[]]
	mancala_new[0] = input[4]
	mancala_new[0].append(input[6])
	mancala_new[1] = input[3]
	mancala_new[1].append(input[5])
	return mancala_new
	
def readInput():
	filename = sys.argv[2]
	file = open(filename,'r')
	filestr = file.read()
	filelist = filestr.rsplit('\n')
	#print filelist
	if '' in filelist:
		filelist.remove('')
	state_2 = filelist[3].split(' ')
	#print state_2
	state_1 = filelist[4].split(' ')
	#print state_1
	filelist.pop(3)
	filelist.pop(3)
	#print filelist
	filelist = map(int, filelist)
	state_2 = map(int, state_2)
	
	state_1 = map(int, state_1)
	
	filelist.insert(3,state_2)
	filelist.insert(4,state_1)
	return filelist

import sys
import time
start_time = time.time()
def nextMove_1(mancala_new,i):
	##print 'Mancala'
	##print mancala_new
	repeat = 0
	pits = len(mancala_new[0])
	temp = list(mancala_new[0][:])
	temp[len(temp):] = list(mancala_new[1][pits-2::-1])
	
	#print 'Temp'
	#print temp
 	current_stones = temp[i]
	count = current_stones
	temp[i] = 0
	k = i
	##print temp
	while k < len(temp)-1 and count != 0:
		k = k + 1
		temp[k] = temp[k]+1
		count = count - 1
	##print count	
	if count == 0:
		if k == pits-1:
			repeat = 1
		else:
			repeat = 0
			opposite = len(temp) - k - 1
			#print opposite
			if k < pits-1 and temp[k] == 1:
				#print temp[opposite]
				add = temp[k] + temp[opposite]
				temp[k] = 0
				temp[opposite] = 0
				temp[pits - 1] = temp[pits - 1] + add
	else:			
		add = count/len(temp)
	#	#print add
		balance = count%len(temp)
	#	#print balance
		if add != 0:
			temp = map(lambda x:x+add, temp)
		if balance != 0:
			for current_key in range(balance):
				temp[current_key] = temp[current_key] + 1
		#	#print temp
			if balance == pits:
				repeat = 1
			else:
				repeat = 0
				if balance < pits and temp[balance-1] == 1:
					opposite = len(temp) - balance
					add = temp[balance-1] + temp[opposite]
					temp[balance-1] = 0
					temp[opposite] = 0
					temp[pits - 1] = temp[pits-1] + add
	m1 = list(mancala_new[0])
	m2 = list(mancala_new[1])
	if all(current_key == 0 for current_key in temp[0:pits-1]) or all(current_key == 0 for current_key in temp[:pits-1:-1]):
		temp[pits-1] = temp[pits-1] + sum(temp[0:pits-1])
		
		m2[-1] = m2[-1] + sum(temp[:pits-1:-1])
		temp[0:pits-1] = [0] * ((pits-1)-0)
		temp[:pits-1:-1] = [0] * ((len(temp))-pits)
		repeat = 0
	#print 'Temp'
	#print temp
	new_mancala = [[],[]]		
	eval = temp[pits-1] - m2[-1]
	new_mancala[0] = list(temp[0:pits])
	new_mancala[1] = list(temp[:pits-1:-1])
	new_mancala[1].append(m2[-1])
	#print new_mancala
	result = [eval,i,repeat,new_mancala]
	return result
	
def nextMove_2(mancala_new,i):
	#print 'Mancala'
	#print mancala_new
	repeat = 0
	pits = len(mancala_new[0])
	#print pits
	temp = []
	temp[0:pits-1] = list(mancala_new[1][pits-2::-1])
	temp.append(mancala_new[1][pits-1])
	temp[len(temp):] = list(mancala_new[0][:])
	del temp[-1]
	#print 'Temp'
	#print temp
 	
	k = pits - i - 2
	current_stones = temp[k]
	count = current_stones
	temp[k] = 0
	#print k
	#print temp
	while k < len(temp)-1 and count != 0:
		k = k + 1
		temp[k] = temp[k]+1
		count = count - 1
	#print count	
	if count == 0:
		if k == pits-1:
			repeat = 1
		else:
			repeat = 0
			if k < pits-1 and temp[k] == 1:
				opposite = -(k+1)
				add = temp[k] + temp[opposite]
				temp[k] = 0
				temp[opposite] = 0
				temp[pits - 1] = temp[pits - 1] + add
	else:			
		add = count/len(temp)
	#	print add
		balance = count%len(temp)
	#	print balance
		if add != 0:
			temp = map(lambda x:x+add, temp)
		if balance != 0:
			for current_key in range(balance):
				temp[current_key] = temp[current_key] + 1
		#	print temp
			if balance == pits:
				repeat = 1
			else:
				repeat = 0
				opposite = -(balance)
				if balance < pits and temp[balance-1] == 1:
					add = temp[balance-1] + temp[opposite]
					temp[balance-1] = 0
					temp[opposite] = 0
					temp[pits - 1] = temp[pits-1] + add
	m1 = list(mancala_new[0])
	
	if all(current_key == 0 for current_key in temp[0:pits-1]) or all(current_key == 0 for current_key in temp[:pits-1:-1]):
		temp[pits-1] = temp[pits-1] + sum(temp[0:pits-1])
		m1[-1] = m1[-1] + sum(temp[:pits-1:-1])
		temp[0:pits-1] = [0] * ((pits-1)-0)
		temp[:pits-1:-1] = [0] * ((len(temp))-pits)
		repeat = 0
		
	new_mancala = [[],[]]		
	#print mancala_new[0][-1]
	#print temp[pits-1]
	#print temp
	eval = m1[-1] - temp[pits-1] 
	new_mancala[1] = temp[pits-2::-1]
	new_mancala[1].append(temp[pits-1])
	new_mancala[0] = temp[pits:]
	new_mancala[0].append(m1[-1])
	#print new_mancala
	result = [eval,i,repeat,new_mancala]
	return result
graph = []	
from collections import deque

def path_to_leaf(state):
	if state[1][0] == 2:
		temp = [state]
		currentst = deque()
		currentst.appendleft(temp)
		result = []
		d = 0
		while True:
			c = []
			#print currentst
		#	if all(i == 0 for i in currentst[0][-1][5][0:-1]) and all(i == 0 for i in currentst[0][-1][5][0:-1]):
		#		result.append(currentst.popleft())
		#		continue
			temp = currentst.popleft()
			tempsort = []	
			#print temp
			if temp[-1][3] == 1:
				for i in range(len(temp[-1][5][0])-1):
					if temp[-1][5][0][i]!=0:
						t = list(temp)
						next = list(nextMove_1(t[-1][5],i))
						depth = state[2]+1
						
						
						if next[2] == 0:
							minimax = 'MIN'
							eval = sys.maxint
						else:
							minimax = 'MAX'
							eval = -sys.maxint
						c = [eval,[1,i],depth,next[2]]	
						c.append(minimax)
						c.append(next[3])
						tempsort.append(c)
				tempsort.reverse()		
				for i in tempsort:
					n = list(temp)
					n.append(i)
					currentst.appendleft(n)	
				count = 0
				for j in range(len(currentst)):
					if currentst[j][-1][3] == 0:
						count = count + 1
					else:
						break
				
				if count!=0:
					for cnt in range(count):
						result.append(currentst.popleft())
				
			if len(currentst) == 0:
				return result
	
	if state[1][0] == 1:
		temp = [state]
		currentst = deque()
		currentst.appendleft(temp)
		result = []
		d = 0
		while True:
			c = []
			#print 'Curr'
			#print currentst
			temp = currentst.popleft()
			tempsort = []	
			#print temp
			if temp[-1][3] == 1:
				for i in range(len(temp[-1][5][0])-1):
					if temp[-1][5][1][i]!=0:
						next = nextMove_2(temp[-1][5],i)
						depth = state[2]+1
						if next[2] == 0:
							minimax = 'MAX'
							eval = -(sys.maxint)
						else:
							minimax = 'MIN'
							eval = sys.maxint
						
						c = [eval,[2,i],depth,next[2]]
						
						c.append(minimax)
						c.append(next[3])
						tempsort.append(c)
				tempsort.reverse()		
				for i in tempsort:
					n = list(temp)
					n.append(i)
					currentst.appendleft(n)	
				count = 0
				for j in range(len(currentst)):
					if currentst[j][-1][3] == 0:
						count = count + 1
					else:
						break
				
				if count!=0:
					for cnt in range(count):
						result.append(currentst.popleft())
				
			if len(currentst) == 0:
				return result
def get_tree(root, depth):
	current = [[root]]
	result = []
	d = 0
	res = []
	while len(current)!=0:
		for i in range(len(current)):
			#print current
			new = current.pop(0)
			if all(i == 0 for i in new[-1][5][0][0:-1]) and all(i == 0 for i in new[-1][5][1][0:-1]):
				
				res.append(new)
				continue
			elif new[-1][3] == 0 and new[-1][2] == depth:
				
				res.append(new)
				continue
			state = new[-1]
			
			state[3] = 1
			
			result = path_to_leaf(state)
			
			for j in range(len(result)):
				
				result[j].remove(result[j][0])
				t = list(new)
				
				for k in range(len(t)):
					result[j].insert(0,t.pop())
			
			result.reverse()
			for j in range(len(result)):
				current.insert(0,result.pop(0))
				
			count = 0
			
			#for j in current:
			#if all(j[-1][3] == 0 for j in current) and (all(j[-1][2] == depth for j in current) or (all(k[-1][5][0][0:-1] == 0 for k in current) and all(k[-1][5][1][0:-1] == 0 for k in current))):
			#		count = count + 1
			#if count == len(current):
				#print current
	for i in res:
		i[-1][0] = i[-1][5][0][-1] - i[-1][5][1][-1]
		
	return res
	
parent = []
def parent_child(tree):
	temptree = list(tree)
	while len(temptree)!=0:
		current = temptree.pop(0)
		temp = []
		for i in range(len(current)-1):
			temp = [current[i],current[i+1]]
			if temp not in parent:
				parent.append(temp)
	return parent			
			
def find_parent(child,tree):
	for i in tree:
		ind = 0
		if child in i:
			ind = i.index(child)
			break
		if ind-1 == 0:
			return None
		else:
			return i[ind-1]
def find_parent1(child):
	ps = []
	for i in parent:
		if i[1] == child:
			ps.append(i[0])
	return ps		
def find_children(p):
	children = []
	for i in parent:
		if i[0] == p:
			children.append(i[1])
	return children


#print 'PC'		
#print parent_children	

def has_more_children(parent1,found):
	i = 0
	while i<len(parent):	
		if parent[i][0] == parent1 and found == parent[i][1]:
			break
		else:
			i=i+1
	j = i+1
	flag = 0
	#print parent
	while j<len(parent):
		if parent[j][0] == parent1:
			flag = 1
			break
		else:
			j = j+1
	if flag == 0:
		return False
	else:
		return True
		
def parent_by_state(state):
	new = []
	for i in parent:
		if i[1][5] == state:
			new.append(i[0])
	return new		
def minimax_tree(tree):
	current_branch = []
	root1 = tree[0][0]
	final_log = []
	marker = root1
	while len(tree)!=0:
		#print 'Tree'
		#print tree[0]
		current_branch = tree.pop(0)
	#	print 'Parent'
	#	print parent
		#print current_branch
		b = current_branch.index(marker)
		
		i = b
		while i<len(current_branch)-1:
			final_log.append(current_branch[i])
			i = i+1
		e1 = current_branch[-1][5][0][-1]
		e2 = current_branch[-1][5][1][-1]
		eval =  e1 - e2	
		current_branch[-1][0] = eval	
		final_log.append(current_branch[-1])
		j = len(current_branch)-2
		#print j
		while j>=0:
			
			
			if tree != [] and current_branch[j] in list(tree[0]):
				#print current_branch[j]
				#print tree[0]
			#if has_more_children(current_branch[j],current_branch[j+1]):
			#	print 'True'
			#	for i in pc:
			#		print i
				marker = list(current_branch[j])
				#print 'Marker'
				#print marker
				break
			else:
				final_log.append(current_branch[j])
				j = j-1
		#print 'Log'
		#print final_log
	return final_log			

def leaf(tree):
	leaf_nodes = []
	for i in range(len(tree)):
		if tree[i][0] != -sys.maxint and tree[i][0] != sys.maxint:
			leaf_nodes.append(tree[i])
	return leaf_nodes
	
def traverse_minimax(minimaxtree):
	result = []
	tree = list(minimaxtree)
	leaf_nodes = leaf(tree)
	i = 0
	p1 = []
	while i<(len(tree)-1):
		#ttt=list(tree)
		tt = list(tree[i])
		#print ttt
	#	print 'tt'	
	#	print tt	
		p1 = find_parent1(tt)
	#	print p1
		if p1 == []:
			result.append(list(tree[i]))
			i = i+1
			continue
			
		p1= list(p1)	
		temp_p = list(p1)	
		if tree[i+1] in p1:
			pp1 = p1.index(tree[i+1])
			if p1[pp1][4] == 'MIN':
				
				tree[i+1][0] = min(tree[i][0],tree[i+1][0])
			else:
				tree[i+1][0] = max(tree[i][0],tree[i+1][0])
			result.append(list(tree[i]))	
			#print 'ti'
			#print tree[i]
			result.append(list(tree[i+1]))	
			j = i+1
			while tree[j] == temp_p and j<len(tree)-1:
				tree[j] = list(tree[i+1])
				j = j+1
			i = i+1
		elif tree[i] in leaf_nodes:
			result.append(list(tree[i]))
			i=i+1
		else:
			result.append(list(tree[i]))
			i=i+1
		
	return result
					

def getstates(root, log, maxval):
	paths = path_to_leaf(root)
	#print paths
	#print maxval
	val = None
	while True:
		current = paths.pop()
		current = current[1:len(current)]
	#	print current
		for j in range(len(current)):
			flag = 0
			i=len(log)-1
	#		print i
	#		print current[j]
			while i>=0:
	#			print log[i]
				if log[i][1]==current[j][1] and log[i][2]==current[j][2] and log[i][4]==current[j][4] and log[i][5]==current[j][5]:
					val = log[i][0]
	#				print val
					break
				else:
					i = i-1
			if val == maxval:
	#			print True
				flag = 1
				
				continue
			else:
				flag = 0
				break
			
		if flag == 1:
			return current[-1]
	
		
			
			
def Greedy():
	graph = []
	input_list = readInput()
	mancala = createMancala(input_list)
	player = input_list[1]
	pits = len(mancala[0])
	#print pits
	
	if player == 1:
		for i in range(len(mancala[0])):
			if mancala[0][i] != 0:
				temp_hold = []
				next_move = nextMove_1(mancala,i)
				#print 'Next'
				#print next_move
				current_index = next_move[1]
				current = next_move
				current[1] = [i]
				if current[2] == 0:
					graph.append(current)
				else:
					temp_hold.append(current)
				#print 'Graph'	
				#print graph	
				while len(temp_hold) != 0:
					for j in range(len(temp_hold)):
						if temp_hold[j][2] == 1:
							current_ele = temp_hold.pop(j)
							#print 'Current'
							#print current_ele
							for k in range(len(mancala[0])-1):
								current = current_ele[3]
								if current[0][k] != 0:
									next_move = nextMove_1(current,k)
									new = next_move[3]
								
									current = next_move
									new_i = current_ele[1]
									new_i.append(k)
									current[1] = new_i
									temp_hold.append(current)
					for l in temp_hold:
						if l[2] == 0:
							graph.append(l)
							temp_hold.remove(l)
							
									
							
			
		
		
				graph.sort()	
	
	if player == 2:
		for i in range(len(mancala[1])):
			if mancala[1][i] != 0:
				temp_hold = []
				#print mancala
				next_move = nextMove_2(mancala,i)
				#print 'Next'
				#print next_move
				current_index = next_move[1]
				current = next_move
				current[1] = [i]
				if current[2] == 0:
					graph.append(current)
				else:
					temp_hold.append(current)
				#print 'Graph'	
				#print graph	
				while len(temp_hold) != 0:
					for j in range(len(temp_hold)):
						if temp_hold[j][2] == 1:
							current_ele = temp_hold.pop(j)
							#print 'Current'
							#print current_ele
							for k in range(len(mancala[1])-1):
								current = current_ele[3]
								if current[1][k] != 0:
									next_move = nextMove_2(current,k)
									new = next_move[3]
								
									current = next_move
									new_i = current_ele[1]
									new_i.append(k)
									current[1] = new_i
									temp_hold.append(current)
					for l in temp_hold:
						if l[2] == 0:
							graph.append(l)
							temp_hold.remove(l)
							
									
							
			
		
		
				graph.sort()		
				
	i = len(graph)-1
		
	maxval = graph[i][0]
	maxlist = []
	for i in graph:
		if i[0] == maxval:
			maxlist.append(i)
	finalval = maxlist[0]
	filename = 'next_state.txt'
	file = open(filename,'w') 
	st2 = map(str,finalval[3][1])
	#print st2
	st22 = ' '.join(st2[0:len(st2)-1])
	#print st22
	st1 = map(str,finalval[3][0])
	#print st1
	st11 = ' '.join(st1[0:len(st1)-1])
	#print st22
	f2 = str(st2[-1])
	f1 = str(st1[-1])
	file.write(st22+'\n')
	file.write(st11+'\n')
	file.write(f2+'\n')
	file.write(f1)
				
		
			

def main():
	inputlist = readInput()
	if inputlist[0] == 1:
		Greedy()
	if inputlist[0] == 2:
		input_list = readInput()
		mancala = createMancala(input_list)
		player = input_list[1]
		depth = input_list[2]
		if player == 1:
			root = [-sys.maxint,[2,0],0,1,'MAX',mancala]
		else:	
			root = [-sys.maxint,[1,0],0,1,'MAX',mancala]
		a = get_tree(root,depth)
		parent_child(a)
		b = minimax_tree(a)
		c = traverse_minimax(b)
		from itertools import groupby
		def remove_dupes(arg):
			l = []
			l = [i for i in groupby(arg)]
			for i in range(len(l)):
				l[i] = l[i][0]
			return l	
		c = remove_dupes(c)
		#print 'c'
		#for i in c:
			#print i
		filename = 'traverse_log.txt'
		file = open(filename,'w')
		file.write('Node,Depth,Value'+'\n')
		for ele in c:
			if ele[5] == root[5]:
				node = 'root'
			else:
				if ele[1][0] == 1:
					node = 'B'
					ind = str(ele[1][1]+2)
					node = node+ind
				if ele[1][0] == 2:
					node = 'A'
					ind = str(ele[1][1]+2)
					node = node+ind
			depth1 = str(ele[2])
			value = ele[0]
			if value == sys.maxint:
				value = 'Infinity'
			elif value == -sys.maxint:
				value = '-Infinity'
			else:
				value = str(value)
			finalstr = node+','+depth1+','+value+'\n'
			file.write(finalstr)
		
		maxval = c[-1][0]
		state = root
		getst = getstates(root,c,maxval)
		#print getst
		st1=map(str,getst[5][0])
		st11 = ' '.join(st1[0:len(st1)-1])
		st2=map(str,getst[5][1])
		st22 = ' '.join(st2[0:len(st2)-1])
		f1 = str(getst[5][0][-1])
		f2 = str(getst[5][1][-1])
		filename = 'next_state.txt'
		file = open(filename,'w')
		file.write(st22+'\n')
		file.write(st11+'\n')
		file.write(f2+'\n')
		file.write(f1)
			
main()	
