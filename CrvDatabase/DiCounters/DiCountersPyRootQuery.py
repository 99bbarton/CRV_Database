# -*- coding: utf-8 -*-
##
##  File = "guiDiCounters.py"
##  Derived from File = "guiDiCounters.py"
##  Derived from File = "guiDiCounters_2017July11.py"
##
##  Test program read di-counter entries from the database and
##  produces a root tree in a root output file...
##  To run this setup the mu2e environment.
##
##   Merrill Jenkins
##   Department of Physics
##   University of South Alabama
##   2015Sep23
##
#!/bin/env python
##
##  To run this script:
##	1) Input the initial diCounter information... 
##	 python DiCounters_2016Dec27.p -i 'CounterSpreadSheets/Counter_2016May13.csv'
##	2) Input the image file for the cut
##	 python DiCounters_2016Dec27.py -i 'diCounterSpreadSheets/DiCounter_Tests_2016Dec20.csv' --mode 'image'
##	3) Input the test results
##	 python DiCounters_2016Dec27.py -i 'diCounterSpreadSheets/DiCounter_Tests_2016Dec20.csv' --mode 'measure'
##
##  Modified by cmj 2016Jan7... Add the databaseConfig class to get the URL for 
##		the various databases... change the URL in this class to change for all scripts.
##  Modified by cmj 2016Jan14 to use different directories for support modules...
##		These are located in zip files in the various subdirectories....
##  Modified by cmj2016Jan26.... change the maximum number of columns decoded to use variable.
##				change code to accomodate two hole positions										"pre_production" or "production"
##  Modified by cmj2016Jun24... Add one more upward level for subdirectory to get to the utilities directory
##  Modified by cmj2017Mar14... Add instructions for use in the call of the script.
##  Modified by cmj2017Mar14... Add test mode option; option to turn off send to database.
##  Modified by cmj2017May31... Add "di-" identifiery for di-counters.
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
Version = "version2017.06.13"
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
    ## arays needed to build root tree....
    self.__numberOfSignal = 0
    self.__signalDiCounterId = vector('string')()
    self.__signalTestDate = vector('string')()
    self.__signalFlashRate = vector('string')()
    self.__signalPosition = []
    self.__signalTemperature = []
    self.__signalVoltage = []
    self.__currentA1 = []; self.__currentA2 = []; self.__currentA3 = []; self.__currentA4 = []
    self.__currentB1 = []; self.__currentB2 = []; self.__currentB3 = []; self.__currentB4 = []
    self.__numberOfDark = 0
    self.__darkCurrentId = vector('string')()
    self.__darkCurrentTestDate = vector('string')()
    self.__darkCurrentTestDate = vector('string')()
    self.__darkCurrentlPosition = []
    self.__darkCurrentTemperature = []   
    self.__darkCurrentVoltage = []
    self.__darkCurrentA1 = []; self.__darkCurrentA2 = []; self.__darkCurrentA3 = []; self.__darkCurrentA4 = []
    self.__darkCurrentB1 = []; self.__darkCurrentB2 = []; self.__darkCurrentB3 = []; self.__darkCurrentB4 = []
## -------------------------------------------------------------
  def __del__(self):
    if(self.__cmjProgramFlow != 0) : print("askDiCounter__del__askDiCounter... enter \n") 
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
#  def unpackDiCounter(self):
#    if(self.__cmjProgramFlow != 0): print("...askDiCounter::unpackDiCounter... enter \n")
## -------------------------------------------------------------
  def plotScatterPlots(self):
    if(self.__cmjProgramFlow != 0): print("...askDiCounter::plotScatterPlots... enter \n")
