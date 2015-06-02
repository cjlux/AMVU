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

# Version 0.9
# Last update : 13/05/2015

import pyaudio
import numpy
import wave
from threading import Thread
import time as t
from PyQt4 import Qt
from PyQt4 import QtCore
from PyQt4 import Qwt5 as Qwt

from scipy.fftpack import fft, fftfreq, ifft, rfft, irfft, rfftfreq


class Signal():
    """ Signal provided by the soundcard """

    def __init__(self, rate, size, format = pyaudio.paInt16, channel = 2) :
        """
        Open a stream from the sound card
        /!\ All the attributes are public for the moment
        If you want to access them without setters or getters, be carefull
        """
        
        print "[New signal] Size "+str(size)+", rate "+str(rate)
        
        # state of recording
        self.threadsDieNow        = False
        self.stopRecordingSignal  = False
        self.newAudio             = False
        self.hasStartedRecording  = False
        
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
        
        # recording time
        self.recordingTime = 0
        
    def setTimeSignal(self, newTimeSignal):
        """ set the time and frequential signal from a new time signal"""
        self.timeSignal = newTimeSignal
        self.frequentialSignal = getFreqSignalFromTimeSignal(newTimeSignal)
        
    def setFreqSignal(self, newFreqSignal):
        """ set the time and frequential signal from a new frequential signal """
        self.frequentialSignal = newFreqSignal
        self.timeSignal = getTimeSignalFromFreqSignal(newFreqSignal)
    
    def startRecording(self, time=None):
        """
        Start to record signal parts in timeSignal for time second if time is given
        """
        print "[Signal] Start recording"
        
        self.stopRecordingSignal = False
        self.hasStartedRecording = True
        
        self.startRecordingTime = t.time()
        
        self.recordingProcess = Thread(target=self.record)
        self.recordingProcess.start()
        
        # if time given, stop recording when time is reached
        if time!=None :
            t.sleep(time)
            self.stopRecording()
            
    def __updateTriggerAnalysis(self, step):
        """
        This function may not be called by class user.
        Else it will probably cause huge dammages, like
        end of the world, big explosions, etc...
        
        Analyse a signal part to see if the trigger
        is set off.
        If it is, the signal start to be recorded.
        If not, the signal is not recorded.
        """

        print "[Trigger] Wait for a suffisant signal"
        
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
                        
                        print "[Trigger] start recording"
    
                        # end of signal parts recording
                        # and trigger analysis
                        self.threadsDieNow  = True
                        isTriggerSetOff     = True
                        
                        # start recording the signal
                        # acquisition will be done at the same time for
                        # frenquential and time signal
                        self.timeSignal.append(numpy.copy(self.signalPart))
                        self.frequentialSignal.append(Signal.getFreqSignalFromTimeSignal(numpy.copy(self.signalPart)))
                        self.startRecording()
                        
                        break
        
                # this portion of signal have been analyzed      
                self.newAudio = False

        print "[Trigger] end of the function"

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
        self.signalPartsRecording = Thread(target=self.__recordSignalPart)
        self.signalPartsRecording.start()
        
        # signal analysis to start recording when trigger is set off
        self.triggerAnalysis = Thread(target=self.__updateTriggerAnalysis(step))
        self.triggerAnalysis.start()
        
        # if time given, stop recording when time is reached
        if time!=None :
            t.sleep(time)
            self.stopRecording()
    
    def stopRecording(self):
        """ Stop any recording currently running """
        print "[Signal] Stop recording"
        self.stopRecordingSignal = True
        self.hasStartedRecording = False
        self.stopRecordingTime   = t.time()
        self.recordingTime       += (self.stopRecordingTime - self.startRecordingTime)
    
    def stopDisplaying(self):
        """ Stop any displaying currently running """
        self.threadsDieNow = True
        
    def deleteSignal(self):
        """
        Delete the link of the current signal object with the sound card
        """
        self.threadsDieNow = True
        
        try :
            t.sleep(0,01)
            self.stopSignalStream()
            t.sleep(0,01)
            self.soundCardLink.terminate()
        except Exception :
            print "Baoum, explosion due to huge level of reccursion"
        #self.closeSignalStream()
    
    #
    # UN SIGNAL TRAITE DOIT ETRE RENVOYE SOUS SA FORME TEMPORELLE
    #
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
    
    def getTimeSignal(self):
        # x represent all the recorded time signal 
        x = numpy.empty(len(self.timeSignal)*self.size*self.channel,dtype=numpy.int16)
       
        # fill in x with signal values
        for i in range(len(self.timeSignal)):
            x[i*self.size*self.channel:(i+1)*self.size*self.channel] = self.timeSignal[i][0:self.size*self.channel] 
        
        return x
        
    def getWellFormattedTimeSignal(self):
        """
        Return time signal on an adapted form to display it
        * If channel number is 1   : an array of an array containing the signal values is returned
        * If channel number is 2   : an array of two arrays containing each one a channel signal values is returned
        * If channel number is n>2 : it will probably explode
        Note : this currently work by formating int16 audio data
        """

        # x represent all the recorded time signal 
        x = self.getTimeSignal()
        
        # format x and give it back
        return Signal.getWellFormatedSignal(x, self.channel)
    
    def getFreqSignal(self):
        # x represent all the recorded frequential signal 
        x = numpy.empty(len(self.frequentialSignal)*self.size*self.channel,dtype=numpy.int16)
       
        # fill in x with signal values
        for i in range(len(self.frequentialSignal)):
            x[i*self.size*self.channel:(i+1)*self.size*self.channel] = self.frequentialSignal[i][0:self.size*self.channel] 
        
        return x
        
    def getWellFormattedFreqSignal(self):
        """
        Return frequential signal on an adapted form to display it
        * If channel number is 1   : an array of an array containing the signal values is returned
        * If channel number is 2   : an array of two arrays containing each one a channel signal values is returned
        * If channel number is n>2 : it will probably explode
        Note : this currently work by formating int16 audio data
        """
        
        # x represent all the recorded frequential signal 
        x = self.getFreqSignal()
        
        # format x and give it back
        return Signal.getWellFormatedSignal(x, self.channel)
    
    #
    # = Under development ================
    #    
    def getBPFilteredSignalPart(self, w0, w1):
        """
        Return a band pass filtered signalPart, in time form
        w0 and w1 stand for the cutoff frequencies.
        * If channel number is 1   : an array of an array containing the signal values is returned
        * If channel number is 2   : an array of two arrays containing each one a channel signal values is returned
        * If channel number is n>2 : it will probably explode
        """
        
        freqSignalPart = Signal.getFreqSignalFromTimeSignal(self.signalPart)
        timeSignalPart = self.signalPart.copy()
        
        # filtering signalParts
        for k in range(len(freqSignalPart)):
            if w0>freqSignalPart[k] or freqSignalPart[k]>w1 :
                timeSignalPart[k]=0
        
        return Signal.getWellFormatedSignal(timeSignalPart, self.channel)
        
    def getBPFilteredSignal(self, w0, w1):
        """
        Return a band pass filtered signal, in time form
        w0 and w1 stand for the cutoff frequencies.
        * If channel number is 1   : an array of an array containing the signal values is returned
        * If channel number is 2   : an array of two arrays containing each one a channel signal values is returned
        * If channel number is n>2 : it will probably explode
        """
        
        timeSignalTmp = self.getTimeSignal()
        freqSignalTmp = getTimeSignalFromFreqSignal(timeSignalTmp)
        
        # filtering signalParts
        for k in range(len(freqSignalTmp)):
            if w0>freqSignalTmp[k] or freqSignalTmp[k]>w1 :
                timeSignalTmp[k]=0
        
        return timeSignalTmp
        
    #
    # = Under development ================
    #
    def getLPFilteredSignalPart(self, wo):
        """
        Return a low pass filtered signalPart, in time form
        w0 stands for the cutoff frequency.
        * If channel number is 1   : an array of an array containing the signal values is returned
        * If channel number is 2   : an array of two arrays containing each one a channel signal values is returned
        * If channel number is n>2 : it will probably explode
        """

        freqSignalPart = Signal.getFreqSignalFromTimeSignal(self.signalPart)
        timeSignalPart = self.signalPart.copy()
        
        for k in range(len(freqSignalPart)):
            if freqSignalPart[k]>wo :   #Filter definition
                timeSignalPart[k]=0   #Values outside filter's range =0
        
        return Signal.getWellFormatedSignal(timeSignalPart, self.channel)
        
    def getLPFilteredSignal(self, wo):
        """
        Return a low pass filtered signal, in time form
        w0 stands for the cutoff frequency.
        * If channel number is 1   : an array of an array containing the signal values is returned
        * If channel number is 2   : an array of two arrays containing each one a channel signal values is returned
        * If channel number is n>2 : it will probably explode
        """

        timeSignalTmp = self.getTimeSignal()
        freqSignalTmp = Signal.getTimeSignalFromFreqSignal(timeSignalTmp)
        
        for k in range(len(freqSignalTmp)):
            if freqSignalTmp[k]>wo :   #Filter definition
                timeSignalTmp[k]=0   #Values outside filter's range =0
        
        return Signal.getWellFormatedSignal(timeSignalTmp, self.channel)
    
    #
    # = Under development ================
    #
    def getHPFilteredSignalPart(self, wo):
        """
        Return a high pass filtered signalPart, in time form
        w0 stands for the cutoff frequency.
        * If channel number is 1   : an array of an array containing the signal values is returned
        * If channel number is 2   : an array of two arrays containing each one a channel signal values is returned
        * If channel number is n>2 : it will probably explode
        """
        
        # filtering signalParts
        freqSignalPart = Signal.getFreqSignalFromTimeSignal(self.signalPart)
        timeSignalPart = self.signalPart.copy()

        for k in range(len(freqSignalPart)):
            if freqSignalPart[k]<wo :   
                timeSignalPart[k]=0

        return Signal.getWellFormatedSignal(timeSignalPart, self.channel)
        
    def getHPFilteredSignal(self, wo):
        """
        Return a high pass filtered signal, in time form
        w0 stands for the cutoff frequency.
        * If channel number is 1   : an array of an array containing the signal values is returned
        * If channel number is 2   : an array of two arrays containing each one a channel signal values is returned
        * If channel number is n>2 : it will probably explode
        """
        
        # filtering signalParts
        timeSignalTmp = self.getTimeSignal()
        freqSignalTmp = Signal.getTimeSignalFromFreqSignal(timeSignalTmp)

        for k in range(len(freqSignalTmp)):
            if freqSignalTmp[k]<wo :   
                timeSignalTmp[k]=0

        return Signal.getWellFormatedSignal(timeSignalTmp, self.channel)        

    def getAntiNoiseSignalPart(self, noisePercent) :
        """
        Return a noise free signalPart, in frequential form
        noisePercent is percentage of noise filtered
        """
        Amax = 0
        freqSignalPart = Signal.getFreqSignalFromTimeSignal(self.signalPart)
        for k in range(len(freqSignalPart)) :
            if freqSignalPart[k] > Amax :
                Amax = freqSignalPart[k]         #Research of FFT's max value

        for k in range(len(freqSignalPart)):
            if freqSignalPart[k] < noisePercent*Amax :   
                freqSignalPart[k] = 0
        
        return Signal.getWellFormatedSignal(Signal.getTimeSignalFromFreqSignal(freqSignalPart), self.channel)   
        
    def getAntiNoiseSignal(self, noisePercent) :
        """
        Return a noise free signal, in frequential form
        noisePercent is percentage of noise filtered
        """
        Amax = 0

        freqSignalTmp = Signal.getFreqSignalFromTimeSignal(self.getTimeSignal())
        
        for k in range(len(freqSignalTmp)) :
            if freqSignalTmp[k] > Amax :
                Amax = freqSignalTmp[k]         #Research of FFT's max value

        for k in range(len(freqSignalTmp)):
            if freqSignalTmp[k] < noisePercent*Amax :   
                freqSignalTmp[k] = 0
        
        #print "get time signal : "+str(self.getTimeSignal())
        #print "get WF time signal : "+str(self.getWellFormattedTimeSignal())
        #print "function result : "+str(Signal.getWellFormatedSignal(freqSignalTmp, self.channel))
        
        #return self.getWellFormattedTimeSignal()
        
        return Signal.getWellFormatedSignal(Signal.getTimeSignalFromFreqSignal(freqSignalTmp), self.channel)
        
        
         
        
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
        self.soundCardStream.close()
        
    # Not usefull with pyaudio ?
    #def closeSignalStream(self):
    #    """ Close the stream used for the current signal """
    #    self.soundCardStream.close_stream()

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
        return abs(rfft(timeSignalToConvert))
        
    @staticmethod    
    def getTimeSignalFromFreqSignal(freqSignalToConvert):
        """ Return the time signal corresponding to a frequential signal """
        return irfft(freqSignalToConvert)
    
    
    
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
        while not(self.stopRecordingSignal):
            
            # all the readings from the sound card are recorder as signal portions
            self.signalPart[0:self.size*self.channel] = self.readSignal(self.size)
            self.timeSignal.append(numpy.copy(self.signalPart))
            
            # this portion of signal is new and doesn't have been displayed
            # to the user
            self.newAudio=True
            
    def __recordSignalPart(self):
        """ Record only parts of signal """
        
        print "[Record Signal Part]"
        
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
    
    def startRealTimeDisplay(self, time=None):
        """
        Actualize the signal buffer with currently received
        sound card signal.
        Used for real time diplay of the signal
        """
        self.realTimeDisplayProcess = Thread(target=self.__recordSignalPart)
        self.realTimeDisplayProcess.start()
        
        # if time given, stop recording when time is reached
        if time!=None :
            t.sleep(time)
            self.stopRecording()
            
    
    def getAmplitudeMax(self) : 
        """ 
        Return the maximal amplitude of all sinus in the current signal.
        This method doesn't apply to the recorded signal, it's just working
        for real time signal information.
        """
        Amax = 0

        freqSignalTmp = Signal.getFreqSignalFromTimeSignal(self.signalPart)
        
        for k in range(len(freqSignalTmp)) :
            if freqSignalTmp[k] > Amax :
                Amax = freqSignalTmp[k]             
        
        return round(Amax , 3)
        
    def getPeakToPeak(self) :
        """ 
        Return the peak to peak value of the signal with the maximal amplitude
        This method doesn't apply to the recorded signal, it's just working
        for real time signal information.
        """
        Amax = 0
        Amin = 0
        
        signalPart = self.signalPart.copy()
        
        for k in range(len(signalPart)) :
            if signalPart[k] > Amax :
                Amax = signalPart[k]         

        for k in range(len(signalPart)) :
            if signalPart[k] < Amin :
                Amin = signalPart[k] 
        
        return round(Amax - Amin , 3)
        
    def getRecordingTime(self) :
        """ 
        Return the recording time
        This method doesn't apply to the recorded signal, it's just working
        for real time signal information.
        """
        tmpRecordingTime = 0
        
        if self.hasStartedRecording :
            # the signal is still recording
            self.stopRecordingTime = t.time()
            tmpRecordingTime     = (self.stopRecordingTime - self.startRecordingTime)
        
        return round(self.recordingTime + tmpRecordingTime, 2)
        
    def getPhaseShift(self) :
        return 0

    
    


    




