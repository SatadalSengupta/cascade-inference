import generate_timelines as GT
import simulation_properties as SP
import numpy as np
import os
from datetime import datetime
from utilities import *
import timeit

############################################################

def load_parameters_for_test_run():

    PARAMS, ALLVAR, STATVAR = load_all_properties()
    PARAMS = load_default_properties(PARAMS)
    PARAMS['relevant_nodes'] = getRelevantNodes(PARAMS)
    PARAMS['event_string'] = build_event_string(PARAMS)
    fp = open(os.path.join("timelines","event_timeline"+PARAMS['event_string']+".txt"),"wb")
    PARAMS['event_timeline_file'] = fp
    #display("load_parameters_for_test_run", "Parameters loaded for test run.")

    return PARAMS

############################################################

def load_all_properties():

    # Build the all-important parameter dictionary

    PARAMS = {}
    ALLVAR = {}
    STATVAR = {}

    # Load static properties first

    PARAMS['verbose'] = SP.VERBOSE
    PARAMS['dataset'] = SP.DATASET
    #PARAMS['sampled_dataset'] = SP.SAMPLED_DATASET
    PARAMS['run_count'] = SP.RUN_COUNT
    PARAMS['content_levels'] = SP.CONTENT_LEVELS
    PARAMS['poi_mean'] = SP.POI_MEAN
    PARAMS['poi_stdv'] = SP.POI_STDV
     
    # Load all-variable properties in a different dictionary for now
    
    #ALLVAR['sampling_technique'] = SP.SAMPLING_TECHNIQUE

    # Load variable-while-others-static properties in a different dictionary for now

    #STATVAR['sample_size'] = SP.SAMPLE_SIZE
    STATVAR['content_count'] = SP.CONTENT_COUNT
    STATVAR['vwshprob_mean'] = SP.VWSHPROB_MEAN
    STATVAR['vwshprob_stdv'] = SP.VWSHPROB_STDV
    #STATVAR['view_boost'] = SP.VIEW_BOOST
    #STATVAR['share_boost'] = SP.SHARE_BOOST
    #STATVAR['weight_threshold'] = SP.WEIGHT_THRESHOLD
    STATVAR['cmlb_view'] = SP.CONTENT_MINLVL_BOOST_VIEW
    STATVAR['cmlb_share'] = SP.CONTENT_MINLVL_BOOST_SHARE

    # Comparison parameters
    #STATVAR['compare_with'] = SP.COMPARE_WITH
    #STATVAR['threshold'] = SP.THRESHOLD

    return PARAMS, ALLVAR, STATVAR

############################################################

def load_default_properties(PARAMS):

    #PARAMS['sampling_technique'] = SP.SAMPLING_TECHNIQUE[0]
    #PARAMS['sample_size'] = SP.SAMPLE_SIZE[3]
    PARAMS['content_count'] = SP.CONTENT_COUNT[3]
    PARAMS['vwshprob_mean'] = SP.VWSHPROB_MEAN[3]
    PARAMS['vwshprob_stdv'] = SP.VWSHPROB_STDV[3]
    #PARAMS['view_boost'] = SP.VIEW_BOOST[3]
    #PARAMS['share_boost'] = SP.SHARE_BOOST[3]
    #PARAMS['weight_threshold'] = SP.WEIGHT_THRESHOLD[3]
    PARAMS['cmlb_view'] = SP.CONTENT_MINLVL_BOOST_VIEW[3]
    PARAMS['cmlb_share'] = SP.CONTENT_MINLVL_BOOST_SHARE[3]
    #PARAMS['compare_with'] = SP.COMPARE_WITH[0]
    #PARAMS['threshold'] = SP.THRESHOLD[3]

    return PARAMS 

############################################################

def dump_results (fp, PARAMS, comparison_stats, count):

    fmt = '{0:50} = {1}\n'
    writeline = ""
    writeline += "RUN " + str(count[0]) + " OUT OF " + str(count[1]) + " AT TIME: " + str(datetime.now()) + "\n\n"
    writeline += fmt.format("Community", PARAMS['community'])
    writeline += fmt.format("Content count", str(PARAMS['content_count']))
    writeline += fmt.format("View share probability mean", str(PARAMS['vwshprob_mean']))
    writeline += fmt.format("View share probability standard deviation", str(PARAMS['vwshprob_stdv']))
    writeline += fmt.format("Content minimum level view probability boost", str(PARAMS['cmlb_view']))
    writeline += fmt.format("Content minimum level share probability boost", str(PARAMS['cmlb_share']))
    writeline += fmt.format("Filtered on basis of mean", str(PARAMS['filtered_mean']))
    writeline += fmt.format("Filtered on basis of median", str(PARAMS['filtered_median']))
    writeline += "\n"
    writeline += fmt.format("Total number of edges", str(comparison_stats['total_edges']))
    writeline += fmt.format("True positive", str(comparison_stats['true_positive']))
    writeline += fmt.format("True positive ratio", str(comparison_stats['true_positive_ratio']))
    writeline += fmt.format("False positive", str(comparison_stats['false_positive']))
    writeline += fmt.format("False positive ratio", str(comparison_stats['false_positive_ratio']))
    writeline += fmt.format("Missed edges", str(comparison_stats['missed_edges']))
    writeline += fmt.format("Missed edges ratio", str(comparison_stats['missed_edges_ratio']))
    writeline += "\n\n"
    fp.write(writeline)
    fp.flush()

    return
    