### -------------------------------------------------------------
#  def plotHistograms(self):
#    if(self.__cmjProgramFlow != 0): print("...askDiCounter::plotHistograms... enter \n")
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
	    self.__currentA1.append(float(self.__temp[3]))
	    self.__signalDiCounterId.push_back(self.__Id)
	    self.__signalTestDate.push_back(self.__Date)
	    self.__signalFlashRate.push_back(self.__FlashRate)
	    self.__signalPosition.append(float(self.__LightPosition))
	    self.__signalTemperature.append(float(self.__Temperature))
	    self.__signalVoltage.append(float(self.__SipmVoltage))
	    self.__numberOfSignal += 1  ## assume that all Sipm positions have an entry in the database
	  if(self.__SipmPosition == 'a2'): 
	    self.__hSipmA2.Fill(float(self.__temp[3]))
	    self.__currentA2.append(float(self.__temp[3]))
	  if(self.__SipmPosition == 'a3'): 
	    self.__hSipmA3.Fill(float(self.__temp[3]))
	    self.__currentA3.append(float(self.__temp[3]))
	  if(self.__SipmPosition == 'a4'): 
	    self.__hSipmA4.Fill(float(self.__temp[3]))
	    self.__currentA4.append(float(self.__temp[3]))
	  if(self.__SipmPosition == 'b1'): 
	    self.__hSipmB1.Fill(float(self.__temp[3]))
	    self.__currentB1.append(float(self.__temp[3]))
	  if(self.__SipmPosition == 'b2'): 
	    self.__hSipmB2.Fill(float(self.__temp[3]))
	    self.__currentB2.append(float(self.__temp[3]))
	  if(self.__SipmPosition == 'b3'): 
	    self.__hSipmB3.Fill(float(self.__temp[3]))
	    self.__currentB3.append(float(self.__temp[3]))
	  if(self.__SipmPosition == 'b4'): 
	    self.__hSipmB4.Fill(float(self.__temp[3]))
	    self.__currentB4.append(float(self.__temp[3]))
	if(self.__LightSource == 'dark'):
	  if(self.__SipmPosition == 'a1'): 
	    self.__hSipmDarkA1.Fill(float(self.__temp[3]))
	    self.__numberOfDark += 1  ## assume all Sipm position have an entry in the database
	    self.__darkCurrentTestDate.push_back(self.__Date)
	    self.__darkCurrentId.push_back(self.__Id)   
	    self.__darkCurrentA1.append(float(self.__temp[3]))
	  if(self.__SipmPosition == 'a2'): 
	    self.__hSipmDarkA2.Fill(float(self.__temp[3]))
	    self.__darkCurrentA2.append(float(self.__temp[3]))
	  if(self.__SipmPosition == 'a3'): 
	    self.__hSipmDarkA3.Fill(float(self.__temp[3]))
	    self.__darkCurrentA3.append(float(self.__temp[3]))
	  if(self.__SipmPosition == 'a4'): 
	    self.__hSipmDarkA4.Fill(float(self.__temp[3]))
	    self.__darkCurrentA4.append(float(self.__temp[3]))
	  if(self.__SipmPosition == 'b1'): 
	    self.__hSipmDarkB1.Fill(float(self.__temp[3]))
	    self.__darkCurrentB1.append(float(self.__temp[3]))
	  if(self.__SipmPosition == 'b2'): 
	    self.__hSipmDarkB2.Fill(float(self.__temp[3]))
	    self.__darkCurrentB2.append(float(self.__temp[3]))
	  if(self.__SipmPosition == 'b3'): 
	    self.__hSipmDarkB3.Fill(float(self.__temp[3]))
	    self.__darkCurrentB3.append(float(self.__temp[3]))
	  if(self.__SipmPosition == 'b4'): 
	    self.__hSipmDarkB4.Fill(float(self.__temp[3]))
	    self.__darkCurrentB4.append(float(self.__temp[3]))
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
    self.__c1.SaveAs(self.__outputGraphicsDirectory+"signal_"+self.__saveGraphicsTime+"_py.png")
    self.__c2.SaveAs(self.__outputGraphicsDirectory+"darkCurrent"+self.__saveGraphicsTime+"_py.png")

