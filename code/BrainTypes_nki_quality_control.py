## Make an overview of the FA files
import os
from shutil import copyfile

in_folder = '/imaging/jb07/CALM/BrainTypes/dwi_preproc/'
out_folder = '/imaging/jb07/CALM/BrainTypes/FA_files/'

dwi = lambda subject: in_folder + '/_subject_id_' + subject + '/dtifit/' + subject + '_FA.nii.gz'
subject_list = sorted([subject.split('_')[-1] for subject in os.listdir(in_folder) if os.path.isfile(dwi(subject.split('_')[-1]))])

for subject in subject_list:
    in_file = in_folder + '/_subject_id_' + subject + '/dtifit/' + subject + '_FA.nii.gz'
    out_file = out_folder + subject + '_FA.nii.gz'

    copyfile(in_file, out_file)

cmd = 'cd ' + out_folder + ' slicesdir *.nii.gz'


## Extract the movement 
import nibabel as nib
import os
import pandas as pd

in_folder = '/imaging/jb07/CALM/BrainTypes/dwi_preproc/'
dwi = lambda subject: in_folder + '/_subject_id_' + subject + '/dtifit/' + subject + '_FA.nii.gz'
subject_list = sorted([subject.split('_')[-1] for subject in os.listdir(in_folder) if os.path.isfile(dwi(subject.split('_')[-1]))])
results = []

for subject in subject_list:
    in_file = in_folder + '/_subject_id_' + subject + '/eddy/eddy_corrected.eddy_movement_rms'
    max_movement = pd.read_csv(in_file, header=None, sep='  ').iloc[:,1].max()

    in_file = in_folder + '/_subject_id_' + subject + '/eddy/eddy_corrected.nii.gz'
    number_of_volumes = nib.load(in_file).header.get_data_shape()[-1]

    results.append({'subject': subject,
                    'movement': max_movement,
                    'volumes': number_of_volumes})

results = pd.DataFrame(results)
results.set_index('subject')
results.to_csv('/imaging/jb07/CALM/BrainTypes/NKI_movement.csv')