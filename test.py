# -*- coding: utf-8 -*-
"""
Post processing script
"""

from polar_pp import pp_core as polar

class post_process(object):

      #mmsi;date_time_utc;lon;lat;sog;cog;true_heading;nav_status;message_nr

      def __init__(self):
          self.newcount = False
          self.FNLOCAL = '' 
          self.FP = '/Volumes/IBES_LynchLab/AIS/2011/20110101-20110601'
          self.FN = 'ais_20110101.csv'
          self.FNOUT = ''
          self.frmt = 'csv'

      def read_write(self):
          inData = polar.read_file(self.FNLOCAL, self.frmt, 'mmsi', 'date_time_utc') 
          polar.write_file(self.FNOUT, inData, self.frmt, 'mmsi', 'date_time_utc', 'seconds') 

if __name__ == "__main__":
   pp = post_process()

   pp.FNLOCAL = '/Users/jack/Arbeit/lynch_lab/postproc/test_data/ais_20110124.csv' 
   pp.FNOUT = '/Users/jack/Downloads/ais_test/ais_test2011.csv'
   pp.read_write()

