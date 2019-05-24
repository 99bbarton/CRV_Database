# -*- coding: utf-8 -*-
##
##  File = "Modules.py"
##  Derived from File = "Modules_2017Jan13.py"
##  Derived from File = "Modules_2017Jan12.py"
##  Derived from File = "Modules_2016Dec20.py"
##  Derived from File = "DiCounters_2016Dec20.py"
##  Derived from File = "DiCounters_2016Dec19.py"
##  Derived from File = "DiCounters_2016Jun14.py"
##  Derived from File = "DiCounters_2016May16.py"
##  Derived from File = "Counters_2016May13.py"
##  Derived from File = "Fibers_2016May12.py"
##  Derived from File = "Extrusions_2016Jan27.py"
##  Derived from File = "Extrusions_2016Jan26.py"
##  Derived File = "Extrusions_2016Jan21.py"
##  Derived from File = "Extrusions_2016Jan14.py"
##  Derived from File = "Extrusions_2016Jan7.py"
##  Derived from File = "Extrusions_2015Oct12.py"
##
##  Test program to read in the lines from a comma separated
##  file saved from a spread sheet.  Here the delimiter is 
##  a tab and text is enclosed in "
##
##   Merrill Jenkins
##   Department of Physics
##   University of South Alabama
##   2015Sep23
##
#!/bin/env python
##
##  To run this script:
##	1) Input the initial Module information... 
##	python Modules.py -i 'moduleSpreadSheets/Module_2016Dec20.csv'
##	2) Input the test results
##	python Modules.py -i 'moduleSpreadSheets/ModuleTests_2017Jan13.csv' --mode 'measure'
##
##  Modified by cmj 2016Jan7... Add the databaseConfig class to get the URL for 
##		the various databases... change the URL in this class to change for all scripts.
##  Modified by cmj 2016Jan14 to use different directories for support modules...
##		These are located in zip files in the various subdirectories....
##  Modified by cmj2016Jan26.... change the maximum number of columns decoded to use variable.
##				change code to accomodate two hole positions										"pre_production" or "production"
##  Modified by cmj2016Jun24... Add one more upward level for subdirectory to get to the utilities directory
##  Modified by cmj2017Jan13... Add instructions for use in the call of the script.
##  Modified by cmj2017Feb2... Add test mode option; option to turn off send to database.
##  Modified by cmj2018Jun8... Change to hdbClient_v2_0
##  Modified by cmj2018Oct4.... Change the crvUtilities to contain version of cmjGuiLibGrid2018Oct1 that adds
##				yellow highlight to selected scrolled list items
##  Modified by cmj2019May16... Change "hdbClient_v2_0" to "hdbClient_v2_2"
##  Modified by cmj2019May23... Add update mode for modules...
##  Modified by cmj2019May23... Add a loop to give maxTries to send information to database.
##
##
##
sendDataBase = 0  ## zero... don't send to database
#
import os
import sys        ## 
import optparse   ## parser module... to parse the command line arguments
import math
from collections import defaultdict
from time import *
sys.path.append("../../Utilities/hdbClient_v2_2/Dataloader.zip")  ## 2018Jun8
sys.path.append("../CrvUtilities/crvUtilities2018.zip")      ## 2018Oct2 add highlight to scrolled list
from DataLoader import *   ## module to read/write to database....
from databaseConfig import *
from cmjGuiLibGrid2018Oct1 import *       ## 2018Oct2 add highlight to scrolled list
from generalUtilities import generalUtilities

ProgramName = "Modules.py"
Version = "version2019.05.22"


##############################################################################################
##############################################################################################
###  Class to store diCounter elements
class crvModules(object):
  def __init__(self):
    self.__cmjDebug = 0        ## no debug statements
    self.__maxColumns1 = 11  ## maximum columns in the spread sheet for input option: initial
    self.__maxColumns2 = 6   ## maximum columns in the spread sheet for input option: measure
    self.__maxColumns3 = 13	## maximum columns in the spread sheet for dicouner layer,position
    self.__maxColumns4 = 2 ## for the one module per spreadsheet scheme...
    self.__sendToDatabase = 0  ## Do not send to database
    self.__maxTries = 3		## set up maximum number of tries to send information to the database.
    self.__update = 0		## update = 0, add new entry, update = 1, update existing entry.
    self.__database_config = databaseConfig()
    self.__url = ''
    self.__password = ''
    self.__cmjDebug = 1
    ## Di-Counters Initial information
    self.__currentModuleId = ''		## For the one module per spreadsheet scheme... store the module id
    self.__moduleId = ''		
    self.__moduleType = ''
    self.__moduleConstructionDate = ''
    self.__moduleLocation = ''
    self.__moduleWidth = ''
    self.__moduleLength = ''
    self.__moduleThick = ''
    self.__moduleEpoxyLot = ''
    self.__moduleAluminum  = ''
    self.__moduleDeviationFromFlat = ''
    self.__moduleComments = ''
    ##					## The layer and position are contained in the di-counter tables....
    self.__moduleDiCounterPosition = defaultdict(dict)  ## Nested dictionary to hold the position and layer of a 
							## dicounter in the module....
							## (keys: [layer][position]
							## layer ranges from top to bottom: layer1, layer2, layer3, layer4
							## position 0, 1, 2, 3, 4, 5, 6, 7
