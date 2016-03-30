import os
import networkx as nx
import matplotlib.pyplot as plt
import math, random
import collections
from operator import itemgetter as itg
#from statistics import median
import numpy as np
import simulation_properties as SP
from verbose_display import display
import run_all_simulations as RAS

path_prefix = SP.CWD

##################################################

def filter_edgelist (PARAMS, node_list):
    
    ifp = open(os.path.join(path_prefix,PARAMS['dataset']),"r")
    ofp = open(os.path.join(path_prefix,PARAMS['sampled_dataset']),"w")
    edges = ifp.readlines()
    ifp.close()

    count = 0
    mapping = {}
    for node in node_list:
        mapping[node] = count
        count += 1
    display("filter_edgelist","Created mapping for nodes for " + str(count) + " nodes.")

    writelines = ""

    cedge = 0
    cmatch = 0
    for edge in edges:
        cedge += 1
        tokens = edge.rstrip().split(" ")
        if (int(tokens[0]) in node_list) and (int(tokens[1]) in node_list):
            writelines += str(mapping[int(tokens[0])]) + " " + str(mapping[int(tokens[1])]) + "\n"
            cmatch += 1

    ofp.write(writelines)
    ofp.close()
    display("filter_edgelist", "The edge-list corresponding to filtered node-list with " + str(cedge) + " edges and " + str(cmatch) + " matching edges.")
    
    return

##################################################

def draw_graph(graph,title):
    graph_gvz = nx.to_agraph(graph)
    graph_gvz.layout(prog="neato")
    graph_gvz.draw(os.path.join(path_prefix,title+".ps"))
    display("draw_graph","Drawn "+title+" and saved to "+title+".ps")

##################################################

def assign_probabilities(Gcomplete,mean,sd):
    
    #Assign viewing probability to each node
    no_of_nodes = nx.number_of_nodes(Gcomplete)
    temp=[]
    for n in range(0,no_of_nodes):
        for m in range(0,no_of_nodes):
            temp.append(random.gauss(mean,sd))
        Gcomplete.node[n]['Pview']=temp
        temp=[]

    #Assign sharing probability to each node
    temp = []
    for n in range(0, no_of_nodes):
        for m in range(0, no_of_nodes):
            temp.append(random.gauss(mean,sd))
        Gcomplete.node[n]['Pshare']=temp
        temp=[]

    return

##################################################

def sanitize_prob (Gcomplete):
  
    for edge in Gcomplete.edges():
    
        if Gcomplete.node[edge[0]]['Pview'][edge[1]] > 1.0:
            Gcomplete.node[edge[0]]['Pview'][edge[1]] = 1.0
    
        if Gcomplete.node[edge[0]]['Pshare'][edge[1]] > 1.0:
            Gcomplete.node[edge[0]]['Pshare'][edge[1]] = 1.0

        if Gcomplete.node[edge[1]]['Pview'][edge[0]] > 1.0:
            Gcomplete.node[edge[1]]['Pview'][edge[0]] = 1.0

        if Gcomplete.node[edge[1]]['Pshare'][edge[0]] > 1.0:
            Gcomplete.node[edge[1]]['Pshare'][edge[0]] = 1.0

        if Gcomplete.node[edge[0]]['Pview'][edge[1]] < 0.0:
            Gcomplete.node[edge[0]]['Pview'][edge[1]] = 0.0
    
        if Gcomplete.node[edge[0]]['Pshare'][edge[1]] < 0.0:
            Gcomplete.node[edge[0]]['Pshare'][edge[1]] = 0.0

        if Gcomplete.node[edge[1]]['Pview'][edge[0]] < 0.0:
            Gcomplete.node[edge[1]]['Pview'][edge[0]] = 0.0

        if Gcomplete.node[edge[1]]['Pshare'][edge[0]] < 0.0:
            Gcomplete.node[edge[1]]['Pshare'][edge[0]] = 0.0

    display("sanitize_prob", "Sanitized Gcomplete.")

    return

##################################################

