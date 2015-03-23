#!/usr/bin/env python
from __future__ import division

"""
    Class for signal management 
    
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
# Last update : 23/03/2015 22:13

import pyaudio
import numpy
from threading import *
import time
from PyQt4 import Qt
from PyQt4 import Qwt5 as Qwt


class Signal():
    """ Signal provided by the soundcard """

    def __init__(self, rate, size) :
        """ Open a stream from the sound card """
        self.rate = rate
        self.size = size
        
        pyAudio = pyaudio.PyAudio()
        self.stream  = pyAudio.open( format            = pyaudio.paInt16, 
                                     channels          = 2,
                                     input             = True,
                                     rate              = rate,
                                     frames_per_buffer = size)
        
    def getStream(self):
        """ Return the stream used for the current signal """
        return self.stream
    
    def startSignalStream(self):
        """ Start the stream used for the current signal """
        self.stream.start_stream()
    
    def stopSignalStream(self):
        """ Stop the stream used for the current signal """
        self.stream.stop_stream()
        
    def closeSignalStream(self):
        """ Close the stream used for the current signal """
        self.stream.close_signal()

    def getSignalInfo(self):
        """ Give some information about the signal """
        return "Rate : "+str(self.rate)+" | Size : "+str(self.size)
    
    def getSignalForScope(self):
        """ return an array containing formated signal for scope display """
        X = self.readSignal(self.size)
        cal = 1./65536.0
        P = numpy.array(X, dtype='d')*cal  # 'd' -> double
        R, L = P[0::2], P[1::2]
        lenR = len(R)

        L -= L.mean()
        R -= R.mean()
        return [L,R]
    
        
    def displayContinuousSignal(self):
        """ Display a part of the stream every seconds"""
        bite = 0
        self.bufferTotal = []
        while True :
            self.audioStream = self.readSignal(8)
            self.printSignal()
            self.bufferTotal.extend(self.audioStream)
            bite = bite + 1
            if bite==10 : break
            
        #time.sleep(0.5)
        #self.displayContinuousSignal()
        #t1 = Timer(1.0, self.displayContinuousSignal)
        #t1.start()
    
    def readStream(self, n):
        """ Read n value from the stream of the current signal"""
        return self.stream.read(n)

    def readSignal(self,n) :
        """ Read some data from this signal """
        dataCollected = self.stream.read(n)
        return numpy.fromstring(dataCollected,dtype=numpy.int16)
    
    def displayStream(self):
        """ Read and display all the stream """
        print "[displayStream] Acquisition du signal"
        self.audioStream2 = self.readSignal(2048)
        print "[displayStream] Lecture du signal"
        time.sleep(0.5)
        print "[displayStream] Affichage du signal"
        self.printStream()
        
    def printStream(self):
        """ Print the stream in the command line """
        print "[printStream] Plot stream "
        print str(self.audioStream2)
    




