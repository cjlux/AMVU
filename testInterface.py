
#-*-coding: utf-8 -*-
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

#
# Global values
#

# stand for the MainFrame object used
# in different function
SCOPE = None


class MainFrame(QMainWindow):

    def __init__(self, signalFrame):
        
        QMainWindow.__init__(self)

        # signal frame for signal display and management
        self.signalFrame = signalFrame
      
        #know the size of the main frame
        size_fenetre = self.geometry()
        size_fenetre = size_fenetre.getCoords()
        width_fenetre = size_fenetre[2]
        height_fenetre = size_fenetre[3]
          
        # tabs
        self.timeGraphTab = None
        self.freqGraphTab = None
        
        # control buttons
        #self.stack      = None
        self.btnPause   = None
        self.grid       = None
        
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
        
#<<<<<<< Updated upstream
        # for tab 1      
#=======
        # for tab 1
#<<<<<<< Updated upstream
#>>>>>>> Stashed changes
        self.StartRecording = None
        self.StartNsec = None
        self.StopRecording = None
        self.Trigger = None
        self.checkboxOffset = None
        self.checkboxAntiNoise = None
        self.checkboxDerivate = None
        self.checkboxIntegrate = None
        self.checkboxLP = None
        self.checkboxHP = None
        self.checkboxBP = None
        self.checkboxCut = None
#<<<<<<< Updated upstream
        self.InputBoxNSecond = None
        self.InputBoxFrequency1 = None
        self.InputBoxFrequency2 = None
        self.InputBoxThreshold = None
        self.InputBoxOffset = None
        self.InputBoxChanel1Sensibility = None
        self.InputBoxChanel2Sensibility = None
               
#=======
        
        # for tab 2
        
#=======
        #self.controlButton11 = None
        #self.controlButton12 = None
        
        # for tab 2
        #self.controlButton21 = None
        #self.controlButton22 = None
