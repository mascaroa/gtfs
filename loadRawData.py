#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Load raw bus route data
This function loads a specified file and returns a dictionary of pandas
dataframes where the items are the time and GPS coordinates of one bus
running along a route.

Parameters
----------



"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def loadRawData(filename):
    # First let's load the data into numpy arrays
    dataIn = np.load(filename)
    
    # Copy it into a less shitty format (not a NpzFile class)
    newDataIn = dict(dataIn)
    
    # Timestamp at midnight on december 23rd, 2018
    t0 = 1545523200
    
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
            



