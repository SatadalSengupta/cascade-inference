import os
import networkx as nx
import pickle

def generate_nodes_in_all_graphs():
    
    graphsPaths = []
    for f in os.listdir("resource"):
        if ".txt" in f:
            graphsPaths.append(f)

    for graphsPath in graphsPaths:
        graph = nx.read_edgelist(os.path.join("resource",graphsPath),nodetype=int)
        graphNodes = nx.nodes(graph)
        pickle.dump(graphNodes,open(os.path.join("resource",str(graphsPath).replace("txt","nodes")),"wb"))
        #print graphsPath.replace("txt","nodes")

    #print graphsPaths
    #graphsPath = os.path.join("resource")

def main():
    generate_nodes_in_all_graphs()
    return

if __name__ == '__main__':
    main()
