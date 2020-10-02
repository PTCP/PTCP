import os
import copy
import time
import random
from random import randint
from bitarray import bitarray
#import bitarray
from bitarray import bitdiff

PopulationSize = 100
GenerationSize = 300
CrossoverProbability = 0.8
MutationProbability  = 0.1
MaxLength = 0
TestNumber = 0
CoverageDict = {}
CoverageList = []
log_flag = ''
apxcindex = []
apxcvalue = []


def readFile(filepath):
	f = open(filepath)
	content = f.read()
	f.close()
	return content.splitlines()

def getRandomList(temp_list):
	tt = copy.deepcopy(temp_list)
	random_list = []
	while len(tt) != 0:
		temp_len = len(tt)
		random_list.append(tt.pop(random.randint(0,temp_len-1)))
	return random_list

def GenerateRandomPopulation(temp_list):
	result_list = []
	while len(result_list)!= PopulationSize:
		temp_random = getRandomList(temp_list)
		if temp_random not in result_list:
			result_list.append(temp_random)
		else:
			continue
	#print 'check random init : ' + str(len(result_list))
	return result_list

# Tournament selection strategy
def championships(temp_fitness,temp_list,N):
        if len(temp_list) == N:
                return temp_list
        individuals = []
        sub_number = 4
        while len(individuals) < N:
                index_list = random.sample(range(len(temp_list)),sub_number)
                index_fitness = []
                for i in index_list:
                        index_fitness.append((temp_list[i],temp_fitness[i]))
                if chaMax(index_fitness)[0] in individuals:
                        continue
                else:
                        #print '-----------------------------------------------------'
                        #print index_fitness
                        #print chaMax(index_fitness)
                        individuals.append(chaMax(index_fitness)[0])
                        #raw_input('championships...')
        return individuals

def chaMax(temp_list):
        max_select = (0,0)
        for i in temp_list:
                if i[1] > max_select[1]:
                        max_select = (i[0],i[1])
        return max_select


# Stochastic Universal Sampling
def SUS(temp_fitness,temp_list,N):
        totalFitness = 0
        P = 0.0
        for i in range(len(temp_fitness)):
                totalFitness += temp_fitness[i]
        P = float(totalFitness/(N * 1.0))
        #print P
        start = random.random() * P
        #print start
        individuals = []
        index = 0
        Sum = temp_fitness[index]
        for i in range(N):
                pointer = start + i * P
                if Sum >= pointer:
                        individuals.append(temp_list[index])
                else:
                        index += 1
                        for j in range(index,len(temp_fitness)):
                                Sum += temp_fitness[j]
                                index = j
                                if Sum >= pointer:
                                        individuals.append(temp_list[index])
                                        break
        return individuals

def getAveragePercentCoverage(chromosome):
        #AveragePercentageCoverage = 0
	firstCoveredSum = 0
	coverageLen = len(CoverageList[chromosome[0]])
	for k in range(coverageLen):
		for i in range(len(chromosome)):
			if CoverageList[chromosome[i]][k] == '1':
				firstCoveredSum += i
				break
	AveragePercentageCoverage = 1 - firstCoveredSum/(TestNumber * coverageLen * 1.0) + 1/(2 * TestNumber * 1.0)
	return AveragePercentageCoverage


# get all the APxC and the corresponding fitness value for the populations
def getAllAveragePercentageCoverageMetricAndFitness(temp_list):
        Metric = []
        Fitness = [0]*len(temp_list)
        tt = copy.deepcopy(temp_list)
	
	global apxcindex
	global apxcvalue
        for item in temp_list:
		if item in apxcindex:
			item_index = apxcindex.index(item)
			Metric.append(apxcvalue[item_index])
		else:
                	Metric.append(getAveragePercentCoverage(item))
	apxcindex = []
	apxcvalue = []
	for i in range(len(temp_list)):
		apxcindex.append(temp_list[i])
		apxcvalue.append(Metric[i])
        # update the populationdict to record the corresponding apfxcc for the current iteration
        temp_Metric = copy.deepcopy(Metric)
        temp_Metric.sort()

        Positions = [0]*len(temp_Metric)
        for i in range(len(Metric)):
                for j in range(len(temp_Metric)):
                        if temp_Metric[j] == Metric[i]:
                                Positions[i] = j+1
                                temp_Metric[j] = -1
                                break
        for i in range(len(Positions)):
                Fitness[i] = 2 * ((Positions[i]-1)/(PopulationSize*1.0))
        return Fitness



def getSelection(temp_list):
	tt = copy.deepcopy(temp_list)
	Fitness = getAllAveragePercentageCoverageMetricAndFitness(tt)
	N = PopulationSize
	#selected_individuals = championships(Fitness,tt,N)
	selected_individuals = SUS(Fitness,tt,N)
	return selected_individuals


def getIndex(temp_test,temp_list):
        for j in range(len(temp_list)):
                #for j in range(len(item)):
		if temp_list[j] == temp_test:
			return j
		else:
			continue


