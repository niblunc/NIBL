if not os.path.exists(confound_path):
    os.system(outlier_cmd)

    ## EXAMINE OUTLIER FILE AND GRAB RELEVANT DATA
with open(outlier_path, 'r') as f:
    lines = f.readlines()
    statsA = lines[1].strip("\n")  # maskmean
    statsB = lines[3].strip("\n")  # metric range
    statsC = lines[4].strip("\n")  # outliers found
    if int(statsC.split(" ")[1]) > 0:
        statsD = lines[6].strip("\n")  # spikes found
    else:
        statsD = "\n"
f.close()
## GRAB MOTION CORRECTION PLOT AND WRITE PLOT & INFO TO HTML
plotz = plot_path + ".png"
FILEINFO = """<p><font size=6> <b>{CURR_FILENAME} </b></font><br>"""
CURR_FILEINFO = FILEINFO.format(CURR_FILENAME=file)
outfile.write(CURR_FILEINFO)
INFO = """<p><font size=6>{A} <br><b>{B}<b><br>{C}<br><b>{D}</b><br><br>"""
CURR_INFO = INFO.format(A=statsA, B=statsB, C=statsC, D=statsD)
outfile.write(CURR_INFO)
PLOT = """<IMG SRC=\"{PLOTPATH}\" WIDTH=100%><br><br>"""
CURR_PLOT = PLOT.format(PLOTPATH=plotz)
outfile.write(CURR_PLOT)
print(">>>>----> ADDING PLOT TO HTML")
## ADD FILE FOR GOOD SUBJECT
# --sometimes you have a great subject who didn't move
if os.path.isfile(confound_path) == False:
    os.system("touch %s" % confound_path)
## CHECK FOR BAD SUBJECTS: ABOVE OUR THRESHOLD
# how many columns are there = how many 'bad' points
check = subprocess.check_output("grep -o 1 %s | wc -l" % (confound_path), shell=True)
num_scrub = [int(s) for s in check.split() if s.isdigit()]
print("NUM SCRUB: ", str(num_scrub[0]), "\n")
if num_scrub[0] > comparator:  # if the number in check is greater than num_scrub then we don't want it
    with open(out_bad_bold_list, "a") as myfile:  # making a file that lists all the bad ones
        myfile.write("%s/%s\n" % (derivatives_dir, file))
        print("wrote bad file")
    myfile.close()
except FileNotFoundError:
print("FILE IS EMPTY, PASSING")

python prepro.py -fd 0.9 -ses -ses_id 1 -bids  /projects/niblab/bids_projects/Experiments/bbx/bids


python prepro.py -fd 0.9 -ses -ses_id 1 -bids  /projects/niblab/bids_projects/Experiments/bbx/bids
python prepro.py -bet 0.6 -ses -ses_id 1 -bids /Users/nikkibytes/Documents/git_nibl/data/bbx_test_data/bids

python fmri_pipe.py -motion -ses -ses_id 1 -bids /projects/niblab/bids_projects/Experiments/bbx/bids