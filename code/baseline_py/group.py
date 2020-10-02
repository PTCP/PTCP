import os
import copy
import sys

def readFile(file_path):
        f = open(file_path)
        content = f.read()
        f.close()
        return content.splitlines()
def writeFile(file_path,file_content):
        f = open(file_path,'w')
        for line in file_content:
                f.write(line + '\n')
        f.close() 


if __name__ == '__main__':
        path = '/PTCP/subjects/experiment/'
        subject_list = readFile(path + 'uselist-all')
        #subject_list = ['test']
        g_n = int(sys.argv[1])
        for subject in subject_list:
                subject_path = path + subject + '/'
                test_list = readFile(subject_path + '/testList')
                #time_list = read_file(root_path + '/time.txt')
                if os.path.exists(subject_path + 'exeTime.txt') == True:
                        time_list = readFile(subject_path + 'exeTime.txt')
                else:
                        time_list = readFile(subject_path + 'exeTime')
                
                test_dict = {}
                for i in range(0,len(test_list)):
                        test_dict[test_list[i]] = float(time_list[i])

                pri_file_list = ['SequenceTTMethod.txt',
                                  'SequenceGAMethod.txt',
                                  'SequenceARTMethod.txt',
                                  'SequenceGeneticMethod.txt',
                                  'SequenceTAMethod.txt']
                for pri_file in pri_file_list:
                        #if subject_list.index(subject) > subject_list.index('metrics-core') and (pri_file == 'SequenceARTMethod.txt' or pri_file == 'SequenceGeneticMethod.txt'):
                                #continue
                        pri_file_path = subject_path +'baseline/statement/'+ pri_file
                        if os.path.exists(pri_file_path) == False:
                            continue
                        tcp_order = readFile(pri_file_path)
                        group_number = g_n
                        group_dict = {}
                        for i in range(0,group_number):
                                group_dict[i] = [0,[]]

                        next_group = [0,0]
                        for item in tcp_order:
                                '''
                                print pri_file_path
                                if pri_file_path == '/devdata/zjy/parallelTCP/subject/test/subjects/jackson-datatype-guava/baseline/statement/SequenceTAMethod.txt':
                                        print group_dict
                                        print next_group
                                        print '******************'
                                        raw_input('check...')
                                '''
                                group_dict[next_group[0]][1].append(item)
                                #print item
                                #print test_dict
                                #raw_input('check...')
                                try:
                                        group_dict[next_group[0]][0] += test_dict[item]
                                        next_group = [0,group_dict[0][0]]
                                except:
                                        print pri_file
                                        print subject_path
                                        raw_input('check...')
                                for i in range(1,group_number):
                                        if next_group[1] > group_dict[i][0]:
                                                next_group = [i,group_dict[i][0]]
                        f = open(pri_file_path.replace('Sequence',str(g_n) + '-Group'),'w')
                        for i in range(0,group_number):
                                for j in group_dict[i][1]:
                                        f.write(str(j) + '\t')
                                #f.write(str(group_dict[i][1][-1]) + '\n')
                                f.write('\n')
                        f.close()
                print subject_path + ' is complete...'

        
                        

