#Read in a module layout spreadsheet and a module electronics spreadsheet and combine into a single file for database upload
#Ben Barton
#bb6yx@virginia.edu
#06/20


import sys

DEBUG = False #If true, will print out the module layout and electronics information to the console

#############################################################################################################################3
## A class to read in, manipulate, and output module layouts 
class ModuleLayout:
    def __init__(self, side, offset = True):
        self.side = side #A or B
        self.offset = offset #Whether the module is offset
        self.mID = "" #Module ID e.g. crvmod-101
        self.mType = "" #Type of module e.g. right
        self.date = ""
        self.location = ""
        self.width = -9999
        self.length = -9999
        self.thick = -9999
        self.epoxy = -9999
        self.flatness = -9999
        self.al = ""
        self.comments = ""
        self.layer1 = [] #Numbered from top down
        self.layer2 = []
        self.layer3 = []
        self.layer4 = []
    #----------------------------------------------------------------------------

    #Read a layout csv file and fill the class attributes
    def readFile(self, filename):
       inFile = open(filename, "r")
       lines = inFile.readlines()

       #Read in all the module info separately in case its useful ever
       self.mID = lines[0].split(",")[1]

       if len(self.mID) == 3:
           self.mID = "crvmod-" + self.mID

       self.mType = lines[1].split(",")[1]
       self.date = lines[2].split(",")[1]
       self.location = lines[3].split(",")[1]
       self.width = lines[4].split(",")[1]
       self.length = lines[5].split(",")[1]
       self.thick = lines[6].split(",")[1]
       self.epoxy = lines[7].split(",")[1]
       self.flatness = lines[8].split(",")[1]
       self.al = lines[9].split(",")[1]
       self.comments = lines[10].split(",")[1]

       if len(self.mID) < 10: #Should always be the form of crvmod-1##
            print "\nWARNING: Module ID from layout file is incorrect"
       if len(self.mType) == 0: 
            print "\nWARNING: Module type from layout file is incorrect"
            

       lines = lines[10:] #Don't scan lines already read above
       
       for line in lines:
           splitLine = line.split(",")
           key = splitLine[0]

           if key == "layer1":
               for cell in splitLine[1:]:
                   if cell != "":
                       self.layer1.append(cell)
               self.layer1[-1] = self.layer1[-1][:-2] # Remove return/newline characters
           elif key == "layer2":
               for cell in splitLine[1:]:
                   if cell != "" and cell != "\r\n" and cell != "\n":
                       self.layer2.append(cell)
           elif key == "layer3":
               for cell in splitLine[1:]:
                   if cell != "" and cell != "\r\n" and cell != "\n":
                       self.layer3.append(cell)
           elif key == "layer4":
               for cell in splitLine[1:]:
                   if cell != "" and cell != "\r\n" and cell != "\n":
                       self.layer4.append(cell)
           else:
               continue

    #-------------------------------------------------------------------------

    #Reverse the layout so it corresponds to the opposite side view
    def flipSide(self):
        if self.side == "A":
            self.side = "B"
        elif self.side == "B":
            self.side = "A"
        else:
            print "\nWARNING: Side specifier is unrecognized. Must be A or B."
            return

        for i in range(4):
            tmp = self.layer1[i]
            self.layer1[i] = self.layer1[7 - i]
            self.layer1[7 - i] = tmp
            tmp = self.layer2[i]
            self.layer2[i] = self.layer2[7 - i]
            self.layer2[7-i] = tmp
            tmp = self.layer3[i]
            self.layer3[i] = self.layer3[7 - i]
            self.layer3[7-i] = tmp
            tmp = self.layer4[i]
            self.layer4[i] = self.layer4[7 - i]
            self.layer4[7-i] = tmp
            
    #------------------------------------------------------------------------
        
    #Print the layout of the module
    def printLayout(self):
        print "\nLayout of module " + self.mID + " as viewed from side " + self.side
        print self.layer1
        print self.layer2
        print self.layer3
        print self.layer4

    #------------------------------------------------------------------------


##################################################################################################################

