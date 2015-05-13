
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
        self.checkboxStartRecording = None
        self.checkboxStartNsec = None
        self.checkboxStopRecording = None
        self.checkboxTrigger = None
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
        self.timeGraphTab = QWidget() 
        self.freqGraphTab = QWidget()

        # set the tab widget hosting each graph tab
        self.signalGraph = QTabWidget(self) 
        
        self.signalGraph.addTab(self.timeGraphTab,"Time")
        
        self.signalGraph.addTab(self.freqGraphTab,"Freq")
        
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
        self.connect(btnQuit,QtCore.SIGNAL('clicked()'),QtCore.SLOT('close()'))

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
##        self.connect(btnQuit,QtCore.SIGNAL('clicked()'),QtCore.SLOT('close()')

        
    def ExportPDF(self):
        # Export in PDF mode
        print('ExportPDF')

    def ExportPNG(self):
        # Export in PNG mode
        print('ExportPNG')
      
    
    #
    # ORGANIZE EACH TAB ---------------------------------------------
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

    def setSignalInformation(self):
        
        # create a label to display information
        self.informationLabel1 = QtGui.QLabel(u"Amplitude : mv")
        self.informationLabel2 = QtGui.QLabel(u"Valeur crète à crète: rad/s")
        self.informationLabel3 = QtGui.QLabel(u"Temps d'enregistrement : s")
        self.informationLabel4 = QtGui.QLabel(u"Déphasage : rad/s")
        

        # create a combobox to chose the channel to display
        self.channelButton = Qt.QComboBox()
        
        self.channelButton.insertItem(0,"Channels 1+2")
        self.channelButton.insertItem(1,"Channel 1")
        self.channelButton.insertItem(2,"Channel 2")
        
        # add this label to the global interface
        self.signalInformationLayout = QtGui.QGridLayout()
        self.signalInformationLayout.addWidget(self.informationLabel1, 0, 0)
        self.signalInformationLayout.addWidget(self.informationLabel2, 1, 0)
        self.signalInformationLayout.addWidget(self.informationLabel3, 2, 0)
        self.signalInformationLayout.addWidget(self.informationLabel4, 3, 0)
        self.signalInformationLayout.addWidget(self.channelButton, 1, 1)

        self.signalInformation = QWidget()
        self.signalInformation.setLayout(self.signalInformationLayout)
        
        self.globalInterfaceLeftLayout.addWidget(self.signalInformation, 0, 0)
        
    def setControlPanelRight(self):
        
        # define the layout use to dispose the controls
        self.controlPanelRightLayout = QtGui.QGridLayout()
        
        # set all the controls and add them to the layout
        self.controlButtonVerticalScale = Qwt.QwtKnob()
        self.controlButtonVerticalScale.setTotalAngle(270)
        self.controlButtonHorizontalScale = Qwt.QwtKnob()
        self.controlButtonHorizontalScale.setTotalAngle(270)
        
        self.controlButtonSize = Qwt.QwtKnob()
        self.controlButtonSize.setTotalAngle(270)
        self.controlButtonRate = Qwt.QwtKnob()
        self.controlButtonRate.setTotalAngle(270)
        
        #rate       = 8192   #44100
        #size       = 2048    #4096
        
        self.controlButtonSize.setScale(512, 4096, 512)
        self.controlButtonSize.setRange(512, 4096)
        self.controlButtonRate.setScale(8192, 44100, 4096)
        self.controlButtonRate.setRange(8192, 44100)
