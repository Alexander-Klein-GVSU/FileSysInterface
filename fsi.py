import os
from os.path import exists
from os.path import expanduser
import glob
from stat import *

# Name: Alexander Klein
# Date: 12/7/21
# Assignment: File System Interface

# Opens text file and separates data.
oldFile = open("files.txt", "a+")
ofText = oldFile.read()
oldFile.close()
oldData = ofText.splitlines()
for i in range(len(oldData)):
    oldData[i] = oldData[i].split("#")
print(oldData)


# Gets user directory.
home = expanduser("~")

# Recursively searches through files in directory.
def seek(filepath):
    for file in glob.iglob(f'{filepath}/*'):
        if (os.path.isdir(file)):
            seek(file)
        else:
            
            if (not(exists(file))):
                print(str(file) + "does not exist anymore")
                if str(file) in oldData:
                    oldData.remove(str(file))
                continue
            accesses = ""
            if (not(os.access(file, os.R_OK)) and not(os.access(file, os.W_OK)) and not(os.access(file, os.X_OK))):
                accesses += "N/A"
            else:
                if (os.access(file, os.R_OK)):
                    accesses += "r"
                if (os.access(file, os.W_OK)):
                    accesses += "w"
                if (os.access(file, os.X_OK)):
                    accesses += "e"
            size = str(os.lstat(file).st_size)
            strFile = str(file)
            if strFile in oldData:
                if (size != oldData[oldData.index(strFile)][2]):
                    print("Size changed from " + str(oldData[oldData.index(strFile)][2]) + " bytes to " + size + " bytes for file: " + strFile)
                    oldData[oldData.index(strFile)][2] = size
                if (accesses == oldData[oldData.index(strFile)][1]):
                    print("Permissions changed from " + str(oldData[oldData.index(strFile)][1]) + " to " + accesses + " for file: " + strFile)
                    oldData[oldData.index(strFile)][1] = accesses
            else:
                print(strFile + "has been created with permissions: " + accesses + "    and size: " + size)
                oldData.append([strFile, accesses, size])


seek(home)
os.remove("files.txt")
newFile = open("files.txt", "w")
for i in range(len(oldData)):
    for j in range(len(oldData[i])):
        newFile.write(oldData[i][j])
        newFile.write("#")
    newFile.write("\n")
newFile.close()