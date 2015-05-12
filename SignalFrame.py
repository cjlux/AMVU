#!/usr/bin/env python
from __future__ import division

"""
    Class for signal display management
    
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
# Last update : 06/05/2015

from Signal import Signal
from TimePlot import TimePlot
from FreqPlot import FreqPlot

class SignalFrame():
    
    def __init__(self):
        """
        Create a SignalFrame object. Allow to store and
        manage the display of many signals 
        """
        
        # referenced signal form (time or frequential)
        self.freqScope = None
        self.timeScope = None
        
        # signals storage
        self.signalList = []
        self.currentSignal = 0
        
    def consider(self, signal):
        """
        Add a signal to the signal storage
        """
        self.signalList.append(signal)
        
    def getFreqScope(self):
        """ Return the frequential scope for the current signal """
        return self.freqScope
    
    def getTimeScope(self):
        """ Return the time scope for the current signal """
        return self.timeScope
    
    def displayPreviousSignal(self):
        """
        Select the previous signal in the signal list
        and make it ready to display
        """
        if (self.currentSignal > 0):
            self.currentSignal -= 1
            self.freqScope = self.signalList[self.currentSignal].getWellFormattedFreqSignal()
            self.timeScope = self.signalList[self.currentSignal].getWellFormattedTimeSignal()
        # else : there isn't any previous signal to display
    
    def displayNextSignal(self):
        """
        Select the next signal in the signal list
        and make it ready to display
        """
        if (self.currentSignal < len(self.signalList) - 1):
            self.currentSignal += 1
            self.freqScope = self.signalList[self.currentSignal].getWellFormattedFreqSignal()
            self.timeScope = self.signalList[self.currentSignal].getWellFormattedTimeSignal()
        # else : there isn't any previous signal to display
    
    def displayLastSignal(self):
        """
        Select the last signal in the signal list
        and make it ready to display
        """
        self.currentSignal = len(self.signalList) - 1
        self.freqScope = FreqPlot(self.signalList[self.currentSignal].getWellFormattedFreqSignal(), 0, 0)
        self.timeScope = TimePlot(self.signalList[self.currentSignal].getWellFormattedTimeSignal(), 0, 0)
    
    def displayDerivatedSignal(self):
        """
        Compute the derivated signal of the current signal,
        add it to the list and make it ready to display
        """
        print "[Display Derivated Signal]"
    
    def displayIntegratedSignal(self):
        """
        Compute the integrated signal of the current signal,
        add it to the list and make it ready to display
        """
        print "[Display Integrated Signal]"
    
    def displayFilteredSignal(self, filteringType, w0 = 0, w1 = 0):
        """
        Compute the filterd signal of the current signal,
        add it to the list and make it ready to display.
        The different filteringType value allowed are :
        - "BP" : band pass filtering. w0 and w1 must be filled with
        cutoff frequencies
        - "LP" : low pass filtering. Only w0 is required to be filled
        - "HP" : high pass filtering. Only w0 is required to be filled
        """
        
        # get filtered signal from the current signal
        rate    = self.signalList[self.currentSignal].rate
        size    = self.signalList[self.currentSignal].size
        format  = self.signalList[self.currentSignal].format
        channel = self.signalList[self.currentSignal].channel
            
        filteredSignal = Signal(rate, size, format, channel)
            
        if (filteringType == "HP"):
            
            filteredSignal.setTimeSignal(self.signalList[self.currentSignal].getHPFilteredTimeSignal(w0))
            # NB : the signal class automatically compute the filtered signal
        
        elif (filteringType == "LP"):
            
            filteredSignal.setTimeSignal(self.signalList[self.currentSignal].getBPFilteredTimeSignal(w0))
            # NB : the signal class automatically compute the filtered signal
        
        elif (filteringType == "BP"):
            
            filteredSignal.setTimeSignal(self.signalList[self.currentSignal].getBPFilteredTimeSignal(w0, w1))
            # NB : the signal class automatically compute the filtered signal
        
        # else : we consider an empty signal
        
        # add it to the signal list
        self.consider(filteredSignal)
            
        # make it ready to display
        self.displayLastSignal()
    
    def displayContinuousSignal(self):
        """
        Allow to display continous signal by a mainFrame object.
        """
        pass
    
    
    
    
    
    
    
    
    
