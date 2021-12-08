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

# Creates changelog file.
if exists("changelog.txt"):
    os.remove("changelog.txt")
changelog = open("changelog.txt", "w+")

# Recursively searches through files in directory.
def seek(filepath):
    for file in glob.iglob(f'{filepath}/*'):
        # Runs function recursively if file is a directory.
        if (os.path.isdir(file)):
            seek(file)
        else:
            # If file doesnt exist, removes it from the dict.
            if (not(exists(file))):
                changelog.write(str(file) + "does not exist anymore.\n")
                if str(file) in oldData:
                    oldData.pop(str(file))
                continue
            
            # Gets permissions from file.
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

            # Gets size of file.
            size = str(os.lstat(file).st_size)

            # Converts filename to string
            strFile = str(file)

            # If the file existed in the previous startup, checks if file size and/or permissions have changed and updates changelog if so.
            if strFile in oldData:
                if (size != oldData[strFile][1]):
                    changelog.write("Size changed from " + str(oldData[strFile][1]) + " bytes to " + size + " bytes for file: " + strFile + ".\n")
                    oldData[strFile][1] = size
                if (accesses != oldData[strFile][0]):
                    changelog.write("Permissions changed from " + str(oldData[strFile][0]) + " to " + accesses + " for file: " + strFile + ".\n")
                    oldData[strFile][0] = accesses
            else:
                # If the file did not exist in the previous startup, adds it to the list and updates the changelog.
                changelog.write(strFile + " has been created with    permissions: " + accesses + "    and size: " + size + ".\n")
                oldData[strFile] = [accesses, size]

# Runs the recursive function.
seek(home)

# Closes the changelog file.
changelog.close()

# Updates the files text file.
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