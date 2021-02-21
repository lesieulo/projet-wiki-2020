# Comparaison python et C

Tests pour comparer les performances de:
- python
- C
- C2 = C avec optimisation O2
- C3 = C avec optimisation O3

Lignes des logs:
Groupes de 5 lignes (5 runs) par jeu de données.

Colonnes des logs:
- cas python -> total, levenshtein, alignment, differences
- cas C -> total, write_unicode, subprocess, lecture_alignment, differences

10*10 = 100
python	0.001
C	0.005
C2	0.006
C3	0.005

70*70 = 4900
python	0.024
C	0.007
C2	0.008
C3	0.006 (sans compter outlier 0.087)

280*280 = 78400
python	0.376
C	0.012
C2	0.011
C3	0.009

Conclusion: C et C2 ne sont jamais les meilleurs. On peut choisir d'utiliser python ou C3 selon la taille du tableau. Pour les gros tableaux, on appelle C. Limite ?
Total pour 32*32=1024:
python	0.005
C3 	0.005

BILAN:
Taille tableau <= 1000 -> python
Taille tableau > 1000 -> C avec optimisation O3.

# Au-delà du filtre 1e5

500*500 = 250.000
python	1.242
C3	0.013 (subprocess: 0.008)

1000*1000 = 1.000.000
python	5.020
C3	0.294 (subprocess: 0.291)







