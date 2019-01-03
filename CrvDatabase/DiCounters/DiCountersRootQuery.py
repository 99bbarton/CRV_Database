# -*- coding: utf-8 -*-
##
##  File = "DiCountersRootQuery.py"
##  Deived from File = "DiCountersRootQuery2017Jul14.py"
##  Derived from File = "guiDiCounters.py"
##  Derived from File = "guiDiCounters_2017July11.py"
##
##  python script to read the dicounter test information from 
##  the database and place results in root tree.
##  This version uses PyROOT... to uses it setup
##  root with PyRoot or set up the mu2e runtime enviroment.
##
##  cmj 2017Jul29.....
##  The PyROOT examples save everything in a set of lists which
##  look like one branch in the root macro file for root... The lists
##  appear as arrays in the root file (used by root... i.e.
##  >root 
##  .x rootfile.C
##  I haven't figured out how to get to the string arrays in the
##  root macro file.
##  So, I don't use the normal PyROOT examples, and I have to 
## locally change string list into character arrays to be passed onto
## the root tree!!!!  The resulting tree is like the one used by
## root macros and NOT by PyROOT!  See the root  macro file 
## "outfiles/analyzeDicounters.C" to use this root tree!
##
##   Merrill Jenkins
##   Department of Physics
##   University of South Alabama
##   2015Sep23
##
#!/bin/env python
##
##
##
##
sendDataBase = 0  ## zero... don't send to database
#
from Tkinter import *         # get widget class
import Tkinter as tk
import tkFileDialog
import os
import sys        ## 
import optparse   ## parser module... to parse the command line arguments
import math
from collections import defaultdict
from time import *

#import ssl		## new for new version of DataLoader
#import random		## new for new version of Dat##  File = "DiCounters_2017Mar13.py"aLoader
sys.path.append("../../Utilities/Dataloader.zip")
sys.path.append("../CrvUtilities/crvUtilities2017.zip")
from DataLoader import *   ## module to read/write to database....
from databaseConfig import *
#from generalUtilities import generalUtilities
from cmjGuiLibGrid2017Jun23 import *
from DiCounters import *
##  Import for PyRoot
from ROOT import TCanvas, TFile, TProfile, TNtuple, TH1F, TH2F, TGraph, TStyle, TTree, TString, TDirectory
from ROOT import gROOT, gBenchmark, gRandom, gSystem, Double, string, vector
from array import array
ProgramName = "DiCountersRootQuerry.py"
Version = "version2017.06.19"
##
##
## -------------------------------------------------------------
## 	A class to interogate the di-counters in the database
##	then product the root tree in the root file!
##
class askDiCounter(object):
  def __init__(self):
    self.__cmjProgramFlow = 0
    if(self.__cmjProgramFlow != 0): print("askDiCounter__init__askDiCounter... enter \n")
    self.__cmjPlotDiag = 0
    self.__database_config  = databaseConfig()
##  This information is stored such that we need nested dictionaries......
##
    self.__diCounterSipmLocation = {'A1':'A1','A2':'A2','A3':'A3','A4':'A4','B1':'B1','B2':'B2','B3':'B3','B4':'B4'}
    self.__diCounterSipms = ['A1','A2','A3','A4','B1','B2','B3','B4']
    self.__nestedDirectory = generalUtilities()
    self.__diCounterCurrent = self.__nestedDirectory.nestedDict()		## A nested dictionary to hold a dictionary that holds the
								## current measured for the Sipm at some location on the di-counter
								## the keys are [di-counter][[diCounterTestDate][diCounterSipmLocation]
    self.__diCounterDate = defaultdict(dict)			## Nested dictionary to hold the date of the tests (keys: [diCounterId][diCounterTestDate])
    self.__diCounterLightSource = defaultdict(dict)		## Nested dictionary to hold the test light result (keys: [diCounterId][diCounterTestDate])	
    self.__diCounterFlashRate = defaultdict(dict)		## Nested dictionary to hold the test light source flash rate (keys: [diCounterId][diCounterTestDate])
    self.__diCounterVoltage = defaultdict(dict)			## Nested dictionary to hold the voltage on the Sipm (keys: [diCounterId][diCounterTestDate])
    self.__diCounterTemperature = defaultdict(dict)		## Nested ictionary to hold the temperature the measurement is made (keys: [diCounterId][diCounterTestDate]))
    self.__diCounterLightSourceVector = defaultdict(dict)	## Nested dictionary to hold the side the measurement is made (keys: [diCounterId][diCounterTestDate]))
    self.__diCounterLightSourceDistance = defaultdict(dict)	## Nested dictionary to hold the distance from source measurement is made (keys: [diCounterId][diCounterTestDate]))
    self.__diCounterComment = defaultdict(dict)			## Nested dictionary to hold the comments on the test (keys: [diCounterId][diCounterTestDate])
