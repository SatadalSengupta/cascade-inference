import os
import pickle
import community as LouvainCommunity
import networkx as nx
from verbose_display import display

#####################################

def build_louvain_communities ():

    G = nx.read_edgelist("resource/facebook.txt",nodetype=int)
    partition = LouvainCommunity.best_partition(G)
    number_of_partitions = len(set(partition.values()))
    community_count = 0
    communities = []
    
    for community in set(partition.values()) :
        community_count += 1
        community_nodes = [nodes for nodes in partition.keys() if partition[nodes] == community]
        communities.append(community_nodes)
    
    fp = open(os.path.join("resource","louvain_communities.pkl"),"wb")
    pickle.dump (communities, fp)
    fp.close()

#####################################

def build_community (G, criterion):
    
    fp = None
    communities = []
    maxCommunityEdgeList = []
    
    try:
        fp = open(os.path.join("resource","louvain_communities.pkl"),"rb")
        #print "Pickle exists"
    except:
        build_louvain_communities()
        fp = open(os.path.join("resource","louvain_communities.pkl"),"rb")
        #print "Pickle written"
    finally:
        communities = pickle.load(fp)
        fp.close()

    communityNodeList = []

    if criterion == "max_size":
        maxSize = len(communities[0])
        maxPos = 0
        for i in range(len(communities)):
            if len(communities[i]) > maxSize:
                maxSize = len(communities[i])
                maxPos = i
        communityNodeList = communities[maxPos]
        #print "Max size node list: "+str(communityNodeList)


    elif criterion == "max_edge_density":
        maxEdgeDensity = 0.0
        maxPos = 0
        for i in range(len(communities)):
            communityEdgeList = edges_in_community(G,communities[i])
            edgeDensity = len(communityEdgeList)*1.0/len(communities[i])
            if edgeDensity > maxEdgeDensity:
                maxEdgeDensity = edgeDensity
                maxPos = i
        communityNodeList = communities[maxPos]
        #print "Max edge density node list: "+str(communityNodeList)

    else:
        print "Criterion not supported"
        return

    print criterion+": nodes: "+str(len(communityNodeList))
    communityAllEdges = edges_in_community(G,communityNodeList)
    print criterion+": edges: "+str(len(communityAllEdges))
    #print communityAllEdges
    fp = open("resource/facebook_"+criterion+".txt","w")
    writeline = ""
    for edge in communityAllEdges:
        writeline += str(edge[0]) + " " + str(edge[1]) + "\n"
    fp.write(writeline)
    fp.close()

    return

#####################################

def edges_in_community (G, communityNodeList):

    #print G.edges()
    communityEdges = []
    for edge in G.edges():
        if edge[0] in communityNodeList and edge[1] in communityNodeList:
            communityEdges.append((edge[0],edge[1]))
    #print communityEdges
    return communityEdges      

#####################################

def validate_communities():
    Gms = nx.read_edgelist("resource/facebook_max_size.txt", nodetype=int)
    Gmed = nx.read_edgelist("resource/facebook_max_edge_density.txt", nodetype=int)
    print "Nodes in max size graph: " + str(Gms.number_of_nodes())
    print "Edges in max size graph: " + str(Gms.number_of_edges())
    print "Nodes in max edge density graph: " + str(Gmed.number_of_nodes())
    print "Edges in max edge density graph: " + str(Gmed.number_of_edges())
    return

#####################################

def main():
    G = nx.read_edgelist("resource/facebook.txt", nodetype=int)
    build_community(G,"max_edge_density")
    build_community(G,"max_size")
    validate_communities()
    return

#####################################

if __name__ == '__main__':
    main()

#####################################

