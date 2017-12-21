## CALM
import os
import pandas as pd
from subprocess import call

df = pd.read_csv('/imaging/jb07/CALM/DWI/motion_estimation/Displacement_Results.csv')
df.columns = ['ID', 'movement', 'volumes']
subject_list = sorted(df[(df['movement'] < 3) & (df['volumes'] == 69)]['ID'])
out_directory = '/imaging/jb07/CALM/BrainTypes/CALM/scripts/'

for subject in subject_list:
    cmd = "python /home/jb07/joe_python/GitHub/BrainTypes/code/BrainTypes_whole_brain_tractography.py \
        --base_directory '/imaging/jb07/CALM/CALM_BIDS/' \
        --subject_list " + subject + " \
        --template_directory '/home/jb07/joe_python/GitHub/Modularity/NKI/' \
        --out_directory '/imaging/jb07/CALM/BrainTypes/CALM/' \
        --parcellation_directory '/home/jb07/joe_python/GitHub/Modularity/FreeSurfer_templates/' \
        --acquisition_parameters '/imaging/jb07/CALM/CALM_BIDS/acqparams.txt' \
        --index_file '/imaging/jb07/CALM/CALM_BIDS/index.txt'"
    file = open(out_directory + subject + '_tractography.sh', 'w')
    file.write(cmd)
    file.close()

    cmd = 'qsub ' + out_directory + subject + '_tractography.sh -l walltime=48:00:00'
    call(cmd, shell=True)

# ===============================================================================================
## ACE

df = pd.read_csv('/imaging/jb07/ACE/motion_estimation/Displacement_Results.csv')
df.columns = ['ID', 'movement', 'volumes']
subject_list = sorted(df[(df['movement'] < 3) & (df['volumes'] == 69)]['ID'])
out_directory = '/imaging/jb07/CALM/BrainTypes/ACE/scripts/'

for subject in subject_list:
    cmd = "python /home/jb07/joe_python/GitHub/BrainTypes/code/BrainTypes_whole_brain_tractography.py \
        --base_directory '/imaging/aj05/ACE_DTI_data/original_BIDS/' \
        --subject_list " + subject + " \
        --template_directory '/home/jb07/joe_python/GitHub/Modularity/NKI/' \
        --out_directory '/imaging/jb07/CALM/BrainTypes/ACE/' \
        --parcellation_directory '/home/jb07/joe_python/GitHub/Modularity/FreeSurfer_templates/' \
        --acquisition_parameters '/imaging/jb07/CALM/CALM_BIDS/acqparams.txt' \
        --index_file '/imaging/jb07/CALM/CALM_BIDS/index.txt'"
    file = open(out_directory + subject + '_tractography.sh', 'w')
    file.write(cmd)
    file.close()

    cmd = 'qsub ' + out_directory + subject + '_tractography.sh -l walltime=48:00:00'
    call(cmd, shell=True)