#>>>>>>> Stashed changes
#>>>>>>> Stashed changes
        
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
        self.globalInterfaceCenter.setFixedSize(0.50*width_fenetre,height_fenetre)

    def setTitle(self, titre="") :
        self.setWindowTitle(titre)

    def setGraphTab(self):
        
        # set each graph tab
        self.timeGraphTab   = QWidget() 
        self.freqGraphTab   = QWidget()
        self.recordedSignal = QWidget()

        # set the tab widget hosting each graph tab
        self.signalGraph = QTabWidget(self) 
        self.signalGraph.addTab(self.timeGraphTab,"Time")
        self.signalGraph.addTab(self.freqGraphTab,"Freq")
        self.signalGraph.addTab(self.recordedSignal,"Recorded signal")
        
        # add the graph tab to the global interface
        self.globalInterfaceLeftLayout.addWidget(self.signalGraph, 1, 0)

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

        self.btnPause = Qt.QToolButton(toolBar)
        self.btnPause.setText("Pause")
        self.btnPause.setToolTip('Pauses the acquisition...')
        self.btnPause.setIcon(Qt.QIcon("pause"))
        self.btnPause.setCheckable(True)
        self.btnPause.setToolButtonStyle(Qt.Qt.ToolButtonTextUnderIcon)
        toolBar.addWidget(self.btnPause)
        #self.connect(self.btnPause,Qt.SIGNAL('toggled(bool)'),self.Pause)

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
        self.timeGraph =  self.signalFrame.timeScope
        self.freqGraph =  self.signalFrame.freqScope
        
        # add the graphs to the tabs
        self.timeGraphLayout = QtGui.QGridLayout()
        self.freqGraphLayout = QtGui.QGridLayout()
        
        self.timeGraphLayout.addWidget(self.timeGraph, 0, 0)
        self.freqGraphLayout.addWidget(self.freqGraph, 0, 0)
        
        self.timeGraphTab.setLayout(self.timeGraphLayout)
        self.freqGraphTab.setLayout(self.freqGraphLayout)

    def setRecordedSignalDisplay(self):
        self.recordedSignal = pg.PlotWidget()

    def setSignalInformation(self):
        
        # create a label to display information
        self.informationLabel1 = QtGui.QLabel(u"Amplitude : mv")
        self.informationLabel2 = QtGui.QLabel(u"Valeur crète à crète: rad/s")
        self.informationLabel3 = QtGui.QLabel(u"Temps d'enregistrement : s")
        self.informationLabel4 = QtGui.QLabel(u"Déphasage : rad/s")
        
        
        # add this label to the global interface
        self.signalInformationLayout = QtGui.QGridLayout()
        self.signalInformationLayout.addWidget(self.informationLabel1, 0, 0)
        self.signalInformationLayout.addWidget(self.informationLabel2, 1, 0)
        self.signalInformationLayout.addWidget(self.informationLabel3, 2, 0)
        self.signalInformationLayout.addWidget(self.informationLabel4, 3, 0)
        
        self.signalInformation = QWidget()
        self.signalInformation.setLayout(self.signalInformationLayout)
        
        self.globalInterfaceLeftLayout.addWidget(self.signalInformation, 0, 0)
        
    def setControlPanelRight(self):
        
        # define the layout use to dispose the controls
        self.controlPanelRightLayout = QtGui.QGridLayout()
        
        # set all the controls and add them to the layout
        
        # scales controls
        self.controlButtonVerticalScale = Qwt.QwtKnob()
        self.controlButtonVerticalScale.setTotalAngle(270)
        self.controlButtonHorizontalScale = Qwt.QwtKnob()
        self.controlButtonHorizontalScale.setTotalAngle(270)
        
        # set propreties for this controls
        self.controlButtonVerticalScale.setScale(0, 1, 0.2)
        self.controlButtonVerticalScale.setRange(0, 1)
        self.controlButtonHorizontalScale.setScale(0, 0.5, 0.1)
        self.controlButtonHorizontalScale.setRange(0, 0.5)
        
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
        self.controlPanelRightLayout.addWidget(self.controlButtonVerticalScale, 0, 0)
        self.controlPanelRightLayout.addWidget(self.controlButtonHorizontalScale, 2, 0)
        self.controlPanelRightLayout.addWidget(self.controlButtonSize, 4, 0)
        self.controlPanelRightLayout.addWidget(self.controlButtonRate, 6, 0)

        
        # set  all buttons' Ranges     
    

        # Add text under each button

        self.button1Text = Qt.QLabel("Vertical Scale")
        self.button1Text.setAlignment(QtCore.Qt.AlignCenter)
        self.button2Text = Qt.QLabel("Horizontal Scale")
        self.button2Text.setAlignment(QtCore.Qt.AlignCenter)
        self.button3Text = Qt.QLabel("Size")
        self.button3Text.setAlignment(QtCore.Qt.AlignCenter)
        self.button4Text = Qt.QLabel("Rate")
        self.button4Text.setAlignment(QtCore.Qt.AlignCenter)

        # set all the texts and add them to the layout

        self.controlPanelRightLayout.addWidget(self.button1Text, 1, 0)
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
        
        
        self.StartRecording = QtGui.QPushButton("Start",self)
        self.StartNsec = QtGui.QPushButton("",self)
        self.StopRecording = QtGui.QPushButton("Stop",self)        
        self.Trigger = QtGui.QPushButton("",self)
        
        self.checkboxOffset = QtGui.QCheckBox("",self)
        
        self.checkboxDerivate = QtGui.QCheckBox("",self)
        self.checkboxIntegrate = QtGui.QCheckBox("",self)

        self.checkboxAntiNoise = QtGui.QCheckBox("",self)
        self.sliderAntiNoise = QtGui.QSlider(self)
                
        self.checkboxLP = QtGui.QCheckBox("",self)
        self.checkboxHP = QtGui.QCheckBox("",self)
        self.checkboxBP = QtGui.QCheckBox("",self)
        self.checkboxCut = QtGui.QCheckBox("",self)

        self.InputBoxNSecond = QtGui.QLineEdit(self)
        self.InputBoxFrequency1 = QtGui.QLineEdit(self)
        self.InputBoxFrequency2 = QtGui.QLineEdit(self)
        self.InputBoxThreshold = QtGui.QLineEdit(self)
        self.InputBoxOffset = QtGui.QLineEdit(self)
        self.InputBoxChanel1Sensibility = QtGui.QLineEdit(self)
        self.InputBoxChanel2Sensibility = QtGui.QLineEdit(self)

        #create label with the text of the inputbox as a Widget to be put in the grid above the checkbox
        self.EmptyText = QtGui.QLabel(" ")
        self.InputBoxNSecondText = QtGui.QLabel("sec")
        self.InputBoxThresholdText = QtGui.QLabel("Threshold")
        self.InputBoxFrequency1Text = QtGui.QLabel("Frequency 1")
        self.InputBoxFrequency2Text = QtGui.QLabel("Frequency 2")
        self.InputBoxOffsetText = QtGui.QLabel("Offset")
        self.InputBoxChanel1SensibilityText = QtGui.QLabel("Channel 1 Sensibility")
        self.InputBoxChanel2SensibilityText = QtGui.QLabel("Channel 2 Sensibility")       
               

        # add all the controls and text to the layout
        self.controlPanelLeftLayout.addWidget(self.channelButton, 0, 0)
        self.controlPanelLeftLayout.addWidget(self.EmptyText, 1, 0)
        self.controlPanelLeftLayout.addWidget(self.StartRecording, 2, 0)
        self.controlPanelLeftLayout.addWidget(self.StartNsec, 3, 0)
        self.controlPanelLeftLayout.addWidget(self.InputBoxNSecond, 3, 1)
        self.controlPanelLeftLayout.addWidget(self.InputBoxNSecondText, 3, 2)
        self.controlPanelLeftLayout.addWidget(self.StopRecording, 4, 0)
        self.controlPanelLeftLayout.addWidget(self.Trigger, 5, 0)
        self.controlPanelLeftLayout.addWidget(self.InputBoxThreshold, 5, 1)
        self.controlPanelLeftLayout.addWidget(self.InputBoxThresholdText, 5, 2)        
        self.controlPanelLeftLayout.addWidget(self.checkboxOffset, 6, 0)
        self.controlPanelLeftLayout.addWidget(self.checkboxDerivate, 7, 0)
        self.controlPanelLeftLayout.addWidget(self.checkboxIntegrate, 7, 1)
        self.controlPanelLeftLayout.addWidget(self.checkboxAntiNoise, 8, 0)
        self.controlPanelLeftLayout.addWidget(self.sliderAntiNoise, 8, 1)
        self.controlPanelLeftLayout.addWidget(self.checkboxLP, 9, 0)
        self.controlPanelLeftLayout.addWidget(self.checkboxHP, 9, 1)
        self.controlPanelLeftLayout.addWidget(self.checkboxBP, 10, 0)
        self.controlPanelLeftLayout.addWidget(self.checkboxCut, 10, 1)
        self.controlPanelLeftLayout.addWidget(self.InputBoxFrequency1Text, 11, 0)
        self.controlPanelLeftLayout.addWidget(self.InputBoxFrequency1, 11, 1)
        self.controlPanelLeftLayout.addWidget(self.InputBoxFrequency2Text, 12, 0)
        self.controlPanelLeftLayout.addWidget(self.InputBoxFrequency2, 12, 1)
        self.controlPanelLeftLayout.addWidget(self.InputBoxOffsetText, 13, 0)
        self.controlPanelLeftLayout.addWidget(self.InputBoxOffset, 13, 1)
        self.controlPanelLeftLayout.addWidget(self.InputBoxChanel1Sensibility, 14, 0)
        self.controlPanelLeftLayout.addWidget(self.InputBoxChanel1SensibilityText, 14, 1)
        self.controlPanelLeftLayout.addWidget(self.InputBoxChanel2Sensibility, 15, 0)
        self.controlPanelLeftLayout.addWidget(self.InputBoxChanel2SensibilityText, 15, 1)
        

        # add tooltips on each button
        self.channelButton.setToolTip('Choose the channel to be displayed')
        self.StartRecording.setToolTip('Start recording the measure')
        self.StartNsec.setToolTip('Start recording the measure for a number of seconds specified. The record will automatically stop itself')
        self.StopRecording.setToolTip('Stop recording the measure')
        self.Trigger.setToolTip('Use the mode Trigger to automatically start recording for the threshold specified')
        self.checkboxOffset.setToolTip('Add an offset to the measure ')
     
        self.checkboxDerivate.setToolTip('Derivate the signal')
        self.checkboxIntegrate.setToolTip('Integrate the signal')

        self.checkboxAntiNoise.setToolTip('Activate the AntiNoise filter')
        self.checkboxLP.setToolTip('Activate the Low Pass filter')
        self.checkboxHP.setToolTip('Activate the High Pass filter')
        self.checkboxBP.setToolTip('Activate the Band Pass filter')
        self.checkboxCut.setToolTip('Activate the Band Cut filter')
        self.InputBoxFrequency1.setToolTip('Principal frequency used by the Low Noise filter and the High Pass filter')
        self.InputBoxFrequency2.setToolTip('secondary frequency used by the Band Pass filter and the Band Cut filter')
        
        

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


        #set Alignment to the text QLabel

