# get call graph coverage information , save as binary txt
import os
import io
import re
import xml.dom.minidom
import random
import commands
from sys import stdin
from os.path import join
from os import walk
import bitarray
from bitarray import bitdiff
from bitarray import bitarray
import copy
from tqdm import tqdm


def getPath(projectpath):
    os.chdir(projectpath)
    pathlist = []
    for i in os.listdir('.'):
        if os.path.isdir(i):
            #print(os.path.join(projectpath,i))
            pathlist.append(os.path.join(projectpath,i))
    return pathlist

def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc: # Python >2.5 (except OSError, exc: for Python <2.5)
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else: raise

def readFile(filename):
    f = open(filename,"r")
    filecontentlist = []
    while True:
        line = f.readline()
        if line:
            filecontentlist.append(line.rstrip("\n"))
        else:
            break
    f.close()
    return filecontentlist

'''
def callgraph_analysis(CallFile):
    contentlist = readFile(CallFile)
    #every node in call graph,use to give them index
    Nodelist = []
    #TestNodeList = []
    Node_to_node = []
    count = 0
    for line in contentlist:
        if line[0:5] == "Node:":
            if line not in Nodelist:
                Nodelist.append(line)
            node_index = Nodelist.index(line)
            #count += 1
        elif line[0:9] == " - invoke":
            #count_in += 1
            pass
        elif line[0:13] == "     -> Node:":
            #count_node += 1
            line = line[8:]
            if line not in Nodelist:
                Nodelist.append(line)
            tarnode_index = Nodelist.index(line)
            Node_to_node.append([node_index,tarnode_index])
        #print len(Nodelist)
        #print line
        #raw_input("pause!")
    #print "the total node is : " + str(count)
    return (Nodelist,Node_to_node)
'''

def getTestIndex(nodelist,testlist):
    index_list = []
    for item in testlist:
        isfind = 0
        item = item.split("-")[0]
        temp = ("/").join(item.split(".")[1:-1]) + ", " + item.split(".")[-1]
        for i in range(len(nodelist)):
            if nodelist[i].find(temp) != -1:
                index_list.append(i)
                isfind = 1
                break
        if isfind == 0:
            print temp
    return index_list

def list_to_dict(llist):
    temp_dict = {}
    init_point = []
    for item in llist:
        if item[0] not in init_point:
            init_point.append(item[0])
    for item in init_point:
        temp_dict[item] = []
        for x in llist:
            if x[0] == item:
                temp_dict[item].append(x[1])
    #print len(temp_dict)
    return temp_dict

def getAllCall(ini_point,dic):
    if ini_point not in dic.keys():
        call_list = []
        return call_list
    elif ini_point in dic.keys():
        call_list = list(set(dic[ini_point]))
        start_index = 0
        while True:
            add_list = []
            for i in range(start_index,len(call_list)):
                try:
                    temp_list = dic[call_list[i]]
                    for item in temp_list:
                        add_list.append(item)
                except:
                    continue
            if len(add_list) == 0:
                break
            else:
                start_index = len(call_list)
                for item in add_list:
                    if item not in call_list:
                        call_list.append(item)
                continue
        return call_list

#get all files in /src/test/.. that have no "Test" in their names
def getFileList(pppath):
    filelist = []
    for root, dirs, filenames in os.walk(pppath):
        for filename in filenames:
            #print "the full name of the file is:" + os.path.join(root,filename)
            if ".java" in filename and "/test/" in root:
                #if "Test" not in filename:
                filelist.append(os.path.join(root,filename))
    return filelist

def isFilter(objectlist,ppp):
    temp_count = 0
    for item in objectlist:
        if item in ppp:
            temp_count = 1
            break
    return temp_count


