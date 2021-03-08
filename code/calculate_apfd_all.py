import os
import random
import copy
from bitarray import bitarray
from bitarray import bitdiff
import time
import sys
from random import randint
from tqdm import tqdm

MaxLength = 0
TestNumber = 0
CoverageIndexList = []
CoverageList = []
CoverageNumber = []
log_flag = ''
apxcindex = []
apxcvalue = []
TestList = []

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

def checknumber(chromosome):
    count = 0
    for item in chromosome:
        count += len(item)
    return count

def getMaxLength(chromosome):
    global MaxLength
    MaxLength = 0
    for item in chromosome:
        if len(item) > MaxLength:
            MaxLength = len(item)
        else:
            continue

def getAveragePercentCoverage(chromosome):
        firstCoveredSum = 0
        getMaxLength(chromosome)
        #print 'getAPFD : ' + str(MaxLength)
        init_cov = '0' * len(CoverageList[0])
        for i in range(MaxLength):
                temp_cov = '0' * len(CoverageList[0])
                for g in range(len(chromosome)):
                        if len(chromosome[g]) <= i:
                                continue
                        else:
                            try:
                                    temp_cov = bitarray.to01(bitarray(temp_cov)|bitarray(CoverageList[chromosome[g][i]]))
                            except:
                                    print str(len(chromosome)) + ' : ' + str(g) 
                                    print str(len(chromosome[g])) + ' : ' + str(i)
                                    raw_input('getAPFD error ...')
                #diff_cov = bitdiff(bitarray(temp_cov),(bitarray(init_cov)&bitarray(temp_cov)))
                diff_list = getCoverageIndex(temp_cov,bitarray.to01(bitarray(init_cov)&bitarray(temp_cov)))
                init_cov = bitarray.to01(bitarray(temp_cov)|bitarray(init_cov))
                #firstCoveredSum += diff_cov * (i + 1)
                for df in diff_list:
                        firstCoveredSum  += ((i + 1) * CoverageNumber[df])
        try:
            AveragePercentageCoverage = 1 - firstCoveredSum/(TestNumber * sum(CoverageNumber) * 1.0) + 1/(2 * TestNumber * 1.0)
        except:
            print 'test number : ' + str(TestNumber)
            print 'coverage number : ' + str(sum(CoverageNum))
        return AveragePercentageCoverage

# use another algorithm, try to save time
def getFirstTest(chromosome):
        max_time = MaxTime
        result_list = []
        result_dict = {}
        try:
            covered_cov = range(0,len(CoverageList[chromosome[0][0]]))
        except:
            print len(CoverageList)
            print chromosome
            print checknumber(chromosome)
            raw_input('getFirstTest error...')
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
        tt = copy.deepcopy(result_dict.keys())
        tt.sort()
        init_cov = '0'*len(CoverageList[chromosome[0][0]])
        for item in tt:
                temp_cov = '0'*len(CoverageList[chromosome[0][0]])
                for test_item in result_dict[item]:
                        temp_name = test_item[1]
                        temp_cov = bitarray.to01(bitarray(temp_cov)|bitarray(CoverageList[temp_name]))
                        diff_list = getCoverageIndex(temp_cov,bitarray.to01(bitarray(init_cov)&bitarray(temp_cov)))
                        init_cov = bitarray.to01(bitarray(init_cov)|bitarray(temp_cov))
                        for i in diff_list:
                                result_list.append((test_item,CoverageNumber[i]))
        return result_list

 
def getAveragePercentCoverage_c(chromosome):
        firstCoveredSum = 0
        apxcc_count_list = getFirstTest(chromosome)
        for item in apxcc_count_list:
                firstCoveredSum += (item[0][2] * item[1])
        apxcc = firstCoveredSum * 1.0/(MaxTime * sum(CoverageNumber) * 1.0)
        return apxcc


def readTCPfile(filepath):
    f = open(filepath)
    content = f.read()
    f.close()
    result_list = []
    tt = content.splitlines()
    for i in range(len(tt)):
        temp_group = tt[i].split('\t')
        result_list.append(temp_group[0:-1])
    return result_list


# temp_list = [(apfdc,apfd)...]
def writeFile(filefolder,filepath,temp_list):
    if os.path.exists(filefolder + 'apfd_total') == False:
        os.makedirs(filefolder + 'apfd_total')
    if os.path.exists(filefolder + 'apfdc_total') == False:
        os.makedirs(filefolder + 'apfdc_total/')
    f_apfdc = open(filefolder + 'apfdc_total/' + filepath,'w')
    f_apfd  = open(filefolder + 'apfd_total/' + filepath,'w') 

    f_apfdc.write(str(temp_list[0]) + '\n')
    f_apfd.write(str(temp_list[1]) + '\n')
    f_apfdc.close()
    f_apfd.close()
    
