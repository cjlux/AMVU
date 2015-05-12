#!/usr/bin/env python
from __future__ import division

"""
    Class for time plot management
    
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

from Plot import Plot

class TimePlot(Plot):
    
    def __init__(self, signal, df=0, fr=0):
        Plot.__init__(self, signal)
        self.df = df
        self.fr = fr
    
    
    def __init__(self, a1, a2, dt, df=0, fr=0):
        Plot.__init__(self, a1, a2, dt)
        self.df = df
        self.fr = fr