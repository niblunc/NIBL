#!/usr/bin/env
# -*- coding: utf-8 -*-
"""
Created on Thu May 31 20:38:28 2018

@author: nikkibytes, extending from original by Dr. Grace Shearrer
"""
from multiprocessing import Pool
import glob
import argparse
import os
import subprocess
import datetime
import shutil








# The write_files() method sets the file paths for output files

def output_files():
    global datestamp
    global outhtml
    global out_bad_bold_list
    global outfile

    datestamp=datetime.datetime.now().strftime("%Y-%m-%d-%H_%M_%S")

    if arglist["SES"] == False:
        outhtml = os.path.join(derivatives_dir,'bold_motion_QA_%s.html'%(datestamp))
        out_bad_bold_list = os.path.join(derivatives_dir,'TEST_%s.txt'%(datestamp))
    else:
        outhtml = os.path.join(derivatives_dir,'%s_bold_motion_QA_%s.html'%(arglist["SES"],datestamp))
        out_bad_bold_list = os.path.join(derivatives_dir,'%s_TEST_%s.txt'%(arglist["SES"], datestamp))
    if arglist["MOCO"] != False:
        outfile = open(outhtml, 'a')


###########################################

def set_parser():
    global parser
    global arglist
    global args
    parser=argparse.ArgumentParser(description='preprocessing')
    #parser.add_argument('-task',dest='TASK', default=False, help='which task are we running on?')
    parser.add_argument('-moco',dest='MOCO',
                        action="store_true", help='this is using fsl_motion_outliers to preform motion correction and generate a confounds.txt as well as DVARS')
    parser.add_argument('-bet',dest='STRIP',action='store_true',
                        default=False, help='bet via fsl using defaults for functional images')
    parser.add_argument('-mderiv',dest='MAKEDIR',
                        default=False, help='enter directory where you want to make the derivatives/ directory,')
    parser.add_argument('-fpath',dest='FPREP',
                        default=False, help="enter the directory path where the fmriprep subjects are held.")
    parser.add_argument('-derivpath',dest='DERIV',
                        default=False, help="enter the derivatives directory path")
    parser.add_argument('-indir',dest='INDIR',
                        default=False, help="enter the input directory path where the subject ids,  'sub-*', are held(may be the same as fmriprep/derivatives/etc)" )
    parser.add_argument('-ses',dest='SES',
                        default=False, help='have multiple sessions use flag?')
    parser.add_argument('-bet_thresh',dest='BET_THRESH',
                        default=False, help='fractional intensity threshold (0->1)')


    args = parser.parse_args()
    arglist={}
    for a in args._get_kwargs():
        arglist[a[0]]=a[1]

############################################

def skull_strip(sub):
    print(">>>>----------------> starting bet on ", sub )
    try:
        for nifti in glob.glob(os.path.join(func_input_path, '*bold_space-MNI152NLin2009cAsym_preproc.nii*')):
            # make our variables
            filename = nifti.split("/")[-1].split(".")[0]
            print("FILENAME ", filename)
            bet_name=filename+'_brain'
            # check if data exists already
            bet_output = os.path.join(func_output_path, bet_name)
            if os.path.exists(bet_output + '.nii'):
                print(bet_output + ' exists, skipping \n')
            else:
                print("Running bet on ", nifti)
                bet_cmd=("bet %s %s -F -m -f %s"%(nifti, bet_output, arglist["BET_THRESH"]))
                print(">>>-----> BET COMMAND:", bet_cmd)
                shutil.copy(nifti, func_output_path)
                os.system(bet_cmd)
    # If cannot find file move on
    except FileNotFoundError:
        print("BAD FILE PASSING")
        outfile = os.path.join(derivatives_dir, 'empty_subjects_betstrip.txt')
        with open(outfile, 'a') as f:
            f.write("Empty: %s \n "%(sub))
        f.close()

def fd_check(sub):
    print("---------> Starting motion correction on ", sub)
    try:
# iterate over nifti file
        for nifti in glob.glob(os.path.join(func_output_path, '*brain.nii.gz')):
            filename=nifti.split('.')[0]
            newfilename = filename.split("/")[-1].replace("_bold_space-MNI152NLin2009cAsym_preproc_brain", " ")

            

            #### PUT IN CORRECT FILENAME IDENTIFIER HERE!!!
            
               
            print("RUN ID >>>>>>>>>--------> ", run_id)
            # set comparison param
            nvols_cmd="fslnvols " + nifti
            volume = subprocess.check_output(nvols_cmd, shell=True, encoding="utf-8")
            volume = volume.strip()
            comparator = int(volume) *.25
            ## RUN 'fsl_motion_outliers' TO RETRIEVE MOTION CORRECTION ANALYSIS
            outlier_cmd = "fsl_motion_outliers -i %s  -o %s/%s_confound.txt  --fd --thresh=0.9 -p %s/%s_fd_plot -v > %s/%s_outlier_output.txt"%(filename, motion_assessment_path, newfilename, motion_assessment_path,newfilename, motion_assessment_path, newfilename)
            print(">>>>>>>>>-------->  RUNNING FSL MOTION OUTLIERS ")
            print("COMMAND NVOLS: ", nvols_cmd)
            print("OUTLIER CMD: ", outlier_cmd)
            os.system(outlier_cmd)
        ## EXAMINE OUTLIER FILE AND GRAB RELEVANT DATA 
            outlier_file="%s/%s_outlier_output.txt"%(motion_assessment_path, newfilename)
            with open(outlier_file, 'r') as f:
                lines=f.readlines()
                statsA = lines[1].strip("\n") #maskmean
                statsB = lines[3].strip("\n") #metric range
                statsC = lines[4].strip("\n") #outliers found
                if int(statsC.split(" ")[1])  > 0:
                    statsD = lines[6].strip("\n") #spikes found
                else:
                    statsD = "\n"
            f.close()
        ## GRAB MOTION CORRECTION PLOT AND WRITE PLOT & INFO TO HTML
            plotz=os.path.join(motion_assessment_path, run_id+'_fd_plot.png')
            FILEINFO="""<p><font size=7> <b>{CURR_FILENAME} </b></font><br>"""
            CURR_FILEINFO = FILEINFO.format(CURR_FILENAME=file)
            outfile.write(CURR_FILEINFO)
            INFO="""<p><font size=6>{A} <br><b>{B}<b><br>{C}<br><b>{D}</b><br><br>"""
            CURR_INFO= INFO.format(A=statsA, B=statsB, C=statsC, D=statsD)
            outfile.write(CURR_INFO)
            PLOT="""<IMG SRC=\"{PLOTPATH}\" WIDTH=100%><br><br>"""
            CURR_PLOT = PLOT.format(PLOTPATH=plotz)
            outfile.write(CURR_PLOT)
            print(">>>>>>>>>--------> COPYING OUTPUT TO HTML")
            print(">>>>>>>>>--------> ADDING PLOT TO HTML")
                ## ADD FILE FOR GOOD SUBJECT 
        # --sometimes you have a great subject who didn't move
            if os.path.isfile("%s/%s_confound.txt"%(motion_assessment_path, file))==False:
                os.system("touch %s/%s_confound.txt"%(motion_assessment_path, file))
        ## CHECK FOR BAD SUBJECTS: ABOVE OUR THRESHOLD
        # how many columns are there = how many 'bad' points
            check = subprocess.check_output("grep -o 1 %s/%s_confound.txt | wc -l"%(motion_assessment_path, file), shell=True)
            num_scrub = [int(s) for s in check.split() if s.isdigit()]
            print("NUM SCRUB: ", str(num_scrub[0]), "\n")
            if num_scrub[0] > comparator: #if the number in check is greater than num_scrub then we don't want it
                with open(out_bad_bold_list, "a") as myfile: #making a file that lists all the bad ones
                    myfile.write("%s/%s\n"%(derivatives_dir, file))
                    print("wrote bad file")
                myfile.close()
    except FileNotFoundError:   
        print("FILE IS EMPTY, PASSING")

#
def check_output_directories(sub):
    # check for motion_assesment directory

    if not os.path.exists(os.path.join(derivatives_dir, sub)):
        os.makedirs(os.path.join(derivatives_dir, sub))

    if arglist["SES"] != False:
        if not os.path.exists(os.path.join(derivatives_dir, sub, arglist["SES"])):
            os.makedirs(os.path.join(derivatives_dir, sub, arglist["SES"]))

    if not os.path.exists(os.path.join(anat_output_path)):
        os.makedirs(os.path.join(anat_output_path))
    if not os.path.exists(os.path.join(func_output_path)):
        os.makedirs(os.path.join(func_output_path))
    if not os.path.exists(os.path.join(func_output_path,'motion_assessment')):
        os.makedirs(os.path.join(func_output_path,  'motion_assessment'))
    if not os.path.exists(os.path.join(func_output_path,'Analysis')):
        os.makedirs(os.path.join(func_output_path,  'Analysis'))





def set_paths(sub):
    global func_output_path
    global anat_output_path
    global func_input_path
    global motion_assessment_path

    if arglist["SES"] == False:
        out_dir = os.path.join(DERIV_PATH, sub)
        func_input_path=os.path.join(FRPEP_PATH, sub, "func")
    else:
        out_dir = os.path.join(DERIV_PATH, sub, arglist["SES"])
        func_input_path=os.path.join(FPREP_PATH,sub,arglist["SES"],"func")
        
    anat_output_path=os.path.join(out_dir, 'anat')
    func_output_path=os.path.join(out_dir,'func')
    motion_assessment_path=os.path.join(out_dir,'func','motion_assessment')
    print("NEW PATH: %s \n %s \n %s "%(anat_output_path, func_output_path, motion_assessment_path))
def start_process(subjects):
    for sub in sorted(subjects):
        set_paths(sub)
        #if args.STRIP == True:
           # skull_strip(sub)
        #if args.MOCO == True:
           # fd_check(sub)

def split_list(a_list):
    half = int(len(a_list)/2)
    return a_list[:half], a_list[half:]

def main():
    global FPREP_PATH
    global DERIV_PATH
    global subjects
    
    
    subjects = [] 
    FPREP_PATH = arglist["FPREP"]
    set_parser() 
# Set paths 
# if '-mderiv' is false, means they have derivatives directory 
    if arglist["MAKEDIR"] == False:
        print("We have a deriv directory")
        DERIV_PATH = arglist["DERIV"]
#  
    else:
        print("We are making a deriv directory")
        BASE_PATH = arglist["MAKEDIR"]
        # MAKE DERIV PATH
        # HERE
        DERIV_PATH = os.path.join(BASE_PATH, "derivatives")
        if not os.path.exists(DERIV_PATH):
            os.makedirs(DERIV_PATH)
        
        
    output_files()

# Get Subjects
    SUB_DIR = glob.glob(os.path.join(arglist["INDIR"], "sub-*")
    for path in SUB_DIR:
        sub = path.split("/")[-1]
        subjects.append(sub)



    B, C = split_list(subjects)
    pool = Pool(processes=2)
    pool.map(start_process, [B,C])

                         
# Start Program
if __name__ == "__main__":
    main()
