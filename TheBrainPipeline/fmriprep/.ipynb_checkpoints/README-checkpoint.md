# Running the FMRIPREP container
Image: fmriprep.simg

This container allows us to open up an environment to run fmriprep.  
  
The `fmriprep` workflow takes as principal input the path of the dataset that is to be processed. The input dataset it required to be in valid BIDS format, must include at least one T1w structural image, and a BOLD series(this can be disabled with a flag). 

[Reference the docs](https://fmriprep.readthedocs.io/en/stable/usage.html)
### Command Template: <br>
fmriprep command: 
```
fmriprep [-h] [--version] [--skip_bids_validation]
                [--participant_label PARTICIPANT_LABEL [PARTICIPANT_LABEL ...]]
                [-t TASK_ID] [--echo-idx ECHO_IDX] [--nthreads NTHREADS]
                [--omp-nthreads OMP_NTHREADS] [--mem_mb MEM_MB] [--low-mem]
                [--use-plugin USE_PLUGIN] [--anat-only] [--boilerplate]
                [--ignore-aroma-denoising-errors] [-v] [--debug]
                [--ignore {fieldmaps,slicetiming,sbref} [{fieldmaps,slicetiming,sbref} ...]]
                [--longitudinal] [--t2s-coreg] [--bold2t1w-dof {6,9,12}]
                [--output-space {T1w,template,fsnative,fsaverage,fsaverage6,fsaverage5} [{T1w,template,fsnative,fsaverage,fsaverage6,fsaverage5} ...]]
                [--force-bbr] [--force-no-bbr]
                [--template {MNI152NLin2009cAsym}]
                [--output-grid-reference OUTPUT_GRID_REFERENCE]
                [--template-resampling-grid TEMPLATE_RESAMPLING_GRID]
                [--medial-surface-nan] [--use-aroma]
                [--aroma-melodic-dimensionality AROMA_MELODIC_DIMENSIONALITY]
                [--skull-strip-template {OASIS,NKI}]
                [--skull-strip-fixed-seed] [--fmap-bspline] [--fmap-no-demean]
                [--use-syn-sdc] [--force-syn] [--fs-license-file PATH]
                [--no-submm-recon] [--cifti-output | --fs-no-reconall]
                [-w WORK_DIR] [--resource-monitor] [--reports-only]
                [--run-uuid RUN_UUID] [--write-graph] [--stop-on-first-crash]
                [--notrack] [--sloppy]
                bids_dir output_dir {participant}
```
Common fmriprep command for NIBL:
```
fmriprep [input directory] [output directory] \
    participant  \
    --participant-label [participant label]  \
    --fs-license-file /home_dir/freesurfer/license.txt \
    --fs-no-reconall \
    --omp-nthreads 16 --n_cpus 16 \
    --ignore slicetiming  \
    --bold2t1w-dof 12 \
    --output-space template --template MNI152NLin2009cAsym \
    --debug \
    --resource-monitor --write-graph --stop-on-first-crash 
```

### Examples

Opening fmriprep:
```
# with the shell
singularity shell -B /projects/niblab/bids_projects:/home_dir /projects/niblab/bids_projects/Singularity_Containers/fmriprep.simg  

# with exec
singularity exec -B /projects/niblab/bids_projects:/home_dir /projects/niblab/bids_projects/Singularity_Containers/fmriprep.simg \
fmriprep [input directory] [output directory] \
    participant  \
    --participant-label [participant label]  \
    --fs-license-file /home_dir/freesurfer/license.txt \
    --fs-no-reconall \
    --omp-nthreads 16 --n_cpus 16 \
    --ignore slicetiming  \
    --bold2t1w-dof 12 \
    --output-space template --template MNI152NLin2009cAsym \
    --debug \
    --resource-monitor --write-graph --stop-on-first-crash 

```

Running with shell  
```
sinteractive -m 99000
singularity shell -B /projects/niblab/bids_projects:/home_dir /projects/niblab/bids_projects/Singularity_Containers/fmriprep.simg  
cd /home_dir 
fmriprep /home_dir/Experiments/Bevel/Nifti /home_dir/Experiments/Bevel/test/ \
    participant  \
    --participant-label 001 \
    --fs-license-file /home_dir/freesurfer/license.txt \
    --fs-no-reconall \
    --omp-nthreads 16 --n_cpus 16 \
    --ignore slicetiming  \
    --bold2t1w-dof 12 \
    --output-space template --template MNI152NLin2009cAsym \
    --debug \
    --resource-monitor --write-graph --stop-on-first-crash 
```

Running batch processes
[Batch File](https://github.com/niblunc/NIBL/blob/master/TheBrainPipeline/fmriprep/fmriprep_batch.job)
```
# edit batch file
# submit job
sbatch --array=1-10%10 fmriprep_batch.job
```
