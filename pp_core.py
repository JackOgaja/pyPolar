# -*- coding: utf-8 -*-

__all__ = [ 'read_data', 'write_data' ]

__version__ = '0.1.0'
__description__ = 'post-processing AIS/sea ice Data' 
__author__ = 'Jack Ogaja  <jack_ogaja@brown.edu> '
__license__ = 'MIT'

#-----------------------------------------------------------------------------#

import os, sys, inspect
from abc import ABCMeta, abstractmethod
from datetime import timedelta, datetime, tzinfo
import time as time
from numpy import linspace
import itertools
import collections
import threading
#-----------------------------------------------------------------------------#

class progressBase(object):
    __metaclass__ = ABCMeta
    """
    base class for progress indicator
    """

    @abstractmethod
    def __call__(self, *args):
       pass

class progress(progressBase):
    """
    : This is a wrapper with progress indicator
    : All decorated functions must have 'progressBase' as the parent class
    """
    
    def __init__(self):
       pass

    def __call__(self, gObj, ln):
       startT = time.time()
       endT = startT
       deci = 100
       refT = 1
       deciSteps = {}
       print(' total counts = {}'.format(ln))
       tstr = '[00:00:00, --:--:--]'
       cstr = ('', u'\u258E',u'\u258C',u'\u258A')
       deciSteps = {int(ii):(int(jj/4.0),int(jj%4)) for ii,jj in zip(linspace(0,ln-1,min(101,ln)), linspace(0,100,min(101,ln)))}

       for cnt, row in enumerate(gObj):
           if cnt in deciSteps:
              haDry   = u'\u2588'*(deciSteps[cnt][0])+cstr[deciSteps[cnt][1]]
              yetTo   = ' '*(25-len(haDry))
              progbar = '%3d%% |%s%s|' %((cnt)/(ln-1.0)*100.0, haDry, yetTo)
              if cnt>0:
                 progbar  = '\r'+progbar
                 endT = time.time()
                 tstr = ' [%s, %s]'%(self.tToStr(endT-startT), self.tToStr((endT-startT)*(ln/(cnt+1.0)-1)))
              if cnt == ln-1: 
                 tstr += '\n'
              sys.stdout.write((progbar+tstr).encode('utf-8')); sys.stdout.flush()
           elif time.time()-endT > refT:
              endT = time.time()
              tstr = ' [%s, %s]'%(self.tToStr(endT-startT), self.tToStr((endT-startT)*(ln/(cnt+1.0)-1)))
              progbar = '%3d%% |%s%s|' %((cnt)/(ln-1.0)*100.0, haDry, yetTo)
              sys.stdout.write(('\r'+progbar+tstr).encode('utf-8')); sys.stdout.flush()
           yield row

    def tToStr(self, tInSec):
        minutes, secs = divmod(tInSec, 60)
        hrs, minutes = divmod(minutes, 60)
        return u'%02d:%02d:%02d' %(hrs,minutes,secs)
   
class pp_core(object):
    """
    Attributes. 
    :read_csv:   read csv files
    ...
    """

    # Additional class attributes
    cls_time_threshold = 21600
    cls_timeSpan = 108000
    cls_newCount = True 

    def __init__(self):
        """
        create the class instance
        """

    class __qVector(progressBase):
        """
        Determine the time step
        """
        def __init__(self, inFunc):
           self.func = inFunc

        def __call__(self, *args):
           inObj = self.func(*args)
           inObj, inObjCp = itertools.tee(inObj)
           ln = pp_core.lengthOfgen(inObjCp)
           _t  = []
           _sid = []
           _diff = []
           _subStepCount = []
           _ax = 0; _step = 0

           for cnt, row in enumerate(progress()(inObj, ln)):
               _sid.append(row[0])
               _t.append(row[1])
               _a = _sid[_ax]; _b = _sid[cnt]
               _c = _t[_ax]; _d = _t[cnt]
               start = datetime.strptime(_c, "%Y-%m-%d %H:%M:%S")
               end = datetime.strptime(_d, "%Y-%m-%d %H:%M:%S")
               _diff.append(end-start); _e = end-start
               _step += _diff[cnt].seconds
               if ( _a == _b and _diff[cnt].seconds < pp_core.cls_time_threshold ):
                  _subStepCount.append(cnt)
               else: 
                   _ax = cnt 
                   _step = 0 
                   yield row

           data_gen = (newData for newData in _diff if newData.seconds >= pp_core.cls_time_threshold)
           if pp_core.cls_newCount: 
              dCount = sum(1 for n in data_gen)
           else:
              dCount = 0

           subTot = len(_subStepCount)
           tot = subTot + cnt + 1 

           self.__printSummary(start, end, cnt, subTot, dCount, tot, _diff, _step)

        def __printSummary(self, start, end, cnt, subtot, dcount, tot, diff, step):
            print("")
            print('*'*20)
            print('-'*3+'PP summary'+'-'*3)
            print('-')
            print('* start: {}'.format(start))
            print('* end: {}'.format(end))
            print('* time step [sec]: {}'.format(pp_core.cls_time_threshold))
            print('* number of rows: {}'.format(cnt))
            print('* Substep count of rows: {}'.format(subtot))
            print('* TOTAL number of rows read: {}'.format(tot))
            print('* NEW number of rows: {}'.format(dcount))
            print('* difference: {}'.format(diff[5]))
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

        fields = strs
        if fmt == 'csv':
           try:
              import csv
              try:
                 data = itertools.chain(*map(lambda f: csv.DictReader(open(f), delimiter=';'), filename))
                 for counter, rw in enumerate(data):
                     yield rw[strs[0]], rw[strs[1]], rw[strs[2]], \
                           rw[strs[3]], rw[strs[4]], rw[strs[5]], \
                           rw[strs[6]], rw[strs[7]], rw[strs[8]]

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
        if fmt == 'csv':
           try:
              import csv
              try:
                 with open(filename, 'w') as f:
                      fnames = [strs[0], strs[1], strs[2],
                                strs[3], strs[4], strs[5],
                                strs[6], strs[7], strs[8]]
                      out_file = csv.DictWriter(f, fieldnames=fnames, delimiter=';')
                      out_file.writeheader()
                      for counter, rw in enumerate(data):
                          out_file.writerow({strs[0]: rw[0], strs[1]: rw[1], strs[2]: rw[2],
                                             strs[3]: rw[3], strs[4]: rw[4], strs[5]: rw[5],
                                             strs[6]: rw[6], strs[7]: rw[7], strs[8]: rw[8]})

              except csv.Error as e:
                 sys.exit('file {}, line {}: {}'.format(filename, reader.line_num, e))

           except ImportError:
              raise ImportError('cannot import csv module')

    @classmethod 
    def __test_gen(class_, gen):
        """ Try to determine the size of your new data """
        class_.count = sum(1 for n in gen) 
        return class_.count

    @staticmethod 
    def lengthOfgen(genObj):

        """ Determine length of a generator """

        print 'Calculating total duration....  ',
        sys.stdout.flush()
        for n, m in enumerate(genObj):  
            if (n%4) == 0:
                sys.stdout.write('\b/')
            elif (n%4) == 1:
                sys.stdout.write('\b-')
            elif (n%4) == 2:
                sys.stdout.write('\b\\')
            elif (n%4) == 3:
                sys.stdout.write('\b|')

            sys.stdout.flush()
            time.sleep(0.0)
        print '\b\b Done!',
        return n+1


