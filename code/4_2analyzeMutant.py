import os
from bs4 import BeautifulSoup


def readFile(filepath):
    f = open(filepath)
    content = f.read()
    f.close()
    return content.splitlines()



if __name__ == '__main__':
    path = './subjects/source/'
    subject_list = readFile(path + 'uselist-add')
    cry = []
    for subject in subject_list:
        subject_path = path + subject + '/'
        #print subject
        testlist = readFile(subject_path + 'testList')
        if os.path.exists(subject_path + 'mutations.xml') == False:
            print subject + '   cry -----------------'
            cry.append(subject)
            continue
        mutant_info = BeautifulSoup(open(subject_path + 'mutations.xml'),'xml')    
        mutant_list = mutant_info.findAll('mutation',{'detected':'true','status':'KILLED'})
        #print len(mutant_list)
        #print mutant_list[0]
        mutant_dict = {}
        for test in testlist:
            mutant_dict[test] = []
        for i in range(len(mutant_list)):
            #print mutant_list[i]
            detected_str = mutant_list[i].find('killingTest').text
            detected_list = detected_str.split(',')
            #print detected_str
            for detected_test in detected_list:
                if '(' not in detected_test:
                    continue
                detected_testmethod = detected_test.split('(')[0].replace('.','/')
                #print detected_testmethod
                try:
                    mutant_dict[detected_testmethod].append(i)
                except:
                    print mutant_list[i]
                    print detected_str
                    print detected_list
                    print detected_testmethod
                    raw_input('exception ...')
                #print mutant_dict[detected_testmethod]
                #raw_input('check...')
        #print mutant_dict
        #raw_input('check ...')
        f = open(subject_path + 'newmutantkill','w')
        for test in testlist:
            temp_str = ''
            for i in range(len(mutant_list)):
                if i in mutant_dict[test]:
                    temp_str += '1'
                else:
                    temp_str += '0'
            f.write(temp_str + '\n')    
        f.close()    
    
        f = open(subject_path + 'usemutant-info','w')    
        for item in mutant_list:
            f.write(str(item) + '\n')
        f.close()
        print subject + ' is completed!'
