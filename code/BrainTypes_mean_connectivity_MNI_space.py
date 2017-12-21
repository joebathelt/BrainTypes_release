import sys
sys.path.append('/home/jb07/nipype_installation/')
sys.path.append('/home/jb07/python_modules/')

from nipype.interfaces import dipy
from nipype.interfaces import fsl
import os

base_directory = '/imaging/jb07/CALM/BrainTypes/CALM/'
out_directory = '/imaging/jb07/CALM/BrainTypes/CALM/tractography_illustration/'

for side in ['rightCing']: #'leftCing',
    filename = lambda subject: base_directory + '/tractography/' + subject + '/leftCing_density.nii'
    subject_list = sorted([subject for subject in os.listdir(base_directory + '/tractography') if os.path.isfile(filename(subject))])

    for subject in subject_list:
        # Move FA to MNI space
        flt = fsl.FLIRT()
        flt.inputs.dof = 12
        flt.inputs.cost_func='corratio'
        flt.inputs.reference = os.environ['FSLDIR'] + '/data/standard/FMRIB58_FA_1mm.nii.gz'
        flt.inputs.out_matrix_file = out_directory + subject + '_2MNI.mat'
        flt.inputs.out_file = out_directory + subject + '_MNI.nii.gz'
        flt.inputs.in_file = base_directory + '/whole_brain_tractography/_subject_id_' + subject + '/preprocessed/' + subject + '_FA.nii.gz'
        flt.run()

        applyxfm = fsl.FLIRT()
        applyxfm.inputs.apply_xfm = True
        applyxfm.inputs.reference = os.environ['FSLDIR'] + '/data/standard/FMRIB58_FA_1mm.nii.gz'
        applyxfm.inputs.in_file = base_directory + '/tractography/' + subject + '/' + side + '_density.nii'
        applyxfm.inputs.in_matrix_file = out_directory + subject + '_2MNI.mat'
        applyxfm.inputs.out_file = out_directory + subject + '_' + side + '_density.nii.gz'
        applyxfm.run()

    import nibabel as nib
    import numpy as np

    filename = lambda subject: out_directory + subject + '_' + side + '_density.nii.gz'
    density_images = np.rollaxis(np.asarray([nib.load(filename(subject)).get_data() for subject in subject_list]), 0, 4)
    mean_density = np.mean(density_images, axis=3)
    nib.save(nib.Nifti1Image(mean_density, nib.load(filename(subject_list[0])).affine), out_directory + side + '_mean_density.nii.gz')

for tract in ['leftCing', 'rightCing']:
    import nibabel as nib
    img = nib.load('/imaging/jb07/CALM/BrainTypes/CALM/tractography_illustration/' + tract +'_mean_density.nii.gz')
    data = img.get_data()

    data = np.log10(data)
    data[isinf(data)] = 0
    nib.save(nib.Nifti1Image(data, img.affine), out_directory + tract + '_mean_density_log.nii.gz')
