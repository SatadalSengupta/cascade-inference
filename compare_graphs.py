import os
import simulation_properties as SP
import infer_graph as IG
import generate_graphs as GG

###################################################

def get_comparison_stats (Gbase, Gcomplete):

    return

###################################################

def compare_graphs ():
    
    Gbase, Gcomplete = GG.generate_graphs (SP.SAMPLE_SIZE, SP.MEAN, SP.SD, SP.VIEW_BOOST, SP.SHARE_BOOST)
    Ginferred = IG.infer_graph (Gcomplete, SP.RUN_COUNT)
    get_comparison_stats (Gbase, Ginferred)
    
    return

###################################################

def main():
    compare_graphs()
    return

###################################################

if __name__ == "__main__":
    main()

###################################################