##  for the root tree...
    ## arrays needed to build root tree....
    self.__signalDiCounterId = {}
    self.__signalTestDate = {}
    self.__signalFlashRate = {}
    self.__signalPosition = {}
    self.__signalTemperature = {}
    self.__signalVoltage = {}
    self.__signalLightSource = {}
    self.__currentA1 = {}; self.__currentA2 = {}; self.__currentA3 = {}; self.__currentA4 = {}
    self.__currentB1 = {}; self.__currentB2 = {}; self.__currentB3 = {}; self.__currentB4 = {}
    self.__numberOfDark = 0
##
    self.__darkCurrentId = {}
    self.__darkCurrentTestDate = {}
    self.__darkCurrentTemperature = {}   
    self.__darkCurrentVoltage = {}
    self.__darkCurrentA1 = {}; self.__darkCurrentA2 = {}; self.__darkCurrentA3 = {}; self.__darkCurrentA4 = {}
    self.__darkCurrentB1 = {}; self.__darkCurrentB2 = {}; self.__darkCurrentB3 = {}; self.__darkCurrentB4 = {}
## -------------------------------------------------------------
  def __del__(self):
    if(self.__cmjProgramFlow != 0) : print("askDiCounter__del__askDiCounter... enter \n") 
## -------------------------------------------------------------
  def turnOnDebug(self,temp):
    self.__cmjPlotDiag = temp
    print("askDiCounter__turnOnDebug... debug level =  %s \n") % (self.__cmjPlotDiag)
## -------------------------------------------------------------
##	Make queries to data base
##	Set up queries to the development database
  def setupDevelopmentDatabase(self):
    self.__database = 'mu2e_hardware_dev'
    self.__group = "Composite Tables"
    self.__whichDatabase = 'development'
    if(self.__cmjPlotDiag != 0): print("...askDiCounter::getFromDevelopmentDatabase... get to development database \n")
    self.__queryUrl = self.__database_config.getQueryUrl()
    if(self.__cmjPlotDiag > 2) : 
      print("...askDiCounter::getFromDevelopmentDatabase... self.__database = %s \n") % (self.__database)
      print("...askDiCounter::getFromDevelopmentDatabase... self._queryUrl = %s \n") %(self.__queryUrl)
## -------------------------------------------------------------
##	Make queries to the database
##	Setup queries to the production database
  def setupProductionDatabase(self):
    self.__database = 'mu2e_hardware_dev'
    self.__group = "Composite Tables"
    self.__whichDatabase = 'production'
    if(self.__cmjPlotDiag != 0): print("...askDiCounter::getFromProductionDatabase... get to production database \n")
    self.__queryUrl = self.__database_config.getProductionQueryUrl()
    if(self.__cmjPlotDiag > 2) : 
      print("...askDiCounter::getFromProductionDatabase... self.__database = %s \n") % (self.__database)
      print("...askDiCounter::getFromProductionDatabase... self._queryUrl = %s \n") %(self.__queryUrl)
## -------------------------------------------------------------
##  Ask the database for the di-counter information here!
  def loadDiCounterRequest(self):
    if(self.__cmjProgramFlow != 0): print("...askDiCounter::loadDiCounterRequest... enter \n")
    self.__tempResults = self.getDiCounterFromDatabase()
## -------------------------------------------------------------
  def getDiCounterFromDatabase(self):
    if(self.__cmjProgramFlow != 0): print("...askDiCounter::getDiCounterFromDatabase... enter \n")
    self.__getDiCounterValues = DataQuery(self.__queryUrl)
    self.__diCounterResults = []
    self.__table = "di_counter_tests"
    self.__fetchThese = "di_counter_id,test_date,sipm_location,current_amps,light_source,flash_rate_hz,temperature,distance,sipm_test_voltage"
    self.__fetchCondition = "test_date:gt:2017-01-01 00:00"
    self.__numberReturned = 0
    self.__diCounterResults = self.__getDiCounterValues.query(self.__database,self.__table,self.__fetchThese,self.__fetchCondition,'-'+self.__fetchThese)
    if(self.__cmjPlotDiag > 4): print ("...askDiCounter::getDiCounterFromDatabase... self.__diCounterResults = %s \n") % (self.__diCounterResults)
    if(self.__cmjPlotDiag > 5):
      for self.__l in self.__diCounterResults:
	print self.__l
    return self.__diCounterResults
 
## -------------------------------------------------------------
  def getScatterPlots(self):
    if(self.__cmjProgramFlow != 0): print("...askDiCounter::getScatterPlots... enter \n")
    self.plotScatterPlots(self)
