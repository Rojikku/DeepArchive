#!/usr/bin/env python3
#import kivy #UI
import sqlite3 #Database
import os #Needed to chdir
#Variables
dbl = '.da/db.sqlite' #Database Location
tbln = 'core' #Table name
idc='Name' #Identifying Column
dir = 'C:\\Users\\Rojikku\\Documents\\Library\\PDF' #Directory in use TEMPORARY
scan_exceptions = ['.da'] #Files to ignore when scanning

#Functions Section
def Insert(Col, Val):
    c.execute("INSERT INTO {tn} ({col}) VALUES ('{val}')"\
        .format(tn=tbln, col=Col, val=Val))

def Scan(): #Function for scanning
    for filename in os.listdir(dir):
        if filename in scan_exceptions: #Skip adding exceptions to the database
            continue
        print("Adding {fn} to database".format(fn=filename))
        Insert(idc, filename)

def Initialize(): #Function to create database foundations
    c.execute('CREATE TABLE {tn} ({nf} {ft})'\
        .format(tn=tbln, nf=idc, ft='TEXT'))
    conn.commit() #Save

#Init
#Go to relevant  directory
#Must add direcotry selecting functionality
os.chdir(dir)

exists = os.path.isfile(dbl) #Check if DB exists
if exists: #Connect if so
    conn = sqlite3.connect(dbl)
    c = conn.cursor()
else: #Create and initialize if not
    os.mkdir('.da') #Make DB folder
    conn = sqlite3.connect(dbl) #Create DB File
    c = conn.cursor()
    Initialize()

#Main
Scan()

#Ends
conn.commit()
conn.close() #Close connection
