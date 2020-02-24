import os
import copy
import random
from random import randint
from bitarray import bitarray
#import bitarray
from bitarray import bitdiff
import time
import sys

PopulationSize = 100
GenerationSize = 300
#PopulationSize = 5
#GenerationSize = 2
CrossoverProbability = 0.8
MutationProbability  = 0.1
MaxLength = 0
MaxTime = 0
#CoverageDict = {}
#TimeDict = {}
#CoverageIndexDict = {}
CoverageList = []
CoverageNumber = []
TimeList = []
CoverageIndexList =[]
ApxccIndex = []
ApxccValue = []
LimitTime = 0


log_flag = ''

def readFile(filepath):
	f = open(filepath)
	content = f.read()
	f.close()
	return content.splitlines()

def checknumber(temp_list):
	count = 0
	for item in temp_list:
		count += len(item)
	return count

def checkIsEmpty(temp_list):
	for item in temp_list:
		if len(item) == 0:
			return 'empty'

def checktime(st,et):
	return et-st

def getMinIndex(temp_list):
	temp_min = temp_list[0]
	temp_index = 0
	for i in range(len(temp_list)):
		if temp_min > temp_list[i]:
			temp_min = temp_list[i]
			temp_index = i
	return temp_index	

def getRandomList(temp_number, temp_name, temp_limit):
	tt = copy.deepcopy(temp_name)
	random_result = []
	random_time = []
	for i in range(temp_number):
		random_result.append([])
		random_time.append(0)
	while len(tt)!= 0:
		temp_len = len(tt)
		temp_tt = tt.pop(random.randint(0,temp_len-1))	
		temp_index = getMinIndex(random_time)
		random_result[temp_index].append(temp_tt)
		random_time[temp_index] += TimeList[temp_tt]
	return random_result 


def GenerateRandomPopulation(g_number, test_name, time_limit):
	temp_list = []
	#for i in range(PopulationSize):
	while len(temp_list) < PopulationSize:
		temp_population = getRandomList(g_number, test_name, time_limit)
		if checkIsEmpty(temp_population) == 'empty':
			continue
		if temp_population not in temp_list and checklimit(temp_population):
			temp_list.append(temp_population)
		#print 'length : ' + str(len(temp_list))
	tt = dropRepeat(temp_list)
	if len(tt) != len(temp_list):
		print 'length not equal ...'
		print len(tt)
		print len(temp_list)
		raw_input('random init error ...')
	return temp_list


#get the group coverage metric for a given chromosome
def getGroupCoverage(chromosome):
	groupMetric = []
	max_len = getMaxLen(chromosome)
	for item in chromosome:
		print len(item)
	print max_len
	raw_input('getgroupcoverage...')
	for j in range(max_len):
		init_cov = ''
		for cov in range(len(CoverageList[chromosome[0][0]])):
			init_cov += '0'
		for i in range(len(chromosome)):
			if len(chromosome[i]) == j:
				continue
			#print chromosome
			#print str(i) + ' - ' + str(j)
			init_cov = bitarray.to01(bitarray(init_cov)|bitarray(CoverageList[chromosome[i][j]]))
		groupMetric.append(init_cov)
	return groupMetric

def getMaxTime(chromosome):
	#temp_list = []
	max_count = -1
	for group_item in chromosome:
		temp_count = 0
		for test_item in group_item:
			temp_count += TimeList[test_item]
		#temp_list.append(temp_count)
		if temp_count > max_count:
			max_count = temp_count
	#print temp_list
	#print max_count
	#raw_input('...')
	return max_count

def getCoverageIndex(a,b):
	ci_list = []
	for i in range(len(a)):
		if a[i] != b[i]:
			ci_list.append(i)
	return ci_list	


