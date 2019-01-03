##Plotting and data verification tools for source QA data
##Written by Ben Barton
##bb6yx@virginia.edu, 99bbarton@gmail.com
##540-355-8918
##10/25/17 - Initial version completed - Untested
##12/07/17 - Fully tested 
##02/08/18 - Added function to re-title histogram
##05/24/18 - Modified renaming function to support multiple operations

import ROOT

##Display canvas object for ROOT 
canvas = None

##Lists to store data
aChannels = []
bChannels = []
allChannels = []
darkChannels = []

##Histogram objects for source QA data plotting
aHist = ROOT.TH1F()
bHist = ROOT.TH1F()
allHist = ROOT.TH1F()
darkHist = ROOT.TH1F()

#----------------------------------------------------------------------------

##Function to assign a list of data to aChannels and format and fill aHist
def setASideObjects(data = []):
    global aChannels, aHist

    aChannels = data

    if len(aChannels) > 0:
        xRange = max(aChannels)-min(aChannels)


        aHist = ROOT.TH1F("A-Side Channels", "Source QA:  A-Side Channels",int(float(xRange)/0.02),min(aChannels)-0.02, max(aChannels) + 0.02)
        
        aHist.SetXTitle("Current (mA)")
        
        for entry in aChannels:
            aHist.Fill(entry)

#-------------------------------------------------------------------------------

##Function to assign a list of data to bChannels and format and fill bHist
def setBSideObjects(data = []):
    global bChannels, bHist

    bChannels = data
 
    if len(bChannels) > 0:
        xRange = max(bChannels)-min(bChannels)

        bHist = ROOT.TH1F("B-Side Channels", "Source QA:  B-Side Channels",int(float(xRange)/0.02),min(bChannels)-0.02, max(bChannels) + 0.02)

        bHist.SetXTitle("Current (mA)")

        for entry in bChannels:
            bHist.Fill(entry)

#-------------------------------------------------------------------------------

##Function to assign data to allChannels and format and fill allHist
def setAllChannelsObjects():
    global aChannels, bChannels, allChannels, allHist
    
    allChannels = aChannels + bChannels
 
    if len(allChannels) > 0:
        xRange = max(allChannels)-min(allChannels)
   
        allHist = ROOT.TH1F("All Channels", "Source QA:  All Channels",int(float(xRange)/0.02),min(allChannels)-0.02,max(allChannels)+0.02)
        
        allHist.SetXTitle("Current (mA)")

        for entry in allChannels:
            allHist.Fill(entry)

#-------------------------------------------------------------------------------

##Function to assign a list of data to darkChannels and format and fill darkHist
def setDarkObjects(data = []):
    global darkChannels, darkHist

    darkChannels = data

    if len(darkChannels) > 0:
        darkHist = ROOT.TH1F("Dark Current", "Source QA: Dark Current",int((max(darkChannels)-min(darkChannels))/0.02),min(darkChannels)-0.02,max(darkChannels)+0.02)
        darkHist.SetXTitle("Current (mA)")

        for entry in darkChannels:
            darkHist.Fill(entry)

#-------------------------------------------------------------------------------

##Function to initialize a new canvas
def initializeCanvas(name,title):
    global canvas
    canvas = ROOT.TCanvas(name,title,1)

#-------------------------------------------------------------------------------

##Function to look for and flag obviously false data values (e.g. negative current) in the lines of
##read from a file in the database upload format
##Returns a list of lines which contain bad data
def flagBadData(fileLines):
    badDataLines = []


    for lnNum in range(len(fileLines)):
        data = fileLines[lnNum].split(",")[7:16]

        for val in data:

            if float(val) < 0 or float(val) > 2:
                badDataLines.append(lnNum)

    return badDataLines
            
#-------------------------------------------------------------------------------

##Function to make a histogram of source QA data
def plotSourceQAData(hist, canvPad = 1):
    global canvas

    canvas.cd(canvPad)

    hist.Draw()
    canvas.Update()

#------------------------------------------------------------------------------

##Function to plot histograms for all lists of data (all, dark, A, B)
def plotAllSourceQAData():
    global aHist, bHist, allHist, darkHist, canvas

    canvas.Divide(2,2)

    plotSourceQAData(allHist, 1)
    plotSourceQAData(darkHist, 2)
    plotSourceQAData(aHist, 3)
    plotSourceQAData(bHist, 4)

#------------------------------------------------------------------------------

##Function to rename a histogram
def renameHistograms():
    global canvas

    while True:
        print "Would you like to re-title a histogram?"
        print "Note: Histograms on multi-histogram canvasses will not be re-titled"
        print 'Enter "A", "B", "All", or "Dark", or hit "Enter" to skip: '
        choice = raw_input();

        if choice == "":
            break
    
        print 'Enter a new title for ' + choice + ':'
        title = raw_input();

        if choice.upper() == "A":
            aHist.SetNameTitle("A-side Channels", title)
        elif choice.upper() == "B":
            bHist.SetNameTitle("B-side Channels", title)
        elif choice.upper() == "ALL":
            allHist.SetNameTitle("All Channels", title)
        elif choice.upper() == "DARK":
            darkHist.SetNameTitle("Dark Current", title)
        else:
            print "Using default titles\n"
        
    canvas.Update()

#------------------------------------------------------------------------------

##Function to destroy/close ROOT histogram and canvas objects
def cleanRootObjects():
    global aHist, bHist, allHist, darkHist, canvas

    del(aHist)
    del(bHist)
    del(allHist)
    del(darkHist)
    
    canvas.Close()

#-------------------------------------------------------------------------------
