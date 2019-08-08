#Converts .csv files containing all e-prime task data 
#separates by subject and saves as .tsv in subject's bids folder
#written for James Booth's lab longitudinal lexicality project
#May 2018

import pandas as pd
import numpy as np
import json
import sys
np.warnings.filterwarnings('ignore') # ignore warnings


sub_map = json.load(open('files/subj_map.json','r')) #subj_map.json contains a dictonary of original subject numbers to consecutive bids subject numbers


# ask for user input instead, only works for one run at a time
# trial = input('Ses (T1, T2): ')
trial = input('Ses (T1, T2): ')
modality = input('Modality (AA, AV, VV): ')    
task = input('Task (NonWord, Word): ')
run = input('Run (01, 02): ')
readingfiles = [trial+'_'+modality+task+'_Run'+run] #name of the file containing all e-prime data for that run


bidpath = input('\nPath to bids folder \n   ./ for current directory \n  ../ for back a directory: ')
for file in readingfiles:
    file_ext = '.csv'
    print('\nCSV file: '+file+file_ext)
    stim = 'files/{}{}-stims_Run{}.csv'.format(modality, task, run)#name of the csv file that contains the stimuli file name per trial, separate from e-prime data due to standardization in naming
    print('Stim file: '+stim)
    
    # read in csv file
    df = pd.read_csv('files/'+file+file_ext)
    
    # rename columns for manageability
    df = df.rename(columns={"Subject_Number": "Subject", "Condition": "trial_type", "TargetCRESP": "cresp", "durations": "duration",
                       "PrimeOnsetTime": "onset", "TargetACC": "accuracy", "TargetRESP": "resp", "TargetRT": "response_time"})
    
    df = df[['Subject', 'onset', 'trial_type', 'accuracy', 'response_time', 'cresp', 'resp', 'duration']]
    
    # convert times from ms to s
    df['duration'] = df['duration'] + 1800 #add stimuli and iti duration to response period duration
    df[['onset', 'response_time', 'duration']] = df[['onset', 'response_time', 'duration']].applymap(lambda x: x / 1000)
    df
    
    # break up tables for each subject
    subjects = df['Subject'].unique()
    
    subjects.sort() # might not need this anymore since we read in sub nums from a dict
    print("Total subjects: " + str(len(subjects)))
    
    for subj in subjects: 
        df0 = df[(df['Subject'] == subj)].reset_index(drop=True)
    
        # error checking
        for x in range(len(df0['response_time'].values)):
            if np.isnan(df0['resp'].iloc[x]) and df0['accuracy'].iloc[x] == 0: #if RT is blank and accuracy is 0 reset RT to be n/a indicating no response
                df0['response_time'].iloc[x] = 'n/a'
            elif np.isnan(df0['resp'].iloc[x]) and df0['accuracy'].iloc[x] == 1: #if RT is blank and accuracy is 1 there is an error in e-prime
                df0['response_time'].iloc[x] = 'err'
                df0['accuracy'] = 'err'


      # calculate onset time
        init = df0['onset'][0]
        df0[['onset']] = df0[['onset']].applymap(lambda x: x-init)
        # ignore warning, meant for modifying the original df
        # since we have a new df object, don't need to worry
        pd.options.mode.chained_assignment = None # removes the warning message

    
        # drop extra columns, rearrange and add in stim columns
        #df0 = df0.drop(columns=['Subject', 'cresp', 'resp', 'ft'])
        df0 = df0[['onset', 'duration', 'trial_type', 'accuracy', 'response_time']]
        stims = pd.read_csv(stim)
        df0 = pd.concat([df0, stims],axis=1)
    
        # replace NaN values with n/a
        for col in list(df0):
            df0[col] = df0[col].replace(np.nan, 'n/a')
        
        # reference sub_map dict first to figure out correct subject number
        sub_num = sub_map[str(subj)]
            
        # get new bids subject number
        if sub_num < 10:
            new_subj = '00' + str(sub_num)
        elif sub_num < 100:
            new_subj = '0' + str(sub_num)
        else:
            new_subj = str(sub_num)
    
        # save to tsv file
        fname = bidpath+'bids/sub-{}/ses-{}/func/sub-{}_ses-{}_task-{}{}_run-{}_events.tsv'.format(new_subj, trial, new_subj, trial, modality, task, run)
        # use --pretend flag to see what files will be made
        # need to implement better flag checking
        if len(sys.argv)>1 and sys.argv[1] == '--pretend':
            print(fname)
        else:
            df0.to_csv(fname, sep='\t', index=False)
    
