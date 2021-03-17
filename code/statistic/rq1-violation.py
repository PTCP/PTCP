import os
import math
import numpy as np
import csv
from collections import defaultdict
import copy
import sys


def tree(): return defaultdict(tree)

def readFile(filepath):
    f = open(filepath)
    content = f.read()
    f.close()
    return content.splitlines()

def countnumber(templist):
    count = 0
    for item in templist:
        count += len(item)
    return count

def readTCPfile(filepath,checknum):
        f = open(filepath)
        content = f.read()
        f.close()
        result_list = []
        tt = content.splitlines()
        for i in range(len(tt)):
                temp_group = tt[i].split('\t')
                result_list.append(temp_group[0:-1])
        count = countnumber(result_list)
        if count != checknum:
            print filepath + ' : not equal !'
        return result_list

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

def divideSmallandLarge(temp_list,temp_number,timedict,totaltime,timeconstraint):
        large = []
        small = []
        if len(temp_list) != len(timedict.keys()):
                raw_input('divideSmallandLarge not equal error ...')
        avg = totaltime/(temp_number * 1.0)
        for item in temp_list:
                if timedict[item] > (timeconstraint*avg):
                        large.append(item)
                else:
                        small.append(item)
        return (large,small,avg)

def getGroupTime(temp_list,timedict):
        count = 0
        for item in temp_list:
            #temp_time = TimeList[NameList.index(item)]
            temp_time = timedict[item]
            count += temp_time
        return count

def getTestingTime(temp_list,timedict):
    max_time = 0
    for item in temp_list:
        temp_time = 0
        for t_item in item:
            temp_time += timedict[t_item]
        max_time = max(max_time,temp_time)
    return max_time

def checklimit(temp_list,temp_large,temp_limit,timedict):
        tt = copy.deepcopy(temp_list)
        for item in temp_large:
                if [item] in tt:
                        tt.pop(tt.index([item]))
                        continue
                else:
                        return False
        if len(tt) != (len(temp_list) - len(temp_large)):
                raw_input('check limit error : not equal ...')
        for item in tt:
                temp_time = getGroupTime(item,timedict)
                if temp_time > temp_limit:
                        return False
                else:
                        continue
        return True

def checkcc(checklist):
    ccl = {}
    for item in checklist:
        if item in ccl.keys():
            ccl[item] += 1
        else:
            ccl[item] = 1
    return ccl

def writeTEX(filecontent,filepath):
    f = open(filepath,'w')
    f.write(r'''\begin{table}[h!]
    \center\tiny \begin{tabular}{c|c|c|c|c|c|c|c|c|c}
        \hline
        \multirow{2}*{core number} & \multicolumn{4}{c}{Parallel Test Prioritization} & \multicolumn{5}{|c}{Sequence Test Prioritization} \\
        \cline{2-10}
        ~& p-total & p-additional & p-search & p-arp & s-total & s-additional & s-search & s-arp & s-timeadditional \\
        \hline\hline''')
    for i in range(len(filecontent)):
        f.write(str(filecontent[i][0]))
        for item in filecontent[i][1:]:
            f.write('& ' + str(item))
    f.write(r'''\hline
    \end{tabular}
    \caption{Overall results for parallel test prioritization on open-source subjects.}
    \label{tab:effectiveness}
\end{table}''' + '\n')
    f.close()
    

