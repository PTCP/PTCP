import os
import sys
import commands
from xml.dom.minidom import parse
import xml.dom.minidom
import xml.etree.ElementTree as ET
from lxml.etree import Element,SubElement,tostring
import pprint
from xml.dom.minidom import parseString
from lxml import etree

# read file, return list
def readFile(filepath):
    f = open(filepath)
    content = f.read()
    f.close()
    return content.splitlines()

# read file, return string
def readFile_content(filepath):
    f = open(filepath)
    content = f.read()
    f.close()
    return content

if __name__ == '__main__':
    path = './subjects/source/'

    iDFlakies = '''
	<plugin>
            <groupId>edu.illinois.cs</groupId>
            <artifactId>testrunner-maven-plugin</artifactId>
            <version>1.0</version>
            <dependencies>
                <dependency>
                    <groupId>edu.illinois.cs</groupId>
                    <artifactId>idflakies</artifactId>
                    <version>1.0.1-SNAPSHOT</version>
                </dependency>
            </dependencies>
            <configuration>
                <className>edu.illinois.cs.dt.tools.detection.DetectorPlugin</className>
            </configuration>
        </plugin>
        ''' 
    filelist = readFile(path + 'uselist-add')
	
    for fileitem in filelist:
        sub_path = path + fileitem + '/'
        os.chdir(sub_path)
        pom = sub_path + 'pom.xml.ori'

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
        build_node = root.findall('{' + ns + '}' + 'build')[0]
        print build_node.tag
        plugins_node = build_node.findall('{' + ns + '}' + 'plugins')
        plugins_node[0].append(ET.fromstring(iDFlakies))
        tree.write(sub_path + 'pom.xml.iDFlakies', encoding="utf-8",xml_declaration=True,method='xml')
        
        commands.getoutput('cp pom.xml.iDFlakies pom.xml')
        output = commands.getoutput('mvn testrunner:testplugin -Ddetector.detector_type=random-class-method -Ddt.randomize.rounds=10')
        f = open(sub_path + 'iDFlakies-log','w')
        f.write(str(output))
        f.close()
        
        print fileitem + ' is completed!'
        #raw_input('check...')
