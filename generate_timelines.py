import os
import generate_graphs as GG
import introduce_content as IC
import random
import run_all_simulations as RAS
#from verbose_display import display
import utilities as util
import timeit
from datetime import datetime

#########################################

def get_content_level (levels):
    content_level = random.randint(1,levels)
    return content_level

#########################################

def generate_timeline (PARAMS):

    start_time = timeit.default_timer()
    event_string = util.build_event_string(PARAMS)
    PARAMS['event_string'] = event_string
    time = datetime.now().strftime("%Y%m%d-%H%M%S-%f-")
    fp = open(os.path.join("timelines",PARAMS['compare_with'],time+"event_timeline"+event_string+".txt"),"wb")
    PARAMS['event_timeline_file'] = fp

    Gfriendship = GG.generate_graphs(PARAMS)
    content_count = PARAMS['content_count']
    content_levels = PARAMS['content_levels']

    for i in range(content_count):
        content_level = get_content_level(content_levels)
        IC.introduce_content (Gfriendship, content_level, PARAMS)
        elapsed = timeit.default_timer() - start_time
        if (i+1)%(content_count/5)==0:
            print "   Current content: "+str(i+1)+" out of "+str(content_count)+"; Elapsed Time: "+str(elapsed)
            start_time = timeit.default_timer()
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
