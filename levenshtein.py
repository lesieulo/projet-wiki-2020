import numpy as np
import os
from time import time
import csv

def opti(s, t):
    '''
    Suppression du préfixe commun, et du suffixe commun.
    '''
    a = 0
    while s[a] == t[a]:
        a += 1
    if s[-1] != t[-1]:
        return s[a:], t[a:]
    else:
        z = 0
        while s[z-1] == t[z-1]:
            z -= 1
    return s[a:z],t[a:z]
    

def levenshtein(s, t):
    '''
    Inputs: 2 str to be compared
    Output: Levenshtein path matrix, composed of D, I and S.
    '''
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
    '''
    Inputs: 2 str and the Levenshtein path matrix
    Output: matrice d'alignement avec 2 lignes, chaque ligne contient
        les caractères de son str, avec éventuellement des ' ' pour I et D.
        On remplit en partant de la fin, le début est donc souvent vide.
    '''
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
        
    a = 0
    while align[0][a] == align[1][a]:
        a += 1
    new_align = np.empty((2, m+n-a), dtype=str)
    new_align[0] = align[0][a:]
    new_align[1] = align[1][a:]

    return new_align


def compare(s, t, align, n_display=60):
    '''
    Inputs: 2 str, matrice d'alignement, n_display=nombre de caractères
        à afficher sur une ligne.
    Output: Nouvelles chaînes de caractères avec '-' pour visualiser
        l'alignement.
    '''
    s2, t2 = '', ''
    for k in range(align.shape[1]):
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


def differences(s, t, align, seuil, cont):
    '''
    Inputs: 2 str, matrice d'alignement,
        seuil = nombre de caractères égaux consécutifs qu'on autorise au sein
        d'une différence.
        cont = nombre de caractères de contexte qu'on garde de chaque côté.
    Outputs: liste de différences. Chaque différence est une liste de 4:
        (texte de s, texte de t, contexte à G, contexte à D).
        
    Remarques sur le contexte:
        1. on prend celui de s
        2. les préfixe/suffixe communs de s et t sont déjà supprimés donc
        ils ne font pas partie du contexte. La 1ère différence n'a pas le
        contexte avant, et la dernière le contexte après.
    '''
    # Construction de tuples, qui permet d'obtenir les indices des séquences
    # ininterrompues de caractères différents (resp. égaux) dans align.
    equals = [align[0][k] == align[1][k] for k in range(align.shape[1])]
    flag = [equals[k] != equals[k+1] for k in range(align.shape[1]-1)]
    index = []
    for i in range(len(flag)):
        if flag[i] == True:
            index.append(i+1)    
    index = [0] + index + [align.shape[1]]
    tuples = [(index[i], index[i+1]) for i in range(len(index)-1)]

    # Construction de index_diffs, liste de couples d'indices start,end 
    # pour chaque différence. C'est ici qu'on regarde si une séquence de 
    # caractères égaux est conservée dans une différence.
    index_diff = []
    start = 0
    inDiff = True
    for i in range(0, len(tuples)-2, 2):
        change = tuples[i]
        equal = tuples[i+1]        
        if inDiff:
            if equal[1] - equal[0] > seuil:
                # End diff
                index_diff.append((start,change[1]))
                inDiff = False
        else:
            # Start diff
            start = change[0]
            inDiff = True
            if equal[1] - equal[0] > seuil:
                # End diff
                index_diff.append((start,change[1]))
                inDiff = False
    # Dernier tuple
    change = tuples[-1]
    if inDiff:
        index_diff.append((start,change[1]))
    else:
        index_diff.append(change)

    # Sauvegarde des str
    l_diffs = []
    for ind in index_diff:
        i0, i1 = ind[0], ind[1]
        sDiff, tDiff, contG, contD = '', '', '', ''
        for c in align[0][i0:i1]:
            sDiff += c
        for c in align[1][i0:i1]:
            tDiff += c
        for c in align[0][i0-cont:i0]:
            contG += c
        for c in align[0][i1:i1+cont]:
            contD += c
        display_diff = '\nS: {}\nT: {}\nC: {}  |  {}'
        print(display_diff.format(sDiff, tDiff, contG, contD))
        difference = [sDiff, tDiff, contG, contD]
        l_diffs.append(difference)

    return l_diffs
    

def process(path_rev1, path_rev2, seuil=10, cont=10):
    '''
    Inputs: chemins pour 2 fichiers de révisions.
    Output: liste des différences.
    '''
    # Read data
    rev1 = open(path_rev1, "r")
    rev2 = open(path_rev2, "r")
    r1 = rev1.read()
    r2 = rev2.read()

    # Pre-process, Levenshtein algo
    r1, r2 = opti(r1, r2)
    t0 = time()
    path = levenshtein(r1, r2)
    t1 = time()
    print("levenhstein:", t1-t0)
    
    # Align, Compare, Diffs
    align = alignment(r1, r2, path)
    compare(r1, r2, align, n_display=130)
    diffs = differences(r1, r2, align, seuil, cont)
    rev1.close()
    rev2.close()
    
    return diffs
        


if __name__ == "__main__":
    
    
    '''
    s = 'BBBBBAAAAAACADAAEAAAFA'
    t = 'AAAAAAAAAAAAAAAAAAAAAA'
    s, t = opti(s, t)
    path = levenshtein(s, t)
    align = alignment(s, t, path)
    compare(s, t, align)
    differences(s, t, align, seuil=2, cont=4)
    '''
    
    
    # HERMIT EX
    path = "/media/louis/TOSHIBA EXT/data/hermit-dump/"
    page_id = 1284561
    rev1_id = 8483054
    rev2_id = 8483079
    path_rev1 = os.path.join(path, str(page_id), str(rev1_id))
    path_rev2 = os.path.join(path, str(page_id), str(rev2_id))
    
    # SENTENCE EX
    #path_rev1 = "/media/louis/TOSHIBA EXT/data/sentence/1"
    #path_rev2 = "/media/louis/TOSHIBA EXT/data/sentence/2"
    
    diffs = process(path_rev1, path_rev2)
    for diff in diffs:
        print(diff)
        
        
    

    
    
    
    
    
    
    