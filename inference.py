import sys,re
from itertools import groupby
from operator import itemgetter
from collections import deque
clauses = {}
index = {}
global queue
queue = deque()
visited = deque()
allkeys = []

def substitute(subs,predicate):
    strtemp = predicate.split('(')
    str1 = strtemp[0]+'('
    arg = strtemp[1][0:-1].split(',')
    sub = subs
    for i in range(len(arg)):
        for j in sub:
            if arg[i] == j[0]:
                arg[i] = j[1]
                
    for i in range(len(arg)):
        str1 = str1 + arg[i]+','

    str1 = str1[0:-1]
    str1 = str1 +')'
    return str1

def skolemize(clauses):
    prog1 = re.compile('[a-z]{1}')
    newcl = {}
    clkeys = clauses.keys()
    c = 1
    for i in clkeys:
        ptemp = i.split('(')
        pp = ptemp[0]
        parg = ptemp[1][0:-1].split(',')
        
        child = clauses[i]
        if not any(prog1.match(i) for i in parg) and child == []:
            newcl[i]=[]
            continue
        for j in child:
            sub = []
            ntemp = []
            for k in parg:
                if prog1.match(k):
                    sub.append([k,'a'+str(c)])
                    c=c+1
            newparent = substitute(sub,i)
            newcl[newparent]=[]
            for k in j:
                ktemp = k.split('(')
                kp = ktemp[0]
                karg = ktemp[1][0:-1].split(',')
                for l in karg:
                    if l not in parg:
                        if prog1.match(l):
                            sub.append([l,'a'+str(c)])
                            c=c+1
                newk = substitute(sub,k)
                ntemp.append(newk)
            newcl[newparent].append(ntemp)
    return newcl
                
            
def sentenceParser(sentence):
    clauses_ops = sentence.rsplit(" ")
    if len(clauses_ops) == 1:
        clauses[clauses_ops[0]] = []
    elif '=>' in clauses_ops:
        temp = []
        tempclause = sentence.rsplit(" => ")
        temp_and_left = tempclause[0].rsplit(" ^ ")
        temp_right = tempclause[1]
        if temp_right not in clauses.keys():
            clauses[temp_right] = [temp_and_left]
        else:
            clauses[temp_right].append(temp_and_left)
    global allkeys
    allkeys = clauses.keys()
    
def processInput(filename):
    file = open(filename,'r')
    lines = file.read()
    lines = lines.splitlines()
    count_q = int(lines[0])
    i = 1
    queries = []
    while i <= count_q:
        queries.append(lines[i])
        i = i+1
    kb = []
    count_kb = lines[i]
    i = i+1
    while i< len(lines):
        kb.append(lines[i])
        i = i+1
    input = []
    input.append(kb)
    input.append(queries)
    return input

def indexKeys():
    keys = clauses.keys()
    
    for i in keys:
        temp = i.split('(')
        predicate = temp[0]
        args = temp[1][0:-1].split(',')
        if predicate not in index.keys():
            index[predicate] = [args]
        else:
            index[predicate].append(args)


           
    
def findIndex(predicate):
    temp = predicate.split('(')
    p = temp[0]
