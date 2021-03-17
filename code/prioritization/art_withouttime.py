import os
import sys
import copy
from bitarray import bitarray
from bitarray import bitdiff
import time
import random
import pickle

CoverageNumber = []
TimeList = []

def readFile(filepath):
    f = open(filepath)
    content = f.read()
    f.close()
    return content.splitlines()

def LoadPickle(filepath):
    f = open(filepath,'rb')
    data = pickle.load(f)
    f.close()
    for item in data:
        data[item] = set(data[item])
    return data


def getJaccardDistance_old(a,b,index_list):
    if len(a) != len(b):
        print 'Error: length not equal.'
        #raw_input('pause...')
        assert(0)
    if a.count('1') == 0 and b.count('1') == 0:
        return 0
    length = len(a)
    distance = float(0)
    join = bitarray.to01(bitarray(a)&bitarray(b))
    combine = bitarray.to01(bitarray(a)|bitarray(b))
    join_count = 0
    combine_count = 0
    for i in range(len(join)):
        if join[i] == '1':
            join_count += index_list[i]
        if combine[i] == '1':
            combine_count += index_list[i]
    distance = 1 - (join_count/(combine_count*1.0))
    return distance

def getJaccardDistance(a,b,index_list):
    if len(a) == 0 and len(b) == 0:
        return 0
    join = a&b
    combine = a|b
    join_count = len(join)
    combine_count = len(combine)
    distance = 1 - (join_count/(combine_count*1.0))
    return distance

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
    return current|newArray

def getAllCoverage(temp_str):
    count = 0
    for i in temp_str:
        count += CoverageNumber[i]
    return count

def quick_sort_time(temp_name):
    temp_list = []
    for i in range(len(temp_name)):
        temp_list.append((temp_name[i],TimeList[temp_name[i]]))
    return quickSort(temp_list)

# basic quick sort
def quickSort(temp_list):
    less = []
    pivotList = []
    more = []
    if len(temp_list) <= 1:
        return temp_list
    else:
        pivot = temp_list[0]
        for i in temp_list:
            if i[1] < pivot[1]:
                less.append(i)
            elif i[1] > pivot[1]:
                more.append(i)
            else:
                pivotList.append(i)

    less = quickSort(less)
    more = quickSort(more)
    return more + pivotList + less


def countnumber(templist):
    count = 0
    for item in templist:
        count += len(item)
    return count


# list_group and list_time record the sorted result of group while prioritization
# list_candidate record the information of candidate test, i.e., (candidate_test,candidate_time,candidate_index)
# list_max record the unsorted test with max execution time
# list_limit record the time limit of while prioritization
def checkTime(list_group,list_time,list_candidate,list_max,list_limit):
    result = 0
    for i in range(len(list_time)):
        if i == list_candidate[2]:
            temp_time = list_time[i] + list_candidate[1]
        else:
            temp_time = list_time[i]
        if temp_time + list_max[1] <= sum(list_limit):
            result = 1
            break
        else:
            continue
    return result

def getAllTime(temp_list):
    temp_count = 0
    for item in temp_list:
        temp_count += item[1]
    return temp_count


def divideSmallandLarge(temp_list,temp_number,temp_time,temp_avg):
    large = []
    small = []
    avg = sum(temp_time)/(temp_number * 1.0)
    for item in temp_list:
        if TimeList[item] > (temp_avg * avg):
            large.append(item)
        else:
            small.append(item)
    return (large,small,avg)

