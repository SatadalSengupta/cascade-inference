from operator import itemgetter as itg
import os
import networkx as nx
from statistics import median, mean

def deg_dist(G):
    degrees = G.degree(list(G.node))
    node_deg_asc = sorted ( degrees.items(), key=itg(1) )
    node_deg_desc = sorted (degrees.items(), key=itg(1), reverse=True)
    deg_asc = [i[1] for i in node_deg_asc]
    deg_desc = [i[1] for i in node_deg_desc]
    print "ASC:\n"
    print deg_asc
    print "DESC: \n"
    print deg_desc
    print "Median: "+str(median(deg_asc))
    print "Mean: " + str(mean(deg_asc))
    return

def main():
    G = nx.read_edgelist("facebook.txt",nodetype=int)
    deg_dist(G)
    return

if __name__ == '__main__':
    main()
