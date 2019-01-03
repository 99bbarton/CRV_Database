# -*- coding: utf-8 -*-
## File = "databaseConfig.py"
##
##   Written by:
##   Merrill Jenkins
##   Department of Physics
##   University of South Alabama
##   2016Jan
##
##  This python script contains the class to access
##  the development and production database
##
#!/usr/bin/env python
##
##  To transmit any changes to the dependent
##  python scripts, complete these steps in the
##  Utilities directory:
##     > rm Utilities.zip
##     > zip -r Utilities.zip *.py
##
##	2016Jan21... Add simp and extrusion keys...
##	2016May9... Add Composite, Electronics and Fibers 
##      2016May9... Add getVersion method....
##
##	2018Feb16... Add urls for updated databases.
##
class databaseConfig(object):
  def __init__(self):
    self.__cmjDebug = 0  ## set to 1 to print debug statements
    #self.__queryUrl = "http://ifb-data.fnal.gov:8131/QE/mu2e_hw/app/SQ/query"  ## url updated 2018Feb15
    #self.__writeUrl = "http://dbweb5.fnal.gov:8080/mu2edev/hdb/loader"
    #self.__writeUrl = "http://dbweb5.fnal.gov:8443/mu2edev/hdb/loader"  ## url updataed 2018Feb16
    #self.__productionQueryUrl ="http://ifb-data.fnal.gov:8131/QE/mu2e_hw/app/SQ/query"
    #self.__productionWriteUrl = "http://ifb-data.fnal.gov:8133/mu2e/hdb/loader"

    self.__queryUrl = "http://ifb-data.fnal.gov:9090/QE/hw/app/SQ/query"  ## url updated 2018Feb27
    self.__writeUrl = "https://dbweb5.fnal.gov:8443/hdb/mu2edev/loader"  ## url updataed 2018Feb16
    self.__productionQueryUrl ="http://ifb-data.fnal.gov:9090/QE/hw/app/SQ/query" ## url updated 2018Feb27
    self.__productionWriteUrl = "https://dbweb6.fnal.gov:8443/hdb/mu2e/loader"  ## url updated 2018Apr27 
                                                                                 ## Vladimir's Email 
    #print '==============>>>> databaseConfig -----%s----- \n' % self.__queryUrl
    self.__sipmKey  = ' '
    self.__extrusionKey = ' '
## -------------------------------------------------------------
  def getVersion(self):
    self.__version="2018Feb28"
    return self.__version
## -------------------------------------------------------------
  def setDebugOn(self):
    self.__cmjDebug = 1
    print "..databaseConfig::setDebugOn \n"
## -------------------------------------------------------------
  def setDebugOff(self):
    self.__cmjDebug = 0
    print "..databaseConfig::setDebugOff \n"
## -------------------------------------------------------------
  def getQueryUrl(self):
    if (self.__cmjDebug == 1 ): 
      print '..databaseConfig::getQueryUrl...'
      print '..databaseConfig:self.__queryUrl = %s \n' % self.__queryUrl
    return self.__queryUrl.rstrip()
## -------------------------------------------------------------
  def getWriteUrl(self):
    if (self.__cmjDebug == 1 ): 
      print '..databaseConfig::getWriteUrl...'
      print '..databaseConfig:self.__writeUrl = %s \n' % self.__writeUrl
    return self.__writeUrl
## -------------------------------------------------------------
##  This is the sipm development key
  def getSipmKey(self):
    if (self.__cmjDebug == 1): print 'getSipmKey.... enter'
    self.__sipmKey = ''
    try:
      if (self.__cmjDebug == 1 ): print '..databaseConfig::getSipmKey... before open'
      self.__tempFile=open('../CrvUtilities/86Sipm.txt','r')
      if (self.__cmjDebug == 1): print '..databaseConfig::getSipmKey... after open'
    except Exception as e:
      print 'exception: %s' % e
      print 'file not found: contact database administrators \n'
      print 'the program will run, but in the test mode... \n'
      print 'DATA WILL NOT BE SENT TO THE DATABASE \n'
      return ' '
    if (self.__cmjDebug == 1): print '..databaseConfig::getSipmKey.... enter'
    self.__sipmKey=self.__tempFile.read()
    self.__tempFile.close()
    return self.__sipmKey.rstrip()
## -------------------------------------------------------------
##  This is the extrusion development key
  def getExtrusionKey(self):
    if (self.__cmjDebug == 1): print '..databaseConfig::getExtrusionKey.... enter'
    self.__extrusionKey = ''
    try:
      if (self.__cmjDebug == 1 ): print '..databaseConfig::getExtrusionmKey... before open'
      self.__tempFile=open('../CrvUtilities/86Extrusions.txt','r')
      if (self.__cmjDebug == 1): print '..databaseConfig::getExtrusionKey... after open'
    except Exception as e:
	print 'exception: %s' % e
	print 'file not found: contact database administrators \n'
	print 'the program will run, but in the test mode... \n'
	print 'DATA WILL NOT BE SENT TO THE DATABASE \n'
	return ' '
    if (self.__cmjDebug == 1): print '..databaseConfig::getExtrusionKey.... enter'
    self.__extrusionKey=self.__tempFile.read()
    self.__tempFile.close()
    return self.__extrusionKey.rstrip()
