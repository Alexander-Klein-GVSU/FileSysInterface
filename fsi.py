import os
from os.path import exists
from os.path import expanduser
import glob
from stat import *

# Name: Alexander Klein
# Date: 12/7/21
# Assignment: File System Interface

# Opens text file and separates data.
if exists("files.txt"):
    oldFile = open("files.txt", "r")
    ofText = oldFile.read()
    oldFile.close()
    oldDataT = ofText.splitlines()
    oldData = {}
    for i in range(len(oldDataT)):
        oldDataT[i] = oldDataT[i].split("#")
        oldData[oldDataT[i][0]] = [oldDataT[i][1], oldDataT[i][2]]
else:
    oldData = {}


# Gets user directory.
home = expanduser("~")
home = "C:/Users/The Dragon Of Light/Desktop/"

# Creates changelog file.
if exists("changelog.txt"):
    os.remove("changelog.txt")
changelog = open("changelog.txt", "w+")

# Recursively searches through files in directory.
def seek(filepath):
    for file in glob.iglob(f'{filepath}/*'):
        if (os.path.isdir(file)):
            seek(file)
        else:
            if (not(exists(file))):
                print(str(file) + "does not exist anymore")
                if str(file) in oldData:
                    oldData.pop(str(file))
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
                if (size != oldData[strFile][1]):
                    changelog.write("Size changed from " + str(oldData[strFile][1]) + " bytes to " + size + " bytes for file: " + strFile + "\n")
                    oldData[strFile][1] = size
                if (accesses != oldData[strFile][0]):
                    changelog.write("Permissions changed from " + str(oldData[strFile][0]) + " to " + accesses + " for file: " + strFile + "\n")
                    oldData[strFile][0] = accesses
            else:
                changelog.write(strFile + " has been created with    permissions: " + accesses + "    and size: " + size + "\n")
                oldData[strFile] = [accesses, size]


seek(home)
changelog.close()
if exists("files.txt"):
    os.remove("files.txt")
newFile = open("files.txt", "w")
for fileName in oldData:
    newFile.write(fileName)
    newFile.write("#")
    for j in range(len(oldData[fileName])):
        newFile.write(oldData[fileName][j])
        newFile.write("#")
    newFile.write("\n")
newFile.close()