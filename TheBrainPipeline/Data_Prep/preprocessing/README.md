# Preprocessing Scripts  

### Workflow:  
The current workflow is below:   
* Setting up derivatives directory 
* Skull stripping functionals (running -bet) 
* Motion correction (FD Check)
* Collecting motion parameters 
* Collecting onsets   
  
  
#### Note:
* this workflow and the scripts are subject to change, and are made to be as flexible and essential as possible.  
* these scripts assume you have fmriprep data and follow the `derivatives`/ directory setup  

### Directory template ~/derivatives/ 
Here is the ~/derivatives/ directory that we set up for our essential data. 
```
    ~/derivatives/
        code/
            heuristic_file.py
        design_files/
            design1.fsf
            design2.fsf
            design3.fsf
        group_ana/
            cope.fsf/
            cope_XX.gfeat/
        quality_ana/
        README.md
        sub-XX/
            anat/
                highres.nii.gz
            func/
                sub-XX_*_brain_mask.nii.gz
                sub-XX_*_preproc_brain.nii.gz
                sub-XX_*_preproc.nii.gz
                .
                .
                .
                onsets/
                    sub-XX_task-sweet_run-1.txt
                    sub-XX_task-sweet_run-2.txt
                    sub-XX_task-sweet_run-3.txt
                    sub-XX_task-sweet_run-4.txt
                    .
                    .
                    .
                motion_assessment/
                    sub-XX_*_preproc_brain_confound.txt
                    sub-XX_*_preproc_brain_outlier_output.txt
                    .
                    .
                    .
                Analysis/
                    feat1/
                        sub-XX_design_file_*.fsf
                        task-*_run1.feat/
                        task-*_run2.feat/
                        task-*_run3.feat/
                        task-*_run4.feat/
                    feat2/
                        sub-XX_design_file_*.fsf
                        sub-XX.gfeat/

                
```