import sys
import os

if len(sys.argv) != 3:
    print("Two arguments are required:")
    print("   "+sys.argv[0]+" <transmitter drive letter> <destination directory>")
    exit(1)

txDrive = sys.argv[1]
dstDir = sys.argv[2]

txDrive = txDrive[0]+":"

print("Copying '"+txDrive+"' -> '"+dstDir+"'")

txModelsDir = os.path.join(txDrive, "models")

#f=open("guru99.txt", "r")
for f in os.listdir(txModelsDir):
    print(f)
