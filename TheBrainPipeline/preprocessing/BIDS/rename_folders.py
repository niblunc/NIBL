import os, glob, shutil

# This program is going to input original DICOM directories
# that we will rename so our analysis will follow a consistent naming scheme. 


# Input Needed: directory path containing subject folders, output directory (if different than original)

input_dir = '/projects/niblab/bids_projects/Experiments/bbx/DICOM'

FOLDERS = glob.glob(os.path.join(input_dir, "*"))

for folder in FOLDERS:
    folder_name_split = folder.split("/")[-1].split("_")
    print(folder_name)
    study_name = folder_name.split("_")[0]
    subject_id = folder_name.split("_")
    print(study_name, subject_id)
    #if folder_name.split("_") > 2: 
     #   sess_id = folder_name.split("_")[2]
      #  print(sess_id)