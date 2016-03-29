import os

### STATIC PROPERTIES ###

VERBOSE = False
DATASET = "facebook.txt"
SAMPLED_DATASET = DATASET.split(".")[0] + "_sampled.txt"
RUN_COUNT = 1
CONTENT_LEVELS = 3
POI_MEAN = 0.3 # 30% of Sample Size
POI_STDV = 0.2 # 20% of Sample Size


### VARIABLE PROPERTIES VARIED FOR ALL SUBSEQUENT PROPERTIES ###

SAMPLING_TECHNIQUE = [ "DegreeMin", "DegreeMax" ] # Can be any sub-set of (Random, DegreeMin, DegreeMax)


### VARIABLE PROPERTIES VARIED WHILE OTHER PROPERTIES ARE CONSTANT ###

SAMPLE_SIZE = [ 100, 1000, 100, 500 ] # The format is [StartValue, EndValue, Step, ValueWhenStatic]

CONTENT_COUNT = [ 100, 10000, 100, 1000 ] # The format is [StartValue, EndValue, Step, ValueWhenStatic]

VWSHPROB_MEAN = [ 0.3, 0.7, 0.1, 0.5 ] # The format is [StartValue, EndValue, Step, ValueWhenStatic]
VWSHPROB_STDV = [ 0.10, 0.20, 0.05, 0.15 ] # The format is [StartValue, EndValue, Step, ValueWhenStatic]

VIEW_BOOST = [ 0.00, 1.00, 0.25, 0.5 ] # The format is [StartValue, EndValue, Step, ValueWhenStatic]
SHARE_BOOST = [ 0.00, 1.00, 0.25, 0.5 ] # The format is [StartValue, EndValue, Step, ValueWhenStatic]

WEIGHT_THRESHOLD = [ 1.0, 5.0, 0.5, 2.5 ] # Threshold = Mean + (Std * WEIGHT_THRESHOLD)

CONTENT_MINLVL_BOOST_VIEW = [ 0.0, 0.8, 0.1, 0.3 ] # Level-X Boost = Level-Min Boost + 0.2*(X-1)
CONTENT_MINLVL_BOOST_SHARE = [ 0.0, 0.8, 0.1, 0.3 ] # Level-X Boost = Level-Min Boost + 0.2*(X-1)
