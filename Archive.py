#!/usr/bin/env python3
import sqlite3 #Database
import os #Needed to chdir
import sys #Allow Arguments
import argparse as arg #Better Arguments
import logging as log #For logging verbosity options
from PyQt5.QtWidgets import QApplication, QWidget, QDesktopWidget, QMainWindow, QAction, qApp, QLabel, QFileDialog, QGridLayout, \
QPushButton, QStackedWidget
from PyQt5.QtGui import QIcon

#Load Arguments
parser = arg.ArgumentParser(
    description='The Deep Archive Utility'
)
parser.add_argument(
    "-d", "--debug",
    help="Print full debug output",
    action="store_const", dest="loglevel", const=log.DEBUG,
    default=log.WARNING,
)
parser.add_argument(
    "-v", "--verbose",
    help="Increase Verbosity",
    action="store_const", dest="loglevel", const=log.INFO,
)
args = parser.parse_args()
log.basicConfig(format='%(levelname)s: %(message)s', level=args.loglevel)

#Variables
dbfolder = '.da' #Name of Database Folder
dbfilename = 'db.sqlite' #Name of Database File
dbl = dbfolder + '/' + dbfilename #Database Location - Relative Path
tbln = 'core' #Table name
idc='FileName' #Identifying Column
scan_exceptions = ['.da', 'db.sqlite'] #Files to ignore when scanning
db_status = 0 #Current DB Status

#Functions Section
def Close(): #In case I add to it later
    conn.commit() #Save
    conn.close() #Close connection
    log.info("Saved and closed!")

def Insert(Val): #Add New Entires To Database
    for x in Val:
        print("Adding {fn} to database".format(fn=x))
        c.execute("INSERT INTO {tn} ({col}) VALUES ('{val}')"\
            .format(tn=tbln, col=idc, val=x))

def Scan(): #Function for scanning
    files = [] #Init Array for names
    for filename in os.listdir(dir):
        if filename in scan_exceptions: #Skip adding exceptions to the database
            continue
        files.append(filename) #Add filename to array
    return files #Return Array of all file names

def Initialize(): #Function to create database foundations
    global db_status
    if db_status == 1:
        Close()
    os.chdir(dir) #Go to relevant  directory
    log.info("Initializing...")
    exists = os.path.isfile(dbl) #Check if DB exists
    if not exists: #If it doesn't exist
        log.info("New Location: Initializing Database!")
        os.mkdir(dbfolder) #Make DB folder
    global conn, c #Make DB connection global
    conn = sqlite3.connect(dbl)
    c = conn.cursor()
    db_status = 1
    if not exists: #After Database Establishment, create table and populate
        c.execute('CREATE TABLE {tn} ({nf} text, Name text, Description text, Icon text, Tags text)'\
            .format(tn=tbln, nf=idc)) #Create Table and Identifying Column
        Insert(Scan()) #Initial Population
        conn.commit() #Save
    log.info("Done!")

def Search(type, req): #Search function, with type and request
    res = []
    log.debug("Doing a " + type + " search for: " + req)
    if type == "single": #If only searching for one column
        for row in c.execute('SELECT {fld} FROM {tn} ORDER BY {ord}'.format(tn=tbln, ord=idc, fld=req)):
            res.append(row[0])
    log.debug(res)
    return res


#UI Functions
class DAUI(QMainWindow):
    def __init__(self):
        super().__init__() #Load Parent's Init

        self.initUI()


    def initUI(self):
        #Settings
        self.setGeometry(300, 300, 300, 220)
        self.center()
        self.setWindowTitle("Deep Archive: The File Library Manager")

        #Menu Bar
        menu = self.menuBar()
        fileMenu = menu.addMenu('&File')

        #File Menu
        #Exit
        exitAct = QAction(QIcon('exit.png'), '&Exit', self)
        exitAct.setShortcut('Ctrl+Q')
        exitAct.setStatusTip('Exit application')
        exitAct.triggered.connect(qApp.quit)
        #Open library
        openLibrary = QAction(QIcon('open.png'), '&Open Library...', self)
        openLibrary.setShortcut('Ctrl+O')
        openLibrary.setStatusTip('Open A Library')
        openLibrary.triggered.connect(self.browseLib)
        #Organization
        fileMenu.addAction(openLibrary)
        fileMenu.addAction(exitAct)


        #Core
        #Files
        self.central_widget = QStackedWidget()
        self.setCentralWidget(self.central_widget)
        FUI = FileUI()
        self.central_widget.addWidget(FUI)

        self.show()

    def browseLib(self): #Select Library Location
        # Allow user to select a directory and store it in global var
        # called dir
        global dir
        dir = str(QFileDialog.getExistingDirectory(self, "Select Directory"))
        self.setWindowTitle(dir + " - Deep Archive")
        print(dir)
        Initialize()
        FileUI.populate(self)

    def center(self): #Function to center window
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

class FileUI(QWidget): #Widget for main window pane
    def __init__(self):
        super().__init__() #Load Parent's Init

        self.initUI() #Load UI

    def initUI(self):
        global grid #Make layout available to populate
        grid = QGridLayout()
        self.setLayout(grid)

    def populate(self):
        global conn, c, grid, idc #Load DB and Layout
        fileNames = Search("single", idc) #Search by identifying column
        positions = [(i,j) for i in range(10) for j in range(4)]
        for position, name in zip(positions, fileNames):
            button = QPushButton(name)
            grid.addWidget(button, *position)

#Init
app = QApplication(sys.argv)
ui = DAUI()
sys.exit(app.exec_()) #Load UI

#End
if db_status == 1:
    Close() #Clean Exit
