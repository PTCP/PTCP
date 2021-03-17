import os
import numpy
import copy
from collections import defaultdict

def tree(): return defaultdict(tree)

def readFile(filepath):
    f = open(filepath)
    content = f.read()
    f.close()
    return content.splitlines()

def getAverage(content):
    for i in range(len(content)):
        content[i] = eval(content[i])
    return sum(content)/(len(content) * 1.0)

if __name__ == '__main__':
    path = '../../subjects/'
    subjects = readFile(path + 'uselist-gnadd-all')
    apps = ['greedytotal_withouttime.txt','greedyadditional_withouttime.txt','genetic_withouttime.txt','arp_withouttime.txt','greedytotal_withtime.txt','greedyadditional_withtime.txt','genetic_withtime.txt','arp_withtime.txt','random']
    result = defaultdict(tree)
    gn = [50,100,200]
    ts = [1.5]
    tosem_path = 'testmethod/dynamic'
    gran = 'state'
    fw = []
    for subject in subjects:
        spath = path + subject + '/' + tosem_path + '/'
        for gitem in gn:
            for titem in ts:
                tb = [0]*len(apps)
                tmax = 0
                for i in range(len(apps)):
                    app = apps[i]
                    if True:
                        tempf = eval(readFile(spath + gran + '/' + str(titem) + 'avg-new/evaluate/' + str(gitem) + '/dectedtime/firsttime/' + app)[0])
                        tempa = eval(readFile(spath + gran + '/' + str(titem) + 'avg-new/evaluate/' + str(gitem) + '/dectedtime/averagetime/' + app)[0])
                        result[subject][gitem][titem]['ft'][app] = tempf
                        result[subject][gitem][titem]['at'][app] = tempa
    metrics = ['ft','at']
    texfile = []
    print('computing resource : ')
    for m in metrics:
        texstr = ''
        for gitem in gn:
            if gitem == 50:
                tempstr = r'\multirow{4}*{$\varDelta %s$} & %s'%(m.upper(),gitem)
            else:
                tempstr = '\t' + r'~ &%s'%gitem
            timelist = []
            for app in apps:
                timelist.append([])
            for titem in ts:
                for subject in subjects:
                    for i in range(len(apps)):
                        tempratio = result[subject][gitem][titem][m][apps[-1]]/(result[subject][gitem][titem][m][apps[i]] * 1.0)
                        timelist[i].append(tempratio)
            for i in range(len(apps)-1):
                tempvalue = sum(timelist[i])/(len(timelist[i])*1.0)
                if tempvalue > 0:
                    arrow = '$\uparrow$'
                else:
                    arrow = '$\downarrow$'
                tempstr += '& %.2f'%(tempvalue)
            tempstr += r'\\' + '\n'
            print('%s - %s : %s'%(m,gitem,tempstr))
            texstr += tempstr
        print(texstr)
        print('************')
    
    print('group number : ')
    for m in metrics:
        texstr = ''
        for titem in ts:
            if titem == 1.25:
                tempstr = r'\multirow{4}*{$\varDelta %s$} & %s'%(m.upper(),titem)
            else:
                tempstr = '\t' + r'~ &%s'%titem
            timelist = []
            for app in apps:
                timelist.append([])
            for gitem in gn:
                for subject in subjects:
                    for i in range(len(apps)):
                        tempratio = result[subject][gitem][titem][m][apps[-1]]/(result[subject][gitem][titem][m][apps[i]] * 1.0)
                        timelist[i].append(tempratio)
            for i in range(len(apps)-1):
                tempvalue = sum(timelist[i])/(len(timelist[i])*1.0)
                if tempvalue > 0:
                    arrow = '$\uparrow$'
                else:
                    arrow = '$\downarrow$'
                tempstr += '& %.2f'%(tempvalue)
            tempstr += r'\\' + '\n'
            print('%s - %s : %s'%(m,titem,tempstr))
            texstr += tempstr
        print(texstr)
        print('************')
