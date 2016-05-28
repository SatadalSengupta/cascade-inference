import os
import inference as IF
import utilities as util
import networkx as nx
import timeit

#################################

def generate_all_results():

    Grelevant = nx.read_edgelist(os.path.join("resource","facebook.txt"), nodetype=int)

    for community in ["MaxSize","MaxEdgeDensity"]:
        print "Starting for community: "+community
        PARAMS = {}
        PARAMS['compare_with'] = community
        relevantNodes = util.getRelevantNodes(PARAMS)
        for node in Grelevant.nodes():
            if node not in relevantNodes:
                Grelevant.remove_node(node)
        path = os.path.join("timelines",community)
        allFiles = os.listdir(path)
        i = 1
        for f in allFiles:
            start_time = timeit.default_timer()
            IF.infer_graph(Grelevant,f,community,(i,len(allFiles)))
            elapsed = timeit.default_timer() - start_time
            print "   Graph inferred for file "+str(i)+" of "+str(len(allFiles))+"; Elapsed time = "+str(elapsed)
            i += 1

#################################

def main():
    generate_all_results()
    return

##################################

if __name__ == "__main__":
    main()
