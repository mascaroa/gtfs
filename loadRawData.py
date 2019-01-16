#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Load raw bus route data
This function loads a specified file and returns a dictionary of pandas
dataframes where the items are the time and GPS coordinates of one bus
running along a route.

Parameters
----------
    first : filename
        name of the .npz file to open (including extension)
    second : year
        Year when data was genereated
    third : month
        Month when data was generated
    fourth : day
        Day when data was generate

Returns
-------
    dfDict
        A dictionary containing pandas arrays with the timestamps and GPS
        data (zero-padded so they're uniform size)
        
Raises
------
    IOError
        When file not found
    
"""

import numpy as np
import pandas as pd
import time
from datetime import date


def loadRawData(filename,year,month,day):
    # First let's load the data into numpy arrays
    dataIn = np.load(filename)
    
    # Copy it into a less shitty format (not a NpzFile class)
    newDataIn = dict(dataIn)
    
    # Get the (Unix) timestamp for this day's data:
    d = date(year, month, day)
    t0 = time.mktime(d.timetuple())
    
    # Bus stop we care about (kind of...):
    # 45.538254 -73.601215
    # 0.0005
    
    
    dfDict = dict()
    
    # Zero the timestamps, save to dictionary of dataframes:
    i = 0
    for key in newDataIn.keys():
        newDataIn[key][:,0] -= t0
        dfDict[i] = pd.DataFrame(newDataIn[key],columns = ['Time','Lat','Long'])
        i += 1
    
    # Get the longest one:
    longestRun = max(len(dfDict[key]) for key in dfDict.keys())
    stDevRuns = np.std([len(dfDict[key]) for key in dfDict.keys()])
    
    dfZeroPad = pd.DataFrame([[0,0,0]],columns = ['Time','Lat','Long'])
    for key in dfDict.keys():
        if(len(dfDict[key]) < longestRun-2*stDevRuns):
            del dfDict[key] # Purge anything way out-of-whack
        elif(len(dfDict[key])<longestRun):
            for i in range(longestRun-len(dfDict[key])):
                dfDict[key] = dfDict[key].append(dfZeroPad)
    
    return dfDict
            
