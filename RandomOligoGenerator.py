# written Nicholas A DeLateur in Weiss Lab, MIT; delateur@mit.edu
# Version 1.0
# Run using PyCharm Community Edition 2016.1.3 with Anaconda3 on Windows 10
# Generates and writes M N-length DNA sequences satisfying user parameters to an excel file.
# Does so by generating a random sequence and then checking if it meets paramaters

import xlsxwriter
import datetime
import random
import re

def RC_DNA(sequence):
    # Taken from https://gist.github.com/crazyhottommy/7255638#file-reverse_complement-py
    seq_dict = {'A':'T','T':'A','G':'C','C':'G'}
    return "".join([seq_dict[base] for base in reversed(sequence)])

def checkGCcontent(min, max, sequence):
    ATcount=0
    GCcount=0
    for i in sequence:
        if i == 'A' or i == 'T':
            ATcount+=1
        else:
            GCcount+=1
    GCpercent = int(round((100* GCcount / (GCcount + ATcount))))
    if GCpercent >= min and GCpercent <= max:
        return True
    else:
        return False

def checkHomopolymers(max, sequence):
    highestHomoLength = 0 #this function only returns the highest homopolymer length found
    for i in range(0,len(sequence)):
        homolength = 1
        j = 1
        stillHomo = True
        while stillHomo == True:

            if i+j>=len(sequence): #have we reached the end of the sequence? Python gets very grumpy if you check for something not there
                break #we've reached the end

            if sequence[i] == sequence[i+j]: #if the next nucleotide is the same as the current
                homolength+=1
                j+=1 #check one more down

            else:
                stillHomo = False
                if homolength > highestHomoLength: #if this was a record length, replace it as the highest
                    highestHomoLength = homolength
    if highestHomoLength > max:
        return False
    else:
        return True

def checkForbiddenSites(list,sequence):
    forbiddenSiteFlag = True

    for i in range(0,len(list)):
        forbiddenSites = re.compile(list[i])
        forbiddenSiteFoundList = forbiddenSites.findall(sequence)

        if forbiddenSiteFoundList == []:
            pass
        else:
            forbiddenSiteFlag = False

    return forbiddenSiteFlag

def generateRandomSequence(NumNucleotides):
    generatedSequence = '' # empty sequence
    for i in range(NumNucleotides):
        dieRoll = random.randrange(4)
        if dieRoll == 0:
            generatedNucleotide = 'A'
        elif dieRoll == 1:
            generatedNucleotide = 'C'
        elif dieRoll == 2:
            generatedNucleotide = 'G'
        else:
            generatedNucleotide = 'T'
        generatedSequence+=generatedNucleotide
    return generatedSequence

####################################### USER PARAMATERS HERE
N = 61 # Length in nucleotides
M = 1 # Amount of sequences to generate
GCmin = 40 # minimum percentage GC content
GCmax = 60 # maximum percentage GC content
maxHomoPolymerLength = 6 # maximum amount a nucleotide may be repeated in a row
forbiddenSites = ['GAAGAC', 'GGTCTC','CACCTCGC']
####################################### USER PARAMATERS HERE

for i in range(0, len(forbiddenSites)):
    forbiddenSites.append(RC_DNA(forbiddenSites[i]))

#sanity checks
if N >= 10000 or N <= 1:
    print('Please choose a better N')
    exit(0)
if M >= 10000 or M < 1:
    print('Please choose a better M')
    exit(0)
if GCmin >= GCmax:
    print('Please make your GCmin less than your GCmax')
    exit(0)
if GCmin <= 0:
    print('Please make your GCmin >= 0')
    exit(0)
if GCmax >= 100:
    print('Please make your GCmax <= 100')
    exit(0)
if maxHomoPolymerLength < 1:
    print('Please make your maxHomoPolymerLength >= 1')
    exit(0)

random.seed(0) # known random seed
succesfullyFound = 0 # successfully found sequences
attempts=0 # sanity counter

# Generate and write acceptable sequences
GeneratedSequences = []

while succesfullyFound < M:
    attempts+=1 # sanity counter

    approvedForGCcontent = False
    approvedForHomopolymers = False
    approvedForForbiddenSites = False

    candidateSequence = generateRandomSequence(N)

    approvedForGCcontent = checkGCcontent(GCmin, GCmax, candidateSequence)
    approvedForHomopolymers = checkHomopolymers(maxHomoPolymerLength, candidateSequence)
    approvedForForbiddenSites = checkForbiddenSites(forbiddenSites, candidateSequence)

    if approvedForGCcontent == True and approvedForHomopolymers == True and approvedForForbiddenSites == True:
        print(str(candidateSequence)) #optional but useful
        GeneratedSequences.append(candidateSequence)
        succesfullyFound += 1

    if attempts > 100000: # sanity check failed
        print("something went TERRIBLY wrong I'm so sorry!")
        succesfullyFound=M

# Create an new Excel file and add a worksheet.
# WARNING doesn't check if the filename already exists.
# Shouldn't be a problem if you don't run the program within seconds of itself
filename = 'RandomNucleotides' + datetime.datetime.now().strftime("%y%m%d%H%M%S") + '.xlsx'
workbook1 = xlsxwriter.Workbook(filename)
worksheet1 = workbook1.add_worksheet()

worksheet1.write(0, 0, 'Sequence')
for i in range(0,M):
    worksheet1.write(i+1, 0, GeneratedSequences[i])

# MANDATORY close the workbook
workbook1.close()





