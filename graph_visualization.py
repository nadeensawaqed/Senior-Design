import graphviz
import pandas as pd
import numpy as np
from iteration_utilities import deepflatten

tags_installed = 14
FWD = 'F'
BCK = 'B'
RIGHT = 'R'
LEFT = 'L'
directions = [FWD, BCK, RIGHT, LEFT]
blg_dict = {}
file = 'NC_FIRST_FLOOR.xlsx'

class CreateDict(dict):
    def __init__(self):
        self = dict()

    def add(self, key, value):
        self[key] = value
  
def file_handler(file_name):

    df = pd.read_excel(file_name, engine = 'openpyxl')
    nodes = CreateDict()

    for col, values in df.iteritems():
        rooms = df[col].dropna().tolist()
        rooms = list(map(int, rooms))
        nodes.add(col, rooms)
    return nodes
    
def graph(CLUSTER):
    dot = graphviz.Digraph()
    res = np.array([[i for i in CLUSTER[x]] for x in CLUSTER.keys()])
    flat = list(deepflatten(res))
    print(flat)

    for tag in range(0, tags_installed):
        dot.node(str(tag), str(tag)) ### create apriltag digit nodes
        if tag == 0:
            left = CLUSTER['O']
            for n in left:
                dot.edge(str(tag), str(n), label = LEFT)
            
            for j in list(set(flat) - set(left)):
                dot.edge(str(tag), str(j), label = RIGHT)
        if tag == 1:
            left = CLUSTER['O']
            fwd = CLUSTER['N'] + CLUSTER['M'] + CLUSTER['J'] + CLUSTER['K']
            for n in left:
                dot.edge(str(tag), str(n), label = LEFT)
            for m in fwd:
                dot.edge(str(tag), str(m), label = FWD)
            for j in list(set(flat) - (set(left+fwd))):
                dot.edge(str(tag), str(j), label = RIGHT)
        if tag == 2:
            left = CLUSTER['L'] + CLUSTER['N'] + CLUSTER['O'] + CLUSTER['M']
            fwd = CLUSTER['H'] + CLUSTER['I'] + CLUSTER['J'] + CLUSTER['K'] 
            for n in left:
                dot.edge(str(tag), str(n), label = LEFT)
            for m in fwd:
                dot.edge(str(tag), str(m), label = FWD)
            for j in list(set(flat) - (set(left+fwd))):
                dot.edge(str(tag), str(j), label = RIGHT)
        if tag == 3:
            right = CLUSTER['A'] + CLUSTER['B'] + CLUSTER['C'] + CLUSTER['D'] + CLUSTER['P']  
            fwd = CLUSTER['E'] + CLUSTER['F']

            for n in right:
                dot.edge(str(tag), str(n), label = RIGHT)
            for m in fwd:
                dot.edge(str(tag), str(m), label = FWD)
            for j in list(set(flat) - (set(left+fwd))):
                dot.edge(str(tag), str(j), label = LEFT)
        if tag == 4:
             
            fwd = CLUSTER['A'] + CLUSTER['C'] + CLUSTER['P']

            for m in fwd:
                dot.edge(str(tag), str(m), label = FWD)
            for j in list(set(flat) - set(fwd)):
                dot.edge(str(tag), str(j), label = LEFT)
            
            
        #     dot.edge()
    

    #dot.edges(['01', '02', '03'])
    # dot.edge('B', 'L', constraint='false')
    # print(dot.source)
    #dot.view()
    dot.render('doctest-output/round-table.gv', view=True)

if __name__ == '__main__':
    
    graph(file_handler(file))