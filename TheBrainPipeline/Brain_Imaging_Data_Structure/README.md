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
For an example heuristic file reference here: [Heuristic Example](https://github.com/niblunc/NIBL/blob/master/TheBrainPipeline/Brain_Imaging_Data_Structure/heuristic_example.py)  
Then you can modify the template we have here: [Heuristic File template](https://github.com/niblunc/NIBL/blob/master/TheBrainPipeline/Brain_Imaging_Data_Structure/heuristic_template.py)    


### Run the GUI  
Now that the the heuristic file is setup and the subjects have been renamed we can run the bids conversion process. One way we do this is to run the GUI. You can find that here, `/projects/niblab/bids_projects/BIDS_GUI` , in RENCI.  
```
# change to the directory
cd /projects/niblab/bids_projects/BIDS_GUI
# start the GUI 
python BIDS_GUI.py 
```  
  
When you press "CONVERT" the terminal will output that a batch job has been submitted, please use `squeue -u YOUR_USERNAME` to see the process, the is titled `BIDS_Conversion`    
``` 
# when you have pressed convert you can close the GUI then type the following, replacing 'nbytes' with your username
squeue -u nbytes
```  

The GUI has a few assumptions:
- The subject folders are labeled with the prefix `sub-`, if you need to do this reference: [Rename_Folders.ipynb](ADD_LINK_HERE)  
- The GUI assumes the dicoms are listed directly after the subject folders, therefore it assumes the structure is: /my/directory/path/is/maindir/sub-XXX/*dcm  
- Currently the GUI grabs all subject folders found from the given input directory, it then will run a conversion on all the confirmed subjects, future updates will allow the selection of a single, or specific subjects.  
 
### Setup batch script & run 
Here we are going to go over the batch script and setting it up.  
Reference the batch script here for reference: [Batch script](ADD_LINK_HERE)  
  
  
### Cleaning up the BIDS directory
Reference here for the BIDS specs: [BIDS](https://bids.neuroimaging.io/bids_spec.pdf)  
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

