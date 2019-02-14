import os
def create_key(template, outtype=('nii.gz',), annotation_classes=None):
    if template is None or not template:
        raise ValueError('Template must be a valid format string')
    return template, outtype, annotation_classes


def infotodict(seqinfo):
    # create directories and key files here 
    # common directories are:
    
    # anat/


    # fmap/



    # func/



    # create info dictionary below to reference ids
    info = { }
    
    
    # sort dicoms below and fill in the info dictionary
    for s in seqinfo:

    return info