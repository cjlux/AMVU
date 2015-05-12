#!/usr/bin/env python
from __future__ import division

"""
    Scope to visualize signal and test AMVU application
    
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
# Last update : 06/05/2015

import pyqtgraph as pg

import sys

from PyQt4 import Qt
from PyQt4 import QtCore
from PyQt4 import Qwt5 as Qwt

from Signal import Signal
from SignalFrame import SignalFrame

class Scope(Qt.QMainWindow):
    
    def __init__(self, signalFrame, rate, size, *args):
        
        Qt.QMainWindow.__init__(self)
        self.signalFrame = signalFrame
        
        # Graphic user interface
        #apply(Qwt.QwtPlot.__init__, (self,) + args)
        #self.setFixedSize(800,400)
        
    
    def displaySignal(self, T):
        
        print "[Oh yeah, I update]"
        # signal to display
        #self.a1 = T[0]
        #self.a2 = T[1]
        
        # display
        #l=len(self.a1)
        #self.curve1.setData([0.0,0.0], [0.0,0.0])
        #self.curve2.setData(self.ti[0:l], self.a2[:l])
        #self.replot()


def updateDisplay():
    
    # test if there is a new portion of signal
    # to display
    if (SCOPE.signalFrame.signalList[SCOPE.signalFrame.currentSignal].newAudio and not(SCOPE.signalFrame.signalList[SCOPE.signalFrame.currentSignal].threadsDieNow)) :
        
        # get signal and display it
        T = SCOPE.signalFrame.signalList[SCOPE.signalFrame.currentSignal].getLastSignalRecordedPart()
        #print "[Display signal]"
        SCOPE.displaySignal(T)

        # this portion of signal have been displayed        
        SCOPE.signalFrame.signalList[SCOPE.signalFrame.currentSignal].newAudio = False
        
def seeRecord():
    
    # stop current signal acquisition
    SCOPE.signalFrame.signalList[SCOPE.signalFrame.currentSignal].threadsDieNow = True
    
    # display recorded signal
    signalToDisplay = SR.getWellFormatedTimeSignal()[0]
    print "[Display recorded signal]"
    pg.plot(signalToDisplay) 


def launchTrigger():
    
    # set the default value for the trigger
    triggerStep = 12222
    
    # launch the trigger
    SCOPE.signalFrame.signalList[SCOPE.signalFrame.currentSignal].startTrigger(triggerStep, 4)
    
def exportFile():
    SCOPE.signalFrame.signalList[SCOPE.signalFrame.currentSignal].exportWavFormat()

    
def startRecord():
    
    # restart current signal acquisition
    SCOPE.signalFrame.signalList[SCOPE.signalFrame.currentSignal].threadsDieNow = False
    
    # restart signal recording
    SCOPE.signalFrame.signalList[SCOPE.signalFrame.currentSignal].startRecording() # signal SR = current sound card record
                        # at any time
    #SR.startTrigger()
    
    # display continuous signal
    timer = QtCore.QTimer()
    timer.start(1.0)
    SCOPE.connect(timer, QtCore.SIGNAL('timeout()'), updateDisplay)

if __name__ == "__main__" :
    """ Test of Signal class """
    
    # signal properties
    rate       = 8192   #44100
    size       = 2048    #4096

    # create a scope window
    app = Qt.QApplication(sys.argv)
    
    # create a new signal ready to be displayed in the scope
    firstSignal = Signal(rate, size)
    signalFrame = SignalFrame()
    signalFrame.consider(firstSignal)
    
    # create the scope
    SCOPE = Scope(signalFrame, rate, size)
    
    # affect a first signal to this scope
    SCOPE.signalFrame.consider(firstSignal)
    SCOPE.signalFrame.displayLastSignal()
    
    #SCOPE.signalFrame.timeScope # qwtplot
    #SCOPE.signalFrame.freqScope # qwtplot
    #SCOPE.signalFrame.signalList[SCOPE.signalFrame.currentSignal]
    
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
    SCOPE.addToolBar(toolBar)
    
    # display continuous signal
    timer = QtCore.QTimer()
    timer.start(1.0)
    SCOPE.connect(timer, QtCore.SIGNAL('timeout()'), updateDisplay)
    
    #show all the graphical stuff
    #SCOPE.setCentralWidget(SCOPE.signalFrame.timeScope)
    SCOPE.show()
    SCOPE.signalFrame.timeScope.show()
    app.exec_()
    
    # close the signal
    SCOPE.signalFrame.signalList[SCOPE.signalFrame.currentSignal].threadsDieNow = True
    SCOPE.signalFrame.signalList[SCOPE.signalFrame.currentSignal].stopSignalStream()



        
        
            