def ARP(test_list,cov_dict,time_list,group_number,tl_number):
    selected = []
    grouped = []
    toleratenumber = 0
        
    global TimeList
    TimeList = copy.deepcopy(time_list)
    TestList = range(len(test_list))
        
    large_group,small_group,avg = divideSmallandLarge(TestList,group_number,TimeList,tl_number)
    small_number = group_number - len(large_group)
    groupTimeLimit = (avg,(tl_number -1)*avg)
        
    grouped_cov = []
    for i in range(small_number):
        grouped.append([])
        grouped_cov.append(set())
    
    grouped_time = [float(0)] * small_number

    # for construct distance metric
    length = len(cov_dict.keys())
    DistanceMetric = []
    for i in range(length):
        j_list = []
        for j in range(length):
            j_list.append(0)
        DistanceMetric.append(copy.deepcopy(j_list))
    for i in range(length):
        for j in range(i,length):
            temp_distance = getJaccardDistance(cov_dict[i],cov_dict[j],CoverageNumber)
            DistanceMetric[i][j] = temp_distance
            DistanceMetric[j][i] = temp_distance
        
    length = len(small_group)
    time_sequence = quick_sort_time(small_group)
    LIMIT = 10
    first = random.randint(0,length-1)
    selected.append(small_group[first])
    grouped[random.randint(0,len(grouped)-1)].append(small_group[first])
    unselected = []
    for i in range(length):
        unselected.append(small_group[i])
    unselected.remove(small_group[first])

    while len(selected) < length:
        candidate = []
        covered = set()
        coveredNum = -1
        stop = False

        firstRandom = random.randint(0,len(unselected)-1)
        candidate.append(unselected[firstRandom])
        covered = mergeIntoCurrentArray(covered,cov_dict[unselected[firstRandom]])
        coveredNum = getAllCoverage(covered)
        temp_count = 0
        leftToChoose = copy.deepcopy(unselected)
        leftToChoose.remove(unselected[firstRandom])
        while True:
            if len(leftToChoose) == 0:
                break
            selectedRandom = random.randint(0,len(leftToChoose)-1)
            newCandidateIndex = leftToChoose[selectedRandom]
            covered = mergeIntoCurrentArray(covered,cov_dict[newCandidateIndex])
            currentCovered = getAllCoverage(covered)
            if currentCovered > coveredNum:
                coveredNum = currentCovered
                candidate.append(newCandidateIndex)
                leftToChoose.remove(newCandidateIndex)
                temp_count += 1
            else:
                break

        MaxDistances = [0] * len(candidate)
        for j in range(len(candidate)):
            candidateNo = candidate[j]
            MinDistance = [0] * len(selected)
            for i in range(len(selected)):
                testcaseNo = selected[i]
                MinDistance[i] = DistanceMetric[testcaseNo][candidateNo]
            MinIndex = getMinIndex(MinDistance)
            MaxDistances[j] = MinDistance[MinIndex]
        MaxIndex = getMaxIndex(MaxDistances)
        candidate_test = candidate[MaxIndex]
        candidate_time = time_list[candidate_test]
    
        grouped_index = getGroupIndex(grouped,grouped_cov,grouped_time,cov_dict[candidate[MaxIndex]],time_list[candidate[MaxIndex]])
        cT = checkTime(grouped,grouped_time,(candidate_test,candidate_time,grouped_index),time_sequence[0],groupTimeLimit)
        if cT == 1:
            selected.append(candidate[MaxIndex])
            unselected.remove(candidate[MaxIndex])
            grouped[grouped_index].append(candidate[MaxIndex])
            grouped_cov[grouped_index] = grouped_cov[grouped_index]|cov_dict[candidate[MaxIndex]]
            grouped_time[grouped_index] = grouped_time[grouped_index] + time_list[candidate[MaxIndex]]
            for time_sequence_index in range(len(time_sequence)):
                if candidate[MaxIndex] == time_sequence[time_sequence_index][0]:
                    time_sequence.pop(time_sequence_index)
                    break
                else:
                    continue
        else:
            selected.append(time_sequence[0][0])
            unselected.remove(time_sequence[0][0])
            grouped[grouped_index].append(time_sequence[0][0])
            grouped_cov[grouped_index] = grouped_cov[grouped_index]|cov_dict[time_sequence[0][0]]
            grouped_time[grouped_index] = grouped_time[grouped_index] + time_list[time_sequence[0][0]]
            time_sequence.pop(0)
            toleratenumber += 1
    if len(large_group) != 0:
        for item in large_group:
            grouped.append([item])
    selectedTestSequence = copy.deepcopy(grouped)
    for i in range(len(grouped)):
        for j in range(len(grouped[i])):
            selectedTestSequence[i][j] = test_list[grouped[i][j]]
    return selectedTestSequence,toleratenumber

