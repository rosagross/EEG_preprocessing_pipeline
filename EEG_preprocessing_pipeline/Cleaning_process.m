% CLEANING the data from artifacts and noisy channels
eeglabpath = 'C:\Program Files\MATLAB\eeglab2020_0'
eeglab;

%%
% Enter the pathname, where you saved the downsampled and (high/lowpass)
% filtered the data
downsampled_data_path = "C:\Users\rosah\Desktop\Rosas Unikrams\6th semester from Asus\" ...
                        + "Parkinson study project\Thesis things\EEG_feelSpace\" ...
                        + "EEG_data_feelSpace\CNT_DownsampledAndFiltered";
cd(downsampled_data_path);
subjectID = '16'; % Choose subject data that you want to clean
filename = ['ID' subjectID '.set'];

% Load existing data
eeg_cnt = pop_loadset(filename);
%% 

% Apply notch filter to remove 50Hz 


% look up location of channels and change location of VEOG from right to
% left
eeg_cnt = pop_chanedit(eeg_cnt, 'lookup', fullfile(eeglabpath,'plugins/dipfit3.4/standard_BESA/standard-10-5-cap385.elp'));

% Deblanking
x=size(eeg_cnt.event);
for t=1:max(x)
    eeg_cnt.event(t).type = deblank(eeg_cnt.event(t).type);
end

eeg_cnt.preprocessing = [eeg_cnt.preprocessing 'Deblanked, '];

%deleting unused channels for I amplifier 
eeg_cnt = pop_select(eeg_cnt, 'nochannel', {'BIP2' 'BIP3' 'BIP4' 'AUX1' ...
                                            'AUX2' 'AUX3' 'AUX4'}); 
%%
% Save to use later before interpolation (only have to do that for one
% participant since we use the same electrodes for all of them)
full_channels_locs = eeg_cnt.chanlocs;
save('64_channels.mat', 'full_channels_locs')

% Re-reference data since we removed electrodes
eeg_cnt = pop_reref( eeg_cnt, []);
eeg_cnt.preprocessing = [eeg_cnt.preprocessing 'Re-referenced 1, '];

% Plot the signal and go through the channels. Write down which one to
% reject
eegplot(eeg_cnt.data,'srate',eeg_cnt.srate,'eloc_file',eeg_cnt.chanlocs,'events',eeg_cnt.event)

%%
% Reject noisy/broken electrodes
channels_to_reject = {'T8'}; % enter here channels to reject
eeg_cnt = pop_select(eeg_cnt, 'nochannel', channels_to_reject);
eeg_cnt.preprocessing = [eeg_cnt.preprocessing 'ChannelReject,'];

% Save file without noisy channels 
pop_editset(eeg_cnt, 'setname',eeg_cnt);
eeg_cnt = pop_saveset(eeg_cnt, 'filename',['removed_channels_' filename]);
% Save name of rejected channels
save([subjectID '_channels_to_reject.mat'],'channels_to_reject')

%%
% Remove artifacts from the data

eegplot(eeg_cnt.data,'command','rej=TMPREJ;','srate',eeg_cnt.srate,'eloc_file',eeg_cnt.chanlocs,'events',eeg_cnt.event);



tmprej = eegplot2event(rej, -1);
eeg_cnt = eeg_eegrej(eeg_cnt,tmprej(:,[3 4]));
reject_array = tmprej(:,[3 4])

% ID 16
% 335 - 429
% 1044 - 1224
% 1841 - 1921
% 2544 - 2641
% 

% ID 15
% 335 - 429
% 754 - 774
% 1076 - 1344
% 1636 - 1838
% 1851 - 2375
breaks = [335 429; 1044 1224; 1841 1921; 2544 2641];
reject_array = cat(1, reject_array, breaks)
sorted = sort(reject_array)

save([subjectID '_times_to_reject.mat'],'reject_array')
eeg_cnt = eeg_checkset(eeg_cnt,'makeur');

% Save file with removed time points of noisy parts
pop_editset(eeg_cnt, 'setname',eeg_cnt);
eeg_cnt = pop_saveset(eeg_cnt, 'filename',['removed_times_' filename]);

% Plot to check if times were removed correctly
eegplot(eeg_cnt.data,'srate',eeg_cnt.srate,'eloc_file',eeg_cnt.chanlocs,'events',eeg_cnt.event)

%%
% Apply ICA (File has to be cleaned already!)
subjectID = '16'; % Choose subject data that you want to apply ICA 
filename = ['removed_times_ID' subjectID '.set'];

% Load existing data
eeg_cnt = pop_loadset(filename);

eeg_cnt_tmp = pop_eegfiltnew(eeg_cnt, 2, []);  
% remove low frequency to receive de
eeg_cnt_tmp = pop_runica(eeg_cnt, 'icatype', 'runica');

eeg_cnt_tmp2 = eeg_cnt_tmp;


%EPOCH %%%
window=[-0.2 .6];
[eeg_cnt_tmp2 indices] = pop_epoch( eeg_cnt_tmp, {'1' '3' '5' '7' '9' '11' '13' '14'}, window, 'epochinfo', 'yes');
eeg_cnt_tmp2.orig_indices = indices;

% Remove baseline
eeg_cnt_tmp2 = pop_rmbase( eeg_cnt_tmp2, [-199 0]);

% Exploring and labeling ICA components
EEG = eeg_cnt_tmp2;
EEG = iclabel(EEG);   
pop_viewprops(EEG, 0)
pop_selectcomps(EEG);

% Finding components that we selected and remove them
%reject selected components
comps_to_rej = find(EEG.reject.gcompreject);
eeg_cnt = pop_subcomp( eeg_cnt_tmp);

%%
pop_plotdata(EEG)

pop_eegplot(EEG, 0)
