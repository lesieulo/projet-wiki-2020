#!/bin/bash
# For each page, for each diff file, add content to alldiff.csv

touch alldiff.csv

for page in `ls -d 1*`
	do
	for d in `ls $page/differences/*`
		do
		cat $d >> alldiff.csv
		done
	done
			