## Di-Counters Initial information
    self.__startTime = strftime('%Y_%m_%d_%H_%M')
    self.__sleepTime = 1.0
## -----------------------------------------------------------------
  def __del__(self):
    self.__stopTime = strftime('%Y_%m_%d_%H_%M')
    self.__endBanner= []
    self.__endBanner.append("## ----------------------------------------- \n")
    self.__endBanner.append("## Program "+ProgramName+" Terminating at time "+self.__stopTime+" \n")
    for self.__endBannerLine in self.__endBanner:
      self.__logFile.write(self.__endBannerLine)
## -----------------------------------------------------------------
  def turnOnDebug(self,tempDebug):
    self.__cmjDebug = tempDebug  # turn on debug
    print("...crvModules::turnOnDebug... turn on debug \n")
## -----------------------------------------------------------------
  def turnOffDebug(self):
    self.__cmjDebug = 0  # turn on debug
    #print("...crvModules::turnOffDebug... turn off debug \n")
## -----------------------------------------------------------------
  def turnOnSendToDatabase(self):
    self.__sendToDatabase = 1      ## send to database
    print("...crvModules::turnOnSendToDataBase... send to database: self.__sendToDatabase = %s \n",self.__sendToDatabase)
## -----------------------------------------------------------------
  def turnOffSendToDatabase(self):
    self.__sendToDatabase = 0      ## send to database
    print("...crvModules::turnOffSendToDatabase... do not send to database \n")
## -----------------------------------------------------------------
  def sendToDevelopmentDatabase(self):
    self.__sendToDatabase = 1      ## send to database
    self.__whichDatabase = 'development'
    print("...crvModules::sendToDevelopmentDatabase... send to development database \n")
    self.__url = self.__database_config.getWriteUrl()
    self.__password = self.__database_config.getCompositeKey()
## -----------------------------------------------------------------
  def sendToProductionDatabase(self):
    self.__sendToDatabase = 1      ## send to database
    self.__whichDatabase = 'production'
    print("...crvModules::sendToProductionDatabase... send to production database \n")
    self.__url = self.__database_config.getProductionWriteUrl()
    self.__password = self.__database_config.getCompositeProductionKey()
## ---------------------------------------------------------------
##  Change dataloader to update rather than insert.
  def updateMode(self):
    print("...crvModules::updateMode ==> change from insert to update mode")
    self.__update = 1
## -----------------------------------------------------------------
## -----------------------------------------------------------------
## -----------------------------------------------------------------
## -----------------------------------------------------------------
###############################################1###############################################
##############################################################################################
##############################################################################################
###   This is a class to read in an Excel spreadsheet page saved as a comma separated file
###   for the Sipms... The results are written in the database
###   The user can choose between the development or production database....
###
### -----------------------------------------------------------------
  def openFile(self,tempFileName):	## method to open the file
    self.__inFileName = tempFileName
    self.__inFile=open(self.__inFileName,'r')   ## read only file
## -----------------------------------------------------------------
  def readFile(self,tempInputMode):		## method to read the file's contents
    ## Module Test information
    self.__moduleTestDate = {}			## Dictionary to hold the date of the tests (key modulesId)
    self.__moduleTestLightSource = {}		## Dictionary to hold the test light source (key modulesId)
    self.__moduleTestLightYieldAverage = {}	## Dictionary to hold the test light average (key modulesId)
    self.__moduleTestLightYieldStDev = {}	## Dictionary to hold the test light StDev (key modulesId)
    self.__moduleTestComments = {}		## Dictionary to hold comments on the module (key modulesId)

##
    if(self.__cmjDebug > 0): print 'mode value %s \n' % tempInputMode
    self.__fileLine = []
    self.__fileLine = self.__inFile.readlines()  ## Read whole file here....
##	Sort, define and store information here...
    if(tempInputMode == 'initial'):
      for self.__newLine in self.__fileLine:
	if(self.__cmjDebug > 99): print("self.__newLine = %s \n") % (self.__newLine)
	if (self.__newLine.find('Module_Id') != -1): 		self.storeModuleId(self.__newLine)
	if (self.__newLine.find('Module_Type') != -1):		self.storeModuleType(self.__newLine)
	if (self.__newLine.find('Construction_Date') != -1): 	self.storeModuleDate(self.__newLine)
	if (self.__newLine.find('Module_Location') != -1): 	self.storeModuleLocation(self.__newLine)
	if (self.__newLine.find('Width_mm') != -1): 		self.storeModuleWidth(self.__newLine)
	if (self.__newLine.find('Length_mm') != -1): 		self.storeModuleLength(self.__newLine)
	if (self.__newLine.find('Thick_mm') != -1):		self.storeModuleThick(self.__newLine)
	if (self.__newLine.find('Epoxy_Lot') != -1):		self.storeModuleExpoxyLot(self.__newLine)
	if (self.__newLine.find('Aluminum') != -1):		self.storeModuleAluminum(self.__newLine)
	if (self.__newLine.find('Total_flatness_dev_mm') != -1): self.storeModuleFlat(self.__newLine)
	if (self.__newLine.find('Comments') != -1): 		self.storeModuleComments(self.__newLine)
	if (self.__newLine.find('layer') != -1): self.storeDicounterPosition(self.__newLine)
      print 'Read in crvModules initial information'
    elif(tempInputMode == 'measure'):
      for self.__newLine in self.__fileLine:
	#print("self.__newLine = <%s>") % self.__newLine
	if (self.__newLine.find('crvModule-') != -1): self.storeModuleMeasure(self.__newLine)
      print 'Read in crvModules test results information'
    print 'end of crvModules::readFile'
