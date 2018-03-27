#!/usr/bin/python
# -*- coding: utf-8 -*-

#This script works with a file containing a list of HyLiTE read.summary files.
from pprint import pprint
import csv
import sys
import re
import os
import argparse
from itertools import islice
import collections
import pandas as pd

hyliteSNP = sys.argv[1] #HyliTE.snp.txt file
#inputFile = sys.argv[2] #.bam alignment file
outputName = sys.argv[2] #output name

myList = []
dP1 = collections.defaultdict(dict)#Make a empty dict collections (nested disctionnaries)
dP2 = collections.defaultdict(dict)

#Make list with lines of hyliteSNP file
with open(hyliteSNP,"r") as f:#opens file with name of "test.txt"
    for line in f:
        myList.append(line.strip('\n'))

#Make nested dictionnary of dictionnaries with {'gene': {'position': 'allele'}}. One for each diploid parent
doubleList = []
for i in range(0, len(myList)):
    line = myList[i]
    listedLine = line.split('\t')
    #For the moment only fixed parental SNP. FIND BETTER CONDITIONS!!!
    if listedLine[5] == "1,1" and listedLine[6] == "0,0":
        #Test for transcripts with no reference SNP
        #CARFULL EXEMPLE:
        #comp34838_c0_seq1	149	G	C	1,0,0	0,0	0,0
        #comp34838_c0_seq1	149	G	T	1,0,0	1,1	0,0
        if i > 1 and listedLine[1] == myList[i-1].split('\t')[1] and (myList[i-1].split('\t')[5] == myList[i].split('\t')[6] and myList[i-1].split('\t')[6] == myList[i].split('\t')[5]):
            doubleList.append(listedLine)
            #dP1[str(listedLine[0])][str(listedLine[1])] = str(listedLine[3]) # CHECK IF THE REFERENCE SNP IS PRESENT IN BOTH PARENTS
            #dP2[str(listedLine[0])][str(listedLine[1])] = str(myList[i-1].split('\t')[3])
            del dP1[str(listedLine[0])]
            del dP2[str(listedLine[0])]
            
        else:# These are the SNP where there is a fixed mutation in one parent and the ansestral SNP is fixed in the other parent
            dP1[str(listedLine[0])][str(listedLine[1])] = str(listedLine[3]) # SNP chr=comp72; pos=677
            dP2[str(listedLine[0])][str(listedLine[1])] = str(listedLine[2])

        
    elif listedLine[5] == "0,0" and listedLine[6] == "1,1":
        #Test for transcripts with no reference SNP
        if i > 1 and listedLine[1] == myList[i-1].split('\t')[1] and (myList[i-1].split('\t')[5] == myList[i].split('\t')[6] and myList[i-1].split('\t')[6] == myList[i].split('\t')[5]):
            doubleList.append(listedLine)
            #dP1[str(listedLine[0])][str(listedLine[1])] = str(myList[i-1].split('\t')[3])
            #dP2[str(listedLine[0])][str(listedLine[1])] = str(listedLine[3])
            del dP1[str(listedLine[0])]
            del dP2[str(listedLine[0])]
                    
        else:
            dP1[str(listedLine[0])][str(listedLine[1])] = str(listedLine[2])
            dP2[str(listedLine[0])][str(listedLine[1])] = str(listedLine[3])
            
pprint(doubleList)
print(len(doubleList))
# FASTER: CREATE A LESS COMPACTED LIST OF CONDITIONS. DON'T FORGET TO REMOVE THE LAST OR AT THE END OF OUTPUT FILES
#with open(str(outputName) + ".P1.conditions.simple.txt", "w") as outfile:
#    for chromosome in dP1:
#        for position in dP1[chromosome]:
#            outfile.write("(chr("+str(chromosome)+") & nt_exact("+str(position)+", "+str(dP1[chromosome][position]+")) | \n"))

#with open(str(outputName) + ".P2.conditions.simple.txt", "w") as outfile:
#    for chromosome in dP2:
#        for position in dP2[chromosome]:
#            outfile.write("(chr("+str(chromosome)+") & nt_exact("+str(position)+", "+str(dP2[chromosome][position]+")) | \n"))

# SLOWER: CREATE A COMPACTED LIST OF CONDITIONS. DON'T FORGET TO REMOVE THE LAST OR AT THE END OF OUTPUT FILES
with open(str(outputName) + ".P1.conditions.listed.txt", "w") as outfile:
    for chromosome in dP1:
#        #outfile.write("(chr("+str(chromosome)+") & ")
        line = "(chr("+str(chromosome)+") & ("
        for position in dP1[chromosome]:
#            #outfile.write("nt_exact("+str(position)+", "+str(dP1[chromosome][position]+") | "))
            line = line + "nt_exact("+str(position)+", "+str(dP1[chromosome][position])+") | "
        line = line.strip(" | ")
        line = line + ")) | \n"
        outfile.write(line)

with open(str(outputName) + ".P2.conditions.listed.txt", "w") as outfile:
    for chromosome in dP2:
#        #outfile.write("(chr("+str(chromosome)+") & ")
        line = "(chr("+str(chromosome)+") & ("
        for position in dP1[chromosome]:
#            #outfile.write("nt_exact("+str(position)+", "+str(dP1[chromosome][position]+") | "))
            line = line + "nt_exact("+str(position)+", "+str(dP2[chromosome][position])+") | "
        line = line.strip(" | ")
        line = line + ")) | \n"
        outfile.write(line)
