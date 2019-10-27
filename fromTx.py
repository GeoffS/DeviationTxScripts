import sys
import os

# returns total as checksum
# input - string
def checksum(st):
    return reduce(lambda x,y:x+y, map(ord, st))

def checksumFile(fname):
    with open(fname, 'r') as file:
        return checksum(file.read())

if len(sys.argv) != 3:
    print("Two arguments are required:")
    print("   "+sys.argv[0]+" <transmitter drive letter> <destination directory>")
    exit(1)

txDrive = sys.argv[1]
dstDir = sys.argv[2]

txDrive = txDrive[0]+":"

print("Copying '"+txDrive+"' -> '"+dstDir+"'")

txModelsDir = os.path.join(txDrive, "models")

defaultModelName = os.path.join(txModelsDir, "default.ini")
defaultFileCkSum = 0
if os.path.exists(defaultModelName):
    defaultFileCkSum = checksumFile(defaultModelName)
print("default.ini checksum = "+str(defaultFileCkSum))

#f=open("guru99.txt", "r")
for fName in os.listdir(txModelsDir):
    print(fName)
    fullPath = os.path.join(txModelsDir, fName)
    if fName.startswith("model") & fName.endswith(".ini"):
        modelNumStr = (fName[5:])[:-4]
        #print("   "+modelNumStr)

        if(checksumFile(fullPath) == defaultFileCkSum):
            print("   Identical to default file.")
            continue

        with open(fullPath, 'r') as f:
            lines = f.readlines()
            if lines[0].startswith("name="):
                modelName = (lines[0][5:])[:-1]
            else:
                modelName = fName
                print("   WARNING: no 'name=' first line in '"+fName+"'")
