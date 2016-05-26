import os
import networkx as nx
import matplotlib.pyplot as plt
import math, random
import collections
from operator import itemgetter as itg
#from statistics import median
import numpy as np
import simulation_properties as SP
from utilities import display
import run_all_simulations as RAS

path_prefix = SP.CWD

#################################################

def draw_graph(graph,title):
    graph_gvz = nx.to_agraph(graph)
    graph_gvz.layout(prog="neato")
    graph_gvz.draw(os.path.join(path_prefix,title+".ps"))
    display("draw_graph","Drawn "+title+" and saved to "+title+".ps")

##################################################

def assign_probabilities(Gfriendship,mean,sd):
    
    #Assign viewing probability to each node
    #no_of_nodes = nx.number_of_nodes(Gfriendship)
    temp={}
    for head in Gfriendship.node:
        for tail in Gfriendship.neighbors(head):
            temp[tail] = random.gauss(mean,sd)
        Gfriendship.node[head]['Pview']=temp
        temp={}

    #Assign sharing probability to each node
    temp = {}
    for head in Gfriendship.node:
        for tail in Gfriendship.neighbors(head):
            temp[tail] = random.gauss(mean,sd)
        Gfriendship.node[head]['Pshare']=temp
        temp={}

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
'''
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
'''
##################################################
'''
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
'''
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

    #filter_count = PARAMS['sample_size']
    mean = PARAMS['vwshprob_mean']
    sd = PARAMS['vwshprob_stdv']
    #view_boost = PARAMS['view_boost']
    #share_boost = PARAMS['share_boost']
    
    #Goriginal = nx.read_edgelist(os.path.join(path_prefix,PARAMS['dataset']), nodetype=int)
    #display("generate_graphs", "Prepared Goriginal from entire dataset.")
    #filtered_nodelist = get_filtered_nodes (Goriginal, PARAMS)
    #display("generate_graphs", "Received filtered node list from get_filtered_nodes().")

    #filter_edgelist(PARAMS,filtered_nodelist)
    #display("generate_graphs", "Filtered edge list recorded in sampled dataset.")
    #Gbase = nx.read_edgelist(os.path.join(path_prefix,PARAMS['sampled_dataset']), nodetype=int)
    #display("generate_graphs", "Prepared Gbase from sampled dataset.")

    #Gcomplete = nx.complete_graph(nx.number_of_nodes(Gbase))
    #display("generate_graphs", "Prepared Gcomplete from sampled dataset.")

    Gfriendship = nx.read_edgelist(os.path.join(path_prefix,"resource","facebook.txt"), nodetype=int)
    #print Gfriendship.edge[1]
    assign_probabilities(Gfriendship,mean,sd)
    #print Gfriendship.node[1]

    #fp = open(os.path.join(path_prefix,"resource","facebook.txt"))
    #print fp.readlines()
    #display("generate_graphs", "Assigned probabilities to all nodes.")

    #edges_matched = boost_view_share_probabilities(Gcomplete,Gbase,view_boost,share_boost)
    #display("generate_graphs", "Boosted view and share probabilities, number of matched edges is "+str(edges_matched))

    return Gfriendship

##################################################

def main():
    params = RAS.load_parameters_for_test_run()
    #print params
    #params['sampling_technique'] = "DegreeMin"
    Gfriendship = generate_graphs (params)
    #print Gfriendship.node[2048]
    # display("generate_graphs:main", "Gbase node-list: " + str(Gbase.node))
    # display("generate_graphs:main", "Gbase edge-list: " + str(Gbase.edge))
    # display("generate_graphs:main", "Gcomplete node-list: " + str(Gcomplete.node))
    # display("generate_graphs:main", "Gcomplete edge-list: " + str(Gcomplete.edge))
    #draw_graph(Gfriendship,"Gfriendship")
    #draw_graph(Gcomplete,"Gcomplete")
    return

##################################################

if __name__ == '__main__':
    main()
