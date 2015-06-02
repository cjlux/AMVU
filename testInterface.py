#-*-coding: utf-8 -*-
#!/usr/bin/env python
from __future__ import division

from PyQt4 import QtGui
from PyQt4.QtGui import QMainWindow,QWidget,QAction,QTabWidget,QApplication
from PyQt4 import Qt
from PyQt4 import QtCore
from PyQt4 import Qwt5 as Qwt

import os,sys
import Icons
import numpy as np

import pyqtgraph as pg

from Signal import Signal
from SignalFrame import SignalFrame

# Last update : S122, 13/05/2015
# test line for git integration S122 

#
# Global values
#

# stand for the MainFrame object used
# in different function
SCOPE = None


class MainFrame(QMainWindow):

    def __init__(self, signalFrame):
        
        QMainWindow.__init__(self)
        
        # is recording ?
        self.isRecording = False

        # signal frame for signal display and management
        self.signalFrame = signalFrame
      
        #know the size of the main frame
        size_fenetre = self.geometry()
        size_fenetre = size_fenetre.getCoords()
        width_fenetre  = size_fenetre[2]
        height_fenetre = size_fenetre[3]
          
        # tabs
        self.timeGraphTab = None
        self.freqGraphTab = None
        
        # control buttons
        #self.stack      = None
        self.btnPause   = None
        self.grid       = None
        
        self.selectedChannel = 3 # default, channel 1+2 selected
        
        #
        # Interface elements (widgets) 
        #
        self.globalInterface        = None
        self.globalInterfaceRight   = None
        self.globalInterfaceLeft    = None
        self.globalInterfaceCenter  = None
        
        self.signalInformation  = None
        self.controlPanelRight  = None
        self.controlPanelLeft   = None
        self.signalGraph        = None
        
        #
        # Layouts
        #
        
        # interface
        self.globalInterfaceLayout        = None
        self.globalInterfaceRightLayout   = None
        self.globalInterfaceLeftLayout    = None
        self.globalInterfaceCenterLayout  = None
        
        self.signalInformationLayout  = None
        self.controlPanelRightLayout  = None
        self.controlPanelLeftLayout   = None
        self.signalGraphLayout        = None
        
        # graphs
        self.timeGraphLayout    = None
        self.freqGraphLayout    = None
        
        #
        # All this stuff if for the tab presentations
        #
        
        
        # LAYOUTS ------------------------------------------


        # Layouts for each tabs
        #self.layoutTab1 = None
        #self.layoutTab2 = None
        
        # Layouts for the controls
        #self.layoutControls1 = None
        #self.layoutControls2 = None
        
        # Layouts for the graphs
        #self.layoutGraph1 = None
        #self.layoutGraph2 = None

        
        # WIDGETS ------------------------------------------

        
        # Control widget for each tab
        #self.controlWidget1 = None
        #self.controlWidget2 = None
        
        # Graph widget for each tab
        #self.graphWidget1 = None
        #self.graphWidget2 = None
        
        
        # GRAPHS ------------------------------------------

        
        # graph for each tab
        #self.timeGraph = None
        #self.freqGraph = None

        
        # BUTTONS ------------------------------------------

        
        # Control buttons for each tab
        

        # for tab 1

        self.StartRecording 	= None
        self.StartNsec 			= None
        self.StopRecording 		= None
        self.Trigger 			= None
        self.checkboxOffset 	= None
        self.checkboxAntiNoise 	= None
        self.checkboxDerivate 	= None
        self.checkboxIntegrate 	= None
        self.checkboxLP 		= None
        self.checkboxHP 		= None
        self.checkboxBP 		= None
        self.checkboxCut 		= None

        self.InputBoxNSecond 	= None
        self.InputBoxFrequency1 = None
        self.InputBoxFrequency2 = None
        self.InputBoxThreshold 	= None
        self.InputBoxOffset 	= None
        self.InputBoxAntiNoise 	= None
        self.InputBoxChanel1Sensibility = None
        self.InputBoxChanel2Sensibility = None

        self.units = 'V'
        self.units1 = None
        self.units2 = None
               
#=======
        
        # for tab 2
        
