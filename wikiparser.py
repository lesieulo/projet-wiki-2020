
import os
import xml.etree.ElementTree as etree
import time
import csv
import sys

def log(logFileName, line):
    print(line)
    logFile = open(logFileName, 'a') 
    logFile.write(line)
    logFile.close()
    return


def parse(path, dump):  
    """
    Parse a wikipedia xml dump file.
    It creates a folder for each page, and a text file for each revision.
    Metadata log file with id, oldid, timestamp
    """    
    pathDump = os.path.join(path, dump)
    pageId = 0              # current page id
    revId = 0               # current revision id
    parentId = ''            # current parent id
    expectPageId = False
    expectRevId = False
    nPage = 0               # number of pages
    prefix = "{http://www.mediawiki.org/xml/export-0.10/}"
    logFileName = path + 'logParse.txt'
    
    time0 = time.time()
    
    log(logFileName, '---Reading xml dump file---\n')
    for event, elem in etree.iterparse(pathDump, events=('start', 'end')):
        elemTag = elem.tag[len(prefix):]
        
        if event == 'start':
            if elemTag == 'page':
                expectPageId = True
                nPage += 1

            elif elemTag == 'revision':
                expectRevId = True

        else:
            if elemTag == 'id':
                if expectPageId:
                    pageId = elem.text
                    os.mkdir(path + str(pageId))
                    os.mkdir(path + str(pageId) + '/revisions')
                    os.mkdir(path + str(pageId) + '/differences')
                    expectPageId = False
                elif expectRevId:
                    revId = elem.text
                    expectRevId = False
                    
            elif elemTag == 'parentid':
                parentId = elem.text
                
            elif elemTag == 'timestamp':
                timestamp = elem.text
                
            elif elemTag == 'text':
                if type(elem.text) == str:
                    fileName = str(revId) + '-' + str(parentId)
                    pathRev = path + str(pageId) + '/revisions/' + fileName
                    file = open(pathRev, 'w') 
                    file.write(elem.text)
                    file.close()
                    
                metadataFile = path + str(pageId) + '/metadata.csv'
                with open(metadataFile, 'a', newline=None) as file:  
                    csvwriter = csv.writer(file)
                    csvwriter.writerow([revId, parentId, timestamp])
                revId, parentId, timestamp = '', '', ''
                    
            elif elemTag == 'page':
                logLine = 'Page {} done\n'.format(pageId)
                log(logFileName, logLine)
            elem.clear()

    log(logFileName, '---Done---\nTotal {} pages\n'.format(nPage))
    
    seconds = time.time() - time0
    minutes = int(seconds / 60)
    log(logFileName, '{} minutes\n'.format(minutes))
    
    return



if __name__ == "__main__":
    
    pathAndDump = sys.argv[1]
    path, dump = os.path.split(pathAndDump)
    path += '/'
    
    parse(path, dump)

    
    
