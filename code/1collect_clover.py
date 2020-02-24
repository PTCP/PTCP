import os
import sys
import commands
import time
from xml.dom.minidom import parse
import xml.dom.minidom
import xml.etree.ElementTree as ET
from lxml.etree import Element,SubElement,tostring
import pprint
from xml.dom.minidom import parseString
from lxml import etree


def readFile(filepath):
    f = open(filepath)
    content = f.read()
    f.close()
    return content.splitlines()


def writeFile(filepath,filecontent):
    f = open(filepath,'a')
    f.write(filecontent + '\n')
    f.close()

def readFile_content(filepath):
    f = open(filepath)
    content = f.read()
    f.close()
    return content

if __name__ == '__main__':
    path = '/PTCP/subject/source/'
    success = path + 'successlist'
    fail = path + 'faillist'
    fail_log = '[INFO] BUILD FAILURE\n'
    success_log = '[INFO] BUILD SUCCESS\n'

    clover = '''
	<dependency>
            <groupId>org.openclover</groupId>
            <artifactId>clover-maven-plugin</artifactId>
            <version>4.2.0</version>
            <type>maven-plugin</type>
        </dependency>


    '''
    #filelist = os.listdir(path)
    #f = open(path + 'sublist','w')
    #for fileitem in filelist:
    #    f.write(fileitem + '\n')
    #f.close()
    filelist = readFile(path + 'uselist-add')


	
    for fileitem in filelist:
        sub_path = path + fileitem + '/'
        print(sub_path)
        os.chdir(sub_path)
        pom = sub_path + 'pom.xml.ori'
        #output = commands.getoutput('mvn test')
	#commands.getoutput('cp pom.xml pom.xml.ori')
	
        #if fail_log in output:
        #    writeFile(fail,fileitem)
        #elif success_log in output:
        #    writeFile(success,fileitem)    

         
        print pom
        ns_all = etree.fromstring(readFile_content(pom)).nsmap
        ns = etree.fromstring(readFile_content(pom)).nsmap[None]
        for item in ns_all:
            if item == None:
                ET.register_namespace('',ns_all[item])
            else:
                ET.register_namespace(item,ns_all[item])
        tree = ET.parse(pom)
        print 'namespace : ' + ns

        root = tree.getroot()
        dependency_node = root.findall('{' + ns + '}' + 'dependencies')[0]
        print dependency_node.tag
        dependency_node.append(ET.fromstring(clover))
        #plugins_node = build_node.findall('{' + ns + '}' + 'dependencies')
        #plugins_node.append(ET.fromstring(clover))
        tree.write(sub_path + 'pom.xml.openclover', encoding="utf-8",xml_declaration=True,method='xml')
        
        
        commands.getoutput('cp pom.xml.openclover pom.xml')
        stime = time.time()
        output = commands.getoutput('mvn clean clover:setup test clover:aggregate clover:clover')
        timelog = time.time() - stime
        f = open(sub_path + 'clover-log','w')
        f.write(str(output))
        f.close()
        f = open(sub_path + 'clover-time','w')
        f.write(str(timelog))
        f.close()
        print fileitem + ' is completed!'
        #raw_input('check...')