#=======
        #self.controlButton11 = None
        #self.controlButton12 = None
        
        # for tab 2
        #self.controlButton21 = None
        #self.controlButton22 = None

        
        #
        # --------------------------------------------------
        #
        
        #
        # Set the global interface and its layout
        #
        
        # define all the global interface layouts
        self.globalInterface = QWidget()
        self.globalInterfaceLayout = QtGui.QGridLayout()
        
        self.globalInterfaceLeft = QWidget()
        self.globalInterfaceLeftLayout = QtGui.QGridLayout()
        self.globalInterfaceLeft.setLayout(self.globalInterfaceLeftLayout)
        
        self.globalInterfaceRight = QWidget()
        self.globalInterfaceRightLayout = QtGui.QGridLayout()
        self.globalInterfaceRight.setLayout(self.globalInterfaceRightLayout)
        
        self.globalInterfaceCenter = QWidget()
        self.globalInterfaceCenterLayout = QtGui.QGridLayout()
        self.globalInterfaceCenter.setLayout(self.globalInterfaceCenterLayout)
        
        # set the link between this interfaces
        self.globalInterfaceLayout.addWidget(self.globalInterfaceLeft, 0, 0)
        self.globalInterfaceLayout.addWidget(self.globalInterfaceCenter, 0, 1)
        self.globalInterfaceLayout.addWidget(self.globalInterfaceRight, 0, 2)
        
        self.globalInterface.setLayout(self.globalInterfaceLayout)
        
        self.setCentralWidget(self.globalInterface)

        #change size of the widget
        #====== self.globalInterfaceCenter.setFixedSize(0.55*width_fenetre,height_fenetre)

    def setTitle(self, titre="") :
        self.setWindowTitle(titre)

    def setGraphTab(self):
        
        # set each graph tab
        self.timeGraphTab   	= QWidget() 
        self.freqGraphTab   	= QWidget()
        self.recordedSignalTab 	= QWidget()

        # set the tab widget hosting each graph tab
        self.signalGraph = QTabWidget(self) 
        self.signalGraph.addTab(self.timeGraphTab,"Time")
        self.signalGraph.addTab(self.freqGraphTab,"Frequency")
        self.signalGraph.addTab(self.recordedSignalTab,"Recorded signal")
        
        # add the graph tab to the global interface
        self.globalInterfaceLeftLayout.addWidget(self.signalGraph, 2, 0)

    def setToolBar(self):

        toolBar = Qt.QToolBar(self) # création d'un lieu pouvant acceuillir widget
        self.addToolBar(toolBar) # ajout toolbar
        sb=self.statusBar()
        sbfont=Qt.QFont("Helvetica",12)
        sb.setFont(sbfont)

        btnQuit = Qt.QToolButton(toolBar)
        btnQuit.setToolTip('Quits the application')
        btnQuit.setText("Quit")
        btnQuit.setIcon(Qt.QIcon(Qt.QPixmap(Icons.quit)))
        btnQuit.setCheckable(True)
        btnQuit.setToolButtonStyle(Qt.Qt.ToolButtonTextUnderIcon)
        toolBar.addWidget(btnQuit)
        self.connect(btnQuit,QtCore.SIGNAL('clicked()'),self.closeMainFrame)

        btnSave = Qt.QToolButton(toolBar)
        btnSave.setToolTip('Save in .wav')
        btnSave.setText("Save")
        btnSave.setIcon(Qt.QIcon(Qt.QPixmap("save")))
        btnSave.setCheckable(False)
        btnSave.setToolButtonStyle(Qt.Qt.ToolButtonTextUnderIcon)
        toolBar.addWidget(btnSave)
##        self.connect(btnQuit,QtCore.SIGNAL('clicked()'),QtCore.SLOT('close()'))

        btnPDF = Qt.QToolButton(toolBar)
        btnPDF.setText("PDF")
        btnPDF.setToolTip('Prints the display in a PDF file')
        btnPDF.setIcon(Qt.QIcon(Qt.QPixmap(Icons.print_xpm)))
        btnPDF.setToolButtonStyle(Qt.Qt.ToolButtonTextUnderIcon)
        toolBar.addWidget(btnPDF)
        #self.connect(btnPDF, Qt.SIGNAL('clicked()'), self.ExportPDF)

        btnPNG = Qt.QToolButton(toolBar)
        btnPNG.setText("PNG")
        btnPNG.setToolTip('Prints the display in a PNG file')
        btnPNG.setIcon(Qt.QIcon(Qt.QPixmap(Icons.print_xpm)))
        btnPNG.setToolButtonStyle(Qt.Qt.ToolButtonTextUnderIcon)
        toolBar.addWidget(btnPNG)            
##        #self.connect(btnPNG, Qt.SIGNAL('clicked()'), self.ExportPNG)

        btnMode = Qt.QToolButton(toolBar)
        btnMode.setToolTip('Choose the mode of the application')
        btnMode.setText("Mode")
        btnMode.setIcon(Qt.QIcon("cible.png"))
        btnMode.setCheckable(True)
        btnMode.setToolButtonStyle(Qt.Qt.ToolButtonTextUnderIcon)
        toolBar.addWidget(btnMode)
