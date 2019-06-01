#!/usr/bin/env python3
import sqlite3 #Database
import os #Needed to chdir
import sys #Allow Arguments
# from tkinter import filedialog #Select Folders
# from tkinter import * #UI

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
def browse_button():
    # Allow user to select a directory and store it in global var
    # called dir
    global dir
    filename = filedialog.askdirectory()
    dir.set(filename)
    print(filename)



#Init
#Check if directory passed as argument
if len(sys.argv) > 1:
    dir = sys.argv[1] #Directory in use

# root = Tk()
# dir = StringVar()
# lbl1 = Label(master=root,textvariable=folder_path)
# lbl1.grid(row=0, column=1)
# button2 = Button(text="Browse", command=browse_button)
# button2.grid(row=0, column=3)
#
# mainloop()

#Go to relevant  directory
os.chdir(dir)

Initialize()

#Main

#Ends
conn.commit()
conn.close() #Close connection
