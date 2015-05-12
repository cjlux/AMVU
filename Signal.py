#!/usr/bin/env python
from __future__ import division

"""
    Class for signal management
    
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

# Version 0.8
# Last update : 05/05/2015

import pyaudio
import numpy
import wave
from threading import Thread
import time as t
from PyQt4 import Qt
from PyQt4 import QtCore
from PyQt4 import Qwt5 as Qwt


class Signal():
    """ Signal provided by the soundcard """

    def __init__(self, rate, size, format = pyaudio.paInt16, channel = 2) :
        """
        Open a stream from the sound card
        /!\ All the attributes are public for the moment
        If you want to access them without setters or getters, be careful
        """
        
        # state of recording
        self.threadsDieNow  = False
        self.newAudio       = False
        
        # processus used to record signal
        self.recordingProcess = None
        
        # signal characteristics
        self.rate           = rate
        self.size           = size
        self.channel        = channel
        self.format         = format
        self.offset         = 0
        
        # sound acquisition
        self.soundCardLink    = pyaudio.PyAudio()
        self.soundCardStream  = self.soundCardLink.open( format   = self.format, 
                                                channels          = self.channel,
                                                input             = True,
                                                rate              = rate,
                                                frames_per_buffer = size)
        
        # current signal portion
        self.signalPart  = numpy.empty(self.size*self.channel,dtype=numpy.int16)  
        
        # time signal under it's primar form <=> all the signal portions since a signal object creation
        self.timeSignal         = []
        # time signal under its frequential form
        self.frequentialSignal  = []
        
    def setTimeSignal(self, newTimeSignal):
        """ set the time and frequential signal from a new time signal"""
        self.timeSignal = newTimeSignal
        self.freqSignal = getFreqSignalFromTimeSignal(newTimeSignal)
        
    def setFreqSignal(self, newFreqSignal):
        """ set the time and frequential signal from a new frequential signal """
        self.freqSignal = newFreqSignal
        self.timeSignal = getTimeSignalFromFreqSignal(newFreqSignal)
    
    def startRecording(self, time=None):
        """
        Start to record signal parts in timeSignal for time second if time is given
        """
        self.recordingProcess = Thread(target=self.record)
        self.recordingProcess.start()
        
        # if time given, stop recording when time is reached
        if time!=None :
            t.sleep(time)
            self.stopRecording()
            
    def __updateTriggerAnalysis(self, step, signalPartsRecording):
        """
        This function may not be called by class user.
        Else it will probably cause huge dammages, like
        end of the world, big explosions, etc...
        
        Analyse a signal part to see if the trigger
        is set off.
        If it is, the signal start to be recorded.
        If not, the signal is not recorded.
        """
        
        # ready to record
        self.threadsDieNow  = False
        isTriggerSetOff     = False
        
        while not(isTriggerSetOff) :
            
            # test if there is a new portion of signal
            # to analyze
            if self.newAudio :
            
                # analyse signal part
                for i in range(self.signalPart.size):
                    # test if the current value is enough
                    # to set off the trigger
                    if (self.signalPart[i]>step) :
                        # trigger is set off
                        
                        print "[startTrigger] start recording"
    
                        # end of signal parts recording
                        # and trigger analysis
                        signalPartsRecording.Terminated = True
                        isTriggerSetOff = True
                        
                        # start recording the signal
                        self.timeSignal.append(numpy.copy(self.signalPart))
                        self.startRecording()
                        break
        
                # this portion of signal have been analyzed      
                self.newAudio = False
            
    #
    # TODO : need to optimize
    #
    def startTrigger(self, step, time=None):
        """
        Start to record signal when a step amplitude is
        reached by the signal for time second(s). If no time
        is given, the trigger stop when threadsDieNow is true.
        
        Analyse a signal part to see if the trigger
        is set off.
        If it is, the signal start to be recorded.
        If not, the signal is not recorded.
        """
        
        print "[startTrigger("+str(step)+")]"
        
        # start signal parts recording
        signalPartsRecording = Thread(target=self.__recordSignalPart)
        signalPartsRecording.start()
        
        # signal analysis to start recording when trigger is set off
        triggerAnalysis = Thread(target=self.__updateTriggerAnalysis(step, signalPartsRecording))
        triggerAnalysis.start()
        
        # if time given, stop recording when time is reached
        if time!=None :
            t.sleep(time)
            self.stopRecording()
    
    def stopRecording(self):
        """ Stop any recording currently running """
        self.threadsDieNow=True
        
    def getLastSignalRecordedPart(self):
        """
        Return the last recorded signal part
        * If channel number is 1   : an array of an array containing the signal values is returned
        * If channel number is 2   : an array of two arrays containing each one a channel signal values is returned
        * If channel number is n>2 : it will probably explode
        Note : this currently work by formating int16 audio data
        """
        
        # format the last recorded signal part and give it back
        return Signal.getWellFormatedSignal(self.signalPart, self.channel)
    
    def getWellFormattedTimeSignal(self):
        """
        Return time signal on an adapted form to display it
        * If channel number is 1   : an array of an array containing the signal values is returned
        * If channel number is 2   : an array of two arrays containing each one a channel signal values is returned
        * If channel number is n>2 : it will probably explode
        Note : this currently work by formating int16 audio data
        """

        # x represent all the recorded time signal 
        x = numpy.empty(len(self.timeSignal)*self.size*self.channel,dtype=numpy.int16)
       
        # fill in x with signal values
        for i in range(len(self.timeSignal)):
            x[i*self.size*self.channel:(i+1)*self.size*self.channel] = self.timeSignal[i][0:self.size*self.channel] 
        
        # format x and give it back
        return Signal.getWellFormatedSignal(x, self.channel)
    
    def getWellFormattedFreqSignal(self):
        """
        Return frequential signal on an adapted form to display it
        * If channel number is 1   : an array of an array containing the signal values is returned
        * If channel number is 2   : an array of two arrays containing each one a channel signal values is returned
        * If channel number is n>2 : it will probably explode
        Note : this currently work by formating int16 audio data
        """
        
        # x represent all the recorded frequential signal 
        x = numpy.empty(len(self.frequentialSignal)*self.size*self.channel,dtype=numpy.int16)
       
        # fill in x with signal values
        for i in range(len(self.frequentialSignal)):
            x[i*self.size*self.channel:(i+1)*self.size*self.channel] = self.frequentialSignal[i][0:self.size*self.channel] 
        
        # format x and give it back
        return Signal.getWellFormatedSignal(x, self.channel)
    
    #
    # = Under development ================
    #
    def getBPFilteredTimeSignal(self, w0, w1):
        """
        Return band pass filtered time signal in a new signal object
        w0 and w1 stand for the cutoff frequencies.
        * If channel number is 1   : an array of an array containing the signal values is returned
        * If channel number is 2   : an array of two arrays containing each one a channel signal values is returned
        * If channel number is n>2 : it will probably explode
        """
        
        # filtering signalParts
        
        # [...]
        # Filtering stuff
        # [...]
        #filteredSignalParts = numpy.array(...)
        
        # create a new signal object containing the filtered signal result
        filteredSignal = Signal(self.rate, self.size, self.format, self.channel)
        filteredSignal.setTimeSignal(filteredSignalParts)
        
        return filteredSignal
    
    #
    # = Under development ================
    #    
    def getBPFilteredFreqSignal(self, w0, w1):
        """
        Return band pass filtered frequential signal in a new signal object
        w0 and w1 stand for the cutoff frequencies.
        * If channel number is 1   : an array of an array containing the signal values is returned
        * If channel number is 2   : an array of two arrays containing each one a channel signal values is returned
        * If channel number is n>2 : it will probably explode
        """
        
        # filtering signalParts
        
        # [...]
        # Filtering stuff
        # [...]
        #filteredSignalParts = numpy.array(...)
        
        # create a new signal object containing the filtered signal result
        filteredSignal = Signal(self.rate, self.size, self.format, self.channel)
        filteredSignal.setTimeSignal(filteredSignalParts)
        
        return filteredSignal
    
    #
    # = Under development ================
    #
    def getLPFilteredTimeSignal(self, w0):
        """
        Return low pass time time signal in a new signal object
        w0 stands for the cutoff frequency.
        * If channel number is 1   : an array of an array containing the signal values is returned
        * If channel number is 2   : an array of two arrays containing each one a channel signal values is returned
        * If channel number is n>2 : it will probably explode
        """
        
        # filtering signalParts
        
        # [...]
        # Filtering stuff
        # [...]
        #filteredSignalParts = numpy.array(...)
        
        # create a new signal object containing the filtered signal result
        filteredSignal = Signal(self.rate, self.size, self.format, self.channel)
        filteredSignal.setTimeSignal(filteredSignalParts)
        
        return filteredSignal
    
    #
    # = Under development ================
    #
    def getLPFilteredFreqSignal(self, w0):
        """
        Return low pass filtered frequential signal in a new signal object
        w0 stands for the cutoff frequency.
        * If channel number is 1   : an array of an array containing the signal values is returned
        * If channel number is 2   : an array of two arrays containing each one a channel signal values is returned
        * If channel number is n>2 : it will probably explode
        """
        
        # filtering signalParts
        
        # [...]
        # Filtering stuff
        # [...]
        #filteredSignalParts = numpy.array(...)
        
        # create a new signal object containing the filtered signal result
        filteredSignal = Signal(self.rate, self.size, self.format, self.channel)
        filteredSignal.setTimeSignal(filteredSignalParts)
        
        return filteredSignal
    
    #
    # = Under development ================
    #
    def getHPFilteredTimeSignal(self, w0):
        """
        Return high pass filtered time signal in a new signal object
        w0 stands for the cutoff frequency.
        * If channel number is 1   : an array of an array containing the signal values is returned
        * If channel number is 2   : an array of two arrays containing each one a channel signal values is returned
        * If channel number is n>2 : it will probably explode
        """
        
        # filtering signalParts
        
        # [...]
        # Filtering stuff
        # [...]
        #filteredSignalParts = numpy.array(...)
        
        # create a new signal object containing the filtered signal result
        filteredSignal = Signal(self.rate, self.size, self.format, self.channel)
        filteredSignal.setTimeSignal(filteredSignalParts)
        
        return filteredSignal
    
    #
    # = Under development ================
    #
    def getHPFilteredFreqSignal(self, w0):
        """
        Return high pass filtered filtered signal in a new signal object
        w0 stands for the cutoff frequency.
        * If channel number is 1   : an array of an array containing the signal values is returned
        * If channel number is 2   : an array of two arrays containing each one a channel signal values is returned
        * If channel number is n>2 : it will probably explode
        """
        
        # filtering signalParts
        
        # [...]
        # Filtering stuff
        # [...]
        #filteredSignalParts = numpy.array(...)
        
        # create a new signal object containing the filtered signal result
        filteredSignal = Signal(self.rate, self.size, self.format, self.channel)
        filteredSignal.setTimeSignal(filteredSignalParts)
        
        return filteredSignal
    
    #
    # = Under development ================
    #
    def exportWavFormat(self):
        """
        Create a exportedSignal.wav file to store the recorded signal  
        """
        print "[ExportWaveFormat]"
        wavefile = wave.open("exportedSignal.wav", 'w')
        
        # set format characteristics
        wavefile.setnchannels(self.channel)
        wavefile.setframerate(self.rate)
        wavefile.setsampwidth(self.format)
        
        # record signal
        wavefile.writeframes(self.timeSignal)
        
        wavefile.close()
        
    #-------------------------------------------------------------
    #
    # Utilities methods
    #
    #-------------------------------------------------------------
    def getStream(self):
        """ Return the stream used for the current signal """
        return self.soundCardStream
    
    def startSignalStream(self):
        """ Start the stream used for the current signal """
        self.soundCardStream.start_stream()
    
    def stopSignalStream(self):
        """ Stop the stream used for the current signal """
        self.soundCardStream.stop_stream()
        
    def closeSignalStream(self):
        """ Close the stream used for the current signal """
        self.soundCardStream.close_signal()

    def getSignalInfo(self):
        """ Give some information about the signal """
        return "Rate : "+str(self.rate)+" | Size : "+str(self.size)
    
    def readStream(self, n):
        """ Read n value from the stream of the current signal"""
        return self.soundCardStream.read(n)
    
    def readSignal(self,n) :
        """ Read some data from this signal """
        try :
            dataCollected = self.soundCardStream.read(n)
            return numpy.fromstring(dataCollected,dtype=numpy.int16)
        except IOError :
            return self.readSignal(n)
        
    @staticmethod    
    def getWellFormatedSignal(signal, channel):
        """
        Return a signal on an adapted form to display it
        * If channel number is 1   : an array of an array containing the signal values is returned
        * If channel number is 2   : an array of two arrays containing each one a channel signal values is returned
        * If channel number is n>2 : it will probably explode
        """
        
        # display the current portion of signal
        cal  = 1./65536.0
        P    = numpy.array(signal, dtype='d')*cal  # 'd' -> double
        
        # return what the user ask for depending on the channel numbers
        if channel == 2 :
            R, L = P[0::2], P[1::2]
            L -= L.mean()
            R -= R.mean()
            return [L,R]
        else :
            return [P]
        
    @staticmethod
    def getFreqSignalFromTimeSignal(timeSignalToConvert):
        """ Return the frequential signal corresponding to a time signal """
        return numpy.fft(timeSignalToConvert)
        
    @staticmethod    
    def getTimeSignalFromFreqSignal(freqSignalToConvert):
        """ Return the time signal corresponding to a frequential signal """
        return numpy.ifft(freqSignalToConvert)
    
    
    
    #-------------------------------------------------------------
    #
    # Deprecated methods
    #
    #-------------------------------------------------------------
    
    #def getRecordedSignal(self):
    #    """ Give the whole recorded signal """
    #    
    #    # x represent all the recorded signal 
    #    x = numpy.empty(len(self.timeSignal)*self.size*self.channel,dtype=numpy.int16)
    #   
    #    # format x
    #    for i in range(len(self.timeSignal)):
    #        x[i*self.size*self.channel:(i+1)*self.size*self.channel] = self.timeSignal[i][0:self.size*self.channel] 
    # 
    #     return x
    
    #def getSignalForScope(self):
    #    """ return an array containing formated signal for scope display """
    #    # display all the recorded signal on the command line terminal
    #    x = self.getRecordedSignal()
    #    print "Signal (size : "+str(len(x))+")   : "+str(x)
    #    print "Signal part (size : "+str(len(self.signalPart))+") : "+str(self.signalPart)
    #    print "-------------"
    #    
    #    # display the current portion of signal
    #    cal  = 1./65536.0
    #    P    = numpy.array(self.signalPart, dtype='d')*cal  # 'd' -> double
    #    R, L = P[0::2], P[1::2]
    #
    #    L -= L.mean()
    #    R -= R.mean()
    #    return [L,R]
    
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
            self.signalPart[0:self.size*self.channel] = self.readSignal(self.size)
            self.timeSignal.append(numpy.copy(self.signalPart))
            
            # this portion of signal is new and doesn't have been displayed
            # to the user
            self.newAudio=True
            
    def __recordSignalPart(self):
        """ Record only parts of signal """
        
        # daemon recording as fast as it can the data from the sound card
        while not(self.threadsDieNow):
            
            # all the readings from the sound card are recorder as signal portions
            self.signalPart[0:self.size*self.channel] = self.readSignal(self.size)
            
            # this portion of signal is new and doesn't have been displayed
            # to the user
            self.newAudio=True
    

    #def continuousStart(self):
    #    """ CALL THIS to start running forever."""
    #    self.t = Thread(target=self.record)
    #    self.t.start()
        
    #def continuousEnd(self):
    #    """ Shut down continuous recording."""
    #    self.threadsDieNow=True

    # ------------------------------------------------------

    
    


    




