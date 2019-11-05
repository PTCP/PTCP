import os
import copy
import random
import sys
import time


def readFile(filepath):
    f = open(filepath)
    content = f.read()
    f.close()
    return content.splitlines()

def Random_P(g_number,test_name,TimeList,avg_number):
    sorted_group = []
    sorted_time = []
    toleratenumber = 0
    TestList = range(len(test_name)) 
    large_group,small_group,avg = divideSmallandLarge(TestList,g_number,TimeList,avg_number)
    small_number = g_number - len(large_group)
    #small_avg = sum(small_time)/(small_number*1.0)
    groupTimeLimit = (avg,(avg_number-1) * avg)
    
    for i in range(small_number):
        sorted_group.append([])
        #sorted_coverage.append(init_cov)
        sorted_time.append(0)
    time_sequence = quick_sort_time(small_group,TimeList)
    #candidate_list = range(len(small_group))
    candidate_list = copy.deepcopy(small_group)
    while len(candidate_list) != 0:
        #print random.randint(0,2)
        candidate_test = candidate_list[random.randint(0,len(candidate_list)-1)]
        candidate_time = timelist[candidate_test]
        candidate_index= getIndex(sorted_time,candidate_time,groupTimeLimit)
        #print candidate_list
        #print time_sequence
        #print '----------------------------'
        cT = checkTime(sorted_group,sorted_time,(candidate_test,candidate_time,candidate_index),time_sequence[0],groupTimeLimit)
        if cT == 1:
            add_name = candidate_test
            #add_cov = test_cov[test_name.index(add_name)]
            #add_time = test_time[test_name.index(add_name)]
            #add_cov = CoverageList[add_name]
            add_time = TimeList[add_name]
        else:
            add_name = time_sequence[0][0]
            #add_cov = test_cov[test_name.index(add_name)]
            #add_time = test_time[test_name.index(add_name)]
            #add_cov = CoverageList[add_name]
            add_time = TimeList[add_name]
            toleratenumber += 1
        sorted_group[candidate_index].append(add_name)
        sorted_time[candidate_index] = sorted_time[candidate_index] + add_time
        for i in range(len(time_sequence)):
            if time_sequence[i][0] == add_name:
                asd = time_sequence.pop(i)
                #print add_name
                #print asd
                break
        for i in range(len(candidate_list)):
            if candidate_list[i] == add_name:
                candidate_list.pop(i)
                break
        #print '******************'
    for item in large_group:
        sorted_group.append([item])
    sorted_group_name = copy.deepcopy(sorted_group)
    for i in range(len(sorted_group_name)):
        for j in range(len(sorted_group_name[i])):
            sorted_group_name[i][j] = test_name[sorted_group[i][j]]
    return sorted_group_name,toleratenumber







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



def getIndex(temp_list,temp_time,temp_limit):
    tt = copy.deepcopy(temp_list)
    tt.sort()
    min_time = tt[0]
    index_list = []
    for i in range(len(temp_list)):
        if temp_list[i] == min_time:
            index_list.append(i)
    if len(index_list) != 0:
        return index_list[0]
    else:
        raw_input('get candidate test index error!')



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


def quick_sort_time(temp_name,temp_time):
    temp_list = []
    for i in range(len(temp_name)):
        temp_list.append((temp_name[i],temp_time[temp_name[i]]))
    return quickSort(temp_list)


def divideSmallandLarge(temp_list,temp_number,temp_time,temp_avg):
    large = []
    small = []
    avg = sum(temp_time)/(temp_number * 1.0)
    for item in temp_list:
        if temp_time[item] > (temp_avg * avg):
            large.append(item)
        else:
            small.append(item)
    return (large,small,avg)



if __name__ == '__main__':
    path = '../data/'
    subject_list = readFile(path + 'uselist-all')
    g_n = int(sys.argv[1])
    tl_n = float(sys.argv[2])
    for subject in subject_list:
        subject_path = path + subject + '/'
        testlist = readFile(subject_path + 'testList')
        if os.path.exists(subject_path + 'exeTime.txt') == True:
            timelist = readFile(subject_path + 'exeTime.txt')
        else:
            timelist = readFile(subject_path + 'exeTime')
        for i in range(len(timelist)):
            timelist[i] = float(timelist[i])
        
        if os.path.exists(subject_path + str(tl_n) + 'avg-new/group'+str(g_n) + '/random/') == False:
            os.makedirs(subject_path + str(tl_n) + 'avg-new/group'+str(g_n) + '/random/')

        for i in range(50):
            st = time.time()
            tt,tc =  Random_P(g_n,testlist,timelist,tl_n)
            prioritize_time = time.time() - st
            f = open(subject_path + str(tl_n) + 'avg-new/group'+str(g_n)+'/random/random'+str(i)+'.txt','w')
            for group_item in tt:
                for test_item in group_item:
                    f.write(test_item + '\t')
                f.write('\n')
            f.close()
            f_tolerate = open(subject_path + str(tl_n) + 'avg-new/group'+str(g_n)+'/random/toleraterandom' + str(i),'w')
            f_tolerate.write(str(tc))
            f_tolerate.close()
            #print tt
            #print str(i) + 'th random is completed...'
            #raw_input('pause...')
        print subject_path + ' is completed! '
