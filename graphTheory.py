import pandas as pd
import numpy as np
import networkx as nx
#data = pd.read_csv('hall_data.csv')

room_number = input("Room Number: ")
apriltag = int(input("AprilTag ID: "))


data = pd.read_csv("Hall_data.csv")
df = nx.from_pandas_edgelist(data, source = 'ATID', target = 'Connection', edge_attr=True)

shortest_path = nx.dijkstra_path(df, source = apriltag, target = room_number, weight = 'Room Distance')

print(shortest_path)
if len(shortest_path) == 2:
    target = data[(data['ATID'] == shortest_path[0])]
    target2 = target[(target['Connection'] == shortest_path[1])]
    print(target2['Direction'].to_string(index = False))
else:
    # l = [s for s in shortest_path if type(s) != str]
    target = data[(data['ATID'] == shortest_path[0])]
    target2 = target[(target['Connection'] == shortest_path[1])]
    print(target2['Direction'].to_string(index = False))
    


#Delete strings in shortest_path that are not the nodes, only the target room number
#should be the only string in the list

#print direction by finding index of first two shortest_path vars after massaging it
