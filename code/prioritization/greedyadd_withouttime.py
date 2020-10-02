import os
from collections import defaultdict
from bitarray import bitarray
import copy
import bitarray
from bitarray import bitdiff
from bitarray import bitarray
import os.path
import os, errno
import copy
import time
import sys
import pickle

#CoverageList = []
#CoverageNumber = []
TimeList = []
#CoverageIndexList =[]
LimitTime = 0

def tree(): return defaultdict(tree)

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
                raw_input('get candidate test index error!')


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
                raw_input('error')
        return selected_index

def getTestCoverage(c):
        count = 0
        for i in range(len(c)):
                if c[i] == '1':
                        count += CoverageNumber[i]
        return count

def getCoverageIndex(a,b):
        ci_list = []
        for i in range(len(a)):
                if a[i] != b[i]:
                        ci_list.append(i)
        return ci_list

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

# temp_list : the unsorted test 
# temp_str : the coverage of sorted test

def get_Not_empty(temp_list): 
    usefullist = []
    for item in temp_list:
        if CoverageList[item].count('1') != 0:
            usefullist.append(item)
    return usefullist

def selection(test_cov,number_list,unsorted_dict,detected_unit):
    s,uni_max = -1,-1
    for test_item in unsorted_dict:
        #print(test_cov[test_item])
        #print(detected_unit)
        uni_list = test_cov[test_item] - detected_unit
        uni_sum = 0
        for uni_item in uni_list:
            uni_sum += number_list[uni_item]
        #uni_sum = uni_sum/(TimeList[test_item]*1.0)
        #uni_item = len(test_cov[test_item] - detected_unit)/(TimeList[test_item])
        if uni_sum > uni_max:
            s = test_item
            uni_max = uni_sum
    if uni_max == -1:
        return False
    else:
        return s


def greedyAdditional(g_number, test_name, test_cov, number_list, test_time,tl_number):        
        # construct initial group - sorted_group, with the group number g_number
        # the coverage of the group is recorded in sorted_coverage
        sorted_group = []
        sorted_coverage = []
        sorted_time = []
        init_cov = ''
        toleratenumber = 0
        #groupTimeLimit = (sum(test_time)/(g_number*1.0),time_tolerate)
        
        global TimeList
        global TimeLimit


        TestList = range(len(test_name))
        TimeList = copy.deepcopy(test_time)

        large_group,small_group,avg = divideSmallandLarge(TestList,g_number,TimeList,tl_number)
        small_number = g_number - len(large_group)
        groupTimeLimit = (avg,(tl_number -1)*avg)

        used_cov_unit = []
        for i in range(small_number):
                sorted_group.append([])
                sorted_coverage.append(set())
                sorted_time.append(0)
        
        time_sequence = quick_sort_time(small_group)        

        #sort tests to get the candidate test for each step
        #small_cov = []
        #small_time = []
        #for i in small_group:
        #        small_cov.append(CoverageList[i])
        #        small_time.append(TimeList[i])
        #cc_list = additional_sort(small_group,small_cov,small_time)
        #init_cov = '0' * len(CoverageList[0])
        #detected_cov = '0' * len(CoverageList[0])
        detected_cov = set()
        candidate_dict = {}
        for item in small_group:
            candidate_dict[item] = set(copy.deepcopy(test_cov[item]))
        #candidate_list = get_Not_empty(candidate_list)
        while len(candidate_dict) > 0:
                #candidate_index_list = getIndex(sorted_group)
                #candidate_test = candidate_list[0]
                #checkcov.append(detected_cov)
                candidate_test = selection(test_cov,number_list,candidate_dict,detected_cov)
                if candidate_test == False:
                        #print 'additional init ...'
                        detected_cov = set()
                        candidate_test = selection(test_cov,number_list,candidate_dict,detected_cov)
                        #continue
                else:
                        pass
                candidate_time = TimeList[candidate_test]
                candidate_index_list = getIndex(sorted_time,candidate_time,groupTimeLimit)

                if len(candidate_index_list) == 1:
                        candidate_index = candidate_index_list[0]
                else:
                        candidate_index = getMaxCoverage(sorted_coverage,candidate_index_list)
                cT = checkTime(sorted_group,sorted_time,(candidate_test,candidate_time,candidate_index),time_sequence[0],groupTimeLimit)
                if cT == 1:
                        add_name = candidate_test
                        #add_cov = CoverageList[add_name]
                        add_cov = test_cov[add_name]
                        add_time = TimeList[add_name]
                else:
                        add_name = time_sequence[0][0]
                        #add_cov = CoverageList[add_name]
                        add_cov = test_cov[add_name]
                        add_time = TimeList[add_name]
                        toleratenumber += 1
                sorted_group[candidate_index].append(add_name)
                #sorted_coverage[candidate_index] = bitarray.to01(bitarray(sorted_coverage[candidate_index])|bitarray(add_cov))
                sorted_coverage[candidate_index] = sorted_coverage[candidate_index] | candidate_dict[add_name]
                sorted_time[candidate_index] = sorted_time[candidate_index] + add_time
                #detected_cov = bitarray.to01(bitarray(detected_cov)|bitarray(add_cov))
                detected_cov = detected_cov | candidate_dict[add_name]
                #checklist.append(add_name)
                #print 'check point : ' + str(checklist)
                for i in range(len(time_sequence)):
                        if time_sequence[i][0] == add_name:
                                time_sequence.pop(i)
                                break
                del candidate_dict[add_name]
                #print(detected_cov)
                #input('check...')
        for item in large_group:
                sorted_group.append([item])
        for i in range(len(sorted_group)):
                for j in range(len(sorted_group[i])):
                        sorted_group[i][j] = test_name[sorted_group[i][j]]
        return sorted_group,toleratenumber