## -------------------------------------------------------------
  def defineTree(self):
    if(self.__cmjProgramFlow != 0): print("...askDiCounter::defineTree... enter \n")
    ## Define the root tree
    ## Define the root tree output file
    self.__treeTime = myTime()
    self.__treeTime.getComputerTime()
    self.__saveTreeTime = self.__treeTime.getTimeForSavedFiles()
    self.__outRootTreeFileName = "outputFiles/DiCounters"+self.__saveTreeTime+"py.root"
    self.__rootTreeFile = TFile(self.__outRootTreeFileName,'RECREATE')
    ## place the signal in one directory
    self.__rootTreeFile.mkdir('DiCounterSignal')
    self.__rootTreeFile.cd('DiCounterSignal')
    self.__localRootTree1 = TTree('diCounterSignal','root tree with ntuples')
    ## define arrays for the signal...
    if(self.__cmjPlotDiag > 2): print("...askDiCounter::defineTree... define arrays \n")
    self.__arrayNumberOfSignalEntries = array('i',self.__numberOfSignal*[0])
    self.__arrayCurrentA1 = array('f',self.__currentA1)
    self.__arrayCurrentA2 = array('f',self.__currentA2)
    self.__arrayCurrentA3 = array('f',self.__currentA3)
    self.__arrayCurrentA4 = array('f',self.__currentA4)
    self.__arrayCurrentB1 = array('f',self.__currentB1)
    self.__arrayCurrentB2 = array('f',self.__currentB2)
    self.__arrayCurrentB3 = array('f',self.__currentB3)
    self.__arrayCurrentB4 = array('f',self.__currentB4)
    self.__arrayPosition = array('f',self.__signalPosition)
    self.__arrayTemperature = array('f',self.__signalTemperature)
    self.__arrayVoltage = array('f',self.__signalVoltage)
    if(self.__cmjPlotDiag > 2): 
      print("...askDiCounter::defineTree... self.__numberSignal = %d \n") % (self.__numberOfSignal)
      print("...askDiCounter::defineTree... self.__arrayNumberOfSignalEntries = %s \n")   % (self.__arrayNumberOfSignalEntries)
      print("...askDiCounter::defineTree... self.__arrayCurrentA1 = %s \n")   % (self.__arrayCurrentA1)
      print("...askDiCounter::defineTree... self.__arrayCurrentA2 = %s \n")   % (self.__arrayCurrentA2)
      print("...askDiCounter::defineTree... self.__arrayCurrentA3 = %s \n")   % (self.__arrayCurrentA3)
      print("...askDiCounter::defineTree... self.__arrayCurrentA4 = %s \n")   % (self.__arrayCurrentA4)
      print("...askDiCounter::defineTree... self.__arrayCurrentB1 = %s \n")   % (self.__arrayCurrentB1)
      print("...askDiCounter::defineTree... self.__arrayCurrentB2 = %s \n")   % (self.__arrayCurrentB2)
      print("...askDiCounter::defineTree... self.__arrayCurrentB3 = %s \n")   % (self.__arrayCurrentB3)
      print("...askDiCounter::defineTree... self.__arrayCurrentB4 = %s \n")   % (self.__arrayCurrentB4)
    ## define branches....  for the signal
    if(self.__cmjPlotDiag > 2): print("...askDiCounter::defineTree... define branches \n")
    self.__localRootTree1.Branch('numberOfSignalEntries',self.__arrayNumberOfSignalEntries,'numberOfSignalEntries/I')
    self.__localRootTree1.Branch('diCounterId',self.__signalDiCounterId)
    self.__localRootTree1.Branch('signalTestDate',self.__signalTestDate)
    self.__localRootTree1.Branch('signalFlashRate',self.__signalFlashRate)
    self.__localRootTree1.Branch('signalTemperature',self.__arrayTemperature,'self._arrayTemperature[numberOfSignalEntries]/F')
    self.__localRootTree1.Branch('signalVoltage',self.__arrayVoltage,'self.__arrayVoltage[numberOfSignalEntries]/F')
    self.__localRootTree1.Branch('currentA1',self.__arrayCurrentA1,'self.__arrayCurrentA1[numberOfSignalEntries]/F')
    self.__localRootTree1.Branch('currentA2',self.__arrayCurrentA2,'self.__arrayCurrentA2[numberOfSignalEntries]/F')
    self.__localRootTree1.Branch('currentA3',self.__arrayCurrentA3,'self.__arrayCurrentA3[numberOfSignalEntries]/F')
    self.__localRootTree1.Branch('currentA4',self.__arrayCurrentA4,'self.__arrayCurrentA4[numberOfSignalEntries]/F')
    self.__localRootTree1.Branch('currentB1',self.__arrayCurrentB1,'self.__arrayCurrentB1[numberOfSignalEntries]/F')
    self.__localRootTree1.Branch('currentB2',self.__arrayCurrentB2,'self.__arrayCurrentB2[numberOfSignalEntries]/F')
    self.__localRootTree1.Branch('currentB3',self.__arrayCurrentB3,'self.__arrayCurrentB3[numberOfSignalEntries]/F')
    self.__localRootTree1.Branch('currentB4',self.__arrayCurrentB4,'self.__arrayCurrentB4[numberOfSignalEntries]/F')
    self.__arrayNumberOfSignalEntries[0] =  self.__numberOfSignal       ## this is important!  It tells how many entries in the arrays!
    self.__localRootTree1.Fill()
    if(self.__cmjPlotDiag > 2) : self.__localRootTree1.Scan()   ## use for debug... let's see what is in the root tree...
    ## place the dark current in another  directory, in another tree!
    self.__rootTreeFile.mkdir('DiCounterDarkCurrent')
    self.__rootTreeFile.cd('DiCounterDarkCurrent')
    self.__localRootTree2 = TTree('diCounterDarkCurrent','root tree with ntuples')								## without this, the arrays will be empty!
    self.__arrayNumberOfDarkCurrentEntries = array('i',self.__numberOfDark*[0])
    self.__arrayDarkCurrentA1 = array('f',self.__darkCurrentA1)
    self.__arrayDarkCurrentA2 = array('f',self.__darkCurrentA2)
    self.__arrayDarkCurrentA3 = array('f',self.__darkCurrentA3)
    self.__arrayDarkCurrentA4 = array('f',self.__darkCurrentA4)
    self.__arrayDarkCurrentB1 = array('f',self.__darkCurrentB1)
    self.__arrayDarkCurrentB2 = array('f',self.__darkCurrentB2)
    self.__arrayDarkCurrentB3 = array('f',self.__darkCurrentB3)
    self.__arrayDarkCurrentB4 = array('f',self.__darkCurrentB4)
    ## define branches....  for the signal
    if(self.__cmjPlotDiag > 2): print("...askDiCounter::defineTree... define branches \n")
    self.__localRootTree2.Branch('numberOfDarkCurrentEntries',self.__arrayNumberOfDarkCurrentEntries,'numberOfDarkCurrentEntries/I')
    self.__localRootTree2.Branch('darkCurrentId',self.__darkCurrentId)
    self.__localRootTree2.Branch('darkCurrentTestDate',self.__darkCurrentTestDate)
    self.__localRootTree2.Branch('darkCurrentA1',self.__arrayDarkCurrentA1,'self.__arrayDarkCurrentA1[numberOfDarkCurrentEntries]/F')
    self.__localRootTree2.Branch('darkCurrentA2',self.__arrayDarkCurrentA2,'self.__arrayDarkCurrentA2[numberOfDarkCurrentEntries]/F')
    self.__localRootTree2.Branch('darkCurrentA3',self.__arrayDarkCurrentA3,'self.__arrayDarkCurrentA3[numberOfDarkCurrentEntries]/F')
    self.__localRootTree2.Branch('darkCurrentA4',self.__arrayDarkCurrentA4,'self.__arrayDarkCurrentA4[numberOfDarkCurrentEntries]/F')
    self.__localRootTree2.Branch('darkCurrentB1',self.__arrayDarkCurrentB1,'self.__arrayDarkCurrentB1[numberOfDarkCurrentEntries]/F')
    self.__localRootTree2.Branch('darkCurrentB2',self.__arrayDarkCurrentB2,'self.__arrayDarkCurrentB2[numberOfDarkCurrentEntries]/F')
    self.__localRootTree2.Branch('darkCurrentB3',self.__arrayDarkCurrentB3,'self.__arrayDarkCurrentB3[numberOfDarkCurrentEntries]/F')
    self.__localRootTree2.Branch('darkCurrentB4',self.__arrayDarkCurrentB4,'self.__arrayDarkCurrentB4[numberOfDarkCurrentEntries]/F')
    self.__arrayNumberOfDarkCurrentEntries[0] =  self.__numberOfDark       ## this is important!  It tells how many entries in the arrays
    if(self.__cmjPlotDiag > 2) : print("self.__number of dark = %d \n") % (self.__numberOfDark)
    ##
    self.__localRootTree2.Fill()		## fill the root tree here...
    if(self.__cmjPlotDiag > 2) : self.__localRootTree2.Scan()   ## use for debug... let's see what is in the root tree...
    self.__rootTreeFile.Write()
    self.__rootTreeFile.Close()