def getCallGraph(ppath,granularity):
    specialfilelist = getFileList(ppath.replace("/experiment/","/source/") + "/src")
    for i in range(len(specialfilelist)):
        specialfilelist[i] = ".".join(specialfilelist[i].rstrip(".java").split("/")[-3:])
    calllist = readFile(ppath + "/call-graph-info.txt")
    testcaselist = readFile(ppath + "/" + granularity + "/testList")
    sourcemethodlist = []
    sourcemethodlist_linenumber = []
    allmethodlist = []
    allmethodlist_normal = []
    node_to_node = []
    project_class_name = (".").join(testcaselist[0].split("-")[0].split(".")[0:3])
    for i in range(len(testcaselist)):
        testcaselist[i] = testcaselist[i].split("-")[0]
    for item in calllist:
        if item[0] == "C":
            continue
        if item[0] == "D":
            temp = item[2:]
            temp_name = temp.split("|")[0].rstrip(" ").replace(":",".")
            temp_number = temp.split("|")[1].lstrip(" ")
            temp_tt = temp_name.split("(")[0]
            if temp_name not in sourcemethodlist:
                if isFilter(specialfilelist,temp_tt) == 0:
                    sourcemethodlist.append(temp_name)
                    sourcemethodlist_linenumber.append(int(temp_number))
            if temp_name not in allmethodlist:
                allmethodlist.append(temp_name)
                allmethodlist_normal.append(temp_name.split("(")[0])
            continue
        temp = item[2:]
        temp_tar = temp.split("|")[0].rstrip(" ")
        temp_call = temp.split("|")[1].lstrip(" ")
        temp_tar = temp_tar.replace(":",".")
        temp_call = temp_call[3:].replace(":",".")
        '''
        if project_class_name in temp_tar and "Test" not in temp_tar and "commons.io." not in temp_tar and "commons.lang." not in temp_tar and "<init>" not in temp_tar and "<client>" not in temp_tar and "<clinit>" not in temp_tar:
            if temp_tar not in sourcemethodlist:
                if isFilter(specialfilelist,temp_tar) == 0:
                    sourcemethodlist.append(temp_tar)
        if project_class_name in temp_call and "Test" not in temp_call and "commons.io." not in temp_call and "commons.lang." not in temp_call and "<init>" not in temp_call and "<client>" not in temp_call and "<clinit>" not in temp_call:
            if temp_call not in sourcemethodlist:
                if isFilter(specialfilelist,temp_call) == 0:
                    sourcemethodlist.append(temp_call)
        '''
        if temp_tar not in allmethodlist:
            allmethodlist.append(temp_tar)
            allmethodlist_normal.append(temp_tar.split("(")[0])
        if temp_call not in allmethodlist:
            allmethodlist.append(temp_call)
            allmethodlist_normal.append(temp_call.split("(")[0])
        node_to_node.append([allmethodlist.index(temp_tar),allmethodlist.index(temp_call)])
    temp_dict = list_to_dict(node_to_node)
    detect_list = []
    for item in sourcemethodlist:
        if item not in allmethodlist:
            detect_list.append(item)
    for item in detect_list:
        temp_index = sourcemethodlist.index(item)
        sourcemethodlist.pop(temp_index)
        sourcemethodlist_linenumber.pop(temp_index)
    return (allmethodlist,allmethodlist_normal,sourcemethodlist,sourcemethodlist_linenumber,testcaselist,temp_dict)

# no use!!!
def getCallGraph_class(ppath,granularity):
    specialfilelist = getFileList(ppath + "/src")
    for i in range(len(specialfilelist)):
        specialfilelist[i] = ".".join(specialfilelist[i].rstrip(".java").split("/")[-3:])
    calllist = readFile(ppath + "/call-graph-info.txt")
    testcaselist = readFile(ppath + "/" + granularity + "/method-namelist.txt")
    sourcemethodlist = []
    allmethodlist = []
    allmethodlist_normal = []
    node_to_node = []
    project_class_name = (".").join(testcaselist[0].split("-")[0].split(".")[0:3])
    for i in range(len(testcaselist)):
        testcaselist[i] = testcaselist[i].split("-")[0]
    for item in calllist:
        if item[0] == "C":
            continue
        if item[0] == "D":
            continue
        temp = item[2:]
        temp_tar = temp.split("|")[0].rstrip(" ")
        temp_call = temp.split("|")[1].lstrip(" ")
        #temp_tar = temp_tar.replace(":",".")
        temp_tar = temp_tar.split(":")[0]
        temp_call = temp_call[3:].replace(":",".")
        if project_class_name in temp_tar and "Test" not in temp_tar and "commons.io." not in temp_tar and "commons.lang." not in temp_tar and "<init>" not in temp_tar and "<client>" not in temp_tar and "<clinit>" not in temp_tar:
            if temp_tar not in sourcemethodlist:
                if isFilter(specialfilelist,temp_tar) == 0:
                    sourcemethodlist.append(temp_tar)
        if project_class_name in temp_call and "Test" not in temp_call and "commons.io." not in temp_call and "commons.lang." not in temp_call and "<init>" not in temp_call and "<client>" not in temp_call and "<clinit>" not in temp_call:
            if temp_call not in sourcemethodlist:
                if isFilter(specialfilelist,temp_call) == 0:
                    sourcemethodlist.append(temp_call)
        if temp_tar not in allmethodlist:
            allmethodlist.append(temp_tar)
            allmethodlist_normal.append(temp_tar.split("(")[0])
        if temp_call not in allmethodlist:
            allmethodlist.append(temp_call)
            allmethodlist_normal.append(temp_call.split("(")[0])
        node_to_node.append([allmethodlist.index(temp_tar),allmethodlist.index(temp_call)])
    temp_dict = list_to_dict(node_to_node)
    return (allmethodlist,allmethodlist_normal,sourcemethodlist,testcaselist,temp_dict)
    

