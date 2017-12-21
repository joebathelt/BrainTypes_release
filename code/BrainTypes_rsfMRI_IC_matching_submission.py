import os
import pandas as pd
from subprocess import call

out_directory = '/imaging/jb07/CALM/BrainTypes/CALM/scripts/'

# Getting the subject list
file = open('/imaging/jb07/CALM/BrainTypes/CALM/rsfMRI/Melodic_30Oct17+.gica/.filelist', 'r')
subject_list = [line.split('/')[8] for line in file]
file.close()

for subject in subject_list[1:]:
    cmd = "python /home/jb07/joe_python/GitHub/BrainTypes/code/BrainTypes_rsfMRI_IC_matching.py " + \
    "--subject " + subject + " " + \
    "--out_directory '/imaging/jb07/CALM/BrainTypes/CALM/rsfMRI/individual_IC/'"

    file = open(out_directory + subject + '_IC_matching.sh', 'w')
    file.write(cmd)
    file.close()

    cmd = 'qsub ' + out_directory + subject + '_IC_matching.sh -l walltime=48:00:00'
    call(cmd, shell=True)
