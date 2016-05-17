import os
import generate_graphs as GG
import utilities as util
import networkx as nx
import random
from collections import defaultdict, deque
import run_all_simulations as RAS

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

def get_view_prob (G, child, parent, content_level):
    
    # display("get_view_prob","VIEW:: Node is "+str(child))

    view_prob = G.node[child]['Pview'][parent]
    # display("get_view_prob", "VIEW:: Initial value: "+str(view_prob))

    #for node in not_viewed:
    #    view_prob *= (1.0 - G.node[child]['Pview'][node])
        # display("get_view_prob", "VIEW:: Value now: "+str(view_prob)+" for source node "+str(node))

    view_boost, share_boost = get_content_boost(content_level)
    view_prob *= (1.0 + view_boost)
    # display("get_view_prob", "VIEW:: Final value after content boost: "+str(view_prob))

    view_prob = view_prob if view_prob < 1.0 else 1.0

    return view_prob

######################################################

def get_share_prob (G, child, parent, content_level):

    # display("get_share_prob","SHARE:: Node is: "+str(child))
    
    share_prob = G.node[child]['Pshare'][parent]
    # display("get_share_prob", "SHARE:: Initial value: "+str(share_prob))

    #for node in not_shared:
    #    share_prob *= (1.0 - G.node[child]['Pshare'][node])
        # display("get_share_prob", "SHARE:: Value now: "+str(share_prob)+" for source node "+str(node))

    view_boost, share_boost = get_content_boost(content_level)
    share_prob *= (1.0 + share_boost)
    # display("get_share_prob", "SHARE:: Final value after content boost: "+str(share_prob))

    share_prob = share_prob if share_prob < 1.0 else 1.0

    return share_prob

######################################################

def introduce_for_node (G, node_id, content_level, content_id):

    # G: Friendship graph
    #contentId = get_content_id(content_level)
    source = node_id
    visited = []
    visited.append(source)
    #not_viewed_for = {i: [] for i in range(G.number_of_nodes())}
    #not_shared_for = {i: [] for i in range(G.number_of_nodes())}
    next_sources = []
    next_sources.append(source)

    while True:
        
        if len(next_sources) == 0:
            break
        
        current_sources = [i for i in next_sources]
        next_sources = []
        # display("introduce_for_node", "Sources for this iteration: "+str(current_sources))
        
        for source in current_sources:
            # display("introduce_for_node","Current source: "+str(source))
            neighbors = [n for n in G.neighbors(source) if n not in visited]
            # display("introduce_for_node", "Neighbors: "+str(neighbors))
            
            for neighbor in neighbors:
                view_prob = get_view_prob(G, neighbor, source, content_level)

                if should_child_view(view_prob):
                    #ET.add_edge(source,neighbor)
                    util.logEvent(contentId,True)
                    visited.append(neighbor)
                    # display("introduce_for_node", "Viewed for "+str(neighbor)+" with prob "+str(view_prob))
    
                    share_prob = get_share_prob(G, neighbor, source, content_level)

                    if should_child_share(share_prob):
                        util.logEvent(contentId,False)
                        next_sources.append(neighbor)
                        # display("introduce_for_node", "Shared for "+str(neighbor)+" with prob "+str(share_prob))
                    #else:
                        #not_shared_for[neighbor].append(source)
                        # display("introduce_for_node", "Not shared for "+str(neighbor)+" with prob "+str(share_prob))

                #else:
                    #not_viewed_for[neighbor].append(source)
                    #not_shared_for[neighbor].append(source)
                    # display("introduce_for_node", "Not viewed for "+str(neighbor)+" with prob "+str(view_prob))

    return

######################################################

def get_next_point_of_intro (size):
    #return 0
    return random.randint(0,size-1)

######################################################

def get_points_of_intro (Gfriendship, no_of_points):

    #util.display("get_points_of_intro","No. of points of introduction: "+str(no_of_points))
    points_of_intro = []
    
    for i in range(no_of_points):
        points_of_intro.append(get_next_point_of_intro(Gfriendship.number_of_nodes()))
    # display("get_points_of_intro", "Points of introduction: "+str(points_of_intro))   
 
    return points_of_intro

######################################################

def get_no_of_points_of_intro (size):
    
    #return 1
    return int(random.gauss (size*PARAMS['poi_mean'], size*PARAMS['poi_stdv']))

######################################################

def introduce_content (Gfriendship, contentLevel, parameters):   

    global PARAMS
    PARAMS = parameters
    points_of_intro = get_points_of_intro (Gfriendship, get_no_of_points_of_intro(Gfriendship.number_of_nodes()))

    contentId = datetime.datetime.now().strftime('%Y%m%d%H%M%S%f')
    count = 0
    for point in points_of_intro:
        introduce_for_node (Gfriendship, point, contentLevel, contentId)
        count += 1
        #util.display("introduce_content", "Current POI count: "+str(count)+" out of "+str(len(points_of_intro)))

    return

######################################################

def main():
    Gbase, Gcomplete = GG.generate_graphs (RAS.load_parameters_for_test_run())
    introduce_content (Gcomplete, random.randint(1,3), RAS.load_parameters_for_test_run())
    # print EFlocal
    return

######################################################

if __name__ == "__main__":
    main()

######################################################