##        
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
        
        
####        # define the layout use to dispose the text above the Filters checkbox
####        self.checkboxAntiNoiseLayout = QtGui.QGridLayout()
####        self.checkboxLPLayout = QtGui.QGridLayout()
####        self.checkboxHPLayout = QtGui.QGridLayout()
####        self.checkboxBPLayout = QtGui.QGridLayout()
####        self.checkboxCutLayout =QtGui.QGridLayout()

        
        # set all the controls       
        
        # S122 : i think it's better for the main control to be buttons
        #        they are the control the user use the most, they have
        #        to be wide and different from the others controls
        self.checkboxStartRecording = QtGui.QPushButton("Start",self)
        self.checkboxStopRecording = QtGui.QCheckBox("Stop",self)
        # ---------------------------------------------------------------
        
        self.checkboxStartNsec = QtGui.QPushButton("",self)
        
        self.checkboxTrigger = QtGui.QCheckBox("",self)        
        self.checkboxOffset = QtGui.QCheckBox("",self)
        
        self.checkboxDerivate = QtGui.QCheckBox("",self)
        self.checkboxIntegrate = QtGui.QCheckBox("",self)

        self.checkboxAntiNoise = QtGui.QCheckBox("",self)
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
        

        # add all the controls to the layout        
        self.controlPanelLeftLayout.addWidget(self.checkboxStartRecording, 0, 0)
        self.controlPanelLeftLayout.addWidget(self.checkboxStartNsec, 1, 0)
        self.controlPanelLeftLayout.addWidget(self.checkboxStopRecording, 2, 0)
        self.controlPanelLeftLayout.addWidget(self.checkboxTrigger, 3, 0)
        self.controlPanelLeftLayout.addWidget(self.checkboxOffset, 4, 0)

        self.controlPanelLeftLayout.addWidget(self.checkboxDerivate, 5, 0)
        self.controlPanelLeftLayout.addWidget(self.checkboxIntegrate, 5, 1)

        self.controlPanelLeftLayout.addWidget(self.checkboxAntiNoise, 7, 0)
        self.controlPanelLeftLayout.addWidget(self.checkboxLP, 8, 0)
        self.controlPanelLeftLayout.addWidget(self.checkboxHP, 8, 1)
        self.controlPanelLeftLayout.addWidget(self.checkboxBP, 9, 0)
        self.controlPanelLeftLayout.addWidget(self.checkboxCut, 9, 1)

        self.controlPanelLeftLayout.addWidget(self.InputBoxNSecond, 1, 1)
        self.controlPanelLeftLayout.addWidget(self.InputBoxFrequency1, 10, 1)
        self.controlPanelLeftLayout.addWidget(self.InputBoxFrequency2, 11, 1)
        self.controlPanelLeftLayout.addWidget(self.InputBoxThreshold, 12, 1)
        self.controlPanelLeftLayout.addWidget(self.InputBoxOffset, 13, 1)
        self.controlPanelLeftLayout.addWidget(self.InputBoxChanel1Sensibility, 14, 0)
        self.controlPanelLeftLayout.addWidget(self.InputBoxChanel2Sensibility, 15, 0)
        

        # add tooltips on each button
        self.checkboxStartRecording.setToolTip('Start recording the measure')
        self.checkboxStartNsec.setToolTip('Start recording the measure for a number of seconds specified. The record will automatically stop itself')
        self.checkboxStopRecording.setToolTip('Stop recording the measure')
        self.checkboxTrigger.setToolTip('Use the mode Trigger to automatically start recording for a threshold specified')
        self.checkboxOffset.setToolTip('Add an offset to the measure ')
     
        self.checkboxDerivate.setToolTip('Derivate the signal')
        self.checkboxIntegrate.setToolTip('Integrate the signal')

        self.checkboxAntiNoise.setToolTip('Activate the antinoise filter')
        self.checkboxLP.setToolTip('Activate the Low Pass filter')
        self.checkboxHP.setToolTip('Activate the High Pass filter')
        self.checkboxBP.setToolTip('Activate the Band Pass filter')
        self.checkboxCut.setToolTip('Activate the Band Cut filter')      
        

        #add text to all the buttons
        self.checkboxStartRecording.setText('Start Recording')
        self.checkboxStartNsec.setText('Start for N sec')
        self.checkboxStopRecording.setText('Stop Recording')
        self.checkboxTrigger.setText('Trigger')
        self.checkboxOffset.setText('Offset')

        self.checkboxDerivate.setText('Derivate')
        self.checkboxIntegrate.setText('Integrate')

        self.checkboxAntiNoise.setText('AntiNoise Filter')
        self.checkboxLP.setText('Low Pass Filter')
        self.checkboxHP.setText('High Pass Filter')
        self.checkboxBP.setText('Band Pass Filter')
        self.checkboxCut.setText('Band Cut Filter')


        #create label with the text of the inputbox as a Widget to be put in the grid above the checkbox
        self.InputBoxNSecondText = QtGui.QLabel("")
        self.InputBoxFrequency1Text = QtGui.QLabel("Frequency 1")
        self.InputBoxFrequency2Text = QtGui.QLabel("Frequency 2")
        self.InputBoxThresholdText = QtGui.QLabel("Threshold")
        self.InputBoxOffsetText = QtGui.QLabel("Offset")
        self.InputBoxChanel1SensibilityText = QtGui.QLabel("Chanel 1 Sensibility")
        self.InputBoxChanel2SensibilityText = QtGui.QLabel("Chanel 2 Sensibility")       
        

        #add the text and the checkbox on each layout
        self.controlPanelLeftLayout.addWidget(self.InputBoxFrequency1Text, 10, 0)
        self.controlPanelLeftLayout.addWidget(self.InputBoxFrequency2Text, 11, 0)
        self.controlPanelLeftLayout.addWidget(self.InputBoxThresholdText, 12, 0)
        self.controlPanelLeftLayout.addWidget(self.InputBoxOffsetText, 13, 0)
        self.controlPanelLeftLayout.addWidget(self.InputBoxChanel1SensibilityText, 14, 1)
        self.controlPanelLeftLayout.addWidget(self.InputBoxChanel2SensibilityText, 15, 1)