## -----------------------------------------------------------------
##	Methods to open logfiles
##    def setLogFileName(self,tempFileName):
##	  self.__logFileName = 'logFiles/'+tempFileName+strftime('%Y_%m_%d_%H_%M')+'.txt'
## -----------------------------------------------------------------
  def openLogFile(self):
    self.__logFileName = 'logFiles/di-counter-logFile-'+strftime('%Y_%m_%d_%H_%M')+'.txt'
    self.__logFile = open(self.__logFileName,"w+")
    if(self.__cmjDebug == 2): print '----- saveResult::openFile: write to %s' % self.__logFileName
    self.__banner = []
    self.__banner.append("##")
    self.__banner.append("##  module log file: "+self.__logFileName+"\n")
    self.__banner.append("##	This is a file that logs then di-counter entries into \n")
    self.__banner.append("##	the Mu2e CRV Quality Assurance/Quality Control Harware database \n")
    self.__banner.append("##  Program "+ProgramName+" Begining at time "+self.__startTime+" \n")
    self.__banner.append("##    Input Module File (.csv) = "+self.__inFileName+" \n")
    self.__banner.append("##    Start :"+self.__startTime+"\n")
    self.__banner.append("## \n")
    self.__banner.append("## ----------------------------------------- \n")
    self.__banner.append("## \n")
    for self.__beginBannerLine in self.__banner:
      self.__logFile.write(self.__beginBannerLine)
##
##
##	Method to setup access to the database
## -----------------------------------------------------------------
## -----------------------------------------------------------------
##
##	This method allows three different types of entries:
##	1) (inital) Setup the initial dicounter dimensions and history
##	2) (measure) Enter the test results... this may be done multiple times
##
## -----------------------------------------------------------------
## -----------------------------------------------------------------
##
  def sendToDatabase(self,tempInputMode):
    if(tempInputMode.strip() == 'initial'):
      self.connectDiCounterLayerPosition()
      self.sendModuleToDatabase()
      #self.connectDiCounterLayerPosition()
    elif(tempInputMode.strip() == 'measure'):
      self.sendModuleTestsToDatabase()
    else:
      print ("XXXX __crvModules__::sendToDatabase: invalid choice inputMode = %s") % tempInputMode 
## -----------------------------------------------------------------
##  This is for the GUI... It can't pass arguments from button clicks!
  def sendInitialToDatabase(self):
    self.sendModuleToDatabase()
    self.connectDiCounterLayerPosition()
## -----------------------------------------------------------------
##  This is for the GUI... It can't pass arguments from button clicks!
  def sendTestToDatabase():
    self.sendModuleTestsToDatabase()
##
## -----------------------------------------------------------------
## -----------------------------------------------------------------
####  The next three functions construct the output string sent to the
####    database, send the string to the database and dump the string if needed...
####  Option 1: "initial": Send crvModules initial information to the database
####  Next send the crvModules data to the database... one crvModules at a time!
####  This done after the statistics for a batch have been loaded....
  def sendModuleToDatabase(self):
    self.__group = "Composite Tables"
    self.__crvModulesTable = "Modules"
    if(self.__cmjDebug > 10):
      print "XXXX __crvModules__::sendModuleToDatabase... self.__url = %s " % self.__url
      print "XXXX __crvModules__::sendModuleToDatabase... self.__password = %s \n" % self.__password
      ### Must load the crvModules table first!
    self.__crvModulesString = self.buildRowString_for_Module_table()
    self.logModuleString()
    if self.__cmjDebug != 0: 
      print ("XXXX __crvModules__::sendModuleToDatabase: self.__moduleId = %s") % (self.__moduleId)
      self.dumpModuleString()  ## debug.... dump crvModules string...
    if self.__sendToDatabase != 0:
      print "send crvModule to database!"
      self.__myDataLoader1 = DataLoader(self.__password,self.__url,self.__group,self.__crvModulesTable)
      if(self.__update == 0):					##cmj2019May23... add update
	self.__myDataLoader1.addRow(self.__crvModulesString)	##cmj2019May23... add new line
      else:
	self.__myDataLoader1.addRow(self.__crvModulesString,'update')	##cmj2019May23... update existing line
      for n in range(0,self.__maxTries):				## cmj2019May23... try to send maxTries time to database
	(self.__retVal,self.__code,self.__text) = self.__myDataLoader1.send()  ## send it to the data base!
	print "self.__text = %s" % self.__text
	sleep(self.__sleepTime)     ## sleep so we don't send two records with the same timestamp....
	if self.__retVal:				## sucess!  data sent to database
	  print "XXXX __crvModules__::sendModuleToDatabase: "+self.__moduleId+" Transmission Success!!!"
	  self.__logFile.write('XXXX__diCounter__::sendModuleToDatabase: send '+self.__moduleId+' to database.')
	  print self.__text
	  break
	elif self.__password == '':
	  print('XXXX __crvModules__::sendModuleToDatabase: Test mode... DATA WILL NOT BE SENT TO THE DATABASE')()
	  break
	else:
	  print "XXXX __crvModules__::sendModuleToDatabase:  Counter Transmission: Failed!!!"
	  print self.__code
	  print self.__text 
	  self.__logFile.write("XXXX__diCounter__::sendModuleToDatabase:  Transmission: Failed!!!")
	  self.__logFile.write('XXXX__diCounter__::sendModuleToDatabase... self.__code = '+self.__code+'\n')
	  self.__logFile.write('XXXX__diCounter__::sendModuleToDatabase... self.__text = '+self.__text+'\n')
    return 0
