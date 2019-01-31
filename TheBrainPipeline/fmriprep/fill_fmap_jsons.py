
# coding: utf-8

# In[ ]:


import glob, os
import json
import argparse 

def set_parser():
    global arglist
    parser=argparse.ArgumentParser(description='Fill in the jsons in BIDS for SDC')
    parser.add_argument('-input',dest='IN',
                        default=False, help='Enter input directory where sub-*/ folders are held')
    args = parser.parse_args()
    arglist={}
    for a in args._get_kwargs():
        arglist[a[0]]=a[1]


# In[ ]:


def run_program():
    INPUT_DIR = arglist["IN"]
    subjects = glob.glob(os.path.join(INPUT_DIR, "sub-*"))
    for subDir in sorted(subjects):
    #initiate the data dictionary
        new_data = {"IntendedFor" : []}
    #grab all the functionals for the subject
        funcs=glob.glob(os.path.join(subDir, "func/*.nii.gz"))
    #fill in our data dictionary with the functionals
        for func in funcs:
            x = func.split("/")[-1]
            x = os.path.join("func",x)
            new_data["IntendedFor"].append(x)
    #get the json files we need to append data to
        jsons=glob.glob(os.path.join(subDir, "fmap/*.json"))
    #loop through jsons and edit each file
        for j in jsons:
        #print(new_data)
            print("Editing file ....... %s"%j)
        #open the json file
            try:
                with open(j) as f:
                    data = json.load(f)
        #update the data file with our new data
                data.update(new_data)
        #add the new update to the json file
                with open(j, 'w') as f:
                    json.dump(data, f, indent=2)
            except:
                print("CANT EDIT FILE ", j)
        

def main():
    set_parser()
    run_program()
    
if __name__== "__main__":
    main()

