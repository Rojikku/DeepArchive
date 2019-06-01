#!/usr/bin/env python3
#import kivy #UI
import sqlite3 #Database
import os #Needed to chdir
import sys #Allow Arguments

#Variables
dbl = '.da/db.sqlite' #Database Location
tbln = 'core' #Table name
idc='FileName' #Identifying Column
scan_exceptions = ['.da', 'db.sqlite'] #Files to ignore when scanning

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
#Check if directory passed as argument
if len(sys.argv) > 1:
    dir = sys.argv[1] #Directory in use
else:
    print("Please specify a Directory")
    exit()
#Go to relevant  directory
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
