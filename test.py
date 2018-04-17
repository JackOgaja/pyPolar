# -*- coding: utf-8 -*-
"""
Post processing script
"""

from polar_pp import pp_core as polar
import glob, os
import pandas as pd

class post_process(object):

      #mmsi;date_time_utc;lon;lat;sog;cog;true_heading;nav_status;message_nr

      def __init__(self):
          self.newcount = False
          self.FNLOCAL = '' 
          self.FNOUT = ''
          self.frmt = ''
          self.header = ''

      def read_write(self):
          inData = polar.read_data(self.FNLOCAL, self.frmt, *self.header) 
          polar.write_data(self.FNOUT, inData, self.frmt, *self.header) 

def combineFiles1(fPath, fInPrefix, fOut):
    os.chdir(fPath)
    results = pd.DataFrame([])

    for counter, file in enumerate(glob.glob(fInPrefix+'*')):
        namedf = pd.read_csv(file, skiprows=0)
        results = results.append(namedf)
        print('==> {} file read'.format(counter))

    results.to_csv(fPath+fOut)

def combineFiles2(fPath, fInPrefix):
    """
    creates a list of all files
    """
    os.chdir(fPath)
    files = sorted(glob.glob(fInPrefix+'*'))
    return files 

def countFiles(fPath, frmt):
    # output: [path, dir, files]
    availFiles = len([f for f in next(os.walk(fPath))[2] if f[-4:] == '.'+frmt])
    return availFiles

if __name__ == "__main__":
   pp = post_process()
   
   pp.frmt = 'csv'
   pp.header = 'mmsi', 'date_time_utc', 'seconds'

   fpath = '/Volumes/IBES_LynchLab/AIS/2011/20110101-20110601/'
   prefix = 'ais_2011'
   fOut = 'combinedfile.csv'
   availFiles = countFiles(fpath, pp.frmt)
   print(availFiles)
   files = combineFiles2(fpath, prefix)
   print(files)

   pp.FNLOCAL = files
   pp.FNOUT = '/Users/jack/Downloads/ais_test/ais_test2011.csv'

   pp.read_write()