def getGroupIndex(temp_group,temp_cov,temp_time,testcov,testtime):
    min_time = temp_time[0]
    for item in temp_time:
        temp = item
        if min_time > temp:
            min_time = temp
    min_list = []
    for i in range(len(temp_time)):
        if temp_time[i] == min_time:
            min_list.append(i)
    if len(min_list) == 1:
        return min_list[0]
    else:
        max_distance = getJaccardDistance(temp_cov[min_list[0]],testcov,CoverageNumber)
        max_index = min_list[0]
        for max_item in min_list:
            temp_distance = getJaccardDistance(temp_cov[max_item],testcov,CoverageNumber)
            if temp_distance > max_distance:
                max_index = max_item
                max_distance = temp_distance

        return max_index



if __name__ == '__main__':
    path = '../../subjects/'
    if len(sys.argv) == 5:
        g_n = int(sys.argv[1])
        tl_n = float(sys.argv[2])
        tosem_path = str(sys.argv[3])
        gran = str(sys.argv[4])
    else:
        print('Usage: greedytotal_withtime.py <group_number> <time_constraint> <test_granularity> <coverage_granularity>.')
        sys.exit(0)
    subject_list = readFile(path + 'uselist-all')
    '''
    if 'dynamic' in tosem_path:
        subject_list = readFile(path + 'uselist-adddy')
    elif 'callgraph' in tosem_path:
        subject_list = readFile(path + 'uselist-addcg')
    else:
        raw_input('error check ...')
    '''
    for subject in subject_list:
        subject_path = path + subject + '/' + tosem_path + '/'
        print subject_path + ' is starting...'
        if os.path.exists(subject_path + gran + '/' + str(tl_n) +'avg-new/group'+str(g_n)+'/') == False:
            os.makedirs(subject_path + gran + '/' + str(tl_n) +'avg-new/group'+str(g_n)+'/')

        testlist = readFile(subject_path + 'testList')
        coveragedict = LoadPickle(subject_path + gran + 'Dict_reduced.pickle')
        coveragenumber = readFile(subject_path + gran + '-reduce-index.txt')
        for i in range(len(coveragenumber)):
            coveragenumber[i] = int(coveragenumber[i])
        global CoverageNumber
        CoverageNumber = copy.deepcopy(coveragenumber)

        if os.path.exists(subject_path + 'exeTime.txt') == True:
            timelist = readFile(subject_path + 'exeTime.txt')
        else:
            timelist = readFile(subject_path + 'exeTime')

        for i in range(len(timelist)):
            timelist[i] = float(timelist[i])
        st = time.time()
        arp,tc = ARP(testlist,coveragedict,timelist,g_n,tl_n)
        prioritize_time = time.time() - st
        if countnumber(arp) != len(testlist):
            print 'not equal !' + str(countnumber(arp)) + ' : ' + str(len(testlist))
        f = open(subject_path + gran + '/' + str(tl_n) + 'avg-new/group'+str(g_n)+'/arp_withouttime.txt','w')
        for group_item in arp:
            for test_item in group_item:
                f.write(str(test_item) + '\t')
            f.write('\n')
        f.close()
        f_time = open(subject_path + gran + '/' + str(tl_n) + 'avg-new/group'+str(g_n)+'/timearp_withouttime','w')
        f_time.write(str(prioritize_time))
        f_time.close()
        f_tolerate = open(subject_path + gran + '/' + str(tl_n) + 'avg-new/group'+str(g_n)+'/toleratearp_withouttime','w')
        f_tolerate.write(str(tc))
        f_tolerate.close()
        print subject_path + ' is completed! ' + str(prioritize_time)