## -------------------------------------------------------------
  def getHistograms(self):
    if(self.__cmjProgramFlow != 0): print("...askDiCounter::getHistograms... enter \n")
    self.bookHistograms()     
    self.fillHistograms(self.__diCounterResults)
    self.drawCanvas()
    self.defineTree()
## -------------------------------------------------------------
  def plotScatterPlots(self):
    if(self.__cmjProgramFlow != 0): print("...askDiCounter::plotScatterPlots... enter \n")
## -------------------------------------------------------------
  def bookHistograms(self):
    if(self.__cmjProgramFlow != 0): print("...askDiCounter::bookHistograms... enter \n")
    self.__nBins = 100
    self.__lowBin = 0.0
    self.__hiBin = 2.0
    ##  Signal
    self.__hSipmA1 = TH1F("self.__hSipmA1","Sipm Current A1",self.__nBins,self.__lowBin,self.__hiBin)
    self.__hSipmA2 = TH1F("self.__hSipmA2","Sipm Current A2",self.__nBins,self.__lowBin,self.__hiBin)
    self.__hSipmA3 = TH1F("self.__hSipmA3","Sipm Current A3",self.__nBins,self.__lowBin,self.__hiBin)
    self.__hSipmA4 = TH1F("self.__hSipmA4","Sipm Current A4",self.__nBins,self.__lowBin,self.__hiBin)
    self.__hSipmB1 = TH1F("self.__hSipmB1","Sipm Current B1",self.__nBins,self.__lowBin,self.__hiBin)
    self.__hSipmB2 = TH1F("self.__hSipmB2","Sipm Current B2",self.__nBins,self.__lowBin,self.__hiBin)
    self.__hSipmB3 = TH1F("self.__hSipmB3","Sipm Current B3",self.__nBins,self.__lowBin,self.__hiBin)
    self.__hSipmB4 = TH1F("self.__hSipmB4","Sipm Current B4",self.__nBins,self.__lowBin,self.__hiBin)
    ## Dark
    self.__hSipmDarkA1 = TH1F("self.__hSipmDarkA1","Sipm Dark Current A1",self.__nBins,self.__lowBin,self.__hiBin)
    self.__hSipmDarkA2 = TH1F("self.__hSipmDarkA2","Sipm Dark Current A2",self.__nBins,self.__lowBin,self.__hiBin)
    self.__hSipmDarkA3 = TH1F("self.__hSipmDarkA3","Sipm Dark Current A3",self.__nBins,self.__lowBin,self.__hiBin)
    self.__hSipmDarkA4 = TH1F("self.__hSipmDarkA4","Sipm Dark Current A4",self.__nBins,self.__lowBin,self.__hiBin)
    self.__hSipmDarkB1 = TH1F("self.__hSipmDarkB1","Sipm Dark Current B1",self.__nBins,self.__lowBin,self.__hiBin)
    self.__hSipmDarkB2 = TH1F("self.__hSipmDarkB2","Sipm Dark Current B2",self.__nBins,self.__lowBin,self.__hiBin)
    self.__hSipmDarkB3 = TH1F("self.__hSipmDarkB3","Sipm Dark Current B3",self.__nBins,self.__lowBin,self.__hiBin)
    self.__hSipmDarkB4 = TH1F("self.__hSipmDarkB4","Sipm Dark Current B4",self.__nBins,self.__lowBin,self.__hiBin)
