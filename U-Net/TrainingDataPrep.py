
import numpy as np

#print(norm.ppf(0.25))#Getting the invNorm
#print(norm.cdf(norm.ppf(0.25)))

#print(np.random.rand())

'''
mu = norm.ppf(0.25)
sigma = 1

s = np.random.normal(mu, sigma, 10000)
process = lambda x: norm.cdf(x)
s = np.array([process(x) for x in s])


print(abs(np.mean(s)))
import matplotlib.pyplot as plt
count, bins, ignored = plt.hist(s, 30, density=True)
plt.plot(bins, 1/(sigma * np.sqrt(2 * np.pi)) *
               np.exp( - (bins - mu)**2 / (2 * sigma**2) ),
         linewidth=2, color='r')
plt.show()
'''

def getProbabilities():
    x = np.random.rand(4)
    x = x / sum(x)
    return x


from pyrsistent import m
import os
from tqdm import tqdm 

finalLength = 128

#ifile = open("JASPAR2022_CORE_vertebrates_non-redundant_v2.meme", 'r')

testPath = '../motif_databases/JASPAR/'

#fileNames = next(os.walk(testPath))[2]
fileNames = ["JASPAR2022_CORE_vertebrates_non-redundant_v2.meme"]

#print(fileNames)

def processMotif():
    motifName = ifile.readline()
    #print(motifName)
    if (motifName == "\n" or motifName == ""):
        return False
    
    motifName = motifName.split(" ")[1]
    totLen = ifile.readline()
    #print("originaltotLen = " + totLen)
    if (totLen == "" or totLen == "\n"):
        totLen = ifile.readline()
    #print("totLen = " + totLen)
    totLen = int(totLen.split(" ")[5])
    #print(motifName)
    #print(totLen)
    for i in range(totLen):
        ifile.readline()
    test = ifile.readline()
    if (test == "" or test == "\n"):
        ifile.readline()
    ifile.readline()
    
    return totLen



def main(ifile):
    beginBurn = ifile.readline()


    while (beginBurn != "Background letter frequencies\n" and beginBurn != "Background letter frequencies (from uniform background):\n"):
        beginBurn = ifile.readline()
    ifile.readline() #This would read the specific letter frequences
    #print ("YAYAYA")

    test = ifile.readline() #blank line
    #print ("test output = " + test)
    maxLen = -1
    status = processMotif()
    #print("passed!")
    count = 0
    while(status):
        maxLen = max(maxLen, status)
        #print(maxLen)
        status = processMotif()
        count += 1
    print(count)
    return(maxLen)

totMax = -1

for n, fileName in tqdm(enumerate(fileNames), total = len(fileNames)):
    #print ("entered " + fileName)
    path = testPath + fileName
    ifile = open(path, 'r')
    totMax = max(totMax, main(ifile))

print (totMax)
