
#-*-coding: utf-8 -*-
from PyQt4 import QtGui
from PyQt4.QtGui import QMainWindow,QWidget,QAction,QTabWidget,QApplication
from PyQt4 import Qt
from PyQt4 import QtCore
from PyQt4 import Qwt5 as Qwt

import os,sys
import Icons
import numpy as np

class MainFrame(QMainWindow):

    def __init__(self):
        
        QMainWindow.__init__(self)

        self.resize(1100,700)

      
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
        self.layoutTab1 = None
        self.layoutTab2 = None
        
        # Layouts for the controls
        self.layoutControls1 = None
        self.layoutControls2 = None
        
        # Layouts for the graphs
        self.layoutGraph1 = None
        self.layoutGraph2 = None

        
        # WIDGETS ------------------------------------------

        
        # Control widget for each tab
        self.controlWidget1 = None
        self.controlWidget2 = None
        
        # Graph widget for each tab
        self.graphWidget1 = None
        self.graphWidget2 = None
        
        
        # GRAPHS ------------------------------------------

        
        # graph for each tab
        self.timeGraph = None
        self.freqGraph = None

        
        # BUTTONS ------------------------------------------

        
        # Control buttons for each tab
        
        # for tab 1
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
        self.InputBoxNSecond = None
        self.InputBoxFrequency1 = None
        self.InputBoxFrequency2 = None
        self.InputBoxThreshold = None
        self.InputBoxOffset = None
        self.InputBoxChanel1Sensibility = None
        self.InputBoxChanel2Sensibility = None
        
        # for tab 2
        
        
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

        #change size
        self.globalInterfaceCenter.setFixedSize(0.25*width_fenetre,700)


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
    # SET THE GRAPHS FOR EACH TAB -----------------------------------------
    #
        
    def setTimeGraph(self):
        # set the graph for the first tab
        # In this example, the graph is just a Qlabel
        # This is where the link with others class will be
        
        self.timeGraph = Qwt.QwtPlot()

        # grid
        self.grid = Qwt.QwtPlotGrid()
        self.grid.enableXMin(True)
        self.grid.setMajPen(Qt.QPen(Qt.Qt.gray, 0, Qt.Qt.SolidLine))
        self.grid.attach(self.timeGraph)

        # axes
        self.timeGraph.enableAxis(Qwt.QwtPlot.yRight);
        self.timeGraph.setAxisTitle(Qwt.QwtPlot.xBottom, 'Time [s]');
        self.timeGraph.setAxisTitle(Qwt.QwtPlot.yLeft,  'Amplitude Chan. 1 [V]');
        self.timeGraph.setAxisTitle(Qwt.QwtPlot.yRight, 'Amplitude Chan. 2 [V]');
        self.timeGraph.setAxisMaxMajor(Qwt.QwtPlot.xBottom, 10);
        self.timeGraph.setAxisMaxMinor(Qwt.QwtPlot.xBottom, 0);

        self.timeGraph.setAxisScaleEngine(Qwt.QwtPlot.yRight, Qwt.QwtLinearScaleEngine());
        self.timeGraph.setAxisMaxMajor(Qwt.QwtPlot.yLeft, 10);
        self.timeGraph.setAxisMaxMinor(Qwt.QwtPlot.yLeft, 0);
        self.timeGraph.setAxisMaxMajor(Qwt.QwtPlot.yRight, 10);
        self.timeGraph.setAxisMaxMinor(Qwt.QwtPlot.yRight, 0);
        
        # add the graph to the interface using a layout
        #self.layoutGraph1 = QtGui.QGridLayout()
        #self.layoutGraph1.addWidget(self.timeGraph, 0, 0)
        #self.graphWidget1 = QtGui.QWidget()
        #self.graphWidget1.setLayout(self.layoutGraph1)
    
    def setFreqGraph(self):
        # set the graph for the second tab
        # In this example, the graph is just a Qlabel
        # This is where the link with others class will be
        
        # create the graph
        self.freqGraph = Qwt.QwtPlot()

        # grid
        self.grid = Qwt.QwtPlotGrid()
        self.grid.enableXMin(True)
        self.grid.setMajPen(Qt.QPen(Qt.Qt.gray, 0, Qt.Qt.SolidLine))
        self.grid.attach(self.freqGraph)

        # axes
        self.freqGraph.enableAxis(Qwt.QwtPlot.yRight);
        self.freqGraph.setAxisTitle(Qwt.QwtPlot.xBottom, 'Time [s]');
        self.freqGraph.setAxisTitle(Qwt.QwtPlot.yLeft,  'Amplitude Chan. 1 [V]');
        self.freqGraph.setAxisTitle(Qwt.QwtPlot.yRight, 'Amplitude Chan. 2 [V]');
        self.freqGraph.setAxisMaxMajor(Qwt.QwtPlot.xBottom, 10);
        self.freqGraph.setAxisMaxMinor(Qwt.QwtPlot.xBottom, 0);

        self.freqGraph.setAxisScaleEngine(Qwt.QwtPlot.yRight, Qwt.QwtLinearScaleEngine());
        self.freqGraph.setAxisMaxMajor(Qwt.QwtPlot.yLeft, 10);
        self.freqGraph.setAxisMaxMinor(Qwt.QwtPlot.yLeft, 0);
        self.freqGraph.setAxisMaxMajor(Qwt.QwtPlot.yRight, 10);
        self.freqGraph.setAxisMaxMinor(Qwt.QwtPlot.yRight, 0);
        
        # add the graph to the interface using a layout
        #self.layoutGraph2 = QtGui.QGridLayout()
        #self.layoutGraph2.addWidget(self.freqGraph, 0, 0)
        #self.graphWidget2 = QtGui.QWidget()
        #self.graphWidget2.setLayout(self.layoutGraph2)

    #
    # SET THE BUTTONS FOR EACH TAB ---------------------------------------
    #
    # This buttons are currently QPushButton objects.
    # They can be knob, radio button, ... It only depends on the class used.
    # This buttons aren't linked to an action for the moment : if someone
    # click on them, nothing happen (except a nuclear explosion in some far away
    # countries, but nevermind... ).
    #
    