## -------------------------------------------------------------
## -------------  2016 May9 ---- Add Electronics ---------------
## -------------------------------------------------------------
##  This is the electronics development key
  def getElectronicsKey(self):
    if (self.__cmjDebug == 1): print '..databaseConfig::getElectronicsKey.... enter'
    self.__electronicsKey = ''
    try:
      if (self.__cmjDebug == 1 ): print '..databaseConfig::getElectronicsKey... before open'
      self.__tempFile=open('../Utilities/86Electronics.txt','r')
      if (self.__cmjDebug == 1): print '..databaseConfig::getElectronicsKey... after open'
    except Exception as e:
	print 'exception: %s' % e
	print 'file not found: contact database administrators \n'
	print 'the program will run, but in the test mode... \n'
	print 'DATA WILL NOT BE SENT TO THE DATABASE \n'
	return ' '
    if (self.__cmjDebug == 1): print '..databaseConfig::getElectronicsKey.... enter'
    self.__electronicsKey=self.__tempFile.read()
    self.__tempFile.close()
    return self.__electronicsKey.rstrip() 
## -------------------------------------------------------------
## -------------  2016 May9 ---- Add Electronics ---------------
##--------------------------------------------------------------
##
## -------------------------------------------------------------
## -------------  2016 May9 ---- Add Fibers --------------------
## -------------------------------------------------------------
##  This is the fibers development key
  def getFibersKey(self):
    if (self.__cmjDebug == 1): print '..databaseConfig::getFibersKey.... enter'
    self.__fibersKey = ''
    try:
      if (self.__cmjDebug == 1 ): print '..databaseConfig::getFibersKey... before open'
      self.__tempFile=open('../CrvUtilities/86Fibers.txt','r')
      if (self.__cmjDebug == 1): print '..databaseConfig::getFibersKey... after open'
    except Exception as e:
	print 'exception: %s' % e
	print 'file not found: contact database administrators \n'
	print 'the program will run, but in the test mode... \n'
	print 'DATA WILL NOT BE SENT TO THE DATABASE \n'
	return ' '
    if (self.__cmjDebug == 1): print '..databaseConfig::getFibersKey.... enter'
    self.__fibersKey=self.__tempFile.read()
    self.__tempFile.close()
    return self.__fibersKey.rstrip()
## -------------------------------------------------------------
## -------------  2016 May9 ---- Add Fibers --------------------
##--------------------------------------------------------------
##
## -------------------------------------------------------------
## -------------  2016 May9 ---- Add Composite -----------------
## -------------------------------------------------------------
##  This is the composite development key
  def getCompositeKey(self):
    if (self.__cmjDebug == 1): print '..databaseConfig::getCompositeKey.... enter'
    self.__compositeKey = ''
    try:
      if (self.__cmjDebug == 1 ): print '..databaseConfig::getCompositeKey... before open'
      self.__tempFile=open('../CrvUtilities/86Composite.txt','r')
      if (self.__cmjDebug == 1): print '..databaseConfig::getCompositeKey... after open'
    except Exception as e:
	print 'exception: %s' % e
	print 'file not found: contact database administrators \n'
	print 'the program will run, but in the test mode... \n'
	print 'DATA WILL NOT BE SENT TO THE DATABASE \n'
	return ' '
    if (self.__cmjDebug == 1): print '..databaseConfig::getCompositeKey.... enter'
    self.__compositeKey=self.__tempFile.read()
    self.__tempFile.close()
    return self.__compositeKey.rstrip()
## -------------------------------------------------------------
## -------------  2016 May9 ---- Add Composite -----------------
##--------------------------------------------------------------
##
## -------------------------------------------------------------
##--------------------------------------------------------------
## -------------------------------------------------------------
##		Production database accessor functions....
  def getProductionQueryUrl(self):
    if (self.__cmjDebug == 1 ): 
      print '..databaseConfig::getProductionQueryUrl...'
      print '..databaseConfig:self.__productionQueryUrl = %s \n' % self.__productionQueryUrl
    return self.__productionQueryUrl.rstrip()
## -------------------------------------------------------------
  def getProductionWriteUrl(self):
    if (self.__cmjDebug == 1 ): 
      print '..databaseConfig::getProductionWriteUrl...'
      print '..databaseConfig:self.__productionWriteUrl = %s \n' % self.__productionWriteUrl
    return self.__productionWriteUrl.rstrip()
## -------------------------------------------------------------
##  This is the sipm production key
  def getSipmProductionKey(self):
    if (self.__cmjDebug == 1): print 'getSipmProductionKey.... enter'
    self.__sipmKey = ''
    try:
      if (self.__cmjDebug == 1 ): print '..databaseConfig::getSipmProductionKey... before open'
      self.__tempFile=open('../CrvUtilities/86SipmPro.txt','r')
      if (self.__cmjDebug == 1): print '..databaseConfig::getSipmProductionKey... after open'
    except Exception as e:
      print 'exception: %s' % e
      print 'file not found: contact database administrators \n'
      print 'the program will run, but in the test mode... \n'
      print 'DATA WILL NOT BE SENT TO THE DATABASE \n'
      return ' '
    if (self.__cmjDebug == 1): print '..databaseConfig::getSipmProductionKey.... enter'
    self.__sipmKey=self.__tempFile.read()
    self.__tempFile.close()
    return self.__sipmKey.rstrip()
