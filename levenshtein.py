

import numpy as np
import os
from time import time


def levenshtein(s, t):
    
    m = len(s)
    n = len(t)
    
    D = np.zeros((m+1, n+1), dtype=int)
    pathMatrix = np.empty((m+1, n+1), dtype=str)
    
    for i in range(1, m+1):
        D[i, 0] = i
    for j in range(1, n+1):
        D[0, j] = j
        
    for i in range(1, m+1):
        for j in range(1, n+1):
            if s[i-1] == t[j-1]:
                substitutionCost = 0
            else:
                substitutionCost = 1
            deletion = D[i-1, j] +1
            insertion = D[i, j-1] +1
            substitution = D[i-1, j-1] + substitutionCost
            
            mini = min(deletion, insertion, substitution)
            D[i, j] = mini
            
            if mini == deletion:
                pathMatrix[i, j] = 'D'
            elif mini == insertion:
                pathMatrix[i, j] = 'I'
            elif mini == substitution:
                pathMatrix[i, j] = 'S'
                
        #print(D, '\n')
        #print(pathMatrix)
    return pathMatrix

def alignment(s, t, pathMatrix):
    
    m = len(s)
    n = len(t)
    align = np.empty((2, m+n), dtype=str)
    
    k = m + n - 1
    i, j = m, n
    direction = pathMatrix[i][j]

    while direction != '':
        s_car, t_car = s[i-1], t[j-1]
        if direction == 'S':
            align[0][k] = s_car
            align[1][k] = t_car
            i -= 1
            j -= 1
        elif direction == 'D':
            align[0][k] = s_car
            i -= 1
        elif direction == 'I':
            align[1][k] = t_car
            j -= 1
        direction = pathMatrix[i][j]
        k -= 1
        
    #print(align)
    return align


def compare(s, t, align, n_display=130):
    
    m, n = len(s), len(t)  # virer t et s, on a déjà l'info m+n
    s2, t2 = '', ''
    for k in range(m+n):
        s_car, t_car = align[0][k], align[1][k]
        if s_car != '' or t_car != '':
            if s_car == '':
                s2 += '-'
            else:
                s2 += s_car
            if t_car == '':
                t2 += '-'
            else:
                t2 += t_car

    for i in range(len(s2)//n_display + 1):
        print('\n')
        print(s2[i*n_display:(i+1)*n_display])
        print(t2[i*n_display:(i+1)*n_display])
    
    return s2, t2

def compare2(s, t, align):
    m, n = len(s), len(t)
    in_modif = False
    l_s, l_t = [], []
    
    for k in range(m+n):
        s_car, t_car = align[0][k], align[1][k]
        
        if not in_modif:
            if s_car != t_car:
                in_modif = True
                l_s.append(s_car)
                l_t.append(t_car)
        else:
            if s_car == t_car:
                in_modif = False
            else:
                l_s[-1] += s_car
                l_t[-1] += t_car
    
    for k in range(len(l_s)):
        print('\n Modif', k, "len", len(l_s[k]), len(l_t[k]))
        print('S', l_s[k])
        print('T', l_t[k])
    
    return 
        
        
        


if __name__ == "__main__":
    
    #s = "levenshtein"
    #t = "meilenstein"
    s = "CTATCACCTGACCTCCAGGCCGATGCCCCTTCCGGC"
    t = "GCGAGTTCATCTATCACGACCGCGGTCG"
    
    #path = levenshtein(s, t)
    #align = alignment(s, t, path)
    #compare = compare(s, t, align)
    
    path = "../../../data/hermit-dump/"
    page_id = 1284561
    rev1_id = 8483054
    rev2_id = 8483079
    
    path_rev1 = os.path.join(path, str(page_id), str(rev1_id))
    path_rev2 = os.path.join(path, str(page_id), str(rev2_id))
    
    rev1 = open(path_rev1, "r")
    rev2 = open(path_rev2, "r")
    
    r1 = rev1.read()
    r2 = rev2.read()
    
    t0 = time()
    path = levenshtein(r1, r2)
    t1 = time()
    print("levenhstein:", t1-t0)
    
    align = alignment(r1, r2, path)
    t2 = time()
    print("alignment:", t2-t1)
    
    my_compare = compare2(r1, r2, align)
    t3 = time()
    print("compare:", t3-t2)
    
    rev1.close()
    rev2.close()
    
    
    
    
    
    
    
    
    