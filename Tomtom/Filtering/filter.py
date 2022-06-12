import math
ifile = open("test.chen", 'r')

entropyThresh = 1.85
consecThresh = 8

def processSequence():
    origName = ifile.readline()
    #print ("origname = " + origName)
    origArr = []
    temp = ifile.readline()
    while (temp != "\n"):
        origArr += [temp]
        lineEntropy = shannonEntropy(temp)
        if (lineEntropy > entropyThresh):
            continue;
        temp = ifile.readline()
    print (ifile.readline())



def shannonEntropy(currLine):
    currLine = currLine.split("\t")

    arr = list(map(lambda x: int(x), currLine))
    totSum = sum(arr)
    #print (arr)
    arr = list(map(lambda x: x / totSum, arr))
    #print (arr)
    arr = list(map(lambda x: x * math.log(1 / x, 2), arr))
    #print(arr)
    return sum(arr)
    

def main():
    processSequence()

main()
