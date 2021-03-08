# Important parameters defined for the main experiment

participant_ID = # e.g. 38
fingertapping_file_name = 'Fingertapping_Data/EEG_feelSpace_fingertapping_participant_' + str(participant_ID) + '.csv'

trials = 200
identical_blocks = 2
oddball_ratio = 0.3
trial_break = 0.7
trial_length = 0.8

# Parameters for the visual oddball task
color_standard = "cyan"
color_oddball = "pink"

# Parameters for the vibrotactile oddball task
ankle_vibromotor = 13
wrist_vibromotor = 7
waist_vibromotor_left =  9
waist_vibromotor_right = 8

# Trigger codes (oddball, standard, break) for the 4 different blocks 
ankle_trigger = [9, 11, 12]
wrist_trigger = [5, 7, 8]
waist_trigger = [1, 3, 4]
visual_trigger = [14, 13, 15]

# "Translation" to the attached labels on the feelSpace belt:
# variable above:attached label
# 12:2
# 7:9
# 9:7
# 8:8
