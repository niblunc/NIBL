"""
Author: Nichollette Acosta @ NIBL UNC Chapel Hill

Module for BIDS Conversion GUI
This is a conversion script the GUI uses to run Heudiconv

"""

from __main__ import *

def setSTUDYNAME(x):
    global STUDYNAME
    STUDYNAME = x
def setINPUTDIR(x):
    global INPUTDIR
    INPUTDIR = x
def setOUTPUTDIR(x):
    global OUTPUTDIR
    OUTPUTDIR = x
def setDICOMPATH(x):
    global DICOMPATH
    DICOMPATH = x
def setMULTISESS(x):
    global MULTISESS
    MULTISESS = x
def setHEURISTICFILE(x):
    global HEURISTICFILE
    HEURISTICFILE = x

def runConversion():
    print(">>>>---------------------------> STARTING CONVERSION")
    print(">>>>----------------> HERE ARE MY VARIABLES: \n STUDYNAME:%s \nINPUTDIR:%s \nOUTPUTDIR:%s \nDICOMPATH:%s \
                \nMULTISESS:%s \nHEURISTICFILE:%s "%(STUDYNAME, INPUTDIR, OUTPUTDIR, DICOMPATH, MULTISESS, HEURISTICFILE))
    if MULTISES == False:
        bids_command = "singularity exec -B %s:/test %s heudiconv -b -d %s -s %s -f %s -c dcm2niix -b -o %s/{addsubject}"
    else:
        bids_command = "singularity exec -B %s:/test %s heudiconv -b -d %s -s -ss %s -f %s -c dcm2niix -b -o %s/{addsubject}"


    ##input bash script here

"""
def main():
    runConversion(STUDYNAME)

if __name__ == '__main__':
    main()
"""