#    print 'findind'
 #   print 'p'
  #  print p
    arg = temp[1][0:-1].split(',')
    #print 'arg'
    #print arg
    if p not in index.keys():
        return []
    index_arg = index[p]
  #  print 'indarg'
   # print index_arg
    is_var = []
    prog1 = re.compile('[a-z]{1}[0-9]{1,}')
    prog2 = re.compile('[A-Z]{1}[a-zA-Z]{0,}')
    result = []
                       
    for i in index_arg:
        subs = []
        flag = 0
        for j in range(len(i)):
            if prog1.match(i[j]) and prog1.match(arg[j]):
                if [i[j],arg[j]] in subs:
                    continue
                ret = None
                for k in subs:
                    if k[0] == i[j]:
                        ret = k[1]
                        break
                if ret == None:
                    temp = [i[j],arg[j]]
                    subs.append(temp)
                else:
                    if prog2.match(ret):
                        temp = [arg[j],ret]
                        subs.append(temp)
                 
                
            elif prog1.match(i[j]) and prog2.match(arg[j]):
                if [i[j],arg[j]] in subs:
                    continue
                
                temp = [i[j],arg[j]]
                subs.append(temp)
            elif prog2.match(i[j]) and prog1.match(arg[j]):
                
                temp=[arg[j],i[j]]
                subs.append(temp)
            elif prog2.match(i[j]) and prog2.match(arg[j]) and i[j] == arg[j]:
                temp = [i[j],i[j]]
                subs.append(temp)
            else:
                flag = 1
        tsub = []
        for k in subs:
            for l in subs:
                if k!=l:
                    if k[0]==l[0]:
                        if prog2.match(k[1]) and prog2.match(l[1]) and k[1]!=l[1]:
                            flag = 1
                        if prog1.match(k[1]) and prog2.match(l[1]):
                            temp = [k[1],l[1]]
                            tsub.append(temp)
                            
                        if prog2.match(k[1]) and prog1.match(l[1]):
                            temp = [l[1],k[1]]
                            tsub.append(temp)
                            
                    elif k[1]==l[0] and prog2.match(l[1]):
                        temp = [k[0],l[1]]
                        tsub.append(temp)
                        
                    elif k[0]==l[1] and prog2.match(k[1]):
                        temp = [l[0],k[1]]
                        tsub.append(temp)
        for ele in tsub:
            subs.append(ele)
        
        if flag == 1:
            continue
        else:
            temp_subs = [p]
            temp_subs.append(i)
            temp_subs.append(arg)
            temp_subs.append(subs)
            result.append(temp_subs)
        
  #  print 'index'
  #  print result
    return result
                
def findliteral(s):
    str1 = s[0]+'('
    for i in range(len(s[1])):
        str1 = str1 + s[1][i] + ','
    str1 = str1[0:-1]
    str1 = str1+')'
    return str1
        

        
def addToQueue(pred):
    d = findIndex(pred)
    flag = []
    for j in range(len(d)):
        newlit = findliteral(d[j])
 #       print 'Lit'
  #      print newlit
   #     print d[j]
        
        count = len(clauses[newlit])
        newsub = substitute(d[j][3],newlit)
        if newlit not in allkeys:
            queue.appendleft([[newsub,newlit,d[j][3]]])
            flag.append(None)
    #    print 'Newsub'
     #   print newsub
        
        if count>0:
            
            queue.appendleft([[newsub,newlit,d[j][3]]])
            flag.append(True)
        if count == 0:
            queue.appendleft([[newsub,newlit,d[j][3]]])
            flag.append(False)
      #  print queue
    return flag

def checkPresent(pred):
    d = findIndex(pred)
    flag = []
    for j in range(len(d)):
        newlit = findliteral(d[j])
      #  print 'Lit'
       # print newlit
        #print d[j]
        
        count = len(clauses[newlit])
        if newlit not in allkeys:
            flag.append(None)
        elif count > 0:
            flag.append(True)
        elif count == 0 :
            flag.append(False)
    return flag

def getNext1(pred):
    if pred[1] not in allkeys:
        return []
    found = clauses[pred[1]]
  #  print found
    finaltemp=[]
    for i in found:
        for j in range(len(i)):
        #    print i[j]
         #   print pred[2]
            newsub = substitute(pred[2],i[j])
            templist = [newsub,i[j],pred[2]]
            if templist in visited:
                break
            else:
                finaltemp.append(templist)
   # print 'Final'
    #print finaltemp
    return finaltemp

def getNext2(pred):
    print 'pred'
    print pred
    finaltemp=[]
    if pred[1] not in allkeys:
        t1 = findIndex(pred[0])
        print 't1'
        print t1
        if len(t1) == 0:
            return []
        else:
            for i in t1:
                lit = findliteral([i[0],i[1]])
                templist = [lit,pred[0],i[3]]
                finaltemp.append(templist)
            return finaltemp
    found = clauses[pred[1]]
    print 'found'
    print found
    
    for i in found:
        for j in i:
            newsub = substitute(pred[2],j)
          #  print 'newsub'
           # print newsub
            newtemp = [newsub,j,pred[2]]
  #          print allkeys
            if j not in allkeys:
                
                t2 = findIndex(newsub)
                print 't2'
                print t2
                if len(t2) == 0:
                    finaltemp.append([])
                    continue
                else:
                    for k in t2:
                        lit = findliteral([k[0],k[1]])
                        templist = [lit,j,k[3]]
                        finaltemp.append(templist)
                    continue    
        for j in range(len(i)):
    #        print i[j]
    #        print pred[2]
            newsub = substitute(pred[2],i[j])
            templist = [newsub,i[j],pred[2]]
            finaltemp.append(templist)
    #print 'Final'
    #print finaltemp
    return finaltemp
