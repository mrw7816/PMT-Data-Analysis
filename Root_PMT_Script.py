# -*- coding: utf-8 -*-
"""
Created on Mon Jul  8 15:22:41 2019

@author: Michael
"""
import ROOT as r
import sys
if len(sys.argv) != 3:
    print " USAGE : %s <input file > <output file >" %(sys.argv [0])
    sys.exit (1) #this if statement assures that you get three input params
inFileName = sys.argv [1] #assigns variable names to input and output files
outFileName = sys.argv [2]
print " Reading from ", inFileName , "and writing to", outFileName

inFile = r.TFile.Open ( inFileName ," READ ") #open the TFile
Graph_DarkPlot = inFile.Get("dark_plot;1 ") #point it to which tree I want 
print(Graph_DarkPlot)
DarkPlot_canvas = r.TCanvas('Dark_Canvas')
Graph_DarkPlot.Draw()
DarkPlot_canvas.SaveAs('Dark_Count_Long')

#These three lines grap the x and y arrays and their errors from the root file
DarkX_buff = Graph_DarkPlot.GetX()
DarkY_buff = Graph_DarkPlot.GetY()
Yerror_buff = Graph_DarkPlot.GetEY()
# These two lines provide the pythonization of the buffers into actual doubles
DarkX_buff.SetSize(Graph_DarkPlot.GetN())
DarkY_buff.SetSize(Graph_DarkPlot.GetN())
Yerror_buff.SetSize(Graph_DarkPlot.GetN())
#These two create the actual arrays
DarkX = ar.array('d' ,DarkX_buff)
DarkY = ar.array('d' ,DarkY_buff)
DarkYerror = ar.array('d', Yerror_buff)


plt.errorbar(DarkX,DarkY,yerr=DarkYerror)
plt.show()
#points = r.TH1D("dark rate", "Dark Count Rate", 0,100)

#for entryNum in range(0,tree.GetEntries()):  #fills histo
    #tree.GetEntry(entryNum)
    #points.Fill()

#points.SetDirectory(0) #makes sure hist doesnt close if input files is closed
#inFile.Close() #close input file

#outHistFile = r.TFile.Open(outFileName, "RECREATE")
#outHistFile.cd()