## -----------------------------------------------------------------
## -----------------------------------------------------------------
#### Build the string for a crvModules
  def buildRowString_for_Module_table(self):  
      self.__sendModuleRow = {}
      self.__sendModuleRow['module_id'] = self.__moduleId
      self.__sendModuleRow['module_type'] = self.__moduleType
      self.__sendModuleRow['location'] = self.__moduleLocation
      self.__sendModuleRow['width_mm'] = self.__moduleWidth
      self.__sendModuleRow['height_mm'] = self.__moduleLength
      self.__sendModuleRow['thick_mm'] = self.__moduleThick
      self.__sendModuleRow['expoxy_lot'] = self.__moduleEpoxyLot
      self.__sendModuleRow['aluminum'] = self.__moduleAluminum
      self.__sendModuleRow['deviation_from_flat_mm'] = self.__moduleDeviationFromFlat
      self.__sendModuleRow['comments'] = self.__moduleComments
      return self.__sendModuleRow
## ----------------------------------------------------------------- 
#### Diagnostic function to print out the dictionary for the fiber batch table:
  def dumpModuleString(self):
      print "XXXX __crvModules__::dumpModuleString:  Diagnostic"
      print "XXXX __crvModules__::dumpModuleString:  Print dictionary sent to database"
      for self.__tempLocal in self.__sendModuleRow:
	print('    self.__sendModuleRow[%s] = %s') % (self.__tempLocal,str(self.__sendModuleRow[self.__tempLocal]))
## ----------------------------------------------------------------- 
#### Diagnostic function to print out the dictionary for the fiber batch table:
  def logModuleString(self):
    for self.__tempLocal in self.__crvModulesString.keys():
	self.__logFile.write(' self.__crvModulesString['+self.__tempLocal+'] = '+str(self.__crvModulesString[self.__tempLocal])+'\n')
##
## -----------------------------------------------------------------
## -----------------------------------------------------------------
####  The next three functions construct the output string sent to the
####    database, send the string to the database and dump the string if needed...
####  Option 2: "measure": Send diCounter test results information to the database
####  Next send the diCounter data to the database... one crvModules at a time!
####  This done after the statistics for a batch have been loaded....
  def sendModuleTestsToDatabase(self):
    self.__group = "Composite Tables"
    self.__crvModulesTestsTable = "Module_Tests"
    if(self.__cmjDebug > 10):
      print "XXXX __crvModules__::sendModuleTestsToDatabase... self.__url = %s " % self.__url
      print "XXXX __crvModules__::sendModuleTestsToRowoDatabase... self.__password = %s \n" % self.__password
    for self.__localModuleTestsId in sorted(self.__moduleId.keys()):
      ### Must load the crvModules table first!
      self.__crvModulesTestsString = self.buildRowString_for_ModuleTests_table(self.__localModuleTestsId)
      self.logModuleString()
      if self.__cmjDebug != 0: 
	print ("XXXX __crvModules__::sendModuleTestsToDatabase: self.__localFiberId = %s") % (self.__localModuleTestsId)
	self.dumpModuleTestsString()  ## debug.... dump crvModules string...
      if self.__sendToDatabase != 0:
	if(self.__cmjDebug != 0): print "send to crvModules database!"
	self.__myDataLoader1 = DataLoader(self.__password,self.__url,self.__group,self.__crvModulesTestsTable)
	if(self.__update ==0):							## cmj2019May23... add update
	  self.__myDataLoader1.addRow(self.__crvModulesTestsString,'insert')	## cmj2019May23... add new entry
	else:
	  self.__myDataLoader1.addRow(self.__crvModulesTestsString,'update')	## cmj2019May23... update existing row.
	for n in range(0,self.__maxTries):					## cmj2019May23... try to send to database maxTries times
	  (self.__retVal,self.__code,self.__text) = self.__myDataLoader1.send()  	## send it to the data base!
	  print "self.__text = %s" % self.__text
	  sleep(self.__sleepTime)     ## sleep so we don't send two records with the same timestamp....
	  if self.__retVal:				## sucess!  data sent to database
	    if(self.__cmjDebug !=0): print "XXXX __crvModules__::sendModuleTestsToDatabase:"+self.__moduleId[self.__localModuleTestsId]+" Transmission Success!!!"
	    print self.__text
	    break
	  elif self.__password == '':
	    print('XXXX __crvModules__::sendModuleTestsToDatabase: Test mode... DATA WILL NOT BE SENT TO THE DATABASE')()
	    break
	  else:
	    print "XXXX __crvModules__::sendModuleTestsToDatabase:  Counter Transmission: Failed!!!"
	    print self.__code
	    print self.__text 
	    self.__logFile.write("XXXX__crvModules__::sendModuleTestsToDatabase:  Transmission: Failed!!!")
	    self.__logFile.write('XXXX__crvModules__:sendModuleTestsToDatabase... self.__code = '+self.__code+'\n')
	    self.__logFile.write('XXXX__crvModules__:sendModuleTestsToDatabase... self.__text = '+self.__text+'\n')
    return 0
