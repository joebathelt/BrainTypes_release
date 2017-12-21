import os
from subprocess import call

# Submission for NKI sample
in_folder = '/imaging/jb07/NKI/BIDS/'
dwi = lambda subject: "/imaging/jb07/NKI/BIDS/" + subject + "/dwi/" + subject + "_dwi.nii.gz"
subject_list = sorted([subject for subject in os.listdir(in_folder) if os.path.isfile(dwi(subject))])
out_directory = '/imaging/jb07/CALM/BrainTypes/NKI/'


for subject in subject_list:
	cmd = "python /home/jb07/joe_python/GitHub/BrainTypes/code/BrainTypes_dwi_preproc.py " + \
	"--acqparams '/imaging/jb07/NKI/BIDS/acqparams.txt' " + \
	"--base_directory '/imaging/jb07/NKI/BIDS/' " + \
	"--subject_list '" + subject + "' " + \
	"--index_file '/imaging/jb07/NKI/BIDS/index.txt' " + \
	"--out_directory " + out_directory

	file = open(out_directory + '/scripts/' + subject + '_dwi_preproc.sh', 'w')
	file.write(cmd)
	file.close()

	cmd = 'qsub ' + out_directory + '/scripts/' + subject + '_dwi_preproc.sh'
	call(cmd, shell=True)

# Submission for the CALM sample
in_folder = '/imaging/jb07/CALM/CALM_BIDS/'
dwi = lambda subject: "/imaging/jb07/CALM/CALM_BIDS/" + subject + "/dwi/" + subject + "_dwi.nii.gz"
subject_list = sorted([subject for subject in os.listdir(in_folder) if os.path.isfile(dwi(subject))])
out_directory = '/imaging/jb07/CALM/BrainTypes/CALM/'


for subject in subject_list:
	cmd = "python /home/jb07/joe_python/GitHub/BrainTypes/code/BrainTypes_dwi_preproc.py " + \
	"--acqparams '/imaging/jb07/CALM/CALM_BIDS/acqparams.txt' " + \
	"--base_directory '/imaging/jb07/CALM/CALM_BIDS/' " + \
	"--subject_list '" + subject + "' " + \
	"--index_file '/imaging/jb07/CALM/CALM_BIDS/index.txt' " + \
	"--out_directory '/imaging/jb07/CALM/BrainTypes/CALM/' "

	file = open(out_directory + '/scripts/' + subject + '_dwi_preproc.sh', 'w')
	file.write(cmd)
	file.close()

	cmd = 'qsub ' + out_directory + '/scripts/' + subject + '_dwi_preproc.sh'
	call(cmd, shell=True)


# Submission for the ACE sample
in_folder = '/imaging/aj05/ACE_DTI_data/original_BIDS/'
dwi = lambda subject: "/imaging/aj05/ACE_DTI_data/original_BIDS/" + subject + "/dwi/" + subject + "_dwi.nii.gz"
subject_list = sorted([subject for subject in os.listdir(in_folder) if os.path.isfile(dwi(subject))])
out_directory = '/imaging/jb07/CALM/BrainTypes/ACE/'


for subject in subject_list:
	cmd = "python /home/jb07/joe_python/GitHub/BrainTypes/code/BrainTypes_dwi_preproc.py " + \
	"--acqparams '/imaging/jb07/CALM/CALM_BIDS/acqparams.txt' " + \
	"--base_directory '/imaging/aj05/ACE_DTI_data/original_BIDS/' " + \
	"--subject_list '" + subject + "' " + \
	"--index_file '/imaging/jb07/CALM/CALM_BIDS/index.txt' " + \
	"--out_directory '/imaging/jb07/CALM/BrainTypes/ACE/' "

	file = open(out_directory + '/scripts/' + subject + '_dwi_preproc.sh', 'w')
	file.write(cmd)
	file.close()

	cmd = 'qsub ' + out_directory + '/scripts/' + subject + '_dwi_preproc.sh'
	call(cmd, shell=True)