############################################################

def generate_all_timelines ():

    #fp = open(os.path.join("/home/satadal/Workspaces/Projects/Social.Caching/Code","all_results_"+str(sequence_number)+".txt"),"w")
    count = 0    
    totalCount = 226

    PARAMS, ALLVAR, STATVAR = load_all_properties()
    
    # Prepare the property set for current simulation run

    for comparisonCriterion in SP.COMPARE_WITH:

	print "Starting for comparison criterion: "+comparisonCriterion
        PARAMS['compare_with'] = comparisonCriterion
        PARAMS = load_default_properties(PARAMS)
        PARAMS['relevant_nodes'] = getRelevantNodes(PARAMS)

        # Variation for content count
        start = STATVAR['content_count'][0]
        stop = STATVAR['content_count'][1]
        step = STATVAR['content_count'][2]
        for i in range (start, stop+step, step):
            PARAMS['content_count'] = i
            start_time = timeit.default_timer()
            GT.generate_timeline(PARAMS)
            elapsed = timeit.default_timer() - start_time
            print ("Generated timeline for "+str(count+1)+" out of "+str(totalCount)+"; Elapsed time: "+str(elapsed))
            count += 1
        PARAMS['content_count'] = STATVAR['content_count'][3]

        # Variation for view-share probability mean and standard deviation
        mn_start = STATVAR['vwshprob_mean'][0]
        mn_stop = STATVAR['vwshprob_mean'][1]
        mn_step = STATVAR['vwshprob_mean'][2]
        sd_start = STATVAR['vwshprob_stdv'][0]
        sd_stop = STATVAR['vwshprob_stdv'][1]
        sd_step = STATVAR['vwshprob_stdv'][2]
        for i in np.linspace(mn_start, mn_stop, num = int((mn_stop-mn_start)/mn_step)+1):
            for j in np.linspace(sd_start, sd_stop, num = int((sd_stop-sd_start)/sd_step)+1):
                PARAMS['vwshprob_mean'] = i
                PARAMS['vwshprob_stdv'] = j
                start_time = timeit.default_timer()
            	GT.generate_timeline(PARAMS)
            	elapsed = timeit.default_timer() - start_time
            	print ("Generated timeline for "+str(count+1)+" out of "+str(totalCount)+"; Elapsed time: "+str(elapsed))
                count += 1
        PARAMS['vwshprob_mean'] = STATVAR['vwshprob_mean'][3]
        PARAMS['vwshprob_stdv'] = STATVAR['vwshprob_stdv'][3]

        # Variation of content level view and share probability boosts
        cbv_start = STATVAR['cmlb_view'][0]        
        cbv_stop = STATVAR['cmlb_view'][1]
        cbv_step = STATVAR['cmlb_view'][2]
        cbs_start = STATVAR['cmlb_share'][0]
        cbs_stop = STATVAR['cmlb_share'][1]
        cbs_step = STATVAR['cmlb_share'][2]
        for i in np.linspace(cbv_start, cbv_stop, num = int((cbv_stop-cbv_start)/cbv_step)+1):
            for j in np.linspace(cbs_start, cbs_stop, num = int((cbs_stop-cbs_start)/cbs_step)+1):
                PARAMS['cmlb_view'] = i
                PARAMS['cmlb_share'] = j
                start_time = timeit.default_timer()
            	GT.generate_timeline(PARAMS)
            	elapsed = timeit.default_timer() - start_time
            	print ("Generated timeline for "+str(count+1)+" out of "+str(totalCount)+"; Elapsed time: "+str(elapsed))
                count += 1
        PARAMS['cmlb_view'] = STATVAR['cmlb_view'][3]
        PARAMS['cmlb_share'] = STATVAR['cmlb_share'][3]
        print ("COUNT: "+str(count))

    return

############################################################

def run_all_simulations ():

    #for i in range (10):
    generate_all_timelines()

    return

############################################################

def fake_comparison_stats_fill ():
    comparison_stats = {}
    comparison_stats['total_edges'] = 0
    comparison_stats['true_positive'] = 0
    comparison_stats['true_positive_ratio'] = 0.0
    comparison_stats['false_positive'] = 0
    comparison_stats['false_positive_ratio'] = 0.0
    comparison_stats['missed_edges'] = 0
    comparison_stats['missed_edges_ratio'] = 0.0
    return comparison_stats

#############################################################

def main():

    run_all_simulations()

    return

############################################################

if __name__ == '__main__':
    main()

###########################################################
