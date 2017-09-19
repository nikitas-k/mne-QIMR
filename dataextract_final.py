# -*- coding: utf-8 -*-
import re
import numpy as np
import matplotlib.pyplot as plt

#NB, SET INFILE DIRECTORY TO FILE TO BE ANALYSED
#IF 'VALUE ERROR IS RETURNED, CHECK ARRAY SIZES FOR LINE 90

infile = raw_input(r"Input file directory: ")

#r"C:\Users\User\Documents\eeg_localiser\eeg\data\1_loc_v1_2017_Sep_04_1119.log"
#SET DIRECTORY OF LOG FILE 

important = []
# FOR FIRST SEARCH, ONLY KEEP STIM TIMES AND KEYS
keep_phrases = ["text_4: text = 'M'",
                "text_4: text = 'W'"]

# FOR SECOND SEARCH, ONLY KEEP RESPONSE TIMES AND KEYS
keep_phrases2 = ["Keypress"]


file = open("stim.csv","w") # open stim.csv for writing (will store stim times and keys)

#begin search of log file for stim times and keys
with open(infile) as f:
    f = f.readlines()

for line in f:
    for phrase in keep_phrases:
        if phrase in line: 
            line=re.split('\s+',line) #converts to .csv
            line=str(line)
            file.write(line + "\n") #writes lines when found
            break

file.close()


file = open("resp.csv","w") #open resp.csv for writing (will store resp times and keys)
with open(infile) as f:
    f = f.readlines()

#begin search of log file for resp times and keys
for line in f:
    for phrase in keep_phrases2:
        if phrase in line: 
            line=re.split('\s+',line) # removing these 2 lines will result in 
            line=str(line)              # data split by space , rather than ','
            file.write(line + "\n")
            break

file.close()

# THE FOLLOWING SECTION GRABS REQUIRED LINES FROM CSV FILES AND CREATES THEIR OWN VARIABLES 
# (stimes, skeys, rtimes, rkeys)

import csv

with open('stim.csv') as csvfile:
    readCSV = csv.reader(csvfile, delimiter=',')
    stimes = []
    skeys = []
    for column in readCSV:
        stime = column[0]
        skey = column[5]

        stimes.append(stime)
        skeys.append(skey)
    
import csv

with open('resp.csv') as csvfile:
    readCSV = csv.reader(csvfile, delimiter=',')
    rtimes = []
    rkeys=[]
    for column in readCSV:
        rtime = column[0]
        rkey = column[3]

        rtimes.append(rtime)
        rkeys.append(rkey)

    #next step is to merge appropriate variables into a single array
    
    responses=np.column_stack((rtimes, rkeys))
    stimuli=np.column_stack((stimes, skeys)) #are these 2 arrays the same length? if not, why? 
                                            # I pressed a button twice! :/
    
    responsestrim=responses[2:172] #regardless, need to trim off space bar at start - this is not ideal as its 
    # not autonomous, perhaps could modify the phrases to be more specific
    alldata=np.column_stack((stimuli, responsestrim))
    
    alldata=np.char.replace (alldata, '\'', ' ') #these three lines search for ', " and [                                              
    alldata=np.char.replace (alldata, '"', ' ')  #and remove them from the alldata array 
    alldata=np.char.replace (alldata, '[', ' ')
    
    
    #---------------------------------Create PLots ----------------------------#

    a = np.array(alldata[:,0], dtype=float)
    b = np.array(alldata[:,2], dtype=float)
    resp=[]
    resp=b-a
    plt.plot(a[:], resp[:])
    plt.ylabel('response time (s)')
    plt.xlabel('time (s)')
    plt.title('Rsponse times as a function of trial progression')
    
    print alldata
    
    
    
    

