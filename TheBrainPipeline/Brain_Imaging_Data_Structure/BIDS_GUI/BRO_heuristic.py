import os
def create_key(template, outtype=('nii.gz',), annotation_classes=None):
    if template is None or not template:
        raise ValueError('Template must be a valid format string')
    return template, outtype, annotation_classes


def infotodict(seqinfo):
    # create directories

    # anat/
    t1 = create_key('anat/{subject}_{session}_T1w')


    # fmap/
    fmap_phase = create_key('fmap/{subject}_{session}_phasediff')
    fmap_magnitude = create_key('fmap/{subject}_{session}_magnitude')


    # func/
    rest = create_key('func/{subject}_{session}_task-resting_run-{item:01d}_bold')
    train = create_key('func/{subject}_{session}_task-training_run-{item:01d}_bold')
    pe = create_key('func/{subject}_{session}_task-pe_run-{item:01d}_bold')



    info = {t1: [],  fmap_phase: [], fmap_magnitude: [], rest: [], train: [], pe: []}
    for s in seqinfo:
        print(s)
        if ('anat' in s.protocol_name):
            info[t1].append(s.series_id)  ## append if multiple series meet criteria
        if (s.dim3 == 36) and ('fmap' in s.protocol_name):
                info[fmap_phase].append(s.series_id)  ## append if multiple series meet criteria
        if (s.dim3 == 72) and ('fmap' in s.protocol_name):
                info[fmap_magnitude].append(s.series_id)  # append if multiple series meet criteria

        if ('training' in s.protocol_name):
            info[train].append(s.series_id)  # append if multiple series meet criteria
        if ('resting' in s.protocol_name):
            info[rest].append(s.series_id)  # append if multiple series meet criteria
        if  ('pe' in s.protocol_name):
            info[pe].append(s.series_id)


    return info