# use another algorithm, try to save time
def getFirstTest(chromosome):
	#max_time = getMaxTime(chromosome)
	max_time = MaxTime
	result_list = []
	result_dict = {}
	covered_cov = range(0,len(CoverageList[0]))
	st = time.time()
	for group_item in chromosome:
		group_time  = 0
		for test_item in group_item:
			group_time += TimeList[test_item]
			temp_count = max_time - group_time + 0.5 * TimeList[test_item]
			if group_time in result_dict.keys():
				result_dict[group_time].append((group_time,test_item,temp_count))
			else:
				result_dict[group_time] = [(group_time,test_item,temp_count)]
	#print checktime(st,time.time())
	#print result_dict
	et_1 = time.time()
	tt = copy.deepcopy(result_dict.keys())
	tt.sort()
	init_cov = '0'*len(CoverageList[0])
	for item in tt:
		temp_cov = '0'*len(CoverageList[0])
		for test_item in result_dict[item]:
			temp_name = test_item[1]
			temp_cov = bitarray.to01(bitarray(temp_cov)|bitarray(CoverageList[temp_name]))
			#temp_diff = bitdiff((bitarray(init_cov)&bitarray(temp_cov)),bitarray(temp_cov))
			temp_diff_index = getCoverageIndex(bitarray.to01(bitarray(init_cov)&bitarray(temp_cov)),temp_cov)
			#if len(temp_diff_index) != temp_diff:
			#	raw_input('getFirstTest error : not equal...')
			init_cov = bitarray.to01(bitarray(init_cov)|bitarray(temp_cov))
			for i in temp_diff_index:
				result_list.append((test_item,CoverageNumber[i]))
				#result_list.add(test_item)
		#print 'diff  ---- ' + str(len(cov_diff)) + ' : ' + str(cov_diff.count('1'))
		#print 'final ---- ' + str(len(init_cov)) + ' : ' + str(init_cov.count('1'))
		#print len(result_list)
		#raw_input('get first test check...')
	et_2 = time.time()
	#print chromosome
	#print 'end time 1 : ' + str(checktime(st,et_1))
	#print 'end time 2 : ' + str(checktime(st,et_2))
	#raw_input('check time...')
	#print checktime(et_1,time.time())
	return result_list		
	#raw_input('check...')
				
def getAveragePercentCoverage(chromosome):
	firstCoveredSum = 0
	st = time.time()
	apxcc_count_list = getFirstTest(chromosome)
	#max_group_time = getMaxTime(chromosome)
	for item in apxcc_count_list:
		firstCoveredSum += (item[0][2] * item[1])
	apxcc = firstCoveredSum * 1.0/(MaxTime * sum(CoverageNumber))
	return apxcc
	

# get all the APxC and the corresponding fitness value for the populations
def getAllAveragePercentageCoverageMetricAndFitness(temp_list):
	Metric = []
	Fitness = [0]*len(temp_list)
	tt = copy.deepcopy(temp_list)
	st = time.time()
	for item in temp_list:
		if item not in ApxccIndex:
			#apfdst = time.time()
			Metric.append(getAveragePercentCoverage(item))
			#print 'caculate apfd time : ' + str(time.time()-apfdst)
		else:
			Metric.append(ApxccValue[ApxccIndex.index(item)])
	# update the populationdict to record the corresponding apfxcc for the current iteration
	global ApxccIndex
	global ApxccValue
	ApxccIndex = []
	ApxccValue = []
	for i in range(len(temp_list)):
		ApxccIndex.append(temp_list[i])
		ApxccValue.append(Metric[i])
	temp_Metric = copy.deepcopy(Metric)
	temp_Metric.sort()
	'''
	sorted_populations = []
	for apxc in temp_Metric:
		sorted_populations.append(tt.pop(pop.index(apxc)))
	for position in range(len(sorted_populations)):
		temp_fitness = 2 * (position/(PopulationSize * 1.0))
		Fitness.append((sorted_populations[position],temp_fitness))
	'''
	#print '2 : ' + str(checktime(st,time.time()))
	Positions = [0]*len(temp_Metric)
	for i in range(len(Metric)):
		for j in range(len(temp_Metric)):
			if temp_Metric[j] == Metric[i]:
				Positions[i] = j+1
				temp_Metric[j] = -1
				break
	for i in range(len(Positions)):
		Fitness[i] = 2 * ((Positions[i]-1)/(PopulationSize*1.0))
	#print '3 : ' + str(checktime(st,time.time()))
	#raw_input('check all time...')
	return Fitness


def getMaxAveragePercentageCoverage(temp_list):
        Metric = {}
        #tt = copy.deepcopy(temp_list)
        for item in temp_list:
                apxc = getAveragePercentCoverage(item)
                #print apxc
                if apxc not in Metric.keys():
                        Metric[apxc] = [item]
                else:
                        Metric[apxc].append(item)
        tt = Metric.keys()
        tt.sort()
        return Metric[tt[-1]]



# Stochastic Universal Sampling
def SUS(temp_fitness,temp_list,N):
	totalFitness = 0
	P = 0
	for i in range(len(temp_fitness)):
		totalFitness += temp_fitness[i]
	P = int(totalFitness/N)
	print P
	start = random.randint(0,P)
	individuals = []
	index = 0
	Sum = temp_fitness[index]
	for i in range(N):
		pointer = start + i * P
		if Sum >= pointer:
			individuals.append(index)
		else:
			index += 1
			for j in range(index,len(temp_fitness)):
				Sum += temp_fitness[j]
				index = j
				if Sum >= pointer:
					individuals.append(j)
					break
	return individuals

