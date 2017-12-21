# Repository of analysis code for "Data-driven brain types and their cognitive consequences"
This repository contains the analysis code to reproduce the analyses presented in the paper Bathelt, J., Johnson, A., Zhang, M., the CALM team & Astle, D. E. "Data-driven brain types and their cognitive consequences". The main analyses can be found in the following IPython Notebooks:

- Brain_Types_main_analysis.ipynb:
    - descriptive statistics of all samples
    - grouping based on FA values in 20 white matter tracts using community detection
    - application of these grouping to the CALM and ACE sample
    - robustness testing of community clustering with simulated data
    - statistical comparison of cognitive scores between the clustering-defined groups


- BrainTypes_CingulumConnectivity.ipynb:
    - mapping of structural connectivity of the cingulum
    - comparison of cingulum connectivity between the brain types
    - regression analysis of single cingulum connectivity and cognitive scores


- BrainTypes_rsfMRI_analysis.ipynb:
    - identification of the default mode network (DMN) from group-level independent component analysis (ICA)
    - identification of the DMN from individual ICA
    - comparison of spatial extent and total acitvation of the DMN between brain types


There are also several python scripts that contain the pipelines and functions used for data preprocessing. Specifically:

- BrainTypes_additional_interfaces.py: definition of additional interfaces called by the pipelines


- BrainTypes_additional_pipelines.py: definition of additional pipelines called by higher-order pipelines


- BrainTypes_analysis_functions.py: helper functions used in the analysis notebooks


- BrainTypes_dwi_preproc.py: pipeline for preprocessing of diffusion-weighted data


- BrainTypes_dwi_preproc_submission.py: wrapper script to submit the dwi preprocessing to a compute cluster


- BrainTypes_mean_connectivity_MNI_space.py: functions to map individual cingulum connectivity to MNI space for visualization


- BrainTypes_nki_quality_control.py: script to extract dwi quality indices in the NKI sample


- BrainTypes_rsfMRI_correlation.py: script to extract partial correlations between ROIs from fMRI data


- BrainTypes_rsfMRI_data_quality.py: script to extract quality metrics from fMRI data


- BrainTypes_rsfMRI_IC_matching.py: script to match components from individual ICA to a template


- BrainTypes_rsfMRI_IC_matching_submission.py: wrapper script to submit IC matching to a compute cluster


- BrainTypes_rsfMRI_processing.py: preprocessing pipeline for fMRI data


- BrainTypes_rsfMRI_processing_submission.py: wrapper script to submit rsfMRI preprocessing to a compute cluster


- BrainTypes_Tract_Extraction.py: script to extract FA values defined in an atlas parcellation from dwi


- BrainTypes_whole_brain_tractography.py: pipeline to perform whole-brain probabilistic tractography


- BrainTypes_whole_brain_tractography_submission.py: wrapper script to submit whole-brain tractography to a compute cluster




written by
Dr Joe Bathelt
MRC Cognition & Brain Sciences Unit
University of Cambridge

please direct any queries to:
joe.bathelt [at] mrc-cbu.cam.ac.uk
