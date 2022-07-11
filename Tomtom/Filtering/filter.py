#Program to filter

import math


ifile = open("kernel-0.all.ppm.chen", 'r')
ofile = open("output.chen", 'w')
rawFile = open("raw.chen", 'w')

entropyThresh = 1.95
consecThresh = 10
pseudoCount = 1e-10

def processFile():
    count = 0
    while (processSequence()):
        count += 1
        continue


def processSequence():
    origName = ifile.readline()
    #print ("origname = " + origName)
    if (origName == "\n" or origName == ""):
        return False
    origArr = []
    temp = ifile.readline()
    lineNum = 0
    while (temp != "\n"):
        #origArr += [temp]
        lineEntropy = shannonEntropy(temp)
        if (lineEntropy > entropyThresh):
            origArr += [temp]
        else:
            if (len(origArr) >= consecThresh):
                ofile.write(origName[:-1] + "_" + str(lineNum - len(origArr)) + "_" + str(lineNum - 1) + "\n")
                for line in origArr:
                    ofile.write(line)
                ofile.write("\n")
            origArr = []
        rawFile.write(str(lineNum) + " " + str(lineEntropy) + "\n")
        temp = ifile.readline()
        lineNum += 1
    return True
    
    #print (ifile.readline())



def shannonEntropy(currLine):
    currLine = currLine.split("\t")

    arr = list(map(lambda x: int(x), currLine))
    totSum = sum(arr)
    #print (arr)
    arr = list(map(lambda x: x / totSum + pseudoCount, arr))
    #print (arr)
    arr = list(map(lambda x: x * math.log(1 / x, 2), arr))
    #print(arr)
    return sum(arr)

    

def main():
    processFile()

main()