def countnumber(templist):
    count = 0
    for item in templist:
        count += len(item)
    return count


if __name__ == '__main__':
        #print greedyAdditional(2,['t1','t2','t3','t4'],['000001','010000','101000','101000'],[50,200,60,20],20)
        path = '/devdata/zjy/parallelTCP/tosem_add/experiment/'
        subject_list = readFile(path + 'uselist-all')
        g_n = int(sys.argv[1])
        tl_n = float(sys.argv[2])
        tosem_path = str(sys.argv[3])
        gran = str(sys.argv[4])
        '''
	if 'dynamic' in tosem_path:
            subject_list = readFile(path + 'uselist-adddy')
        elif 'callgraph' in tosem_path:
            subject_list = readFile(path + 'uselist-addcg')
        else:
            raw_input('error check ...')
        '''
        #subject_list = readFile(path + 'uselist-gnadd-all')
        for subject_item in subject_list:
                #if subject_item in skip:
                #    continue
                subject_path = path + subject_item + '/' + tosem_path + '/'
                testlist = readFile(subject_path + 'testList')
                coveragedict = LoadPickle(subject_path + gran + 'Dict_reduced.pickle')
                numberlist = readFile(subject_path + gran + '-reduce-index.txt')
                if os.path.exists(subject_path + 'exeTime.txt') == True:
                        timelist = readFile(subject_path + 'exeTime.txt')
                else:
                        timelist = readFile(subject_path + 'exeTime')
                #print(coveragedict)
                #timelist = readFile(subject_path + 'time.txt')
                #print len(testlist)
                for i in range(len(timelist)):
                        timelist[i] = float(timelist[i])
                for i in range(len(numberlist)):
                        numberlist[i] = eval(numberlist[i])
                st = time.time()
                tt,tc =  greedyAdditional(g_n,testlist,coveragedict,numberlist,timelist,tl_n)
                prioritize_time = time.time() - st
                if countnumber(tt) != len(testlist):
                    print countnumber(tt)
                    print ' not equal !!!!!!!!!'
                '''
                print '----------------'
                count = 0
                for item in tt:
                        print len(item)
                               count += len(item)
                print '----------------'
                print count
                '''
                f = open(subject_path + gran + '/' + str(tl_n) + 'avg-new/group'+str(g_n)+'/greedyadditional_withouttime.txt','w')
                for group_item in tt:
                        for test_item in group_item:
                                f.write(test_item + '\t')
                        f.write('\n')
                f.close()
                f_time = open(subject_path + gran + '/' + str(tl_n) + 'avg-new/group'+str(g_n)+'/timegreedyadditional_withouttime','w')
                f_time.write(str(prioritize_time))
                f_time.close()
                f_tolerate = open(subject_path + gran + '/' + str(tl_n) + 'avg-new/group'+str(g_n)+'/tolerategreedyadditional_withouttime','w')
                f_tolerate.write(str(tc))
                f_tolerate.close()
                print subject_path + ' is completed!'

