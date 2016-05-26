import os
import pickle
import networkx as nx
from datetime import datetime

#################################

def infer_graph(filename, community):

    PARAMS = {}
    tokens = filename.split("_")
    PARAMS["poi_mean"] = float(tokens[2])
    PARAMS["poi_stdv"] = float(tokens[3])
    PARAMS["content_count"] = int(tokens[4])
    PARAMS["vwshprob_mean"] = float(tokens[5])
    PARAMS["vwshprob_stdv"] = float(tokens[6])
    PARAMS["cmlb_view"] = float(tokens[7])
    PARAMS["cmlb_share"] = float(tokens[8].replace(".txt",""))
    #print PARAMS

    fp = open(filename,"r")
    lines = fp.readlines()
    fp.close()

    if community == "MaxSize":
        nodes = pickle.load(open("resource/facebook_max_size.nodes","rb"))
    elif community == "MaxEdgeDensity":
        nodes = pickle.load(open("resource/facebook_max_edge_density.nodes","rb"))
    else:
        return

    Gintermediate = nx.Graph()
    Gintermediate.add_nodes_from(nodes)

    for line in lines:
        tokens = line.rstrip().split(",")
        timestamp = datetime.strptime(tokens[0],"%Y-%m-%d %H:%M:%S.%f")
        nodeId = int(tokens[1])
        contentId = tokens[2]
        vworsh = tokens[3]
        if nodeId in nodes:





#################################

def main():
    infer_graph("timelines/event_timeline_0.148_0.079_100_0.5_0.15_0.4_0.4.txt")
    return

#################################

if __name__ == "__main__":
    main()

#################################

