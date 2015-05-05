
#-*-coding: utf-8 -*-
from PyQt4 import QtGui
from PyQt4.QtGui import QMainWindow,QWidget,QAction,QTabWidget,QApplication
from PyQt4 import Qt
from PyQt4 import QtCore
from PyQt4 import Qwt5 as Qwt

import os,sys
import Icons


class MainFrame(QMainWindow):

    def __init__(self):
        
        QMainWindow.__init__(self)
        
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
        self.controlButton11 = None
        self.controlButton12 = None
        
        # for tab 2
        self.controlButton21 = None
        self.controlButton22 = None
        
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
        btnSave.setCheckable(True)
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
        btnHelp.setCheckable(True)
        btnHelp.setToolButtonStyle(Qt.Qt.ToolButtonTextUnderIcon)
        toolBar.addWidget(btnHelp)
##        self.connect(btnQuit,QtCore.SIGNAL('clicked()'),QtCore.SLOT('close()')
       
##        

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
    
#    def setControl1(self):
#        # set the controls for the first tab
#        
#        # set a layout to clearly dispose all the buttons
#        self.layoutControls1 = QtGui.QGridLayout()
#        
#        # create all the control buttons
#        self.controlButton11 = QtGui.QPushButton("Button 1 - tab 1")
#        self.controlButton12 = QtGui.QPushButton("Button 2 - tab 1")
#        
#        # add this buttons to the layout
#        self.layoutControls1.addWidget(self.controlButton11, 0, 0)
#        self.layoutControls1.addWidget(self.controlButton12, 1, 0)
#        
#        # add this layout to the controls widget
#        self.controlWidget1 = QtGui.QWidget()
#        self.controlWidget1.setLayout(self.layoutControls1)
#
#        # create all the knob buttons
#        self.knobButton11 = Qwt.QwtKnob()
#        
#        self.knobButton12 = Qwt.QwtKnob()
#        self.knobButton11.setTotalAngle(270)
#
#        # add this knobs to the layout
#        
#        self.layoutControls1.addWidget(self.knobButton11, 0, 1)
#        self.layoutControls1.addWidget(self.knobButton12, 1, 1)
         
#    def setControl2(self):
#        # set the controls for the second tab
#        
#        # set a layout to clearly dispose all the buttons
#        self.layoutControls2 = QtGui.QGridLayout()
#        
#        # create all the control buttons
#        self.controlButton21 = QtGui.QPushButton("Button 1 - tab 2")
#        self.controlButton22 = QtGui.QPushButton("Button 1 - tab 2")
#        
#        # add this buttons to the layout
#        self.layoutControls2.addWidget(self.controlButton21, 0, 0)
#        self.layoutControls2.addWidget(self.controlButton22, 1, 0)
#        
#        # add this layout to the controls widget
#        self.controlWidget2 = QtGui.QWidget()
#        self.controlWidget2.setLayout(self.layoutControls2)
    
    
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
        self.freqGraphLayout = QtGui.QGridLayout()
        
        self.timeGraphLayout.addWidget(self.timeGraph, 0, 0)
        self.freqGraphLayout.addWidget(self.freqGraph, 0, 0)
        
        self.timeGraphTab.setLayout(self.timeGraphLayout)
        self.freqGraphTab.setLayout(self.freqGraphLayout)

    def setSignalInformation(self):
        
        # create a label to display information
        self.informationLabel = QtGui.QLabel("Signal information : bla bla bla")
        
        # add this label to the global interface
        self.signalInformationLayout = QtGui.QGridLayout()
        self.signalInformationLayout.addWidget(self.informationLabel, 0, 0)
        
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
        
        self.controlPanelRightLayout.addWidget(self.controlButton1, 0, 0)
        self.controlPanelRightLayout.addWidget(self.controlButton2, 1, 0)
        
        # add all this stuff to the global interface
        self.controlPanelRight = QWidget()
        self.controlPanelRight.setLayout(self.controlPanelRightLayout)
        
        self.globalInterfaceRightLayout.addWidget(self.controlPanelRight, 0, 0)
        
    def setControlPanelLeft(self):
        
        # define the layout use to dispose the controls
        self.controlPanelLeftLayout = QtGui.QGridLayout()
        
        # set all the controls and add them to the layout
        self.controlButton3 = QtGui.QPushButton("Button 1")
        self.controlButton4 = QtGui.QPushButton("Button 2")
        
        self.controlPanelLeftLayout.addWidget(self.controlButton3, 0, 0)
        self.controlPanelLeftLayout.addWidget(self.controlButton4, 1, 0)
        
        # add all this stuff to the global interface
        self.controlPanelLeft = QWidget()
        self.controlPanelLeft.setLayout(self.controlPanelLeftLayout)
        
        self.globalInterfaceCenterLayout.addWidget(self.controlPanelLeft, 0, 0)
    

def main(args):

    a = QApplication(args)

    f = MainFrame()
##    f.SetMenu()
    f.setTitle("AMVU")
    
    # set the toolbar
    f.setToolBar()
    
    # set the graphical elements of the interface
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
