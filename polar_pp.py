# -*- coding: utf-8 -*-

__all__ = [ 'read_data', 'write_data' ]

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
import itertools
#-----------------------------------------------------------------------------#

class pp_core(object):
    """
    Attributes. 
    :read_csv:   read csv files
    ...
    """

    def __init__(self):
        self.time_threshold = 21600
        self.timeSpan = 108000
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
           _subStepCount = []
           _ax = 0; _step = 0
           for cnt, row in enumerate(inObj):
               _sid.append(row[0])
               _t.append(row[1])
               _a = _sid[_ax]; _b = _sid[cnt]
               _c = _t[_ax]; _d = _t[cnt]
               start = datetime.strptime(_c, "%Y-%m-%d %H:%M:%S")
               end = datetime.strptime(_d, "%Y-%m-%d %H:%M:%S")
               _diff.append(end-start); _e = end-start
               _step += _diff[cnt].seconds
               if ( _a == _b and _diff[cnt].seconds < pp_core().time_threshold ):
                  _subStepCount.append(cnt)
                  print ('sid: {}, step: {}'.format(_b,_diff[cnt].seconds))
                  next(inObj)
               else: 
                   _ax = cnt 
                   _step = 0 
                   yield _b, _d, _diff[cnt].seconds 

           data_gen = (newData for newData in _diff if newData.seconds >= pp_core().time_threshold)
           if pp_core().newCount: 
              dCount = sum(1 for n in data_gen)
           else:
              dCount = 0

           subTot = len(_subStepCount)
           tot = subTot + cnt + 1 

           self.__printSummary(start, end, cnt, subTot, dCount, tot, _diff, _step)

        def __printSummary(self, start, end, cnt, subtot, dcount, tot, diff, step):
            print("")
            print('*'*20)
            print('* start: {}'.format(start))
            print('* end: {}'.format(end))
            print('* number of rows: {}'.format(cnt))
            print('* Substep count of rows: {}'.format(subtot))
            print('* TOTAL number of rows read: {}'.format(tot))
            print('* NEW number of rows: {}'.format(dcount))
            print('* difference: {}'.format(diff[5]))
#            print('* duration in seconds: {}'.format(diff[cnt].seconds))
            print('* number of days: {}'.format(diff[5].days))
            print('* Steps: {}'.format(step))
            print('*'*20)
            print("")

        def __filter(self, ax, bx, cx, dx):
            pass 

    @staticmethod
    @__qVector
    def read_data(filename, fmt, *strs):
        """ read input file: """

        if fmt == 'csv':
           try:
              import csv
              try:
#                 with open(filename) as f:
#                      data = csv.DictReader(f, delimiter=';')
#                      data = itertools.chain(*map(lambda f: csv.DictReader(open(f, 'r')), files))
                 data = itertools.chain(*map(lambda f: csv.DictReader(open(f), delimiter=';'), filename))
                 for counter, rw in enumerate(data):
#                          print counter
                     yield rw[strs[0]], rw[strs[1]]

              except csv.Error as e:
                 sys.exit('file {}, line {}: {}'.format(filename, reader.line_num, e))

           except ImportError:
              raise ImportError('cannot import csv module')

        else: pass

    @staticmethod
    def write_data(filename, data, fmt, *strs):
        """
        Write out data to a file
        """

        if strs:
           print strs

        if fmt == 'csv':
           try:
              import csv
              try:
                 with open(filename, 'w') as f:
                      fnames = [strs[0], strs[1], strs[2]]
                      out_file = csv.DictWriter(f, fieldnames=fnames, delimiter=';')
                      out_file.writeheader()
                      for counter, rw in enumerate(data):
                          out_file.writerow({strs[0]: rw[0], strs[1]: rw[1], strs[2]: rw[2]})

              except csv.Error as e:
                 sys.exit('file {}, line {}: {}'.format(filename, reader.line_num, e))

           except ImportError:
              raise ImportError('cannot import csv module')

    @classmethod 
    def __test_gen(class_, gen):
        """ Try to determine the size of your new data """
        class_.count = sum(1 for n in gen) 
        return class_.count