def CrossOver_sort(temp_t, temp_p):
        sorted_t = []
        index_dict = {}
        for item in temp_t:
		temp_index = getIndex(item,temp_p)
		index_dict[temp_index] = item
        index_list = index_dict.keys()
        index_list.sort()
        for i in index_list:
                temp_test = index_dict[i]
		sorted_t.append(temp_test)
        return sorted_t


def CrossOver(temp_1,temp_2):
	t1 = copy.deepcopy(temp_1)
	t2 = copy.deepcopy(temp_2)
	#print t1
	#print t2
	Kth = random.randint(0,len(t1))
	#print 'Kth : ' + str(Kth)
	#print '***************************************************************'
	c1 = t1[Kth:]
	c2 = t2[Kth:]
	c1 = CrossOver_sort(c1,t2)
	c2 = CrossOver_sort(c2,t1)
	#print c1
	#print c2
	#print '------------------------------'
	for i in range(len(c1)):
		t1[Kth + i] = c1[i]
	for i in range(len(c2)):
		t2[Kth + i] = c2[i]
	#print t1
	#print t2
	#raw_input('check mutation...')
	return t1,t2
		
def getCrossOver(temp_list):
	tt = copy.deepcopy(temp_list)
	crossover_list = []
	for i in range(int(PopulationSize * CrossoverProbability)):
		temp_len = len(tt)
		crossover_list.append(tt.pop(randint(0,temp_len-1)))
	for i in range(len(crossover_list)/2):
		p1 = crossover_list[2 * i]	
		p2 = crossover_list[2 * i + 1]
		o1,o2 = CrossOver(p1,p2)
		crossover_list[2 * i] = o1
		crossover_list[2 * i + 1] = o2
	return crossover_list

def Mutation(temp_1):
	temp = copy.deepcopy(temp_1)
	Kth = random.sample(range(0,len(temp)),2)
	temp_i = temp[Kth[0]]
	temp[Kth[0]] = temp[Kth[1]]
	temp[Kth[1]] = temp_i
	return temp

def getMutation(temp_list):
	tt = copy.deepcopy(temp_list)
	mutation_list = []
	for i in range(int(PopulationSize * MutationProbability)):
                temp_len = len(tt)
                mutation_list.append(tt.pop(randint(0,temp_len-1)))
	for i in range(len(mutation_list)):
		mutant = mutation_list[i]
		mutation_list[i] = Mutation(mutant)
	return mutation_list	


def Genetic(test_list,test_cov):
	global TestNumber
        TestNumber = len(test_list)
	
	global CoverageList
        CoverageList = copy.deepcopy(test_cov)	

	Populations = [GenerateRandomPopulation(range(TestNumber))]
	for Gth in range(1,GenerationSize+1):
		original = copy.deepcopy(Populations[Gth-1])
		print 'original : ' + str(len(original))
                st = time.time()
                print 'start the ' + str(Gth) + ' th generation... '
                individuals = getSelection(original)
		print len(individuals)
                print 'selection end... ' + str(time.time()-st)
                co_list = getCrossOver(individuals)
		print len(co_list)
                print 'CrossOver end... ' + str(time.time()-st)
                mu_list = getMutation(individuals)
		print len(mu_list)
                print 'Mutation end... ' + str(time.time()-st)
		#Gth_populations = copy.deepcopy(individuals)
		#print 'ccc : ' + str(len(individuals))
		temp_Gth = copy.deepcopy(individuals)
		temp_Gth.extend(co_list)
		temp_Gth.extend(mu_list)
                Populations.append(temp_Gth)
                print str(Gth) + 'th is completed... ' + str(time.time()-st)
		#raw_input('pause...')
        return Populations[-1]




if __name__ == '__main__':
	'''
	#root_path = '/devdata/zjy/parallelTCP/subject/'
	root_path = '/devdata/zjy/parallelTCP/subject/test/subjects/'
	#subject_list = readFile(root_path + 'subject_list')
	subject_list = os.listdir(root_path)
	for subject in subject_list:
		subject_path = root_path + subject + '/'
		testlist = readFile(subject_path + 'testList')
		coveragelist = readFile(subject_path + 'stateMatrix.txt')
		st = time.time()
		ge = Genetic(testlist,coveragelist)
		prioritize_time = time.time() - st
		
		f = open(subject_path + 'baseline/statement/SequenceGeneticMethod.txt','w')
                for item in ge:
                        f.write(str(item) + '\n')
                f.close()
                f = open(subject_path + 'baseline/statement/TimeGeneticMethod','w')
                f.write(str(prioritize_time))
                f.close()
                print subject_path + ' is completed!'

	'''
	# for unit test
	testlist = readFile('/devdata/zjy/parallelTCP/subject/test/subjects/blueflood/testList')
	coveragelist = readFile('/devdata/zjy/parallelTCP/subject/test/subjects/blueflood/stateMatrix.txt')
	ge = Genetic(testlist,coveragelist)
	#print len(ge)
