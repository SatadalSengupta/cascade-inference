import networkx as nx
import matplotlib.pyplot as plt
import math,random
import collections
from ast import literal_eval

##################################################################################################################
#Global variable declaration
#We can change various parameters in global declaration for testing 
x=1.30
y=1.15
z=1
contentpop=0
no_of_nodes=20
viewthresh=0.5
sharethresh=0.35
connection_probability=0.1
filtering_parameter=1#parameter is use to filter edges whose weight is greater than filtering parameter
no_of_source_nodes=5#no of nodes in graph where information is introduce
G=nx.complete_graph(20)
randomG=nx.gnp_random_graph(no_of_nodes,connection_probability)

#initial random graph
K=nx.DiGraph()#Inferenced graph from initial random graph
L=nx.DiGraph()#Inferenced graph is filtered using filtering parameter to create Filtered graph
M=nx.Graph() 
myList=[]#myList holds all the DFS trees
edgelist=[]#Edgelist holds all the edges of each tree return by DFS algorithm
weightlist=[]#weightlist holds all the weight of each edge return by DFS algorithm
com=[]#com holds list of tuples ((A,B,weight),(A,B,weight)....) where A and B is edge and weight is weight of edge (A,B)
Pview=[]
###################################################################################################################
#Generation of random graph 
#no_of_nodes contain number of nodes 
#connection probability contains probability of edge between two nodes

def Graph():
#Assigning viewing probability to each node
    temp=[]
    for n in range(0, no_of_nodes):
        for m in range(0, no_of_nodes):
            temp.append(random.random())
        G.node[n]['Pview']=temp
        temp=[]

#Assigning sharing probability to each node
    for n in range(0, no_of_nodes):
        for m in range(0, no_of_nodes):
            temp.append(random.random())
        G.node[n]['Pshare']=temp
        temp=[]
    
    for e in G.edges():
        if randomG.has_edge(*e):
           G.node[e[0]]['Pview'][e[1]]=(G.node[e[0]]['Pview'][e[1]])*x
           G.node[e[0]]['Pshare'][e[1]]=(G.node[e[0]]['Pshare'][e[1]])*x
           G.node[e[1]]['Pview'][e[0]]=(G.node[e[1]]['Pview'][e[0]])*x
           G.node[e[1]]['Pshare'][e[0]]=(G.node[e[1]]['Pshare'][e[0]])*x

          

#drawing above constructed graph
#nx.draw(G, with_labels=True)
#plt.show()

#####################################################################################################################

#DFS algo for single source node
def dfs_tree(G, source):
     
    T = nx.DiGraph()
    if source is None:
        T.add_nodes_from(G)
    else:
        T.add_node(source)
    T.add_edges_from(dfs_edges(G,source))
    return T


def dfs_edges(G, source=None):

    
    if source is None:
          nodes = G
    else:
        nodes = [source]
    visited=set()
    for start in nodes:
        if start in visited:
            continue
        visited.add(start)
        stack = [(start,iter(G[start]))]
        while stack:
            parent,children = stack[-1]
            try:
                child = next(children)

                if contentpop==1:
                   if child not in visited and ((G.node[child]['Pview'][parent]*x)>viewthresh and (G.node[child]['Pshare'][parent]*x)>sharethresh):
                      yield parent,child
                      visited.add(child)
                      stack.append((child,iter(G[child])))

                if contentpop==2:
                   if child not in visited and ((G.node[child]['Pview'][parent]*y)>viewthresh and (G.node[child]['Pshare'][parent]*y)>sharethresh):
                      yield parent,child
                      visited.add(child)
                      stack.append((child,iter(G[child])))

                if contentpop==3:
                   if child not in visited and (G.node[child]['Pview'][parent]*z>viewthresh and G.node[child]['Pshare'][parent]*z>sharethresh):
                      yield parent,child
                      visited.add(child)
                      stack.append((child,iter(G[child])))
            except StopIteration:
                stack.pop()