if __name__ == '__main__':
    path_s = '/devdata/zjy/parallelTCP/tosem_add/source/'
    path_e = '/devdata/zjy/parallelTCP/tosem_add/experiment/'
    path_a = '/devdata/zjy/parallelTCP/subjects/'
    subjects = readFile(path_s + 'uselist-noclover2')
    passlist = ['streamex']
    #for subject in tqdm(subjects):
    for subject in subjects:
        if subject in passlist:
            continue
        print(subject)
        subject_path_s = path_s + subject + '/'
        subject_path_e = path_e + subject + '/'
        subject_path_a = path_a + subject + '/'
        if os.path.exists(subject_path_e) == False:
            os.makedirs(subject_path_e)
        os.system('cp %s %s'%(subject_path_s + 'call-graph-info.txt', subject_path_e + 'call-graph-info.txt'))
        if os.path.exists(subject_path_e + 'testmethod/callgraph/') == False:
            os.makedirs(subject_path_e + 'testmethod/callgraph/')
            #os.makedirs(subject_path_e + 'testclass/')
        if os.path.exists(subject_path_e + 'testmethod/callgraph/testList') == False:
            os.system('cp %s %s'%(subject_path_a + 'testList', subject_path_e + 'testmethod/callgraph/testList'))
        namelist,namelist_normal,sourcelist,sourcelist_linenumber,testlist,call_dict = getCallGraph(subject_path_e,"testmethod")
        #print(testlist[0])
        #print(namelist_normal)
	
        f = open(subject_path_e + "/testmethod/callgraph/method-cg-cov","w")
        f_test = open(subject_path_e + "/testmethod/callgraph/method-cg-namelist","w")
        f_source = open(subject_path_e + "/testmethod/callgraph/method-cg-functioneffected","w")
        f_log = open(subject_path_e + "/testcase-notinsource","w")
        s = open(subject_path_e + "/testmethod/callgraph/statement-cg-cov","w")
        s_test = open(subject_path_e + "/testmethod/callgraph/statement-cg-namelist","w")
        s_source = open(subject_path_e + "/testmethod/callgraph/statement-cg-functioneffected","w")
        count = 0 
	
	for item in sourcelist:
            f_source.write(item + "\n")
        f_source.close()

	for i in range(len(sourcelist)):
            #temp_number = sourcelist_linenumber[i]
            for j in range(sourcelist_linenumber[i]):
                s_source.write(sourcelist[i] + "-" + str(j) + "\n")
        s_source.close()

	for item in testlist:
            item = item.replace('/','.')
            if item not in namelist_normal:
                f_log.write(item + "\n")
                continue
            f_test.write(item + "\n")
            temp_index = namelist_normal.index(item)
            temp_list = getAllCall(temp_index,call_dict)
            for i in sourcelist:
                i_index = namelist.index(i)
                if i_index in temp_list:
                    f.write("1")
                    count += 1
                elif i_index not in temp_list:
                    f.write("0")
            f.write("\n")
        f.close()
        f_test.close()
        f_log.close()
        
        for item in testlist:
            item = item.replace('/','.')
            if item not in namelist_normal:
                continue
            s_test.write(item + "\n")
            temp_index = namelist_normal.index(item)
            temp_list = getAllCall(temp_index,call_dict)
            for i in sourcelist:
                i_index = namelist.index(i)
                if sourcelist_linenumber[sourcelist.index(i)] == 0:
                    temp_number = 1
                else:
                    temp_number = sourcelist_linenumber[sourcelist.index(i)]
                if i_index in temp_list:
                    for j in range(temp_number):
                        s.write("1")
                elif i_index not in temp_list:
                    for j in range(temp_number):
                        s.write("0")
            s.write("\n")
        s.close()
        s_test.close()
        #s_log.close()
        
        #raw_input(subject + ' check ...')