## -------------------------------------------------------------
  def fillHistograms(self,tempResults):
    if(self.__cmjProgramFlow != 0): print("...askDiCounter::fillHistograms... enter \n")
    self.__numberOfSignal  = 0
    self.__numberOfDark = 0
    for diCounterTest in tempResults:
      if(diCounterTest != ""):
	self.__temp = []
	self.__temp = diCounterTest.rsplit(",",9)
	self.__Id = self.__temp[0]
	self.__Date = self.__temp[1]
	self.__SipmPosition = self.__temp[2]
	self.__LightSource = self.__temp[4]
	self.__FlashRate = self.__temp[5]
	self.__Temperature = self.__temp[6]
	self.__LightPosition = self.__temp[7]
	self.__SipmVoltage = self.__temp[8]
	if(self.__LightSource == 'rad'):
	  if(self.__SipmPosition == 'a1'): 		## Assume that all 8 Sipm posistions are reported..
							## fill common measurements once with a1
	    self.__hSipmA1.Fill(float(self.__temp[3]))
	    self.__currentA1[self.__Id] = float(self.__temp[3])
	    self.__signalDiCounterId[self.__Id] = str(self.__Id)
	    self.__signalTestDate[self.__Id] = str(self.__Date)
	    self.__signalFlashRate[self.__Id] = str(self.__FlashRate)
	    self.__signalLightSource[self.__Id] = str(self.__LightSource)
	    self.__signalPosition[self.__Id] = float(self.__LightPosition)
	    self.__signalTemperature[self.__Id] = float(self.__Temperature)
	    self.__signalVoltage[self.__Id] = float(self.__SipmVoltage)
	    self.__numberOfSignal += 1  ## assume that all Sipm positions have an entry in the database
	  if(self.__SipmPosition == 'a2'): 
	    self.__hSipmA2.Fill(float(self.__temp[3]))
	    self.__currentA2[self.__Id] = float(self.__temp[3])
	  if(self.__SipmPosition == 'a3'): 
	    self.__hSipmA3.Fill(float(self.__temp[3]))
	    self.__currentA3[self.__Id] = float(self.__temp[3])
	  if(self.__SipmPosition == 'a4'): 
	    self.__hSipmA4.Fill(float(self.__temp[3]))
	    self.__currentA4[self.__Id] = float(self.__temp[3])
	  if(self.__SipmPosition == 'b1'): 
	    self.__hSipmB1.Fill(float(self.__temp[3]))
	    self.__currentB1[self.__Id] = float(self.__temp[3])
	  if(self.__SipmPosition == 'b2'): 
	    self.__hSipmB2.Fill(float(self.__temp[3]))
	    self.__currentB2[self.__Id] = float(self.__temp[3])
	  if(self.__SipmPosition == 'b3'): 
	    self.__hSipmB3.Fill(float(self.__temp[3]))
	    self.__currentB3[self.__Id] = float(self.__temp[3])
	  if(self.__SipmPosition == 'b4'): 
	    self.__hSipmB4.Fill(float(self.__temp[3]))
	    self.__currentB4[self.__Id] = float(self.__temp[3])
	if(self.__LightSource == 'dark'):
	  if(self.__SipmPosition == 'a1'): 
	    self.__hSipmDarkA1.Fill(float(self.__temp[3]))
	    self.__darkCurrentA1[self.__Id] = (float(self.__temp[3]))
	    self.__darkCurrentId[self.__Id] = str(self.__Id)
	    self.__darkCurrentTestDate[self.__Id] = str(self.__Date)
	    self.__darkCurrentTemperature[self.__Id] = float(self.__Temperature)
	    self.__darkCurrentVoltage[self.__Id]  = float(self.__SipmVoltage)        
	  if(self.__SipmPosition == 'a2'): 
	    self.__hSipmDarkA2.Fill(float(self.__temp[3]))
	    self.__darkCurrentA2[self.__Id] = float(self.__temp[3])
	  if(self.__SipmPosition == 'a3'): 
	    self.__hSipmDarkA3.Fill(float(self.__temp[3]))
	    self.__darkCurrentA3[self.__Id] = float(self.__temp[3])
	  if(self.__SipmPosition == 'a4'): 
	    self.__hSipmDarkA4.Fill(float(self.__temp[3]))
	    self.__darkCurrentA4[self.__Id] = float(self.__temp[3])
	  if(self.__SipmPosition == 'b1'): 
	    self.__hSipmDarkB1.Fill(float(self.__temp[3]))
	    self.__darkCurrentB1[self.__Id] = float(self.__temp[3])
	  if(self.__SipmPosition == 'b2'): 
	    self.__hSipmDarkB2.Fill(float(self.__temp[3]))
	    self.__darkCurrentB2[self.__Id] = float(self.__temp[3])
	  if(self.__SipmPosition == 'b3'): 
	    self.__hSipmDarkB3.Fill(float(self.__temp[3]))
	    self.__darkCurrentB3[self.__Id] = float(self.__temp[3])
	  if(self.__SipmPosition == 'b4'): 
	    self.__hSipmDarkB4.Fill(float(self.__temp[3]))
	    self.__darkCurrentB4[self.__Id] = float(self.__temp[3])