## -------------------------------------------------------------
##  This is the extrusion production key
  def getExtrusionProductionKey(self):
    if (self.__cmjDebug == 1): print '..databaseConfig::getExtrusionProductionKey.... enter'
    self.__extrusionKey = ''
    try:
      if (self.__cmjDebug == 1 ): print '..databaseConfig::getExtrusionmProductionKey... before open'
      self.__tempFile=open('../CrvUtilities/86ExtrusionsPro.txt','r')
      if (self.__cmjDebug == 1): print '..databaseConfig::getExtrusionProductionKey... after open'
    except Exception as e:
	print 'exception: %s' % e
	print 'file not found: contact database administrators \n'
	print 'the program will run, but in the test mode... \n'
	print 'DATA WILL NOT BE SENT TO THE DATABASE \n'
	return ' '
    if (self.__cmjDebug == 1): print '..databaseConfig::getExtrusionKey.... enter'
    self.__extrusionKey=self.__tempFile.read()
    self.__tempFile.close()
    return self.__extrusionKey.rstrip()

## -------------------------------------------------------------
## --- 2016 May9 ---- Add Electronics Production Database ------
## -------------------------------------------------------------
##  This is the electronics production key
  def getElectronicsProductionKey(self):
    if (self.__cmjDebug == 1): print 'getElectronicsProductionKey.... enter'
    self.__electronicsKey = ''
    try:
      if (self.__cmjDebug == 1 ): print '..databaseConfig::getElectronicsProductionKey... before open'
      self.__tempFile=open('../CrvUtilities/86ElectroincsPro.txt','r')
      if (self.__cmjDebug == 1): print '..databaseConfig::getElectronicsProductionKey... after open'
    except Exception as e:
      print 'exception: %s' % e
      print 'file not found: contact database administrators \n'
      print 'the program will run, but in the test mode... \n'
      print 'DATA WILL NOT BE SENT TO THE DATABASE \n'
      return ' '
    if (self.__cmjDebug == 1): print '..databaseConfig::getElectronicsProductionKey.... enter'
    self.__electronicsKey=self.__tempFile.read()
    self.__tempFile.close()
    return self.__electronicsKey.rstrip()
## -------------------------------------------------------------
## --- 2016 May9 ---- Add Electronics Production Database ------
## -------------------------------------------------------------
##
## -------------------------------------------------------------
## --- 2016 May9 ---- Add Fibers Production Database -----------
## -------------------------------------------------------------
##  This is the fibers production key
  def getFibersProductionKey(self):
    if (self.__cmjDebug == 1): print 'getFibersProductionKey.... enter'
    self.__fibersKey = ''
    try:
      if (self.__cmjDebug == 1 ): print '..databaseConfig::getFibersProductionKey... before open'
      self.__tempFile=open('../CrvUtilities/86FibersPro.txt','r')
      if (self.__cmjDebug == 1): print '..databaseConfig::getFibersProductionKey... after open'
    except Exception as e:
      print 'exception: %s' % e
      print 'file not found: contact database administrators \n'
      print 'the program will run, but in the test mode... \n'
      print 'DATA WILL NOT BE SENT TO THE DATABASE \n'
      return ' '
    if (self.__cmjDebug == 1): print '..databaseConfig::getFibersProductionKey.... enter'
    self.__fibersKey=self.__tempFile.read()
    self.__tempFile.close()
    return self.__fibersKey.rstrip()
## -------------------------------------------------------------
## --- 2016 May9 ---- Add Fibers Production Database -----------
## -------------------------------------------------------------
##
## -------------------------------------------------------------
## --- 2016 May9 ---- Add Composite Production Database -----------
## -------------------------------------------------------------
##  This is the fibers production key
  def getCompositeProductionKey(self):
    if (self.__cmjDebug == 1): print 'getCompositeProductionKey.... enter'
    self.__compositeKey = ''
    try:
      if (self.__cmjDebug == 1 ): print '..databaseConfig::getCompositeProductionKey... before open'
      self.__tempFile=open('../CrvUtilities/86CompositePro.txt','r')
      if (self.__cmjDebug == 1): print '..databaseConfig::getCompositeProductionKey... after open'
    except Exception as e:
      print 'exception: %s' % e
      print 'file not found: contact database administrators \n'
      print 'the program will run, but in the test mode... \n'
      print 'DATA WILL NOT BE SENT TO THE DATABASE \n'
      return ' '
    if (self.__cmjDebug == 1): print '..databaseConfig::getCompositeProductionKey.... enter'
    self.__compositeKey=self.__tempFile.read()
    self.__tempFile.close()
    return self.__compositeKey.rstrip()
## -------------------------------------------------------------
## --- 2016 May9 ---- Add Composite Production Database -----------
## ------------------------------------------------------------

