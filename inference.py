import os
import pickle
import networkx as nx
from datetime import datetime
from utilities import *
import numpy as np
import run_all_simulations as RAS
import random
import sys
###################################################

def get_comparison_stats (Grelevant, Ginferred):

    Ginferred_ud = Ginferred.to_undirected()
    base_edges = set(Grelevant.edges())
    inferred_edges = set(Ginferred_ud.edges())

    total_no_of_edges = len(base_edges)
    true_positive = len(base_edges & inferred_edges)
    false_positive = len(inferred_edges - base_edges)
    missed_edges = len(base_edges - inferred_edges)    

    return total_no_of_edges, true_positive, false_positive, missed_edges

###################################################

def compare_graphs (Grelevant,Ginferred):

    comparison_stats = {}
    total_no_of_edges, true_positive, false_positive, missed_edges = get_comparison_stats (Grelevant, Ginferred)
    comparison_stats['total_edges'] = total_no_of_edges
    comparison_stats['true_positive'] = true_positive
    comparison_stats['true_positive_ratio'] = (true_positive*1.0)/(total_no_of_edges*1.0)
    comparison_stats['false_positive'] = false_positive
    comparison_stats['false_positive_ratio'] = (false_positive*1.0)/(total_no_of_edges*1.0)
    comparison_stats['missed_edges'] = missed_edges
    comparison_stats['missed_edges_ratio'] = (missed_edges*1.0)/(total_no_of_edges*1.0)
   
    return comparison_stats

#################################

def add_to_inferred_graph (Gintermediate, contentTimeline):

    length = len(contentTimeline)
    count = 0

    # Bypass all views before first share
    while (count<length) and (contentTimeline[count][3] == "view"):
        count += 1

    while count<length:

        begin = count
        while (count<length) and (contentTimeline[count][3] == "share"):
            count += 1
        
        latestShare = contentTimeline[random.randint(begin,count-1)]
        while (count<length) and (contentTimeline[count][3] == "view"):
            if Gintermediate.has_edge(latestShare[1],contentTimeline[count][1]):
                Gintermediate[latestShare[1]][contentTimeline[count][1]]['weight'] += 1
            else:
                Gintermediate.add_edge(latestShare[1],contentTimeline[count][1],weight=1)
            count += 1

    return

#################################

def build_intermediate_graph(filename,community,isLatest):

    PARAMS = {}
    tokens = filename.split("_")
    PARAMS["poi_mean"] = float(tokens[2])
    PARAMS["poi_stdv"] = float(tokens[3])
    PARAMS["content_count"] = int(tokens[4])
    PARAMS["vwshprob_mean"] = float(tokens[5])
    PARAMS["vwshprob_stdv"] = float(tokens[6])
    PARAMS["cmlb_view"] = float(tokens[7])
    PARAMS["cmlb_share"] = float(tokens[8].replace(".txt",""))
    PARAMS["compare_with"] = community
    
    relevantNodes = getRelevantNodes(PARAMS)

    Gintermediate = nx.DiGraph()
    #Gintermediate.add_nodes_from(relevantNodes)

    flag = True
    currentContent = "0"
    contentTimeline = []

    with open(os.path.join("timelines",community,filename),"r") as f:
        for line in f:
            tokens = line.rstrip().split(",")
            #timestamp = datetime.strptime(tokens[0],"%Y-%m-%d %H:%M:%S.%f")
            timestamp = datetime.now()
            nodeId = int(tokens[1])
            contentId = tokens[2]
            vworsh = tokens[3]
            if flag:
                currentContent = contentId
                flag = False
            if not (contentId == currentContent):
                flag = True
                add_to_inferred_graph(Gintermediate,contentTimeline)
                contentTimeline = []
            contentTimeline.append((timestamp,nodeId,contentId,vworsh))

    return Gintermediate, PARAMS

#################################

def add_confidence_values(Ginferred):

    for v in Ginferred.nodes():
        wall = 0
        for i in Ginferred.neighbors(v):
            wall += Ginferred[v][i]['weight']
        Ginferred.node[v]['wall'] = wall

    values = []
    for (v,u) in Ginferred.edges():
        Ginferred[v][u]['conf'] = Ginferred[v][u]['weight']*1.0/Ginferred.node[v]['wall']
        values.append(Ginferred[v][u]['conf'])

    Ginferred.graph['mean'] = np.mean(values)
    Ginferred.graph['median'] = np.median(values)

    return

#################################

def filter_on_mean(Ginferred):
    Ginferred_mean = Ginferred.copy()
    for (v,u,d) in Ginferred_mean.edges(data=True):
        if d['conf'] < Ginferred_mean.graph['mean']:
            Ginferred_mean.remove_edge(v,u)
    return Ginferred_mean

#################################

def filter_on_median(Ginferred):
    Ginferred_median = Ginferred.copy()
    for (v,u,d) in Ginferred_median.edges(data=True):
        if d['conf'] < Ginferred_median.graph['median']:
            Ginferred_median.remove_edge(v,u)
    return Ginferred_median

#################################

def infer_graph(Grelevant, filename, community, count):

    Ginferred, PARAMS = build_intermediate_graph(filename,community,True)
    add_confidence_values(Ginferred)
    Ginferred_mean = filter_on_mean(Ginferred)
    Ginferred_median = filter_on_median(Ginferred)
    PARAMS['community'] = community
    fp = open("results_random.txt","a")
    PARAMS['filtered_mean'] = 1
    PARAMS['filtered_median'] = 0
    comparisonStats = compare_graphs(Grelevant,Ginferred_mean)
    RAS.dump_results(fp,PARAMS,comparisonStats,count)
    PARAMS['filtered_mean'] = 0
    PARAMS['filtered_median'] = 1
    comparisonStats = compare_graphs(Grelevant,Ginferred_median)
    RAS.dump_results(fp,PARAMS,comparisonStats,count)

#################################

def main():
    Grelevant = nx.Graph()
    Grelevant.add_edge(0,1)
    infer_graph(Grelevant, "event_timeline_0.148_0.079_500_0.5_0.15_0.3_0.3.txt", "MaxSize", (0,1))
    return

#################################

if __name__ == "__main__":
    main()

#################################
