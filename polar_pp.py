# -*- coding: utf-8 -*-
"""
Post processing script
"""

from pp_core import pp_core as ppc
import glob, os
import pandas as pd

class pp_process(object):
      """
      : Read --> Process --> Write data files
      """

      def __init__(self):
          self.newcount = False
          self.FNLOCAL = '' 
          self.FNIN = '' 
          self.FNOUT = ''
          self.frmt = ''
          self.header = ''
          self.timeStep = 21600

      def read_write(self):
          ppc.cls_time_threshold = self.timeStep
          inData = ppc.read_data(self.FNIN, self.frmt, *self.header) 
          ppc.write_data(self.FNOUT, inData, self.frmt, *self.header) 

def combineFiles1(fPath, fInPrefix, fOut):
    """
    : Collect and append files into a new file
    : Caution:
    : This process is memory intensive and 
    : is not recommended for huge files
    """
    os.chdir(fPath)
    results = pd.DataFrame([])

    for counter, file in enumerate(glob.glob(fInPrefix+'*')):
        namedf = pd.read_csv(file, skiprows=0)
        results = results.append(namedf)
        print('==> {} file read'.format(counter))

    results.to_csv(fPath+fOut)

def combineFiles2(fPath, fInPrefix):
    """
    : creates a list of all files
    """
    os.chdir(fPath)
    files = sorted(glob.glob(fInPrefix+'*'))
    return files 

def countFiles(fPath, frmt):
    """
    : Count the number of files available
    : for processing in a directory
    """
    # output: [path, dir, files]
    availFiles = len([f for f in next(os.walk(fPath))[2] if f[-4:] == '.'+frmt])
    return availFiles

if __name__ == "__main__":
   """
   : In case this file is executed as the run script
   : Make the necessary settings below
   """
   pp = pp_process()
   
   pp.frmt = 'csv'
   pp.timeStep = 21600
   pp.header = 'mmsi', 'date_time_utc', \
               'lon', 'lat', 'sog', 'cog', \
               'true_heading', 'nav_status', 'message_nr' 

   fpath = '/Users/jack/Arbeit/lynch_lab/postproc/test_data/'
   prefix = 'ais_201101'
   fOut = 'pp_test_'+prefix+'.'+pp.frmt
   availFiles = countFiles(fpath, pp.frmt)
   print('-'*3+'number of files: {}'.format(availFiles))
   files = combineFiles2(fpath, prefix)

   pp.FNIN = files
   pp.FNOUT = '/Users/jack/Downloads/ais_test/'+fOut

   pp.read_write()