def getAPFDC(tcp_sequence):
    #result_list = []
    apfd = getAveragePercentCoverage(tcp_sequence)
    apfdc = getAveragePercentCoverage_c(tcp_sequence)
    return (apfdc,apfd)

def writeMutant(temp_list,filepath):
    f = open(filepath,'w')
    f.write(str(temp_list))
    f.close()

def readMutant(filepath):
    f = open(filepath)
    content = f.read()
    f.close()
    return eval(content)

def TestName_Index(temp_namelist):
    result = copy.deepcopy(temp_namelist)
    for i in range(len(result)):
        for j in range(len(result[i])):
            result[i][j] = TestList.index(temp_namelist[i][j])
    return result    


if __name__ =='__main__':
    path = './subjects/experiment/'
    subject_list = readFile(path + 'uselist-all')
    gl = float(sys.argv[1])
    #gl = float(2.0)
    # the dir for coverage, e.g., 'testmethod/dynamic'
    tosem_path = str(sys.argv[1])
    # coverage granularity, e.g., state
    gran = str(sys.argv[2])

    # more argvs are refered to README.md
    for subject_item in subject_list:
        #if subject_item in pass_list:
        #    continue
        subject_path = path + subject_item + '/' + tosem_path + '/'
        path_baseline = subject_path + 'result/'
        testlist = readFile(subject_path + 'testList')
        print subject_path + ' test number : ' + str(len(testlist))
        if os.path.exists(subject_path + 'exeTime.txt') == True:
            timelist = readFile(subject_path + 'exeTime.txt')
        else:
            timelist = readFile(subject_path + 'exeTime')
        if os.path.exists(subject_path + 'mutantkill-reduce') == True:
            mulist = readFile(subject_path + 'mutantkill-reduce')
            index_list = readFile(subject_path + 'mutantkill-reduce-index')
        else:
            input('mutants read error ...')

        global TimeList
        global CoverageList
        global CoverageNumber
        global MaxTime
        global CoverageIndexList
        global TestList
        global TestNumber
        TestNumber = len(testlist)
        TestList = copy.deepcopy(testlist)
        TimeList = []
        CoverageList = copy.deepcopy(mulist)
        CoverageNumber = []
        CoverageIndexList =[]

        for i in range(len(testlist)):
            TimeList.append(float(timelist[i]))
            CoverageIndexList.append([])
            for j in range(len(CoverageList[i])):
                if CoverageList[i][j] == '1':
                    CoverageIndexList[i].append(j)
        
        MaxTime = sum(TimeList)

        for i in index_list:
            CoverageNumber.append(int(i))
        
        #group_factor = ['50','100','200']
        group_factor = ['4','8','12','16']

        for group_index in group_factor:
            tcp_filelist = ['greedytotal_withouttime.txt','greedytotal_withtime.txt','greedyadditional_withouttime.txt','greedyadditional_withtime.txt','genetic_withouttime.txt','genetic_withtime.txt','arp_withouttime.txt','arp_withtime.txt','random']
            tt_index = group_index
            
            for tcp_file in tcp_filelist:
                if tcp_file != 'random':
                #if 'time' == tcp_file[0:4]:
                #    continue
                    print tcp_file + ' is starting...'
                    st = time.time()
                    test = readTCPfile(subject_path + gran + '/' + str(gl) + 'avg-new/group' + group_index + '/' + tcp_file)
                    test_index = TestName_Index(test)
                    ss = getAPFDC(test_index)
                    writeFile(subject_path + gran + '/' + str(gl) + 'avg-new/evaluate/'+ tt_index + '/',tcp_file,ss)
                    print tcp_file + ' is completed... ' + str(time.time()-st)
                else:
                    for i in tqdm(range(50)):
                        test = readTCPfile(subject_path + gran + '/' + str(gl) + 'avg-new/group' + group_index + '/random/random' + str(i) + '.txt')
                        test_index = TestName_Index(test)
                        ss = getAPFDC(test_index)
                        writeFile(subject_path + gran + '/' + str(gl) + 'avg-new/evaluate/'+ tt_index + '/','random' + str(i) + '.txt',ss)
            
            print subject_path + ' ' + tt_index + ' is complete!'
            
        print subject_path + ' is completed!'