####    def setControl1(self):
####        # set the controls for the first tab
####        
####        # set a layout to clearly dispose all the buttons
####        self.layoutControls1 = QtGui.QGridLayout()
####        
####        # create all the control buttons
####        self.controlButton11 = QtGui.QPushButton("Button 1 tab 1")
####        self.controlButton12 = QtGui.QPushButton("Button 2 tab 1")
####             
####        # add this buttons to the layout
####        self.layoutControls1.addWidget(self.controlButton11, 0, 0)
####        self.layoutControls1.addWidget(self.controlButton12, 1, 0)
####                
####        # add this layout to the controls widget
####        self.controlWidget1 = QtGui.QWidget()
####        self.controlWidget1.setLayout(self.layoutControls1)
####
####        # create all the knob buttons
####        self.knobButton11 = Qwt.QwtKnob()
####        
####        self.knobButton12 = Qwt.QwtKnob()
####        self.knobButton11.setTotalAngle(270)
####
####        # add this knobs to the layout
####        
####        self.layoutControls1.addWidget(self.knobButton11, 0, 1)
####        self.layoutControls1.addWidget(self.knobButton12, 1, 1)
         
    def setControl2(self):
        # set the controls for the second tab
        
        # set a layout to clearly dispose all the buttons
        self.layoutControls2 = QtGui.QGridLayout()
        
        # create all the control buttons
        self.controlButton21 = QtGui.QPushButton("Button 1 - tab 2")
        self.controlButton22 = QtGui.QPushButton("Button 1 - tab 2")
       
        # add this buttons to the layout
        self.layoutControls2.addWidget(self.controlButton21, 0, 0)
        self.layoutControls2.addWidget(self.controlButton22, 1, 0)
               
        # add this layout to the controls widget
        self.controlWidget2 = QtGui.QWidget()
        self.controlWidget2.setLayout(self.layoutControls2)
    
    
    #
    # ORGANIZE EACH TAB ---------------------------------------------
    #

    def setScopes(self):
        
        # create tabs to host graphs
        self.setGraphTab()
        
        # create the graphs
        self.setTimeGraph()
        self.setFreqGraph()
        
        # add the graphs to the tabs
        self.timeGraphLayout = QtGui.QGridLayout()
