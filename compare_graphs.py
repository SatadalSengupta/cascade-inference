import os
import simulation_properties as SP
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

def compare_graphs ():
    
    Gbase, Gcomplete = GG.generate_graphs (SP.SAMPLE_SIZE, SP.MEAN, SP.SD, SP.VIEW_BOOST, SP.SHARE_BOOST)
    Ginferred = IG.infer_graph (Gcomplete, SP.RUN_COUNT)
    total_no_of_edges, true_positive, false_positive, missed_edges = get_comparison_stats (Gbase, Ginferred)
    print "Total edges: "+str(total_no_of_edges)
    print "True positive: "+str(true_positive)+"; Ratio: "+str(true_positive*1.0 / total_no_of_edges*1.0)
    print "False positive: "+str(false_positive)+"; Ratio: "+str(false_positive*1.0 / total_no_of_edges*1.0)
    print "Missed edges: "+str(missed_edges)
    
    return

###################################################

def main():
    compare_graphs()
    return

###################################################

if __name__ == "__main__":
    main()

###################################################
