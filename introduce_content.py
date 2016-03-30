import os
import generate_graphs as GG
from verbose_display import display
import networkx as nx
import random
from collections import defaultdict, deque

######################################################

PARAMS = {}

######################################################

def get_content_boost (content_level):

    view_boost = PARAMS['cmlb_view'] + (0.2*(content_level-1))
    share_boost = PARAMS['cmlb_share'] + (0.2*(content_level-1))
   
    return view_boost, share_boost

######################################################

def should_child_view (view_prob):
    result = True if random.random() <= view_prob else False
    return result

######################################################

def should_child_share (share_prob):
    result = True if random.random() <= share_prob else False
    return result

######################################################

def get_view_prob (G, child, parent, not_viewed, content_level):
    
    display("\nVIEW:: Node is "+str(child))

    view_prob = G.node[child]['Pview'][parent]
    display("VIEW:: Initial value: "+str(view_prob))

    for node in not_viewed:
        view_prob *= (1.0 - G.node[child]['Pview'][node])
        display("VIEW:: Value now: "+str(view_prob)+" for source node "+str(node))

    view_boost, share_boost = get_content_boost(content_level)
    view_prob *= (1.0 + view_boost)
    display("VIEW:: Final value after content boost: "+str(view_prob))

    view_prob = view_prob if view_prob < 1.0 else 1.0

    return view_prob

######################################################

def get_share_prob (G, child, parent, not_shared, content_level):

    display("\nSHARE:: Node is: "+str(child))
    
    share_prob = G.node[child]['Pshare'][parent]
    display("SHARE:: Initial value: "+str(share_prob))

    for node in not_shared:
        share_prob *= (1.0 - G.node[child]['Pshare'][node])
        display("SHARE:: Value now: "+str(share_prob)+" for source node "+str(node))

    view_boost, share_boost = get_content_boost(content_level)
    share_prob *= (1.0 + share_boost)
    display("SHARE:: Final value after content boost: "+str(share_prob))

    share_prob = share_prob if share_prob < 1.0 else 1.0

    return share_prob

######################################################

def introduce_for_node (Gcomplete, node_id, content_level):

    #ET = bfs_tree (Gcomplete, node_id, content_level)
    ET = nx.DiGraph()
    G = Gcomplete
    source = node_id
    ET.add_node(source)
    visited = []
    visited.append(source)
    not_viewed_for = {i: [] for i in range(G.number_of_nodes())}
    not_shared_for = {i: [] for i in range(G.number_of_nodes())}
    next_sources = []
    next_sources.append(source)

    while True:
        
        if len(next_sources) == 0:
            break
        
        current_sources = [i for i in next_sources]
        next_sources = []
        display("\n\nSources for this iteration: "+str(current_sources))
        
        for source in current_sources:
            display("\nCurrent source: "+str(source))
            neighbors = [n for n in G.neighbors(source) if n not in visited]
            display("Neighbors: "+str(neighbors))
            
            for neighbor in neighbors:
                view_prob = get_view_prob(G, neighbor, source, not_viewed_for[neighbor], content_level)

                if should_child_view(view_prob):
                    ET.add_edge(source,neighbor)
                    visited.append(neighbor)
                    display("Viewed for "+str(neighbor)+" with prob "+str(view_prob))
    
                    share_prob = get_share_prob(G, neighbor, source, not_shared_for[neighbor], content_level)

                    if should_child_share(share_prob):
                        next_sources.append(neighbor)
                        display("Shared for "+str(neighbor)+" with prob "+str(share_prob))
                    else:
                        not_shared_for[neighbor].append(source)
                        display("Not shared for "+str(neighbor)+" with prob "+str(share_prob))

                else:
                    not_viewed_for[neighbor].append(source)
                    not_shared_for[neighbor].append(source)
                    display("Not viewed for "+str(neighbor)+" with prob "+str(view_prob))

    return ET

######################################################

def get_next_point_of_intro (size):
    #return 0
    return random.randint(0,size-1)

######################################################

def get_points_of_intro (Gcomplete, no_of_points):

    display("No. of points of introduction: "+str(no_of_points))
    points_of_intro = []
    
    for i in range(no_of_points):
        points_of_intro.append(get_next_point_of_intro(Gcomplete.number_of_nodes()))
    display("Points of introduction: "+str(points_of_intro))   
 
    return points_of_intro

######################################################

def get_no_of_points_of_intro (size):
    
    #return 1
    return int(random.gauss (size*PARAMS['poi_mean'], size*PARAMS['poi_stdv']))

######################################################

def introduce_content (Gcomplete, content_level, parameters):

    EFlocal = []
    global PARAMS
    PARAMS = parameters
    points_of_intro = get_points_of_intro (Gcomplete, get_no_of_points_of_intro(Gcomplete.number_of_nodes()))
    
    for point in points_of_intro:
        ET = introduce_for_node (Gcomplete, point, content_level)
        EFlocal.append(ET)

    #display("\n\n"+str(EFlocal[0].edge))

    return EFlocal

######################################################

def main():
    #Gbase, Gcomplete = GG.generate_graphs (SP.SAMPLE_SIZE, SP.MEAN, SP.SD, SP.VIEW_BOOST, SP.SHARE_BOOST)
    #EFlocal = introduce_content (Gcomplete, random.randint(1,3))
    return

######################################################

if __name__ == "__main__":
    main()

######################################################
