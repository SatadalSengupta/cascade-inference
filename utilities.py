import os
import simulation_properties as SP
from datetime import datetime as dt
import pickle

##################################################

def display(fnc,text):
    
    if SP.VERBOSE:
        log_path = os.path.join(SP.CWD,"log.txt")
        fp = open(log_path,"a")
        fmt = "{0} : {1: <25} : {2}"
        writeline = fmt.format(str(dt.now())[:19],fnc[:25],text)
        fp.write(writeline+"\n")
        fp.close()

    return

##################################################

def clearEventLog():
    os.remove(os.path.join("resource","event_timeline.txt"))

##################################################

def build_event_string(PARAMS):
    event_string = "_"
    event_string += str(PARAMS["poi_mean"])+"_"
    event_string += str(PARAMS["poi_stdv"])+"_"
    event_string += str(PARAMS["content_count"])+"_"
    event_string += str(PARAMS["vwshprob_mean"])+"_"
    event_string += str(PARAMS["vwshprob_stdv"])+"_"
    event_string += str(PARAMS["cmlb_view"])+"_"
    event_string += str(PARAMS["cmlb_share"])
    return event_string

##################################################

def isNodeRelevant (node_id):
    isNodeRelevant = False
    fbMaxEdgeDensityNodes = pickle.load(open(os.path.join("resource","facebook_max_edge_density.nodes"),"rb"))
    fbMaxSizeNodes = pickle.load(open(os.path.join("resource","facebook_max_size.nodes"),"rb"))
    if (node_id in fbMaxEdgeDensityNodes) or (node_id in fbMaxSizeNodes):
        isNodeRelevant = True
    return isNodeRelevant

##################################################

def getRelevantNodes():
    fbMaxEdgeDensityNodes = pickle.load(open(os.path.join("resource","facebook_max_edge_density.nodes"),"rb"))
    fbMaxSizeNodes = pickle.load(open(os.path.join("resource","facebook_max_size.nodes"),"rb"))
    relevantNodes = []
    for n in fbMaxSizeNodes:
        relevantNodes.append(n)
    for n in fbMaxEdgeDensityNodes:
        relevantNodes.append(n)
    return relevantNodes

##################################################

def logEvent (PARAMS, node_id, content_id, isView):
    
    fp = PARAMS["event_timeline_file"]
    time = dt.now()
    fp.write(str(time))
    fp.write(",")
    fp.write(str(node_id))
    fp.write(",")
    fp.write(str(content_id))
    fp.write(",")
    if isView:
        fp.write("view")
    else:
        fp.write("share")
    fp.write("\n")

##################################################

def main():
    #display("Hello World")
    logEvent("12345")
    logEvent("234")
    for i in range(10):
        logEvent(str(i))
    return

##################################################

if __name__ == "__main__":
    main()

##################################################
