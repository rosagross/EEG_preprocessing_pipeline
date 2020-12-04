% CLEANING the data from artifacts and noisy channels
eeglabpath = 'C:\Program Files\MATLAB\eeglab2020_0'
eeglab;

%%
% Load existing data
downsampled_data_path = 'C:\Users\rosah\Desktop\Rosas Unikrams\6th semester from Asus\Parkinson study project\Thesis things\EEG_feelSpace\EEG_data_feelSpace\CNT_DownsampledAndFiltered'
cd(downsampled_data_path)
subjectID = '15'; % Choose subject data that you want to clean
eeg_cnt = pop_loadset('ID15.set');
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
eeg_cnt = pop_select(eeg_cnt, 'nochannel', {'BIP2' 'BIP3' 'BIP4' 'AUX1' 'AUX2' 'AUX3' 'AUX4'}); % measurements with one amplifier
%%
% Plot the signal and go through the channels. Write down which one to
% reject
eegplot(eeg_cnt.data,'srate',eeg_cnt.srate,'eloc_file',eeg_cnt.chanlocs,'events',eeg_cnt.event)

% save to use later before interpolation (only have to do that for one
% participant since we use the same electrodes for all of them)
full_channels_locs = eeg_cnt.chanlocs;
save('64_channels.mat', 'full_channels_locs')

% Re-reference data since we removed electrodes
eeg_cnt = pop_reref( eeg_cnt, []);
eeg_cnt.preprocessing = [eeg_cnt.preprocessing 'Re-referenced 1, '];

%%
% Reject noisy/broken electrodes
channels_to_reject = {'Fp2'}; % enter here channels to reject
eeg_cnt = pop_select(eeg_cnt, 'nochannel', channels_to_reject);

