
import numpy as np
from pyrsistent import m
import os
from tqdm import tqdm 

finalLength = 128

#ifile = open("JASPAR2022_CORE_vertebrates_non-redundant_v2.meme", 'r')

testPath = '../motif_databases/JASPAR/'

fileNames = next(os.walk(testPath))[2]
#fileNames = ["JASPAR2022_CORE_vertebrates_non-redundant_v2.meme"]

#print(fileNames)


def getProbabilities():
    x = np.random.rand(4)
    x = x / sum(x)
    return x

def isInteger(integer):
    try:
        eval(integer)
        return True
    except:
        return False



def processMotif(ifile, totMotif):
    #Gets name of motif
    motifName = ifile.readline()
    if (motifName == "\n" or motifName == ""):
        return False
    motifName = motifName.split(" ")[1]
    #Gets the length of motif
    totLen = ifile.readline()
    if (totLen == "" or totLen == "\n"):
        totLen = ifile.readline()
    totLen = int(totLen.split(" ")[5])

    retMotif = []
    #Loops through the next totLen lines, reading in each position and adding noise
    for i in range(totLen):
        pos = ifile.readline().strip().split(" ")
        pos = list(filter(isInteger, pos))
        try:
            
            retMotif += [list(map(lambda x : eval(x), pos))]
            a, c, t, g = getProbabilities()
            retMotif[-1][0] = (retMotif[-1][0] + a) / 2
            retMotif[-1][1] = (retMotif[-1][1] + c) / 2
            retMotif[-1][2] = (retMotif[-1][2] + t) / 2
            retMotif[-1][3] = (retMotif[-1][3] + g) / 2
        except:
            #We will only enter here if there is an error
            print("ERROR")
            print(pos)
            print(eval(pos[0]))
            print(eval(pos[1]))
            print(eval(pos[2]))
            print(eval(pos[3]))
            return
        #Insert processes
    totMotif += [retMotif]
    #Processes rest to prepare for next motif read
    test = ifile.readline()
    if (test == "" or test == "\n"):
        ifile.readline()
    ifile.readline()
    #Returns whether the process was sucessful
    return True



def processFile(ifile, totMotif):
    #Burns the first lines
    beginBurn = ifile.readline()
    while (beginBurn != "Background letter frequencies\n" and beginBurn != "Background letter frequencies (from uniform background):\n"):
        beginBurn = ifile.readline()
    #This would read the specific letter frequences
    ifile.readline() 
    test = ifile.readline() #blank line
    #Processes the motif
    status = processMotif(ifile, totMotif)
    #While we still have motifs, we continue looping through
    while(status):
        status = processMotif(ifile, totMotif)


def main():
    #We loop through all the possible files
    totMotif = []
    for n, fileName in tqdm(enumerate(fileNames), total = len(fileNames)):
        path = testPath + fileName
        ifile = open(path, 'r')
        processFile(ifile, totMotif)
    print(len(totMotif))

main()