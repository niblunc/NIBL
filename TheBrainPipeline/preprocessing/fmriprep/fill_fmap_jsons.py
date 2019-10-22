
# coding: utf-8

# In[ ]:


import glob, os
import json
import argparse

def set_parser():
    global arglist
    parser=argparse.ArgumentParser(description='Fill in the jsons in BIDS for Susceptibility Distortion Correction(SDC)')
    parser.add_argument('-input',dest='IN',
                        default=False, help='Enter input directory where sub-*/ folders are held')
    parser.add_argument('-sess', dest="SESS", default=False, action='store_true',
                        help='Use flag if multiple sessions, if only specific session, use -sess_id flag instead')
    parser.add_argument('-sess_id', dest="SESS_ID", default=False,
                        help='Use flag if multiple sessions, if only specific session, use -sess_id flag instead')
    args = parser.parse_args()
    arglist={}
    for a in args._get_kwargs():
        arglist[a[0]]=a[1]


# In[ ]:


def run_program():
    INPUT_DIR = arglist["IN"]

    # Check if there is a specific session given
    if arglist["SESS_ID"] != False:
        subjects = glob.glob(os.path.join(INPUT_DIR, "sub-*",  arglist["SESS_ID"]))
        print(">Running single session: {} \n".format(arglist["SESS_ID"]))
    # if not check if there is just a general session flag given
    elif arglist["SESS"] == True:
        subjects = glob.glob(os.path.join(INPUT_DIR, "sub-*", "ses-*"))
        print(">Running multiple sessions \n")
    # if not, assume NO SESSIONS, get subjects from input dir
    else:
        subjects = glob.glob(os.path.join(INPUT_DIR, "sub-*"))
        print(">Running single study, no sessions. \n")


    for sub_dir in sorted(subjects):
    #initiate the data dictionary
        new_data = {"IntendedFor" : []}
    #grab all the functionals for the subject
        funcs=glob.glob(os.path.join(sub_dir, "func/*.nii.gz"))
    #fill in our data dictionary with the functionals
        for func in funcs:
            x = func.split("/")[-1]
            x = os.path.join("func",x)
            new_data["IntendedFor"].append(x)
    #get the json files we need to append data to
        jsons=glob.glob(os.path.join(sub_dir, "fmap/*.json"))
    #loop through jsons and edit each file
        for j in jsons:
        #print(new_data)
            print("Editing file ....... %s"%j)
        #open the json file
    """        try:
                with open(j) as f:
                    data = json.load(f)
        #update the data file with our new data
                data.update(new_data)
        #add the new update to the json file
                with open(j, 'w') as f:
                    json.dump(data, f, indent=2)
            except:
                print("CANT EDIT FILE -- check permissions on folders ", j)"""


def main():
    set_parser()
    run_program()

if __name__== "__main__":
    main()
