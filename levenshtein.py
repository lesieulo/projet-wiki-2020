import numpy as np
import os
from time import time


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

    return align


def compare(s, t, align, n_display=60):
    '''
    Inputs: 2 str, matrice d'alignement, n_display=nombre de caractères
        à afficher sur une ligne.
    Output: Nouvelles chaînes de caractères avec '-' pour visualiser
        l'alignement.
    '''
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


def differences(s, t, align, seuil):
    '''
    Inputs: 2 str, matrice d'alignement, seuil = nombre de caractères égaux
        consécutifs qu'on autorise au sein d'une différence.
    Algo: parcourt la matrice d'alignement et enregistre les différences en 
        levant des flags.
    Outputs: 2 listes de différences, une différence correspond à un indice i,
        la partie de s est l_s[i] et celle de t l_s[i].
    '''
    m, n = len(s), len(t)
    l_s, l_t = [], []
    inDiff = align[0][0] != align[1][0]
    flagEqual = False
    equalStr = ''
    
    for k in range(m+n):
        s_car, t_car = align[0][k], align[1][k]
        
        if inDiff:
            if s_car == t_car:
                if flagEqual:
                    if len(equalStr) >= seuil:
                        # Fin de la différence
                        flagEqual= False
                        inDiff = False
                        equalStr = ''
                    else:
                        # Contribution à la période d'égalité
                        equalStr += s_car
                else:
                    if seuil == 0:
                        inDiff = False
                    else:
                        #Initialisation d'une période d'égalité
                        flagEqual = True
                        equalStr = s_car
            else:
                if flagEqual:
                    # Contribution de la période d'égalité à la différence
                    l_s[-1] += equalStr
                    l_t[-1] += equalStr
                    flagEqual = False
                    equalStr = ''
                # Contribution à la différence
                l_s[-1] += s_car
                l_t[-1] += t_car
        else:
            if s_car != t_car:
                # Init d'une nouvelle différence
                inDiff = True
                l_s.append(s_car)
                l_t.append(t_car)

    for k in range(len(l_s)):
        modif = '\n-----Modif {}, len {} {}-----\nS: {}\nT: {}'
        print(modif.format(k, len(l_s[k]), len(l_t[k]), l_s[k], l_t[k]))
    
    return l_s, l_t
        


if __name__ == "__main__":
    
    '''
    s = 'BBBBBAAAAAACADAAEAAAF'
    t = 'AAAAAAAAAAAAAAAAAAAAA'
    
    path = levenshtein(s, t)
    align = alignment(s, t, path)
    compare(s, t, align)
    differences(s, t, align, 1)
    '''
    
    
    
    # HERMIT EX
    path = "/media/louis/TOSHIBA EXT/data/hermit-dump/"
    page_id = 1284561
    rev1_id = 8483054
    rev2_id = 8483079
    path_rev1 = os.path.join(path, str(page_id), str(rev1_id))
    path_rev2 = os.path.join(path, str(page_id), str(rev2_id))
    
    # SENTENCE EX
    path_rev1 = "/media/louis/TOSHIBA EXT/data/sentence/1"
    path_rev2 = "/media/louis/TOSHIBA EXT/data/sentence/2"
    
    # READ DATA
    rev1 = open(path_rev1, "r")
    rev2 = open(path_rev2, "r")
    r1 = rev1.read()
    r2 = rev2.read()
    
    # LEVENSHTEIN
    t0 = time()
    path = levenshtein(r1, r2)
    t1 = time()
    print("levenhstein:", t1-t0)
    
    # ALIGN
    align = alignment(r1, r2, path)
    
    # COMPARE
    compare(r1, r2, align)
    
    # DIFF
    for seuil in [0, 2, 5, 10]:
        print("\n SEUIL {}".format(seuil))
        differences(r1, r2, align, seuil)
    
    rev1.close()
    rev2.close()
    
    
    
    
    
    
    
    
    