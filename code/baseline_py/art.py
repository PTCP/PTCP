import os
import copy
from bitarray import bitarray
from bitarray import bitdiff
import time
import sys
import random
import numpy as np

def readFile(filepath):
    f = open(filepath)
    content = f.read()
    f.close()
    return content.splitlines()


# calculate the Jaccard distance between two vector
def getJaccardDistance(a,b,index_list):
    if len(a) != len(b):
        print 'Error: length not equal.'
        raw_input('pause...')
    if a.count('1') == 0 and b.count('1') == 0:
        return 0
    length = len(a)
    distance = float(0)
    join = bitarray.to01(bitarray(a)&bitarray(b))
    combine = bitarray.to01(bitarray(a)|bitarray(b))
    join_count = 0
    combine_count = 0
    #jdst = time.time()
    for i in range(len(join)):
        if join[i] == '1':
            join_count += index_list[i]
        if combine[i] == '1':
            combine_count += index_list[i]
    #print '1 : ' + str(time.time() - jdst)
    '''
    jdst = time.time()
    temp1 = [0]*length
    temp2 = [0]*length
    for i in range(len(join)):
        temp1[i] = int(join[i])
        temp2[i] = int(combine[i])
    
    t1 = np.dot(np.array(temp1),np.array(index_list))
    t2 = np.dot(np.array(temp2),np.array(index_list))
    print '2 : ' + str(time.time() - jdst)
    
    raw_input('check : ' + str(join_count) + '-' + str(t1))
    '''
    distance = 1 - (join_count/(combine_count*1.0))

    return distance


# adaptive random prioritization algorithm
def ARP(test_list,cov_list,cov_index):
    length = len(cov_list)
    columnNum = len(cov_list[0])
    selectedTestSequence = []
    selected = []
    
    '''
    cov_array = []
    for i in range(len(cov_list)):
        temp_list = []
        for j in range(len(cov_list[i])):
            temp_list.append(int(cov_list[i][j]))
        cov_array.append(temp_list)
    cov_array = np.array(cov_array)
    '''
    
    DistanceMetric = []
    for i in range(length):
        j_list = []
        for j in range(length):
            j_list.append(0)
            DistanceMetric.append(j_list)
    for i in range(length):
        for j in range(i,length):
            temp_distance = getJaccardDistance(cov_list[i],cov_list[j],cov_index)
            DistanceMetric[i][j] = temp_distance
            DistanceMetric[j][i] = temp_distance

    LIMIT = 10
    first = random.randint(0,length-1)
    selected.append(first)
    count = 0
    while len(selected) < length:
        candidate = []
        covered = '0' * columnNum
        coveredNum = 0
        stop = False
        
        templist = []
        for i in range(length):
            if i not in selected:
                templist.append(i)
        firstRandom = random.randint(0,len(templist)-1)
        candidate.append(templist[firstRandom])
        # maybe there is a bug in ARTMinMax.java, as firstRandom is the index of templist
        covered = mergeIntoCurrentArray(covered,cov_list[templist[firstRandom]])    
        #covered = mergeIntoCurrentArray(covered,cov_list[firstRandom])
        coveredNum = covered.count('1')
        #print 'coveredNum : ' + str(coveredNum)
        temp_count = 0
        while True:
            leftToChoose = []
            for i in range(length):
                if i not in selected and i not in candidate:
                    leftToChoose.append(i)
            if len(leftToChoose) == 0:
                break
            selectedRandom = random.randint(0,len(leftToChoose)-1)
            newCandidateIndex = leftToChoose[selectedRandom]
            #print 'new candidate index : ' + str(newCandidateIndex)
            #print 'check coverage : ' + str(check(covered,cov_list[newCandidateIndex]))
            covered = mergeIntoCurrentArray(covered,cov_list[newCandidateIndex])    
            currentCovered = covered.count('1')
            #print 'the length of current covered : ' + str(currentCovered)
            #print 'the length of covered :         ' + str(coveredNum)
            if currentCovered > coveredNum:
                coveredNum = currentCovered
                candidate.append(newCandidateIndex)
                temp_count += 1
                #print 'check candidate : ' + str(temp_count)
                #raw_input('check candidate in ...')
            else:
                break
        
        MaxDistances = [0] * len(candidate)
        for j in range(len(candidate)):
            candidateNo = candidate[j]
            MinDistance = [0] * len(selected)
            for i in range(len(selected)):
                testcaseNo = selected[i]
                #MinDistance[i] = getJaccardDistance(cov_list[testcaseNo],cov_list[candidateNo])
                MinDistance[i] = DistanceMetric[testcaseNo][candidateNo]
            MinIndex = getMinIndex(MinDistance)
            MaxDistances[j] = MinDistance[MinIndex]
        MaxIndex = getMaxIndex(MaxDistances)
        selected.append(candidate[MaxIndex])
        #print str(count) + ' : has candidate test - ' + str(len(candidate))  
        count += 1
        #raw_input('check...')
    for i in selected:
        selectedTestSequence.append(test_list[i])
    return selectedTestSequence
    