## -------------------------------------------------------------
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
##Scatter Plots
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
    self.__myInstructions.setText('','Instructions/InstructionsForGuiDiCounters2017Jul7.txt')
    self.__myInstructions.grid(row=self.__firstRow,column=self.__col,columnspan=2)
    self.__firstRow += 1
##
    self.__col = 0
    self.__secondRow = 1
    self.__buttonWidth = 20
#    self.__getValues = Button(self,text='Get Input File',command=self.openFileDialog,width=self.__buttonWidth,bg='lightblue',fg='black')
#    self.__getValues.grid(row=self.__secondRow,column=self.__col,sticky=W)
#    self.__secondRow += 1
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
##
## --------------------------------------------------------------------
##
  def startInitialEntries(self):
    self.__myDiCounters.readFile("initial")
    self.__myDiCounters.sendDiCounterToDatabase()
##
## --------------------------------------------------------------------
##
  def sendMeasurements(self):
    self.__myDiCounters.readFile("measure")
    self.__myDiCounters.sendDiCounterTestsToDatabase()
##
## --------------------------------------------------------------------
##
  def sendImages(self):
    self.__myDiCounters.readFile("image")
    self.__myDiCounters.sendDiCounterImageToDatabase()
##
## --------------------------------------------------------------------
##
#  def turnOnDebug(self,tempDebug):
#    self.__myDiCounters.turnOnDebug(tempDebug)
## --------------------------------------------------------------------
#  def turnOnSendToDatabase(self):
#    self.__myDiCounters.turnOnSendToDatabase()
## --------------------------------------------------------------------
#  def turnOffSendToDatabase(self):
#    self.__myDiCounters.turnOffSendToDatabase()
## --------------------------------------------------------------------
#  def sendToDevelopmentDatabase(self):
#    self.__myDiCounters.sendToDevelopmentDatabase()
## --------------------------------------------------------------------
#  def sendToProductionDatabase(self):
#    self.__myDiCounters.sendToProductionDatabase()

## --------------------------------------------------------------------
if __name__ == '__main__':
  parser = optparse.OptionParser("usage: %prog [options] file1.txt \n")
  parser.add_option('-d',dest='debugMode',type='int',default=0,help='set debug: 0 (off - default), 1 = on')
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
#  if(options.debugMode != 0): myMultiForm.turnOnDebug(options.debugMode)
#  if(options.testMode != 0): 
#    myMultiForm.turnOffSendToDatabase()
#  else:
#    myMultiForm.turnOnSendToDatabase()
#    if(options.database == "development"): myMultiForm.sendToDevelopmentDatabase()
#    else: myMultiForm.sendToProductionDatabase()
  myMultiForm.grid()
  root.mainloop()



