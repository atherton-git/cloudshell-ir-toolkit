# Azure Cloud Shell Toolkit
```
        __                __     __         ____      _            __              ____   _ __ 
  _____/ /___  __  ______/ /____/ /_  ___  / / /     (_)____      / /_____  ____  / / /__(_) /_
 / ___/ / __ \/ / / / __  / ___/ __ \/ _ \/ / /_____/ / ___/_____/ __/ __ \/ __ \/ / //_/ / __/
/ /__/ / /_/ / /_/ / /_/ (__  ) / / /  __/ / /_____/ / /  /_____/ /_/ /_/ / /_/ / / ,< / / /_  
\___/_/\____/\__,_/\__,_/____/_/ /_/\___/_/_/     /_/_/         \__/\____/\____/_/_/|_/_/\__/
```
# Installation
## Cloud Shell
This toolkit can be installed to any Azure Cloud Shell instance by running the following command from within a Cloud Shell instance:

```
git clone https://github.com/atherton-git/cloudshell-ir-toolkit.git /usr/csuser/clouddrive/cloudshell-ir-toolkit/ && /usr/csuser/clouddrive/cloudshell-ir-toolkit/initialise.sh
```
To launch the toolkit, type ```python ./launch.py``` from the directory ```/usr/csuser/clouddrive/cloudshell-ir-toolkit/```.

## Windows
This toolkit can be installed to Windows by downloading the reposiitory as a zip file, and executing the ```initialise.ps1``` script.

## Ubuntu
The following command must be executed prior to installation on an Ubuntu VM:
```
sudo apt-get update && sudo apt-get upgrade -y && sudo apt-get install unzip -y && sudo apt install python-is-python3 -y && sudo apt install python3-pip -y && sudo apt install default-jre -y
```
This toolkit can be installed to Ubuntu by downloading the reposiitory as a zip file, and executing the ```initialise.sh``` script.

To launch the toolkit, type ```python ./launch.py``` from the installation directory.

# Prerequisites and Suggestions

### <ins>Storage Account</ins>
- You must have access to an Azure storage account from which to operate Cloud Shell

### <ins>Increasing Storage Quota</ins>
- By default, your fileshare will be provisioned with 6 GB of storage.
- To increase this quota:
    1. Browse to your storage account in Azure Portal.
    2. Click ```File Shares```
    3. On the file share, click the meatball menu and select ```Edit quota```.
    4. Set the quota to a suggested 100 GB, and confirm with ```OK```.

### <ins>Mounting Storage to Windows</ins>
- To make the transfer of files to and from the storage account more accessible, consider mounting as an SMB share in Windows.
- To to this:
    1. Browse to your storage account in Azure Portal.
    2. Click ```File Shares```.
    3. On the file share, click the meatball menu and select ```Connect```.
    4. Adjust the drive letter as required. Ensure ```Storage account key``` is selected.
    5. Click ```Show Script```.
    6. Copy this script and execute it with ```Windows Powershell ISE```.

### <ins>Mounting Storage to Ubuntu</ins>
- To make the transfer of files to and from the storage account more accessible, consider mounting as an SMB share in Ubuntu.
- To to this:
    1. Browse to your storage account in Azure Portal.
    2. Click ```File Shares```.
    3. On the file share, click the meatball menu and select ```Connect```.
    4. Select the 'Linux' tab.
    5. Click ```Show Script```.
    6. Copy this script to your clipboard.
    7. Create a bash script on the VM using Vim by typing ```vim mount.sh```.
    8. Paste the script to the VM using the Vim text editor (Using Nano leads to a formatting issue)
    9. Make the script executable by tying ```chmod +x mount.sh``` and execute it by typing ```./mount.sh```.
    10. You can now browse to this storage using ```cd /mnt/{storage_account_name}/```.

### <ins>Tmux</ins>
- Azure Cloud Shell can sometimes time-out during the execution of a script. If this happens without a tmux session your progress will be lost.
- Tmux will allow you to reconnect to your previous session in the event of a time-out.
- As a basic guide; type ```tmux``` from shell to create and enter a tmux session.
- To reconnect to a tmux session, type ```tmux a```.

#Tools

### <ins>Log Parsing: Windows Events (EvtxECmd)</ins>
- This tool utilises EvtxExplorer to parse Windows Event Log files (.evtx), and output to a csv file.
- The CSV export format in EvtxECmd normalizes the event record into standard fields from the common area of the XML payload, such as Computer, Channel, EventID, Level, TimeCreated.
- The native XML data structure of Windows Events Logs can lead to analytical issues, because different event ID's can have different payloads.
- EvtxECmd uses a map to convert the customized data into several standardized fields in the CSV (and json) data. These include:
    - **UserName:** user and/or domain info as found in various event IDs
    - **RemoteHost:** IP address and/or host name information found in event IDs
    - **ExecutableInfo:** used for things like process command line, scheduled task, info from service install, etc.
    - **PayloadData1-6**