## -----------------------------------------------------------------
## -----------------------------------------------------------------
#### Build the string for a crvModules tests...
  def buildRowString_for_ModuleTests_table(self,tempKey):  
    self.__sendModuleTestsToRow = {}
    self.__sendModuleTestsToRow['module_id'] = self.__moduleId[tempKey]
    self.__sendModuleTestsToRow['test_date'] = self.__moduleTestDate[tempKey]
    self.__sendModuleTestsToRow['light_yield_source'] = self.__moduleTestLightSource[tempKey]
    self.__sendModuleTestsToRow['light_yield_avg'] = self.__moduleTestLightYieldAverage[tempKey]
    self.__sendModuleTestsToRow['light_yield_stdev'] = self.__moduleTestLightYieldStDev[tempKey]
    self.__sendModuleTestsToRow['comments'] = self.__moduleTestComments[tempKey]
    return self.__sendModuleTestsToRow

## ----------------------------------------------------------------- 
#### Diagnostic function to print out the dictionary for the fiber batch table:
  def dumpModuleTestsString(self):
    print "XXXX __crvModules__::dumpModuleTestsString:  Diagnostic"
    print "XXXX __crvModules__::dumpModuleTestsString:  Print dictionary sent to database"
    for self.__tempLocal in self.__sendModuleTestsToRow:
      print('    self.__sendModuleTestsToRow[%s] = %s') % (self.__tempLocal,str(self.__sendModuleTestsToRow[self.__tempLocal]))
## ----------------------------------------------------------------- 
#### Diagnostic function to print out the dictionary for the fiber batch table:
  def logModuleTestString(self):
    for self.__tempLocal in self.__crvModulesTestsString.keys():
	self.__logFile.write(' self.__crvModulesTestsString['+self.__tempLocal+'] = '+str(self.__crvModulesTestsString[self.__tempLocal])+'\n')
##
## ***************************************************************************************
## ***************************************************************************************
##	Connect the layer and position of the dicounter
##	to the dicounter in the dicounter tables....
##	Note this is a different table!!!
  def connectDiCounterLayerPosition(self):
    self.__group = "Composite Tables"
    self.__diCounterTable = "Di_Counters"
    if(self.__cmjDebug != 0):  print "XXXX __crvModules__::writeDiCounterLayerPosition... self.__url = %s " % self.__url
    if(self.__cmjDebug == 10): print "XXXX __crvModules__::writeDiCounterLayerPosition... self.__password = %s \n" % self.__password
    ## loop over the di-counters.... layer, then position.....
    self.__localLayerIndex = 0
    for self.__localModuleLayer in sorted(self.__moduleDiCounterPosition.keys()):
      if(self.__cmjDebug > 1): print("XXXX __crvModules__::writeDiCounterLayerPosition: localModuleLayer = %s \n") %(self.__localModuleLayer) 
      self.__localDiCounterIndex = 0
      for self.__localDiCounterPosition in sorted(self.__moduleDiCounterPosition[self.__localModuleLayer].keys()):
	self.__localDiCounterId = self.__moduleDiCounterPosition[self.__localModuleLayer][self.__localDiCounterPosition]
	if(self.__cmjDebug > 1): print("XXXX __crvModules__::writeDiCounterLayerPosition: localDiCounterPosition = %s \n") %(self.__localDiCounterIndex) 
	self.__diCounterString = self.buildDicounterLayerPositionString(self.__localDiCounterId,self.__localModuleLayer,self.__localDiCounterIndex)
	##self.__diCounterString = self.buildDicounterLayerPositionString(self.__localDiCounterId,self.__localLayerIndex,self.__localDiCounterIndex)
	self.logDiCounterString()
	if self.__cmjDebug > 1: 
	  print ("XXXX __crvModules__::writeDiCounterLayerPosition: self.__localFiberId = %s") % (self.__localDiCounterId)
	  self.dumpDiCounterConnectionString()  ## debug.... dump diCounter string...
	if self.__sendToDatabase != 0:
	  print "send to diCounter layer,position to  database!"
	  self.__myDataLoader1 = DataLoader(self.__password,self.__url,self.__group,self.__diCounterTable)
	  self.__myDataLoader1.addRow(self.__diCounterString,'update')  ## update the existing di-counter record
	  for n in range(0,self.__maxTries):
	    (self.__retVal,self.__code,self.__text) = self.__myDataLoader1.send()  ## send it to the data base!
	    print "self.__text = %s" % self.__text
	    sleep(self.__sleepTime)     ## sleep so we don't send two records with the same timestamp....
	    if self.__retVal:				## sucess!  data sent to database
	      print "XXXX __crvModules__::writeDiCounterLayerPosition: diCounter:"+self.__localDiCounterId+' Layer: '+str(self.__localLayerIndex)+' Position: '+str(self.__localDiCounterIndex)+" Counter Transmission Success!!!"
	      #### change back after requested change.... self.__logFile.write('XXXX __crvModules__::writeDiCounterLayerPosition: connect '+self.__localDiCounterId+' '+self.__localModuleLayer+' '+str(self.__localDiCounterIndex)+' in database')
	      self.__logFile.write('XXXX __crvModules__::writeDiCounterLayerPosition: connect '+self.__localDiCounterId+' '+str(self.__localLayerIndex)+' '+str(self.__localDiCounterIndex)+' in database')
	      print self.__text
	    elif self.__password == '':
	      print('XXXX__crvModules__::writeDiCounterLayerPosition: Test mode... DATA WILL NOT BE SENT TO THE DATABASE')()
	    else:
	      print "XXXX__crvModules__::writeDiCounterLayerPosition:  Counter Transmission: Failed!!!"
	      if(self.__cmjDebug > 1): 
		print("XXXX__crvModules__:writeDiCounterLayerPosition... Counter Transmission Failed: \n")
		print("XXXX__crvModules__:writeDiCounterLayerPosition... String sent to dataLoader: \n")
		print("XXXX__crvModules__:writeDiCounterLayerPosition... self.__diCounterString \%s \n") % (self.__diCounterString)
	      print ("XXXX__crvModules__:writeDiCounterLayerPosition... self.__code = %s \n") % (self.__code)
	      print ("XXXX__crvModules__:writeDiCounterLayerPosition... self.__text = %s \n") % (self.__text) 
	      self.__logFile.write("XXXX__crvModules__::writeDiCounterLayerPosition:  Counter Transmission: Failed!!!")
	      self.__logFile.write('XXXX__crvModules__::writeDiCounterLayerPosition... self.__code = '+self.__code+'\n')
	      self.__logFile.write('XXXX__crvModules__::writeDiCounterLayerPosition... self.__text = '+self.__text+'\n')
	self.__localDiCounterIndex += 1
      self.__localLayerIndex += 1
