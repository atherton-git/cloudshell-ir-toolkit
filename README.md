# Azure Cloud Shell Toolkit
```
        __                __     __         ____      _            __              ____   _ __ 
  _____/ /___  __  ______/ /____/ /_  ___  / / /     (_)____      / /_____  ____  / / /__(_) /_
 / ___/ / __ \/ / / / __  / ___/ __ \/ _ \/ / /_____/ / ___/_____/ __/ __ \/ __ \/ / //_/ / __/
/ /__/ / /_/ / /_/ / /_/ (__  ) / / /  __/ / /_____/ / /  /_____/ /_/ /_/ / /_/ / / ,< / / /_  
\___/_/\____/\__,_/\__,_/____/_/ /_/\___/_/_/     /_/_/         \__/\____/\____/_/_/|_/_/\__/
```
# Installation
This toolkit can be installed to any Azure Cloud Shell instance by running the following command from within a Cloud Shell instance:

```
git clone https://github.com/atherton-git/cloudshell-ir-toolkit.git /usr/csuser/clouddrive/cloudshell-ir-toolkit/ && /usr/csuser/clouddrive/cloudshell-ir-toolkit/initialise.sh
```
To launch the toolkit, type ```python ./launch.py``` from the directory ```/usr/csuser/clouddrive/cloudshell-ir-toolkit/```.

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

### <ins>Mounting Storage</ins>
- To make the transfer of files to and from the storage account more accessible, consider mounting as an SMB share in Windows.
- To to this:
    1. Browse to your storage account in Azure Portal.
    2. Click ```File Shares```.
    3. On the file share, click the meatball menu and select ```Connect```.
    4. Adjust the drive letter as required. Ensure ```Storage account key``` is selected.
    5. Click ```Show Script```.
    6. Copy this script and execute it with ```Windows Powershell ISE```.

### <ins>Tmux</ins>
- Azure Cloud Shell can sometimes time-out during the execution of a script. If this happens without a tmux session your progress will be lost.
- Tmux will allow you to reconnect to your previous session in the event of a time-out.
- As a basic guide; type ```tmux``` from shell to create and enter a tmux session.
- To reconnect to a tmux session, type ```tmux a```.

# Tools

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
1. Copy Windows Event Log files to ```/usr/csuser/clouddrive/cloudshell-ir-toolkit/_input/win/```.
2. Launch option 2 from the cloudshell-ir-toolkit.
3. Once processed, collect the output from ```/usr/csuser/clouddrive/cloudshell-ir-toolkit/_output/```.

### <ins>Log Parsing: Linux Timestamps</ins>
- Custom Python code used to parse Linux logs and translate their timestamp to a universally readable format.
- Processed logs are output to csv.

#### Usage
1. Copy Linux logs to ```/usr/csuser/clouddrive/cloudshell-ir-toolkit/_input/linux/```.
2. Launch option 3 from the cloudshell-ir-toolkit.
3. Once processed, collect the output from ```/usr/csuser/clouddrive/cloudshell-ir-toolkit/_output/```.

### <ins>Search: Free-text</ins>
- Custom Python code used to search cleartext files for strings that are specified by the user.
- Matches are exported to csv with the following column headers:
    - **File** (Source filename)
    - **Line Number** (Identifies the line on which the string was identified in case a manual review is required)
    - **Matched Line** (A full copy of the data on the corrosponding line)

#### Usage
1. Copy cleartext source files to any directory within ```/usr/csuser/clouddrive/cloudshell-ir-toolkit/_input/```.
2. Launch option 4 from the cloudshell-ir-toolkit.
3. Follow on-screen prompts, and provide string to be searched.
4. Once processed, collect the output from ```/usr/csuser/clouddrive/cloudshell-ir-toolkit/_output/```.

### <ins>Search: IPv4</ins>
- Custom Python code used to search cleartext files for IPv4 addresses.
- Can be set to include or exclude private IP addresses (RFC1918).
- Matches are exported to csv with the following column headers:
    - **File** (Source filename)
    - **Line Number**
    - **IPv4 Address** (The address identified in the search)
    - **Matched Line** (A full copy of the data on the corrosponding line)

#### Usage
1. Copy cleartext source files to any directory within ```/usr/csuser/clouddrive/cloudshell-ir-toolkit/_input/```.
2. Launch option 5 from the cloudshell-ir-toolkit.
3. Follow on-screen prompts.
4. Once processed, collect the output from ```/usr/csuser/clouddrive/cloudshell-ir-toolkit/_output/```.

### <ins>Decode: QR codes</ins>
- Uses a library called PyBoof to analyse image files that contain QR Codes.
- The payload of the QR code is printed to console. (E.g. Phishing URL's).

#### Usage
1. Copy QR codes (in .png, .jpg, or .jpeg format) to ```/usr/csuser/clouddrive/cloudshell-ir-toolkit/_input/qrcodes/```
2. Launch option 5 from the cloudshell-ir-toolkit
3. Results will be printed to the active shell/terminal