def chaMax(temp_list):
	max_select = (0,0)
	for i in temp_list:
		if i[1] > max_select[1]:
			max_select = (i[0],i[1])
	return max_select

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

# Tournament selection strategy
def championships(temp_fitness,temp_list,N):
	#tt = copy.deepcopy(temp_list)
	#tt = set(tt)
	#print len(tt)
	#print len(temp_list)
	#print N	
	#tt = dropRepeat(temp_list)
	#print 'has : ' + str(len(tt)) + ' different individuals'
	
	#print len(temp_list)
	if len(temp_list) < N or len(temp_list) == N:
		#print 'less individuals ...'
		return temp_list
	#raw_input('championships check ...')
	#tt_fitness = []
	#for i in range()
	individuals = []
	#if len(temp_list) < N:
		#individuals = copy.deepcopy(temp_list)
		#return individuals
	sub_number = 4
	while len(individuals) < N:
		#print '12121'
		index_list = random.sample(range(len(temp_list)),sub_number)
		index_fitness = []
		for i in index_list:
			index_fitness.append((temp_list[i],temp_fitness[i]))
		selected = chaMax(index_fitness)[0]
		if selected in individuals:
			#print 'already selected ...'
			continue
		elif checklimit(selected) == False:
			#print 'time limit ...'
			continue
		else:
			#print '-----------------------------------------------------'
			#print index_fitness
			#print chaMax(index_fitness)
			individuals.append(selected)
			#raw_input('championships...')	
	return individuals

def Selection(N,temp_list):
	#selected__individuals = []
	# randomly select individuals, only for quick coding...
	tt = copy.deepcopy(temp_list)
	tt = dropRepeat(tt)
	#print 'before selection : ' + str(len(tt))
	Fitness = getAllAveragePercentageCoverageMetricAndFitness(tt)
	#print 'check point 1 ...'
	selected_individuals = championships(Fitness,tt,N)
	#print 'after selection : ' + str(len(selected_individuals))
	#print 'check point 2 ...'
	return selected_individuals

def getIndex(temp_test,temp_list):
	for item in temp_list:
		for j in range(len(item)):
			if item[j] == temp_test:
				return j
			else:
				continue
def getTestCoverage(c):
        count = 0
        for i in range(len(c)):
                if c[i] == '1':
                        count += CoverageNumber[i]
        return count

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

def getSortedTest(temp_list):
	tt = []
	for item in temp_list:
		tt.append((item,getTestCoverage(CoverageList[item])))
	return quickSort(tt)

def quick_sort_time(temp_name):
        temp_list = []
        for i in range(len(temp_name)):
                temp_list.append((temp_name[i],TimeList[temp_name[i]]))
        return quickSort(temp_list)

def getTestTime(temp_list):
	resultdict = {}
	for item in temp_list:
		temp_time = 0
		for i in item:
			resultdict[i] = temp_time
			temp_time += TimeList[i]
	return resultdict

# sort the item in temp_t with its corresponding execution time in temp_p
def CrossOver_Sort(temp_t, temp_p):
	sorted_t = []
	index_dict = {}
	timedict = getTestTime(temp_p)
	for item in temp_t:
		temptime = timedict[item]
		if temptime not in index_dict.keys():
			index_dict[temptime] = [item]
		else:
			index_dict[temptime].append(item)
	index_list = index_dict.keys()
	index_list.sort()
	for i in index_list:
		temp_list = index_dict[i]
		if len(temp_list) == 1:
			sorted_t.append(temp_list[0])
		else:
			temp_list = getSortedTest(temp_list)
			for item in temp_list:
				sorted_t.append(item[0])
	return sorted_t

def getMinAll(temp_1,temp_2):
	temp_min = 1000000
	for item in temp_1:
		if len(item) < temp_min:
			temp_min = len(item)
	for item in temp_2:
		if len(item) < temp_min:
			temp_min = len(item)
	return temp_min

def getGroupTime(temp_list):
	time_list = []
	#tt = copy.deepcopy(temp_list)
	for group_item in temp_list:
		temp_count = 0
		#print group_item
		for test_item in group_item:
			temp_count += TimeList[test_item]
		time_list.append(temp_count)
	time_list.sort()
	return time_list

def getTime(temp_list):
	time_count = 0
	for test_item in temp_list:
		time_count += TimeList[test_item]
	return time_count

def getGroupIndex(temp_list,time_poke):
	index_dict = {}
	for group_item in range(len(temp_list)):
		temp_count = 0
		for test_item in temp_list[group_item]:
			temp_count += TimeList[test_item]
			if temp_count < time_poke:
				continue
			else:
				index_dict[group_item] = temp_list[group_item].index(test_item)
				break
	return index_dict

