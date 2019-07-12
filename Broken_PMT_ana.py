# -*- coding: utf-8 -*-
"""
Created on Thu Jul 11 16:33:49 2019

@author: Michael
"""

import ROOT as r
import sys
import array as ar
import matplotlib.pyplot as plt

if len(sys.argv) != 3:
    print " USAGE : %s <input file > <output file >" %(sys.argv [0])
    sys.exit (1) #this if statement assures that you get three input params
inFileName = sys.argv [1] #assigns variable names to input and output files
outFileName = sys.argv [2]
print " Reading from ", inFileName , "and writing to", outFileName

inFile = r.TFile.Open ( inFileName ," READ ") #open the TFile

Ttree = inFile.Get("event") #grabs the tree
win_charge = r.TH1D("Window Charge","Charge, counts",10,6000)

for entryNum in range (0 , Ttree.GetEntries()):
    Ttree.GetEntry(entryNum)
    Charge = getattr(Ttree,"fWindowCharge_pC")
    win_charge.Fill(Charge)

win_charge.SetDirectory(0)
inFile.Close()
