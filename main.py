
from wikiparser import parse
from levenshtein import process, write_diffs, read_diffs



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

# Parser le dump
parse(path, dump)

# Choisir la page et révisions à extraire, rev1=avant, rev2=après
page_id = '1284561'
rev1_id = '8483054-'
rev2_id = '8483079-8483054'

path_rev1 = path + page_id + '/revisions/' + rev1_id
path_rev2 = path + page_id + '/revisions/' + rev2_id

# Calculer les différences
diffs = process(path_rev1, path_rev2)

# Ecriture et lecture
fname = path + page_id + '/differences/' + rev2_id + '.csv'
write_diffs(fname, diffs)
rdiffs = read_diffs(fname, display=True)