#<<<<<<< HEAD

        # create the frames aroud the checkboxs
       

        # add the frame around the ckeckboxs
        
    


##        #set Alignment to the text QLabel

        #set Alignment to the text QLabel

##        self.InputBoxFrequency1Text.setAlignment(QtCore.Qt.AlignRight)
##        self.InputBoxFrequency2Text.setAlignment(QtCore.Qt.AlignRight)
##        self.InputBoxThresholdText.setAlignment(QtCore.Qt.AlignRight)
##        self.InputBoxOffsetText.setAlignment(QtCore.Qt.AlignRight)
        
#=======
    
#>>>>>>> 2fa4b70b82c65a2ac6ef41b160a3d131f1f52808
        
        # add all this stuff to the global interface
        self.controlPanelLeft = QWidget()
        self.controlPanelLeft.setLayout(self.controlPanelLeftLayout)
        
        self.globalInterfaceCenterLayout.addWidget(self.controlPanelLeft, 0, 0)

        #put margins around the widget
        self.controlPanelLeft.setContentsMargins( 0, 100, 0, 0)

        #add group button to make exclusive some of the checkbox
        self.GroupRecording = QtGui.QButtonGroup(self.controlPanelLeft)
        self.GroupMath = QtGui.QButtonGroup(self.controlPanelLeft)
        self.GroupFilter = QtGui.QButtonGroup(self.controlPanelLeft)

        #add the checkboxs to the group
        self.GroupRecording.addButton(self.checkboxStartRecording)
        self.GroupRecording.addButton(self.checkboxStopRecording)

        #make the groups exclusive
        self.GroupRecording.setExclusive(True)
        
        # connect GUI
        self.connectGUI()
        
    def displaySignal(self):
        """ Display signal in temporal and frequential form """
        
        #print "[Oh yeah, I display]"
        
        # get the data to display
        dataToDisplay = self.signalFrame.signalList[SCOPE.signalFrame.currentSignal].getLastSignalRecordedPart()
        rate          = self.signalFrame.signalList[SCOPE.signalFrame.currentSignal].rate
        
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
 
    #
    # ------------------------------------------------------------------
    #
    # GUI component behaviour
    #
    # ------------------------------------------------------------------
    #
    
    def setSize(self, newSize):
        print "[newSize] "+str(newSize)
        
        # replace the current by a new signal using the new size
        rate    = self.signalFrame.signalList[SCOPE.signalFrame.currentSignal].rate
        channel = self.signalFrame.signalList[SCOPE.signalFrame.currentSignal].channel
        self.signalFrame.signalList[SCOPE.signalFrame.currentSignal] = Signal(rate, newSize, channel)
        self.signalFrame.signalList[SCOPE.signalFrame.currentSignal].actualizeSignalPart()
    
    def setRate(self, newRate):
        print "[newRate] "+str(newRate)
        
        # replace the current by a new signal using the new size
        size    = self.signalFrame.signalList[SCOPE.signalFrame.currentSignal].size
        channel = self.signalFrame.signalList[SCOPE.signalFrame.currentSignal].channel
        self.signalFrame.signalList[SCOPE.signalFrame.currentSignal] = Signal(newRate, size, channel)
        self.signalFrame.signalList[SCOPE.signalFrame.currentSignal].actualizeSignalPart()
    
    
        