def getGroupIndexList(temp_list,time_poke):
	index_list = [None]*len(temp_list)
	for i in range(len(temp_list)):
		temp_count = 0
		for j in range(len(temp_list[i])):
			temp_count += TimeList[temp_list[i][j]]
			if temp_count < time_poke:
				continue
			else:
				index_list[i] = j
				break
	return index_list

def getIndexByTime(temp_list,time_poke):
	temp_count = 0
	index_time = -1
	for test_item in temp_list:
		temp_count += TimeList[test_item]
		index_time += 1
		if temp_count < time_poke:
			continue
		else:
			break
	return index_time	

# temp_test1: first candidate test
# temp_test2: unselected test with maximum execution time
# getCandidate(o1_time,o1_cov,temp_limit,cov_test)
def getCandidate(temp_list,temp_cov,temp_limit,temp_test1):
	tt = copy.deepcopy(temp_list)
	tt.sort()
	can_index = -1
	max_count = -1
	for i in range(len(temp_list)):
		if temp_list[i] == tt[0]:
			temp_count = int(bitarray(temp_cov[i]).count())
			if temp_count > max_count:
				max_count = temp_count
				can_index = i
	if can_index == -1:
		raw_input('get candidate group index error ...')
	return (temp_test1,can_index)


def checkindex(a,b):
	for key in a.keys():
		if a[key] == b[key]:
			continue
		else:
			print str(key) + ' error...'
			return str(key) + ' error...'
	

def randomlist(templist):
	random_list = []
	tt = copy.deepcopy(templist)
	while len(tt) > 0:
		temptest = tt.pop(random.randint(0,len(tt)-1))
		random_list.append(temptest)
	return random_list


def CrossOver_coarsness_old(temp_list,temp_limit):
	crossover_list = copy.deepcopy(temp_list)
	result_list = []
	CovLen = len(CoverageList[temp_list[0][0][0]])
	for crossover_index in range(len(crossover_list)/2):
		#Kth = random.randint(0,MaxLength-1)
		cst = time.time()
		p1 = crossover_list[crossover_index*2]
		p2 = crossover_list[crossover_index*2+1]
		#Ktime = random.randint(0,getMax(getGroupTime(p1)[-1],getGroupTime(p2)[-1]))
		Ktime = random.random() * getMax(getGroupTime(p1)[-1],getGroupTime(p2)[-1])
		#p1_Kth = getGroupIndex(p1,Ktime)
		p1_Kth = getGroupIndexList(p1,Ktime)
		#p2_Kth = getGroupIndex(p2,Ktime)
		p2_Kth = getGroupIndexList(p2,Ktime)
		#checkindex(p1_Kth,p1_tt)
		#checkindex(p2_Kth,p2_tt)
		t1 = []
		t2 = []
		o1 = []
		o2 = []
		o1_time = [0] * len(p1)
		o2_time = [0] * len(p2)
		o1_cov = []
		o2_cov = []
		for i in range(len(p1)):
			if p1_Kth[i] == None:
				continue
			else:
				for j in p1[i][p1_Kth[i]:]:
					t1.append(j)
		for i in range(len(p2)):
			#if i not in p2_Kth.keys():
			if p2_Kth[i] == None:
				continue
			else:
				for j in p2[i][p2_Kth[i]:]:
					t2.append(j)
		t1 = CrossOver_Sort(t1,p2)
		t2 = CrossOver_Sort(t2,p1)
		# construct the new individuals : o1 and o2
		for i in range(len(p1)):
			o1.append(p1[i][0:p1_Kth[i]])
			o2.append(p2[i][0:p2_Kth[i]])
			try:
				if CovLen != len(CoverageList[0]):
					print CovLen
					print len(CoverageList[0])
					raw_input('crossover error...')
			except:
				print CovLen
				print p1
				raw_input('crossover exception error')
			o1_cov.append('0'*CovLen)
			o2_cov.append('0'*CovLen)
			for j in o1[i]:
				o1_time[i] += TimeList[j]
                                o1_cov[i] = bitarray.to01(bitarray(o1_cov[i])|bitarray(CoverageList[j]))
			for j in o2[i]:
				o2_time[i] += TimeList[j]
				o2_cov[i] = bitarray.to01(bitarray(o2_cov[i])|bitarray(CoverageList[j]))
		#print 'check point 3 : ' + str(time.time()-cst)
		cc1 = copy.deepcopy(o1)
		cc2 = copy.deepcopy(o2)
		while len(t1) > 0:
                        cov_test = t1[0]
			time_test = time_sequence_t1[0][0]
                        (candidate_test,candidate_group) = getCandidate(o1_time,o1_cov,temp_limit,cov_test,time_test)
                        o1_time[candidate_group] += TimeList[candidate_test]
                        o1_cov[candidate_group] = bitarray.to01(bitarray(CoverageList[candidate_test])|bitarray(o1_cov[candidate_group]))
                        o1[candidate_group].append(candidate_test)
			t1.pop(t1.index(candidate_test))
			time_sequence_t1.pop(time_sequence_t1.index((candidate_test,TimeList[candidate_test])))
                while len(t2) > 0:
                        cov_test = t2[0]
			time_test = time_sequence_t2[0][0]
                        (candidate_test,candidate_group) = getCandidate(o2_time,o2_cov,temp_limit,cov_test,time_test)
                        o2_time[candidate_group] += TimeList[candidate_test]
                        o2_cov[candidate_group] = bitarray.to01(bitarray(CoverageList[candidate_test])|bitarray(o2_cov[candidate_group]))
                        o2[candidate_group].append(candidate_test)
			t2.pop(t2.index(candidate_test))
			time_sequence_t2.pop(time_sequence_t2.index((candidate_test,TimeList[candidate_test])))
		#print 'check point 4 : ' + str(time.time()-cst)
		result_list.append(o1)
		result_list.append(o2)
	return result_list

