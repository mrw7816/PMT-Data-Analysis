# -*- coding: utf-8 -*-
"""
Created on Thu Jul 11 16:33:49 2019

@author: Michael
"""

import ROOT as r
import sys
import array as ar
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
if len(sys.argv) != 4:
    print " USAGE : %s <analysis type> <input file > <output file > <if analysis is Stability add last files>" %(sys.argv [0])
    sys.exit (1) #this if statement assures that you get three input params
Analysis_Type = sys.argv[1]
inFileName = sys.argv [2] #assigns variable names to input and output files
outFileName = sys.argv [3]
print " Reading from ", inFileName , "and writing to", outFileName
"""
inFile = r.TFile.Open ( inFileName ," READ ") #open the TFile

Ttree = inFile.Get("event") #grabs the tree
win_charge = r.TH1F("Window Charge","Window Charge of KA0181",100,-2,10)
pulse = r.TH1F("Pulse Charge","Pulse Charge of KA0181",100,0,40)
pulseheight = r.TH1F("Pulse Height", "Pulse Height of KA0181",100,0,2)
pulsewidth = r.TH1F("Pulse Width", "Pulse Width of KA0181",100,0,100)
h2w = r.TH1F("1D Height to Width", "Height to width of KA0181",100,0,1)
charge_height = r.TH2F("Charge to Height","Charge to Height Ratio of KA0181",100,-1,10,100,-1,6000)
height_width = r.TH2F("Height to Width vs Height","Height to Width Ratio vs Height of KA0181",100,0,0.01,100,0,0.001)

for entryNum in range (0 , Ttree.GetEntries()):
    Ttree.GetEntry(entryNum)
    WCharge = getattr(Ttree,"fWindowCharge_pC")
    Pulse = getattr(Ttree,"fPulseCharge_pC")
    Charge = getattr(Ttree,"fCharge_pC")
    Height = getattr(Ttree,"fPulseHeight_V")
    Npul = getattr(Ttree,"nPulses")
    RightE = getattr(Ttree,"fPulseRightEdge")
    LeftE = getattr(Ttree,"fPulseLeftEdge")
    Pulse.SetSize(Npul)
    Height.SetSize(Npul)
    RightE.SetSize(Npul)
    LeftE.SetSize(Npul)
    Pulse_Width = np.subtract(RightE,LeftE)
    win_charge.Fill(WCharge)
    for ipul in range(0,Npul-1):
        ch_to_ht = Pulse[ipul]/Height[ipul]
        charge_height.Fill(Pulse[ipul], ch_to_ht)
        pulse.Fill(Pulse[ipul])
        pulseheight.Fill(Height[ipul])
        pulsewidth.Fill(Pulse_Width[ipul])
        ht_to_wd = Height[ipul]/Pulse_Width[ipul]
        h2w.Fill(ht_to_wd)
        height_width.Fill(Height[ipul], ht_to_wd)

win_charge.SetXTitle("Charge_pC")
pulse.SetXTitle("Charge_pC")
charge_height.SetXTitle("Charge")
charge_height.SetYTitle("Charge/Height")
height_width.SetXTitle("Height")
height_width.SetYTitle("Height/Width")
win_charge.Scale(1.0/win_charge.Integral())
charge_height.Scale(1.0/charge_height.Integral())

win_charge.SetDirectory(0)
pulse.SetDirectory(0)
charge_height.SetDirectory(0)
height_width.SetDirectory(0)
pulsewidth.SetDirectory(0)
pulseheight.SetDirectory(0)
h2w.SetDirectory(0)
inFile.Close()

outHistFile = r.TFile.Open(outFileName, "RECREATE")
outHistFile.cd()
win_charge.Write()
pulse.Write()
charge_height.Write()
height_width.Write()
pulsewidth.Write()
pulseheight.Write()
h2w.Write()
outHistFile.Close()

if Analysis_Type == "Afterpulsing":
    inFile = r.TFile.Open ( inFileName ," READ ")
    Ttree = inFile.Get("event")
    After_Pulse = r.TH2F("Time vs Charge", "Time to Charge for KA0181",1000,0,14,1000,0,1200)
    for entryNum in range (0 , Ttree.GetEntries()):
        Ttree.GetEntry(entryNum)
        WCharge = getattr(Ttree,"fWindowCharge_pC")
        Time = getattr(Ttree,"fCalibratedTime")
        Pulse = getattr(Ttree,"fPulseCharge_pC")
        Npul = getattr(Ttree,"nPulses")
        Time.SetSize(Npul)
        Pulse.SetSize(Npul)
        for ipul in range(0,Npul-1):
            if Pulse > float(0.8):
                After_Pulse.Fill(WCharge,Time[ipul],Pulse[ipul])

    After_Pulse.SetXTitle("Charge_pC")
    After_Pulse.SetYTitle("Time/Charge")
    After_Pulse.Scale(1.0/After_Pulse.Integral())
    After_Pulse.SetDirectory(0)
    inFile.Close()
    outHistFile = r.TFile.Open(outFileName, "UPDATE")
    outHistFile.cd()
    After_Pulse.Write()
    outHistFile.Close()
"""
if Analysis_Type == "Stability":
    inFile = r.TFile.Open ( inFileName ," READ ")
    pcharge = r.TH1F("Pulse Charge","Pulse Charge",100,0,40)
    Ttree = inFile.Get("event")
    av_pulse = []
    av_height = []
    av_width = []
    pulse = 0
    height = 0
    width = 0
    count = 0
    for entryNum in range (0 , Ttree.GetEntries()):
        Ttree.GetEntry(entryNum)
        Npul = getattr(Ttree,"nPulses")
        Pulse = getattr(Ttree,"fPulseCharge_pC")
        Height = getattr(Ttree,"fPulseHeight_V")
        RightE = getattr(Ttree,"fPulseRightEdge")
        LeftE = getattr(Ttree,"fPulseLeftEdge")
        Time = getattr(Ttree,"fCalibratedTime")
        Pulse.SetSize(Npul)
        Height.SetSize(Npul)
        RightE.SetSize(Npul)
        LeftE.SetSize(Npul)
        Time.SetSize(Npul)
        Pulse_Width1 = np.subtract(RightE,LeftE)
	for ipul in range(0,Npul-1):
            if 18 < Time[ipul] <45:
	        pulse += Pulse[ipul]
           	height += Height[ipul]
           	width += Pulse_Width1[ipul]
           	count += 1
           	pcharge.Fill(Pulse[ipul])
        if entryNum != 0  and entryNum % 10000 == 0:
            avp = pulse / count
            av_pulse.append(avp)
            avh = height / count
            av_height.append(avh)
            avw = width / count
            av_width.append(avw)
            pulse = 0
            height = 0
            width = 0
            count = 0

    x = ar.array('d',np.linspace(0,300,num=300))
    pulsearray = ar.array('d',av_pulse)
    average_charge = r.TGraph(len(x),x,pulsearray)
    average_charge.SetTitle("Average Pulse Charge over Measurment")
    average_charge.SetMarkerColor(2)
    average_charge.SetMarkerStyle(20)
    average_charge.SetMarkerSize(0.7)

    heightarray = ar.array('d',av_height)
    average_height = r.TGraph(len(x),x,heightarray)
    average_height.SetTitle("Average Pulse Height over Measurment")
    average_height.SetMarkerColor(2)
    average_height.SetMarkerStyle(20)
    average_height.SetMarkerSize(0.7)

    widtharray = ar.array('d',av_width)
    average_width = r.TGraph(len(x),x,widtharray)
    average_width.SetTitle("Average Pulse Width over Measurment")
    average_width.SetMarkerColor(2)
    average_height.SetMarkerStyle(20)
    average_height.SetMarkerSize(0.7)

    pcharge.SetDirectory(0)
    inFile.Close()

    outHistFile = r.TFile.Open(outFileName, "UPDATE")
    outHistFile.cd()
    pcharge.Write()
    average_charge.Write()
    average_height.Write()
    average_width.Write()
    outHistFile.Close()
