# Brain Imaging Data Structure (BIDS) Conversion  
  
Here we are going to describe the process of converting raw dicom files into the BIDS format for further analysis. For NIBL we utilize Singularity containers to run the processes on the high performance computing cluster(HPCC). Below you will find more details on the process and references to specific files found within this folder to use as a template. 


## Getting Started  

To get the data into BIDS format there is series of simples steps to follow to set up our data for conversion.  
```
I.      Rename Data folders
II.     Modify Heuristic File
III.    Setup batch script & run 
IV.     Modify post-BIDS data 
V.      Validate BIDS data
```


### What is Singularity?  
For our processes the Singularity container has already been built and we will use this to run our conversion. Creating a Singularity container may be beyond the scope of this topic, however we will provide documentation for those interested, understanding what it is may come in use if you ever need to modify or create your own container. Singularity containers can be used to pacakge scientific workflows, software and libraries and even data, and more importantly they support use on the HPCC. The key here is to know that with the Singularity container we are able to package the `heudiconv` software and use it for our BIDS conversion. We are able to use the container commands that allow us to run the software easily and with ease that feels similar to running software on a terminal. For our purposes we have utilized the `shell` and `exec` command, which will be discussed in further detail.   
  
  
## BIDS Conversion Workflow 
*this workflow assumes you already have your data on RENCI   
  
  
### Rename Directories  
One of the specifications of BIDS is the naming scheme. While this can be meticulous it allows for a standardized format that can be understood. To avoid complex programming down the line I found it was easiest to name our directories into the BIDS format before our conversion. BIDS expects to find, `sub-XXX`, where `XXX` can be any identifier. In many cases this is straight forward, however every dataset is different and there can be nuances that make it difficult to make an all encompassing script for renaming. However the script [Rename_Folders.ipynb](https://github.com/niblunc/NIBL/blob/master/TheBrainPipeline/Brain_Imaging_Data_Structure/Rename_Folders.ipynb) is flexible enough and should be able to guide you through renaming your directories!  
  
  
### Setting up the Heuristic File  
A great explanation is found here: [Using Heudiconv](http://nipy.org/heudiconv/#21)  
BIDS has very specific naming structures, a summarized document is currently being created to help the team but for now please reference the specs documentation: [BIDS Specs](https://bids.neuroimaging.io/bids_spec.pdf)   
To get the values we need to fill out the heuristic file we can run a "dry pass" on our subjects and look at the `dicominfo.tsv` file. You can run this manually and look at the file yourself or you can run the scripts from the terminal and see the output. *For now* the script will drypass all the input subjects given and then you can run the second script to view a specific subject. Often times it is best to have all the subjects because there are cases the values vary, this is rare, but it has occured and you can reference the individuals files if needed.  
The scripts are found here [Heudiconv_DryPass](https://github.com/niblunc/NIBL/tree/master/TheBrainPipeline/Brain_Imaging_Data_Structure/Heudiconv_Drypass) but you can also find them already on RENCI, no modification is needed, just follow the workflow below.  
The two step process:  
I. Run the `get_dicominfo.py` script, this requires 3 inputs:  
    A. The input directory that holds the subjects (right now the script runs on all found subjects, will be modified to select desired subjects only)   
    B. The output directory (where you want the hidden .heudiconv folder to be held)  
    C. The dicom extension to be found, either IMA or dcm (will be modified to automatically find)   
II. Run the `read_tsv.py` script, requires 2 inputs:   
    A. The input directory, which is the same as the output directory given above.  
    B. The subject you'd like to view  
    
```
# change to the directory
cd /projects/niblab/bids_projects/Heudiconv_drypass

# run the get_dicominfo.py script
python get_dicominfo.py -in /projects/niblab/bids_projects/raw_data/continuing_studies/BBx/ses-1/test 
-out /projects/niblab/bids_projects/raw_data/continuing_studies/BBx/ses-1/test -ext dcm

# run the read_tsv.py script 
python read_tsv.py -subj sub-031 -in 
/projects/niblab/bids_projects/raw_data/continuing_studies/BBx/ses-1/test

```  

Once you get your values you can use them to fill in the heuristic file!  
For an example heuristic file reference here: [Heuristic Example](https://github.com/niblunc/NIBL/blob/master/TheBrainPipeline/Brain_Imaging_Data_Structure/heuristic_example.py)  
Then you can modify the template we have here: [Heuristic File template](https://github.com/niblunc/NIBL/blob/master/TheBrainPipeline/Brain_Imaging_Data_Structure/heuristic_template.py)    




### Run the GUI  
Now that the the heuristic file is setup and the subjects have been renamed we can run the bids conversion process. One way we do this is to run the GUI. You can find that here, `/projects/niblab/bids_projects/BIDS_GUI` , in RENCI.  

The GUI has a few assumptions:
- The subject folders are labeled with the prefix `sub-`, if you need to do this reference: [Rename_Folders.ipynb](https://github.com/niblunc/NIBL/blob/master/TheBrainPipeline/Brain_Imaging_Data_Structure/Rename_Folders.ipynb)  
- The GUI assumes the dicoms are listed directly after the subject folders, therefore it assumes the structure is: /my/directory/path/is/maindir/sub-XXX/*dcm  
- Currently the GUI grabs all subject folders found from the given input directory, it then will run a conversion on all the confirmed subjects, future updates will allow the selection of a single, or specific subjects.  

The Current Inputs:  
- Input Directory: the directory where the subject folders are held
- Output Directory: where you want your BIDS data to be held
- Heuristic File: the already made heuristic file  
- Dicom Extension: the dicom extension dcm or IMA  
- Multiple sessions: yes or no  
- Session: enter the session id IF multiple sessions is yes  

**RUN THE GUI:**
```
# change to the directory
cd /projects/niblab/bids_projects/BIDS_GUI

# start the GUI 
python gui.py 
```  
  
When you press "CONVERT" the terminal will output that a batch job has been submitted, please use `squeue -u YOUR_USERNAME` to see the process, the is titled `BIDS_Conversion`    
``` 
# when you have pressed convert you can close the GUI then type the following, replacing 'nbytes' with your username
squeue -u nbytes
```   
  
The GUI will be updated to:  
- Identify "dcm" or "IMA" without input
- Will allow you to select specific subjects
- Will improve output windows when selecting inputs and running conversion




### Run manually through terminal 
Reference here to run heudiconv manually through terminal or test [Heudiconv Container](https://github.com/niblunc/NIBL/blob/master/TheBrainPipeline/Brain_Imaging_Data_Structure/README_heudiconv.md)  
Reference here for the batch script example and template: [Batch Example](https://github.com/niblunc/NIBL/blob/master/TheBrainPipeline/Brain_Imaging_Data_Structure/batch_example.job) [Batch Template](https://github.com/niblunc/NIBL/blob/master/TheBrainPipeline/Brain_Imaging_Data_Structure/batch_template.job)
  
  
### Cleaning up the BIDS directory
Reference here for the BIDS specs: [BIDS](https://bids.neuroimaging.io/bids_spec.pdf)  
Reference here for script to "clean up" the BIDS directorty post conversion: [BIDS clean up](https://github.com/niblunc/NIBL/blob/master/TheBrainPipeline/Brain_Imaging_Data_Structure/CleaningBIDS.ipynb)  
Single Session Directory Example: 
```
● sub-001/
  ○ anat/
    ■ sub-001_T1w.nii.gz
    ■ sub-001_T1w.json
  ○ func/ 
    ■ sub-001_task-A_bold.nii.gz 
    ■ sub-001_task-A_bold.json
    ■ sub-001_task-A_events.tsv
    ■ sub-001_task-A_physio.tsv.gz
    ■ sub-001_task-A_physio.json
  ○ fmap/
    ■ sub-001_phasediff.nii.gz
    ■ sub-001_phasediff.json
    ■ sub-001_magnitude1.nii.gz
  ○ sub-001_scans.tsv
● code
  ○ deface.py
● derivatives 
  ○ README
● participants.tsv
● dataset_description.json
● README
● CHANGES
```  
### Validate BIDS
Reference here for validating BIDS: [BIDS validator](https://github.com/niblunc/NIBL/blob/master/TheBrainPipeline/Brain_Imaging_Data_Structure/README_BIDS_validator.md)