#! /usr/bin/env python
import optparse
import os
import re
import sys
sys.path.append('/home/jb07/nipype_installation/')
sys.path.append('/home/jb07/joe_python/GitHub/BrainTypes/code/')

def main():
    import os
    import sys
    p = optparse.OptionParser()

    p.add_option('--acqparams', '-a')
    p.add_option('--base_directory', '-b')
    p.add_option('--index_file', '-i')
    p.add_option('--out_directory', '-o')
    p.add_option('--subject_list', '-s')

    options, arguments = p.parse_args()
    acqparams =  options.acqparams
    base_directory = options.base_directory
    index_file =  options.index_file
    out_directory = options.out_directory
    subject_list = options.subject_list
    subject_list = [subject for subject in subject_list.split(
        ',')]

    def dwi_preproc(acqparams, base_directory, index_file, out_directory, subject_list):

        # Loading required packages
        from BrainTypes_additional_interfaces import ants_QuickSyN
        import nipype.interfaces.fsl as fsl
        import nipype.interfaces.io as nio
        import nipype.pipeline.engine as pe
        from nipype import SelectFiles
        import nipype.interfaces.utility as util
        import os

        # ==============================================================
        # Processing of diffusion-weighted data
        infosource = pe.Node(interface=util.IdentityInterface(
        fields=['subject_id']), name='infosource')
        infosource.iterables = ('subject_id', subject_list)

        # Getting the relevant data
        templates = dict(dwi='{subject_id}/dwi/{subject_id}_dwi.nii.gz',
                     bvec='{subject_id}/dwi/{subject_id}_dwi.bvec',
                     bval='{subject_id}/dwi/{subject_id}_dwi.bval')

        selectfiles = pe.Node(SelectFiles(templates), name="selectfiles")
        selectfiles.inputs.base_directory = os.path.abspath(base_directory)

        # Extract b0 image
        fslroi = pe.Node(interface=fsl.ExtractROI(), name='fslroi')
        fslroi.inputs.t_min = 0
        fslroi.inputs.t_size = 1

        # Create a brain mask
        bet = pe.Node(interface=fsl.BET(
        frac=0.3, robust=False, mask=True, no_output=False), name='bet')

        # Eddy-current and motion correction
        eddy = pe.Node(interface=fsl.epi.Eddy(args='-v'), name='eddy')
        eddy.inputs.in_acqp  = acqparams
        eddy.inputs.in_index = index_file

        # Fitting the diffusion tensor model
        dtifit = pe.Node(interface=fsl.DTIFit(), name='dtifit')

        # Moving files to MNI space
        reg = pe.Node(interface=ants_QuickSyN(), name='reg')
        reg.inputs.fixed_image = os.environ['FSLDIR'] + '/data/standard/FMRIB58_FA_1mm.nii.gz'
        reg.inputs.image_dimensions = 3
        reg.inputs.transform_type = 's'

        # ==============================================================
        # Setting up the workflow
        dwi_preproc = pe.Workflow(name='dwi_preproc')
        dwi_preproc.connect(infosource, 'subject_id', selectfiles, 'subject_id')

        # Diffusion data
        # Preprocessing
        dwi_preproc.connect(selectfiles, 'dwi', fslroi, 'in_file')
        dwi_preproc.connect(fslroi, 'roi_file', bet, 'in_file')
        dwi_preproc.connect(bet, 'mask_file', eddy, 'in_mask')
        dwi_preproc.connect(selectfiles, 'dwi', eddy, 'in_file')
        dwi_preproc.connect(selectfiles, 'bvec', eddy, 'in_bvec')
        dwi_preproc.connect(selectfiles, 'bval', eddy, 'in_bval')

        # Calculate diffusion measures
        dwi_preproc.connect(eddy, 'out_corrected', dtifit, 'dwi')
        dwi_preproc.connect(bet, 'mask_file', dtifit, 'mask')
        dwi_preproc.connect(infosource, 'subject_id', dtifit, 'base_name')
        dwi_preproc.connect(selectfiles, 'bvec', dtifit, 'bvecs')
        dwi_preproc.connect(selectfiles, 'bval', dtifit, 'bvals')
        dwi_preproc.connect(dtifit, 'FA', reg, 'moving_image')
        dwi_preproc.connect(infosource, 'subject_id', reg, 'output_prefix')

        # ==============================================================
        # Running the workflow
        dwi_preproc.base_dir = os.path.abspath(out_directory)
        dwi_preproc.write_graph()
        dwi_preproc.run()

    dwi_preproc(acqparams, base_directory, index_file, out_directory, subject_list)

if __name__ == '__main__':
    # main should return 0 for success, something else (usually 1) for error.
    sys.exit(main())
