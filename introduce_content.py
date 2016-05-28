import os
import generate_graphs as GG
import utilities as util
import networkx as nx
import random
from collections import defaultdict, deque
import run_all_simulations as RAS
import datetime
import timeit

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
    view_prob = G.node[child]['Pview'][parent]
    view_boost, share_boost = get_content_boost(content_level)
    view_prob *= (1.0 + view_boost)
    view_prob = view_prob if view_prob < 1.0 else 1.0
    return view_prob

######################################################

def get_share_prob (G, child, parent, content_level):
    share_prob = G.node[child]['Pshare'][parent]
    view_boost, share_boost = get_content_boost(content_level)
    share_prob *= (1.0 + share_boost)
    share_prob = share_prob if share_prob < 1.0 else 1.0
    return share_prob

######################################################

def introduce_for_node (G, node_id, content_level, content_id, relevantNodes):

    #start_time = timeit.default_timer()
    source = node_id
    visited = set([source])
    next_sources = set([source])
    if source in relevantNodes:
        util.logEvent(PARAMS,source,content_id,False)

    while True:
        
        if not next_sources:
            break
        
        current_sources = next_sources
        next_sources = set()
        viewed = set()
        
        for source in current_sources:
            neighbors = set([n for n in G.neighbors(source) if n not in visited])
            for neighbor in neighbors:
                view_prob = get_view_prob(G, neighbor, source, content_level)
                if should_child_view(view_prob):
                    if neighbor in relevantNodes:
                        util.logEvent(PARAMS,neighbor,content_id,True)
                    visited.add(neighbor)
                    viewed.add(neighbor)
            for neighbor in viewed:
                share_prob = get_share_prob(G, neighbor, source, content_level)
                if should_child_share(share_prob):
                    if neighbor in relevantNodes:
                        util.logEvent(PARAMS,neighbor,content_id,False)
                    next_sources.add(neighbor)
            viewed = set()

    #elapsed = timeit.default_timer() - start_time
    #print("Elapsed time: "+str(elapsed))

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
    #print (Gfriendship.number_of_nodes())
    points_of_intro = get_points_of_intro (Gfriendship, get_no_of_points_of_intro(Gfriendship.number_of_nodes()))
    #print ("No. of points of introduction: "+str(len(points_of_intro)))
    #print ("Ratio: "+str(len(points_of_intro)*1.0/Gfriendship.number_of_nodes()))
    points_of_intro = points_of_intro[0:1]

    contentId = datetime.datetime.now().strftime('%Y%m%d%H%M%S%f')
    count = 0
    for point in points_of_intro:
        #print ("Introducing for point no.: "+str(count+1)+" of "+str(len(points_of_intro)))
        introduce_for_node (Gfriendship, point, contentLevel, contentId, PARAMS['relevant_nodes'])
        count += 1
        #util.display("introduce_content", "Current POI count: "+str(count)+" out of "+str(len(points_of_intro)))

    return

######################################################

def main():
    Gfriendship = GG.generate_graphs (RAS.load_parameters_for_test_run())
    introduce_content (Gfriendship, random.randint(1,3), RAS.load_parameters_for_test_run())
    # print EFlocal
    return

######################################################

if __name__ == "__main__":
    main()

######################################################