def CrossOver_coarsness(temp_list,temp_limit):
        crossover_list = copy.deepcopy(temp_list)
        result_list = []
        CovLen = len(CoverageList[temp_list[0][0][0]])
        for crossover_index in range(len(crossover_list)/2):
                cst = time.time()
                p1 = crossover_list[crossover_index*2]
                p2 = crossover_list[crossover_index*2+1]
                Ktime = random.random() * getMax(getGroupTime(p1)[-1],getGroupTime(p2)[-1])
                p1_Kth = getGroupIndexList(p1,Ktime)
                p2_Kth = getGroupIndexList(p2,Ktime)
                t1 = []
                t2 = []
                o1 = []
                o2 = []
                o1_time = [0] * len(p1)
                o2_time = [0] * len(p2)
                o1_cov = []
                o2_cov = []
                for i in range(len(p1)):
                        if p1_Kth[i] == None:
                                continue
                        else:
                                for j in p1[i][p1_Kth[i]:]:
                                        t1.append(j)
                for i in range(len(p2)):
                        #if i not in p2_Kth.keys():
                        if p2_Kth[i] == None:
                                continue
                        else:
                                for j in p2[i][p2_Kth[i]:]:
                                        t2.append(j)
                #print 'check point 1 : ' + str(time.time()-cst)
		t1 = CrossOver_Sort(t1,p2)
                t2 = CrossOver_Sort(t2,p1)
		tt1 = copy.deepcopy(t1)
		tt2 = copy.deepcopy(t2)
                #print 'check point 2 : ' + str(time.time()-cst)
                # construct the new individuals : o1 and o2
                for i in range(len(p1)):
                        o1.append(p1[i][0:p1_Kth[i]])
                        o2.append(p2[i][0:p2_Kth[i]])
                        o1_cov.append('0'*CovLen)
                        o2_cov.append('0'*CovLen)
                        for j in o1[i]:
                                o1_time[i] += TimeList[j]
                                o1_cov[i] = bitarray.to01(bitarray(o1_cov[i])|bitarray(CoverageList[j]))
                        for j in o2[i]:
                                o2_time[i] += TimeList[j]
                                o2_cov[i] = bitarray.to01(bitarray(o2_cov[i])|bitarray(CoverageList[j]))
                #print 'check point 3 : ' + str(time.time()-cst)
                while len(t1) > 0:
                        cov_test = t1[0]
                        (candidate_test,candidate_group) = getCandidate(o1_time,o1_cov,temp_limit,cov_test)
                        o1_time[candidate_group] += TimeList[candidate_test]
                        o1_cov[candidate_group] = bitarray.to01(bitarray(CoverageList[candidate_test])|bitarray(o1_cov[candidate_group]))
                        o1[candidate_group].append(candidate_test)
                        t1.pop(t1.index(candidate_test))
		while len(t2) > 0:
                        cov_test = t2[0]
                        (candidate_test,candidate_group) = getCandidate(o2_time,o2_cov,temp_limit,cov_test)
                        o2_time[candidate_group] += TimeList[candidate_test]
                        o2_cov[candidate_group] = bitarray.to01(bitarray(CoverageList[candidate_test])|bitarray(o2_cov[candidate_group]))
                        o2[candidate_group].append(candidate_test)
                        t2.pop(t2.index(candidate_test))
                #print 'check point 4 : ' + str(time.time()-cst)
                result_list.append(o1)
                result_list.append(o2)
		'''
		if checkIsEmpty(o1) == 'empty' or checkIsEmpty(o2) == 'empty':
			print p1_Kth
			print p2_Kth
			print tt1
			print tt2
			print '------------------------'
			print p1
			print p2
			print '--------------------------'
			print o1
			print o2
			raw_input('crossover empty error ...')
		'''
        return result_list


