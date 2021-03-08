import os
import copy

def readFile(filepath):
    f = open(filepath)
    content = f.read()
    f.close()
    return content.splitlines()


if __name__ == '__main__':
    path = './subjects/source/'
    subject_list = os.listdir(path)
    subject_list = readFile(path + 'uselist-all')
    for subject in subject_list:
        
        subject_path = path + subject + '/testmethod/dynamic/state/'
        testlist = readFile(subject_path + 'testList')
        covlist = readFile(subject_path + 'mutantKillMatrix')
        result = []
        print subject_path + ' is starting...'
        print len(covlist)
        for i in range(len(covlist)):
            temp_list = []
            for j in range(len(covlist[0])):
                temp_list.append(covlist[i][j])
            result.append(temp_list)
        cov = []
        for j in range(len(covlist[0])):
            temp_str = ''
            for i in range(len(covlist)):
                temp_str += covlist[i][j]
            cov.append(temp_str)
        print len(temp_str)
        test = copy.deepcopy(cov)
        test = list(set(test))
        print 'all number : ' + str(len(cov))
        print 'reduce num : ' + str(len(test))
        number_list = []
        for item in test:
            count = 0
            for i in cov:
                if i == item:
                    count += 1
            number_list.append(count)
        use_list = []
        for i in range(len(test[0])):
            temp_str = ''
            for j in range(len(test)):
                temp_str += test[j][i]
            use_list.append(temp_str)
            
        f = open(subject_path + 'mutantkill-reduce','w')
        for item in use_list:
            f.write(item + '\n')
        f.close()
        f = open(subject_path + 'mutantkill-reduce-index','w')
        for item in number_list:
            f.write(str(item) + '\n')
        f.close()
        print 'sum : ' + str(sum(number_list))
        print subject_path + 'is completed!'
