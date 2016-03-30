import os
from verbose_display import display
import networkx as nx
import generate_graphs as GG
import introduce_all_content as IAC
from collections import Counter
import numpy as np

############################################

def combine_event_forests (EFAll):

    edge_list = []
    weighted_edges = []

    for ET in EFAll:
        edge_list.extend(nx.edges(ET))
    #print edge_list

    edge_frequencies = Counter(edge_list)
    #print edge_frequencies

    for key, value in edge_frequencies.iteritems():
        weighted_edges.append((key[0],key[1],value))

    return weighted_edges

############################################

def impose_weight_restriction (weighted_edges, weight_threshold):

    weighted_edges_filtered = [edge for edge in weighted_edges if edge[2]>=weight_threshold]

    return weighted_edges_filtered

############################################

def get_weight_threshold (weighted_edges, PARAMS):

    weights = [int(edge[2]) for edge in weighted_edges]
    mean = np.mean(weights)
    std = np.std(weights)
    #print weights
    #print "Mean: "+str(mean)+", Std: "+str(std)
    std_x = float(PARAMS['weight_threshold'])
    th = int(round(mean+(std*std_x),0))
    #print "Threshold: "+str(th)

    return th

############################################

def get_weighted_graph (weighted_edges_filtered):
    
    Ginferred_weighted_directed = nx.DiGraph()
    Ginferred_weighted_directed.add_weighted_edges_from(weighted_edges_filtered)

    return Ginferred_weighted_directed

############################################

def get_directed_graph(weighted_edges_filtered):

    directed_edges = []    
    for edge in weighted_edges_filtered:
        directed_edges.append((edge[0],edge[1]))
    Ginferred_directed = nx.DiGraph()
    Ginferred_directed.add_edges_from(directed_edges)

    return Ginferred_directed

############################################

def infer_graph (Gcomplete, PARAMS):

    EFAll = []
    run_count = PARAMS['run_count']
    
    for i in range(run_count):
        EF = IAC.introduce_all_content (Gcomplete, PARAMS)
        EFAll.extend(EF)

    weighted_edges = combine_event_forests (EFAll)
    weight_threshold = get_weight_threshold (weighted_edges, PARAMS)
    weighted_edges_filtered = impose_weight_restriction (weighted_edges, weight_threshold)
    
    Ginferred_weighted_directed = get_weighted_graph(weighted_edges_filtered)
    Ginferred_directed = get_directed_graph(weighted_edges_filtered)
    Ginferred = Ginferred_directed.to_undirected()
    
    return Ginferred

############################################

def main():
    #Gbase, Gcomplete = GG.generate_graphs()
    #Ginferred = infer_graph (Gcomplete, SP.RUN_COUNT)
    #print Ginferred.edge
    return

############################################

if __name__ == "__main__":
    main()