def getNext3(pred):
   # print 'pred'
    #print pred
    prog1 = re.compile('[a-z]{1}')
    finaltemp = []
    templist = []
    if pred[1] not in allkeys:
        print pred[0]
        t1 = findIndex(pred[0])
        print 't1'
        print t1
        if len(t1) == 0:
            return []
        else:
            for i in t1:
                
                if any(prog1.match(x) for x in i[2]):
                    
                    lit = findliteral([i[0],i[1]])
                    
                   
                    
                    found = clauses[lit]
                    if found == []:
                        
                        templist = [[lit,pred[0],i[3]]]
                       
                        finaltemp.append(templist)
                        continue
                    
                    for j in found:
                        templist = []
                        for k in j:
                            newsub = substitute(i[3],k)
            #                print newsub
                            templist.append([newsub,k,i[3]])
             #               print 'tmp'
              #              print templist
                        finaltemp.append(templist)
                        
                else:
                    lit = findliteral([i[0],i[2]])
                    org = findliteral([i[0],i[1]])
                    
                    templist = [[lit,pred[1],i[3]]]
                    finaltemp.append(templist)
            print 'Final'
            print finaltemp
            return finaltemp
    else:
        found = clauses[pred[1]]
        print 'found'
        print found
        for i in found:
            templist = []
            for j in i:
                newsub = substitute(pred[2],j)
        #        print newsub
                templist.append([newsub,j,pred[2]])
         #       print templist
            finaltemp.append(templist)
            print 'ft'
            print finaltemp
    return finaltemp

def getNext(pred):
   # print 'pred'
    #print pred
    prog1 = re.compile('[a-z]{1}[0-9]{1,}')
    finaltemp = []
    templist = []
    if pred[1] not in allkeys:
      #  print pred[1]
        t1 = findIndex(pred[0])
    #    print 't1'
     #   print t1
        if len(t1) == 0:
            return []
        else:
            for i in t1:
                
                if any(prog1.match(x) for x in i[2]):
         #           print'i'
        #            print i
                    lit = findliteral([i[0],i[1]])
                    
                 #   print 'lt'
                  #  print lit
                   # print lit
                    found = clauses[lit]
                   # print 'fnd'
                    #print found
                    if found == []:
                        templist = [[lit,pred[0],i[3]]]
                     #   print 'tmp'
                      #  print templist
                        finaltemp.append(templist)
                        continue
                    
                    for j in found:
                        templist = []
                        for k in j:
                            newsub = substitute(i[3],k)
                       #     print'nsub'
                        #    print newsub
                            templist.append([newsub,k,i[3]])
                         #   print 'tmp1'
                          #  print templist
                        finaltemp.append(templist)
                        
                else:
                    lit = findliteral([i[0],i[2]])
                    org = findliteral([i[0],i[1]])
                    #print 'lit'
                    #print lit
                    templist = [[lit,org,i[3]]]
                    finaltemp.append(templist)
          #  print 'Final'
           # print finaltemp
            return finaltemp
    else:
        found = clauses[pred[1]]
       # print 'found'
       # print found
        for i in found:
            templist = []
            for j in i:
                newsub = substitute(pred[2],j)
         #       print 'ns'
          #      print newsub
                templist.append([newsub,j,pred[2]])
           #     print templist
            finaltemp.append(templist)
            #print finaltemp
    return finaltemp

def checkFact(list):
    #print list[0]
    if list[0] not in allkeys:
        return False
    if clauses[list[0]] == []:
        return True
    else:
        return False
    
def addVisited(list1):
    visited.appendleft(list1)

def checkLastVisited():
    for i in range(len(queue)):
        if queue[i] not in visited:
            queue.popleft()
        else:
            break

def checkNotVisited():
    count = 0
    for i in queue:
        if i in visited:
            count = count+1
        else:
            for j in range(count):
                queue.popleft()
            break

