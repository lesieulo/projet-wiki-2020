
from wikiparser import parse, log
from levenshtein import process, write_diffs, read_diffs
import os
import glob
import time
import csv
import sys

def find_pairs(pathDump, pageId, seuil, cont, filtre):
    '''
    Algo: trouve toutes les paires revId-parentId parmi toutes les révisions
        de la page wiki et fait les différences.
    '''
    logFileName = path+'logDiff.txt'
    pathRevisions = pathDump + pageId + '/revisions/'
    n = len(pathRevisions)
    list_rev = glob.glob(pathRevisions + '*')
    
    def diff_process(fn_r1, fn_r2, seuil, cont, filtre):

        rev1 = open(pathRevisions + fn_r1, "r")
        rev2 = open(pathRevisions + fn_r2, "r")
        r1 = rev1.read()
        r2 = rev2.read()
        diffs = process(r1, r2, seuil, cont, filtre)
        if diffs:
            fname = pathDump + pageId + '/differences/' + fn_r2 + '.csv'
            write_diffs(fname, diffs)
                
        rev1.close()
        rev2.close()

    
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
        if int(pageId) != 15821: # TODO: cas où il n'y a pas de différences
            time1 = time.time()
            find_pairs(path, pageId, seuil, cont, filtre)
            time_page = int(time.time() - time1)
            logLine = 'Page {} done in {} seconds\n'.format(pageId, time_page)
            log(logFileName, logLine)
        
    log(logFileName, '---Done---\n')
    seconds = time.time() - time0
    minutes = int(seconds / 60)
    log(logFileName, 'Total: {} minutes\n'.format(minutes))
    return



if __name__ == "__main__":
    

    pathAndDump = sys.argv[1]
    path, dump = os.path.split(pathAndDump)
    path += '/'
    
    parse(path, dump)
    
    process_dump(path, dump)