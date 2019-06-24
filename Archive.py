#!/usr/bin/env python3
import sqlite3 #Database
import os #Needed to chdir
import sys #Allow Arguments
from tkinter import filedialog #Select Folders
from tkinter import * #UI

#Variables
dbfolder = '.da' #Name of Database Folder
dbfilename = 'db.sqlite' #Name of Database File
dbl = dbfolder + '/' + dbfilename #Database Location - Relative Path
tbln = 'core' #Table name
idc='FileName' #Identifying Column
scan_exceptions = ['.da', 'db.sqlite'] #Files to ignore when scanning
db_status = 0 #Current DB Status
conn = None #Set a default
c = None #Set a default

#Functions Section
def Close(): #In case I add to it later
    conn.commit() #Save
    conn.close() #Close connection

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
    print("Initializing...")
    exists = os.path.isfile(dbl) #Check if DB exists
    if not exists: #If it doesn't exist
        print("New Location: Initializing Database!")
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
    print("Done!")

#UI Functions
class DAUI(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)
        self.master = master

        #Settings
        self.master = master
        master.title("Deep Archive: The File Library Manager")

        #Menu Bar
        # creating a menu instance
        menu = Menu(self.master)
        self.master.config(menu=menu)

        # Declare File Menu
        file = Menu(menu)
        file.add_command(label="Open Library", command=self.browseLib)
        file.add_command(label="Exit", command=master.quit)

        # create the file object)
        edit = Menu(menu)
        edit.add_command(label="Undo")

        #Add Entries to Menu Bar
        menu.add_cascade(label="File", menu=file)
        menu.add_cascade(label="Edit", menu=edit)

        #String Data
        global Lbl1
        Lbl1 = StringVar()
        Lbl1.set("Please select library directory!")
        self.label = Label(master, textvariable=Lbl1)
        self.label.grid(row=0, column=2, padx=(10, 10), pady=(10, 10))


        self.center()

    def populate(self): #Function for adding menu entries from Database
        global conn, c
        files=[]
        buttonList=[]
        for row in c.execute('SELECT * FROM {tn} ORDER BY {ord}'.format(tn=tbln, ord=idc)):
            files.append(row)
            for i in range(len(files)):
                name = files[i][0]
                print("File loaded from DB: " + name)
                newButton = Button(root, text=name, command = lambda j=name: openFile(j))
                buttonList.append(newButton)
        for i,x in enumerate(buttonList):
            x.grid(row=2, column=i, padx=(10, 10), pady=(10, 10))


    def browseLib(self): #Select Library Location
        # Allow user to select a directory and store it in global var
        # called dir
        global dir
        filename = filedialog.askdirectory(parent=root, title="Please Select Library Folder:")
        Lbl1.set(filename)
        dir = str(filename)
        print(dir)
        Initialize()
        self.populate()

    def center(self): #Function to center window
        # Gets the requested values of the height and widht.
        windowWidth = root.winfo_reqwidth()
        windowHeight = root.winfo_reqheight()
        print("Width",windowWidth,"Height",windowHeight)

        # Gets both half the screen width/height and window width/height
        positionRight = int(root.winfo_screenwidth()/2 - windowWidth/2)
        positionDown = int(root.winfo_screenheight()/2 - windowHeight/2)

        # Positions the window in the center of the page.
        root.geometry("+{}+{}".format(positionRight, positionDown))
        root.geometry("400x300") #I'd like a less ugly default window size


#Init
root = Tk()
ui = DAUI(root)

#Main
root.mainloop()

#End
if db_status == 1:
    Close() #Clean Exit