def remove_dupes(arg):
    l = []
    l = [i for i in groupby(arg)]
    for i in range(len(l)):
        l[i] = l[i][0]
    return l
def eliminate(true):
    
    for i in range(len(queue)):
        
        
        if queue[i] == true:
            continue
        elif queue[i]!=true:
            
            
            j = len(queue[i])-1
            while j>=0:
                subs = substitute(true[-1][2],queue[i][j][0])
                if subs!=queue[i][j][0]:
                #    print 'org'
                 #   print queue[i][j][0]
                  #  print 'sub'
                   # print subs
                    tq = list(queue[i][j][2])
                    tt1 = list(true[-1][2])
                    for ele in tt1:
                        tq.append(ele)
                    temp = [subs,queue[i][j][0],list(tq)]
                   # print temp
                    queue[i] = queue[i][0:j+1]
                    queue[i].append(temp)
                    #print queue
                    break
                elif subs==queue[i][j][0]:
                    j=j-1
                    continue
         
                
def duplicates(a):
    kt = [tuple(i) for i in a]
    skt = set(kt)
    res = map(list,skt)
    return res

def isPresent(list):
    for i in list:
        if i[1] not in allkeys:
            return False
    return True
def check_dupes(arg):
    l = []
    l = [i for i in groupby(arg,itemgetter(0))]
    
    for i in range(len(l)):
        l[i] = l[i][0]
   # print l
    for i in l:
        if l.count(i)>1:
            return True
    return False

def backchain(query):
    addToQueue(query)
    true = []
    fail = []
    global pc
    pc = {}
    global queue
 #   print 'q'
  #  print queue
    while len(queue)!=0:
        temp = []
       # print 'q'
        #for i in queue:
         #   print i
          #  print '\n'
        for i in queue:
            current = i[-1]
         #   print 'curr'
          #  print current
            if checkFact(current):
                true.append(i)
                #if current == ['Father(Shawn,John)', 'Father(x,John)', [['x', 'Shawn'], ['John', 'John']]]:
                   # print 'queue'
                   # print queue
                
                    
                tt = list(i)
                eliminate(i)
                queue = remove_dupes(queue)
           #     print 'eliminate'
            #    print i
                  #  print 'Q'
                   # for k in queue:
                    #    print k
                     #   print '\n'
                    
                
                continue
            flag = 0

            if current in i[0:-1]:
                fail.append(i)
                continue
            if check_dupes(list(i)):
                #print 'I'
                #print i
                fail.append(i)
                continue
            next = getNext(current)
          #  print 'next'
           # print next
            if next == []:
                fail.append(i)
                continue
            if current[0] in pc.keys():
                
                pc[current[0]].extend(list(next))
            elif current[0] not in pc.keys():
                pc[current[0]] = list(next)
            
            for j in next:
                for k in j:
                
                    temp_i = list(i)
                    temp_i.append(k)
                    temp.append(temp_i)
        queue = deque(temp)
    return [true,fail]

                    
                
def backtrack1(query,true):
    global cmp1
    cmp1 = {}
    for i in true:
        for j in range(len(i)-1):
            parent = i[j]
            child = i[j+1]
         #   print 'pc'
          #  print parent
           # print child
            val = pc[parent[0]]
            print 'val'
            print val
            print child
            temp = []
            final = []
            f1 = []
            for k in val:
                print 'k'
                print k
                if child in k:
                    temp = list(k)
                    break
            print 'temp'
            print temp
            if parent[0] not in cmp1.keys():
                cmp1[parent[0]] = [[child]]
                
            elif parent[0] in cmp1.keys():
                print 'Go dragons'
                print val
                for l in val:
                    print 'ch'
                    print child
                    if child in l:
                       final = l
                       print 'L'
                       print l
                       break
                for k in cmp1[parent[0]]:
                    for l in final:
                        if l in k:
                            f1 = k
                            break
                        else:
                            f1 = [None]
                if f1 == [None]:
                    cmp1[parent[0]].append([child])
                    continue
                for k in cmp1[parent[0]]:
                    if k == f1:
                        k.append(child)
    return cmp1

