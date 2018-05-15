# -*- coding: utf-8 -*-

from polar_pp import pp_process 
from polar_pp import combineFiles1, combineFiles2 
from polar_pp import countFiles 

# Processing .csv files
# Attributes: time interval = 6hrs
#             duration = 30+ hrs

# Call the PP processing routine
pp = pp_process()

# a) Set the attributes:

# file format
pp.frmt = 'csv'     

# time step [seconds]
pp.timeStep = 21600

# file header
pp.header = 'mmsi', 'date_time_utc', \
            'lon', 'lat', 'sog', 'cog', \
            'true_heading', 'nav_status', 'message_nr'

# Path for the raw data files
fpath = '/Users/jack/Arbeit/lynch_lab/data_processing/test_data/'

# Prefix for selecting files of a particular period
prefix = 'ais_2011'  # a file name can be specified e.g. 'ais_20110101.csv'

# Output file name
fOut = 'pp_'+prefix+'_test.'+pp.frmt  # if a complete file name is selected above,
                             # then just add the prefix e.g. fOut='pp_'+prefix

# count the files available for processing
availFiles = countFiles(fpath, pp.frmt)
print('-'*3+'number of files: {}'.format(availFiles))

# If there are few files for processing,
# they can be combined to a single file
# by calling 'combineFiles1', otherwise
# create a list of files using 'combineFiles2'
# before processing. 
# 'combineFiles1' is NOT recommended for huge files due
# to memory limitations
files = combineFiles2(fpath, prefix)
print(files)

# Assign the combined file or the list of files to the input variable
pp.FNIN = files

# Set the output directory + output file name
pp.FNOUT = '/Users/jack/Downloads/ais_test/'+fOut

# b) Call the main PP method "read_write"
# Read, process and write the processed data into a new file
pp.read_write()

