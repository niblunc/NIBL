# BIDS Validator

Image: bids_validator.simg  
Location: /projects/niblab/bids_projects/Singularity_Containers 

### Workflow: <br>
Log onto RENCI --> Start Singularity shell --> Validate BIDS dataset

    BIDS-validator command:
          $ bids-validator {data_directory}


#### Example:

Validate Bevel:
```
cd /projects/niblab/bids_projects
sinteractive
singularity shell -B /projects/niblab/bids_projects:/test Singularity_Containers/bids_validator.simg
cd /test
bids-validator Experiments/Bevel/BIDS
```
