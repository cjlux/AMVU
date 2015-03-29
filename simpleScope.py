#!/usr/bin/env python
from __future__ import division

"""
    Simple scope to visualize signal
    
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

# Version 0.2
# Last update : 29/03/2015

import pyaudio
import sys
import numpy as np

from PyQt4 import Qt
from PyQt4 import QtCore
from PyQt4 import Qwt5 as Qwt

from testSignal import Signal

class Scope(Qwt.QwtPlot):
    
    def __init__(self, rate, size, *args):
        
        # signal characteristics
        self.size = size
        self.rate = rate
        self.dt   = 1./rate
        self.ti   = np.arange(0.0, 1.0, self.dt)
        self.a1   = 0.0*self.ti
        self.a2   = 0.0*self.ti     
        
        # Graphic user interface
        apply(Qwt.QwtPlot.__init__, (self,) + args)
        
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
        
        # test to see if QwtPlot automatically adapt the scale
        # TODO : find a way to display all the signal (it seems to
        # have a display limit when the signal duration is too important)
        self.setAxisScaleEngine(Qwt.QwtPlot.xBottom, Qwt.QwtLinearScaleEngine());
        
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
        
    
    def displaySignal(self, T):
        
        # plot scope traces
        
        # signal to display
        self.a1 = T[0]
        self.a2 = T[1]
        
        # display
        l=len(self.a1)
        self.curve1.setData([0.0,0.0], [0.0,0.0])
        self.curve2.setData(self.ti[0:l], self.a2[:l])
        self.replot()


def updateDisplay():
    
    # test if there is a new portion of signal
    # to display
    if SR.newAudio :
        
        # get signal and display it
        T = SR.getSignalForScope()
        scope.displaySignal(T)

        # this portion of signal have been displayed        
        SR.newAudio = False

if __name__ == "__main__" :
    """ Test of Signal class """
    
    # signal properties
    rate       = 44100
    size       = 4096

    # create a new signal ready to be displayed in the scope
    SR = Signal(rate, size)
    SR.continuousStart() # signal SR = current sound card record
                         # at any time

    # create a scope window
    app         = Qt.QApplication(sys.argv)
    mainWindow  = Qt.QMainWindow()
    scope       = Scope(rate, size)
    
    # display continuous signal
    timer = QtCore.QTimer()
    timer.start(1.0)
    mainWindow.connect(timer, QtCore.SIGNAL('timeout()'), updateDisplay)
    
    #show all the graphical stuff
    scope.show()
    app.exec_()
    
    # close the signal
    SR.stopSignalStream()



        
        
            