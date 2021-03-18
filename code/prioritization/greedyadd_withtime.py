import os
from collections import defaultdict
import copy
import bitarray
from bitarray import bitdiff
from bitarray import bitarray
import os.path
import errno
import time
import sys
import pickle
import unittest


TimeList = []
LimitTime = 0

def tree(): return defaultdict(tree)

def readFile(filepath):
    f = open(filepath)
    content = f.read()
    f.close()
    return content.splitlines()

# load pickle file for coverage, 
def LoadPickle(filepath):
    f = open(filepath,'rb')
    data = pickle.load(f)
    f.close()
    for item in data:
        data[item] = set(data[item])
    return data

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
        temp_count = len(temp_cov[i])
        if temp_count > max_cov:
            selected_index = i
            max_cov = temp_count
    if selected_index == -1:
        #raw_input('error')
        print('getMaxCoverge err: not selected')
        assert(0)
    return selected_index

# get the index of statements that differ in test coverage 
def getCoverageIndex(a,b):
    ci_list = []
    for i in range(len(a)):
        if a[i] != b[i]:
            ci_list.append(i)
    return ci_list

# calculate full coverage by counting the number of statements in each virtual statements
# temp_list is the list of the index of tests that differ in test coverage
def getAllCount(temp_list):
    count = 0
    for i in temp_list:
        count += CoverageNumber[i]
    return count

def quick_sort_time(temp_name):
    temp_list = []
    for i in range(len(temp_name)):
        temp_list.append((temp_name[i],TimeList[temp_name[i]]))
    return quickSort(temp_list)


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


# calculate execution time of test sequence
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
        if TimeList[item] > (avg):
            large.append(item)
        else:
            small.append(item)
    return (large,small,avg)


# select candidate test based on greedy additional strategy
def selection(test_cov,number_list,unsorted_dict,detected_unit):
    s,uni_max = -1,0
    for test_item in unsorted_dict:
        uni_list = test_cov[test_item] - detected_unit
        uni_sum = 0
        for uni_item in uni_list:
            uni_sum += number_list[uni_item]
        uni_sum = uni_sum/(TimeList[test_item]*1.0)
        if uni_sum > uni_max:
            s = test_item
            uni_max = uni_sum
    if uni_max == -1:
        return -1
    else:
        return s

# parallel test prioritization using greedy additional strategy
def greedyAdditional(g_number, test_name, test_cov, number_list, test_time,tl_number):        
    # construct initial group - sorted_group, with the group number g_number
    # the coverage of the group is recorded in sorted_coverage
    sorted_group = []
    sorted_coverage = []
    sorted_time = []
    init_cov = ''
    toleratenumber = 0

    global TimeList
    global TimeLimit

    TestList = range(len(test_name))
    TimeList = copy.deepcopy(test_time)

    # divide tests into two groups: large_group and small_group.
    # large_group: find the tests that exceed the average execution time for various groups.
    # small_group: find the tests that within the average execution time for various groups.
    large_group,small_group,avg = divideSmallandLarge(TestList,g_number,TimeList,tl_number)
    small_number = g_number - len(large_group)
    groupTimeLimit = (avg,(tl_number -1)*avg)

    # init coverage, sorted_group, sorted_coverage, and sorted_time for allocating tests to different groups.
    # sorted_group and sorted_coverage are empty, and sorted_time is 0
    used_cov_unit = []
    for i in range(small_number):
        sorted_group.append([])
        sorted_coverage.append(set())
        sorted_time.append(0)
    
    # get the descending order of test execution time
    time_sequence = quick_sort_time(small_group)  

    # init a candidate_dict to record candidate
    detected_cov = set()
    candidate_dict = {}
    for item in small_group:
        candidate_dict[item] = set(copy.deepcopy(test_cov[item]))
        
    while len(candidate_dict) > 0:
        # get a candidate test by using additional strategy
        candidate_test = selection(test_cov,number_list,candidate_dict,detected_cov)
        # if no candidate test is selected, the detected_cov is reset to empty, and additional strategy is repeated.
        if candidate_test == -1:
            detected_cov = set()
            candidate_test = selection(test_cov,number_list,candidate_dict,detected_cov)
            #continue
        else:
            pass

        # if the number group in candidate list is 1, this group is candidate group
        # otherwise, the group with max coverage is selected as candidate group 
        candidate_time = TimeList[candidate_test]
        candidate_index_list = getIndex(sorted_time,candidate_time,groupTimeLimit)
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
            add_cov = test_cov[add_name]
            add_time = TimeList[add_name]
        else:
            add_name = time_sequence[0][0]
            add_cov = test_cov[add_name]
            add_time = TimeList[add_name]
            toleratenumber += 1
        
        # add candidate test to candidate group
        # update sorted_group, sorted_time, sorted_coverage
        # remove candidate test from time_sequence and candidate_list
        sorted_group[candidate_index].append(add_name)
        sorted_coverage[candidate_index] = sorted_coverage[candidate_index] | candidate_dict[add_name]
        sorted_time[candidate_index] = sorted_time[candidate_index] + add_time
        detected_cov = detected_cov | candidate_dict[add_name]
        for i in range(len(time_sequence)):
            if time_sequence[i][0] == add_name:
                time_sequence.pop(i)
                break
        del candidate_dict[add_name]

    # added the tests in large_group to different group, each group contains only one test
    for item in large_group:
        sorted_group.append([item])

    # return the name of sorted test.
    for i in range(len(sorted_group)):
        for j in range(len(sorted_group[i])):
            sorted_group[i][j] = test_name[sorted_group[i][j]]
    return sorted_group,toleratenumber

