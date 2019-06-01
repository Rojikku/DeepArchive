#!/usr/bin/env python3
#import kivy #UI
import sqlite3 #Database
import os #Needed to chdir
#Variables
dbl = '.da/db.sqlite' #Database Location
tbln = 'core' #Table name

#Go to relevant  directory
#Must add direcotry selecting functionality
os.chdir('C:\\Users\\Rojikku\\Documents\\Library\\PDF')

#def Scan(): #Function for scanning

def Initialize(): #Function to create database foundations
    c.execute('CREATE TABLE {tn} ({nf} {ft})'\
        .format(tn=tbln, nf='Name', ft='TEXT'))
    conn.commit() #Save


exists = os.path.isfile(dbl) #Check if DB exists
if exists: #Connect if so
    conn = sqlite3.connect(dbl)
    c = conn.cursor()
else: #Create and initialize if not
    os.mkdir('.da')
    conn = sqlite3.connect(dbl)
    c = conn.cursor()
    Initialize()

conn.close() #Close connection
