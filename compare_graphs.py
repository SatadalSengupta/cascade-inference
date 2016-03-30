import os
import infer_graph as IG
import generate_graphs as GG

###################################################

def get_comparison_stats (Gbase, Ginferred):
    
    base_edges = set(Gbase.edges())
    #print Gbase.edges()
    #print base_edges
    inferred_edges = set(Ginferred.edges())

    total_no_of_edges = len(base_edges)
    true_positive = len(base_edges & inferred_edges)
    false_positive = len(inferred_edges - base_edges)
    missed_edges = len(base_edges - inferred_edges)    

    return total_no_of_edges, true_positive, false_positive, missed_edges

###################################################

def compare_graphs (PARAMS):
    
    Gbase, Gcomplete = GG.generate_graphs (PARAMS)
    Ginferred = IG.infer_graph (Gcomplete, PARAMS)

    comparison_stats = {}
    total_no_of_edges, true_positive, false_positive, missed_edges = get_comparison_stats (Gbase, Ginferred)
    comparison_stats['total_edges'] = total_no_of_edges
    comparison_stats['true_positive'] = true_positive
    comparison_stats['true_positive_ratio'] = (true_positive*1.0)/(total_no_of_edges*1.0)
    comparison_stats['false_positive'] = false_positive
    comparison_stats['false_positive_ratio'] = (false_positive*1.0)/(total_no_of_edges*1.0)
    comparison_stats['missed_edges'] = missed_edges
    comparison_stats['missed_edges_ratio'] = (missed_edges*1.0)/(total_no_of_edges*1.0)
    
    return comparison_stats

###################################################

def main():
    compare_graphs()
    return

###################################################

if __name__ == "__main__":
    main()

###################################################
