import os
from tqdm import tqdm
import commands

def readFile(filepath):
    f = open(filepath)
    content = f.read()
    f.close()
    return content.splitlines()


if __name__ == '__main__':
    path = '/PTCP/subjects/source/'

    subjects = readFile(path + 'uselist-all')

    for subject in tqdm(subjects):
        subject_path = path + subject
        # make .jar file
        if os.path.exists(subject_path + '/target/classes/main.jar') == False or os.path.exists(subject_path + '/target/test-classes/test.jar') == False:
            if os.path.exists(subject_path + '/target/classes') == True:
                os.chdir(subject_path + "/target/classes")
                os.system('jar cvf main.jar *')
            if os.path.exists(subject_path + '/target/test-classes') == True:
                os.chdir(subject_path + "/target/test-classes")
                os.system('jar cvf test.jar *')

        # generate call graph
        mainjar = subject_path + '/target/classes/main.jar'
        testjar = subject_path + '/target/test-classes/test.jar'
        os.chdir('/PTCP/code/tool/java-callgraph-master/target/')
        templist = commands.getoutput("java -jar javacg-0.1-SNAPSHOT-static.jar " + mainjar + " " + testjar)
        resultfile = subject_path + '/call-graph-info.txt'
        f = open(resultfile,'w')
        f.write(templist)
        f.close()


