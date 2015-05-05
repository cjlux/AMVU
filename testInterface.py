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
        self.tab1 = None
        self.tab2 = None
        
        # control buttons
        self.stack      = None
        self.btnPause   = None
        self.grid       = None
        
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
        self.graph1 = None
        self.graph2 = None

        
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
        
        CentralArea = QWidget()
        self.setCentralWidget(CentralArea)


    def setTitle(self, titre="") :
        self.setWindowTitle(titre)

    def tab(self):
        self.tab1 = QWidget() # création objet Widget pour recevoir onglet
        self.tab2 = QWidget()

        self.stack = QTabWidget(self) #mettre le self?
        
        self.stack.addTab(self.tab1,"Time")
        self.stack.addTab(self.tab2,"Freq")
        
        self.setCentralWidget(self.stack)

    def toolBar(self):

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

        

    
##    def Scope (self):
##
##        
##        # grid tab1
##        babar=Qwt.QwtPlot(self.tab1)
##        babar.replot()
##        self.grid = Qwt.QwtPlotGrid()
##        self.grid.enableXMin(True)
##        self.grid.setMajPen(Qt.QPen(Qt.Qt.blue, 0, Qt.Qt.SolidLine))
##        self.grid.attach(babar)
##
##        # grid tab2
##        babar=Qwt.QwtPlot(self.tab2)
##        babar.replot()
##        self.grid = Qwt.QwtPlotGrid()
##        self.grid.enableXMin(True)
##        self.grid.setMajPen(Qt.QPen(Qt.Qt.blue, 0, Qt.Qt.SolidLine))
##        self.grid.attach(babar)

##
##      
##        # axes
##
##               
##        self.enableAxis(Qwt.QwtPlot.yRight);
##        self.setAxisTitle(Qwt.QwtPlot.xBottom, 'Time [s]');
##        self.setAxisTitle(Qwt.QwtPlot.yLeft,  'Amplitude Chan. 1 [V]');
##        self.setAxisTitle(Qwt.QwtPlot.yRight, 'Amplitude Chan. 2 [V]');
##        self.setAxisMaxMajor(Qwt.QwtPlot.xBottom, 10);
##        self.setAxisMaxMinor(Qwt.QwtPlot.xBottom, 0);
##
##        self.setAxisScaleEngine(Qwt.QwtPlot.yRight, Qwt.QwtLinearScaleEngine());
##        self.setAxisMaxMajor(Qwt.QwtPlot.yLeft, 10);
##        self.setAxisMaxMinor(Qwt.QwtPlot.yLeft, 0);
##        self.setAxisMaxMajor(Qwt.QwtPlot.yRight, 10);
##        self.setAxisMaxMinor(Qwt.QwtPlot.yRight, 0);        
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
        
    def setGraph1(self):
        # set the graph for the first tab
        # In this example, the graph is just a Qlabel
        # This is where the link with others class will be
        
        self.graph1 = QtGui.QLabel("Graphe 1")
        
        # add the graph to the interface using a layout
        self.layoutGraph1 = QtGui.QGridLayout()
        self.layoutGraph1.addWidget(self.graph1, 0, 0)
        self.graphWidget1 = QtGui.QWidget()
        self.graphWidget1.setLayout(self.layoutGraph1)
    
    def setGraph2(self):
        # set the graph for the second tab
        # In this example, the graph is just a Qlabel
        # This is where the link with others class will be
        
        # create the graph
        self.graph2 = QtGui.QLabel("Graphe 2")
        
        # add the graph to the interface using a layout
        self.layoutGraph2 = QtGui.QGridLayout()
        self.layoutGraph2.addWidget(self.graph2, 0, 0)
        self.graphWidget2 = QtGui.QWidget()
        self.graphWidget2.setLayout(self.layoutGraph2)

    #
    # SET THE BUTTONS FOR EACH TAB ---------------------------------------
    #
    # This buttons are currently QPushButton objects.
    # They can be knob, radio button, ... It only depends on the class used.
    # This buttons aren't linked to an action for the moment : if someone
    # click on them, nothing happen (except a nuclear explosion in some far away
    # countries, but nevermind... ).
    #
    
    def setControl1(self):
        # set the controls for the first tab
        
        # set a layout to clearly dispose all the buttons
        self.layoutControls1 = QtGui.QGridLayout()
        
        # create all the control buttons
        self.controlButton11 = QtGui.QPushButton("Button 1 - tab 1")
        self.controlButton12 = QtGui.QPushButton("Button 2 - tab 1")
        
        # add this buttons to the layout
        self.layoutControls1.addWidget(self.controlButton11, 0, 0)
        self.layoutControls1.addWidget(self.controlButton12, 1, 0)
        
        # add this layout to the controls widget
        self.controlWidget1 = QtGui.QWidget()
        self.controlWidget1.setLayout(self.layoutControls1)

        # create all the knob buttons
        self.knobButton11 = LogKnob()
        self.knobButton12 = LblKnob(self.controlWidget1,1,1,'name')

        # add this knobs to the layout
        
        self.layoutControls1.addWidget(self.knobButton11, 0, 0)
        
        self.layoutControls1.addWidget(self.knobButton12, 1, 0)
        
        
        
        

        
    
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
        
# Create a layout for each tab
        self.layoutTab1 = QtGui.QGridLayout()
        self.layoutTab2 = QtGui.QGridLayout()
        
# Instanciate the controls and the graph from each scope
        self.setGraph1()
        self.setGraph2()
        
        self.setControl1()
        self.setControl2()
        
# Insert into this layouts the widget for the graph
# and the widget for the control
        self.layoutTab1.addWidget(self.graphWidget1, 0, 0)
        self.layoutTab1.addWidget(self.controlWidget1, 0, 1)
        
        self.layoutTab2.addWidget(self.graphWidget2, 0, 0)
        self.layoutTab2.addWidget(self.controlWidget2, 0, 1)
        
# Add the layout to the corresponding tab
        self.tab1.setLayout(self.layoutTab1)
        self.tab2.setLayout(self.layoutTab2)
        
        self.stack.show() # don't know if really usefull
        

def main(args):

    a = QApplication(args)

    f = MainFrame()
##    f.SetMenu()
    f.setTitle("AMVU")
    f.tab()
    f.toolBar()
    f.setScopes()
    f.show()
    r=a.exec_()

    return r

  
if __name__=="__main__":
    main(sys.argv)
