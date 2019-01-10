import subprocess
import random
heudiconv_cmd = "singularity exec -B /:/test /projects/niblab/bids_projects/Singularity_Containers/heudiconv.simg heudiconv -b "

item = subprocess.Popen(["/Users/nikkibytes/Documents/TheBrainPipeline/BIDS/test.bat", heudiconv_cmd])
