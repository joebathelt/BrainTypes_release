#! /usr/bin/env python
import optparse
import os
import sys
sys.path.append('/home/jb07/nipype_installation/')

def main():
    p = optparse.OptionParser()

    p.add_option('--out_directory', '-o')
    p.add_option('--subject', '-s')
    sys.path.append(os.path.realpath(__file__))

    options, arguments = p.parse_args()
    out_directory = options.out_directory
    subject = options.subject

    def get_best_matching_component(out_directory, subject):
        # Individual ICA
        import nibabel as nib
        from nipype.interfaces import fsl
        import numpy as np
        import os
        import pandas as pd
        from scipy.stats import zscore

        # Create a 4D component map (outer product of time course and spatial map)
        subject_folder = '/imaging/jb07/CALM/BrainTypes/CALM/rsfMRI/preprocessed/' + subject + '/' + subject + '_functional_15Nov17_indICA.ica/'
        time_courses = subject_folder + 'filtered_func_data.ica/melodic_mix'
        time_courses = pd.read_csv(time_courses, delim_whitespace=True).values
        number_of_components = time_courses.shape[1]
        spatial_maps = subject_folder + 'filtered_func_data.ica/melodic_IC.nii.gz'
        spatial_affine = nib.load(spatial_maps).affine
        spatial_maps = nib.load(spatial_maps).get_data()
        comp_scores = []

        if not os.path.isdir(out_directory + subject):
            os.mkdir(out_directory + subject)

        # Moving the template mask to subject space
        flirt = fsl.FLIRT()
        flirt.inputs.apply_xfm = True
        flirt.inputs.in_file = '/imaging/jb07/CALM/BrainTypes/CALM/rsfMRI/DMN_template_14Nov17.nii.gz'
        flirt.inputs.reference = subject_folder + '/reg/example_func.nii.gz'
        flirt.inputs.in_matrix_file = subject_folder + '/reg/standard2example_func.mat'
        flirt.inputs.out_file = out_directory + '/' + subject + '/DMN_mask.nii.gz'
        flirt.run()

        dmn_mask = nib.load(out_directory + '/' + subject + '/DMN_mask.nii.gz').get_data()

        # Value outside the DMN mask (but inside the brain)
        flirt = fsl.FLIRT()
        flirt.inputs.apply_xfm = True
        flirt.inputs.in_file = os.environ['FSLDIR'] + '/data/standard/MNI152lin_T1_2mm_brain_mask.nii.gz'
        flirt.inputs.reference = subject_folder + '/reg/example_func.nii.gz'
        flirt.inputs.in_matrix_file = subject_folder + '/reg/standard2example_func.mat'
        flirt.inputs.out_file = out_directory + '/' + subject + '/brain_mask.nii.gz'
        flirt.run()

        brain_mask = nib.load(out_directory + '/' + subject + '/brain_mask.nii.gz').get_data()
        brain_mask = brain_mask - dmn_mask

        for comp in np.arange(0, number_of_components):
            print(str(comp+1) + '/' + str(number_of_components))

            # Creating a space x time 4D image for the component
            IC_map = np.rollaxis(np.reshape(np.outer(time_courses[...,comp], spatial_maps[...,comp]), newshape=[265, 64,64,32]), 0, 4)

            # Value within the DMN mask
            IC_map = zscore(IC_map, axis=3)
            IC_mask = np.ma.masked_array(IC_map[dmn_mask==1], np.isnan(IC_map[dmn_mask==1]))
            if IC_mask.count() > 0:
                inside_value = np.mean(IC_mask)
            else:
                inside_value = 0

            outside_value = np.mean(np.ma.masked_array(IC_map[brain_mask == 1], np.isnan(IC_map[brain_mask == 1])))

            comp_scores.append(inside_value - outside_value)

        best_component = np.where(comp_scores == np.max(comp_scores))[0][0]

        results = {'best_component': best_component+1,
                   'number_of_components': number_of_components}
        pd.DataFrame(results, index=[subject]).to_csv(out_directory + subject + '_IC_matching.txt')

    get_best_matching_component(out_directory, subject)

if __name__ == '__main__':
    # main should return 0 for success, something else (usually 1) for error.
    sys.exit(main())