#########################################################################################################################################

#This function calls DFS tree algorithm 
#myList holds all the DFS trees return by DFS tree algorithm
def treecollection():
    for i in range(no_of_source_nodes): #taking random source nodes
        n=random.randint(1, (no_of_nodes-1))
        global contentpop
        contentpop=random.randint(1,3);
        myList.append(dfs_tree(G, n))#appending trees to mylist
        #nx.draw(myList[i], with_labels=True)#printing generated dfs tree
        #plt.show()

##########################################################################################################################################

def processedges():
    global edgelist,weightlist,com
    for i in range(no_of_source_nodes):#This loop executes for each tree i.e each source node
        edgelist.extend(nx.edges(myList[i]))#Adds edges of each tree to edgelist array, now edgelist holds all the edges
    
    counter=collections.Counter(edgelist)#Extracting frequencies of each edge, now counter holds each edge with its frequency or weight

    #Seperating edge and its weight because they are not in desired format ((A,B,weight),(A,B,weight)....)
    edgelist=counter.keys()#Holds edge
    weightlist=counter.values()#holds weight 
    a, b = map(list, zip(*edgelist))
    #Combining edge and its weight in desired format ((A,B,weight),(A,B,weight)....)
    com=zip(a,b,weightlist)#com array holds each edge and its weight

###########################################################################################################################################

#Creating new inference graph by combing all trees
def inference():
    K.add_weighted_edges_from(com)#K is new infered weighted graph where edges are added from com array
    #nx.draw(K, with_labels=True)
    #plt.show()

##########################################################################################################################################

#Filter Module
def filtermodule():
    temp=[t for t in com if t[2]>filtering_parameter]
    L.add_weighted_edges_from(temp)
    #nx.draw(L, with_labels=True)
    #plt.show()


##########################################################################################################################################

def comparemodule():

    presentL=0
    absentL=0
    for e in L.edges():
        if randomG.has_edge(*e):
           presentL=presentL+1
        else:
           absentL=absentL+1
    #print presentL,absentL

    presentK=0
    absentK=0
    for e in K.edges():
        if randomG.has_edge(*e):
           presentK=presentK+1
        else:
           absentK=absentK+1
    #print presentK,absentK

    edges_in_first_graph=G.number_of_edges()
    edges_in_random_graph=randomG.number_of_edges()
    edges_in_infered_graph=K.number_of_edges()
    edges_in_infered_filtered_graph=L.number_of_edges()
    

    nodes_in_first_graph=G.number_of_nodes()
    nodes_in_random_graph=randomG.number_of_nodes()
    nodes_in_infered_graph=K.number_of_nodes()
    nodes_in_filtered_graph=L.number_of_nodes()

    print "Number of edges in complete graph: ", edges_in_first_graph
    print "Number of edges in random graph: ", edges_in_random_graph
    print "Number of edges in inferred graph before filtering: ", edges_in_infered_graph
    print "Number of edges in inferred graph after filtering: ", edges_in_infered_filtered_graph

    print "Number of nodes in complete graph: ", nodes_in_first_graph
    print "Number of nodes in random graph: ", nodes_in_random_graph
    print "Number of nodes in inferred graph: ", nodes_in_infered_graph
    print "Number of nodes in inferred graph after filtering: ", nodes_in_filtered_graph

    print "Number of edges in inferred graph which are present in original graph: ", presentK
    print "Number of edges in inferred graph which are not present in original graph: ", absentK
    print "Number of edges in inferred filtered graph which are present in original graph: ", presentL
    print "Number of edges in inferred filtered graph which are not present in original graph: ", absentK

##########################################################################################################################################

def main():
    Graph()
    treecollection()
    processedges()
    inference()
    filtermodule()
    comparemodule()
    
##########################################################################################################################################

if __name__ == '__main__':
    main()