def backtrack(query,true):
    global cmp1
    cmp1 = {}
    #print 'Tre'
    
    #for i in true:
     #   print i
      #  print '\n'
    for i in true:
        for j in range(len(i)-1):
            parent = i[j]
            child = i[j+1]
           # print 'pc'
            #print parent
           # print child
            
                
            #val = pc[parent[0]]
            #print 'val'
            #print val
            #print child
            temp = []
            final = []
            f1 = []
            
            if parent[0] not in cmp1.keys():
                cmp1[parent[0]] = [child[0]]
                
            elif parent[0] in cmp1.keys() and child not in cmp1[parent[0]]:
                cmp1[parent[0]].append(child[0])
        

def checkPresent(ele,true):
    pr = ele[0]
    #print pr
    if pr not in pc.keys():
       # print 'drag'
        return False
    p1 = pc[pr]
    #print 'p1'
    #print p1
    p1=p1
    p = []
    for i in p1:
     #   print 'I'
      #  print i
        p.append([j[0] for j in i])
    #print 'p'
    #print p
    c1 = cmp1[pr]
    #print 'c1'
    #print c1
   
    for i in p:
     #   print 'i'
      #  print i
        if all(x in c1 for x in i):
           # print True
            return True
    return False

 
def compare(true):
    #print 'compare'
    p_keys = pc.keys()
   # cmp_keys = cmp.keys()
    global n_list
    t=[]
    for c in true:
        t.append(c[-1])
    #print 't'
    #print t
    fail = []
    while True:
        n_list = []
        
        for i in true:
            if any(j in i for j in fail):
                continue
            else:
                for k in i:
                    n_list.append(k)
        
      #  print 'nlist'
       # print remove_dupes(n_list)
        if len(n_list)==0:
            return False
        fail = []
        for i in n_list:
            
           
            if checkPresent(i,t) or i in t:
            #    print 'i'
             #   print i
                continue
            else:
              #  print 'f'
               # print i
                fail.append(i)
                

        if len(fail)==0:
            return True
                
def main():
    result = processInput('input_1.txt')
    kb = result[0]
   # print kb
    q = result[1]
    for i in kb:
        sentenceParser(i)
    global clauses
    #print clauses
    #print '\n'
    clauses = skolemize(clauses)
   # print clauses
    #indexKeys()
    global allkeys
    allkeys = clauses.keys()
    #print allkeys
    indexKeys()
   
    #query = 'H(John)'
    #print checkPresent(query)
  #  visited.append(['H(Bob)','H(x)',[['x','Bob']]])
   # visited.append(['H(Bob)','H(x)',[['x','Bob']]])    
    #temp = getNext(['F(Bob)','F(x)',[['x','Bob']]])
  #  print 'temp'
   # print temp
   # next = getNext([query,'A(x,y)',[['x','Bob'],['y','y']]])
  #  print next
    result = []
    #new = substitute([['q', 'Shawn'], ['John', 'John']],'Mother(q,Sarah)')
    #print 'subsmain'
    #print new
  #  print clauses
   # print '\n'
    #qr = ['Siblings(a30,Amanda)', 'Siblings(a34,a35)', [['a34', 'a30'], ['a35', 'Amanda']]]
    #print 'gn'
    #print getNext(qr)
    #print findIndex(qr[0])
    filename = 'output.txt'
    f = open(filename,'w+')
    for x in q:
        
        true_fail = backchain(x)
    #    print 'tf'
    #    print true_fail
        true = remove_dupes(true_fail[0])
        fail = remove_dupes(true_fail[1])
    #    print 'true1'
     #   for i in true:
      #      print i
       #     print '\n'
       # print 'fail1'
        #for i in fail:
         #   print i
          #  print '\n'
        tru = []
      #  for i in true:
     #       tru.append([j[0] for j in i])
       # print clauses
     #   print 'true final'
      #  print tru
        #print 'pcmain'
       # print pc['Parent(a3,a15)']
        backtrack(x,true)
       # print 'cmp1'
        #print cmp1
   # print checkPresent(['B(John,y)', 'B(x,y)', [['x', 'John']]],true)
  #  print pc
        final = compare(true)
        if final == True:
            f.write('TRUE'+'\n')
        elif final == False:
            f.write('FALSE'+'\n')
        
    
            
    

    
    
    
main()
            