## -------------------------------------------------------------
  def drawCanvas(self):
    if(self.__cmjProgramFlow != 0): print("...askDiCounter::drawCanvas... enter \n")
    self.__cX = 200
    self.__cY = 10
    self.__cWidth = 700	## canvas width
    self.__cHeight = 500	## canvas height
    self.__delX = 20
    self.__delY = 20
    self.__windowTitle = "DiCounter Sipm Current Results"
    self.__c1 = TCanvas('self.__c1',self.__windowTitle,self.__cX,self.__cY,self.__cWidth,self.__cHeight)  
    self.__c1.Divide(4,2)  ## split canvas into pads....
    self.__c1.cd(1)
    self.__hSipmA1.Draw()
    self.__c1.cd(2)
    self.__hSipmA2.Draw()
    self.__c1.cd(3)
    self.__hSipmA3.Draw()
    self.__c1.cd(4)
    self.__hSipmA4.Draw()
    self.__c1.cd(5)
    self.__hSipmB1.Draw()
    self.__c1.cd(6)
    self.__hSipmB2.Draw()
    self.__c1.cd(7)
    self.__hSipmB3.Draw()
    self.__c1.cd(8)
    self.__hSipmB4.Draw()
    #
    self.__cX += self.__delX
    self.__cY += self.__delY
    self.__windowTitle = "DiCounter Sipm DarkCurrent Results"
    self.__c2 = TCanvas('self.__c2',self.__windowTitle,self.__cX,self.__cY,self.__cWidth,self.__cHeight)  
    self.__c2.Divide(4,2)  ## split canvas into pads....
    self.__c2.cd(1)
    self.__hSipmDarkA1.Draw()
    self.__c2.cd(2)
    self.__hSipmDarkA2.Draw()
    self.__c2.cd(3)
    self.__hSipmDarkA3.Draw()
    self.__c2.cd(4)
    self.__hSipmDarkA4.Draw()
    self.__c2.cd(5)
    self.__hSipmDarkB1.Draw()
    self.__c2.cd(6)
    self.__hSipmDarkB2.Draw()
    self.__c2.cd(7)
    self.__hSipmDarkB3.Draw()
    self.__c2.cd(8)
    self.__hSipmDarkB4.Draw()
    ## save graphics
    print("save graphics \n")
    self.__graphicsTime = myTime()
    self.__graphicsTime.getComputerTime()
    self.__saveGraphicsTime = self.__graphicsTime.getTimeForSavedFiles()
    self.__outputGraphicsDirectory = "outputFiles/graphics/"
    self.__c1.SaveAs(self.__outputGraphicsDirectory+"signal_"+self.__saveGraphicsTime+".png")
    self.__c2.SaveAs(self.__outputGraphicsDirectory+"darkCurrent"+self.__saveGraphicsTime+".png")

## -------------------------------------------------------------
##	This method defines the root tree and
##	the file that it is saved on.
##  The root tree has two directories... one for the signal and 
##  one for the dark current readings...  The tree contains information
##  to allow the user to select sides that the source was positioned
##  di-counter id and the test dates.
##
  def defineTree(self):
    if(self.__cmjProgramFlow != 0): print("...askDiCounter::defineTree... enter \n")
    ## Define the root tree output file
    self.__treeTime = myTime()
    self.__treeTime.getComputerTime()
    self.__saveTreeTime = self.__treeTime.getTimeForSavedFiles()
    self.__outRootTreeFileName = "outputFiles/DiCounters"+self.__saveTreeTime+".root"
    self.__rootTreeFile = TFile(self.__outRootTreeFileName,'RECREATE')
    ## place the signal in one directory
    self.__rootTreeFile.mkdir('DiCounterSignal')
    self.__rootTreeFile.cd('DiCounterSignal')
    self.__localRootTree1 = TTree('diCounterSignal','root tree with ntuples')
    ## define arrays for the signal...
    if(self.__cmjPlotDiag > 2): print("...askDiCounter::defineTree... define arrays \n")
    self.__tempDiCounterId = bytearray(21)  ## the di-counter Id
    self.__tempTestDate = bytearray(30)
    self.__tempLightSource=bytearray(20)
    self.__tempFlashRate = bytearray(30)
    self.__arrayCurrentA1 = array('f',[0])
    self.__arrayCurrentA2 = array('f',[0])
    self.__arrayCurrentA3 = array('f',[0])
    self.__arrayCurrentA4 = array('f',[0])
    self.__arrayCurrentB1 = array('f',[0])
    self.__arrayCurrentB2 = array('f',[0])
    self.__arrayCurrentB3 = array('f',[0])
    self.__arrayCurrentB4 = array('f',[0])
    self.__arraySignalTemperature = array('f',[0])
    self.__arraySignalPosition = array('f',[0])
    self.__arraySignalVoltage = array('f',[0])
    ## define branches....  for the signal
    if(self.__cmjPlotDiag > 2): print("...askDiCounter::defineTree... define branches \n")
    self.__localRootTree1.Branch('diCounterId',self.__tempDiCounterId,'self.__tempDiCounterId[21]/C')
    self.__localRootTree1.Branch('testDate',self.__tempTestDate,'self.__tempTestDate[30]/C')
    self.__localRootTree1.Branch('lightSource',self.__tempLightSource,'self.__tempLightSource[20]/C')
    self.__localRootTree1.Branch('flashRate',self.__tempFlashRate,'self.__tempFlashRate[30]/C')
    self.__localRootTree1.Branch('currentA1',self.__arrayCurrentA1,'self.__arrayCurrentA1[1]/F')
    self.__localRootTree1.Branch('currentA2',self.__arrayCurrentA2,'self.__arrayCurrentA2[1]/F')
    self.__localRootTree1.Branch('currentA3',self.__arrayCurrentA3,'self.__arrayCurrentA3[1]/F')
    self.__localRootTree1.Branch('currentA4',self.__arrayCurrentA4,'self.__arrayCurrentA4[1]/F')
    self.__localRootTree1.Branch('currentB1',self.__arrayCurrentB1,'self.__arrayCurrentB1[1]/F')
    self.__localRootTree1.Branch('currentB2',self.__arrayCurrentB2,'self.__arrayCurrentB2[1]/F')
    self.__localRootTree1.Branch('currentB3',self.__arrayCurrentB3,'self.__arrayCurrentB3[1]/F')
    self.__localRootTree1.Branch('currentB4',self.__arrayCurrentB4,'self.__arrayCurrentB4[1]/F')
    self.__localRootTree1.Branch('temperature',self.__arraySignalTemperature,'self.__arraySignalTemperature[1]/F')
    self.__localRootTree1.Branch('position',self.__arraySignalPosition,'self.__arraySignalPosition[1]/F')
    self.__localRootTree1.Branch('sipmVoltage',self.__arraySignalVoltage,'self.__arraySignalVoltage[1]/F')
    for counter in self.__signalDiCounterId.keys():
      self.__arrayCurrentA1[0] = self.__currentA1[counter]
      self.__arrayCurrentA2[0] = self.__currentA2[counter]
      self.__arrayCurrentA3[0] = self.__currentA3[counter]
      self.__arrayCurrentA4[0] = self.__currentA4[counter]
      self.__arrayCurrentB1[0] = self.__currentB1[counter]
      self.__arrayCurrentB2[0] = self.__currentB2[counter]
      self.__arrayCurrentB3[0] = self.__currentB3[counter]
      self.__arrayCurrentB4[0] = self.__currentB4[counter]
      self.__arraySignalTemperature[0] = self.__signalVoltage[counter]
      self.__arraySignalPosition[0] = self.__signalPosition[counter]
      self.__arraySignalVoltage[0] = self.__signalVoltage[counter]
      if(self.__cmjPlotDiag > 2): print("self.__currentA1[%s] = %s, %s, %s, %s, %s, %s, %s, %s ") % (counter,self.__currentA1[counter],self.__currentA2[counter],self.__currentA3[counter],self.__currentA4[counter],self.__currentB1[counter],self.__currentB2[counter],self.__currentB3[counter],self.__currentB4[counter])
