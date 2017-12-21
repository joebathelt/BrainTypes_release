#! /usr/bin/env python
import optparse
import os
import re
import sys
reload(sys)
sys.setdefaultencoding('utf8')

sys.path.append('/home/jb07/nipype_installation/')
sys.path.append('/home/jb07/joe_python/GitHub/BrainTypes/code/')

def main():
    p = optparse.OptionParser()

    p.add_option('--base_directory', '-b')
    p.add_option('--subject_list', '-s')
    p.add_option('--out_directory', '-o')
    sys.path.append(os.path.realpath(__file__))

    options, arguments = p.parse_args()
    base_directory = options.base_directory
    out_directory = options.out_directory
    subject_list = options.subject_list
    subject_list = [subject for subject in subject_list.split(
        ',') if subject]

    def preprocessing_for_Melodic(subject_list, base_directory, out_directory):

        from BrainTypes_additional_interfaces import DipyDenoiseT1
        import nipype.interfaces.fsl as fsl
        import nipype.interfaces.io as nio
        import nipype.pipeline.engine as pe
        import nipype.interfaces.utility as util
        from nipype import SelectFiles
        import os

        # ==================================================================
        # Defining the nodes for the workflow

        # Getting the subject ID
        infosource = pe.Node(interface=util.IdentityInterface(
            fields=['subject_id']), name='infosource')
        infosource.iterables = ('subject_id', subject_list)

        # Getting the relevant diffusion-weighted data
        templates = dict(T1='{subject_id}/anat/{subject_id}_T1w.nii.gz',
                         func='{subject_id}/func/{subject_id}_task-rest.nii.gz')

        selectfiles = pe.Node(interface=SelectFiles(templates),
                              name='selectfiles')
        selectfiles.inputs.base_directory = os.path.abspath(base_directory)

        ### Preprocessing of the structural images
        # Getting a better field of view
        robustfov = pe.Node(interface=fsl.RobustFOV(), name='robustfov')

        # Denoising
        T1_denoise = pe.Node(interface=DipyDenoiseT1(), name='T1_denoise')

        # Brain extraction
        brainextraction = pe.Node(interface=fsl.BET(), name='brainextraction')

        ### Running motion correction on the functional images
        mcflirt = pe.Node(interface=fsl.MCFLIRT(), name='mcflirt')
        mcflirt.inputs.cost = 'mutualinfo'
        mcflirt.inputs.save_plots = True
        mcflirt.inputs.save_rms = True

        ### Getting the motion parameters
        motion_outliers = pe.Node(interface=fsl.utils.MotionOutliers(), name='motion_outliers')
        motion_outliers.inputs.metric = 'fd'

        ### Creating the folder structure
        datasink = pe.Node(interface=nio.DataSink(), name='sinker')
        datasink.inputs.base_directory = out_directory + '/preprocessed/'
        datasink.inputs.container = out_directory + '/preprocessed/'
        datasink.inputs.substitutions = [('_subject_id_', '')]

        functional_rename = pe.Node(interface=util.Rename(format_string="%(subject_id)s_functional.nii.gz"), name='functional_rename')
        structural_rename = pe.Node(interface=util.Rename(format_string="%(subject_id)s_structural.nii.gz"), name='structural_rename')
        brain_rename = pe.Node(interface=util.Rename(format_string="%(subject_id)s_structural_brain.nii.gz"), name='brain_rename')

        # ==================================================================
        # Connecting the pipeline
        MelodicPreproc = pe.Workflow(name='MelodicPreproc')

        MelodicPreproc.connect(infosource, 'subject_id', selectfiles, 'subject_id')

        # T1 preprocessing
        MelodicPreproc.connect(selectfiles, 'T1', robustfov, 'in_file')
        MelodicPreproc.connect(robustfov, 'out_roi', T1_denoise, 'in_file')
        MelodicPreproc.connect(T1_denoise, 'out_file', structural_rename, 'in_file')
        MelodicPreproc.connect(infosource, 'subject_id', structural_rename, 'subject_id')

        MelodicPreproc.connect(T1_denoise, 'out_file', brainextraction, 'in_file')
        MelodicPreproc.connect(brainextraction, 'out_file', brain_rename, 'in_file')
        MelodicPreproc.connect(infosource, 'subject_id', brain_rename, 'subject_id')

        # Functional preprocessing
        MelodicPreproc.connect(selectfiles, 'func', mcflirt, 'in_file')
        MelodicPreproc.connect(mcflirt, 'out_file', functional_rename, 'in_file')
        MelodicPreproc.connect(infosource, 'subject_id', functional_rename, 'subject_id')

        # Getting the motion parameters
        MelodicPreproc.connect(selectfiles, 'func', motion_outliers, 'in_file')

        # Moving everything to a folder structure that is compatible with FSL Melodic
        MelodicPreproc.connect(functional_rename, 'out_file', datasink, '@functional')
        MelodicPreproc.connect(structural_rename, 'out_file', datasink, '@structural')
        MelodicPreproc.connect(brain_rename, 'out_file', datasink, '@brain_structural')

        # ==================================================================
        # Running the workflow
        MelodicPreproc.base_dir = os.path.abspath(out_directory)
        MelodicPreproc.write_graph()
        MelodicPreproc.run()

    os.chdir(out_directory)
    preprocessing_for_Melodic(subject_list, base_directory, out_directory)

if __name__ == '__main__':
    # main should return 0 for success, something else (usually 1) for error.
    sys.exit(main())
