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
if len(sys.argv) != 5:
    print " USAGE : %s <analysis type> <PMT#> <input file > <output file > <if analysis is Stability add last files>" %(sys.argv [0])
    sys.exit (1) #this if statement assures that you get three input params
Analysis_Type = sys.argv[1]
PMT = sys.argv[2]
inFileName = sys.argv [3] #assigns variable names to input and output files
outFileName = sys.argv [4]
print " Reading from ", inFileName , "and writing to", outFileName

inFile = r.TFile.Open ( inFileName ," READ ") #open the TFile

Ttree = inFile.Get("event") #grabs the tree
win_charge = r.TH1F("Window Charge","Window Charge of KA0181 ",100,-2,10)
pulse = r.TH1F("Pulse Charge","Pulse Charge of KA0181",100,0,40)
pulseheight = r.TH1F("Pulse Height", "Pulse Height of KA0181",100,0,2)
pulsewidth = r.TH1F("Pulse Width", "Pulse Width of KA0181",100,0,100)
h2w = r.TH1F("1D Height to Width", "Height to width of KA0181",100,0,1)
charge_height = r.TH2F("Charge to Height","Charge to Height Ratio of KA0181",100,0,10,100,0,0.1)
charge_width = r.TH2F("Charge to Width", "Charge to Width Ratio of KA0181",100,0,10,100,0,35)
height_width = r.TH2F("Height to Width vs Height","Height to Width Ratio vs Height of KA0181",100,0,0.01,100,0,0.001)
h2w_charge = r.TH2F("Height/Width to Charge", "Height/Width vs Charge for KA0181",100,0,10,100,0,0.02)

for entryNum in range (0 , Ttree.GetEntries()):
    Ttree.GetEntry(entryNum)
    WCharge = getattr(Ttree,"fWindowCharge_pC")
    Pulse = getattr(Ttree,"fPulseCharge_pC")
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
        charge_height.Fill(Pulse[ipul], Height[ipul])
        pulse.Fill(Pulse[ipul])
        pulseheight.Fill(Height[ipul])
        pulsewidth.Fill(Pulse_Width[ipul])
        ht_to_wd = Height[ipul]/Pulse_Width[ipul]
        h2w.Fill(ht_to_wd)
        height_width.Fill(Height[ipul], ht_to_wd)
        h2w_charge.Fill(Pulse[ipul],ht_to_wd)
        charge_width.Fill(Pulse[ipul],Pulse_Width[ipul])

win_charge.SetXTitle("Charge_pC")
pulse.SetXTitle("Charge_pC")
charge_height.SetXTitle("Charge")
charge_height.SetYTitle("Pulse Height")
height_width.SetXTitle("Height")
height_width.SetYTitle("Height/Width")
h2w_charge.SetXTitle("Charge_pC")
h2w_charge.SetYTitle("Height/Width")
charge_width.SetXTitle("Charge_pC")
charge_width.SetYTitle("Pulse Width")
win_charge.Scale(1.0/win_charge.Integral())
charge_height.Scale(1.0/charge_height.Integral())
charge_width.Scale(1.0/charge_width.Integral())

win_charge.SetDirectory(0)
pulse.SetDirectory(0)
charge_height.SetDirectory(0)
height_width.SetDirectory(0)
pulsewidth.SetDirectory(0)
pulseheight.SetDirectory(0)
h2w.SetDirectory(0)
h2w_charge.SetDirectory(0)
charge_width.SetDirectory(0)
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
h2w_charge.Write()
charge_width.Write()
outHistFile.Close()

if Analysis_Type == "Afterpulsing":
    inFile = r.TFile.Open ( inFileName ," READ ")
    Ttree = inFile.Get("event")
    After_Pulse = r.TH2F("Time vs Charge", "Time to Charge for KA0181",1000,0,14,1000,0,1800)
    Ratio = r.TH1F("Absolute AP Ratio", "Afterpulse Ratio", 500,0,1800)
    Scale = 0.0
    for entryNum in range (0 , Ttree.GetEntries()):
        Ttree.GetEntry(entryNum)
        WCharge = getattr(Ttree,"fWindowCharge_pC")
        Time = getattr(Ttree,"fCalibratedTime")
        Pulse = getattr(Ttree,"fPulseCharge_pC")
        Npul = getattr(Ttree,"nPulses")
        Time.SetSize(Npul)
        Pulse.SetSize(Npul)
        if WCharge > float(0.4):
            Scale +=1.0
            weight = 1.0/WCharge
            for ipul in range(0,Npul-1):
                if Pulse > float(0.4):
                    Ratio.Fill(Time[ipul],weight)
                    After_Pulse.Fill(WCharge,Time[ipul],Pulse[ipul])

    Ratio.Scale(1/Scale)
    fitFunc = r.TF1('fitFunc','gausn',400,800)
    fitFunc2 = r.TF1('fitFunc2','gausn',825,1350)
    fitFunc3 = r.TF1('fitFunc3','gausn',1375,1800)
    fitFuncAll = r.TF1('fitFuncAll','gausn(0)+gausn(3)+gausn(6)',400,1800)
    After_Pulse.SetXTitle("Window Charge_pC")
    After_Pulse.SetYTitle("Time_ns")
    Ratio.SetXTitle("Time_ns")
    r.gStyle.SetOptFit()
    #Ratio.Fit('fitFunc','R')
    #Ratio.Fit('fitFunc2','R+')
    #Ratio.Fit('fitFunc3','R+')
    Ratio.Fit('fitFuncAll','R')
    #print "Integral of first peak = ", fitFunc.Integral(400,800)
    #print "Integral of second peak = ", fitFunc2.Integral(825,1350)
    #print "Integral of third peak = ", fitFunc3.Integral(1375,1800)
    print "Integral of All =",fitFuncAll.Integral(400,1800)

    After_Pulse.SetDirectory(0)
    Ratio.SetDirectory(0)
    inFile.Close()
    outHistFile = r.TFile.Open(outFileName, "UPDATE")
    outHistFile.cd()
    After_Pulse.Write()
    Ratio.Write()
    outHistFile.Close()

