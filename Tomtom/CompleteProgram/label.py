#Program to label give tom tom output

import pandas as pd

df = pd.read_csv("tomtom_out/tomtom.tsv", delimiter="\t")
#We only take the ones with an e-value lower than this

ifile = open("names.txt", 'r')
ofile = open("labelled.txt", 'w')


def isValid(pValue, eValue, qValue):
    
    return ((eValue) < 0.5)


df = df[["Query_ID", "Optimal_offset", "p-value", "E-value", "q-value", "Overlap"]]


def main():
    dict = {}
    for index, row in df.iterrows():

        if (isValid((row["p-value"]), (row["E-value"]), (row["q-value"]))):
            if (row["Query_ID"] not in dict):
                dict[row["Query_ID"]] = []
            mergeRanges(dict[row["Query_ID"]], row["Optimal_offset"], row["Overlap"])

    print (dict)
    #for key in dict:
    #    processSequence(dict, key)
    while (processSequence(dict)):
        continue

    
    #print(dict)


def processSequence(dict):
    origName = ifile.readline()
    if (origName == "\n" or origName == ""):
        return False
    origName = origName[1:-1]
    name = origName.split("_")
    start = int(name[-2])
    end = int(name[-1])
   
    
    #origName = origName[:-1]
    #print (origName)
    #print (origName in dict)

    if (origName not in dict):
        print(origName in dict)
        return True
    ofile.write(origName + "\n")
    for interval in dict[origName]:
        #If we are currently not a range
        #print (range)
        for i in range(start, interval[0]):
            ofile.write("0\n")
        #We are now currently in a range
        for i in range(interval[0], interval[1] + 1):
            ofile.write("1\n")
        start = int(name[-2]) + interval[1] + 1
        #print("HIHIHIH")
        #print(start)
    #print(start)
    #print(end)
    for i in range(start, end):
        ofile.write("0\n")
    ofile.write("\n")
    return True


def mergeRanges(arrOfRanges, newOffset, overlap):
    #If we don't start at the beginning of the query
    newOffset = int(newOffset)
    overlap = int(overlap)
    start = 0
    end = -1
    if (newOffset < 0):
        start = newOffset * -1
        end = start + overlap - 1
    else:
        start = 0
        end = overlap - 1
    index, isFound = binarySearch(arrOfRanges, start)
    #print (start, end)
    #If the range overlaps with existing range
    if (isFound):
        #If we are at the first element
        if (index == -1):
            arrOfRanges = [[start, end]] + arrOfRanges
        else:
            #While we don't reach the end of the array and we realize we can merge intervals
            while ((index != len(arrOfRanges) - 1) and (arrOfRanges[index + 1][0] < end)):
                arrOfRanges[index][1] = arrOfRanges[index + 1][1]
                del arrOfRanges[index + 1]
            
            arrOfRanges[index][1] = max(arrOfRanges[index][1], end)
    #If the range does not overlap with starting range
    else:
        #If we are at the last element
        if (index == len(arrOfRanges) - 1):
            arrOfRanges += [[start, end]]
        #We are not at the last element
        else:
            #If we do not reach the next interval, we create our own little interval
            if (arrOfRanges[index + 1][0] > end):
                arrOfRanges.insert(index + 1, [start, end])
            #We are intersecting with the next range
            else:
                index = index + 1
                while ((index != len(arrOfRanges) - 1) and (arrOfRanges[index + 1][0] < end)):
                    arrOfRanges[index][1] = arrOfRanges[index + 1][1]
                    del arrOfRanges[index + 1]
                arrOfRanges[index][1] = max(arrOfRanges[index][1], end)
                arrOfRanges[index][0] = start
    return arrOfRanges




    
#Searches for the range that equals, or is less than, our current inquiry
#If we found an overlapping range, return true. If we found lower bound, return false
#Note that if "start" is less than first element, the returned index is -1
def binarySearch(arrOfRanges, start):
    begin = 0
    end = len(arrOfRanges) - 1
    
    while (begin <= end):
        mid = (begin + end)//2
        if ((arrOfRanges[mid][0] <= start) and (arrOfRanges[mid][1] >= start)):
            return (mid, True)
        elif (arrOfRanges[mid][1] < start):
            begin = mid + 1
        else:
            end = mid - 1
    return (end, False)
#testArr = [[2, 12], [18, 23], [40, 3892]]
#print (binarySearch(testArr, 1))
#testArr = mergeRanges(testArr, -1, 2)
#print (mergeRanges(testArr, 2, 1))

main()