##A Class to read in and manipulate SMB files 
class ModuleElectronics:
    
    def __init__(self, offset = True):
        self.mID = ""
        self.mType = ""
        self.comments = ""
        self.offset = offset

        self.electronics = {"SMB-L1-A": [],
                         "SipmId-L1-A" : [],
                         "CmbId-L1-A" : [],
                         "SMB-L2-A": [],
                         "SipmId-L2-A" : [],
                         "CmbId-L2-A" : [],
                         "SMB-L3-A": [],
                         "SipmId-L3-A" : [],
                         "CmbId-L3-A" : [],
                         "SMB-L4-A": [],
                         "SipmId-L4-A" : [],
                         "CmbId-L4-A" : [],
                         "SMB-L1-B": [],
                         "SipmId-L1-B" : [],
                         "CmbId-L1-B" : [],
                         "SMB-L2-B": [],
                         "SipmId-L2-B" : [],
                         "CmbId-L2-B" : [],
                         "SMB-L3-B": [],
                         "SipmId-L3-B" : [],
                         "CmbId-L3-B" : [],
                         "SMB-L4-B": [],
                         "SipmId-L4-B" : [],
                         "CmbId-L4-B" : []}
        
    #-----------------------------------------------------------------------------------------               
                         
    #Read in a file and fill layers - requires that key values are in the file
    def readFile(self, filename):
        inFile = open(filename, "r")
        lines = inFile.readlines()

        self.mID = lines[0].split(",")[2]

        if len(self.mID) == 3:
           self.mID = "crvmod-" + self.mID

        self.mType = lines[1].split(",")[2]

        if len(self.mID) < 10: #Should always be the form of crvmod-1##
            print "\nWARNING: Module ID from electronics file is incorrect"

        
        lnNum = 0
        for line in lines: #Ignore the header lines
            if lnNum < 12:
                lnNum += 1
                continue
            else:
                lnNum += 1

            cols = line.split(",")
            if self.electronics.get(cols[0]) != None: #Skip lines that don't contain electronics info
                ind = 1 # Skip the key column
                while ind < len(cols):
                    if cols[ind] == "" or cols[ind] == "\n" or cols[ind] == "\r\n": #Only read in the electronics info
                        ind += 1
                        continue
                    else:
                        if cols[ind].find("\n") > 0: #Remove new lines, etc
                            cols[ind] = cols[ind][:-1]
                        if cols[ind].find("\r") > 0:
                            cols[ind] = cols[ind][:-1]
                        self.electronics.get(cols[0]).append(cols[ind])
                        ind += 1
                if len(self.electronics.get(cols[0])) % 4 != 0: #There should be 4, 8, or 16 entries in a complete row, depending on type

	                  if self.electronics.get(cols[0])[0] == "A"  or self.electronics.get(cols[0])[0] == "B":
			                  self.electronics[cols[0]].pop(0)
		                else:
	       		            print "\nWARNING: " + cols[0] + " contains " + str(len(self.electronics.get(cols[0]))) + " entries"
		    

    #-----------------------------------------------------------------------------------------

    #Print out the electronics layout
    def printElectronics(self):
        print "\n\nElectronics information for module " + self.mID + ":\n"

        print "Side A:"
        print "SMB-L1 - " + str(self.electronics["SMB-L1-A"])
        print "CMB-L1 - " + str(self.electronics["CmbId-L1-A"])
        print "SiPMs-L1 - " + str(self.electronics["SipmId-L1-A"])
        print "SMB-L2 - " + str(self.electronics["SMB-L2-A"])
        print "CMB-L2 - " + str(self.electronics["CmbId-L2-A"])
        print "SiPMs-L2 - " + str(self.electronics["SipmId-L2-A"])
        print "SMB-L3 - " + str(self.electronics["SMB-L3-A"])
        print "CMB-L3 - " + str(self.electronics["CmbId-L3-A"])
        print "SiPMs-L3 - " + str(self.electronics["SipmId-L3-A"])
        print "SMB-L4 - " + str(self.electronics["SMB-L4-A"])
        print "CMB-L4 - " + str(self.electronics["CmbId-L4-A"])
        print "SiPMs-L4 - " + str(self.electronics["SipmId-L4-A"])

        print "\nSide B:"
        print "SMB-L1 - " + str(self.electronics["SMB-L1-B"])
        print "CMB-L1 - " + str(self.electronics["CmbId-L1-B"])
        print "SiPMs-L1 - " + str(self.electronics["SipmId-L1-B"])
        print "SMB-L2 - " + str(self.electronics["SMB-L2-B"])
        print "CMB-L2 - " + str(self.electronics["CmbId-L2-B"])
        print "SiPMs-L2 - " + str(self.electronics["SipmId-L2-B"])
        print "SMB-L3 - " + str(self.electronics["SMB-L3-B"])
        print "CMB-L3 - " + str(self.electronics["CmbId-L3-B"])
        print "SiPMs-L3 - " + str(self.electronics["SipmId-L3-B"])
        print "SMB-L4 - " + str(self.electronics["SMB-L4-B"])
        print "CMB-L4 - " + str(self.electronics["CmbId-L4-B"])
        print "SiPMs-L4 - " + str(self.electronics["SipmId-L4-B"])
        print "\n"
        
    #-----------------------------------------------------------------------------------------
        
