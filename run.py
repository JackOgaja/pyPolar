# -*- coding: utf-8 -*-

from polar_pp import post_process 
from polar_pp import combineFiles1, combineFiles2 
from polar_pp import countFiles 

# Post processing .csv files
# Attributes: time interval = 6hrs
#             duration = 30+ hrs

# Call the post processing routine
pp = post_process()

# Set the attributes:
pp.frmt = 'csv'     # file format

# file header
pp.header = 'mmsi', 'date_time_utc', \
            'lon', 'lat', 'sog', 'cog', \
            'true_heading', 'nav_status', 'message_nr'

# Path for the raw data files
fpath = '/Volumes/IBES_LynchLab/AIS/2011/20110101-20110601/'

# Prefix for selecting files of a particular period
prefix = 'ais_2011'  # a file name can be specified e.g. 'ais_20110101.csv'

# Output file name
fOut = 'pp_'+prefix+pp.frmt  # if a complete file name is selected above,
                             # then just add the prefix e.g. fOut='pp_'+prefix

# count the files available for post processing
availFiles = countFiles(fpath, pp.frmt)
print('-'*3+'number of files: {}'.format(availFiles))

# If there are few files for post processing,
# they can be combined to a single file
# by calling 'combineFiles1', otherwise
# create a list of files using 'combineFiles2'
# before processing. 
# 'combineFiles1' is NOT recommended for huge files due
# to memory limitations
files = combineFiles2(fpath, prefix)

# Assign the combined file or the list of files to the input variable
pp.FNIN = files

# Set the output directory + output file name
pp.FNOUT = '/Users/jack/Downloads/ais_test/'+fOut

# Read, post process and write the post processed data into a new file
pp.read_write()

