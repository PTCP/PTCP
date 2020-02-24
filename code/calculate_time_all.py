import os
import copy
import time
from tqdm import tqdm


def readFile(filepath):
    f = open(filepath)
    content = f.read()
    f.close()
    return content.splitlines()

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

def TestName_Index(temp_namelist,TestList):
    result = copy.deepcopy(temp_namelist)
    for i in range(len(result)):
        for j in range(len(result[i])):
            result[i][j] = TestList.index(temp_namelist[i][j])
    return result


#getTime(test_index,timelist,testmap,index_list)
def getTime(test_index,timelist,testmap,index_list):
    totaltime = 0
    atime = time.time()
    for i in range(len(testmap)):
        mtime = time.time()
        mutant = i
        detected = testmap[i]
        tmin = float("inf")
        for j in detected:
            temp = 0
            for j1 in test_index:
                if j in j1:
                    for j2 in j1:
                        if j != j2:
                            temp += timelist[j2]
                        elif j == j2:
                            temp += timelist[j2]
                            break
                    break
                else:
                    continue
            tmin = min(temp,tmin)
        #print time.time()-mtime
        totaltime += tmin * eval(index_list[i])
    #print time.time() - atime
    return totaltime

def DetectedTime(test_index,timelist,mutantmap,index_list):
    totaltime = 0
    firsttime = 0
    lasttime = 0
    mtime = time.time()
    mutantnumber = len(index_list)
    mutantlist = range(mutantnumber)
    time_dict = {}
    for group_item in test_index:
        grouptime = 0
        for test_item in group_item:
            grouptime += timelist[test_item]
            if grouptime not in time_dict.keys():
                time_dict[grouptime] = [(grouptime,test_item)]
            else:
                time_dict[grouptime].append((grouptime,test_item))
    tt = copy.deepcopy(time_dict.keys())
    tt.sort()
    for item in tt:
        if len(mutantlist) == 0:
            break
        for test_item in time_dict[item]:
            tempname = test_item[1]
            tempmutant = mutantmap[tempname]
            for mu_item in tempmutant:
                if mu_item in mutantlist:
                    totaltime += test_item[0] * eval(index_list[mu_item])
                    mutantlist.remove(mu_item)
                    if len(mutantlist) == 0:
                        lasttime = test_item[0]
                    elif len(mutantlist) == mutantnumber-1:
                        firsttime = test_item[0]
    #print time.time()-mtime
    if len(mutantlist)!= 0:
        lasttime = tt[-1]
    #print 'alltime  : ' + str(totaltime)
    #print 'lasttime : ' + str(lasttime)
    return totaltime/(mutantnumber*1.0),firsttime,lasttime
            


def writefileSingle(dirpath,filename,content1,content2,content3):
    if os.path.exists(dirpath + 'dectedtime/firsttime/randoms/') == False:
        os.makedirs(dirpath + 'dectedtime/firsttime/randoms/')
    if os.path.exists(dirpath + 'dectedtime/lasttime/randoms/') == False:
        os.makedirs(dirpath + 'dectedtime/lasttime/randoms/')
    if os.path.exists(dirpath + 'dectedtime/averagetime/randoms/') == False:
        os.makedirs(dirpath + 'dectedtime/averagetime/randoms/')
    f = open(dirpath + 'dectedtime/averagetime/randoms/' + filename,'w')
    f.write(str(content1) + '\n')
    f.close()

    f = open(dirpath + 'dectedtime/firsttime/randoms/' + filename,'w')
    f.write(str(content2) + '\n')
    f.close()

    f = open(dirpath + 'dectedtime/lasttime/randoms/' + filename,'w')
    f.write(str(content3) + '\n')
    #print content3
    #f.write(content3)
    f.close()
        
        

def writefile(dirpath,filename,content1,content2,content3):
    if os.path.exists(dirpath + 'dectedtime/firsttime/') == False:
        os.makedirs(dirpath + 'dectedtime/firsttime')
    if os.path.exists(dirpath + 'dectedtime/lasttime/') == False:
        os.makedirs(dirpath + 'dectedtime/lasttime')
    if os.path.exists(dirpath + 'dectedtime/averagetime/') == False:
        os.makedirs(dirpath + 'dectedtime/averagetime')
    f = open(dirpath + 'dectedtime/averagetime/' + filename,'w')
    f.write(str(content1) + '\n')
    f.close()

    f = open(dirpath + 'dectedtime/firsttime/' + filename,'w')
    f.write(str(content2) + '\n')
    f.close()
    
    f = open(dirpath + 'dectedtime/lasttime/' + filename,'w')
    f.write(str(content3) + '\n')
    #print content3
    #f.write(content3)
    f.close()