## -----------------------------------------------------------------
## build the string to connect the dicounters in the layers and positions....
  def buildDicounterLayerPositionString(self,tempDiCounterId,tempModuleLayer,tempDiCounterPosition):
    self.__diCounterUpdate = {}
    self.__diCounterUpdate['di_counter_id'] = 'di-'+tempDiCounterId
    self.__diCounterUpdate['module_id'] = self.__moduleId
    self.__diCounterUpdate['module_layer'] = str(tempModuleLayer)
    self.__diCounterUpdate['layer_position'] = str(tempDiCounterPosition)
    return self.__diCounterUpdate
## -----------------------------------------------------------------
## Diagnostic function to print out the dictionary for the dicounter connection string sent to database
  def dumpDiCounterConnectionString(self):
    print("XXXX__crvModules__::buildDicounterLayerPositionString... self.__diCounterString = %s \n") %(self.__diCounterString)
    print("XXXX__crvModules__::buildDicounterLayerPositionString... self.__diCounterUpdate['di_counter_id'] = %s") %(self.__diCounterUpdate['di_counter_id'])
    print("XXXX__crvModules__::buildDicounterLayerPositionString... self.__diCounterUpdate['module_id'] = %s") %(self.__diCounterUpdate['module_id'])
    print("XXXX__crvModules__::buildDicounterLayerPositionString... self.__diCounterUpdate['module_layer'] = %s") %(self.__diCounterUpdate['module_layer'])
    print("XXXX__crvModules__::buildDicounterLayerPositionString... self.__diCounterUpdate['layer_position'] = %s \n") %(self.__diCounterUpdate['layer_position'])
## -----------------------------------------------------------------
#### Diagnostic function to print out the dictionary for the fiber batch table:
  def logDiCounterString(self):
      for self.__tempLocal in self.__diCounterString.keys():
	self.__logFile.write(' self.__diCounterString['+self.__tempLocal+'] = '+str(self.__diCounterString[self.__tempLocal])+'\n')
##
## ***************************************************************************************
## ***************************************************************************************
##
##
##
## -----------------------------------------------------------------   
### Store functions.... must be called within the class to store the information
## -----------------------------------------------------------------
##
## -----------------------------------------------------------------
##  A series of functions for a single module per spreadsheet
  def storeModuleId(self,tempNewLine):
    self.__item= []
    self.__item = tempNewLine.rsplit(',',self.__maxColumns3)
    self.__moduleId = self.__item[1]
  ## ----------------------------------
  def storeModuleType(self,tempNewLine):
    self.__item =[]
    self.__item = tempNewLine.rsplit(',',self.__maxColumns3)
    self.__moduleType = self.__item[1]
  ## ----------------------------------
  def storeModuleDate(self,tempNewLine):
    self.__item =[]
    self.__item = tempNewLine.rsplit(',',self.__maxColumns3)
    self.__moduleConstructionDate = self.__item[1]
  ## ----------------------------------
  def storeModuleLocation(self,tempNewLine):
    self.__item =[]
    self.__item = tempNewLine.rsplit(',',self.__maxColumns3)
    self.__moduleLocation = self.__item[1]
  ## ----------------------------------
  def storeModuleWidth(self,tempNewLine):
    self.__item =[]
    self.__item = tempNewLine.rsplit(',',self.__maxColumns3)
    self.__moduleWidth = self.__item[1]
  ## ----------------------------------
  def storeModuleLength(self,tempNewLine):
    self.__item =[]
    self.__item = tempNewLine.rsplit(',',self.__maxColumns3)
    self.__moduleLength = self.__item[1]
  ## ----------------------------------
  def storeModuleThick(self,tempNewLine):
    self.__item =[]
    self.__item = tempNewLine.rsplit(',',self.__maxColumns3)
    self.__moduleThick = self.__item[1]
  ## ----------------------------------
  def storeModuleExpoxyLot(self,tempNewLine):
    self.__item =[]
    self.__item = tempNewLine.rsplit(',',self.__maxColumns3)
    self.__moduleEpoxyLot = self.__item[1]
    print("+++++++++++ storeModuleExpoxyLot: item = %s") % (self.__item)
  ## ----------------------------------
  def storeModuleAluminum(self,tempNewLine):
    self.__item =[]
    self.__item = tempNewLine.rsplit(',',self.__maxColumns3)
    self.__moduleAluminum = self.__item[1]
  ## ----------------------------------
  def storeModuleFlat(self,tempNewLine):
    self.__item =[]
    self.__item = tempNewLine.rsplit(',',self.__maxColumns3)
    self.__moduleDeviationFromFlat = self.__item[1]
  ## ----------------------------------
  def storeModuleComments(self,tempNewLine):
    self.__item =[]
    self.__item = tempNewLine.rsplit(',',self.__maxColumns3)
    self.__moduleComments = self.__item[1]


