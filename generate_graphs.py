import os
import networkx as nx
import matplotlib.pyplot as plt
import math, random
import collections
import simulation_properties as SP

path_prefix = "/home/satadal/Workspaces/Projects/Social.Caching/Code"

##################################################

def filter_edgelist(node_count):
    ifp = open(os.path.join(path_prefix,SP.DATASET),"r")
    ofp = open(os.path.join(path_prefix,SP.SAMPLED_DATASET),"w")
    edges = ifp.readlines()
    ifp.close()

    writelines = ""

    for edge in edges:
        tokens = edge.rstrip().split(" ")
        if int(tokens[0]) < node_count and int(tokens[1]) < node_count:
            writelines += edge

    ofp.write(writelines)
    ofp.close()
    return

##################################################

def draw_graph(graph,title):
    graph_gvz = nx.to_agraph(graph)
    graph_gvz.layout(prog="neato")
    graph_gvz.draw(os.path.join(path_prefix,title+".ps"))

##################################################

def assign_probabilities(Gcomplete,mean,sd):
    
    no_of_nodes = Gcomplete.number_of_nodes()

    #Assign viewing probability to each node
    temp=[]
    for n in range(0, no_of_nodes):
        for m in range(0, no_of_nodes):
            temp.append(random.gauss(mean,sd))
        Gcomplete.node[n]['Pview']=temp
        temp=[]

    #Assign sharing probability to each node
    for n in range(0, no_of_nodes):
        for m in range(0, no_of_nodes):
            temp.append(random.gauss(mean,sd))
        Gcomplete.node[n]['Pshare']=temp
        temp=[]

    return

##################################################

def boost_view_share_probabilities(Gcomplete,Gbase,view_boost,share_boost):
    
    count = 0

    for edge in Gcomplete.edges():

        if Gbase.has_edge(*edge):

            Gcomplete.node[edge[0]]['Pview'][edge[1]] *= (1.0+view_boost)
            Gcomplete.node[edge[0]]['Pshare'][edge[1]] *= (1.0+share_boost)
            Gcomplete.node[edge[1]]['Pview'][edge[0]] *= (1.0+view_boost)
            Gcomplete.node[edge[1]]['Pshare'][edge[0]] *= (1.0+share_boost)
            
            if Gcomplete.node[edge[0]]['Pview'][edge[1]] > 1.0:
                Gcomplete.node[edge[0]]['Pview'][edge[1]] = 1.0
                count += 1
            if Gcomplete.node[edge[0]]['Pshare'][edge[1]] > 1.0:
                Gcomplete.node[edge[0]]['Pshare'][edge[1]] = 1.0
                count += 1
            if Gcomplete.node[edge[1]]['Pview'][edge[0]] > 1.0:
                Gcomplete.node[edge[1]]['Pview'][edge[0]] = 1.0
                count += 1
            if Gcomplete.node[edge[1]]['Pshare'][edge[0]] > 1.0:
                count += 1
                Gcomplete.node[edge[1]]['Pshare'][edge[0]] = 1.0    
    
    return count

##################################################

def generate_graphs(filter_count,mean,sd,view_boost,share_boost):
    
    filter_edgelist(filter_count)
    Gbase = nx.read_edgelist(os.path.join(path_prefix,SP.SAMPLED_DATASET), nodetype=int)
    #draw_graph(Gbase,"Gbase")
    Gcomplete = nx.complete_graph(Gbase.number_of_nodes())
    #draw_graph(Gcomplete,"Gcomplete")
    assign_probabilities(Gcomplete,mean,sd)
    edges_with_prob_one = boost_view_share_probabilities(Gcomplete,Gbase,view_boost,share_boost)
    print("Edges with probability 1.0: "+str(edges_with_prob_one))

    return Gbase, Gcomplete

##################################################

def main():
    generate_graphs (SP.SAMPLE_SIZE, SP.MEAN, SP.SD, SP.VIEW_BOOST, SP.SHARE_BOOST)
    return

##################################################

if __name__ == '__main__':
    main()
