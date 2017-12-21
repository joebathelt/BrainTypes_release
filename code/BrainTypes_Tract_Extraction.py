# =============================================
# Extracting the values for each tract

import nibabel as nib
import numpy as np
import os
import pandas as pd
import re

filename = lambda subject:  infolder + subject + '_Warped.nii.gz'

atlas = os.environ['FSLDIR'] + '/data/atlases/JHU/JHU-ICBM-tracts-maxprob-thr25-1mm.nii.gz'
atlas_data = nib.load(atlas).get_data()
results = []

for subject in subject_list:
    subject_img = nib.load(filename(subject))
    subject_data = subject_img.get_data()

    for tract in np.unique(atlas_data)[1:]:
        tract_data = atlas_data.copy()
        tract_data[tract_data == tract] = 100
        tract_data[tract_data < 100] = 0
        tract_data[tract_data == 100] = 1

        subject_tract = subject_data*tract_data
        tract_value = np.mean(subject_tract[subject_tract > 0])
        results.append({'ID': subject,
                         'tract': tract,
                         'FA': tract_value})

results = pd.DataFrame(results)
results.to_csv(out_folder + 'FA_values_by_tract.csv')
