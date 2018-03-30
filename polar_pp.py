# -*- coding: utf-8 -*-

__all__ = [ 'pp_read', 'pp_write' ]

__version__ = '0.1.0'
__description__ = 'post-processing AIS/sea ice Data' 
__author__ = 'Jack Ogaja  <jack_ogaja@brown.edu> '
__license__ = 'MIT'

"""
The MIT License (MIT)

Copyright (C) 2018 Jack Ogaja, Brown University.

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""
#-----------------------------------------------------------------------------#

import os, sys, inspect
from datetime import timedelta, datetime, tzinfo, time
#-----------------------------------------------------------------------------#

class pp_core(object):
    """
    Attributes. 
    :read_csv:   read csv files
    ...
    """

    def __init__(self):
        self.time_threshold = 60000
        self.newCount = True 

    class __qVector(object):
        """
        Determine the time step
        """
        def __init__(self, inFunc):
            self.func = inFunc

        def __call__(self, *args):
           inObj = self.func(*args)
           len_args = len(args)
           if len_args > 1: 
              ncount = args[len_args-1]
              t_threshold = args[len_args-2]
           _t  = []
           _sid = []
           _diff = []
           for cnt, row in enumerate(inObj):
               _sid.append(row[0])
               _t.append(row[1])
               _a = _sid[0]; _b = _sid[cnt]
               _c = _t[0]; _d = _t[cnt]
               start = datetime.strptime(_c, "%Y-%m-%d %H:%M:%S")
               end = datetime.strptime(_d, "%Y-%m-%d %H:%M:%S")
               _diff.append(end-start)
               if ( _a == _b and _diff[cnt].seconds < pp_core().time_threshold):
                  next(inObj)
               yield _b, _d, _diff[cnt].seconds 
#++++++++++++++++++++++
#               _sid.append(row[0])
#               _t.append(row[1])
#               _a = _sid[0]; _b = _sid[cnt]
#               _c = _t[0]; _d = _t[cnt]
#               start = datetime.strptime(_c, "%Y-%m-%d %H:%M:%S")
#               end = datetime.strptime(_d, "%Y-%m-%d %H:%M:%S")
#               _diff.append(end-start)
#               if _diff[cnt].seconds < pp_core().time_threshold:
#                  yield _b, _d, _diff[cnt].seconds 

           data_gen = (newData for newData in _diff if newData.seconds > pp_core().time_threshold)
           if pp_core().newCount: 
              dCount = sum(1 for n in data_gen)
           else:
              dCount = 0

           print("")
           print('******************')
           print('* start: {}'.format(start))
           print('* end: {}'.format(end))
           print('* number of rows: {}'.format(cnt))
           print('* NEW number of rows: {}'.format(dCount))
           print('* difference: {}'.format(_diff[5]))
           print('* duration in seconds: {}'.format(_diff[5].seconds))
           print('* number of days: {}'.format(_diff[5].days))
           print('******************')
           print("")

    @staticmethod
    @__qVector
    def read_file(filename, fmt, *strs):
        """ read input file: """

        if fmt == 'csv':
           try:
              import csv
              try:
                 with open(filename) as f:
                      data = csv.DictReader(f, delimiter=';')
                      for counter, rw in enumerate(data):
                          yield rw[strs[0]], rw[strs[1]]

              except csv.Error as e:
                 sys.exit('file {}, line {}: {}'.format(filename, reader.line_num, e))

           except ImportError:
              raise ImportError('cannot import csv module')

        else: pass

    @staticmethod
    def write_file(filename, data, fmt, *strs):
        """
        Write out data to a file
        """

        if fmt == 'csv':
           try:
              import csv
              try:
                 with open(filename, 'w') as f:
#                      fieldnames = [strs[0], strs[1]]
                      fieldnames = [strs[0], strs[1], 'seconds']
                      out_file = csv.DictWriter(f, fieldnames=fieldnames, delimiter=';')
                      out_file.writeheader()
                      for counter, rw in enumerate(data):
#                          out_file.writerow({strs[0]: rw[0], strs[1]: rw[1]})
                          out_file.writerow({strs[0]: rw[0], strs[1]: rw[1], 'seconds': rw[2]})

              except csv.Error as e:
                 sys.exit('file {}, line {}: {}'.format(filename, reader.line_num, e))

           except ImportError:
              raise ImportError('cannot import csv module')

    @classmethod 
    def __test_gen(cls, gen):
        """ Try to determine the size of your new data """
        cls.count = sum(1 for n in gen) 
        return cls.count


