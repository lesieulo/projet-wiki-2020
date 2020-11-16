
import os
import xml.etree.ElementTree as etree


def parse(pathDump):
    """
    Parse a wikipedia xml dump file.
    It creates a folder for each page, and a text file for each revision.
    """    
    dictPageRevisions = {}  # page: liste des révisions
    pageId = 0              # current page id
    revId = 0               # current revision id
    expectPageId = False
    expectRevId = False
    nStr, nNone = 0, 0      # number of string content in wiki <text>
    prefix = "{http://www.mediawiki.org/xml/export-0.10/}"

    print('---Reading xml dump file---')
    for event, elem in etree.iterparse(pathDump, events=('start', 'end')):
        elemTag = elem.tag[len(prefix):]
        
        if event == 'start':
            if elemTag == 'page':
                expectPageId = True
                
            elif elemTag == 'revision':
                expectRevId = True
                
            elif elemTag == 'id':
                if expectPageId:
                    pageId = elem.text
                    dictPageRevisions[pageId] = {}
                    os.mkdir(path+str(pageId))
                    expectPageId = False
                elif expectRevId:
                    revId = elem.text
                    dictPageRevisions[pageId][revId] = False
                    expectRevId = False
        else:
            if elemTag == 'text':
                if type(elem.text) == str:
                    dictPageRevisions[pageId][revId] = True
                    fileName = path + str(pageId) + '/' + str(revId)
                    file = open(fileName, 'w') 
                    file.write(elem.text)
                    file.close()
                    nStr += 1
                else:
                    nNone +=1
            elif elemTag == 'page':
                nRevisions = len(dictPageRevisions[pageId])
                print('Page {}. {} revisions: {} text, {} None'.format(pageId, nRevisions, nStr, nNone))
                nStr, nNone = 0, 0
            elem.clear()
    print('---Done---')
    
    return


if __name__ == "__main__":
    
    #path = "../../../data/dump1/"
    #dump = "enwiki-20200901-pages-meta-history1.xml-p15606p16009"
    
    path = "../../../data/hermit-dump/"
    dump = "wiki-little-hermit-history.xml"
    
    pathDump = os.path.join(path, dump)
    parse(pathDump)
    
    
