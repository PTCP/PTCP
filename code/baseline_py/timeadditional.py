import os
from bitarray import bitarray
import copy
#import bitarray
from bitarray import bitdiff
import os.path
import os, errno
import time

def readFile(filepath):
    f = open(filepath)
    content = f.read()
    f.close()
    return content.splitlines()

def getCoverageIndex(a,b):
        ci_list = []
        for i in range(len(a)):
                if a[i] != b[i]:
                        ci_list.append(i)
        return ci_list

def getAllCount(temp_list,numberlist):
        count = 0
        for i in temp_list:
                count += int(numberlist[i])
        return count

#def timeadd(test_list,cov_list):
def timeadd(sametestcase_list,coverage_array,time_list,numberlist):
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
                #temp_number = bitdiff(bitarray(detected_mu)&bitarray(coverage_array[j]),bitarray(coverage_array[j]))
                temp_number_list = getCoverageIndex(bitarray.to01(bitarray(detected_mu)&bitarray(coverage_array[j])),coverage_array[j])
                temp_number = getAllCount(temp_number_list,numberlist)/(time_list[j]*1.0)
                if temp_number/(time_list[j] * 1.0) > max_number and sametestcase_list[j] not in addtional_order:
                    max_order = j
                    max_number = temp_number/(time_list[j] * 1.0)
            else:
                continue
        if max_order == int(-1):
            detected_mu = detected_mu_init
            for j in range(len(sametestcase_list)):
                if sametestcase_list[j] not in addtional_order:
                    #temp_index = testsuitlist_old.index(sametestcase_list[j])
                    #temp_number = bitdiff(bitarray(detected_mu)&bitarray(coverage_array[j]),bitarray(coverage_array[j]))
                    temp_number_list = getCoverageIndex(bitarray.to01(bitarray(detected_mu)&bitarray(coverage_array[j])),coverage_array[j])
                    temp_number = getAllCount(temp_number_list,numberlist)/(time_list[j]*1.0)
                    if temp_number/(time_list[j] * 1.0) > max_number and sametestcase_list[j] not in addtional_order:
                        max_order = j
                        max_number = temp_number/(time_list[j] * 1.0)
                else:
                    continue
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
    
def StringToFloat(string_list):
    float_list = []
    for i in string_list:
        float_list.append(float(i))
    return float_list

if __name__ == '__main__':
    root_path = '/PTCP/subjects/experiment/'
    subject_list = readFile(root_path + 'uselist-all')
    for subject in subject_list:
        #if subject in skip:
        #    continue
        subject_path = root_path + subject + '/testmethod/dynamic/'
        testlist = readFile(subject_path + 'testList')
        #coveragelist = readFile(subject_path + 'stateMatrix.txt')
        coveragelist = readFile(subject_path + 'stateMatrix-reduce.txt')
        numberlist = readFile(subject_path + 'reduce-index.txt')
        if os.path.exists(subject_path + 'exeTime.txt') == True:
            timelist = readFile(subject_path + 'exeTime.txt')
        else:
            timelist = readFile(subject_path + 'exeTime')
        timelist = StringToFloat(timelist)
        st = time.time()
        ta = timeadd(testlist,coveragelist,timelist,numberlist)    
        prioritize_time = time.time() - st
        os.system('cp ' + subject_path + 'baseline/statement/SequenceTAMethod.txt ' + subject_path + 'baseline/statement/SequenceTAMethod.bac')
        f = open(subject_path + 'baseline/statement/SequenceTAMethod.txt','w')
        for item in ta:
            f.write(str(item) + '\n')
        f.close()
        f = open(subject_path + 'baseline/statement/TimeTAMethod','w')
        f.write(str(prioritize_time))
        f.close()
        
        print subject_path + ' is completed! ' + str(prioritize_time)