if __name__ == '__main__':
    path = '/devdata/zjy/parallelTCP/tosem_add/experiment/'
    subject_list = readFile(path + 'uselist-all')
    #subject_list.remove('camel-core')
    #subject_list.remove('commons-math')
    #subject_list = ['camel-core','commons-math']
    subjectsdict = {}
    for i in range(len(subject_list)):
        subjectsdict[subject_list[i].lower()] = subject_list[i]
    indexlist = copy.deepcopy(subjectsdict.keys())
    indexlist.sort()
    #indexlist = ['assertj-core']
    #indexlist = ['webbit','raml-java-parser']
    #indexlist = ['jackson-datatype-guava-v2']
    #pass_list = readFile(path + 'uselist-cry')
    #gl = float(sys.argv[1])
    result = []
    #gn = [50,100]
    #gn = [50,100,200]
    #gn = [4,8,12,16]
    #ts = [1.5,2.0]
    #gn = [12]
    #ts = [1.5]
    #ts = [1.25,1.75]
    #gn = [1]
    #ts = [3.0]
    gn = [4,8,12,16]
    ts = [1.25,1.5,1.75,2.0]
    #ts = [20.0]
    tosem_path = 'testmethod/dynamic'
    gran = 'state'
    #apps = ['random']
    #apps = ['greedytotal_withtime.txt']
    #apps = ['arp_withtime.txt']
    #apps = ['genetic_withouttime.txt','genetic_withtime.txt']
    apps = ['greedytotal_withouttime.txt','greedyadditional_withouttime.txt','genetic_withouttime.txt','arp_withouttime.txt','greedytotal_withtime.txt','greedyadditional_withtime.txt','genetic_withtime.txt','arp_withtime.txt','random']
    #apps = ['greedytotal_withouttime.txt','greedyadditional_withouttime.txt','arp_withouttime.txt','greedytotal_withtime.txt','greedyadditional_withtime.txt','arp_withtime.txt']
    for sindex in indexlist:
        subject_item = subjectsdict[sindex]
        #if subject_item in pass_list:
        #    continue
        sresult = []
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
            continue
        for i in range(len(testlist)):
            timelist[i] = eval(timelist[i])
        mutantmap = []
        for j in range(len(testlist)):
            temp = []
            for i in range(len(mulist[0])):
                if mulist[j][i]  == '1':
                    temp.append(i)
            mutantmap.append(temp)

        # testing
        ''' 
        testmap = []
        for i in range(len(mulist[0])):
            temp = []
            for j in range(len(testlist)):
                if mulist[j][i]  == '1':
                    temp.append(j)
            testmap.append(temp)
        '''

        for g in gn:
            for t in ts:
                temp = []
                for app in apps:
                    #print subject_path + str(t) + 'avg-new/group' + str(g) + '/' + app
                    if app != 'random':
                        test = readTCPfile(subject_path + gran + '/' + str(t) + 'avg-new/group' + str(g) + '/' + app)
                        test_index = TestName_Index(test,testlist)
                        mtime = time.time()
                        temptime1,temptime2,temptime3 = DetectedTime(test_index,timelist,mutantmap,index_list)
                        m1 = time.time()-mtime
                        #mtime2 = time.time()
                        #temptime2 = getTime(test_index,timelist,testmap,index_list)
                        #m2 = time.time()- mtime2
                        writefile(subject_path + gran + '/' + str(t) + 'avg-new/evaluate/' + str(g) + '/',app,temptime1,temptime2,temptime3)
                        temp.append(temptime1)
                        #print str(temptime) + ' : ' + str(m1)
                        #print str(temptime2) + ' : ' + str(m2)
                        #print subject_path + str(t) + 'avg-new/evaluate/' + str(g) + '/' + app
                        #print '%.4f , %.4f , %.4f' %(temptime1,temptime2,temptime3)
                        print sindex + ' : ' + app + ' is completed! ' + str(m1)
                    else:
                        rtime = []
                        ftime = []
                        ltime = []
                        for i in tqdm(range(50)):
                            test = readTCPfile(subject_path + gran + '/' + str(t) + 'avg-new/group' + str(g) + '/random/random' + str(i) + '.txt')
                            test_index = TestName_Index(test,testlist)
                            temptime1,temptime2,temptime3 = DetectedTime(test_index,timelist,mutantmap,index_list)
                            rtime.append(temptime1)
                            ftime.append(temptime2)
                            ltime.append(temptime3)
                            writefileSingle(subject_path + gran + '/' + str(t) + 'avg-new/evaluate/' + str(g) + '/',str(app) + str(i),temptime1,temptime2,temptime3)
                        print sindex + ' : ' + app + str(i) + ' is completed! ' 
                        writefile(subject_path + gran + '/' + str(t) + 'avg-new/evaluate/' + str(g) + '/',app,sum(rtime)/(len(rtime)*1.0),sum(ftime)/(len(ftime)*1.0),sum(ltime)/(len(ltime)*1.0))
                        temp.append(sum(rtime)/(len(rtime)*1.0))
                #print temp
                accratio = []
                for i in range(len(apps)):
                    #print apps[i] + ' : ' + str(temp[i]/(temp[-1]*1.0))
                    accratio.append(temp[i]/(temp[-1]*1.0))
                sresult.append(accratio)
                result.append(accratio)
        #for i in range(len(apps)):
        #    tempcount = 0
        #    for j in range(len(sresult)):
        #        tempcount += sresult[j][i]
        #    tempcount = tempcount/(len(sresult)*1.0)
        print sindex + ' is completed!'
            
    
    #for i in range(len(result)):
        





