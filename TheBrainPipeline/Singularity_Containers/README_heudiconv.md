## BIDS Converter with heudiconv

Image: heudiconv.simg

This container allows us to open up an environment to run the heudiconv converter and convert our data into BIDS format.

### Workflow: <br>
Log into RENCI --> Start Singularity shell --> Run commands


    heudiconv command:
          $ heudiconv -b -d {input_directory} -s {SUBJECT} -ss {SESSION} -f {heuristic_file} \
          -c dcm2niix -b  -o {output_directory}



  * Notes:\
    -- heuristic_file: Unique file of keys we must provide that tells how the files are to be converted. \
          We use the information from our dicominfo.tsv to fill in our keys.


#### Examples

Example: command for getting the dicominfo.tsv file
```
heudiconv -d raw_data/ChocolateData/{session}/{subject}/*dcm -s sub-001 sub-003 \
-ss 2 -f convertall.py -c none -o /output/ChocolateData
 
 # output file held here
 /output/ChocolateData/.heudiconv/sub-001/info/dicominfo.tsv

```
Example: converting a single subject
```
```
Example: Converting all subjects To convert multiple subjects we can create a simple script that loops through our subjects.
```
```
