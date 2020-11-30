
from wikiparser import parse
from levenshtein import process, write_diffs, read_diffs
import os
import glob


def find_pairs(pathDump, pageId):
    '''
    Algo: trouve toutes les paires revId-parentId parmi toutes les révisions
        de la page wiki et fait les différences.
    '''
    pathRevisions = pathDump + pageId + '/revisions/'
    revStar = pathRevisions + '*'
    n = len(revStar)
    
    def diff_process(r1, r2):
        path_rev1 = pathRevisions + r1
        path_rev2 = pathRevisions + r2
        print(5, path_rev1)
        print(5, path_rev2)
        diffs = process(path_rev1, path_rev2)
        fname = pathDump + pageId + '/differences/' + r2 + '.csv'
        write_diffs(fname, diffs)
        
    r1 = glob.glob(revStar + '-')[0][n-1:]
    r2 = glob.glob(revStar + '-' + r1[:-1])[0][n-1:]
    diff_process(r1, r2)
    # print("revId {} avec parentId {}".format(r2, r1))
    
    def l_children(rev, revStar):
        # Liste des révisions qui ont rev pour parent
        return glob.glob(revStar + '-' + rev[:rev.index('-')])
    
    i = 1
    while l_children(r2, revStar) != []:
        i += 1
        print(i)
        r1 = r2
        r2 = l_children(r1, revStar)[0][n-1:]
        #print("enfant", r2)
        #print("père", r1)
        diff_process(r1, r2)

    return


if __name__ == "__main__":
    

    # Choisir le dump
    case = 1
    
    if case == 0:
        path = "/media/louis/TOSHIBA EXT/data/dump1/"
        dump = "enwiki-20200901-pages-meta-history1.xml-p15606p16009"
    elif case == 1:
        path = "/media/louis/TOSHIBA EXT/data/hermit-dump/"
        dump = "wiki-little-hermit-history.xml"
    elif case == 2:
        path = "/media/louis/TOSHIBA EXT/data/john/"
        dump = "john-tenniel.xml"
    
    pathDump = path
    pageId = '1284561'
    
    
    
    
    
    
    
    # parse(path, dump)
    
    # find_pairs(pathDump, pageId)
    
    
    
    # Choisir la page et révisions à extraire, rev1=avant, rev2=après
    revId = '502289165-497506271'
    pathRev = path + pageId + '/revisions/' + revId
    
    # Ecriture et lecture
    fname = path + pageId + '/differences/' + revId + '.csv'
    rdiffs = read_diffs(fname, display=True)
    






