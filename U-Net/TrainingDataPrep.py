#Ryan Wang @2022-06-21
#Success and Fail represents how many attempts were successful - does not mean program actually succeeded or failed


import numpy as np
from pyrsistent import m
import os
from tqdm import tqdm 

#np.random.seed(0) #Debugging purposes

finalLength = 128
generateNumSequence = 80000
maxMotifsPerSequence = 4
noiseImpact = 0.8 #Higher the noise impact, the higher the noise
motifDistance = 10#We assume motifs are usually more than 10 base pairs apart

#ifile = open("JASPAR2022_CORE_vertebrates_non-redundant_v2.meme", 'r')

testPath = '../motif_databases/JASPAR/'

PWMFileName = './PWMOut.txt'
labelFileName = './labelOut.txt'

#fileNames = next(os.walk(testPath))[2]
fileNames = ["JASPAR2022_CORE_vertebrates_non-redundant_v2.meme"]



#Randomly gets probabilities for 4 positions
def getProbabilities():
    x = np.random.rand(4)
    x = x / (sum(x))
    return x #Make one position higher than others - not uniform like right now

#Determines whether or not the input is an integer
def isInteger(integer):
    try:
        eval(integer)
        return True
    except:
        return False

#Processes a single motif and creates the PWM correspondingly with added noise
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
            #We want to divide by 1 + noiseImpact because we want to make sure PWM probabilities will still sum up to 1
            retMotif[-1][0] = (retMotif[-1][0] + a * noiseImpact) / (1 + noiseImpact)
            retMotif[-1][1] = (retMotif[-1][1] + c * noiseImpact) / (1 + noiseImpact)
            retMotif[-1][2] = (retMotif[-1][2] + t * noiseImpact) / (1 + noiseImpact)
            retMotif[-1][3] = (retMotif[-1][3] + g * noiseImpact) / (1 + noiseImpact)
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

#Processes an entire file of motifs
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

#Above is all processing motif data
############################################################################################
############################################################################################
############################################################################################
#Below is creating training sequences

#Determines whether or not our random choice is valid (ie the motifs aren't overlapping)
def isValidStarting(randStartPos, currMotifs):
    for i in range(len(randStartPos) - 1):
        if (randStartPos[i] + len(currMotifs[i]) + motifDistance > randStartPos[i + 1]):
            return False
    return True

#This writes an sequence with following parameters into a file: 
    #totMotif is the array of all the motifs
    #numMotifs should be the number of motifs we want to add into the array
    #ofile is the file to write our results into
def createArray(totMotif, numMotif, PWMFile, labelFile):
    #Randomly get indexes for however many motifs we want to include
    randIndex = np.random.randint(0, len(totMotif), numMotif)
    currMotifs = []
    for index in randIndex:
        currMotifs += [totMotif[index]]
    #Get the random starting positions of these motifs (making sure that the motif does not go out of bounds)
    randStartPos = sorted(np.random.randint(0, finalLength - len(currMotifs[-1]), numMotif))
    isFail = 0
    #Test whether these starting positions are valid until we succeed
    while (not isValidStarting(randStartPos, currMotifs)):
        #If we've failed to find a valid starting position for over 100 times, we return fail state
        if (isFail > 100):
            return False
        randStartPos = sorted(np.random.randint(0, finalLength - len(currMotifs[-1]), numMotif))
        isFail += 1

    prevEnd = 0
    for motifInd in range(numMotif):
        #Add in random probabilities until we reach next motif position
        for count in range(prevEnd, randStartPos[motifInd]):
            randomProb = getProbabilities()
            PWMFile.write(str(randomProb[0]) + " " + str(randomProb[1]) + " " + str(randomProb[2]) + " " + str(randomProb[3]) + "\n")
            labelFile.write("0\n")
        #Add in the motif
        for motifLine in range(len(currMotifs[motifInd])):
            PWMFile.write(str(currMotifs[motifInd][motifLine][0]) + " " + str(currMotifs[motifInd][motifLine][1]) + " " + str(currMotifs[motifInd][motifLine][2]) + " " + str(currMotifs[motifInd][motifLine][3]) + "\n")
            labelFile.write("1\n")
        prevEnd = randStartPos[motifInd] + len(currMotifs[motifInd])
    
    #Add in the portion from the last motif to the end of the length (default 128) character cycle
    for count in range(prevEnd, finalLength):
        randomProb = getProbabilities()
        PWMFile.write(str(randomProb[0]) + " " + str(randomProb[1]) + " " + str(randomProb[2]) + " " + str(randomProb[3]) + "\n")
        labelFile.write("0\n")
    
    PWMFile.write("\n")
    labelFile.write("\n")
    return True

def main():
    #We loop through all the possible files
    totMotif = []
    for n, fileName in tqdm(enumerate(fileNames), total = len(fileNames)):
        path = testPath + fileName
        ifile = open(path, 'r')
        processFile(ifile, totMotif)
    #We complete collection of all possible motifs. We now begin creating training sequences

    PWMFile = open(PWMFileName, 'w')
    labelFile = open(labelFileName, 'w')

    PWMFile.write(str(generateNumSequence) + "\n")
    
    success = 0
    fail = 0
    
    #Used to count how many number of motifs sequences we've included
    count = [0 for i in range(maxMotifsPerSequence + 1)]

    #First loop through to get a general sense
    for i in tqdm(range(0, generateNumSequence), desc = "Sequence Generation Process"):
        if (fail / generateNumSequence > 0.5):
            print("FAILED: PLEASE CHOOSE PARAMETERS AGAIN")
            break
        numMotif = np.random.randint(1, maxMotifsPerSequence + 1)
        if (createArray(totMotif, numMotif, PWMFile, labelFile)):
            success += 1
            count[numMotif] += 1
        else:
            fail += 1
    #Loop through number of sequences we want and generate them (as a catch all)
    while (success < generateNumSequence):
        #If over half of our generated numSequence has failed
        if (fail / generateNumSequence > 0.5):
            print("FAILED: PLEASE CHOOSE PARAMETERS AGAIN")
            break
        numMotif = np.random.randint(1, maxMotifsPerSequence + 1)
        if (createArray(totMotif, numMotif, PWMFile, labelFile)):
            success += 1
            count[numMotif] += 1
        else:
            fail += 1
    print("\nSummary: \n\tSuccess - " + str(success) + "\n\tFail - " + str(fail))
    print("\tSequence Motif Distribution = " + str(count))
    #print(len(totMotif))

main()