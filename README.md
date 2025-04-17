# robotic-hip-exoskeleton
### Exoskeleton for  BME 198 Senior Design Project With User Interface

## Description

Desktop application to support data collection for hip exoskeleton research. 
The app handles device connections, and real-time logging of IMU sensor data. Built with a user-friendly interface to streamline experimental trials, it lays the groundwork for future integration of EMG data to support adaptive control algorithms.



## Files
kqExoskeletonIO: Device communication protocol file

Sample: Example to make the device's leg rods swing crosswise. Ensure there is enough space for the device's legs to move before running.

Sample_GUI: Runs on a PC, with the same functionality as Sample but adds a graphical observation interface (requires the pyqtgraph library).

Data_Record: Records sensor data from the device and writes it to a CSV file.

Note: Since Windows is a non-real-time operating system, the communication frequency will be lower when running the script on Windows compared to Linux.


## How to Setup 