def boost_view_share_probabilities(Gcomplete,Gbase,view_boost,share_boost):
    
    count = 0

    for edge in Gcomplete.edges():

        if Gbase.has_edge(*edge):

            count += 1
            Gcomplete.node[edge[0]]['Pview'][edge[1]] *= (1.0+view_boost)
            Gcomplete.node[edge[0]]['Pshare'][edge[1]] *= (1.0+share_boost)
            Gcomplete.node[edge[1]]['Pview'][edge[0]] *= (1.0+view_boost)
            Gcomplete.node[edge[1]]['Pshare'][edge[0]] *= (1.0+share_boost)
   
    display("boost_view_share_probabilities", "Provided view and share probability boosts to existing edges.")
    sanitize_prob(Gcomplete)
    display("boost_view_share_probabilities", "Sanitized probability values > 1 and < 0.")

    return count

##################################################

def get_filtered_nodes (Goriginal, PARAMS):

    size = PARAMS['sample_size']
    sample_using = PARAMS['sampling_technique']
    node_list = []

    degrees = Goriginal.degree(list(Goriginal.node))
    node_deg_asc = sorted ( degrees.items(), key=itg(1) )
    node_deg_desc = sorted ( degrees.items(), key=itg(1), reverse=True )    
    deg_asc = [i[1] for i in node_deg_asc]
    node_desc = [i[0] for i in node_deg_desc]

    if sample_using == "DegreeMin":
        median = int(math.ceil(np.median(deg_asc)))
        start_pos = 0
        for i in node_deg_asc:
            if i[1] == median:
                start_pos = i[0]
                break
        node_asc = [i[0] for i in node_deg_asc]
        node_list = node_asc[start_pos:][:size]

    elif sample_using == "DegreeMax":
        node_list = node_desc[:size]

    display("get_filtered_nodes", "Sampling done using "+sample_using+"; node list size is "+str(len(node_list))+".")

    return node_list

##################################################

#def complete_graph_from_list(L, create_using=None):
#    G = networkx.empty_graph(len(L),create_using)
#    if len(L)>1:
#        edges = itertools.combinations(L,2)
#        G.add_edges_from(edges)
#        display("complete_graph_from_list", "Prepared Gcomplete from filtered node list; size is " + str(len(G.node)) + ".")
#    return G

##################################################

def generate_graphs (PARAMS):

    filter_count = PARAMS['sample_size']
    mean = PARAMS['vwshprob_mean']
    sd = PARAMS['vwshprob_stdv']
    view_boost = PARAMS['view_boost']
    share_boost = PARAMS['share_boost']
    
    Goriginal = nx.read_edgelist(os.path.join(path_prefix,PARAMS['dataset']), nodetype=int)
    display("generate_graphs", "Prepared Goriginal from entire dataset.")
    filtered_nodelist = get_filtered_nodes (Goriginal, PARAMS)
    display("generate_graphs", "Received filtered node list from get_filtered_nodes().")

    filter_edgelist(PARAMS,filtered_nodelist)
    display("generate_graphs", "Filtered edge list recorded in sampled dataset.")
    Gbase = nx.read_edgelist(os.path.join(path_prefix,PARAMS['sampled_dataset']), nodetype=int)
    display("generate_graphs", "Prepared Gbase from sampled dataset.")

    Gcomplete = nx.complete_graph(nx.number_of_nodes(Gbase))
    display("generate_graphs", "Prepared Gcomplete from sampled dataset.")

    assign_probabilities(Gcomplete,mean,sd)
    display("generate_graphs", "Assigned probabilities to all nodes.")

    edges_matched = boost_view_share_probabilities(Gcomplete,Gbase,view_boost,share_boost)
    display("generate_graphs", "Boosted view and share probabilities, number of matched edges is "+str(edges_matched))

    return Gbase, Gcomplete

##################################################

def main():
    params = RAS.load_parameters_for_test_run()
    params['sampling_technique'] = "DegreeMin"
    Gbase, Gcomplete = generate_graphs (params)
    # display("generate_graphs:main", "Gbase node-list: " + str(Gbase.node))
    # display("generate_graphs:main", "Gbase edge-list: " + str(Gbase.edge))
    # display("generate_graphs:main", "Gcomplete node-list: " + str(Gcomplete.node))
    # display("generate_graphs:main", "Gcomplete edge-list: " + str(Gcomplete.edge))
    draw_graph(Gbase,"Gbase")
    draw_graph(Gcomplete,"Gcomplete")
    return

##################################################

if __name__ == '__main__':
    main()