##        self.InputBoxFrequency1Text.setAlignment(QtCore.Qt.AlignRight)
##        self.InputBoxFrequency2Text.setAlignment(QtCore.Qt.AlignRight)
##        self.InputBoxThresholdText.setAlignment(QtCore.Qt.AlignRight)
##        self.InputBoxOffsetText.setAlignment(QtCore.Qt.AlignRight)
        
#=======
    

        
        # add all this stuff to the global interface
        self.controlPanelLeft = QWidget()
        self.controlPanelLeft.setLayout(self.controlPanelLeftLayout)
        
        self.globalInterfaceCenterLayout.addWidget(self.controlPanelLeft, 0, 0)

        #put margins around the widget
        self.controlPanelLeft.setContentsMargins( 0, 20, 0, 0)

        #add group button to make exclusive some of the checkbox
        self.GroupRecording = QtGui.QButtonGroup(self.controlPanelLeft)
        self.GroupMath = QtGui.QButtonGroup(self.controlPanelLeft)
        self.GroupFilter = QtGui.QButtonGroup(self.controlPanelLeft)

        #add the checkboxs to the group
        self.GroupRecording.addButton(self.StartRecording)
        self.GroupRecording.addButton(self.StopRecording)

        #make the groups exclusive
        self.GroupRecording.setExclusive(True)
        
        # connect GUI
        self.connectGUI()
        
    def displaySignal(self):
        """ Display signal in temporal and frequential form """
        
        #print "[Oh yeah, I display]"
        
        # get the data to display
        dataToDisplay = self.signalFrame.signalList[self.signalFrame.currentSignal].getLastSignalRecordedPart()
        rate          = self.signalFrame.signalList[self.signalFrame.currentSignal].rate
        
        # display it
        self.signalFrame.timeScope.update(dataToDisplay, rate)
        self.signalFrame.freqScope.update(Signal.getFreqSignalFromTimeSignal(dataToDisplay), rate)
 
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
        self.connect(self.controlButtonSize, Qt.SIGNAL("valueChanged(double)"), self.setSize)
        self.connect(self.controlButtonRate, Qt.SIGNAL("valueChanged(double)"), self.setRate)
        self.connect(self.controlButtonVerticalScale, Qt.SIGNAL("valueChanged(double)"), self.setVerticalScale)
        self.connect(self.controlButtonHorizontalScale, Qt.SIGNAL("valueChanged(double)"), self.setHorizontalScale)
 
    #
    # ------------------------------------------------------------------
    #
    # GUI component behaviour
    #
    # ------------------------------------------------------------------
    #
    
    def __deleteCurrentSignal(self):
        self.signalFrame.deleteCurrentSignal()
    
    def setSize(self, newSize):
        print "[newSize] "+str(newSize)
        
        # destroy the current signal
        self.__deleteCurrentSignal()
        
        # replace the current by a new signal using the new size
        rate    = self.signalFrame.getCurrentSignal().rate
        channel = self.signalFrame.getCurrentSignal().channel
        format  = self.signalFrame.getCurrentSignal().format
        self.signalFrame.setCurrentSignal(Signal(rate, int(newSize), format, channel))
        self.signalFrame.getCurrentSignal().startRealTimeDisplay()
    
    def setRate(self, newRate):
        print "[newRate] "+str(newRate)
        
        # stop the current signal acquisition
        self.__deleteCurrentSignal()
        
        # replace the current by a new signal using the new size
        size    = self.signalFrame.getCurrentSignal().size
        channel = self.signalFrame.getCurrentSignal().channel
        format  = self.signalFrame.getCurrentSignal().format
        self.signalFrame.setCurrentSignal(Signal(int(newRate), size, format, channel))
        self.signalFrame.getCurrentSignal().startRealTimeDisplay()
    
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
    
    #
    # ==================================================================
    #
    # SIGNAL MANAGEMENT
    # Link with all the AMVU classes
    #
    # ==================================================================
    #
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
        triggerStep = 12222
        
        # launch the trigger
        self.signalFrame.getCurrentSignal().startTrigger(triggerStep, 4)
    
    def exportFile(self):
        
        self.signalFrame.getCurrentSignal().exportWavFormat()
    
    
    


