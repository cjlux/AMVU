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

# Version 0.3
# Last update : 30/03/2015

import pyaudio
import numpy
from threading import Thread
import time
from PyQt4 import Qt
from PyQt4 import Qwt5 as Qwt


class Signal():
    """ Signal provided by the soundcard """

    def __init__(self, rate, size) :
        """ Open a stream from the sound card """
        
        # state of recording
        self.threadsDieNow  = False
        self.newAudio       = False
        
        # signal characteristics
        self.rate           = rate
        self.size           = size
        self.signalPartSize = 1    # Size of a signal portion.
                                   # A signal portion is what will be
                                   # dynamically displayed if we choose
                                   # to show the signal with
                                   # a scope object for example
        self.channel        = 2
        
        self.pyAudio = pyaudio.PyAudio()
        self.stream  = self.pyAudio.open( format            = pyaudio.paInt16, 
                                          channels          = self.channel,
                                          input             = True,
                                          rate              = rate,
                                          frames_per_buffer = size)
        
        # current signal portion
        self.signalPart  = numpy.empty(self.signalPartSize*self.size*self.channel,dtype=numpy.int16)  
        
        # all the signal portions since a signal object creation 
        # <=> represent all the signal
        self.signalParts = []
        
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
    
    def getRecordedSignal(self):
        """ Give the whole recorded signal """
        
        # x represent all the recorded signal 
        x = numpy.empty(len(self.signalParts)*self.signalPartSize*self.size*self.channel,dtype=numpy.int16)
       
        # format x
        for i in range(len(self.signalParts)):
            x[i*self.signalPartSize*self.size*self.channel:(i+1)*self.signalPartSize*self.size*self.channel] = self.signalParts[i][0:self.signalPartSize*self.size*self.channel] 
    
        return x
    
    #
    # Deprecated due to the use of pyqtgraph instead of Qwt
    # to plot the whole recorded signal ---
    #
    
#    def getRecordedSignalForScope(self):
#        """ return an array containing the formated signal for scope display """
#        
#        cal  = 1./65536.0
#        P    = numpy.array(self.getRecordedSignal(), dtype='d')*cal  # 'd' -> double
#        R, L = P[0::2], P[1::2]

#        L -= L.mean()
#        R -= R.mean()
#        return [L,R]

    # -------------------------------------
    
    
    def getSignalForScope(self):
        """ return an array containing formated signal for scope display """

        # display all the recorded signal on the command line terminal
        x = self.getRecordedSignal()
        print "Signal (size : "+str(len(x))+")   : "+str(x)
        print "Signal part (size : "+str(len(self.signalPart))+") : "+str(self.signalPart)
        print "-------------"
        
        # display the current portion of signal
        cal  = 1./65536.0
        P    = numpy.array(self.signalPart, dtype='d')*cal  # 'd' -> double
        R, L = P[0::2], P[1::2]

        L -= L.mean()
        R -= R.mean()
        return [L,R]
    
    #
    # Adapted for this class from swharden work at
    # http://www.swharden.com/blog/2013-05-09-realtime-fft-audio-visualization-with-python/
    #    
    # ------------------------------------------------------
    def record(self):
        """ Record a sample of audio."""
        
        # daemon recording as fast as it can the data from the sound card
        while not(self.threadsDieNow):
            
            # all the readings from the sound card are recorder as signal portions
            # TODO : Optimise by recording immediatly the readSignal(...) result in signalParts ?
            for i in range(self.signalPartSize):
                self.signalPart[i*self.size*self.channel:(i+1)*self.size*self.channel] = self.readSignal(self.size)

            self.signalParts.append(numpy.copy(self.signalPart))
            
            # this portion of signal is new and doesn't have been displayed
            # to the user
            self.newAudio=True

    def continuousStart(self):
        """ CALL THIS to start running forever."""
        self.t = Thread(target=self.record)
        self.t.start()
        
    def continuousEnd(self):
        """ Shut down continuous recording."""
        self.threadsDieNow=True

    # ------------------------------------------------------

    
    def readStream(self, n):
        """ Read n value from the stream of the current signal"""
        return self.stream.read(n)

    def readSignal(self,n) :
        """ Read some data from this signal """
        try :
            dataCollected = self.stream.read(n)
            return numpy.fromstring(dataCollected,dtype=numpy.int16)
        except IOError :
            return self.readSignal(n)
    
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
    




