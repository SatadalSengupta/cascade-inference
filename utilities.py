import os
import simulation_properties as SP
from datetime import datetime as dt

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

def logEvent (content_id, isView):

    with open(os.path.join("resource","event_timeline.txt"), "a") as fp:
        time = dt.now()
        fp.write(str(time))
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
