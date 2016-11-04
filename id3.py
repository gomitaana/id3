import fileinput
import sys
import itertools
import re
import math
import collections
#./run < testcases/or.arff.in

class Node(object):
    def __init__(self, name, states):
        self.entropy = 0
        self.gain = 0
        self.name = name
        self.states = states
        self.total_states = {}
        self.combinations = []
        self.results = {}
        self.visited = 0
    
    def initializeStates(self):
        for state in self.states:
            new = {state: 0}
            self.total_states.update(new)

    def updateStates(self,name):
        self.total_states[name] += 1
        
    def updateEntropy(self,size):
        suma = 0
        for item in self.total_states:
            aux = float(self.total_states[item])/size
            if aux !=0:
                suma += -aux * math.log(aux,2)
        self.entropy = suma
  
    def updateCombinations(self, combinations):
        self.combinations = combinations
    
    def updateResults(self, final_states):
        for value in self.states:
            count =[]
            for index, combination in enumerate(self.combinations):
                if(combination == value):
                    count.append(final_states[index])
            self.results.update({value: count})
        
    def infGain(self,total_entropy):
        tx_entropy=0
        for value in self.states:
            probability=float(self.total_states[value])/len(self.combinations)
            inner_entropy=0
            for aux_value in self.states:
                count = 0
                for result in self.results[value]:
                    if(aux_value == result):
                        count+=1
                aux = float(count)/len(self.results[value])
                if aux!= 0:
                    inner_entropy-=aux*math.log(aux, 2)
            tx_entropy += probability*inner_entropy
        #print("mi entropia: ")
        self.gain = total_entropy - tx_entropy
        #print (self.gain)
    
    def setVisited(self):
        self.visited = 1
   
if __name__ == '__main__':
    input   = []
    nodes   = []
    queries = []
    relation= []
    data_main = []

    # Read each input line
    for line in sys.stdin:
        if line[0] != "%":
            line = line.strip("\n")
            if line != "":
                input.append(line)

    for idx, line in enumerate(input):
        #Read relation
        if line.startswith("@relation"):
            relation = line.split(" ");

        #Read attributes
        if line.startswith("@attribute"):
            attribute = line.split(" ");
            name = attribute[1]
            values = re.search("{(.+?)}", line).group(1)
            f_values = values.split(", ") # attribute values
            node = Node(name, f_values) #creo el nodo
            node.initializeStates()
            nodes.append(node)
            
        if line.startswith("@data"):
            data_list = list(input)
            for data in itertools.islice(data_list, idx+1, None):
                data_set = data.split(",")
                data_value = []
                for data_line in data_set:
                    data_value.append(data_line)
                data_main.append(data_value)
    i =0
    n =0
    while i < len(data_main[0]):
        combinations=[]
        for data in data_main:
            combinations.append(data[i])
        nodes[n].updateCombinations(combinations)
        combinations =[]
        n+=1
        i+=1
    
    #Get States of the nodes
    for data in data_main:
        for index, value in enumerate(data):
            nodes[index].updateStates(value)
            
    #Get results of each node
    i=0
    while i < len(nodes)-1:
        nodes[i].updateResults(nodes[-1].combinations)
        i+=1

    #--------------------------------ID3---------------------------------------#
    #Get the entropy of each node
    for node in nodes:
        node.updateEntropy(len(data_main))

    #Get the Gain
    i=0
    while i < len(nodes)-1:
        nodes[i].infGain(nodes[-1].entropy)
        i+=1
    
    #-------Start painting nodes------#
    
    def f7(seq):
        seen = set()
        seen_add = seen.add
        return [x for x in seq if not (x in seen or seen_add(x))]
    
    #Paint tree function
    def paintTree(level):
        #Obtain best node
        gain = 0
        best_gain=nodes[0] ##AQUI FALLA EL RECURSIVO: llega el punto donde se la pasa en el nodo 0
        i=0
        while i < len(nodes)-1:
            if nodes[i].visited == 0:
                if nodes[i].gain > gain:
                    best_gain = nodes[i]
                    gain = best_gain.gain
            i+=1
        best_gain.setVisited()
        
        #Obtain paths
        paths={}
        for state in best_gain.states:
            #print("State :" + state)
            path={state: f7(best_gain.results[state])}
            paths.update(path)
        
        for state in best_gain.states:
            if(len(paths[state]) <2):
                print((2*level)*" " + best_gain.name + ": " + state)
                print((2*(level+1))*" " + "ANSWER: "+ paths[state][0])
            else:
                print((2*level)*" " + best_gain.name + ": " + state)
                next_lvl  = level +1
                #recursive
                #paintTree(next_lvl)#algo falla en el recursivo

    paintTree(0)