##        self.timeGraphLayout.setSpacing(0)
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
        self.controlButton1 = Qwt.QwtKnob()
        self.controlButton1.setTotalAngle(270)
        self.controlButton2 = Qwt.QwtKnob()
        self.controlButton2.setTotalAngle(270)
        
        self.controlButton3 = Qwt.QwtKnob()
        self.controlButton3.setTotalAngle(270)
        self.controlButton4 = Qwt.QwtKnob()
        self.controlButton4.setTotalAngle(270)
##        
        self.controlPanelRightLayout.addWidget(self.controlButton1, 0, 0)
        self.controlPanelRightLayout.addWidget(self.controlButton2, 2, 0)
        self.controlPanelRightLayout.addWidget(self.controlButton3, 4, 0)
        self.controlPanelRightLayout.addWidget(self.controlButton4, 6, 0)
        
        # set  all buttons' Ranges

        
    

        # Add text under each button

        self.button1Text = Qt.QLabel("blabla1")
        self.button1Text.setAlignment(QtCore.Qt.AlignCenter)
        self.button2Text = Qt.QLabel("blabla2")
        self.button2Text.setAlignment(QtCore.Qt.AlignCenter)
        self.button3Text = Qt.QLabel("blabla3")
        self.button3Text.setAlignment(QtCore.Qt.AlignCenter)
        self.button4Text = Qt.QLabel("blabla4")
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
        
        
##        # define the layout use to dispose the text above the Filters checkbox
##        self.checkboxAntiNoiseLayout = QtGui.QGridLayout()
##        self.checkboxLPLayout = QtGui.QGridLayout()
##        self.checkboxHPLayout = QtGui.QGridLayout()
##        self.checkboxBPLayout = QtGui.QGridLayout()
##        self.checkboxCutLayout =QtGui.QGridLayout()

        
        # set all the controls
        self.checkboxStartRecording = QtGui.QCheckBox("",self)
        self.checkboxStartNsec = QtGui.QCheckBox("",self)
        self.checkboxStopRecording = QtGui.QCheckBox("",self)
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

<<<<<<< HEAD
##        #set Alignment to the text QLabel
=======
        #set Alignment to the text QLabel
>>>>>>> 3dd60e8578a60e92a558e9ccb513f14951fbd940
##        self.InputBoxFrequency1Text.setAlignment(QtCore.Qt.AlignRight)
##        self.InputBoxFrequency2Text.setAlignment(QtCore.Qt.AlignRight)
##        self.InputBoxThresholdText.setAlignment(QtCore.Qt.AlignRight)
##        self.InputBoxOffsetText.setAlignment(QtCore.Qt.AlignRight)
        
        
        # add all this stuff to the global interface
        self.controlPanelLeft = QWidget()
        self.controlPanelLeft.setLayout(self.controlPanelLeftLayout)
        
        self.globalInterfaceCenterLayout.addWidget(self.controlPanelLeft, 0, 0)

       #put margins around the widget
        self.controlPanelLeft.setContentsMargins( 0, 100, 0, 0)
##
##        #resize the width of the Widget
##        self.controlPanelLeft.setMaximumWidth(213)

        
    

def main(args):

    a = QApplication(args)

    f = MainFrame()

    f.setTitle("AMVU")
    
    # set the toolbar
    f.setToolBar()
    
    # set the graphical elements of the interface
##    f.resize(1400,700)
    f.setSignalInformation()
    f.setScopes()
    f.setControlPanelRight()
    f.setControlPanelLeft()
    
    #f.setGraphTab()
    #f.setScopes()
    f.show()
    r=a.exec_()

    return r

  
if __name__=="__main__":
    main(sys.argv)
#
