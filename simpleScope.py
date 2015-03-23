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

# Version 0.1
# Last update : 23/03/2015 16:31

import pyaudio
import sys
import numpy as np
from PyQt4 import Qt
from PyQt4 import Qwt5 as Qwt

from testStream import Signal

class Scope(Qwt.QwtPlot):
    
    def __init__(self, signal, rate, size, *args):
        
        # signal characteristics
        self.size = size
        self.rate = rate
        self.dt   = 1./rate
        self.ti   = np.arange(0.0, 1.0, self.dt)
        self.a1   = 0.0*self.ti
        self.a2   = 0.0*self.ti
        self.signal = signal
        
        
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
        self.setAxisMaxMajor(Qwt.QwtPlot.xBottom, 10);
        self.setAxisMaxMinor(Qwt.QwtPlot.xBottom, 0);

        self.setAxisScaleEngine(Qwt.QwtPlot.yRight, Qwt.QwtLinearScaleEngine());
        self.setAxisMaxMajor(Qwt.QwtPlot.yLeft, 10);
        self.setAxisMaxMinor(Qwt.QwtPlot.yLeft, 0);
        self.setAxisMaxMajor(Qwt.QwtPlot.yRight, 10);
        self.setAxisMaxMinor(Qwt.QwtPlot.yRight, 0);
        
        
        
        # curves for scope traces: 2 first so 1 is on top
        PENWIDTH = 1
        self.curve2 = Qwt.QwtPlotCurve('Trace2')
        self.curve2.setPen(Qt.QPen(Qt.Qt.magenta,PENWIDTH))
        self.curve2.setYAxis(Qwt.QwtPlot.yRight)
        self.curve2.attach(self)

        self.curve1 = Qwt.QwtPlotCurve('Trace1')
        self.curve1.setPen(Qt.QPen(Qt.Qt.blue,PENWIDTH))
        self.curve1.setYAxis(Qwt.QwtPlot.yLeft)
        self.curve1.attach(self)
        
        # curve display initialisation
        self.curve1.setData(self.ti, self.a1)
        self.curve2.setData(self.ti, self.a2)
        
    
    def displaySignal(self):
        
        # plot scope traces
        # basically, there is only 2 channels
        l=len(self.a1)
        self.curve1.setData([0.0,0.0], [0.0,0.0])
        self.curve2.setData(self.ti[0:l], self.a2[:l])
        self.replot()
        
    def startScope(self):
        
        # get signal
        self.signalStream = self.signal.getStream()
        
        x = self.signalStream.read(self.size)
        X = np.fromstring(x, dtype='h') # 'h' -> signed short

        cal = 1./65536.0
        P = np.array(X, dtype='d')*cal  # 'd' -> double
        R, L = P[0::2], P[1::2]
        lenR = len(R)

        L -= L.mean()
        R -= R.mean()
        self.a1 = R
        self.a2 = L
        self.displaySignal()


def main():
    
    # signal properties
    rate       = 44100
    size       = 1024

    # create a new signal
    signal = Signal(rate, size)

    # create a scope window to display the signal
    app  = Qt.QApplication(sys.argv)
    f = Scope(signal, rate, size)
    #f.displaySignal()
    
    f.startScope()

    f.show()
    app.exec_()
    
if __name__ == "__main__" :
    """ Test of Signal class """
    main()



        
        
            