# -*- coding: utf-8 -*-
"""
Post processing script
"""

from polar_pp import pp_core as polar

class post_process(object):

      #mmsi;date_time_utc;lon;lat;sog;cog;true_heading;nav_status;message_nr
      FN = '/Volumes/IBES_LynchLab/AIS/2011/20110101-20110601/ais_20110101.csv'
      FNLOCAL = '/Users/jack/Arbeit/lynch_lab/postproc/test_data/ais_20110124.csv' 
      FP = '/Volumes/IBES_LynchLab/AIS/2011/20110101-20110601/ais_20110101.csv'

      FN_OUT = '//Users/jack/Downloads/ais_test/ais_test2011.csv'

      def __init__(self):
          self.newcount = False
          self.FNLOCAL = '/Users/jack/Arbeit/lynch_lab/postproc/test_data/ais_20110124.csv' 
          self.FP = '/Volumes/IBES_LynchLab/AIS/2011/20110101-20110601'
          self.FN = 'ais_20110101.csv'
          self.FNOUT = ''
          self.format = 'cvs'
          self.fieldnames = ('mmsi', 'date_time_utc')

      def read_write(self):
          inData = polar.read_file(self.FNLOCAL, self.format, self.fieldnames)
          polar.write_file(self.FNOUT, inData, self.format, self.fieldnames)

pp = post_process()

pp.FNOUT = '/Users/jack/Downloads/ais_test/ais_test2011.csv'
pp.read_write()