####################################################################################################################

#Take in a module layout and electronics objects and merge them into a single output file
def mergeLayoutElectronics(layout, elect, filename):
    
    outfile = open(filename, "w")

    if layout.mID != elect.mID:
        print "\nWARNING: Module IDs do not match\n"
    if layout.mType != elect.mType:
        print "\nWARNING: Module type do not match\n"

    if layout.side == "B": #Always start with side A for code simplicity's sake
        layout.flipSide()

    #Write out module identification information
    outfile.write("Module_Id," + layout.mID + ",\n")
    outfile.write("Module_Type," + layout.mType + ",\n\n")

    
    #The [1:1].replace(" ","").replace("'","") removes the ', space, and bracket artifacts from using the default list __str__() methods
    #Using the defaults is equally efficient on this scale and simplifies the code massively.

    #Output A-side information
    outfile.write("view_from,A,\n")
    outfile.write("Layer-1-A," + str(layout.layer1)[1:-1].replace(" ","").replace("'","") + ",\n")
    outfile.write("SMB-L1-A," + str(elect.electronics["SMB-L1-A"])[1:-1].replace(" ","").replace("'","") + ",\n")
    outfile.write("CmbId-L1-A," + str(elect.electronics["CmbId-L1-A"])[1:-1].replace(" ","").replace("'","") + ",\n")
    outfile.write("SipmId-L1-A," + str(elect.electronics["SipmId-L1-A"])[1:-1].replace(" ","").replace("'","") + ",\n")
    
    outfile.write("Layer-2-A," + str(layout.layer2)[1:-1].replace(" ","").replace("'","") + ",\n")
    outfile.write("SMB-L2-A," + str(elect.electronics["SMB-L2-A"])[1:-1].replace(" ","").replace("'","") + ",\n")
    outfile.write("CmbId-L2-A," + str(elect.electronics["CmbId-L2-A"])[1:-1].replace(" ","").replace("'","") + ",\n")
    outfile.write("SipmId-L2-A," + str(elect.electronics["SipmId-L2-A"])[1:-1].replace(" ","").replace("'","") + ",\n")

    outfile.write("Layer-3-A," + str(layout.layer3)[1:-1].replace(" ","").replace("'","") + ",\n")
    outfile.write("SMB-L3-A," + str(elect.electronics["SMB-L3-A"])[1:-1].replace(" ","").replace("'","") + ",\n")
    outfile.write("CmbId-L3-A," + str(elect.electronics["CmbId-L3-A"])[1:-1].replace(" ","").replace("'","") + ",\n")
    outfile.write("SipmId-L3-A," + str(elect.electronics["SipmId-L3-A"])[1:-1].replace(" ","").replace("'","") + ",\n")

    outfile.write("Layer-4-A," + str(layout.layer4)[1:-1].replace(" ","").replace("'","") + ",\n")
    outfile.write("SMB-L4-A," + str(elect.electronics["SMB-L4-A"])[1:-1].replace(" ","").replace("'","") + ",\n")
    outfile.write("CmbId-L4-A," + str(elect.electronics["CmbId-L4-A"])[1:-1].replace(" ","").replace("'","") + ",\n")
    outfile.write("SipmId-L4-A," + str(elect.electronics["SipmId-L4-A"])[1:-1].replace(" ","").replace("'","") + ",\n")

    outfile.write("\n")
    #Write B-side information
    layout.flipSide()
    outfile.write("view_from,B,\n")
    outfile.write("Layer-1-B," + str(layout.layer1)[1:-1].replace(" ","").replace("'","") + ",\n")
    outfile.write("SMB-L1-B," + str(elect.electronics["SMB-L1-B"])[1:-1].replace(" ","").replace("'","") + ",\n")
    outfile.write("CmbId-L1-B," + str(elect.electronics["CmbId-L1-B"])[1:-1].replace(" ","").replace("'","") + ",\n")
    outfile.write("SipmId-L1-B," + str(elect.electronics["SipmId-L1-B"])[1:-1].replace(" ","").replace("'","") + ",\n")
    
    outfile.write("Layer-2-B," + str(layout.layer2)[1:-1].replace(" ","").replace("'","") + ",\n")
    outfile.write("SMB-L2-B," + str(elect.electronics["SMB-L2-B"])[1:-1].replace(" ","").replace("'","") + ",\n")
    outfile.write("CmbId-L2-B," + str(elect.electronics["CmbId-L2-B"])[1:-1].replace(" ","").replace("'","") + ",\n")
    outfile.write("SipmId-L2-B," + str(elect.electronics["SipmId-L2-B"])[1:-1].replace(" ","").replace("'","") + ",\n")

    outfile.write("Layer-3-B," + str(layout.layer3)[1:-1].replace(" ","").replace("'","") + ",\n")
    outfile.write("SMB-L3-B," + str(elect.electronics["SMB-L3-B"])[1:-1].replace(" ","").replace("'","") + ",\n")
    outfile.write("CmbId-L3-B," + str(elect.electronics["CmbId-L3-B"])[1:-1].replace(" ","").replace("'","") + ",\n")
    outfile.write("SipmId-L3-B," + str(elect.electronics["SipmId-L3-B"])[1:-1].replace(" ","").replace("'","") + ",\n")

    outfile.write("Layer-4-B," + str(layout.layer4)[1:-1].replace(" ","").replace("'","") + ",\n")
    outfile.write("SMB-L4-B," + str(elect.electronics["SMB-L4-B"])[1:-1].replace(" ","").replace("'","") + ",\n")
    outfile.write("CmbId-L4-B," + str(elect.electronics["CmbId-L4-B"])[1:-1].replace(" ","").replace("'","") + ",\n")
    outfile.write("SipmId-L4-B," + str(elect.electronics["SipmId-L4-B"])[1:-1].replace(" ","").replace("'","") + ",")
    
    outfile.close()

 #-------------------------------------------------------------------------------------------


 #Driver function
def main(argv):


    filename_layout = ""
    side = ""
    offset = True
    filename_electronics = ""
    if len(argv) == 5:
        filename_layout = argv[1]
        side = argv[2]
        offset = argv[3]
        filename_electronics = argv[4]
    else:
        filename_layout = raw_input("Filename of layout file: ")
        side = raw_input("From which side is the layout viewed from (A/B): ").upper()
        choice = raw_input("Is the module offset (Y/N):").upper()
        if choice == "Y":
            offset = True
        else:
            offset = False
        filename_electronics = raw_input("Filename of electronics file: ")

    layout = ModuleLayout(side, offset)
    layout.readFile(filename_layout)
    if DEBUG:
        layout.printLayout()
    
    electronics = ModuleElectronics(offset)
    electronics.readFile(filename_electronics)
    if DEBUG:
        electronics.printElectronics()
    
    filename_output = raw_input("Enter a filename for the merged output: ")
    mergeLayoutElectronics(layout, electronics, filename_output)

#---------------------------------------------------------------------------------------------
            
if __name__ == "__main__":
    main(sys.argv)
