
from wikiparser import parse, log
from levenshtein import process, write_diffs, read_diffs
import os
import glob
import time


def find_pairs(pathDump, pageId, seuil, cont, filtre):
    '''
    Algo: trouve toutes les paires revId-parentId parmi toutes les révisions
        de la page wiki et fait les différences.
    '''
    pathRevisions = pathDump + pageId + '/revisions/'
    n = len(pathRevisions)
    list_rev = glob.glob(pathRevisions + '*')
    
    def diff_process(r1, r2, seuil, cont, filtre):
        path_rev1 = pathRevisions + r1
        path_rev2 = pathRevisions + r2
        diffs = process(path_rev1, path_rev2, seuil, cont, filtre)
        if diffs:
            fname = pathDump + pageId + '/differences/' + r2 + '.csv'
            write_diffs(fname, diffs)
    
    while list_rev:
        rev = list_rev.pop(0)[n:]
        before_rev = glob.glob(pathRevisions + rev[rev.index('-')+1:] + '-*')
        after_rev = glob.glob(pathRevisions + '*-' + rev[:rev.index('-')])
        if before_rev:
            diff_process(before_rev[0][n:], rev, seuil, cont, filtre)
        if after_rev:
            diff_process(rev, after_rev[0][n:], seuil, cont, filtre)
    return


def process_dump(path, dump, seuil=10, cont=10, filtre=1e5):
    '''
    Ecrit les différences de toutes les pages du dump.
    '''
    logFileName = path+'logDiff.txt'
    time0 = time.time()
    
    log(logFileName, '---Writing differences---\n')
    pages = [f for f in os.listdir(path) if f.isdigit()]
    for pageId in pages:
        if int(pageId) != 15821:
            time1 = time.time()
            find_pairs(path, pageId, seuil, cont, filtre)
            time_page = int(time.time() - time1)
            logLine = 'Page {} done in {} seconds\n'.format(pageId, time_page)
            log(logFileName, logLine)
        
    log(logFileName, '---Done---')
    seconds = time.time() - time0
    minutes = int(seconds / 60)
    log(logFileName, 'Total: {} minutes\n'.format(minutes))
    return


if __name__ == "__main__":
    

    # Choisir le dump
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



    #parse(path, dump)

    #process_dump(path, dump)
    
    
    


