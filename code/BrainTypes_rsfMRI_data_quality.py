import sys
sys.path.append('/home/jb07/nipype_installation/')

import numpy as np
import os
import pandas as pd
import nibabel as nib


# Get the movement parameters for the resting-state time series
infolder = '/imaging/jb07/CALM/BrainTypes/CALM/rsfMRI/MelodicPreproc/'
motion_file = lambda subject: infolder + '_subject_id_' + subject + '/mcflirt/' + subject + '_task-rest_mcf.nii.gz_rel.rms'
subject_list = sorted([subject.split('_')[-1] for subject in os.listdir(infolder) if os.path.isfile(motion_file(subject.split('_')[-1]))])
movement = [np.max(pd.read_csv(motion_file(subject), header=None)[0].values) for subject in subject_list]
movement_df = pd.DataFrame({'MRI.ID':subject_list, 'movement':movement})

# Get the number of volumes
fMRI_data = lambda subject: '/imaging/jb07/CALM/CALM_BIDS/' + subject + '/func/' + subject + '_task-rest.nii.gz'
movement_df['volumes'] = [nib.load(fMRI_data(subject)).get_header().get_data_shape()[3] for subject in subject_list]

# Get list of functional filenames
quality_df = pd.read_csv('/home/jb07/joe_python/GitHub/BrainTypes/data/derived_data/CALM_rsfMRI_data_quality.csv')
subject_list = quality_df[(quality_df['fMRI.volumes'] == 270) & (quality_df['T1.useable'] == 1)]['MRI.ID'].values
in_folder = '/imaging/jb07/CALM/BrainTypes/CALM/rsfMRI/preprocessed/'
filename = lambda subject: in_folder + subject + '/' + subject + '_functional.nii.gz'
subject_list = sorted([subject for subject in os.listdir(in_folder)])
filenames = [filename(subject) for subject in subject_list]

# Get list of structural filenames
in_folder = '/imaging/jb07/CALM/BrainTypes/CALM/rsfMRI/preprocessed/'
filename = lambda subject: in_folder + subject + '/' + subject + '_functional.nii.gz'
subject_list = sorted([subject for subject in os.listdir(in_folder)])
filenames = [filename(subject) for subject in subject_list]

# Make an overview of the structural files
slicesdir /imaging/jb07/CALM/BrainTypes/CALM/rsfMRI/preprocessed/*/*_structural_brain.nii.gz

# Get the list for Melodic
quality_df = pd.read_csv('/home/jb07/joe_python/GitHub/BrainTypes/data/derived_data/CALM_rsfMRI_data_quality.csv')
subject_list = quality_df[(quality_df['fMRI.volumes'] == 270) & (quality_df['T1.useable'] == 1)]['MRI.ID'].values
folder = '/imaging/jb07/CALM/BrainTypes/CALM/rsfMRI/preprocessed/'
subject_list = sorted([folder + subject + '/' + subject + '_functional.nii.gz' for subject in subject_list])

# Getting additional information about subject motion
melodic_folder = '/imaging/jb07/CALM/BrainTypes/CALM/rsfMRI/Melodic_own_template_full.gica'
subject_list = sorted([subject.split('/')[8] for subject in pd.read_csv(melodic_folder + '/.filelist', header=None)[0].values])

in_folder = '/imaging/jb07/CALM/BrainTypes/CALM/rsfMRI/MelodicPreproc/'
outlier_filename = lambda subject: in_folder + '_subject_id_' + subject + '/motion_outliers/' + subject + '_task-rest_outliers.txt'
displacement_filename = lambda subject: in_folder + '_subject_id_' + subject + '/motion_outliers/' + subject + '_task-rest_metrics.txt'

outliers = [np.sum(np.loadtxt(outlier_filename(subject))) for subject in subject_list]
displacement = [np.mean(np.loadtxt(displacement_filename(subject))) for subject in subject_list]
pd.DataFrame({'number_outliers': outliers, 'mean_motion': displacement}, index=subject_list).to_csv('/home/jb07/joe_python/GitHub/BrainTypes/data/derived_data/CALM_rsfMRI_data_quality_additional_measures.csv')