##	There has to be a better way to do this...
##	But amaziningly, there is now easy way to take a 
##	string and convert it into a character!...
##	And the Root trees need a character array to 
##	be read by a root macro later!
      m = 0
      for self.__character in self.__signalDiCounterId[counter]:
	self.__tempDiCounterId[m] = self.__character
	m += 1
      m = 0
      for self.__character in self.__signalTestDate[counter]:
	self.__tempTestDate[m] = self.__character
	m += 1
      m = 0
      for self.__character in self.__signalFlashRate[counter]:
	self.__tempFlashRate[m] = self.__character
	m += 1
      m = 0
      for self.__character in self.__signalLightSource[counter]:
	self.__tempLightSource[m] = self.__character
	m += 1
      self.__localRootTree1.Fill()  ### fill for everay entry... not at once as a list....
##
    if(self.__cmjPlotDiag > 1) : 
      print("...askDiCounter::defineTree... self.__localRootTree1.Scan() \n")
      self.__localRootTree1.Scan("diCounterId:currentA1:currentA2:currentA3:currentA4:currentB1:currentB2:currentB3:currentB4:testDate:temperature:position:sipmVoltage:lightSource:flashRate","","precision=4")   ## use for debug... let's see what is in the root tree...
    ## place the dark current in another  directory, in another tree!
    self.__rootTreeFile.mkdir('DiCounterDarkCurrent')
    self.__rootTreeFile.cd('DiCounterDarkCurrent')
    self.__localRootTree2 = TTree('diCounterDarkCurrent','root tree with ntuples')
    self.__tempDarkCurrentId = bytearray(21)  ## the di-counter Id
    self.__tempDarkCurrentTestDate = bytearray(30)
    self.__arrayDarkCurrentA1 = array('f',[0])
    self.__arrayDarkCurrentA2 = array('f',[0])
    self.__arrayDarkCurrentA3 = array('f',[0])
    self.__arrayDarkCurrentA4 = array('f',[0])
    self.__arrayDarkCurrentB1 = array('f',[0])
    self.__arrayDarkCurrentB2 = array('f',[0])
    self.__arrayDarkCurrentB3 = array('f',[0])
    self.__arrayDarkCurrentB4 = array('f',[0]) 
    self.__arrayDarkCurrentTemperature = array('f',[0])
    self.__arrayDarkCurrentVoltage = array('f',[0])                                                                                                                                      