if Analysis_Type == "Stability":
    inFile = r.TFile.Open ( inFileName ," READ ")
    Sample_Window = r.TH1F("Sample Window Charge","Sample Window Charge KA0181",100,-2,10)
    pcharge = r.TH1F("Pulse Charge for Sample Window 18 - 45","Sample Pulse Charge KA0181",100,0,40)
    twoDHeight_Average = r.TH2F("2d Height","Height to File Number KA0181",300,0,300,300,0,5)
    twoDCharge_Average = r.TH2F("2d Charge","Charge to File Number KA0181",300,0,300,300,0,5)
    twoDWidth_Average = r.TH2F("2d Width","Width to File Number KA0181",100,0,0.01,100,0,0.001)
    Ttree = inFile.Get("event")
    av_pulse = []
    av_pulseSTD = []
    av_height = []
    av_heightSTD = []
    av_width = []
    av_widthSTD = []
    PULSES = []
    HEIGHTS = []
    WIDTHS = []
    File = 0
    for entryNum in range (0 , Ttree.GetEntries()):
        Ttree.GetEntry(entryNum)
        Npul = getattr(Ttree,"nPulses")
	WCharge = getattr(Ttree, "fWindowCharge_pC")
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
		Sample_Window.Fill(WCharge)
           	pcharge.Fill(Pulse[ipul])
                PULSES.append(Pulse[ipul])
                HEIGHTS.append(Height[ipul])
                WIDTHS.append(Pulse_Width1[ipul])
        if (entryNum+1) % 10000 == 0:
            avp = sum(PULSES)/len(PULSES)
            pulse_std = np.std(PULSES)
            av_pulse.append(avp)
            av_pulseSTD.append(pulse_std)
            avh = sum(HEIGHTS)/len(HEIGHTS)
            height_std = np.std(HEIGHTS)
            av_height.append(avh)
            av_heightSTD.append(height_std)
            avw = sum(WIDTHS)/len(WIDTHS)
            width_std = np.std(WIDTHS)
            av_width.append(avw)
            av_widthSTD.append(width_std)
            PULSES = []
            HEIGHTS = []
            WIDTHS = []
	    File += 1.00
	    twoDCharge_Average.Fill(File,avp)

    x = ar.array('d',np.linspace(0,len(av_pulse),num=len(av_pulse)))
    xer = np.zeros(len(av_pulse))
    fitFunc = r.TF1('fitFunc','pol1(0)',0,300)

    pulsearray = ar.array('d',av_pulse)
    pstdarray = ar.array('d',av_pulseSTD)
    average_charge = r.TGraphErrors(len(x),x,pulsearray,xer,pstdarray)
    average_charge.SetTitle("Average Pulse Charge over Measurment KA0181")
    average_charge.SetMarkerColor(2)
    average_charge.SetMarkerStyle(20)
    average_charge.SetMarkerSize(0.7)
    r.gStyle.SetOptFit()
    average_charge.Fit('fitFunc')

    heightarray = ar.array('d',av_height)
    hstdarray = ar.array('d',av_heightSTD)
    average_height = r.TGraphErrors(len(x),x,heightarray,xer,hstdarray)
    average_height.SetTitle("Average Pulse Height over Measurment KA0181")
    average_height.SetMarkerColor(2)
    average_height.SetMarkerStyle(20)
    average_height.SetMarkerSize(0.7)
    average_height.Fit('fitFunc')

    widtharray = ar.array('d',av_width)
    wstdarray = ar.array('d',av_widthSTD)
    average_width = r.TGraphErrors(len(x),x,widtharray,xer,wstdarray)
    average_width.SetTitle("Average Pulse Width over Measurment KA0181")
    average_width.SetMarkerColor(2)
    average_width.SetMarkerStyle(20)
    average_width.SetMarkerSize(0.7)
    average_width.Fit('fitFunc')

    twoDCharge_Average.SetXTitle("File Number")
    twoDCharge_Average.SetYTitle("Sampled Pulse Charge pC")

    pcharge.SetDirectory(0)
    twoDCharge_Average.SetDirectory(0)
    Sample_Window.SetDirectory(0)
    inFile.Close()

    outHistFile = r.TFile.Open(outFileName, "UPDATE")
    outHistFile.cd()
    pcharge.Write()
    Sample_Window.Write()
    average_charge.Write()
    average_height.Write()
    average_width.Write()
    twoDCharge_Average.Write()
    outHistFile.Close()
