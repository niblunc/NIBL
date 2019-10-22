# Walkthrough BIDS

## Steps:  
1. Get heuristic file and bash script, or relevant command.....  
2. Submit process.......  
3. QC -
  * Run BIDS validation:  


      # run singularity container

  * Simple commands to check directory:  


       # change to bids directory -  
       i.e `cd /projects/niblab/bids_projects/Experiments/bbx/bids`  

  Then you can run these commands to quickly get some initial information:  

     # count attempted subjects formatted to bids:  
        `ls sub-*/[ses-*] | wc -l`  
     # good check is to count how many functional, `func/`, directories were created:  
        `ls sub-*/[ses-*]/func | wc -l`    


3. Check volume files and scan notes
5. Fill in `.json` files before running fmriprep, this enables fmriprep to run **Susceptibility Distortion Correction(SDC)** | *NOTE-make sure to add permissions to bids directory or else phasediff json will not be edited.*
6.