def countnumber(templist):
    count = 0
    for item in templist:
        count += len(item)
    return count

class TestAGA(unittest.TestCase):
    def test_aga_result(self): 
        testlist = ['t1','t2','t3','t4','t5','t6']
        coveragedict = {0:set([0,1,2]),
                    1:set([2,3,4]),
                    2:set([0,1]),
                    3:set([2,4]),
                    4:set([1,3]),
                    5:set([4])}
        numberlist = [1,1,1,1,2]
        timelist = [4,20,6,2,5,9]
        oracle = [['t4','t5','t6'],['t1','t3'],['t2']]
        test_result = greedyAdditional(3,testlist,coveragedict,numberlist,timelist,1.5)[0]
        print('test result: %s'%str(test_result))
        self.assertEqual(test_result, oracle)


if __name__ == '__main__':
    
    # test case for AGA
    unittest.main()

    path = '../../subjects/'
    subject_list = readFile(path + 'uselist-all')
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
    
    for subject_item in subject_list:
        subject_path = path + subject_item + '/' + tosem_path + '/'
        testlist = readFile(subject_path + 'testList')
        coveragedict = LoadPickle(subject_path + gran + 'Dict_reduced.pickle')
        numberlist = readFile(subject_path + gran + '-reduce-index.txt')
        if os.path.exists(subject_path + 'exeTime.txt') == True:
            timelist = readFile(subject_path + 'exeTime.txt')
        else:
            timelist = readFile(subject_path + 'exeTime')
        for i in range(len(timelist)):
            timelist[i] = float(timelist[i])
        for i in range(len(numberlist)):
            numberlist[i] = eval(numberlist[i])
        st = time.time()
        tt,tc =  greedyAdditional(g_n,testlist,coveragedict,numberlist,timelist,tl_n)
        prioritize_time = time.time() - st
        # check whether the prioritization results is contain the same number of tests, in case that some bugs exist.
        if countnumber(tt) != len(testlist):
            print countnumber(tt)
            print ' not equal !!!!!!!!!'
            assert(0)

        f = open(subject_path + gran + '/' + str(tl_n) + 'avg-new/group'+str(g_n)+'/greedyadditional_withtime.txt','w')
        for group_item in tt:
            for test_item in group_item:
                f.write(test_item + '\t')
            f.write('\n')
        f.close()
        f_time = open(subject_path + gran + '/' + str(tl_n) + 'avg-new/group'+str(g_n)+'/timegreedyadditional_withtime','w')
        f_time.write(str(prioritize_time))
        f_time.close()
        f_tolerate = open(subject_path + gran + '/' + str(tl_n) + 'avg-new/group'+str(g_n)+'/tolerategreedyadditional_withtime','w')
        f_tolerate.write(str(tc))
        f_tolerate.close()
        print subject_path + ' is completed!'


