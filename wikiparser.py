
import os
import xml.etree.ElementTree as etree
import time

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
    """    
    pathDump = os.path.join(path, dump)
    pageId = 0              # current page id
    revId = 0               # current revision id
    timestamp = ''          # current timestamp
    expectPageId = False
    expectRevId = False
    nPage = 0
    n, nNone = 0, 0               # nbre de pbs revId=None ou ts=None
    prefix = "{http://www.mediawiki.org/xml/export-0.10/}"
    logFileName = path+'dumpLog.txt'
    
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
                n += 1

        else:
            if elemTag == 'id':
                if expectPageId:
                    pageId = elem.text
                    os.mkdir(path+str(pageId))
                    expectPageId = False
                elif expectRevId:
                    revId = elem.text
                    expectRevId = False
                    
            elif elemTag == 'timestamp':
                timestamp = elem.text
                if timestamp == None or revId == None:
                    nNone += 1
                    print(pageId, str(revId), str(timestamp))
            
            elif elemTag == 'text':
                if type(elem.text) == str:
                    fileName = path + str(pageId) + '/' + str(revId)
                    file = open(fileName, 'w') 
                    file.write(elem.text)
                    file.close()
                    
            elif elemTag == 'page':
                logLine = 'Page {}. {} revisions dont {} pbs None\n'.format(pageId, n, nNone)
                log(logFileName, logLine)
                n, nNone = 0, 0
            elem.clear()

    log(logFileName, '---Done---\nTotal {} pages\n'.format(nPage))
    
    seconds = time.time() - time0
    minutes = int(seconds / 60)
    log(logFileName, '{} minutes\n'.format(minutes))
    
    return


if __name__ == "__main__":
    
    case = 0
    
    if case == 0:
        path = "/media/louis/TOSHIBA EXT/data/dump1/"
        dump = "enwiki-20200901-pages-meta-history1.xml-p15606p16009"
    elif case == 1:
        path = "/media/louis/TOSHIBA EXT/data/hermit-dump/"
        dump = "wiki-little-hermit-history.xml"
    elif case == 2:
        path = "/media/louis/TOSHIBA EXT/data/john/"
        dump = "john-tenniel.xml"

    parse(path, dump)

    
    
