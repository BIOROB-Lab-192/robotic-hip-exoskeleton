%% Information
% Post processing script for Khoa Vu's Master Project
% Author: Khoa Vu
% Advisor: Dr. Lin Jiang
% -------------------------------------------------------------------------
% Each section of the script contains the code to be run sequentially. Each
% section description contain the information regarding when the script
% shall be run. Please read through the script description to get
% familiar with all steps involved in this experiment.
%
% Make sure the MATLAB working directory is where the two Simulink models
% are stored. 
%
% Please close all other applications currently running on the computer
% because the Simulink files require memory avoid losing data recorded.
%
% Please contact me, Khoa Vu, at (408) 313-7738 should you have any
% question during the experiment or post processing.
% -------------------------------------------------------------------------

%% Experiment Setup
% Run this section prior to starting the Simulink simulations. Please fill
% in the appropriate information regarding saving directory, task # run in
% the experiment, and test subject ID. Refer to the "Participants.txt" to
% enter the test subject id correctly.
%
% file_name example: KHOAPROJECT_1_1_1_Data
%
% If the data recording is used for machine learning training (no haptic
% feedback model involved), save it to "Data" folder. This rule applies
% similarly for result files, if used haptic feedback model, save it to
% "Result" folder.
%
% Fill in this section first before starting the Simulink files. Start the
% Simulink file 'emg' first, then immediately start 'omni_3Dworld' when 
% it's available. It's recommended to have both windows open side by side 
% for quick access. 

task_number = ('1');
saving_dir_processed = ('"C:\Downloads"');
processed_file_name = ('Processed.xlsx');
saving_dir_raw = ('"C:\Downloads"');
raw_file_name = ('RawData.xlsx');

%% Enter peak contraction number of each muscle
peak_bicep = 624;
peak_tricep = 539;
peak_forearm = 418;
%% Stop the two Simulink simulations at the same time
% This section is to be run after all the tasks have been completed and
% the haptic pen has been put back to the starting location (location 8 
% on the acrylic board). 

simulink.compiler.stopSimulation('omni_3Dworld')
simulink.compiler.stopSimulation('emg_Original')

%% Synchronize data files and machine learning prep
% The overlapped period at which both Simulink files are actively recording
% data corresponds to the length of the omni_3Dworld's output. This means
% that the emg's output needs to be truncated. 

lag = length(emglist)-length(endeff_pos);

% Normalize emg data to the peak of data set
post_emglist = emglist(lag+1:end,:); % Raw emg list
processed_emglist = ones(size(post_emglist)); % Pre-allocate for speed

for i = 2:4
    if i == 1
        processed_emglist(:,i) = post_emglist(:,i)/peak_forearm;
    elseif i == 2
        processed_emglist(:,i) = post_emglist(:,i)/peak_bicep;
    else
        processed_emglist(:,i) = post_emglist(:,i)/peak_tricep;
    end
end

processed_sensor_data = [processed_emglist imu_acc(lag+1:end,:) ... 
    imu_gyr(lag+1:end,:)  imu_orientation(lag+1:end,:)];  

number_of_datapoints = length(processed_sensor_data);
task_col = ones(number_of_datapoints,1)*str2double(task_number);

% Calculate the distance between each data point to the ideal line
task_id = str2double(task_number);

deviation = shortest_distance(task_id,endeff_pos); 

vibration_factor = ones(number_of_datapoints,1);

for i = 1:length(deviation)-1
    if deviation(i) <= 0.25 
        vibration_factor(i) = 1;
    elseif deviation(i) <= 0.6
        vibration_factor(i) = 2;
    else 
        vibration_factor(i) = 3;
    end
end

processed_combined_data = [endeff_pos deviation processed_sensor_data(:,2:end)...
    task_col vibration_factor];

raw_data = [endeff_pos post_emglist(:,2:end) imu_acc(lag+1:end,:) ...
    imu_gyr(lag+1:end,:) imu_orientation(lag+1:end,:) task_col];

raw_var_names = ["timestamp","pos_x","pos_y","pos_z", "raw_forearm",...
    "raw_bicep", "raw_tricep", "acc_x","acc_y","acc_z","gyro_x",...
    "gyro_y","gyro_z", "euler_x", "euler_y", "euler_z", "task_id"];

processed_var_names = ["timestamp","pos_x","pos_y","pos_z","distance","norm_forearm","norm_bicep",...
    "norm_tricep","acc_x","acc_y","acc_z","gyro_x","gyro_y","gyro_z",...
    "euler_x", "euler_y", "euler_z", "task_id","haptic level"];

% Save to spreadsheet
write_dir_processed = strcat(saving_dir_processed,processed_file_name);
writematrix(processed_var_names,write_dir_processed);
writematrix(processed_combined_data,write_dir_processed,'WriteMode','append');

write_dir_raw = strcat(saving_dir_raw,raw_file_name);
writematrix(raw_var_names,write_dir_raw);
writematrix(raw_data,write_dir_raw,'WriteMode','append');

