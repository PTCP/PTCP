import os
from collections import defaultdict
from bitarray import bitarray
import copy
import time
import sys

CoverageList = []
CoverageNumber = []
TimeList = []
CoverageIndexList =[]
LimitTime = 0



def tree(): return defaultdict(tree)

def readFile(filepath):
    f = open(filepath)
    content = f.read()
    f.close()
    return content.splitlines()

# get candidate group with fewest test execution time, with the limit of execution time for each group
def getIndex(temp_list,temp_time,temp_limit):
    tt = copy.deepcopy(temp_list)
    tt.sort()
    min_time = tt[0]
    index_list = []
    for i in range(len(temp_list)):
        if temp_list[i] == min_time:
            index_list.append(i)
    if len(index_list) != 0:
        return index_list
    else:
        #raw_input('get candidate test index error!')
        print('get candidate test index error!')
        assert(0)


# get candidate group with the maximum coverage
def getMaxCoverage(temp_cov, temp_index):
    max_cov = -1
    selected_index = -1
    for i in temp_index:
        temp_count = getTestCoverage(temp_cov[i])
        if temp_count > max_cov:
            selected_index = i
            max_cov = temp_count
    if selected_index == -1:
        #raw_input('error')
        print('getMaxCoverge err: not selected')
        assert(0)
    return selected_index

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


# calculate full coverage by counting the number of statements in each virtual statements
def getTestCoverage(c):
    count = 0
    for i in range(len(c)):
        if c[i] == '1':
            count += CoverageNumber[i]
    return count


# sort with the test name, test coverage and test execution time information, using the ratio of test coverage and its execution time 
def quick_sort(temp_name):
    temp_list = []
    for i in temp_name:
        temp_number = getTestCoverage(CoverageList[i])
        temp_list.append((i,temp_number/(float(TimeList[i]*1.0))))
    return quickSort(temp_list)

def quick_sort_time(temp_name):
    temp_list = []
    for i in range(len(temp_name)):
        temp_list.append((temp_name[i],TimeList[temp_name[i]]))
    return quickSort(temp_list)


def getAllTime(temp_list):
    temp_count = 0
    for item in temp_list:
        temp_count += item[1]
    return temp_count

# check whether the time constraint is satisfied during test prioritization
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


def greedytotal(g_number, test_name, test_cov, test_time, cov_number, avg_number):
    # construct initial group - sorted_group, with the group number g_number
    # the coverage of the group is recorded in sorted_coverage
    sorted_group = []
    sorted_coverage = []
    sorted_time = []
    toleratenumber = 0
    global CoverageList
    global CoverageNumber
    global CoverageIndexList
    global TimeList
    global TimeLimit

    TestList = range(len(test_name))
    TimeList = copy.deepcopy(test_time)
    CoverageList = copy.deepcopy(test_cov)

    # construct global variable to record the number of statements in each virtual statement
    CoverageNumber = []
    for i in cov_number:
        CoverageNumber.append(int(i))

    # divide tests into two groups: large_group and small_group.
    # large_group: find the tests that exceed the average execution time for various groups.
    # small_group: find the tests that within the average execution time for various groups.
    large_group,small_group,avg = divideSmallandLarge(TestList,g_number,TimeList,avg_number)
    small_number = g_number - len(large_group)
    groupTimeLimit = (avg,(avg_number-1) * avg)
    
    # init coverage, sorted_group, sorted_coverage, and sorted_time for allocating tests to different groups.
    init_cov = ''
    for i in range(len(test_cov[0])):
        init_cov += '0'
    for i in range(small_number):
        sorted_group.append([])
        sorted_coverage.append(init_cov)
        sorted_time.append(0)

    # get the descending order of test execution time
    time_sequence = quick_sort_time(small_group)

    # get the order of candidate list based on the descending order of the covered statements
    candidate_list = quick_sort(small_group)

    while len(candidate_list) != 0:
        # get the first test in candidate list as candidate test
        candidate_test = candidate_list[0][0]
        candidate_time = TimeList[candidate_test]

        # get the group in which the test execution time is shortest
        # candidate test will be allocated in this candidate group
        candidate_index_list = getIndex(sorted_time,candidate_time,groupTimeLimit)

        # if the number group in candidate list is 1, this group is candidate group
        # otherwise, the group with max coverage is selected as candidate group 
        if len(candidate_index_list) == 1:
            candidate_index = candidate_index_list[0]
        else:
            candidate_index = getMaxCoverage(sorted_coverage,candidate_index_list)
        
        # time constraint is checked!
        # 1: if the time constraint is satisfied, the candidate test can be added to candidate group in success
        # 2: if the time constraint is violated, the first test in time_sequence (i.e., decending order of execution time) will be selected as candidate test
        #    and then this test will be added to candidate group.  
        cT = checkTime(sorted_group,sorted_time,(candidate_test,candidate_time,candidate_index),time_sequence[0],groupTimeLimit) 
        if cT == 1:
            add_name = candidate_test
            add_cov = CoverageList[add_name]
            add_time = TimeList[add_name]
        else:
            add_name = time_sequence[0][0]
            add_cov = CoverageList[add_name]
            add_time = TimeList[add_name]
            toleratenumber += 1

        # add candidate test to candidate group
        # update sorted_group, sorted_time, sorted_coverage
        # remove candidate test from time_sequence and candidate_list
        sorted_group[candidate_index].append(add_name)
        sorted_coverage[candidate_index] =  bitarray.to01(bitarray(sorted_coverage[candidate_index])|bitarray(add_cov))
        sorted_time[candidate_index] = sorted_time[candidate_index] + add_time
        for i in range(len(time_sequence)):
            if time_sequence[i][0] == add_name:
                time_sequence.pop(i)
                break
        for i in range(len(candidate_list)):
            if candidate_list[i][0] == add_name:
                candidate_list.pop(i)
                break
    # added the tests in large_group to different group, each group contains only one test
    for item in large_group:
        sorted_group.append([item])
    sorted_group_name = copy.deepcopy(sorted_group)
    # return the name of sorted test.
    for i in range(len(sorted_group_name)):
        for j in range(len(sorted_group_name[i])):
            sorted_group_name[i][j] = test_name[sorted_group[i][j]]
    return sorted_group_name,toleratenumber		