if __name__ == "__main__":
    path = '../../subjects/'
    path_o = '../../subjects/'
    result = []
    subjects = readFile(path + 'uselist-all')
    
    apfdc_file= ['greedytotal_withouttime.txt',
                 'greedyadditional_withouttime.txt',
                 'genetic_withouttime.txt',
                 'arp_withouttime.txt',
                 'greedytotal_withtime.txt',
                 'greedyadditional_withtime.txt',
                 'genetic_withtime.txt',
                 'arp_withtime.txt',
                 'GroupTTMethod',
                 'GroupGAMethod',
                 'GroupGeneticMethod',
                 'GroupARTMethod',
                 'SAGT',
                 'GroupTAMethod',
                 'SAARP']
    
    gl = ['2.0']
    groups = [4,8,12,16]

    success_list = []
    violation_list = []
    violationdict = {4:[], 8:[], 12:[], 16:[]}
    testing_time = tree()
    temp = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    
    for gn in groups:
        
        checklist = []
        
        for g in gl:
            for subject in subjects:
                gpath = path + subject + '/testmethod/dynamic/state/' + str(g) + 'avg-new/evaluate/' + str(gn) + '/apfdc_total/'
                testlist = readFile(path + subject + '/testmethod/dynamic/testList')
                if os.path.exists(path + subject + '/testmethod/dynamic/exeTime') == True:
                    timelist = readFile(path + subject + '/testmethod/dynamic/exeTime')
                else:
                    timelist = readFile(path + subject + '/testmethod/dynamic/exeTime.txt')
                timedict = {} 
                totaltime = 0
                for i in range(len(testlist)):
                    timedict[testlist[i]] = float(timelist[i])
                    totaltime += float(timelist[i])
                applist = []
                for app in apfdc_file:
                    if 'Group' in app:
                        app_tcp = readTCPfile(path_o + subject + '/baseline/statement/' + str(gn) + '-' + app + '.txt',len(testlist))
                        app_apfdc = eval(readFile(gpath + app)[0])
                    elif app == 'SAGT':
                        app_tcp = readTCPfile(path + subject + '/testmethod/dynamic/state/' + str(20.0) + 'avg-new/group' + str(gn) + '/greedytotal_withtime.txt',len(testlist))
                        app_apfdc = eval(readFile(path + subject + '/testmethod/dynamic/state/20.0avg-new/evaluate/' + str(gn) + '/apfdc_total/greedytotal_withtime.txt')[0])
                    elif app == 'SAARP':
                        app_tcp = readTCPfile(path + subject + '/testmethod/dynamic/state/' + str(20.0) + 'avg-new/group' + str(gn) + '/arp_withtime.txt',len(testlist))
                        app_apfdc = eval(readFile(path + subject + '/testmethod/dynamic/state/20.0avg-new/evaluate/' + str(gn) + '/apfdc_total/arp_withtime.txt')[0])
                    elif app == 'SAGA':
                        app_tcp = readTCPfile(path + subject + '/testmethod/dynamic/state/' + str(20.0) + 'avg-new/group' + str(16) + '/greedyadditional_withtime.txt',len(testlist))
                        app_apfdc = eval(readFile(path + subject + '/testmethod/dynamic/state/2.0avg-new/evaluate/' + str(gn) + '/apfdc_total/greedyadditional_withtime.txt')[0])
                    else:
                        app_tcp = readTCPfile(path + subject + '/testmethod/dynamic/state/' + str(g) + 'avg-new/group' + str(gn) + '/' + app,len(testlist)) 
                        app_apfdc = eval(readFile(gpath + app)[0])
                    testing_time[subject][gn][g][app] = getTestingTime(app_tcp,timedict)
                    applist.append([app,app_apfdc,app_tcp])
                large_group,small_group,avg = divideSmallandLarge(testlist,int(gn),timedict,totaltime,float(g))
                groupTimeLimit = avg * float(g)
                max_apfdc = -1
                flag = 0
                for item_index in range(len(applist)):
                    item = applist[item_index]
                    check = checklimit(item[2],large_group,groupTimeLimit,timedict)
                    if check == True:
                        success_list.append(item[0])
                        testing_time[subject][gn][g]['check'][apfdc_file[item_index]] = True
                    else:
                        violation_list.append(item[0])
                        violationdict[gn].append(item[0])
                        testing_time[subject][gn][g]['check'][apfdc_file[item_index]] = False
    print apfdc_file
    print temp
    print '***********************'
    print len(success_list) + len(violation_list)
    sl = checkcc(success_list)
    vl = checkcc(violation_list)
    print vl
    print sl
    temp_vl = []
    for item in apfdc_file:
        if item in vl.keys():
            temp_vl.append(vl[item])
        else:
            temp_vl.append(0)
    temp_sl = []
    for item in apfdc_file:
        if item in sl.keys():
            temp_sl.append(sl[item])
        else:
            temp_sl.append(0)
    length = (temp_sl[0] + temp_vl[0])/4
    print 'length : ' + str(length)
    temp_vl_dict = {}
    for gn in groups:
        temp_vl_dict[gn] = checkcc(violationdict[gn])
        tvl = []
        for item in apfdc_file:
            if item in temp_vl_dict[gn].keys():
                tvl.append(str(temp_vl_dict[gn][item]))
            else:
                tvl.append(str(0))
        if gn == 4:
            result.append([r'\multirow{5}*{violation}',str(gn)] + tvl)
        else:
            result.append([r'~',str(gn)] + tvl)
    result.append([r'~','total']+ temp_vl)
    result.append([r'\multicolumn{2}{c|}{success}'] + temp_sl)
    writeTEX(result,'tabs/RQ1-overall.tex')
    
    ratio_sum = []
    time_delta = tree()
    for item_index in range(len(result[0:-2])):
        f = open('data_seq/testing_time_%s.csv'%groups[item_index],'w')
        f.write(','.join(apfdc_file) + '\n')
        for subject in subjects:
            for app in apfdc_file[0:-1]:
                f.write('%s,'%testing_time[subject][groups[item_index]]['2.0'][app])
            f.write('%s\n'%testing_time[subject][groups[item_index]]['2.0']['SAARP'])
        f.close()
        item = result[item_index]
        print(' & '.join(item))
        for ratio_item in item[10:]:
            if type(ratio_item) == str:
                ratio_sum.append(eval(ratio_item)/(54*1.0))
            else:
                ratio_sum.append(ratio_item/(54*1.0))
        app_temp_list = ['AVG']
        for app in apfdc_file:
            temp_list_tt = []
            for subject in subjects:
                temp_list_tt.append(testing_time[subject][groups[item_index]]['2.0'][app])
            app_temp_list.append('%.2f'%np.mean(temp_list_tt))
        print(' & '.join(app_temp_list))
        print('**********************')
    print(np.mean(ratio_sum))

    ugt = []
    uga = []
    uge = []
    uarp = []
    agt = []
    aga = []
    aarp = []
    for gn in groups:
        for subject in subjects:
            ugt.append(testing_time[subject][gn]['2.0']['greedytotal_withouttime.txt'] / testing_time[subject][gn]['2.0']['GroupTTMethod'])
            uga.append(testing_time[subject][gn]['2.0']['greedyadditional_withouttime.txt'] / testing_time[subject][gn]['2.0']['GroupGAMethod'])
            uge.append(testing_time[subject][gn]['2.0']['genetic_withouttime.txt'] / testing_time[subject][gn]['2.0']['GroupGeneticMethod'])
            uarp.append(testing_time[subject][gn]['2.0']['arp_withouttime.txt'] / testing_time[subject][gn]['2.0']['GroupARTMethod'])
            agt.append(testing_time[subject][gn]['2.0']['greedytotal_withtime.txt'] / testing_time[subject][gn]['2.0']['SAGT'])
            aga.append(testing_time[subject][gn]['2.0']['greedyadditional_withtime.txt'] / testing_time[subject][gn]['2.0']['GroupTAMethod'])
            aarp.append(testing_time[subject][gn]['2.0']['arp_withtime.txt'] / testing_time[subject][gn]['2.0']['SAARP'])
    print('ugt  : %s'%np.mean(ugt))
    print('uga  : %s'%np.mean(uga))
    print('uge  : %s'%np.mean(uge))
    print('uarp : %s'%np.mean(uarp))
    print('agt  : %s'%np.mean(agt))
    print('aga  : %s'%np.mean(aga))
    print('age  : %s'%np.mean(aarp))

    print('all : %s'%(np.mean([1/np.mean(ugt),1/np.mean(uga),1/np.mean(uge),1/np.mean(uarp),1/np.mean(agt),1/np.mean(aga),1/np.mean(aarp)])))