#    ## define branches....  for the dark current readings
    self.__localRootTree1.Branch('diCounterId',self.__tempDarkCurrentId,'self.__tempDarkCurrenId[21]/C')
    self.__localRootTree1.Branch('testDate',self.__tempDarkCurrentTestDate,'self.__tempDarkCurrentTestDate[30]/C')
    self.__localRootTree2.Branch('darkCurrentA1',self.__arrayDarkCurrentA1,'self.__arrayDarkCurrentA1[1]/F')
    self.__localRootTree2.Branch('darkCurrentA2',self.__arrayDarkCurrentA2,'self.__arrayDarkCurrentA2[1]/F')
    self.__localRootTree2.Branch('darkCurrentA3',self.__arrayDarkCurrentA3,'self.__arrayDarkCurrentA3[1]/F')
    self.__localRootTree2.Branch('darkCurrentA4',self.__arrayDarkCurrentA4,'self.__arrayDarkCurrentA4[1]/F')
    self.__localRootTree2.Branch('darkCurrentB1',self.__arrayDarkCurrentB1,'self.__arrayDarkCurrentB1[1]/F')
    self.__localRootTree2.Branch('darkCurrentB2',self.__arrayDarkCurrentB2,'self.__arrayDarkCurrentB2[1]/F')
    self.__localRootTree2.Branch('darkCurrentB3',self.__arrayDarkCurrentB3,'self.__arrayDarkCurrentB3[1]/F')
    self.__localRootTree2.Branch('darkCurrentB4',self.__arrayDarkCurrentB4,'self.__arrayDarkCurrentB4[1]/F')
    self.__localRootTree2.Branch('temperature',self.__arrayDarkCurrentTemperature,'self.__arrayDarkCurrentTemperature[1]/F')
    self.__localRootTree2.Branch('sipmVoltage',self.__arrayDarkCurrentVoltage,'self.__arrayDarkCurrentVoltage[1]/F')
    for self.__counter in self.__darkCurrentId.keys():
      self.__arrayDarkCurrentA1[0] = self.__darkCurrentA1[self.__counter]
      self.__arrayDarkCurrentA2[0] = self.__darkCurrentA2[self.__counter]
      self.__arrayDarkCurrentA3[0] = self.__darkCurrentA3[self.__counter]
      self.__arrayDarkCurrentA4[0] = self.__darkCurrentA4[self.__counter]
      self.__arrayDarkCurrentB1[0] = self.__darkCurrentB1[self.__counter]
      self.__arrayDarkCurrentB2[0] = self.__darkCurrentB2[self.__counter]
      self.__arrayDarkCurrentB3[0] = self.__darkCurrentB3[self.__counter]
      self.__arrayDarkCurrentB4[0] = self.__darkCurrentB4[self.__counter]
      self.__arrayDarkCurrentTemperature[0] = self.__darkCurrentTemperature[self.__counter]
      self.__arrayDarkCurrentVoltage[0] = self.__darkCurrentVoltage[self.__counter]
      if(self.__cmjPlotDiag > 2): print("self.__darkCurrentA1[%s] = %s, %s, %s, %s, %s, %s, %s, %s ") % (self.__counter,self.__darkCurrentA1[self.__counter],self.__darkCurrentA2[self.__counter],self.__darkCurrentA3[self.__counter],self.__darkCurrentA4[self.__counter],self.__darkCurrentB1[self.__counter],self.__darkCurrentB2[self.__counter],self.__darkCurrentB3[self.__counter],self.__darkCurrentB4[self.__counter])
      m = 0
      for self.__character in self.__darkCurrentId[counter]:
	self.__tempDarkCurrentId[m] = self.__character
	m += 1
      m = 0
      for self.__character in self.__darkCurrentTestDate[self.__counter]:
	self.__tempDarkCurrentTestDate[m] = self.__character
	m += 1
      self.__localRootTree2.Fill()
    if(self.__cmjPlotDiag > 1) : 
      print("...askDiCounter::defineTree... self.__localRootTree2.Scan() \n")
      self.__localRootTree2.Scan("diCounterId:darkCurrentA1:darkCurrentA2:darkCurrentA3:darkCurrentA4:darkCurrentB1:darkCurrentB2:darkCurrentB3:darkCurrentB4:testDate:temperature:sipmVoltage","","precision=4")   ## use for debug... let's see what is in the root tree...
##	Write the root tree to the root file and close it!!!!
    self.__rootTreeFile.Write()
    self.__rootTreeFile.Close()

##
##
## -------------------------------------------------------------
## 	A class to set up the main window to drive the
##	python GUI
##
class multiWindow(Frame):
  def __init__(self,parent=NONE, myRow = 0, myCol = 0):
    Frame.__init__(self,parent)
    self.__myDiCounters  = askDiCounter()
    self.__myDiCounters.setupDevelopmentDatabase()  ## set up communications with database
    self.__labelWidth = 25
    self.__entryWidth = 20
    self.__buttonWidth = 5
    self.__maxRow = 2