def getMin(temp1,temp2):
	if temp1 < temp2:
		return temp1
	else:
		return temp2

def getMax(temp1,temp2):
	#temp1 = int(temp1)
	#temp2 = int(temp2)
	if temp1 < temp2:
		return temp2
	else:
		return temp1

def CrossOver_fine(temp_list):
	crossover_list = copy.deepcopy(temp_list)
	result_list = []
	for crossover_index in range(len(crossover_list)/2):
		p1 = crossover_list[2*crossover_index]
                p2 = crossover_list[2*crossover_index+1]
		# Mth : randomly select one group to execute crossover
		Mth = random.randint(0,len(crossover_list[0])-1)
		#Ktime = random.randint(0,getMax(getTime(p1[Mth]),getTime(p2[Mth])))
		Ktime = random.random() * getMax(getTime(p1[Mth]),getTime(p2[Mth]))
		Kth_1 = getIndexByTime(p1[Mth],Ktime)
		Kth_2 = getIndexByTime(p2[Mth],Ktime)
		t1 = []
		t2 = []
		o1 = []
		o2 = []
		for i in p1[Mth][Kth_1:]:
			t1.append(i)
		for i in p2[Mth][Kth_2:]:
			t2.append(i)
		t1 = CrossOver_Sort(t1,p2)
		t2 = CrossOver_Sort(t2,p1)
		# construct the new individuals : o1 and o2
		for i in p1:
			if p1.index(i) != Mth:
				o1.append(i)
			else:
				o1.append(i[0:Kth_1])
		for i in p2:
			if p2.index(i) != Mth:
				o2.append(i)
			else:
				o2.append(i[0:Kth_2])
		for j in range(Kth_1-1,len(p1[Mth])):
			if len(t1) == 0:
				break
			else:
				o1[Mth].append(t1.pop(0))
		#print Kth_2
		#print p2[Mth]
		for j in range(Kth_2-1,len(p2[Mth])):
			if len(t2) == 0:
				break
			else:
				o2[Mth].append(t2.pop(0))
		#tt.append(o1)
		#tt.append(o2)
		result_list.append(o1)
		result_list.append(o2)
	return result_list

def Mutation_coarsness(temp_list):
        mutate_list = copy.deepcopy(temp_list)
	result_list = []
        for mutate_index in range(len(mutate_list)):
                Mth = random.sample(range(0,len(mutate_list[mutate_index])-1),2)
                p1 = mutate_list[mutate_index]
		try:
			#getGroupIndex(p1,Ktime)
			#getIndexByTime(p2[Mth],Ktime)
			#(getTime(p1[Mth])
                	#Kth1 = randint(0,len(p1[Mth[0]])-1)
                	#Kth2 = randint(0,len(p1[Mth[1]])-1)
			Ktime1 = random.random() * getTime(p1[Mth[0]])
			Ktime2 = random.random() * getTime(p1[Mth[1]])
			Kth1 = getIndexByTime(p1[Mth[0]],Ktime1)
			Kth2 = getIndexByTime(p1[Mth[1]],Ktime2)
		except:
			for item in p1:
				print item
			print '--------------------------------'
			print p1[Mth[0]]
			print p1[Mth[1]]
			raw_input('error...')
                #print str(Mth) + ' : ' + str(Kth1)
                #print p1[Mth[0]]
                #print p1[Mth[0]][Kth1]
                #print p1[Mth[1]][Kth2]
		try:
                	temp = p1[Mth[0]][Kth1]
                	p1[Mth[0]][Kth1] = p1[Mth[1]][Kth2]
                	p1[Mth[1]][Kth2] = temp
		except:
			print 'p1 : ' + str(p1)
			#print 'p2 : ' + str(p2)
			raw_input('mutation coarsness error ...')
                result_list.append(p1)
        return result_list


def Mutation_fine(temp_list):
	mutate_list = copy.deepcopy(temp_list)
	result_list = []
	for mutate_index in range(len(mutate_list)):
		p1 = mutate_list[mutate_index]
		while True:
			Mth = randint(0,len(mutate_list[mutate_index])-1)
			if len(p1[Mth]) == 1:
				continue
			else:
				break
			#Kth = random.sample(range(0,len(p1[Mth])),2)
		Ktime1 = random.random() * getTime(p1[Mth])
		Kth1 = getIndexByTime(p1[Mth],Ktime1)
		while True:
			Ktime2 = random.random() * getTime(p1[Mth])
			Kth2 = getIndexByTime(p1[Mth],Ktime2)
			if Kth2 == Kth1:
				continue
			elif Kth1 != Kth2:
				Kth = (Kth1,Kth2)
				break
		temp = p1[Mth][Kth[0]]
		p1[Mth][Kth[0]] = p1[Mth][Kth[1]]
		p1[Mth][Kth[1]] = temp
		#tt.append(p1)
		result_list.append(p1)
	return result_list


