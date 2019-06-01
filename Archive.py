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

#Functions Section
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
    exists = os.path.isfile(dbl) #Check if DB exists
    if not exists: #If it doesn't exist
        print("New Location: Initializing Database!")
        os.mkdir(dbfolder) #Make DB folder
    global conn, c #Make DB connection global
    conn = sqlite3.connect(dbl)
    c = conn.cursor()
    if not exists: #After Database Establishment, create table and populate
        c.execute('CREATE TABLE {tn} ({nf} text, Name text, Description text, icon text, tags text)'\
            .format(tn=tbln, nf=idc)) #Create Table and Identifying Column
        Insert(Scan()) #Initial Population
        conn.commit() #Save

#UI Functions
class DAUI:
    def __init__(self, master):
        self.master = master
        master.title("Deep Archive: The File Library Manager")

        global Lbl1
        Lbl1 = StringVar()
        Lbl1.set("Please select library directory!")
        self.label = Label(master, textvariable=Lbl1)
        # self.label.grid(row=0, column=1)
        self.label.pack()

        self.browse_button = Button(master, text="Browse", command=self.browse_buttonFn)
        # self.browse_button.grid(row=2, column=1)
        self.browse_button.pack()

        self.close_button = Button(master, text="Close", command=master.quit)
        self.close_button.pack()


    def browse_buttonFn(self):
        # Allow user to select a directory and store it in global var
        # called dir
        global dir
        filename = filedialog.askdirectory()
        Lbl1.set(filename)
        dir = str(filename)
        print(dir)



#Init
root = Tk()
ui = DAUI(root)
root.mainloop()

#Go to relevant  directory
os.chdir(dir)

Initialize()

#Main

#Ends
conn.commit()
conn.close() #Close connection