#
# ====================================================
#

def startRealTimeSignalDisplay():
    
    # restart current signal acquisition
    SCOPE.signalFrame.getCurrentSignal().threadsDieNow = False
    
    # restart signal recording
    SCOPE.signalFrame.getCurrentSignal().startRealTimeDisplay()
    # at any time
    #SR.startTrigger()
    
    print "[Start RTSD]"
    
    # display continuous signal
    timer = QtCore.QTimer()
    timer.start(1.0)
    SCOPE.connect(timer, QtCore.SIGNAL('timeout()'), SCOPE.updateDisplay)

def startRecord():
    
    # restart current signal acquisition
    SCOPE.signalFrame.getCurrentSignal().threadsDieNow = False
    
    # restart signal recording
    SCOPE.signalFrame.getCurrentSignal().startRecording() # signal SR = current sound card record
                        # at any time
    #SR.startTrigger()
    
    # display continuous signal
    timer = QtCore.QTimer()
    timer.start(1.0)
    SCOPE.connect(timer, QtCore.SIGNAL('timeout()'), SCOPE.updateDisplay)

def stopRecording():
    SCOPE.signalFrame.getCurrentSignal().stopRecording()

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
    startRealTimeSignalDisplay()
    
    # display continuous signal
    timer = QtCore.QTimer()
    timer.start(1.0)
    SCOPE.connect(timer, QtCore.SIGNAL('timeout()'), SCOPE.updateDisplay)
    

    # set all the graphical stuff
    SCOPE.setTitle("AMVU")
    
    # set the toolbar
    SCOPE.setToolBar()
    
    # set the graphical elements of the interface
    #f.resize(1400,700)
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
