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
                temp_count = getTestCoverage(temp_cov[i])
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

#ef additional_sort(temp_name, temp_cov)
def additional_sort(sametestcase_list,coverage_array,time_array):
    coverage_row_array = []
    detected_mu = ""
    temp_list = copy.deepcopy(sametestcase_list)
    for i in range(len(coverage_array[0])):
        detected_mu += "0"
    detected_mu_init = detected_mu
    addtional_order = []
    for i in range(len(sametestcase_list)):
        count = 0
        max_number = int(0)
        max_order = int(-1)
        for j in range(len(sametestcase_list)):
            if sametestcase_list[j] not in addtional_order:
                #temp_index = testsuitlist_old.index(sametestcase_list[j])
                #temp_number = bitdiff(bitarray(detected_mu)&bitarray(coverage_array[j]),bitarray(coverage_array[j]))/(time_array[j]*1.0)
                temp_number_list = getCoverageIndex(bitarray.to01(bitarray(detected_mu)&bitarray(coverage_array[j])),coverage_array[j])
                temp_number = getAllCount(temp_number_list)/(time_array[j]*1.0)
            if temp_number > max_number and sametestcase_list[j] not in addtional_order:
                max_order = j
                max_number = temp_number
            else:
                continue
        if max_order == int(-1):
            detected_mu = detected_mu_init
            for j in range(len(sametestcase_list)):
                if sametestcase_list[j] not in addtional_order:
                    #temp_index = testsuitlist_old.index(sametestcase_list[j])
                    #temp_number = bitdiff(bitarray(detected_mu)&bitarray(coverage_array[j]),bitarray(coverage_array[j]))/(time_array[j]*1.0)
                    temp_number_list = getCoverageIndex(bitarray.to01(bitarray(detected_mu)&bitarray(coverage_array[j])),coverage_array[j])
                    temp_number = getAllCount(temp_number_list)/(time_array[j]*1.0)
                if temp_number > max_number and sametestcase_list[j] not in addtional_order:
                    max_order = j
                    max_number = temp_number
                else:
                    continue
            print max_order
        if max_order != int(-1):
            addtional_order.append(sametestcase_list[max_order])
            temp_list.pop(temp_list.index(sametestcase_list[max_order]))
            #detected_mu = str(bitarray(detected_mu)|bitarray(coverage_array[max_order])).split("'")[1]
            detected_mu = bitarray.to01(bitarray(detected_mu)|bitarray(coverage_array[max_order]))
            continue
        elif max_order == int(-1):
            for item in temp_list:
                addtional_order.append(item)
            break

    return addtional_order

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

def divideSmallandLarge_old(temp_list,temp_number):
        sorted_list = quick_sort_time(temp_list)
        large = []
        small = []
        smalltime = []
        while True:
                temp_avg = getAllTime(sorted_list)/(temp_number - len(large))
                temp_large = []
                for item in sorted_list:
                        if item[1] > (2 * temp_avg):
                                temp_large.append(item)
                if len(temp_large) == 0:
                        break
                else:
                        for item in temp_large:
                                large.append(sorted_list.pop(sorted_list.index(item))[0])
                        continue
        #for item in large:
        #       print str(item) + ' : ' + str(TimeList[item])
        #raw_input('large and small check ...')
        for item in temp_list:
                if item not in large:
                        small.append(item)
                        smalltime.append(TimeList[item])
        return (large,small,smalltime)

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
def getCandidateTest(temp_list,temp_str):
        if len(temp_list) == 1:
                return temp_list[0]
        max_number = -1
        max_index = -1
        #cc = []
        for i in range(len(temp_list)):
                temp_test = temp_list[i]
                temp_cov = CoverageList[temp_test]
                temp_number_list = getCoverageIndex(bitarray.to01(bitarray(temp_str)&bitarray(temp_cov)),temp_cov)
                temp_number = getAllCount(temp_number_list)/(TimeList[temp_test]*1.0)
                #cc.append(getAllCount(temp_number_list))
                if temp_number > max_number:
                        max_index = i
                        max_number = temp_number
        if max_index == -1:
                #print 'do not find candidate test'
                #raw_input('getCandidateTest check...')
                return False
        else:
                #print 'candidete test : ' +  str(temp_list[max_index]) + ' - ' + str(max_number)
                #raw_input('getCandidateTest check...')
                return temp_list[max_index]

def get_Not_empty(temp_list): 
    usefullist = []
    for item in temp_list:
        if CoverageList[item].count('1') != 0:
            usefullist.append(item)
    return usefullist

