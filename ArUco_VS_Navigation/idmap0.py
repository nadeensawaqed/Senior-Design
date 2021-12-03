import pandas as pd
import numpy as np
from iteration_utilities import deepflatten
import yaml
address_db = 'address_database.yaml'
file = 'NC_FIRST_FLOOR.xlsx'

class CreateDict(dict):
    def __init__(self):
        self = dict()

    def add(self, key, value):
        self[key] = value

def file_handler(file_name, func):
    global NODES
    if func == 1:
        try:
            df = pd.read_excel(file_name, engine = 'openpyxl')
            nodes = CreateDict()

            for col, values in df.iteritems():
                rooms = df[col].dropna().tolist()
                rooms = list(map(int, rooms))
                nodes.add(col, rooms)
            NODES = nodes
        except:
            print('File not found')

    if func == 2:
        global DB
        with open(file_name) as file:
            try:
                DB = yaml.safe_load(file)   
                print(DB)
                return DB
            except yaml.YAMLError as exc:
                print(exc)

def get_address(address):
    file_handler(address_db, 2)
    file_handler(file, 1)
    if address in DB.values():
        return address
    else: return 'Address Error'

def graph(room, id):
    res = np.array([[i for i in NODES[x]] for x in NODES.keys()], dtype = object)
    flat = list(deepflatten(res))
    
    if id == 0:
        left = NODES['O']
        if room in left:
            return 'l'
        else:
            return 'r'

    if id == 1:
        left = NODES['O']
        fwd = NODES['N'] + NODES['M'] + NODES['J'] + NODES['K']
        if room in left:
            return 'l'
        if room in fwd:
            return 'f'
        else:
            return 'r'

    if id == 2:
        left = NODES['L'] + NODES['N'] + NODES['O'] + NODES['M']
        fwd = NODES['H'] + NODES['I'] + NODES['J'] + NODES['K'] 
        if room in left:
            return 'l'
        if room in fwd:
            return 'f'
        else:
            return 'r'

    if id == 3:
        right = NODES['A'] + NODES['B'] + NODES['C'] + NODES['D'] + NODES['P'] + NODES['Q'] 
        fwd = NODES['E'] + NODES['F']
        if room in right:
            return 'r'
        if room in fwd:
            return 'f'
        else:
            return 'l'

    if id == 4:
        fwd = NODES['A'] + NODES['C'] + NODES['P'] + NODES['D'] + NODES['Q']
        if room in fwd:
            return 'f'
        else:
            return 'l'

    if id == 5:
        fwd = NODES['Q']
        bck = NODES['A']
        right = NODES['C'] + NODES['D'] + NODES['P']
        if room in right:
            return 'r'
        if room in fwd:
            return 'f'
        if room in bck:
            return 'b'
        else:
            return 'l'

    if id == 6:
        fwd = NODES['A'] + NODES['C'] + NODES['B'] + NODES['Q']
        left = NODES['P']
        
        if room in fwd:
            return 'f'
        if room in left:
            return 'l'
        else:
            return 'r'

    if id == 7:
        fwd = NODES['E'] + NODES['F'] + NODES['B'] + NODES['G']
        left = NODES['P'] + NODES['A'] + NODES['C']  + NODES['D']  + NODES['Q']
        if room in fwd:
            return 'f'
        if room in left:
            return 'l'
        else:
            return 'r'
    
    if id == 8:
        fwd = NODES['H'] + NODES['I'] + NODES['J'] + NODES['K'] + NODES['G'] + NODES['L']
        right = NODES['N'] + NODES['M'] + NODES['O']
        if room in fwd:
            return 'f'
        if room in right:
            return 'r'
        else:
            return 'l'

    if id == 9:
        fwd = NODES['N'] + NODES['M'] + NODES['J'] + NODES['K']
        right = NODES['O']
        if room in fwd:
            return 'f'
        if room in right:
            return 'r'
        else:
            return 'l'

    if id == 10: 
        right = NODES['O']
        if room in right:
            return 'r'
        else:
            return 'f'

    if id == 11:
        fwd = NODES['J'] + NODES['K'] + NODES['H']
        bck = NODES['N']
        if room in fwd:
            return 'f'
        if room in bck:
            return 'b'
        else:
            return 'l'

    if id == 12:
        fwd = NODES['J'] + NODES['K'] + NODES['N']
        bck = NODES['H']
        left = NODES['I']
        if 1402 in left:
            left.remove(1402)
        if room in fwd:
            return 'f'
        if room in bck:
            return 'b'
        if room in left:
            return 'l'
        else:
            return 'r'
    else:
        return 'na'
#file_handler(address_db, 2)