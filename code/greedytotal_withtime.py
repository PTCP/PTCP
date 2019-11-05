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
def getIndex_old(temp_list, temp_time, temp_limit):
        #min_index = 0
        min_time = 100000000
	tt = copy.deepcopy(temp_list)
	tt.sort()
	min_cccc = tt[0]
        for item in temp_list:
                if min_time > item:
			#min_cccc = item
			if item > temp_limit[0]:
				continue
			elif item < temp_limit[0] and (item + temp_time) > sum(temp_limit):
				continue
			else:
                        	#min_index = temp_list.index(item)
                        	min_time = item
                else:
                        continue
	# remain to be better...
	if min_time == 100000000:
		min_time = min_cccc
        index_list = []
        for i in range(len(temp_list)):
                if temp_list[i] == min_time:
                        index_list.append(i)
	if len(index_list) != 0:
        	return index_list
	else:
		raw_input('get candidate test index error!')

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


# get candidate group with fewest test execution time, the limit of selection criteria are as follows:
#1. the execution time for each group < group limit time (average time + bar time)
#2. the left time for each group (group limit time - selected execution time) > the max execution time among the unselected test 
#3. ...
#def getIndex_tt(temp_list, temp_time, temp_limit):
	#pass

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
                #temp_list.append((temp_name[i],temp_number/(float(temp_time[i])*1.0)))
		temp_list.append((i,temp_number/(float(TimeList[i]*1.0))))
        return quickSort(temp_list)

def quick_sort_time(temp_name):
	temp_list = []
	for i in range(len(temp_name)):
		temp_list.append((temp_name[i],TimeList[temp_name[i]]))
	return quickSort(temp_list)

def checklimit(chromosome):
        for i in chromosome:
                temp_time = 0
                for j in i:
                        temp_time += TimeList[j]
                if temp_time > TimeLimit:
                        return False
                else:
                        continue
        return True

def dropRepeat(temp_list):
        unrepeat = []
        for item in temp_list:
                if item not in unrepeat:
                        if checklimit(item):
                                unrepeat.append(item)
                        else:
                                continue
        return unrepeat

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
	
	CoverageNumber = []
    for i in cov_number:
        CoverageNumber.append(int(i))
	
	#large_group,small_group,small_time = divideSmallandLarge(TestList,g_number)
	large_group,small_group,avg = divideSmallandLarge(TestList,g_number,TimeList,avg_number)
	small_number = g_number - len(large_group)
	#small_avg = sum(small_time)/(small_number*1.0)
        groupTimeLimit = (avg,(avg_number-1) * avg)
	'''
	init_cov = '0' * len(test_cov[0])
	sorted_group = [[]] * g_number
	sorted_coverage = [init_cov] * g_number
	sorted_time = [0] * g_number
	'''
	init_cov = ''
	for i in range(len(test_cov[0])):
        init_cov += '0'
    for i in range(small_number):
        sorted_group.append([])
        sorted_coverage.append(init_cov)
        sorted_time.append(0)

	#time_sequence = quick_sort_time(test_name, test_time)
	time_sequence = quick_sort_time(small_group)
	
	candidate_list = quick_sort(small_group)
	while len(candidate_list) != 0:
		candidate_test = candidate_list[0][0]
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
			add_name = time_sequence[0][0]
			#add_cov = test_cov[test_name.index(add_name)]
			#add_time = test_time[test_name.index(add_name)]
			add_cov = CoverageList[add_name]
			add_time = TimeList[add_name]
			toleratenumber += 1
		#print sorted_group
		#print cT
		#print time_sequence[0]
		#print add_name
		#print '***'
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
		#print candidate_index
		#print sorted_group
		#print sorted_time
		#print candidate_list
		#print '--------------------------'
		#raw_input('...')
	for item in large_group:
		sorted_group.append([item])
	sorted_group_name = copy.deepcopy(sorted_group)
	for i in range(len(sorted_group_name)):
		for j in range(len(sorted_group_name[i])):
			sorted_group_name[i][j] = test_name[sorted_group[i][j]]
	return sorted_group_name,toleratenumber		

if __name__ == '__main__':
	#greedytotal(2,['t1','t2','t3','t4'],['000001','111110','101000','101000'],[50,20,70,200],20)
	#print greedytotal(2,['t1','t2','t3','t4'],['000001','111110','101000','101000'],[50,200,60,20],20)
        # folder for data
	path = '../data/'
	subject_list = readFile(path + 'uselist-all')
	g_n = int(sys.argv[1])
	tl_n = float(sys.argv[2])
	for subject_item in subject_list:
		subject_path = path + subject_item + '/'
        	testlist = readFile(subject_path + 'testList')
        	coveragelist = readFile(subject_path + 'stateMatrix-reduce.txt')
		numberlist = readFile(subject_path + 'reduce-index.txt')
		if os.path.exists(subject_path + 'exeTime.txt') == True:
                        timelist = readFile(subject_path + 'exeTime.txt')
                else:
                        timelist = readFile(subject_path + 'exeTime')
		#print len(testlist)
		for i in range(len(timelist)):
			timelist[i] = float(timelist[i])
		st = time.time()
        	tt,tc =  greedytotal(g_n,testlist,coveragelist,timelist,numberlist,tl_n)
		prioritize_time = time.time() - st

		if os.path.exists(subject_path + str(tl_n) +'avg-new/group'+str(g_n)+'/') == False:
                        os.makedirs(subject_path + str(tl_n) + 'avg-new/group'+str(g_n)+'/')
		f = open(subject_path + str(tl_n) + 'avg-new/group'+str(g_n)+'/greedytotal_withtime.txt','w')
		for group_item in tt:
			for test_item in group_item:
				f.write(test_item + '\t')
			f.write('\n')
		f.close()
		f_time = open(subject_path + str(tl_n) + 'avg-new/group'+str(g_n)+'/timegreedytotal_withtime','w')
		f_time.write(str(prioritize_time))
		f_time.close()
		f_tolerate = open(subject_path + str(tl_n) + 'avg-new/group'+str(g_n)+'/tolerategreedytotal_withtime','w')
		f_tolerate.write(str(tc))
		f_tolerate.close()
		print subject_path + ' is completed! ' + str(tc)

