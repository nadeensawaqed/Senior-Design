import graphviz
import pandas as pd
import numpy as np
from iteration_utilities import deepflatten

tags_installed = 13
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
    dot = graphviz.Digraph(engine = 'circo')
    
    res = np.array([[i for i in CLUSTER[x]] for x in CLUSTER.keys()])
    flat = list(deepflatten(res))

    for tag in range(0, tags_installed):

        dot.node(str(tag), str(tag)) ### create apriltag digit nodes

        if tag == 0:
            left = CLUSTER['O']
            for n in left:
                dot.edge(str(tag), str(n), color = 'blue')
            for j in list(set(flat) - set(left)):
                dot.edge(str(tag), str(j), color = 'red')

        if tag == 1:
            left = CLUSTER['O']
            fwd = CLUSTER['N'] + CLUSTER['M'] + CLUSTER['J'] + CLUSTER['K']
            for n in left:
                dot.edge(str(tag), str(n), color = 'blue')
            for m in fwd:
                dot.edge(str(tag), str(m), color = 'cyan')
            for j in list(set(flat) - (set(left+fwd))):
                dot.edge(str(tag), str(j), color = 'red')

        if tag == 2:
            left = CLUSTER['L'] + CLUSTER['N'] + CLUSTER['O'] + CLUSTER['M']
            fwd = CLUSTER['H'] + CLUSTER['I'] + CLUSTER['J'] + CLUSTER['K'] 
            for n in left:
                dot.edge(str(tag), str(n), color = 'blue')
            for m in fwd:
                dot.edge(str(tag), str(m), color = 'cyan')
            for j in list(set(flat) - (set(left+fwd))):
                dot.edge(str(tag), str(j), color = 'red')

        if tag == 3:
            right = CLUSTER['A'] + CLUSTER['B'] + CLUSTER['C'] + CLUSTER['D'] + CLUSTER['P'] + CLUSTER['Q'] 
            fwd = CLUSTER['E'] + CLUSTER['F']

            for n in right:
                dot.edge(str(tag), str(n), color = 'red')
            for m in fwd:
                dot.edge(str(tag), str(m), color = 'cyan')
            for j in list(set(flat) - (set(left+fwd))):
                dot.edge(str(tag), str(j), color = 'blue')

        if tag == 4:
            fwd = CLUSTER['A'] + CLUSTER['C'] + CLUSTER['P'] + CLUSTER['Q']
            for m in fwd:
                dot.edge(str(tag), str(m), color = 'cyan')
            for j in list(set(flat) - set(fwd)):
                dot.edge(str(tag), str(j), color = 'blue')

        if tag == 5:
            fwd = CLUSTER['Q']
            bck = CLUSTER['A']
            right = CLUSTER['C'] + CLUSTER['D'] + CLUSTER['P']
            for m in fwd:
                dot.edge(str(tag), str(m), color = 'cyan')
            for n in bck:
                dot.edge(str(tag), str(n))
            for p in right:
                dot.edge(str(tag), str(p), color = 'red')
            for j in list(set(flat) - set(fwd + bck + right)):
                dot.edge(str(tag), str(j), color = 'blue')

        if tag == 6:
            fwd = CLUSTER['A'] + CLUSTER['C'] + CLUSTER['B'] + CLUSTER['Q']
            left = CLUSTER['P']
            for m in fwd:
                dot.edge(str(tag), str(m), color = 'cyan')
            for n in left:
                dot.edge(str(tag), str(n), color = 'blue')
            for j in list(set(flat) - set(fwd + left)):
                dot.edge(str(tag), str(j), color = 'red')

        if tag == 7:
            fwd = CLUSTER['E'] + CLUSTER['F'] + CLUSTER['B'] + CLUSTER['G']
            left = CLUSTER['P'] + CLUSTER['A'] + CLUSTER['C']  + CLUSTER['D']  + CLUSTER['Q']
            for m in fwd:
                dot.edge(str(tag), str(m), color = 'cyan')
            for n in left:
                dot.edge(str(tag), str(n), color = 'blue')
            for j in list(set(flat) - set(fwd + left)):
                dot.edge(str(tag), str(j), color = 'red')
        
        if tag == 8:
            fwd = CLUSTER['H'] + CLUSTER['I'] + CLUSTER['J'] + CLUSTER['K'] + CLUSTER['G'] + CLUSTER['L']
            right = CLUSTER['N'] + CLUSTER['M'] + CLUSTER['O']
            for m in fwd:
                dot.edge(str(tag), str(m), color = 'cyan')
            for n in right:
                dot.edge(str(tag), str(n), color = 'red')
            for j in list(set(flat) - set(fwd + right)):
                dot.edge(str(tag), str(j), color = 'blue')

        if tag == 9:
            fwd = CLUSTER['N'] + CLUSTER['M'] + CLUSTER['J'] + CLUSTER['K']
            right = CLUSTER['O']
            for m in fwd:
                dot.edge(str(tag), str(m), color = 'cyan')
            for n in right:
                dot.edge(str(tag), str(n), color = 'red')
            for j in list(set(flat) - set(fwd + right)):
                dot.edge(str(tag), str(j), color = 'blue')

        if tag == 10: 
            right = CLUSTER['O']
            for n in right:
                dot.edge(str(tag), str(n), color = 'red')
            for j in list(set(flat) - set(right)):
                dot.edge(str(tag), str(j), color = 'cyan')

        if tag == 11:
            fwd = CLUSTER['J'] + CLUSTER['K'] + CLUSTER['H']
            bck = CLUSTER['N']
            for m in fwd:
                dot.edge(str(tag), str(m), color = 'cyan')
            for n in bck:
                dot.edge(str(tag), str(n))
            for j in list(set(flat) - set(fwd + bck)):
                dot.edge(str(tag), str(j), color = 'blue')

        if tag == 12:
            fwd = CLUSTER['J'] + CLUSTER['K'] + CLUSTER['N']
            bck = CLUSTER['H']
            left = CLUSTER['I']
            left.remove(1402)
            for m in fwd:
                dot.edge(str(tag), str(m), color = 'cyan')
            for n in bck:
                dot.edge(str(tag), str(n))
            for n in left:
                dot.edge(str(tag), str(n), color = 'blue')
            for j in list(set(flat) - set(fwd + bck + left)):
                dot.edge(str(tag), str(j), color = 'red')
            
    dot.render('doctest-output/room_map.gv', view=True)

if __name__ == '__main__':
    
    graph(file_handler(file))