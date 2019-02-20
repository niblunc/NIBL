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



#________________________________________________________________________________________
# This method, check_output_directories(sub), checks the ~/derivatives directory
# and will make relevant directories if we need to {anat/, func/, motion_assesment/ Analysis/},
# as an argument it takes the subject ID.
#________________________________________________________________________________________

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





def set_parser():
    global parser
    global arglist
    global args
    parser=argparse.ArgumentParser(description='preprocessing')
    #parser.add_argument('-task',dest='TASK', default=False, help='which task are we running on?')
    parser.add_argument('-fprepdir',dest='FPREP',
                        default=False, help='enter path for fmriprep/ directory')
    parser.add_argument('-moco',dest='MOCO',
                        default=False, help='this is using fsl_motion_outliers to preform motion correction and generate a confounds.txt as well as DVARS, pass in threshold variable, 0.9 is common')
    parser.add_argument('-bet',dest='STRIP',
                        default=False, help='bet via fsl using defaults for functional images, pass in strip variable for fractional intensity')
    parser.add_argument('-ses',dest='SES',
                        default=False, help='have multiple sessions?')
    parser.add_argument('-derivdir',dest='DERIV',
                        default=False, help='enter path for fmriprep/ directory')
    args = parser.parse_args()
    arglist={}
    for a in args._get_kwargs():
        arglist[a[0]]=a[1]


def skull_strip(sub, func_input_path, func_output_path):
    print(">>>>---> starting bet on ", sub )
    try:
        for nifti in glob.glob(os.path.join(func_input_path, '*_preproc.nii*')):
            # make our variables
            filename = nifti.split("/")[-1].split(".")[0]
            bet_name=filename+'_brain'
            # check if data exists already
            bet_output = os.path.join(func_output_path, bet_name)
            if os.path.exists(bet_output + '.nii'):
                print(bet_output + ' exists, skipping \n')
            else:
                print("Running bet on ", nifti)
                bet_cmd=("bet %s %s -F -m -f %s"%(nifti, bet_output, arglist["STRIP"]))
                print(">>>-----> BET COMMAND:", bet_cmd)
                #shutil.copy(nifti, func_output_path)
                os.system(bet_cmd)
    except FileNotFoundError:
        pass 
        #print("BAD FILE PASSING")
        #out_ = os.path.join(derivatives_dir, 'empty_subjects_betstrip.txt')
        #with open(out_, 'a') as f:
         #   f.write("Empty: %s \n "%(sub))
        #f.close()
        
        
        
        

def fd_check(sub, outfile, motion_assessment_path, out_bad_bold_list, derivatives_dir, func_output_path):
    print(">>>>---> Starting motion correction on ", sub)
    try:
# iterate over nifti file
        for nifti in glob.glob(os.path.join(func_output_path, '*_brain.nii.gz')):
            filename=nifti.split('.')[0]
            file = filename.split("/")[-1]
            new_filename = file.split("_bold_")[0]
            outlier_path = "%s/%s_outlier_output.txt"%(motion_assessment_path, file)
            plot_path = "%s/%s_fd_plot"%(motion_assessment_path, file)
            confound_path = "%s/%s_confound.txt"%(motion_assessment_path, file)
            #need to get identifier for tasks and runs --rn for bevel, need to specify for versatility 
            # set comparison param
            nvols_cmd="fslnvols " + nifti
            volume = subprocess.check_output(nvols_cmd, shell=True, encoding="utf-8")
            volume = volume.strip()
            comparator = int(volume) *.25
            ## RUN 'fsl_motion_outliers' TO RETRIEVE MOTION CORRECTION ANALYSIS
            outlier_cmd = "fsl_motion_outliers -i %s  -o %s --fd --thresh=%s -p %s -v > %s"%(filename, confound_path, arglist["MOCO"], plot_path, outlier_path)
            print(">>-->  RUNNING FSL MOTION OUTLIERS ")
            print("COMMAND NVOLS: ", nvols_cmd)
            print("OUTLIER CMD: ", outlier_cmd)
            os.system(outlier_cmd)
        ## EXAMINE OUTLIER FILE AND GRAB RELEVANT DATA 
            with open(outlier_path, 'r') as f:
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
            plotz=plot_path+".png"
            FILEINFO="""<p><font size=6> <b>{CURR_FILENAME} </b></font><br>"""
            CURR_FILEINFO = FILEINFO.format(CURR_FILENAME=file)
            outfile.write(CURR_FILEINFO)
            INFO="""<p><font size=6>{A} <br><b>{B}<b><br>{C}<br><b>{D}</b><br><br>"""
            CURR_INFO= INFO.format(A=statsA, B=statsB, C=statsC, D=statsD)
            outfile.write(CURR_INFO)
            PLOT="""<IMG SRC=\"{PLOTPATH}\" WIDTH=100%><br><br>"""
            CURR_PLOT = PLOT.format(PLOTPATH=plotz)
            outfile.write(CURR_PLOT)
            print(">>>>----> ADDING PLOT TO HTML")
                ## ADD FILE FOR GOOD SUBJECT 
        # --sometimes you have a great subject who didn't move
            if os.path.isfile(confound_path)==False:
                os.system("touch %s"%confound_path)
        ## CHECK FOR BAD SUBJECTS: ABOVE OUR THRESHOLD
        # how many columns are there = how many 'bad' points
            check = subprocess.check_output("grep -o 1 %s | wc -l"%(confound_path), shell=True)
            num_scrub = [int(s) for s in check.split() if s.isdigit()]
            print("NUM SCRUB: ", str(num_scrub[0]), "\n")
            if num_scrub[0] > comparator: #if the number in check is greater than num_scrub then we don't want it
                with open(out_bad_bold_list, "a") as myfile: #making a file that lists all the bad ones
                    myfile.write("%s/%s\n"%(derivatives_dir, file))
                    print("wrote bad file")
                myfile.close()
    except FileNotFoundError:   
        print("FILE IS EMPTY, PASSING")


        
        
        

    
def main(SUB_IDS):
    fmriprep_dir = arglist["FPREP"]
    derivatives_dir = arglist["DERIV"]
    datestamp=datetime.datetime.now().strftime("%Y-%m-%d-%H_%M_%S")

    # Check if it is a multi-sess study for correct path assignment 
    if arglist["SES"] == False:
        outhtml = os.path.join(derivatives_dir,'bold_motion_QA_%s.html'%(datestamp))
        out_bad_bold_list = os.path.join(derivatives_dir,'TEST_%s.txt'%(datestamp))
    else:
        outhtml = os.path.join(derivatives_dir,'%s_bold_motion_QA_%s.html'%(arglist["SES"],datestamp))
        out_bad_bold_list = os.path.join(derivatives_dir,'%s_TEST_%s.txt'%(arglist["SES"], datestamp))
        
    if args.MOCO != False:
        # if motion correction parameter was given, open the HTML
        outfile = open(outhtml, 'a')
        TITLE="""<p><font size=7> <b> Motion Correction Check</b></font><br>"""
        outfile.write("%s"%TITLE)
    for sub in sorted(SUB_IDS):
        if arglist["SES"] == False:
            out_dir = os.path.join(derivatives_dir, sub)
            func_input_path=os.path.join(fmriprep_dir,sub, "func")
        else:
            out_dir = os.path.join(derivatives_dir, sub, arglist["SES"])
            func_input_path=os.path.join(fmriprep,sub,arglist["SES"], "func")
    
        anat_output_path=os.path.join(out_dir, 'anat')
        func_output_path=os.path.join(out_dir,'func')
        motion_assessment_path=os.path.join(out_dir,'func','motion_assessment')
        
        if args.STRIP != False:
            skull_strip(sub, func_input_path, func_output_path)
        if args.MOCO != False:
            fd_check(sub,  outfile, motion_assessment_path, out_bad_bold_list, derivatives_dir, func_output_path)

    outfile.close()

    
    
    

                 
                 




# Start Program
if __name__ == "__main__":
    global subjects
    subjects = []
    set_parser()
    #get subjects
    subs_dir = glob.glob(os.path.join(arglist["DERIV"], "sub-*"))

    for x in subs_dir:
        sub_id = x.split("/")[-1]
        subjects.append(sub_id)
    subjects = sorted(subjects)
    
    half = int(len(subjects)/2)
    B,C = subjects[:half], subjects[half:]
    pool = Pool(processes=2)
    pool.map(main, [B,C])