## -----------------------------------------------------------------
##      Read the dicounter layer and position 
  def storeDicounterPosition(self,tempLayer):
    self.__item = [] 
    self.__item = tempLayer.rsplit(',',self.__maxColumns3)
    if(self.__item[0] == 'layer1'):
      for n in range(5,13):
	self.__moduleDiCounterPosition[self.__item[0]][n] = self.__item[n].strip()
    if(self.__item[0] == 'layer2'):
      for n in range(4,12):
	self.__moduleDiCounterPosition[self.__item[0]][n] = self.__item[n].strip()
    if(self.__item[0] == 'layer3'):
      for n in range(3,11):
	self.__moduleDiCounterPosition[self.__item[0]][n] = self.__item[n].strip()
    if(self.__item[0] == 'layer4'):
      for n in range(2,10):
	self.__moduleDiCounterPosition[self.__item[0]][n] = self.__item[n].strip()
    if(self.__cmjDebug > 0):
      print("__crvModules::storeDicounterPosition__ self.__moduleDicounterPosition = %s \n") % (self.__moduleDiCounterPosition[self.__item[0]])
    


## -----------------------------------------------------------------
##	Read in diCounter measred test results: option 3: "measure"
  def storeModuleMeasure(self,tempCounter):
    self.__item = []
    self.__item = tempCounter.rsplit(',',self.__maxColumns2)
    self.__moduleId[self.__item[0]] = self.__item[0]
    self.__moduleTestDate[self.__item[0]] = self.timeStamper(self.__item[1])
    self.__moduleTestLightSource[self.__item[0]] = self.__item[2] 
    self.__moduleTestLightYieldAverage[self.__item[0]] = self.__item[3]
    self.__moduleTestLightYieldStDev[self.__item[0]] = self.__item[4]
    self.__moduleTestComments[self.__item[0]] = self.__item[5]

##
##
## -----------------------------------------------------------------
## -----------------------------------------------------------------
##	Utility methods...
##
##
## -----------------------------------------------------------------
##  This method translates the excel spreadiCounterd sheet date into the
##  format expected by the timestamp used in the database
##
  def dateStamper(self,tempInput):
    self.__tempDate = tempInput
    self.__tempMmDdYy = {}
    self.__tempMmDdYy = self.__tempDate.rsplit('/',3)
    self.__tempMonth = self.__tempMmDdYy[0]
    if (int(self.__tempMonth) < 10): self.__tempMonth = '0'+self.__tempMonth 
    self.__tempDay   = self.__tempMmDdYy[1]
    if (int(self.__tempDay) < 10 ): self.__tempDay = '0'+self.__tempDay
    self.__tempYear  = self.__tempMmDdYy[2]
    if (int(self.__tempYear) < 2000 ): self.__tempYear = '20'+self.__tempYear
    self.__tempDateStamp = self.__tempMonth+'/'+self.__tempDay+'/'+self.__tempYear
    if(self.__cmjDebug > 11):
      print("XXXX__crvModules__:dateStamper...... self.__tempDate      = <%s>") % (self.__tempDate)
      print("XXXX__crvModules__:dateStamper...... self.__tempMmDdYy    = <%s>") % (self.__tempMmDdYy)
      print("XXXX__crvModules__:dateStamper...... self.__tempMonth     = <%s>") % (self.__tempMonth)
      print("XXXX__crvModules__:dateStamper....crvModules.. self.__tempDay       = <%s>") % (self.__tempDay)
      print("XXXX__crvModules__:dateStamper...... self.__tempYear      = <%s>") % (self.__tempYear)
    if(self.__cmjDebug > 10):
      print("XXXX__crvModules__:dateStamper...... self.__tempDateStamp = <%s>") % (self.__tempDateStamp)
    return self.__tempDateStamp


