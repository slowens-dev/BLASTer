#!/usr/bin/python3.7
import warnings
warnings.simplefilter('ignore')
from Bio.Blast import NCBIWWW,NCBIXML
from Bio import SearchIO

def fastaFileBlast(filepath):

    fasta = open(filepath).read()#get fasta from the file
    resultHandle = NCBIWWW.qblast('blastn','nr',fasta,hitlist_size = 20)#get the results

    with open('blastData.xml', 'w') as writer:
        writer.write(resultHandle.read()) #writes to the file and empties resultHandle
    resultHandle.close()

    
    resultHandle = open('blastData.xml')#reloads resultHandle
    
    blastRecords = NCBIXML.parse(resultHandle)#get the blast records in Record form
    blastRecords = list(blastRecords)
    print(len(blastRecords[0].alignments))
    for record in blastRecords:
        for align in record.alignments:
            for hsp in align.hsps:
                   print('*****ALIGNMENT***** ', '\nsequence: ', align.title[:100],'\nlength: ', align.length, '\nE Value: ', hsp.expect,'\n',hsp.query[0:100],'\n', hsp.match[0:100],'\n',hsp.sbjct[0:100])

    blastQR = SearchIO.read('blastData.xml', 'blast-xml')#blast QueryResult object
    print(blastQR)


#MAIN
fastaFileBlast('HBA1.fasta')
    
    
    
    