def checklimit_all(t_list,t_limit):
	error_list = []
	for item in t_list:
		for i in item:
			#print i
			temptime = 0
			for j in i:
				#print str(j) + ' : ' + str(TimeList[j])
				#print TimeList[j]
				temptime += TimeList[j]
			if temptime > sum(t_limit):
				#print '----------'
				#print temptime
				#print sum(t_limit)
				#raw_input('checklimit...')
				error_list.append(item)
				break
	return error_list


# carry out crossover operation
def CrossOver(temp_list,temp_limit):
	tt = copy.deepcopy(temp_list)
        crossover_list = []
        for i in range(int(PopulationSize * CrossoverProbability)):
                temp_len = len(tt)
		try:
                	crossover_list.append(tt.pop(randint(0,temp_len-1)))
		except:
			print int(PopulationSize * CrossoverProbability)
			print i
			print temp_len
			print 'length of input : ' + str(len(temp_list))
			raw_input('crossover error ...')

	crossover_list = CrossOver_coarsness(crossover_list,temp_limit)
	#if len(checkEmpty(crossover_list)) != 0:
	#	print 'crossover coarsness error ...'
	#cc = checklimit(crossover_list,temp_limit)
	#print str(len(cc)) + ' : out of limit'
	#raw_input('check limit...')
	# to crossover the individuals between two groups
	crossover_list = CrossOver_fine(crossover_list)
	#if len(checkEmpty(crossover_list)) != 0:
        #        print 'crossover fine error ...'
	return crossover_list

# carry out mutation operation
def Mutation(temp_list,temp_limit):
	tt = copy.deepcopy(temp_list)
        mutation_list = []
        for i in range(int(PopulationSize * MutationProbability)):
		temp_len = len(tt)
                mutation_list.append(tt.pop(randint(0,temp_len-1)))

	# to mutate the individuals between two groups
	mutation_list = Mutation_coarsness(mutation_list)
	# to mutate the individuals within one group
	mutation_list = Mutation_fine(mutation_list)
	#temp_list.extend(mutation_list)
	return mutation_list

def checkTest(temp_list):
	for item in temp_list:
		if checknumber(item) != 87:
			pass
			#print 'missing test...'

def randomselect(temp_list):
	result = []
	while len(result) < 100:
		temp_index = random.randint(0,len(temp_list)-1)
		if temp_list[temp_index] not in result:
			result.append(temp_list[temp_index])
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
	#	print str(item) + ' : ' + str(TimeList[item])
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


def checkEmpty(temp_list):
	empty_list = []
	for item in temp_list:
		if checkIsEmpty(item) == 'empty':
			empty_list.append(item)
	return empty_list