##        self.connect(btnQuit,QtCore.SIGNAL('clicked()'),QtCore.SLOT('close()')

        btnHelp = Qt.QToolButton(toolBar)
        btnHelp.setToolTip('Help')
        btnHelp.setText("Help")
        btnHelp.setIcon(Qt.QIcon("help.png"))
        btnHelp.setCheckable(False)
        btnHelp.setToolButtonStyle(Qt.Qt.ToolButtonTextUnderIcon)
        toolBar.addWidget(btnHelp)
        
    def ExportPDF(self):
        # Export in PDF mode
        print('ExportPDF')

    def ExportPNG(self):
        # Export in PNG mode
        print('ExportPNG')
      
    
    
    #
    # ORGANIZE EACH GUI ELEMENT -----------------------------------------
    #

    def setScopes(self):
        
        # create tabs to host graphs
        self.setGraphTab()
        
        # create the graphs
        self.timeGraph 		= self.signalFrame.timeScope
        self.freqGraph 		= self.signalFrame.freqScope
        #self.recordedSignal = self.signalFrame.recordedScope
        
        # add the graphs to the tabs
        self.timeGraphLayout 		= QtGui.QGridLayout()
        self.freqGraphLayout 		= QtGui.QGridLayout()
        
        self.timeGraphLayout.addWidget(self.timeGraph, 0, 0)
        self.freqGraphLayout.addWidget(self.freqGraph, 0, 0)
        
        self.timeGraphTab.setLayout(self.timeGraphLayout)
        self.freqGraphTab.setLayout(self.freqGraphLayout)

    def setRecordedSignalDisplay(self):

        self.recordedSignal = pg.GraphicsView()
        self.recordedSignal = pg.PlotWidget()

        self.recordedSignalLayout = QtGui.QGridLayout()
        self.recordedSignalLayout.addWidget(self.recordedSignal, 0, 0)
        self.recordedSignalTab.setLayout(self.recordedSignalLayout)
        #self.recordedSignalTab.add(self.recordedSignal)


    def setSignalInformation(self):
        
        # create a label to display information
        self.informationLabel1 = QtGui.QLabel()#u"Amplitude max : [V]")
        self.informationLabel2 = QtGui.QLabel()#u"Peak to peak Value: [V]")
        self.informationLabel3 = QtGui.QLabel()#u"Recording time : [sec]")
        self.informationLabel4 = QtGui.QLabel()#u"Phase shift : [rad]")
        self.informationLabel11 = QtGui.QLabel()
        self.informationLabel22 = QtGui.QLabel()      
        
        
        # add this label to the global interface
        self.signalInformationLayout = QtGui.QGridLayout()
        self.signalInformationLayout.addWidget(self.informationLabel1, 0, 0)
        self.signalInformationLayout.addWidget(self.informationLabel2, 1, 0)
        self.signalInformationLayout.addWidget(self.informationLabel3, 2, 0)
        self.signalInformationLayout.addWidget(self.informationLabel4, 2, 1)
        self.signalInformationLayout.addWidget(self.informationLabel11, 0, 1)
        self.signalInformationLayout.addWidget(self.informationLabel22, 1, 1)
        

        #create the infoAction box
        self.infoAction = QtGui.QLineEdit("Current action : ",self)
        self.infoAction.setReadOnly(True)
        self.infoAction.setText("None")

        #add this label to the running info interface
        self.runningInfoLayout = QtGui.QGridLayout()
        self.runningInfoLayout.addWidget(self.infoAction, 0, 0)
        
        self.runningInfo = QWidget()
        self.runningInfo.setLayout(self.runningInfoLayout)
        self.globalInterfaceLeftLayout.addWidget(self.runningInfo, 1, 0)

                
        self.signalInformation = QWidget()
        self.signalInformation.setLayout(self.signalInformationLayout)
        
        self.globalInterfaceLeftLayout.addWidget(self.signalInformation, 0, 0)
        
    def setControlPanelRight(self):
        
        # define the layout use to dispose the controls
        self.controlPanelRightLayout = QtGui.QGridLayout()
        
        # set all the controls and add them to the layout
        
        # scales controls
        self.controlButtonVerticalScale1 = Qwt.QwtKnob()
        self.controlButtonVerticalScale1.setTotalAngle(270)
        self.controlButtonVerticalScale2 = Qwt.QwtKnob()
        self.controlButtonVerticalScale2.setTotalAngle(270)
        self.controlButtonHorizontalScale = Qwt.QwtKnob()
        self.controlButtonHorizontalScale.setTotalAngle(270)
        
        # set propreties for this controls
        self.controlButtonVerticalScale1.setScale(0.1, 1, 0.2)
        self.controlButtonVerticalScale1.setRange(0.1, 1)
        self.controlButtonVerticalScale2.setScale(0.1, 1, 0.2)
        self.controlButtonVerticalScale2.setRange(0.1, 1)
        self.controlButtonHorizontalScale.setScale(0.1, 0.5, 0.1)
        self.controlButtonHorizontalScale.setRange(0.1, 0.5)
        
        # signal size and rate controls
        self.controlButtonSize = Qwt.QwtKnob()
        self.controlButtonSize.setTotalAngle(270)
        self.controlButtonRate = Qwt.QwtKnob()
        self.controlButtonRate.setTotalAngle(270)
        
        # set properties for this controls
        self.controlButtonSize.setScale(1024, 4096, 512)
        self.controlButtonSize.setRange(1024, 4096)
        self.controlButtonRate.setScale(8192, 44100, 8192)
        self.controlButtonRate.setRange(8192, 44100)

        # disposition on the layout
        self.controlPanelRightLayout.addWidget(self.controlButtonVerticalScale1, 0, 0)
        self.controlPanelRightLayout.addWidget(self.controlButtonVerticalScale2, 0, 1)
        self.controlPanelRightLayout.addWidget(self.controlButtonHorizontalScale, 2, 0)
        self.controlPanelRightLayout.addWidget(self.controlButtonSize, 4, 0)
        self.controlPanelRightLayout.addWidget(self.controlButtonRate, 6, 0)

        
        # set  all buttons' Ranges     
    

        # Add text under each button

        self.button0Text = Qt.QLabel("Vertical Scale Channel 1")
        self.button0Text.setAlignment(QtCore.Qt.AlignCenter)
        self.button1Text = Qt.QLabel("Vertical Scale Channel 2")
        self.button1Text.setAlignment(QtCore.Qt.AlignCenter)
        self.button2Text = Qt.QLabel("Horizontal Scale")
        self.button2Text.setAlignment(QtCore.Qt.AlignCenter)
        self.button3Text = Qt.QLabel("Size")
        self.button3Text.setAlignment(QtCore.Qt.AlignCenter)
        self.button4Text = Qt.QLabel("Rate")
        self.button4Text.setAlignment(QtCore.Qt.AlignCenter)

        # set all the texts and add them to the layout

        self.controlPanelRightLayout.addWidget(self.button0Text, 1, 0)
        self.controlPanelRightLayout.addWidget(self.button1Text, 1, 1)
        self.controlPanelRightLayout.addWidget(self.button2Text, 3, 0)
        self.controlPanelRightLayout.addWidget(self.button3Text, 5, 0)
        self.controlPanelRightLayout.addWidget(self.button4Text, 7, 0)   
           
        # add all this stuff to the global interface
        
        self.controlPanelRight = QWidget()
        self.controlPanelRight.setLayout(self.controlPanelRightLayout)        
        self.globalInterfaceRightLayout.addWidget(self.controlPanelRight, 0, 0)
        
    def setControlPanelLeft(self):
                
        # define the layout use to dispose the controls
        self.controlPanelLeftLayout = QtGui.QGridLayout()
                
        # set all the controls

        # create a combobox to chose the channel to display
        self.channelButton = Qt.QComboBox()
        
        self.channelButton.insertItem(0,"Channels 1+2")
        self.channelButton.insertItem(1,"Channel 1")
        self.channelButton.insertItem(2,"Channel 2")        
        
        self.razButton = QtGui.QPushButton("Delete recorded signal", self)
        
        self.StartRecording = QtGui.QPushButton("Start",self)
        self.StartNsec = QtGui.QPushButton("",self)
        self.StopRecording = QtGui.QPushButton("Stop",self)        
        self.Trigger = QtGui.QPushButton("",self)        
        self.checkboxOffset = QtGui.QCheckBox("",self)        
        self.checkboxDerivate = QtGui.QCheckBox("",self)
        self.checkboxIntegrate = QtGui.QCheckBox("",self)
        self.checkboxAntiNoise = QtGui.QCheckBox("",self)
        self.sliderAntiNoise = QtGui.QSlider(QtCore.Qt.Horizontal,self)
        self.checkboxLP = QtGui.QCheckBox("",self)
        self.checkboxHP = QtGui.QCheckBox("",self)
        self.checkboxBP = QtGui.QCheckBox("",self)
        self.checkboxCut = QtGui.QCheckBox("",self)

        self.InputBoxNSecond = QtGui.QLineEdit(self)
        #self.InputBoxAntiNoise = QtGui.QLineEdit(self)
        self.InputBoxFrequency1 = QtGui.QLineEdit(self)
        self.InputBoxFrequency2 = QtGui.QLineEdit(self)
        self.InputBoxThreshold = QtGui.QLineEdit(self)
        self.InputBoxOffset = QtGui.QLineEdit(self)
        self.InputBoxChannel1Sensibility = QtGui.QLineEdit(self)
        self.InputBoxChannel1Units = QtGui.QLineEdit(self)
        self.InputBoxChannel2Sensibility = QtGui.QLineEdit(self)
        self.InputBoxChannel2Units = QtGui.QLineEdit(self)

                
        #create label with the text of the inputbox as a Widget to be put in the grid above the checkbox
        self.EmptyText1 = QtGui.QLabel("Recording controls")
        self.EmptyText2 = QtGui.QLabel("Optionnal controls")
        self.EmptyText3 = QtGui.QLabel("Sensor Information")
        self.InputBoxNSecondText = QtGui.QLabel("sec")
        self.InputBoxThresholdText = QtGui.QLabel("Threshold")
        self.InputBoxFrequency1Text = QtGui.QLabel("Frequency 1")
        self.InputBoxFrequency2Text = QtGui.QLabel("Frequency 2")
        self.InputBoxChannel1SensibilityText = QtGui.QLabel("Info Sensor Channel 1")
        self.InputBoxChannel2SensibilityText = QtGui.QLabel("Info Sensor Channel 2")       
               
                
        # add all the controls and text to the layout
        self.controlPanelLeftLayout.addWidget(self.razButton,0,1)
        self.controlPanelLeftLayout.addWidget(self.channelButton, 0, 0)
        self.controlPanelLeftLayout.addWidget(self.EmptyText1, 1, 0)
        self.controlPanelLeftLayout.addWidget(self.StartRecording, 2, 0)
        self.controlPanelLeftLayout.addWidget(self.StartNsec, 3, 0)
        self.controlPanelLeftLayout.addWidget(self.InputBoxNSecond, 3, 1)
        self.controlPanelLeftLayout.addWidget(self.InputBoxNSecondText, 3, 2)
        self.controlPanelLeftLayout.addWidget(self.StopRecording, 4, 0)
        self.controlPanelLeftLayout.addWidget(self.Trigger, 5, 0)
        self.controlPanelLeftLayout.addWidget(self.InputBoxThreshold, 5, 1)
        self.controlPanelLeftLayout.addWidget(self.InputBoxThresholdText, 5, 2)
        self.controlPanelLeftLayout.addWidget(self.EmptyText2, 6, 0)        
        self.controlPanelLeftLayout.addWidget(self.checkboxOffset, 7, 0)
        self.controlPanelLeftLayout.addWidget(self.InputBoxOffset, 7, 1)
        self.controlPanelLeftLayout.addWidget(self.checkboxDerivate, 8, 0)
        self.controlPanelLeftLayout.addWidget(self.checkboxIntegrate, 8, 1)
        self.controlPanelLeftLayout.addWidget(self.checkboxAntiNoise, 9, 0)
        self.controlPanelLeftLayout.addWidget(self.sliderAntiNoise, 9, 1)
        #self.controlPanelLeftLayout.addWidget(self.InputBoxAntiNoise, 9, 2)
        self.controlPanelLeftLayout.addWidget(self.checkboxLP, 10, 0)
        self.controlPanelLeftLayout.addWidget(self.checkboxHP, 10, 1)
        self.controlPanelLeftLayout.addWidget(self.checkboxBP, 11, 0)
        self.controlPanelLeftLayout.addWidget(self.checkboxCut, 11, 1)
        self.controlPanelLeftLayout.addWidget(self.InputBoxFrequency1Text, 12, 0)
        self.controlPanelLeftLayout.addWidget(self.InputBoxFrequency1, 12, 1)
        self.controlPanelLeftLayout.addWidget(self.InputBoxFrequency2Text, 13, 0)
        self.controlPanelLeftLayout.addWidget(self.InputBoxFrequency2, 13, 1)
        self.controlPanelLeftLayout.addWidget(self.EmptyText3, 14, 0)
        self.controlPanelLeftLayout.addWidget(self.InputBoxChannel1Sensibility, 15, 1)
        self.controlPanelLeftLayout.addWidget(self.InputBoxChannel1Units, 15, 2)
        self.controlPanelLeftLayout.addWidget(self.InputBoxChannel1SensibilityText, 15, 0)
        self.controlPanelLeftLayout.addWidget(self.InputBoxChannel2Sensibility, 16, 1)
        self.controlPanelLeftLayout.addWidget(self.InputBoxChannel2Units, 16, 2)
        self.controlPanelLeftLayout.addWidget(self.InputBoxChannel2SensibilityText, 16, 0)
        

        # add tooltips on each button
        self.channelButton.setToolTip('Choose the channel to be displayed')
        self.StartRecording.setToolTip('Start recording the measure')
        self.StartNsec.setToolTip('Start recording the measure for a number of seconds specified. The record will automatically stop itself')
        self.StopRecording.setToolTip('Stop recording the measure')
        self.Trigger.setToolTip('Use the mode Trigger to automatically start recording for the threshold specified')
        self.checkboxOffset.setToolTip('Add an offset to the measure ')
        self.InputBoxOffset.setToolTip('Indicate the value of the constant value of the signal if it is known')
     
        self.checkboxDerivate.setToolTip('Derivate the signal')
        self.checkboxIntegrate.setToolTip('Integrate the signal')

        self.checkboxAntiNoise.setToolTip('Activate the AntiNoise filter')
        #self.InputBoxAntiNoise.setToolTip('Set a percentage for the AntiNoise Filter')
        self.checkboxLP.setToolTip('Activate the Low Pass filter')
        self.checkboxHP.setToolTip('Activate the High Pass filter')
        self.checkboxBP.setToolTip('Activate the Band Pass filter')
        self.checkboxCut.setToolTip('Activate the Band Cut filter')
        self.InputBoxFrequency1.setToolTip('Principal frequency used by the Low Noise filter and the High Pass filter')
        self.InputBoxFrequency2.setToolTip('Secondary frequency used by the Band Pass filter and the Band Cut filter')
        self.InputBoxChannel1Sensibility.setToolTip('Indicate the value of the sensor used by the channel 1')
        self.InputBoxChannel1Units.setToolTip('Indicate the units of the sensor used by the channel 1')
        self.InputBoxChannel2Sensibility.setToolTip('Indicate the value of the sensor used by the channel 2')
        self.InputBoxChannel2Units.setToolTip('Indicate the units of the sensor used by the channel 2')
        
        
        

        #add text to all the buttons
        self.StartRecording.setText('Start Recording')
        self.StartNsec.setText('Start for')
        self.StopRecording.setText('Stop Recording')
        self.Trigger.setText('Trigger')
        self.checkboxOffset.setText('Offset')

        self.checkboxDerivate.setText('Derivate')
        self.checkboxIntegrate.setText('Integrate')

        self.checkboxAntiNoise.setText('AntiNoise Filter')
        self.checkboxLP.setText('Low Pass Filter')
        self.checkboxHP.setText('High Pass Filter')
        self.checkboxBP.setText('Band Pass Filter')
        self.checkboxCut.setText('Band Cut Filter')   

        
        # add all this stuff to the global interface
        self.controlPanelLeft = QWidget()
        self.controlPanelLeft.setLayout(self.controlPanelLeftLayout)
        
        self.globalInterfaceCenterLayout.addWidget(self.controlPanelLeft, 0, 0)

        #put margins around the widget
        self.controlPanelLeft.setContentsMargins( 0, 0, 0, 0)

        #add group button to make exclusive some of the checkbox
        self.GroupRecording = QtGui.QButtonGroup(self.controlPanelLeft)
        self.GroupMath = QtGui.QButtonGroup(self.controlPanelLeft)
        self.GroupFilter = QtGui.QButtonGroup(self.controlPanelLeft)

        #add the checkboxs to the group
        self.GroupRecording.addButton(self.StartRecording)
        self.GroupRecording.addButton(self.StopRecording)
        self.GroupMath.addButton(self.checkboxDerivate)
        self.GroupMath.addButton(self.checkboxIntegrate)
        self.GroupFilter.addButton(self.checkboxLP)
        self.GroupFilter.addButton(self.checkboxHP)
        self.GroupFilter.addButton(self.checkboxBP)
        self.GroupFilter.addButton(self.checkboxCut)

        #make the groups exclusive
        self.GroupRecording.setExclusive(True)
        self.GroupMath.setExclusive(False)
        self.GroupFilter.setExclusive(False)
        
        # connect GUI
        self.connectGUI()
        
    def displaySignal(self):
        """
        Display signal in temporal, frequential and recorded form 
        /!\ Mono canal => [0]
        
        """
        
        #print "[Oh yeah, I display]" self.checkboxAntiNoise.isChecked() 

        # get the signal modified by option selected by the user
        # a recorded signal is pure : the filters, anti-noise, ... treatement
        # are visible (are displayed) but doesn't alter the signal recorded
        

        rate = self.signalFrame.getCurrentSignal().rate
        
        # check how the user want to display the signal (filtered, pure, ...)
        if self.checkboxAntiNoise.isChecked() :

            # get the antinoise percentage and display the anti-noised signal
            noisePercent  = self.sliderAntiNoise.value()/100
            # self.sliderAntiNoise.value()

            print "[display] Anti-noise altered signal "+str(noisePercent)
            
            dataToDisplay = self.signalFrame.getCurrentSignal().getAntiNoiseSignalPart(noisePercent)
            recordedSignalToDisplay = self.signalFrame.getCurrentSignal().getAntiNoiseSignal(noisePercent)[0]

        elif self.checkboxHP.isChecked() :

            # set the default value for the cutting frequency
            try :
                wo = float(self.InputBoxFrequency1.text())
            except :
                print "That's not a valid value! Try again"
                self.infoAction.setText("Tuck a valid value")
                wo = 0.0
            
            print "[display] HighPass filtered signal at "+str(wo)
            
            dataToDisplay = self.signalFrame.getCurrentSignal().getHPFilteredSignalPart(wo)
            recordedSignalToDisplay = self.signalFrame.getCurrentSignal().getHPFilteredSignal(wo)[0]

        elif self.checkboxLP.isChecked() :

            # set the default value for the cutting frequency
            try :
                wo = float(self.InputBoxFrequency1.text())
            except :
                print "That's not a valid value! Try again"
                self.infoAction.setText("Tuck a valid value")
                wo = 0.0
            
            print "[display] LowPass filtered signal at "+str(wo)
            
            dataToDisplay = self.signalFrame.getCurrentSignal().getLPFilteredSignalPart(wo)
            recordedSignalToDisplay = self.signalFrame.getCurrentSignal().getLPFilteredSignal(wo)[0]
        
        elif self.checkboxBP.isChecked() :

            # set the default value for the cutting frequency
            try :
                wo = float(self.InputBoxFrequency1.text())
                w1 = float(self.InputBoxFrequency2.text())
            except :
                print "That's not a valid value! Try again"
                self.infoAction.setText("Tuck a valid value")
                wo = 0.0
                w1 = 0.0
            
            print "[display] BandPass filtered signal at "+str(wo)+";"+str(w1)
            
            dataToDisplay = self.signalFrame.getCurrentSignal().getBPFilteredSignalPart(wo,w1)
            recordedSignalToDisplay = self.signalFrame.getCurrentSignal().getBPFilteredSignal(wo,w1)[0]
            
        else :
            
            print "[display] Pure signal"
            
            # get the data to display
            dataToDisplay = self.signalFrame.getCurrentSignal().getLastSignalRecordedPart()
            recordedSignalToDisplay = self.signalFrame.getCurrentSignal().getWellFormattedTimeSignal()[0]
            
        # display it by refresh plot values to display, depending on the
        # channel number
        if self.selectedChannel == 3 :
            
            self.signalFrame.timeScope.update(dataToDisplay, rate)
            self.signalFrame.freqScope.update(Signal.getFreqSignalFromTimeSignal(dataToDisplay), rate)
        
        elif self.selectedChannel == 1 :
            
            print "channel 1"
            
            toDisplayTime = [dataToDisplay[0],[0.0,0.0]]
            toDisplayFreq = [Signal.getFreqSignalFromTimeSignal(dataToDisplay)[0],[0.0,0.0]]
            
            self.signalFrame.timeScope.update(toDisplayTime, rate)
            self.signalFrame.freqScope.update(toDisplayFreq, rate)
            
        else :
            
            print "channel 2"
            
            # channel selected = 2
            toDisplayTime = [[0.0,0.0], dataToDisplay[1]]
            toDisplayFreq = [[0.0,0.0],Signal.getFreqSignalFromTimeSignal(dataToDisplay)[1]]
            
            self.signalFrame.timeScope.update(toDisplayTime, rate)
            self.signalFrame.freqScope.update(toDisplayFreq, rate)
            
        # update recorded signal diplay
        # if recording, real time recorded signal display
        #if self.isRecording :      
        self.recordedSignal.plot(recordedSignalToDisplay, clear=True) 

        #change the units in the display box
        if self.InputBoxChannel1Units.isModified() : self.units1 = self.InputBoxChannel1Units.text()
        if self.InputBoxChannel1Units.text() == '' : self.units1 = 'V'
        if self.InputBoxChannel2Units.isModified() : self.units2 = self.InputBoxChannel2Units.text()
        if self.InputBoxChannel2Units.text() == '' : self.units2 = 'V'
        if self.channelButton.currentIndex() == 1 : self.units = self.units1
        if self.channelButton.currentIndex() == 2 : self.units = self.units2
                
        
        # update signal information
        recordingTime   = self.signalFrame.getCurrentSignal().getRecordingTime()
        amplitudeMax    = self.signalFrame.getCurrentSignal().getAmplitudeMax()
        peakToPeak      = self.signalFrame.getCurrentSignal().getPeakToPeak()
        phaseShift      = self.signalFrame.getCurrentSignal().getPhaseShift()

        #hide or show the different stuff from the infobox
        if self.channelButton.currentIndex() == 0:
            self.informationLabel1.setText(u"Amplitude max Channel 1 : "+str(amplitudeMax)+" ["+str(self.units1)+"]")
            self.informationLabel11.setText(u"Amplitude max Channel 2 : "+str(amplitudeMax)+" ["+str(self.units2)+"]")
            self.informationLabel2.setText(u"Peak to peak Value Channel 1: "+str(peakToPeak)+" ["+str(self.units1)+"]")
            self.informationLabel22.setText(u"Peak to peak Value Channel 2: "+str(peakToPeak)+" ["+str(self.units2)+"]")
            self.informationLabel3.setText(u"Recording time : "+str(recordingTime)+" [sec]")
            self.informationLabel4.show()
            self.informationLabel4.setText(u"Phase shift : "+str(phaseShift)+" [rad]")
        if self.channelButton.currentIndex() == 1:
            self.informationLabel1.setText(u"Amplitude max Channel 1 : "+str(amplitudeMax)+" ["+str(self.units1)+"]")
            self.informationLabel11.setText('')
            self.informationLabel2.setText(u"Peak to peak Value Channel 1: "+str(peakToPeak)+" ["+str(self.units1)+"]")
            self.informationLabel22.setText('')
            self.informationLabel3.setText(u"Recording time : "+str(recordingTime)+" [sec]")
            self.informationLabel4.hide()
        if self.channelButton.currentIndex() == 2:
            self.informationLabel1.setText(u"Amplitude max Channel 2 : "+str(amplitudeMax)+" ["+str(self.units2)+"]")
            self.informationLabel11.setText('')
            self.informationLabel2.setText(u"Peak to peak Value Channel 2: "+str(peakToPeak)+" ["+str(self.units2)+"]")
            self.informationLabel22.setText('')
            self.informationLabel3.setText(u"Recording time : "+str(recordingTime)+" [sec]")
            self.informationLabel4.hide()

        

             
    #
    # -----------------------------------------------------------------
    # 
    # Connexion between GUI and treatment
    #
    # ------------------------------------------------------------------
    #
    def connectGUI(self):
        print "[Connect GUI]"
        # self.controlButtonVerticalScale
        # self.controlButtonHorizontalScale

        # knobs on the right - signal rate, size, scale
        self.connect(self.controlButtonSize, Qt.SIGNAL("valueChanged(double)"), self.setSize)
        self.connect(self.controlButtonRate, Qt.SIGNAL("valueChanged(double)"), self.setRate)
        self.connect(self.controlButtonVerticalScale1, Qt.SIGNAL("valueChanged(double)"), self.setVerticalScale)
        self.connect(self.controlButtonVerticalScale2, Qt.SIGNAL("valueChanged(double)"), self.setVerticalScale)
        self.connect(self.controlButtonHorizontalScale, Qt.SIGNAL("valueChanged(double)"), self.setHorizontalScale)

        # controls in the center of the application
        self.connect(self.StartRecording, QtCore.SIGNAL('clicked()'), self.startRecord)
        self.connect(self.StopRecording, QtCore.SIGNAL('clicked()'), self.stopRecording)
        self.connect(self.Trigger, QtCore.SIGNAL('clicked()'), self.launchTrigger)
        self.connect(self.StartNsec, QtCore.SIGNAL('clicked()'), self.startRecordNsec)
        self.connect(self.razButton, QtCore.SIGNAL('clicked()'), self.deleteCurrentSignal) 
        self.channelButton.currentIndexChanged['QString'].connect(self.setChannel)
            
        
        # control for recorded signal
        #self.connect(self.sliderAntiNoise, QtCore.SIGNAL('valueChanged(int)'), self.applyAntiNoiseRecordedSignal)
        
        # control for recorded signal
        #self.connect(self.checkboxAntiNoise, QtCore.SIGNAL('clicked()'), self.applyAntiNoiseRecordedSignal)

    #
    # ------------------------------------------------------------------
    #
    # GUI component behaviour
    #
    # ------------------------------------------------------------------
    #
    
    
    def setVerticalScale(self, newVerticalScale):
        print "[Vertical Scale] "+str(newVerticalScale)
        self.signalFrame.getFreqScope().setVerticalScale(newVerticalScale)
        self.signalFrame.getTimeScope().setVerticalScale(newVerticalScale)
    
    def setHorizontalScale(self, newHorizontalScale):
        print "[Horizontal Scale] "+str(newHorizontalScale)
        self.signalFrame.getFreqScope().setHorizontalScale(newHorizontalScale)
        self.signalFrame.getTimeScope().setHorizontalScale(newHorizontalScale)
    
    def closeMainFrame(self):
        self.signalFrame.deleteAllSignal()
        self.close()
    
    def setChannel(self, newChannel) :
        
        # read the channel number from the combobox
        if newChannel == "Channel 1" :
            self.selectedChannel = 1
        elif newChannel == "Channel 2": 
            self.selectedChannel = 2
        else :
            self.selectedChannel = 3
            
    def applyAntiNoiseRecordedSignal(self):
        
        print "[Anti noise] "+str(self.sliderAntiNoise.value())
        
        if not(self.isRecording) and self.checkboxAntiNoise.isChecked():
            
            print "[Anti noise] Display new recorded Signal"
            
            noisePercent  = self.sliderAntiNoise.value()/100
            recordedSignalToDisplay = self.signalFrame.getCurrentSignal().getAntiNoiseSignal(noisePercent)[0]
            self.recordedSignal.plot(recordedSignalToDisplay, clear=True)
            
    #def setAntiNoise(self):
    #    print "[Anti noise] "+str(self.sliderAntiNoise.value())
    #    #self.signalFrame.getFreqScope().setVerticalScale(newVerticalScale)
    
    #
    # ==================================================================
    #
    # SIGNAL MANAGEMENT
    # Link with all the AMVU classes
    #
    # ==================================================================
    #
    def setSize(self, newSize):
        print "[newSize] "+str(newSize)
        
        # destroy the current signal
        self.deleteCurrentSignal()
        
        # replace the current by a new signal using the new size
        rate    = self.signalFrame.getCurrentSignal().rate
        #channel = self.signalFrame.getCurrentSignal().channel
        channel = 2
        format  = self.signalFrame.getCurrentSignal().format
        self.signalFrame.setCurrentSignal(Signal(rate, int(newSize), format, channel))
        self.signalFrame.getCurrentSignal().startRealTimeDisplay()
    
    def setRate(self, newRate):
        print "[newRate] "+str(newRate)
        
        # stop the current signal acquisition
        self.deleteCurrentSignal()
        
        # replace the current by a new signal using the new rate
        size    = self.signalFrame.getCurrentSignal().size
        #channel = self.signalFrame.getCurrentSignal().channel
        channel = 2
        format  = self.signalFrame.getCurrentSignal().format
        self.signalFrame.setCurrentSignal(Signal(int(newRate), size, format, channel))
        self.signalFrame.getCurrentSignal().startRealTimeDisplay()
        
        
    def deleteCurrentSignal(self):
        
        # set a new signal to prepare future recording and allow
        # real time display
        size    = self.signalFrame.getCurrentSignal().size
        rate    = self.signalFrame.getCurrentSignal().rate
        channel = self.signalFrame.getCurrentSignal().channel
        format  = self.signalFrame.getCurrentSignal().format
        
        # delete current recorded signal
        self.signalFrame.deleteCurrentSignal()
        self.recordedSignal.clear()
        
        # set new signal
        self.signalFrame.setCurrentSignal(Signal(rate, size, format, channel))
        self.signalFrame.getCurrentSignal().startRealTimeDisplay()
        

       
    def startRecordNsec(self):
        
        # set the default value for the trigger
        try :
            time = float(self.InputBoxNSecond.text())
        except :
            print "Rentrez une valeur valide nom de Zeus"
            time = -1
            
        if time >= 0 :
        
            print "[Start recording N sec] Allez ça part pour "+str(time)+" s !"
            self.infoAction.setText("[Recording N sec] Allez ça part "+str(time)+" s !")
            
            self.isRecording = True
            
            # restart current signal acquisition
            self.signalFrame.getCurrentSignal().threadsDieNow = False
            
            # restart signal recording
            self.signalFrame.getCurrentSignal().startRecording(time) # signal SR = current sound card record
                                # at any time
            #SR.startTrigger()
            
            # display continuous signal
            timer = QtCore.QTimer()
            timer.start(1.0)
            self.connect(timer, QtCore.SIGNAL('timeout()'), self.updateDisplay)
            
        else :
            # ELSE : negative time is too much for AMVU
            print "[Negative time] Boom, explosion"
            
        self.infoAction.setText("None")
    
    def updateDisplay(self):
        
        #print "[Oh yeah, I update]"
        
        # test if there is a new portion of signal
        # to display
        if (self.signalFrame.getCurrentSignal().newAudio and not(self.signalFrame.getCurrentSignal().threadsDieNow)) :
            
            # get signal and display it
            #T = SCOPE.signalFrame.signalList[SCOPE.signalFrame.currentSignal].getLastSignalRecordedPart()
            #print "[Display signal]"
            self.displaySignal()
    
            # this portion of signal have been displayed        
            self.signalFrame.getCurrentSignal().newAudio = False
        
    def seeRecord(self):
        
        # stop current signal acquisition
        self.signalFrame.getCurrentSignal().threadsDieNow = True
        
        # display recorded signal
        signalToDisplay = self.signalFrame.getCurrentSignal().getWellFormattedTimeSignal()[0]
        print "[Display recorded signal]"
        pg.plot(signalToDisplay) 

    def launchTrigger(self):
        
        # set the default value for the trigger
        try :
            triggerStep = float(self.InputBoxThreshold.text())
        except :
            print "That's not a valid value! Try again"
            self.infoAction.setText("Tuck a valid value")
            triggerStep = 0.0

        print "[Launch trigger] : "+str(triggerStep)
        
        # launch the trigger
        if triggerStep > 0.0 :
            self.signalFrame.getCurrentSignal().startTrigger(triggerStep, 4)
        else :
            print "Calm down, you have to tuck a f*cking value for the trigger to run"
            self.infoAction.setText("Please enter a value in the trigger inputbox")
    
    def exportFile(self):
        
        self.signalFrame.getCurrentSignal().exportWavFormat()

    def startRealTimeSignalDisplay(self):
        
        # restart current signal acquisition
        self.signalFrame.getCurrentSignal().threadsDieNow = False
        
        # restart signal recording
        self.signalFrame.getCurrentSignal().startRealTimeDisplay()
        # at any time
        #SR.startTrigger()
        
        print "[Start real time display]"
        
        # display continuous signal
        timer = QtCore.QTimer()
        timer.start(1.0)
        self.connect(timer, QtCore.SIGNAL('timeout()'), self.updateDisplay)

    def startRecord(self):

        print "[Start recording] Here we go"
        self.infoAction.setText("Beginning of the recording")
        
        self.isRecording = True
        
        # restart current signal acquisition
        self.signalFrame.getCurrentSignal().threadsDieNow = False
        
        # restart signal recording
        self.signalFrame.getCurrentSignal().startRecording() # signal SR = current sound card record
                            # at any time
        #SR.startTrigger()
        
        # display continuous signal
        timer = QtCore.QTimer()
        timer.start(1.0)
        self.connect(timer, QtCore.SIGNAL('timeout()'), self.updateDisplay)
        

    def stopRecording(self):

        self.infoAction.setText("None")
        
        self.isRecording = False

        # stop all recording process
        print "[Stop recording]"
        self.signalFrame.getCurrentSignal().stopRecording()

        # restart real time display but without recording process
        self.startRealTimeSignalDisplay()

