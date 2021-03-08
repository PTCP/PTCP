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
import copy
from tqdm import tqdm


# read file, return as list
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

# convert list to dictionary
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

# get all calls start from ini_point
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

#get all java files in dir '/src/test/xxxx'
def getFileList(pppath):
    filelist = []
    for root, dirs, filenames in os.walk(pppath):
        for filename in filenames:
            #print "the full name of the file is:" + os.path.join(root,filename)
            if ".java" in filename and "/test/" in root:
                #if "Test" not in filename:
                filelist.append(os.path.join(root,filename))
    return filelist

# decide whether the item in objectlist are the element in ppp
def isFilter(objectlist,ppp):
    temp_count = 0
    for item in objectlist:
        if item in ppp:
            temp_count = 1
            break
    return temp_count

# generate call graph from call-graph-info.txt
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
            # extract name, number from the line 
            temp = item[2:]
            temp_name = temp.split("|")[0].rstrip(" ").replace(":",".")
            temp_number = temp.split("|")[1].lstrip(" ")
            temp_tt = temp_name.split("(")[0]
            if temp_name not in sourcemethodlist:
                # extract all methods in source code, and store them in sourcemethodlist
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

    

if __name__ == '__main__':
    path_s = './subjects/source/'
    path_e = './subjects/experiment/'
    subjects = readFile(path_s + 'uselist-noclover2')
    #for subject in tqdm(subjects):
    for subject in subjects:
        print(subject)
        subject_path_s = path_s + subject + '/'
        subject_path_e = path_e + subject + '/'
        if os.path.exists(subject_path_e) == False:
            os.makedirs(subject_path_e)
        # copy call-graph-info.txt file from the dir ./subjects/source/xx
        os.system('cp %s %s'%(subject_path_s + 'call-graph-info.txt', subject_path_e + 'call-graph-info.txt'))
        # create the dir for static coverage information on testmethod-level
        if os.path.exists(subject_path_e + 'testmethod/callgraph/') == False:
            os.makedirs(subject_path_e + 'testmethod/callgraph/')

        namelist,namelist_normal,sourcelist,sourcelist_linenumber,testlist,call_dict = getCallGraph(subject_path_e,"testmethod")

	
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

        # function coverage 
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
        
        # statement coverage 
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









