import sys
sys.path.append('/home/jb07/nipype_installation/')

from nilearn import input_data
import numpy as np
import pandas as pd
from scipy import stats
from scipy import linalg

def partial_corr(C):
    """
    Returns the sample linear partial correlation coefficients between pairs of variables in C, controlling
    for the remaining variables in C.
    Parameters
    ----------
    C : array-like, shape (n, p)
        Array with the different variables. Each column of C is taken as a variable
    Returns
    -------
    P : array-like, shape (p, p)
        P[i, j] contains the partial correlation of C[:, i] and C[:, j] controlling
        for the remaining variables in C.
    """

    C = np.asarray(C)
    p = C.shape[1]
    P_corr = np.zeros((p, p), dtype=np.float)
    for i in range(p):
        P_corr[i, i] = 1
        for j in range(i+1, p):
            idx = np.ones(p, dtype=np.bool)
            idx[i] = False
            idx[j] = False
            beta_i = linalg.lstsq(C[:, idx], C[:, j])[0]
            beta_j = linalg.lstsq(C[:, idx], C[:, i])[0]

            res_j = C[:, j] - C[:, idx].dot( beta_i)
            res_i = C[:, i] - C[:, idx].dot(beta_j)

            corr = stats.pearsonr(res_i, res_j)[0]
            P_corr[i, j] = corr
            P_corr[j, i] = corr

    return P_corr

# Getting the subject list
file = open('/imaging/jb07/CALM/BrainTypes/CALM/rsfMRI/Melodic_30Oct17+.gica/.filelist', 'r')
subject_list = [line.split('/')[8] for line in file]
file.close()

results = []
counter = 0

for subject in subject_list:
    # Getting the confounds
    confound_file = '/imaging/jb07/CALM/BrainTypes/CALM/rsfMRI/MelodicPreproc/_subject_id_' + subject + '/mcflirt/' + subject + '_task-rest_mcf.nii.gz.par'
    in_file = '/imaging/jb07/CALM/BrainTypes/CALM/rsfMRI/preprocessed/' + subject + '/' + subject + '_functional_Melodic_14Nov16.ica/reg_standard/filtered_func_data_wds.nii.gz'

    df1 = pd.read_csv(confound_file, delim_whitespace=True, header=None)[4:]
    df1.index = np.arange(0, df1.shape[0])

    in_folder = '/imaging/jb07/CALM/BrainTypes/CALM/rsfMRI/dualreg_output_30Oct17+/'
    df2 = pd.read_csv(in_folder + 'dr_stage1_subject' + str(counter).zfill(5) + '.txt', delim_whitespace=True, header=None)[[0, 17, 18, 19]]
    pd.concat([df1, df2], axis=1).to_csv('/home/jb07/Desktop/temp.csv')

    dmn_coords = [(0, -52, 18), (-46, -68, 32), (46, -68, 32), (1, 50, -5)]
    labels = [
              'Posterior Cingulate Cortex',
              'Left Temporoparietal junction',
              'Right Temporoparietal junction',
              'Medial prefrontal cortex',
             ]

    masker = input_data.NiftiSpheresMasker(
        dmn_coords, radius=8,
        detrend=True, standardize=True,
        low_pass=0.1, high_pass=0.01, t_r=2,
        memory='nilearn_cache', memory_level=1, verbose=2)

    time_series = masker.fit_transform(in_file,
                                       confounds=['/home/jb07/Desktop/temp.csv'])

    correlation, p = stats.pearsonr(time_series[0], time_series[3])
    partial_correlation = partial_corr(time_series)[0, 3]

    results.append({'subject': subject,
                    'correlation': correlation,
                    'partial_correlation': partial_correlation})
    counter += 1
pd.DataFrame(results).to_csv('/home/jb07/joe_python/GitHub/BrainTypes/data/derived_data/rsfMRI_correlation.csv')
