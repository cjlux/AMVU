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

# Version 1.0
# Last update : 01/04/2015

import pyaudio
import sys
import numpy as np

import pyqtgraph as pg

from PyQt4 import Qt
from PyQt4 import QtCore
from PyQt4 import Qwt5 as Qwt

from signalLast import Signal

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
        self.setFixedSize(800,400)
        
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
        
        
        # INIT GUI()
    
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
    if (SR.newAudio and not(SR.threadsDieNow)) :
        
        # get signal and display it
        T = SR.getLastSignalRecordedPart()
        #print "[Display signal]"
        SCOPE.displaySignal(T)

        # this portion of signal have been displayed        
        SR.newAudio = False
        
def seeRecord():
    
    # stop current signal acquisition
    SR.threadsDieNow = True
    
    # display recorded signal
    signalToDisplay = SR.getWellFormatedTimeSignal()[0]
    print "[Display recorded signal]"
    pg.plot(signalToDisplay) 


def launchTrigger():
    
    # set the default value for the trigger
    triggerStep = 12222
    
    # launch the trigger
    SR.startTrigger(triggerStep, 4)
    
def exportFile():
    SR.exportWavFormat()

    
def startRecord():
    
    # restart current signal acquisition
    SR.threadsDieNow = False
    
    # restart signal recording
    SR.startRecording() # signal SR = current sound card record
                        # at any time
    #SR.startTrigger()
    
    # display continuous signal
    timer = QtCore.QTimer()
    timer.start(1.0)
    MAINWINDOW.connect(timer, QtCore.SIGNAL('timeout()'), updateDisplay)

if __name__ == "__main__" :
    """ Test of Signal class """
    
    # signal properties
    rate       = 8192   #44100
    size       = 2048    #4096

    # create a new signal ready to be displayed in the scope
    SR  = Signal(rate, size)
    
    # start signal recording
    #SR.startRecording()  # signal SR = current sound card record
                         # at any time

    # create a scope window
    app         = Qt.QApplication(sys.argv)
    MAINWINDOW  = Qt.QMainWindow()
    SCOPE       = Scope(rate, size)
    
    startRecord()
    
    # create a button to continue recording the signal
    button2 = Qt.QPushButton("Continue record")
    button2.clicked.connect(startRecord)
    button2.show()
    
    # create a button to start with a trigger
    button1 = Qt.QPushButton("Start trigger")
    button1.clicked.connect(launchTrigger)
    button1.show()
    
    # create a button to display recorded signal
    button = Qt.QPushButton("See recorded signal")
    button.clicked.connect(seeRecord)
    button.show()
    
    # create a button to export signal in wave file
    button3 = Qt.QPushButton("Export .wav")
    button3.clicked.connect(exportFile)
    button3.show()
    
    # display this buttons on a toolbar
    toolBar = Qt.QToolBar()
    toolBar.addWidget(button)
    toolBar.addWidget(button1)
    toolBar.addWidget(button2)
    toolBar.addWidget(button3)
    MAINWINDOW.addToolBar(toolBar)
    
    # display continuous signal
    timer = QtCore.QTimer()
    timer.start(1.0)
    MAINWINDOW.connect(timer, QtCore.SIGNAL('timeout()'), updateDisplay)
    
    #show all the graphical stuff
    MAINWINDOW.setCentralWidget(SCOPE)
    MAINWINDOW.show()
    SCOPE.show()
    app.exec_()
    
    # close the signal
    SR.threadsDieNow = True
    SR.stopSignalStream()



        
        
            