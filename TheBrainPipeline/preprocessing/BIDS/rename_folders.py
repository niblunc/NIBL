import os, glob, shutil

# This program is going to input original DICOM directories
# that we will rename so our analysis will follow a consistent naming scheme. 


# Input Needed: directory path containing subject folders, output directory (if different than original)

input_dir = '/projects/niblab/bids_projects/Experiments/bbx/DICOM/originals'

FOLDERS = glob.glob(os.path.join(input_dir, "*"))

for folder in FOLDERS:
    folder_name_split = folder.split("/")[-1].split("_")
    #print(folder_name_split)
    study_name = folder_name_split[0]
    subject_id = folder_name_split[1].split("-")[1]
    #print(study_name, subject_id)
    # Check the length here to see if we have multiple sessions
    if len(folder_name_split) > 2: 
        sess_id = folder_name_split[2]
        multi_sess = True
    else:
        multi_sess = False
        #print(sess_id)
    new_name = ("%s"%subject_id).lower()
    if "sub" not in new_name:
        new_name = "sub-%s"%new_name
    print(new_name)
    # If multi sess is true, move the folders into the session directory
    # first then rename in the folders 
    if multi_sess == True:
        print(">>> I am multiple sessions")
        output_dir = os.path.join(input_dir, sess_id)
        print(output_dir)
        print("")
        #shutil.move(folder, output_dir)