import os
import simulation_properties as SP
import generate_graphs as GG
import networkx as nx
import random

######################################################

def introduce_for_node (node_id, content_level):

    ET = nx.Graph()

    #print "Node ID: "+str(node_id) + "; Content Level: "+str(content_level)

    return ET

######################################################

def get_points_of_intro (Gcomplete, no_of_points):

    print "No. of points of introduction: "+str(no_of_points)
    points_of_intro = []
    
    for i in range(no_of_points):
        points_of_intro.append(random.randint(0,Gcomplete.number_of_nodes()-1))
    
    return points_of_intro

######################################################

def introduce_content (Gcomplete, content_level):

    EFlocal = []
    points_of_intro = get_points_of_intro (Gcomplete, random.randint(1,Gcomplete.number_of_nodes()))
    
    for point in points_of_intro:
        ET = introduce_for_node (point, content_level)
        EFlocal.append(ET)

    return EFlocal

######################################################

def main():
    Gbase, Gcomplete = GG.generate_graphs (SP.SAMPLE_SIZE, SP.MEAN, SP.SD, SP.VIEW_BOOST, SP.SHARE_BOOST)
    EFlocal = introduce_content (Gcomplete, random.randint(1,3))
    return

######################################################

if __name__ == "__main__":
    main()

######################################################
