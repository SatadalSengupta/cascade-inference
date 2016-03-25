import os
import simulation_properties as SP
import introduce_all_content as IAC

############################################

def combine_event_forests (event_forests):

    return Gintermediate_digraph

############################################

def impose_weight_restriction (Gintermediate_digraph, weight_threshold):

    return Gintermediate_filtered

############################################

def get_undirected_graph (Gintermediate_filtered):

    return Gintermediate

############################################

def infer_graph (Gcomplete, run_count):

    event_forests = []
    
    for i in range(run_count):
        event_forest = IAC.introduce_all_content (Gcomplete, SP.CONTENT_COUNT)
        event_forests.append (event_forest)

    Gintermediate_digraph = combine_event_forests (event_forests)
    Gintermediate_filtered = impose_weight_restriction (Gintermediate_digraph, SP.WEIGHT_THRESHOLD)
    Gintermediate = get_undirected_graph (Gintermediate_filtered)
    
    return Gintermediate        

############################################

def main():
    Ginferred = infer_graph (Gcomplete, SP.RUN_COUNT)
    return

############################################

if __name__ == "__main__":
    main()
