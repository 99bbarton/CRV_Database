#Format cosmic test stand data for database upload
#
#Ben Barton
#bb6yx@virginia.edu, 99bbarton@gmail.com
#540-355-8918
#
#Aug, 2020


import sys
sys.path.append("../CrvUtilities/")
import DatabaseQueryTool

#-------------------------------------------------------------------------------------------------------------

#Read the contents of the cosmic test stand datafile
def readFile(filename):
    with open(filename, "r") as inFile:
        lines = inFile.readlines()
    return lines

#---------------------------------------------------------------------------------------------------------------


#Get dicounter IDs and their positions of a module from the database
def getDicounterInfo(moduleID):
    
    fetchCondition = "module_id:eq:crvmod-" + moduleID
    columns = "module_layer,layer_position,di_counter_id"
    order = columns
    print "Querying database..."
    results = DatabaseQueryTool.query("mu2e_hardware_prd", "di_counters",columns, fetchCondition, order)

    return results
#----------------------------------------------------------------------------------------------------------------

#Given an input layer and position in layer from data file, return a touple with the same values in the database label system
def convertPosSystems(layer, pos):
    layer_db = str(5 - int(layer[-1:])) #1->4, 2->3, 3->2, 4->1

    #Because dicounter positions correspond to whichever perspective the layout spreadsheets use (view from "A" or "B")
    #We do not need to account for the module type when calculating the dicounter position in layer
    pos_db = str(8 - int(pos)) #Reverse the positions and map to [0,7]

    return (layer_db, pos_db)
    
#----------------------------------------------------------------------------------------------------------------
    

#Replace dicounter positions in the first column of the input file with dicounter IDs and write to an output file
def writeDicounterIDs(fileLines, dicounterInfo, moduleID):

    with open("crvmod-" + moduleID + "_cosmicTests.csv","w") as outFile:


        for line in fileLines:
            splitLine = line.split(",")
            pos_raw = splitLine[0]

            #Need to convert the dicounter position in the input file to the system used by the database to
            pos_db = convertPosSystems(pos_raw.split("_")[0], pos_raw.split("_")[1])

            #This is innefficient but since we're only doing it for 32 dicounters, we don't care and simple is better
            diID = ""
            for diInfo in dicounterInfo:
                splitInfo = diInfo.split(",")

                if pos_db[0] == splitInfo[0][-1:] and pos_db[1] == splitInfo[1]: #If layer and pos in layer  match
                    diID = splitInfo[2]
                    break
                
            

            outFile.write(diID + line[3:])


#------------------------------------------------------------------------------------------------------------------------
                    
            
#Will accept command line parameters in the form "python formatter_cosmicTests.py <inputFileName> <moduleIDnumber>
#or will prompt user for those values
def main(argv):
    mID = ""
    filename = ""
    
    if len(argv) == 3:
        filename = argv[1]
        mID = argv[2]
    else:
        filename = raw_input("Enter the path/name of the file: ")
        mID = raw_input("Enter the module ID number (e.g. 101): ")

    fileLines = readFile(filename)
    dicounterInfo = getDicounterInfo(mID)
    
    writeDicounterIDs(fileLines, dicounterInfo, mID)

#------------------------------------------------------------------------------------------------------------------------

if __name__ == "__main__":
    main(sys.argv)
    
