# -*- coding: utf-8 -*-
#
# module : ais_pp
# created: Jack Ogaja <jack_ogaja@brown.edu>
# purpose: post-processing AIS Data   
# License: MIT
#
"""
The MIT License (MIT)

Copyright (c) 2018 Jack Ogaja, Brown University.

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
#-----------------------------------------------------------------------------#

class ais_read:
    """
    Attributes. 
              labels:    legend labels
              title:     plot title
              styles:    plot styles
              lwidth:    plot line width
              legLoc:    legend location
              savePlot:  option to save a plot to a file/dir
              plotName:  plot name
              plotDir:   plot directory/folder
              outFormat: format of the output file |pdf/eps/png|
              lblsize:   label fornt size
              ttlsize:   title font size
              ymin:      minimum y-axis limit
              ymax:      maximum y-axis limit
              xmin:      minimum x-axis limit
              xmax:      maximum x-axis limit
              ylabel:    y-axis label
              xlabel:    x-axis label
              lgframe:   legend box 'on' or 'off'
              lgFontSize:legend font size
    """

    def __init__(self):
        self.labels = []
        self.title  = ''
        self.styles = []
        self.lwidth = []
        self.legLoc = 'best'
        self.lblsize = 10
        self.ttlweight ='normal'
        self.ttlsize = 10
        self.savePlot =None
        self.minorticks =None
        self.plotName ='plot'
        self.plotDir  ='out'
        self.outFormat ='png'
        self.ymin =None
        self.ymax =None
        self.xmin =None
        self.xmax =None
        self.ylabel ='y'
        self.xlabel ='x'
        self.lgframe =None
        self.lgFontSize =10

def main(self):
    if self.minorticks: pl.minorticks_on()
    if self.ymin: pl.ylim(ymin=self.ymin)
    if self.ymax: pl.ylim(ymax=self.ymax)
    if self.xmin: pl.xlim(xmin=self.xmin)
    if self.xmax: pl.xlim(xmax=self.xmax)

#*** Make the module executable as a script******#
if __name__ == "__main__":
    fname=__file__.split('/')
    print('\nThe \'{0}\' module is executed as a script\n'
          .format(fname[-1]))
    import numpy as np
    x = np.linspace(0, 2 * np.pi, 50, endpoint=True)
    y1 = 3 * np.sin(x)
    y2 = np.sin(2*x)
    y3 = 0.3 * np.sin(x)
    y4 = np.cos(x)
    hp=hosPlot()
    hp.styles=['b-','r--','g:','m-.']
    hp.lwidth=[2.5,1.5,2,2]
    hp.plotLine(x,y1,y2,y3,y4,hLine=(1,'hLine'))
