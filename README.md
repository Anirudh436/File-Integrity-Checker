# File-Integrity-Checker
Integrity checker using hash value monitoring


*COMPANY* : CODTECH IT SOLUTIONS

*NAME* : ANIRUDH ANILKUMAR

*INTERN ID* :  CT08VAI

*DOMAIN* : CYBER SECURITY AND ETHICAL HACKING

*DURATION* : 4 WEEKS

*MENTOR* : NEELA SANTHOSH

DESCRIPTION:

  The File Integrity Monitoring (FIM) tool is a Python-based application designed to track file modifications, additions, and deletions in a specified directory. By ensuring the integrity of files through cryptographic hash comparisons, the tool helps detect unauthorized or unintended file changes that could indicate security threats such as malware infections or unauthorized access attempts. 
  
  The FIM tool runs continuously in the background, monitoring all files within a user-specified directory. If a change is detected, the tool immediately notifies the user via a pop-up alert. This real-time notification system ensures that any suspicious activity is promptly addressed. The application is particularly valuable for security-sensitive environments where file integrity is critical.
  
*Features*:

  Baseline Creation and Verification: Captures an initial snapshot of file hashes and uses it for ongoing integrity checks.
  
  Real-Time Monitoring: Uses the watchdog library to track file changes as they occur.
  
  Hash-Based Detection: Computes SHA-256 hashes to validate file integrity against the stored baseline.
  
  User Notifications: Displays pop-up alerts using plyer when files are modified, added, or deleted.
  
  Interactive GUI: Utilizes Tkinter to prompt users for directory selection and monitoring configurations.
  
  Resilient Error Handling: Implements retry mechanisms for permission issues and prevents JSON corruption.
  
  Recursive Monitoring: Monitors all subdirectories within the selected directory to ensure comprehensive coverage.
  
*Installation Prerequisites*:

  Ensure you have Python 3.7+ installed on your system. A lower version means that some dependencies may be deprecated or      not function as intended.
  
  Dependencies required: watchdog, plyer, tkinter
  
  dependencies can be downloaded by using pip install dependency_name in the command prompt where python is active
  
*Usage*:

  RUN SCRIPT: Run script with python file_integrity_monitor.py
  
  CHOOSE BASELINE MODE: The tool will ask if you want to either create a new baseline or use an existing one.
    If a baseline does not exist, a new one will be created automatically.
    
  SELECT THE DIRECTORY TO MONITOR: A file selection dialog will appear, allowing you to choose a folder for monitoring.
  
  MONITORING BRGINS: The tool will continuously check for file modifications, new files, and deletions.
    Any detected change will trigger a real-time notification.
    
  STOPPING THE TOOL: Press CTRL + C in the terminal to stop monitoring.

Configuration:

  The tool stores baseline data in a file named baseline.json in the same directory as the script. This JSON file contains file paths and their corresponding SHA-256 hash values, serving as a reference for integrity verification. You can delete this file to reset monitoring, and a new one will be created upon the next execution.
  
  If the baseline.json file is corrupted, the tool automatically regenerates it to prevent monitoring failures.
  
  If no directory is selected, the user will be prompted to retry or exit the tool, ensuring monitoring cannot proceed without valid input.


Future Enhancements:

  Multi-directory support:Extend the monitoring capabilities to multiple directories simultaneously.
  
  Cloud Based Logging: Enable remote storage of changelogs for enhanced security and accessibility.
  
  User-defined exclusion rules: Allowing users to specify file types or paths to be ignored during monitoring.
  
  Command-line interface: Providing an alternative to GUI-based interaction for more advanced users
  
  
Acknowledgements:

This tool leverages open-source libraries such as watchdog, plyer, and Tkinter. Special thanks to the Python developer community for their contributions to these projects.


Output:

![Image](https://github.com/user-attachments/assets/fcce4cd9-86cf-4ae5-a2fb-e9be733b088a)

![Image](https://github.com/user-attachments/assets/8099e35a-5ef9-4406-b157-88b4a51425b5)

![Image](https://github.com/user-attachments/assets/34a12d74-f77e-47e3-a9e0-75f89c2c6887)
