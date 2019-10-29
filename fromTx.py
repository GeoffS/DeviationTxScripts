import sys
import os

# returns total as checksum
# input - string
def checksum(st):
    return reduce(lambda x,y:x+y, map(ord, st))

def checksumFile(fname):
    with open(fname, 'r') as file:
        return checksum(file.read())

def copyFileWithoutTrailingNulls(contents, dstDir, outputFileName):
    firstNullPos = contents.find('\0')
    #print("First NULL Position = "+str(firstNullPos))

    for char in contents[firstNullPos:]:
        if(char != '\0'):
            print("ERROR: Found non-NULL character after the first-NULL-position.")
            return False

    outputFullPath = os.path.join(dstDir, outputFileName)
    with open(outputFullPath, "w") as fOut:
        fOut.write(contents[0:firstNullPos])

#======================================================================
# Main script body:

if len(sys.argv) != 3:
    print("Two arguments are required:")
    print("   "+sys.argv[0]+" <transmitter drive letter> <destination directory>")
    exit(1)

txDrive = sys.argv[1]
dstDir = sys.argv[2]

txDrive = txDrive[0]+":"

print("Copying Files From '"+txDrive+"' to '"+dstDir+"'\n")

txModelsDir = os.path.join(txDrive, "models")

defaultFilename = "default.ini"

defaultModelName = os.path.join(txModelsDir, defaultFilename)
defaultFileCkSum = 0
if os.path.exists(defaultModelName):
    with open(defaultModelName, 'r') as fIn:
        defaultContents = fIn.read()
        print("Copying File '"+defaultFilename+"'")
        with open(os.path.join(dstDir, defaultFilename), "w") as fOut:
            fOut.write(defaultContents)
        defaultFileCkSum = checksum(defaultContents)
#print("default.ini checksum = "+str(defaultFileCkSum))

for fName in os.listdir(txModelsDir):
    #print(fName)
    fullPath = os.path.join(txModelsDir, fName)
    if fName.startswith("model") & fName.endswith(".ini"):
        baseName = fName[:-4]
        modelNum = int((fName[5:])[:-4])

        with open(fullPath, 'r') as f:
            contents = f.read()

            if(checksum(contents) == defaultFileCkSum):
                #print("   Identical to default file. No processing.")
                continue

            outputFileName = baseName

            if contents.startswith("name="):
                nlPos = contents.find("\n", 5, 100)
                modelName = contents[5:nlPos]
                #print("Model name = '"+modelName+"'")
                outputFileName = baseName+"_"+modelName
            else:
                print("   WARNING: no 'name=' first line in '"+fName+"'")

            outputFileName += ".ini"
            print("Copying File '"+fName+"' -> '"+outputFileName+"'")

            copyFileWithoutTrailingNulls(contents, dstDir, outputFileName)
            # firstNullPos = contents.find('\0')
            # #print("First NULL Position = "+str(firstNullPos))
            #
            # continueProcessing = True
            # for char in contents[firstNullPos:]:
            #     if(char != '\0'):
            #         print("ERROR: Found non-NULL character after the first-NULL-position.")
            #         continueProcessing = False
            #         break
            #
            # if continueProcessing:
            #     outputFullPath = os.path.join(dstDir, outputFileName)
            #     with open(outputFullPath, "w") as fOut:
            #         fOut.write(contents[0:firstNullPos])

print("\nDone!")
