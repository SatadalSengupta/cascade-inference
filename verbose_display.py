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

def main():
    display("Hello World")
    return

##################################################

if __name__ == "__main__":
    main()

##################################################
