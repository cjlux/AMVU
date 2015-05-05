#!/usr/bin/env python
from __future__ import division

"""
    Class for plot management
    
    == Currently under development ======================================
    
    Copyright (C) 2015
    Arthur Fages - Loic Fagot - Vincent Labourdette - Thomas Lamant - Guillaume Loizeau
    Arts et Metiers ParisTech, centre de Bordeaux-Talence
    
    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

# Version 0.1
# Last update : 05/05/2015

import pyaudio
import numpy
import wave
from threading import Thread
import time as t
from PyQt4 import Qt
from PyQt4 import QtCore
from PyQt4 import Qwt5 as Qwt

class Plot(Qwt.QwtPlot):
    """ Plot allowing to diplay a signal """

    def __init__(self, a1, a2, dt) :
        
        # signal characteristics
        self.dt   = dt
        self.a1   = a1
        self.a2   = a2
        
        # grid
        self.grid = Qwt.QwtPlotGrid()
        self.grid.enableXMin(True)
        self.grid.setMajPen(Qt.QPen(Qt.Qt.gray, 0, Qt.Qt.SolidLine))
        self.grid.attach(self)
        
        # axes
        self.enableAxis(Qwt.QwtPlot.yRight);
        self.setAxisTitle(Qwt.QwtPlot.xBottom, 'Time [s]');
        self.setAxisTitle(Qwt.QwtPlot.yLeft,  'Amplitude Chan. 1 [V]');
        self.setAxisTitle(Qwt.QwtPlot.yRight, 'Amplitude Chan. 2 [V]');
          
        self.setAxisMaxMajor(Qwt.QwtPlot.xBottom, 20);
        self.setAxisMaxMinor(Qwt.QwtPlot.xBottom, 0);

        self.setAxisScaleEngine(Qwt.QwtPlot.yRight, Qwt.QwtLinearScaleEngine());
        self.setAxisMaxMajor(Qwt.QwtPlot.yLeft, 10);
        self.setAxisMaxMinor(Qwt.QwtPlot.yLeft, 0);
        self.setAxisMaxMajor(Qwt.QwtPlot.yRight, 10);
        self.setAxisMaxMinor(Qwt.QwtPlot.yRight, 0);
        
        # curves for scope traces: 2 first so 1 is on top
        self.curve2 = Qwt.QwtPlotCurve('Trace2')
        self.curve2.setPen(Qt.QPen(Qt.Qt.magenta,1))
        self.curve2.setYAxis(Qwt.QwtPlot.yRight)
        self.curve2.attach(self)

        self.curve1 = Qwt.QwtPlotCurve('Trace1')
        self.curve1.setPen(Qt.QPen(Qt.Qt.blue,1))
        self.curve1.setYAxis(Qwt.QwtPlot.yLeft)
        self.curve1.attach(self)
        
        # curve display initialisation
        self.curve1.setData(self.ti, self.a1)
        self.curve2.setData(self.ti, self.a2)