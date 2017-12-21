import os
import pandas as pd
from subprocess import call

base_directory = '/imaging/jb07/CALM/CALM_BIDS/'
rsfMRI_name  = lambda subject: base_directory + subject + '/func/' + subject + '_task-rest.nii.gz'
subject_list = [subject for subject in os.listdir(base_directory) if os.path.isfile(rsfMRI_name(subject))]
out_directory = '/imaging/jb07/CALM/BrainTypes/CALM/scripts/'

for subject in subject_list:
    cmd = "python /home/jb07/joe_python/GitHub/BrainTypes/code/BrainTypes_rsfMRI_processing.py \
        --base_directory '/imaging/jb07/CALM/CALM_BIDS/' \
        --subject_list " + subject + " \
        --out_directory '/imaging/jb07/CALM/BrainTypes/CALM/rsfMRI/'"
    file = open(out_directory + subject + '_rsfmri_preproc.sh', 'w')
    file.write(cmd)
    file.close()

    cmd = 'qsub ' + out_directory + subject + '_rsfmri_preproc.sh'
    call(cmd, shell=True)