##	Dictionary of arrays to hold the Sipm Batch information
    self.__sipmBatch={}
##	Define Output Log file... remove this later
    self.__mySaveIt = saveResult()
    self.__mySaveIt.setOutputFileName('sipmQuerries')
    self.__mySaveIt.openFile()
    self.__row = 0
    self.__col = 0
    self.__strName = []
    self.__sCount = 0
##
##
##	First Column...
    self.__col = 0
    self.__firstRow = 0
##
##	Instruction Box...
    self.__myInstructions = myScrolledText(self)
    self.__myInstructions.setTextBoxWidth(50)
    self.__myInstructions.makeWidgets()
    self.__myInstructions.setText('','Instructions/InstructionsForDiCountersRootQuery2017Jul14.txt')
    self.__myInstructions.grid(row=self.__firstRow,column=self.__col,columnspan=2)
    self.__firstRow += 1
##
    self.__col = 0
    self.__secondRow = 1
    self.__buttonWidth = 20
##	Send initial Sipm information: PO number, batches recieved and vendor measurements...
    self.__getValues = Button(self,text='Get Di-Counters',command=self.__myDiCounters.loadDiCounterRequest,width=self.__buttonWidth,bg='green',fg='black')
    self.__getValues.grid(row=self.__secondRow,column=self.__col,sticky=W)
    self.__secondRow += 1
    self.__getValues = Button(self,text='Histogram',command=self.__myDiCounters.getHistograms,width=self.__buttonWidth,bg='green',fg='black')
    self.__getValues.grid(row=self.__secondRow,column=self.__col,sticky=W)
    self.__secondRow += 1
###	Third Column...
    self.__row = 0
    self.__col = 2
    self.__logo = mu2eLogo(self,self.__row,self.__col)     # display Mu2e logo!
    self.__logo.grid(row=self.__row,column=self.__col,rowspan=2,sticky=NE)
##         Display the script's version number
    self.__version = myLabel(self,self.__row,self.__col)
    self.__version.setForgroundColor('blue')
    self.__version.setFontAll('Arial',10,'bold')
    self.__version.setWidth(20)
    self.__version.setText(Version)
    self.__version.makeLabel()
    self.__version.grid(row=self.__row,column=self.__col,stick=E)
    self.__row += 1
##         Display the date the script is being run
    self.__date = myDate(self,self.__row,self.__col,10)      # make entry to row... pack right
    self.__date.grid(row=self.__row,column=self.__col,sticky=E)
    self.__col = 0
    self.__row += 1
    self.__buttonWidth = 10
##	Add Control Bar at the bottom...
    self.__col = 0
    self.__firstRow = 6
    self.__quitNow = Quitter(self,0,self.__col)
    self.__quitNow.grid(row=self.__firstRow,column=0,sticky=W)
##sendMeasurements
##
## --------------------------------------------------------------------
##
##	Open up file dialog....
  def openFileDialog(self):
    self.__filePath=tkFileDialog.askopenfilename()
    print("__multiWindow__::openDialogFile = %s \n") % (self.__filePath)
    self.__myDiCounters.openFile(self.__filePath)
    self.__myDiCounters.openLogFile()
## --------------------------------------------------------------------
##
  def turnOnDebug(self,tempDebug):
    self.__myDiCounters.turnOnDebug(tempDebug)
    print("__multiWindow__::turnOnDebug = debug leve = %s") % (tempDebug)
## --------------------------------------------------------------------
## --------------------------------------------------------------------
## --------------------------------------------------------------------
## --------------------------------------------------------------------
## --------------------------------------------------------------------
## --------------------------------------------------------------------
##   Run the pyton script from here!!!
if __name__ == '__main__':
  parser = optparse.OptionParser("usage: %prog [options] file1.txt \n")
  parser.add_option('--debug',dest='debugMode',type='int',default=0,help='set debug: 0 (off - default), 1 = on')
  parser.add_option('-t',dest='testMode',type='int',default=0,help='set to test mode (do not send to database): 1')
  parser.add_option('--database',dest='database',type='string',default="development",help='development or production')
  options, args = parser.parse_args()
  print("'__main__': options.debugMode = %s \n") % (options.debugMode)
  print("'__main__': options.testMode  = %s \n") % (options.testMode)
  print("'__main__': options.database  = %s \n") % (options.database)
  root = Tk()              # or Toplevel()
  bannerText = 'Mu2e::'+ProgramName
  root.title(bannerText)  
  root.geometry("+100+500")  ## set offset of primary window....
  myMultiForm = multiWindow(root,0,0)
  if(options.debugMode != 0): myMultiForm.turnOnDebug(options.debugMode)
  myMultiForm.grid()
  root.mainloop()



