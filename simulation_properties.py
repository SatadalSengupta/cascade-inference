import os

### STATIC PROPERTIES ###

CWD = os.getcwd()
VERBOSE = True
DATASET = "facebook.txt"
RUN_COUNT = 1
CONTENT_LEVELS = 3
POI_MEAN = 0.148 # 14.8% of Sample Size
POI_STDV = 0.079 # 7.9% of Sample Size

### VARIABLE PROPERTIES VARIED WHILE OTHER PROPERTIES ARE CONSTANT ###

CONTENT_COUNT = [ 100, 1000, 100, 200 ] # The format is [StartValue, EndValue, Step, ValueWhenStatic]

VWSHPROB_MEAN = [ 0.3, 0.7, 0.1, 0.5 ] # The format is [StartValue, EndValue, Step, ValueWhenStatic]
VWSHPROB_STDV = [ 0.10, 0.20, 0.05, 0.15 ] # The format is [StartValue, EndValue, Step, ValueWhenStatic]

#VIEW_BOOST = [ 0.00, 1.00, 0.25, 0.5 ] # The format is [StartValue, EndValue, Step, ValueWhenStatic]
#SHARE_BOOST = [ 0.00, 1.00, 0.25, 0.5 ] # The format is [StartValue, EndValue, Step, ValueWhenStatic]

#WEIGHT_THRESHOLD = [ 1.0, 5.0, 0.5, 2.5 ] # Threshold = Mean + (Std * WEIGHT_THRESHOLD)

CONTENT_MINLVL_BOOST_VIEW = [ 0.0, 0.8, 0.2, 0.4 ] # Level-X Boost = Level-Min Boost + 0.2*(X-1)
CONTENT_MINLVL_BOOST_SHARE = [ 0.0, 0.8, 0.2, 0.4 ] # Level-X Boost = Level-Min Boost + 0.2*(X-1)

### COMPARISON MODULE ###

COMPARE_WITH = ["MaxSize", "MaxEdgeDensity"]
THRESHOLD = []
