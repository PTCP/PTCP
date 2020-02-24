import os
from bitarray import bitarray
#import bitarray
#from bitarray import bitdiff


def readFile(filepath):
    f = open(filepath)
    content = f.read()
    f.close()
    return content.splitlines()



if __name__ == '__main__':
    #path_m = '/devdata/zjy/parallelTCP/subjects/'
    path_c = '/PTCP/subjects/experiment/'
    subjects = readFile(path_m + 'uselist-all')

    for subject in subjects:
        subject_path_m = path_c + subject + '/testmethod/dynamic/'
        subject_path_c = path_c + subject + '/testclass/'
        if os.path.exists(subject_path_c) == False:
            os.makedirs(subject_path_c)
        testlist = readFile(subject_path_m + 'testList')
        if os.path.exists(subject_path_m + 'exeTime') == True:
            exetime = readFile(subject_path_m + 'exeTime')
        else:
            exetime = readFile(subject_path_m + 'exeTime.txt')
        for time_index in range(len(exetime)):
            exetime[time_index] = eval(exetime[time_index])
        cov = readFile(subject_path_m + 'stateMatrix-reduce.txt')
        mutant = readFile(subject_path_m + 'mutantkill-reduce')
        os.system('cp %s %s'%(subject_path_m + 'testList', subject_path_c))
        os.system('cp %s %s'%(subject_path_m + 'reduce-index.txt', subject_path_c))
        os.system('cp %s %s'%(subject_path_m + 'mutantkill-reduce-index', subject_path_c))
        #os.system('cp %s %s'%(subject_path_m + 'usemutant-info', subject_path_c))
        testdict = {}
        for test_index in range(len(testlist)):
            test_m = testlist[test_index]
            if '/' in test_m:
                #print('yes1')
                test_c = '/'.join(test_m.split('/')[0:-1])
            elif '.' in test_m:
                #print('yes2')
                test_c = '.'.join(test_m.split('.')[0:-1])
            else:
                raw_input('error check..')
            if test_c in testdict.keys():
                testdict[test_c].append(test_index)
            else:
                testdict[test_c] = [test_index]
            #if subject == 'scribe-java':
            #    print(test_m + '  **  ' + test_c)
        #if subject == 'scribe-java':
        #    print(testlist)
        #    print(testdict)
        #    print(len(testdict.keys()))
        #    raw_input('check ...')
        f_test = open(subject_path_c + 'testList','w')
        f_cov = open(subject_path_c + 'stateMatrix-reduce.txt','w')
        f_time = open(subject_path_c + 'exeTime','w')
        f_mutant = open(subject_path_c + 'mutantkill-reduce','w')
        for test_class in testdict.keys():
            temptime = 0
            tempcov = bitarray('0' * len(cov[0]))
            tempmutant = bitarray('0' * len(mutant[0]))
            f_test.write(test_class + '\n')
            for test_index in testdict[test_class]:
                tempcov = tempcov|bitarray(cov[test_index])
                tempmutant = tempmutant|bitarray(mutant[test_index])
                temptime = temptime + exetime[test_index]
            f_cov.write(bitarray.to01(tempcov) + '\n')
            f_mutant.write(bitarray.to01(tempmutant) + '\n')
            f_time.write(str(temptime) + '\n')
        f_test.close()
        f_cov.close()
        f_mutant.close()
        f_time.close()
        #raw_input(subject + ' check ...')
        print(subject + ' is completed!')
    