'''
# calculate the Jaccard distance between two vector
def getJaccardDistance(a,b):
    if len(a) != len(b):
        print 'Error: length not equal.'
        raw_input('pause...')
    if a.count('1') == 0 and b.count('1') == 0:
        return 0
    length = len(a)
    distance = float(0)
    join = bitarray.to01(bitarray(a)&bitarray(b))
    combine = bitarray.to01(bitarray(a)|bitarray(b))
    distance = 1 - (join.count('1')/(combine.count('1')*1.0))
    return distance
'''



# return the maximum element's index of the list
def getMaxIndex(a):
    maxsize = a[0]
    index = 0
    for i in range(len(a)):
        if a[i] > maxsize:
            maxsize = a[i]
            index = i
    return index

# return the minimum element's index of the list
def getMinIndex(a):
    minsize = a[0]
    index = 0
    for i in range(len(a)):
        if a[i] < minsize:
            minsize = a[i]
            index = i
    return index

# merge all the '1's in the new array into the current array
def mergeIntoCurrentArray(current, newArray):
    if len(current) != len(newArray):
        print 'Error: mergeIntoCurrentArray: length is not equal.'
        raw_input('pause...')
    length = len(current)
    merge_1 = bitarray.to01(bitarray(current)|bitarray(newArray))
    merge = ''
    for i in range(length):
        if newArray[i] == '1':
            merge += newArray[i]
        else:
            merge += current[i]
    if merge != merge_1:
        print 'Error : mergeIntoCurrentArray error...'
        raw_input('mergeIntoCurrentArray error...')
    return merge

def check(a,b):
    result = 0
    for i in range(len(a)):
        if b[i] == '1':
            if a[i] == '1':
                continue
            else:
                result += 1
    return result

if __name__ == '__main__':
    root_path = '/PTCP/subjects/experiment/'
    #root_path = '/devdata/zjy/parallelTCP/subject/test/subjects_add/'
    #subject_list = readFile(root_path + 'subject_list')
    #subject_list = os.listdir(root_path)
    subject_list = readFile(root_path + 'uselist-all')
    for subject in subject_list:
        print subject + ' is started...'
        subject_path = root_path + subject + '/dynamic/testmethod/state/'
        testlist = readFile(subject_path + 'testList')
        coveragelist = readFile(subject_path + 'stateMatrix-reduce.txt')
        coveragenumber = readFile(subject_path + 'reduce-index.txt')
        for i in range(len(coveragenumber)):
            coveragenumber[i] = int(coveragenumber[i])    
        st = time.time()
        arp = ARP(testlist,coveragelist,coveragenumber)
        prioritize_time = time.time() - st
        os.system('cp ' + subject_path + 'baseline/statement/SequenceARTMethod.txt ' + subject_path + 'baseline/statement/SequenceARTMethod.bac')
        f = open(subject_path + 'baseline/statement/SequenceARTMethod.txt','w')
        for item in arp:
            f.write(str(item) + '\n')
        f.close()
        f = open(subject_path + 'baseline/statement/TimeARTMethod','w')
        f.write(str(prioritize_time))
        f.close()
        print subject_path + ' is completed! ' + str(prioritize_time)
        #print arp
        #print str(len(testlist)) + '  -  ' + str(len(arp))
        #raw_input('pasue...')
    '''
    # for unit test
    testlist = readFile('/devdata/zjy/parallelTCP/code/baseline/testList')
    coveragelist = readFile('/devdata/zjy/parallelTCP/code/baseline/statement_matrix.txt')    
    arp = ARP(testlist,coveragelist)    
    '''