#    def getAntiNoiseWorking(self):
#
#        if self.checkboxAntiNoise.isChecked() == 1:
#            self.AntinoiseSliderValue = self.sliderAntiNoise.getValue()
#            print "[Slider value] "+str(self.AntinoiseSliderValue)


def main(args):
    
    global SCOPE
    
    # signal properties
    rate       = 8192   #44100
    size       = 2048    #4096

    # launch the graphics
    a = QApplication(args)
    
    # create a new signal ready to be displayed in the scope
    SIGNAL = Signal(rate, size)
    signalFrame = SignalFrame()
    
    # create the main window
    SCOPE = MainFrame(signalFrame)
    
     # affect a first signal to this scope
    SCOPE.signalFrame.consider(SIGNAL)
    SCOPE.signalFrame.displayLastSignal() # initialize 2 plot for freq and time
    
    # start signal recording
    #startRecord()
    
    # start real time signal acquisition
    SCOPE.startRealTimeSignalDisplay()
    
    # display continuous signal
    timer = QtCore.QTimer()
    timer.start(1.0)
    SCOPE.connect(timer, QtCore.SIGNAL('timeout()'), SCOPE.updateDisplay)
    

    # set all the graphical stuff
    SCOPE.setTitle("AMVU")
    
    # set the toolbar
    SCOPE.setToolBar()
    
    # set the graphical elements of the interface
    #SCOPE.setSize(400,400)
    SCOPE.setSignalInformation()
    SCOPE.setScopes()
    SCOPE.setRecordedSignalDisplay()
    
    SCOPE.setControlPanelRight()
    SCOPE.setControlPanelLeft()
    
    #f.setGraphTab()
    #f.setScopes()
    SCOPE.show()
    r=a.exec_()
    
    # close the signal
    SCOPE.closeMainFrame()

    return r

  
if __name__=="__main__":
    main(sys.argv)
#
