import os
import generate_graphs as GG
import introduce_content as IC
import random
import run_all_simulations as RAS
#from verbose_display import display
import utilities as util

#########################################

def get_content_level (levels):
    content_level = random.randint(1,levels)
    return content_level

#########################################

def generate_timeline (PARAMS):

    Gfriendship = GG.generate_graphs(PARAMS)

    # EF = []
    content_count = PARAMS['content_count']
    content_levels = PARAMS['content_levels']

    for i in range(content_count):
        content_level = get_content_level(content_levels)
        IC.introduce_content (Gfriendship, content_level, PARAMS)
        #EF.extend(EFlocal)
        #util.display("introduce_all_content", "Current content: "+str(i+1)+" out of "+str(content_count))
        print "Current content: "+str(i+1)+" out of "+str(content_count)
        
    return

#########################################

def main():
    params = RAS.load_parameters_for_test_run()
    Gbase, Gcomplete = GG.generate_graphs(params)
    EF = introduce_all_content (Gcomplete, params)
    # print len(EF)
    return

#########################################

if __name__ == "__main__":
    main()

#########################################