#
# ==================================================================
#
# SIGNAL MANAGEMENT
# Link with all the AMVU classes
#
# ==================================================================
#
def updateDisplay():
    
    global SCOPE
    
    #print "[Oh yeah, I update]"
    
    # test if there is a new portion of signal
    # to display
    if (SCOPE.signalFrame.signalList[SCOPE.signalFrame.currentSignal].newAudio and not(SCOPE.signalFrame.signalList[SCOPE.signalFrame.currentSignal].threadsDieNow)) :
        
        # get signal and display it
        #T = SCOPE.signalFrame.signalList[SCOPE.signalFrame.currentSignal].getLastSignalRecordedPart()
        #print "[Display signal]"
        SCOPE.displaySignal()

        # this portion of signal have been displayed        
        SCOPE.signalFrame.signalList[SCOPE.signalFrame.currentSignal].newAudio = False
        
def seeRecord():
    
    global SCOPE
    
    # stop current signal acquisition
    SCOPE.signalFrame.signalList[SCOPE.signalFrame.currentSignal].threadsDieNow = True
    
    # display recorded signal
    signalToDisplay = SIGNAL.getWellFormattedTimeSignal()[0]
    print "[Display recorded signal]"
    pg.plot(signalToDisplay) 


def launchTrigger():
    
    global SCOPE
    
    # set the default value for the trigger
    triggerStep = 12222
    
    # launch the trigger
    SCOPE.signalFrame.signalList[SCOPE.signalFrame.currentSignal].startTrigger(triggerStep, 4)
    
def exportFile():
    
    global SCOPE
    
    SCOPE.signalFrame.signalList[SCOPE.signalFrame.currentSignal].exportWavFormat()
    
def startRecord():
    
    global SCOPE
    
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
    
def startRealTimeSignalDisplay():
    
    global SCOPE
    
    # restart current signal acquisition
    SCOPE.signalFrame.signalList[SCOPE.signalFrame.currentSignal].threadsDieNow = False
    
    # restart signal recording
    SCOPE.signalFrame.signalList[SCOPE.signalFrame.currentSignal].startRealTimeDisplay()
    # at any time
    #SR.startTrigger()
    
    # display continuous signal
    timer = QtCore.QTimer()
    timer.start(1.0)
    SCOPE.connect(timer, QtCore.SIGNAL('timeout()'), updateDisplay)


#
# ====================================================
#

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
    SCOPE.connect(timer, QtCore.SIGNAL('timeout()'), updateDisplay)
    

    # set all the graphical stuff
    SCOPE.setTitle("AMVU")
    
    # set the toolbar
    SCOPE.setToolBar()
    
    # set the graphical elements of the interface
    #f.resize(1400,700)
    SCOPE.setSignalInformation()
    SCOPE.setScopes()
    SCOPE.setControlPanelRight()
    SCOPE.setControlPanelLeft()
    
    #f.setGraphTab()
    #f.setScopes()
    SCOPE.show()
    r=a.exec_()
    
    # close the signal
    SCOPE.signalFrame.signalList[SCOPE.signalFrame.currentSignal].threadsDieNow = True
    SCOPE.signalFrame.signalList[SCOPE.signalFrame.currentSignal].stopSignalStream()


    return r

  
if __name__=="__main__":
    main(sys.argv)
#
