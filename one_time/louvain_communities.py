import community
import networkx as nx
import matplotlib.pyplot as plt

#better with karate_graph() as defined in networkx example.
#erdos renyi don't have true community structure
G = nx.read_edgelist("facebook.txt",nodetype=int)

#first compute the best partition
partition = community.best_partition(G)

#drawing
size = float(len(set(partition.values())))
#print size
pos = nx.spring_layout(G)
count = 0.
for com in set(partition.values()) :
    count = count + 1.
    list_nodes = [nodes for nodes in partition.keys()
                                if partition[nodes] == com]
    edge_count = 0
    for edge in G.edges():
        if edge[0] in list_nodes and edge[1] in list_nodes:
            edge_count += 1
    print "Size of community "+str(count)+": "+str(len(list_nodes))+"; no. of edges = "+str(edge_count)+"; edge density = "+str(edge_count*1.0/len(list_nodes))
    #nx.draw_networkx_nodes(G, pos, list_nodes, node_size = 20, node_color = str(count / size))


#nx.draw_networkx_edges(G,pos, alpha=0.5)
#plt.savefig("louvain_result.png")