- Map files are then used to convert the EventData (unique part of an event ID) to a more standardised format.
- This allows you to see all events in line with all other events, regardless of where the logs came from and what the payload is.

#### Usage
1. Copy Windows Event Log files to ```/{toolkit_directory}/_input/win/```.
2. Choose the relevant option from the cloudshell-ir-toolkit menu.
3. Once processed, collect the output from ```/{toolkit_directory}/_output/```.

### <ins>Log Parsing: Linux Timestamps</ins>
- Custom Python code used to parse Linux logs and translate their timestamp to a universally readable format.
- Processed logs are output to csv.

#### Usage
1. Copy Linux logs to ```/{toolkit_directory}/_input/linux/```.
2. Choose the relevant option from the cloudshell-ir-toolkit menu.
3. Once processed, collect the output from ```/{toolkit_directory}/_output/```.

### <ins>Convert: Documents to txt</ins>
- This tool leverages Apache Tika to convert various filetypes to plaintext (.txt) which reside in ```/{toolkit_directory}/_input/```.
- **Note:** This process removes the original file, so if partially destructive. Ensure you have a copy of the data.

#### Usage
1. Choose the relevant option from the cloudshell-ir-toolkit menu.
2. Document files (currently pdf, docx, xlsx, pptx, msg) within the ```/_input/``` directory will be converted to txt in place.

### <ins>Search: Wordlist</ins>
- Custom Python code used to search cleartext files for strings that are specified in ```/{toolkit_directory}/input_wordlist.txt```.
- Matches are exported to csv with the following column headers:
    - **search_query** (The specific string that has been matched)
    - **source_file** (The directory and name of the file which contained the match)
    - **source_row_number** (Identifies the line on which the string was identified, in case a manual review is required)
    - **source_data** (A full copy of the data on the corrosponding line)

#### Usage
1. Copy cleartext source files to any directory within ```/{toolkit_directory}/_input/```.
2. Choose the relevant option from the cloudshell-ir-toolkit menu.
3. Once processed, collect the output from ```/{toolkit_directory}/_output/```.
4. The filename will contain a timestamp, and end with the suffix "_wordlist".

###<ins>Search: RegEx list</ins>
- Custom Python code used to search cleartext files for strings that are specified in ```/{toolkit_directory}/input_regex.txt```.
- Matches are exported to csv with the following column headers:
    - **regex_pattern** (The specific regex that has been matched)
    - **pattern_description** (The description of the regex that has been matched)
    - **source_file** (The directory and name of the file which contained the match)
    - **source_row_number** (Identifies the line on which the string was identified, in case a manual review is required)
    - **source_data** (A full copy of the data on the corrosponding line)

#### Usage
1. Copy cleartext source files to any directory within ```/{toolkit_directory}/_input/```.
2. Choose the relevant option from the cloudshell-ir-toolkit menu.
3. Once processed, collect the output from ```/{toolkit_directory}/_output/```.
4. The filename will contain a timestamp, and end with the suffix "_regex".

### <ins>Search: Free-text</ins>
- Custom Python code used to search cleartext files for strings that are specified by the user.
- Matches are exported to csv with the following column headers:
    - **source_file** (Source filename)
    - **source_row** (Identifies the line on which the string was identified in case a manual review is required)
    - **source_data** (A full copy of the data on the corrosponding line)

#### Usage
1. Copy cleartext source files to any directory within ```/{toolkit_directory}/_input/```.
2. Choose the relevant option from the cloudshell-ir-toolkit menu.
3. Follow on-screen prompts, and provide string to be searched.
4. Once processed, collect the output from ```/{toolkit_directory}/_output/```.
5. The filename will contain a timestamp, and end with the suffix "_freetext".

### <ins>Search: IPv4</ins>
- Custom Python code used to search cleartext files for IPv4 addresses.
- Can be set to include or exclude private IP addresses (RFC1918).
- Matches are exported to csv with the following column headers:
    - **source_file** (Source filename)
    - **source_row**
    - **matched_ipv4** (The address identified in the search)
    - **source_data** (A full copy of the data on the corrosponding line)

#### Usage
1. Copy cleartext source files to any directory within ```/{toolkit_directory}/_input/```.
2. Choose the relevant option from the cloudshell-ir-toolkit menu.
3. Follow on-screen prompts.
4. Once processed, collect the output from ```/{toolkit_directory}/_output/```.
5. The filename will contain a timestamp, and end with the suffix "_ipv4_addresses"

### <ins>Decode: QR codes</ins>
- Uses a library called PyBoof to analyse image files that contain QR Codes.
- The payload of the QR code is printed to console. (E.g. Phishing URL's).

#### Usage
1. Copy QR codes (in .png, .jpg, or .jpeg format) to ```/{toolkit_directory}/_input/qrcodes/```
2. Choose the relevant option from the cloudshell-ir-toolkit menu.
3. Results will be printed to the active shell/terminal
