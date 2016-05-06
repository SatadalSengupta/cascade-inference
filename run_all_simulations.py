import generate_timelines as GT
import simulation_properties as SP
import numpy as np
import os
from datetime import datetime
from utilities import display

############################################################

def load_parameters_for_test_run():

    PARAMS, ALLVAR, STATVAR = load_all_properties()
    PARAMS = load_default_properties(PARAMS)
    display("load_parameters_for_test_run", "Parameters loaded for test run.")

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
    STATVAR['view_boost'] = SP.VIEW_BOOST
    STATVAR['share_boost'] = SP.SHARE_BOOST
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
    PARAMS['view_boost'] = SP.VIEW_BOOST[3]
    PARAMS['share_boost'] = SP.SHARE_BOOST[3]
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
    writeline += "RUN " + str(count) + " OUT OF ALL AT TIME: " + str(datetime.now()) + "\n\n"
    #writeline += fmt.format("Sampling technique", str(PARAMS['sampling_technique']))
    #writeline += fmt.format("Sample size", str(PARAMS['sample_size']))
    writeline += fmt.format("Content count", str(PARAMS['content_count']))
    writeline += fmt.format("View share probability mean", str(PARAMS['vwshprob_mean']))
    writeline += fmt.format("View share probability standard deviation", str(PARAMS['vwshprob_stdv']))
    writeline += fmt.format("View probability boost", str(PARAMS['view_boost']))
    writeline += fmt.format("Share probability boost", str(PARAMS['share_boost']))
    writeline += fmt.format("Weight threshold", str(PARAMS['weight_threshold']))
    writeline += fmt.format("Content minimum level view probability boost", str(PARAMS['cmlb_view']))
    writeline += fmt.format("Content minimum level share probability boost", str(PARAMS['cmlb_share']))
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

    PARAMS, ALLVAR, STATVAR = load_all_properties()

    # Fake comparison_stats for testing; comment this in actual runs, and uncomment CG.compare_graphs() calls
    # comparison_stats = fake_comparison_stats_fill()

    # Prepare the property set for current simulation run

    #for cw_item in ALLVAR['compare_with']:
    for i in range(1): # Dummy to run just once

        #PARAMS['compare_with'] = cw_item
        PARAMS = load_default_properties(PARAMS)

        # Variation for content count
        start = STATVAR['content_count'][0]
        stop = STATVAR['content_count'][1]
        step = STATVAR['content_count'][2]
        for i in range (start, stop+step, step):
            PARAMS['content_count'] = i
            #comparison_stats = CG.compare_graphs(PARAMS)
            GT.generate_timeline(PARAMS)
            count += 1
            #dump_results (fp, PARAMS, comparison_stats, count)
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
                #comparison_stats = CG.compare_graphs(PARAMS)
                GT.generate_timeline(PARAMS)
                count += 1
                #dump_results (fp, PARAMS, comparison_stats, count)
        PARAMS['vwshprob_mean'] = STATVAR['vwshprob_mean'][3]
        PARAMS['vwshprob_stdv'] = STATVAR['vwshprob_stdv'][3]

        # Variation of view and share probability boost values
        vb_start = STATVAR['view_boost'][0]
        vb_stop = STATVAR['view_boost'][1]
        vb_step = STATVAR['view_boost'][2]
        sb_start = STATVAR['share_boost'][0]
        sb_stop = STATVAR['share_boost'][1]
        sb_step = STATVAR['share_boost'][2]
        for i in np.linspace(vb_start, vb_stop, num = int((vb_stop-vb_start)/vb_step)+1):
            for j in np.linspace(sb_start, sb_stop, num = int((sb_stop-sb_start)/sb_step)+1):
                PARAMS['view_boost'] = i
                PARAMS['share_boost'] = j
                #comparison_stats = CG.compare_graphs(PARAMS)
                GT.generate_timeline(PARAMS)
                count += 1
                #dump_results(fp, PARAMS, comparison_stats, count)
        PARAMS['view_boost'] = STATVAR['view_boost'][3]
        PARAMS['share_boost'] = STATVAR['share_boost'][3]

        # Variation of weight_threshold
        '''wt_start = STATVAR['threshold'][0]
        wt_stop = STATVAR['threshold'][1]
        wt_step = STATVAR['threshold'][2]
        for i in np.linspace(wt_start, wt_stop, num = int((wt_stop-wt_start)/wt_step)+1):
            PARAMS['threshold'] = i
            comparison_stats = CG.compare_graphs(PARAMS)
            count += 1
            dump_results(fp, PARAMS, comparison_stats, count)
        PARAMS['threshold'] = STATVAR['threshold'][3]
        '''

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
                #comparison_stats = CG.compare_graphs(PARAMS)
                GT.generate_timeline(PARAMS)
                count += 1
                #dump_results(fp, PARAMS, comparison_stats, count)
        PARAMS['cmlb_view'] = STATVAR['cmlb_view'][3]
        PARAMS['cmlb_share'] = STATVAR['cmlb_share'][3]

        # Variation for sample size
        #start = STATVAR['sample_size'][0]
        #stop = STATVAR['sample_size'][1]
        #step = STATVAR['sample_size'][2]
        #for i in range ( start, stop+step, step ):
        #    PARAMS['sample_size'] = i
        #    comparison_stats = CG.compare_graphs(PARAMS)
        #    count += 1
        #    dump_results (fp, PARAMS, comparison_stats, count)
        #PARAMS['sample_size'] = STATVAR['sample_size'][3]    

    #fp.close()
    display("generate_all_timelines", str(count))

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
