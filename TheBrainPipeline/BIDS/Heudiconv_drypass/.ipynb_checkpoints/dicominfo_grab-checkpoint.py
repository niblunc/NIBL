# import packages

import glob, os 
import argparse
import subprocess


def set_parser():
    global parser
    global arglist
    global args
    parser=argparse.ArgumentParser(description='bids conversion')
    parser.add_argument('-indir',dest='INDIR',
                        default=False, help='enter directory where the sub-*/ directories are found')
    parser.add_argument('-name',dest='STUDY',
                        default=False, help='enter the study name, must be the same as found in the input path')
    parser.add_argument('-out',dest='OUT',
                        default=False, help='enter directory where you want the output to go')
    parser.add_argument('-multisess',dest='SESS',
                        default=False, help="if multiple session use this param")
    parser.add_argument('-dcmpath',dest='DCMPATH',
                        default=False, help='enter the unique dicom path (as described in docs)')


    args = parser.parse_args()
    arglist={}
    for a in args._get_kwargs():
        arglist[a[0]]=a[1]
        

        
# get parameters         
set_parser() 

# grab dicominfo.tsv file by running heudiconv command --aka "DRY PASS"
studyname = arglist["STUDY"]
dcmpath= "/test"+arglist["DCMPATH"]
outpath = "/test"+arglist["OUT"]
newpath = dcmpath.replace(studyname, "{subject}")

# single session
if arglist["SESS"] == False:
    heudiconv_cmd = "singularity exec -B /:/test /projects/niblab/bids_projects/Singularity_Containers/heudiconv.simg heudiconv -d %s -s %s -f convertall -c none -o %s"%(newpath, studyname, outpath)
# multiple sessions
else:
    session = arglist["SESS"]
    newpath = newpath.replace(session, "{session}")
    heudiconv_cmd = "singularity exec -B /:/test /projects/niblab/bids_projects/Singularity_Containers/heudiconv.simg heudiconv -d %s -s %s -ss %s -f convertall -c none -o %s"%(newpath, studyname, session, outpath)
    
#print(newpath)
print("Running command: ", heudiconv_cmd)
run_batch=subprocess.Popen(["sbatch /projects/niblab/bids_projects/Heudiconv_drypass/drypass.job", heudiconv_cmd])

#dicominfo_tsv = os.path.join("/Users/nikkibytes/Documents/testing/BRO/.heudiconv", studyname, "info", "dicominfo.tsv")
#print(dicominfo_tsv)
#dicominfo_tsv = "dicominfo.tsv"
#import pandas as pd
#dcm_df = pd.read_csv(dicominfo_tsv, sep='\t', header=None)
#refined_dcm_df = dcm_df.iloc[:, 6:13]
#print(refined_dcm_df)