## -----------------------------------------------------------------
##  This method translates the excel spread sheet date and time into the
##  format expected by the timestamp used in the database
##
  def timeStamper(self,tempInput):
    #  The following code is to compensate between the different time formats between excel & database
    #  Begin excel/timestamp format translation.
    #  Allowable formats for production_date are  YYYY-MM-DD or MM/DD/YYYY with year in range 2000-2049
    self.__tempDate = tempInput
    self.__tempMmDdYy = {}
    self.__tempMmDdYy = self.__tempDate.rsplit('/',3)
    self.__tempMonth = self.__tempMmDdYy[0] 
    if (int(self.__tempMonth) < 10): self.__tempMonth = '0' + str(self.__tempMonth)
    self.__tempDay = self.__tempMmDdYy[1]
    if (int(self.__tempDay) < 10) : self.__tempDay = '0'+str(self.__tempDay)
    self.__tempCombined = {}
    self.__tempCombined = self.__tempMmDdYy[2]
    self.__tempYyHM = {}
    self.__tempYyHM = self.__tempCombined.rsplit(' ',2)
    self.__tempYear = self.__tempYyHM[0]
    self.__tempTime = {}
    self.__tempTime = self.__tempYyHM[1].rsplit(':',2)
    self.__tempHour = self.__tempTime[0]

    self.__tempMin  = self.__tempTime[1]
    if(int(self.__tempHour) < 10): self.__tempHour = '0'+ self.__tempHour
    if(int(self.__tempMin) < 10): self.__tempMin = '0' + self.__tempMin
    self.__tempTimeStamp = '20'+self.__tempYear+'-'+self.__tempMonth+'-self.__localDiCounterIndex'+self.__tempDay+' '+self.__tempHour+':'+self.__tempMin
    if(self.__cmjDebug > 11):
      print("XXXX__crvModules__:timeStamper...... self.__tempDate     = <%s>") % (self.__tempDate)
      print("XXXX__crvModules__:timeStamper...... self.__tempMmDdYy   = <%s>") % (self.__tempMmDdYy)
      print("XXXX__crvModules__:timeStamper...... self.__tempMonth    = <%s>") % (self.__tempMonth)
      print("XXXX__crvModules__:timeStamper...... self.__tempDay      = <%s>") % (self.__tempDay)
      print("XXXX__crvModules__:timeStamper...... self.__tempCombined = <%s>") % (self.__tempCombined)
      print("XXXX__crvModules__:timeStamper...... self.__tempYear     = <%s>") % (self.__tempYear)
      print("XXXX__crvModules__:timeStamper...... self.__tempHour  = <%s>") % (self.__tempHour)
      print("XXXX__crvModules__:timeStamper...... self.__tempMin   = <%s>") % (self.__tempMin)
    if(self.__cmjDebug > 10):
      print("XXXX__crvModules__:timeStamper....... self.__tempTimeStamp   = <%s>") % (self.__tempTimeStamp)
    #  End excel/timestamp format translation.
    return self.__tempTimeStamp

## -----------------------------------------------------------------
##

##############################################################################################
##############################################################################################
##  Entry point to program if this file is executed...
if __name__ == '__main__':
  parser = optparse.OptionParser("usage: %prog [options] file1.txt ")
#	Build general help string
  modeString = []
  modeString.append("To run in default mode (add module to database):")
  modeString.append("> python Modules.py -i ModuleSpreadsheet.cvs")
  modeString.append("To run to add module test results to database:")
  modeString.append("> python Modules.py -i ModuleTestSpreadsheet.cvs --mode ''measure''")
  modeString.append("The user may use a relative or absolute path to the spreadsheet ")
#	Input comma separated file name:
  parser.add_option('-i',dest='inputCvsFile',type='string',default="",help=modeString[0]+"\t\t\t"+modeString[1]+"\t\t\t"+modeString[2]+"\t\t\t"+modeString[3]+"\t\t\t\t\t\t\t"+modeString[4])
  modeString1 =[]
  modeString1.append("Input Mode: This script is run in several modes: \t\t\t")
  modeString1.append("initial: The default mode enters the initial module information. \t\t\t\t\t")
  modeString1.append("measure: This mode enters module test results into the database... Multiple test may be entered. ")
  parser.add_option('--mode',dest='inputMode',type='string',default="iniself.__localDiCounterIndextial",help=modeString1[0]+modeString1[1]+modeString1[2])
#	Debug level
  parser.add_option('-d',dest='debugMode',type='int',default=0,help='set debug: 0 (off - default), 1 = on')
  parser.add_option('-t',dest='testMode',type='int',default=0,help='set to test mode (do not send to database): 1')
  options, args = parser.parse_args()
  inputCounterFile = options.inputCvsFile
  if(inputCounterFile == ''):
    print("Supply input spreadsheet comma-separated-file")
    for outString in modeString:
      print("%s") % outString
      exit()
  inputModeValue = options.inputMode
  print ("\nRunning %s \n") % (ProgramName)
  print ("%s \n") % (Version)
  print "inputCounterFile = %s " % inputCounterFile
  myCrvModules = crvModules()
  if(options.debugMode == 0):
    myCrvModules.turnOffDebug()
  else:
    myCrvModules.turnOnDebug(options.debugMode)
  print("__main__ options.testMode = %s \n") % (options.testMode)
  if(options.testMode == 0):
    print("__main__ send to database! \n")
    myCrvModules.sendToDevelopmentDatabase()  ## turns on send to database
    #myCrvModules.sendToProductionDatabase()  ## turns on send to database
  else:
    myCrvModules.turnOffSendToDatabase()
  ## --------------------------------------------
  if(options.debugMode == 1): print '__name__ inputModeValue = %s \n' % inputModeValue
  myCrvModules.openFile(inputCounterFile)
  myCrvModules.openLogFile()
  myCrvModules.readFile(inputModeValue)
  myCrvModules.sendToDatabase(inputModeValue) 
#
  print("Finished running %s \n") % (ProgramName)
#


