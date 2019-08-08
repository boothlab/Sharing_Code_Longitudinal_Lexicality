# A script to check stimuli files listed in events.tsv are all and only ones in stimuli/
# August 2019 for bids formatted dataset entitled "Longitudinal Brain Correlates of Multisensory Lexical Processing in Children"

import sys
import os
import pandas as pd

stimspath = "../stimuli/"
bids_path = "../"

subs = [folder for folder in os.listdir(bids_path) if 'sub' in folder]
event_data = pd.DataFrame()

for subj in subs:
    func_paths = [(bids_path + subj + '/ses-T1/func/'), (bids_path + subj + '/ses-T2/func')]
    for folder in [f for f in func_paths if os.path.isdir(f)]:
        for event_file in [f for f in os.listdir(folder) if 'events' in f]:
            sub_data = pd.read_csv((folder + '/' + event_file), sep='\t', header=0)
            sub_data = sub_data[['A_stim', 'B_stim']]
            event_data = event_data.append(sub_data)

event_data = event_data.unstack().reset_index(drop=True).drop_duplicates()
event_data = event_data.tolist()

stim_files = [f for f in os.listdir(stimspath) if 'tsv' not in f]

missing = [stim for stim in event_data if stim not in stim_files]
extras = [stim for stim in stim_files if stim not in event_data]

print('missing:')
print(missing)
print('extras:')
print(extras)