# test case for check whether the time constraint is satisfied by prioritization result
def TestCheckLimit(chromosome):
    for i in chromosome:
        temp_time = 0
        for j in i:
            temp_time += TimeList[j]
            if temp_time > TimeLimit:
                return False
            else:
                continue
    return True

if __name__ == '__main__':
    path = '../../subject/experiment/'
    if len(sys.argv) == 5:
        g_n = int(sys.argv[1])
        tl_n = float(sys.argv[2])
        tosem_path = str(sys.argv[3])
        gran = str(sys.argv[4])
    else:
        print('Usage: greedytotal_withtime.py <group_number> <time_constraint> <test_granularity> <coverage_granularity>.')
        sys.exit(0)
    
    '''
    # the subjects list used in some experiments in the paper
    if 'dynamic' in tosem_path:
        subject_list = readFile(path + 'uselist-adddy')
    elif 'callgraph' in tosem_path:
        subject_list = readFile(path + 'uselist-addcg')
    else:
        raw_input('error check ...')
    '''
    subject_list = readFile(path + 'uselist-all')
    for subject_item in subject_list:
        subject_path = path + subject_item + '/' + tosem_path + '/'
        testlist = readFile(subject_path + 'testList')
        coveragelist = readFile(subject_path + gran + 'Matrix-reduce.txt')
        numberlist = readFile(subject_path + gran + '-reduce-index.txt')
        if os.path.exists(subject_path + 'exeTime.txt') == True:
            timelist = readFile(subject_path + 'exeTime.txt')
        else:
            timelist = readFile(subject_path + 'exeTime')

        for i in range(len(timelist)):
            timelist[i] = float(timelist[i])
        st = time.time()
        tt,tc =  greedytotal(g_n,testlist,coveragelist,timelist,numberlist,tl_n)
        prioritize_time = time.time() - st

        if os.path.exists(subject_path + gran + '/' + str(tl_n) +'avg-new/group'+str(g_n)+'/') == False:
            os.makedirs(subject_path + gran + '/' + str(tl_n) + 'avg-new/group'+str(g_n)+'/')
        f = open(subject_path + gran + '/' +str(tl_n) + 'avg-new/group'+str(g_n)+'/greedytotal_withtime.txt','w')
        for group_item in tt:
            for test_item in group_item:
                f.write(test_item + '\t')
            f.write('\n')
        f.close()
        f_time = open(subject_path + gran + '/' +str(tl_n) + 'avg-new/group'+str(g_n)+'/timegreedytotal_withtime','w')
        f_time.write(str(prioritize_time))
        f_time.close()
        f_tolerate = open(subject_path + gran + '/' +str(tl_n) + 'avg-new/group'+str(g_n)+'/tolerategreedytotal_withtime','w')
        f_tolerate.write(str(tc))
        f_tolerate.close()
        print subject_path + ' is completed! ' + str(tc)

