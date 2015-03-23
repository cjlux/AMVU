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
# Last update : 23/03/2015 16:31

import pyaudio
import numpy
from threading import *
import time
from PyQt4 import Qt
from PyQt4 import Qwt5 as Qwt


class Signal():
    """ Signal provided by souncard """

    def __init__(self, rate, size) :
        """ Open a stream from the sound card and start it"""
        pyAudio = pyaudio.PyAudio()
        self.stream  = pyAudio.open( format            = pyaudio.paInt16, 
                                     channels          = 2,
                                     input             = True,
                                     rate              = rate,
                                     frames_per_buffer = size)
        self.stream.start_stream()
        
    def getStream(self):
        return self.stream
        
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

    def readSignal(self,n) :
        """ Read some data from this signal """
        dataCollected = self.stream.read(n)
        return numpy.fromstring(dataCollected,dtype=numpy.int16)
    
    def displayStream(self):
        """ Read and display all the stream """
        self.audioStream2 = self.readSignal(2048)
        time.sleep(0.5)
        self.printStream()
        
    def printStream(self):
        """ Print the stream in the command line """
        print "[printStream] Plot stream "
        print str(self.audioStream2)
        
    def printBufferTotal(self):
        print "[printBufferTotal] Print expended buffer"
        print str(self.bufferTotal)
    
    
    def stopSignal(self):
        """ Close the stream providing the signal """
        self.stream.stop_stream()
        self.stream.close()
        #pyaudio.terminate()
    
    def printSignal(self):
        """ Print the buffer in the command line """
        print "[printSignal] Plot signal "
        print str(self.audioStream)




