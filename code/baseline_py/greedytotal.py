import os
import time

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

def str2int(temp_strlist):
	for i in range(len(temp_strlist)):
		temp_strlist[i] = int(temp_strlist[i])
	return temp_strlist

def getAllCount(temp_str,temp_cov_index):
	temp_count = 0
	for i in range(len(temp_str)):
		if temp_str[i] == '1':
			temp_count += temp_cov_index[i]
		else:
			continue
	return temp_count

# sort with the test name and test coverage information
def quick_sort(temp_name, temp_cov,temp_cov_index):
        temp_list = []
        for i in range(len(temp_cov)):
                #temp_number = temp_cov[i].count('1')
		temp_number = getAllCount(temp_cov[i],temp_cov_index)
                temp_list.append((temp_name[i],temp_number))
        return quickSort(temp_list)

def greedytotal(test_name,test_cov,test_cov_index):
	test_cov_index = str2int(test_cov_index)
	selectedTestSequence = quick_sort(test_name,test_cov,test_cov_index)
	result_list = []
	for item in selectedTestSequence:
		result_list.append(item[0])
	return result_list

def createFolder(folder):
        if os.path.exists(folder) == False:
                os.makedirs(folder)

if __name__ == '__main__':
	root_path = '/PTCP/subjects/experiment/'
	subject_list = readFile(root_path + 'uselist-all')
	for subject in subject_list:
		subject_path = root_path + subject + '/testmethod/dynamic/'
		testlist = readFile(subject_path + 'testList')
		coveragelist = readFile(subject_path + 'stateMatrix-reduce.txt')
		numberlist = readFile(subject_path + 'reduce-index.txt')
		st = time.time()
		gt = greedytotal(testlist,coveragelist,numberlist)
		prioritize_time = time.time() - st
		createFolder(subject_path + 'baseline/statement/')
		f = open(subject_path + 'baseline/statement/SequenceTTMethod.txt','w')
		for item in gt:
			f.write(str(item) + '\n')
		f.close()
		f = open(subject_path + 'baseline/statement/TimeTTMethod','w')
		f.write(str(prioritize_time))
		f.close()
		print subject_path + ' is completed!'