def greedyAdditional(g_number, test_name, test_cov, test_time, cov_number,tl_number):
        # construct initial group - sorted_group, with the group number g_number
        # the coverage of the group is recorded in sorted_coverage
        sorted_group = []
        sorted_coverage = []
        sorted_time = []
        init_cov = ''
        toleratenumber = 0
        #groupTimeLimit = (sum(test_time)/(g_number*1.0),time_tolerate)
        
        global CoverageList
        global CoverageNumber
        global CoverageIndexList
        global TimeList
        global TimeLimit


        TestList = range(len(test_name))
        TimeList = copy.deepcopy(test_time)
        CoverageList = copy.deepcopy(test_cov)

        CoverageNumber = []
        for i in cov_number:
                CoverageNumber.append(int(i))

        #large_group,small_group,small_time = divideSmallandLarge(TestList,g_number)
        large_group,small_group,avg = divideSmallandLarge(TestList,g_number,TimeList,tl_number)
        small_number = g_number - len(large_group)
        #small_avg = sum(small_time)/(small_number*1.0)
        groupTimeLimit = (avg,(tl_number -1)*avg)

        for i in range(len(test_cov[0])):
                init_cov += '0'
        for i in range(small_number):
                sorted_group.append([])
                sorted_coverage.append(init_cov)
                sorted_time.append(0)
        #print sorted_group
        #print sorted_coverage
        
        time_sequence = quick_sort_time(small_group)        

        #sort tests to get the candidate test for each step
        small_cov = []
        small_time = []
        for i in small_group:
                small_cov.append(CoverageList[i])
                small_time.append(TimeList[i])
        #cc_list = additional_sort(small_group,small_cov,small_time)
        #cc = 0
        #checklist = []
        init_cov = '0' * len(CoverageList[0])
        detected_cov = '0' * len(CoverageList[0])
        candidate_list = copy.deepcopy(small_group)
        #candidate_list = get_Not_empty(candidate_list)
        while len(candidate_list) != 0:
                #candidate_index_list = getIndex(sorted_group)
                #candidate_test = candidate_list[0]
                #checkcov.append(detected_cov)
                candidate_test = getCandidateTest(candidate_list,detected_cov)
                #if candidate_test != cc_list[cc]:
                    #print str(candidate_test) + ' - ' + str(cc_list[cc])
                    #cc += 1
                    #raw_input('check ...')
                #print 'check point : ' + str(candidate_test)
                if candidate_test == False:
                        #print 'additional init ...'
                        detected_cov = init_cov
                        candidate_test = getCandidateTest(candidate_list,detected_cov)
                        #continue
                else:
                        pass
                #print 'check point : ' + str(candidate_list)        
                #candidate_time = test_time[test_name.index(candidate_test)]
                candidate_time = TimeList[candidate_test]
                candidate_index_list = getIndex(sorted_time,candidate_time,groupTimeLimit)

                if len(candidate_index_list) == 1:
                        candidate_index = candidate_index_list[0]
                else:
                        candidate_index = getMaxCoverage(sorted_coverage,candidate_index_list)
                cT = checkTime(sorted_group,sorted_time,(candidate_test,candidate_time,candidate_index),time_sequence[0],groupTimeLimit)
                if cT == 1:
                        add_name = candidate_test
                        #add_cov = test_cov[test_name.index(add_name)]
                        #add_time = test_time[test_name.index(add_name)]
                        add_cov = CoverageList[add_name]
                        add_time = TimeList[add_name]
                else:
                        #candidate_index = cT[1]
                        #print 'time violation ...'
                        #print candidate_test
                        add_name = time_sequence[0][0]
                        #add_cov = test_cov[test_name.index(add_name)]
                        #add_time = test_time[test_name.index(add_name)]
                        add_cov = CoverageList[add_name]
                        add_time = TimeList[add_name]
                        toleratenumber += 1
                #if add_name in checklist:
                #   print candidate_test
                #  print add_name
                # raw_input('error ...')
                #add_name = item
                #add_cov = test_cov[test_name.index(add_name)]
                #add_time = test_time[test_name.index(add_name)]
                sorted_group[candidate_index].append(add_name)
                sorted_coverage[candidate_index] = bitarray.to01(bitarray(sorted_coverage[candidate_index])|bitarray(add_cov))
                sorted_time[candidate_index] = sorted_time[candidate_index] + add_time
                #checklist.append(add_name)
                detected_cov = bitarray.to01(bitarray(detected_cov)|bitarray(add_cov))
                '''
                if detected_cov == checkcov[-1]:
                        print 'does not add any useful test ...'
                        raw_input('does not add any useful test ...')
                '''
                #checklist.append(add_name)
                #print 'check point : ' + str(checklist)
                for i in range(len(time_sequence)):
                        if time_sequence[i][0] == add_name:
                                time_sequence.pop(i)
                                break
                for i in range(len(candidate_list)):
                        if candidate_list[i] == add_name:
                                candidate_list.pop(i)
                                break

        #print '----------------------------'
        #print candidate_list
        #print sorted_time
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
        # folder for data
        path = '../data/'
        subject_list = readFile(path + 'uselist-all')
        g_n = int(sys.argv[1])
        tl_n = float(sys.argv[2])
        for subject_item in subject_list:
                #if subject_item in skip:
                #    continue
                subject_path = path + subject_item + '/'
                testlist = readFile(subject_path + 'testList')
                coveragelist = readFile(subject_path + 'stateMatrix-reduce.txt')
                numberlist = readFile(subject_path + 'reduce-index.txt')
                if os.path.exists(subject_path + 'exeTime.txt') == True:
                        timelist = readFile(subject_path + 'exeTime.txt')
                else:
                        timelist = readFile(subject_path + 'exeTime')

                #timelist = readFile(subject_path + 'time.txt')
                #print len(testlist)
                for i in range(len(timelist)):
                        timelist[i] = float(timelist[i])
                st = time.time()
                tt,tc =  greedyAdditional(g_n,testlist,coveragelist,timelist,numberlist,tl_n)
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
                f = open(subject_path + str(tl_n) + 'avg-new/group'+str(g_n)+'/greedyadditional_withtime.txt','w')
                for group_item in tt:
                        for test_item in group_item:
                                f.write(test_item + '\t')
                        f.write('\n')
                f.close()
                f_time = open(subject_path + str(tl_n) + 'avg-new/group'+str(g_n)+'/timegreedyadditional_withtime','w')
                f_time.write(str(prioritize_time))
                f_time.close()
                f_tolerate = open(subject_path + str(tl_n) + 'avg-new/group'+str(g_n)+'/tolerategreedyadditional_withtime','w')
                f_tolerate.write(str(tc))
                f_tolerate.close()
                print subject_path + ' is completed!'