def Genetic_sort(g_number, test_name, test_cov, test_cov_number, test_time, tl_number):
	# record the basic information
	# MaxLength : the maximum length of groups in populations
	global MaxTime
	MaxTime = sum(test_time)
	# CoverageDict : record each test and its corresponding coverage information
	global CoverageList
	global CoverageNumber
	global CoverageIndexList
	global TimeList
	global TimeLimit

	TestList = range(len(test_name))
	CoverageList = copy.deepcopy(test_cov)
	TimeList = copy.deepcopy(test_time)
	for i in range(len(test_name)):
		CoverageIndexList.append([])
		for j in range(len(CoverageList[i])):
			if CoverageList[i][j] == '1':
				CoverageIndexList[i].append(j)
	CoverageNumber = []
	for i in test_cov_number:
		CoverageNumber.append(int(i))

	groupAverageTime = sum(test_time)/(g_number*1.0)
	#groupTimeLimit = (groupAverageTime,groupAverageTime)
	#large_group,small_group,small_time = divideSmallandLarge(TestList,g_number)
	large_group,small_group,avg = divideSmallandLarge(TestList,g_number,TimeList,tl_number)
	small_number = g_number - len(large_group)
	#small_avg = sum(small_time)/(small_number*1.0)
	groupTimeLimit = (avg,(tl_number - 1)*avg)
	TimeLimit = sum(groupTimeLimit)
	#print small_avg
	#print small_number
	#print groupTimeLimit
	#for item in large_group:
	#	print str(item) + ' : ' + str(TimeList[item]) 
		
	# initial the first population
	Populations = [GenerateRandomPopulation(small_number, small_group, groupTimeLimit)]
	#cl = checklimit_all(Populations[0],groupTimeLimit)
	#print 'cl : ' + str(len(cl))
	# start the the whole process for the number of generations
	for Gth in range(1,GenerationSize+1):
		print 'start the ' + str(Gth) + ' th generation...'
		select_st = time.time()
		#print 'length of last generation ' + str(Gth-1) + ' : ' + str(len(Populations[Gth-1]))
		individuals = Selection(PopulationSize,Populations[Gth-1])
		#print 'length of selection : ' + str(len(individuals))
		#print 'selection number : ' + str(len(individuals))
		#individuals = randomselect(Populations[Gth-1])
		select_et = time.time()
		#checkTest(individuals)
		#print 'selection end : ' + str(checktime(select_st,select_et))
		#crossover_st = time.time()
		crossover_individuals = CrossOver(individuals,groupTimeLimit)
		#crossover_et = time.time()
		#checkTest(individuals)
		#print 'CrossOver end : ' + str(time.time()-select_st)
		#raw_input('pause...')
		#mutation_st = time.time()
		mutation_individuals = Mutation(individuals,groupTimeLimit)
		#mutation_et = time.time()
		#checkTest(individuals)
		#print 'Mutation end : ' + str(time.time()-select_st)
		#if len(checkEmpty(crossover_individuals)) !=0:
		#	print 'crossover error ...'
		#if len(checkEmpty(mutation_individuals)) !=0:
                #        print 'mutation error ...'
		individuals.extend(crossover_individuals)
		individuals.extend(mutation_individuals)
		Populations.append(individuals)
		#checkTest(individuals)
		#print len(individuals[0])
		#print 'after number : ' + str(len(dropRepeat(individuals)))
		print log_flag + ' : ( ' + str(len(individuals)) + ' ) ' + str(Gth) + 'th is completed... ' + str(checktime(select_st,time.time()))
		#raw_input('pause...')
	#return Populations
	population_last = copy.deepcopy(Populations[-1])
	if len(large_group) == 0:
		return population_last
	else:
		for item in population_last:
			for large in large_group:
				item.append([large])
		return population_last
	

# just for testing 
def randomInitCoverage(size_test,size_cov):
	cov_list = []
	for i in range(size_test):
		temp_cov = ''
		for j in range(size_cov):
			temp_cov += str(random.randint(0,1))
		cov_list.append(temp_cov)
	return cov_list



if __name__ == '__main__':
	path = '/PTCP/subject/experiment/'
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
        subject_list = readFile(path + 'uselist-all')
	for subject_item in subject_list:
                if subject_item == 'camel-core' or subject_item == 'commons-math':
                    continue
		subject_path = path + subject_item + '/' + tosem_path + '/'
		global log_flag
		log_flag = subject_item
        	testlist = readFile(subject_path + 'testList')
                if len(testlist) < (g_n + 2):
                    continue
		print subject_item +  ' has tests : ' + str(len(testlist))
        	coveragelist = readFile(subject_path + gran + 'Matrix-reduce.txt')
		numberlist = readFile(subject_path + gran + '-reduce-index.txt')
		#timelist = readFile(subject_path + 'time.txt')
		if os.path.exists(subject_path + 'exeTime.txt') == True:
                        timelist = readFile(subject_path + 'exeTime.txt')
                else:
                        timelist = readFile(subject_path + 'exeTime')

		for i in range(len(timelist)):
			timelist[i] = float(timelist[i])
		st = time.time()
        	tt = Genetic_sort(g_n,testlist,coveragelist,numberlist,timelist,tl_n)
		ss = getMaxAveragePercentageCoverage(tt)
		l = len(ss)
		ss = ss[randint(0,l-1)]
		#print ss
		result_list = copy.deepcopy(ss)
		for group_index in range(len(result_list)):
			for test_index in range(len(result_list[group_index])):
				result_list[group_index][test_index] = testlist[ss[group_index][test_index]]
		prioritize_time = time.time() - st
		
		if os.path.exists(subject_path + gran + '/' + str(tl_n) + 'avg-new/group'+str(g_n)+'/') == False:
			os.makedirs(subject_path + gran + '/' + str(tl_n) + 'avg-new/group'+str(g_n)+'/')
			
		f = open(subject_path + gran + '/' + str(tl_n) + 'avg-new/group'+str(g_n)+'/genetic_withtime.txt','w')
		for group_item in result_list:
			for test_item in group_item:
				#print test_item
				f.write(test_item + '\t')
			f.write('\n')
		f.close()
		f_time = open(subject_path + gran + '/' + str(tl_n) + 'avg-new/group'+str(g_n)+'/timegenetic_withtime','w')
		f_time.write(str(prioritize_time))
		f_time.close()
		
		print subject_path + ' is completed! '


