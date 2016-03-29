import simulation_properties as SP

############################################################

def load_all_properties():

    # Build the all-important parameter dictionary

    PARAMS = {}
    ALLVAR = {}
    STATVAR = {}

    # Load static properties first

    PARAMS['verbose'] = SP.VERBOSE
    PARAMS['dataset'] = SP.DATASET
    PARAMS['sampled_dataset'] = SP.SAMPLED_DATASET
    PARAMS['run_count'] = SP.RUN_COUNT
    PARAMS['content_levels'] = SP.CONTENT_LEVELS
    PARAMS['poi_mean'] = SP.POI_MEAN
    PARAMS['poi_stdv'] = SP.POI_STDV
     
    # Load all-variable properties in a different dictionary for now
    
    ALLVAR['sampling_technique'] = SP.SAMPLING_TECHNIQUE

    # Load variable-while-others-static properties in a different dictionary for now

    STATVAR['sample_size'] = SP.SAMPLE_SIZE
    STATVAR['content_count'] = SP.CONTENT_COUNT
    STATVAR['vwshprob_mean'] = SP.VWSHPROB_MEAN
    STATVAR['vwshprob_stdv'] = SP.VWSHPROB_STDV
    STATVAR['view_boost'] = SP.VIEW_BOOST
    STATVAR['share_boost'] = SP.SHARE_BOOST
    STATVAR['weight_threshold'] = SP.WEIGHT_THRESHOLD
    STATVAR['cmlb_view'] = SP.CONTENT_MINLVL_BOOST_VIEW
    STATVAR['cmlb_share'] = SP.CONTENT_MINLVL_BOOST_SHARE

    return PARAMS, ALLVAR, STATVAR

############################################################

def run_all_simulations():

    PARAMS, ALLVAR, STATVAR = load_all_properties()

    return

############################################################

def main():

    run_all_simulations()

    return

############################################################

if __name__ == '__main__':
    main()

############################################################
