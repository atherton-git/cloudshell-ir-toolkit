# Define the toolkit directory
$toolkit_dir = $PWD

# Function to calculate hash and compare with expected hash
function Check-Hash {
    param (
        [string]$file_path,
        [string]$expected_hash
    )

    # Check if the file exists
    if (-Not (Test-Path -Path $file_path)) {
        Write-Host "WARNING: File not found: $file_path"
        return $false
    }

    # Calculate the file hash
    $actual_hash = (Get-FileHash -Path $file_path -Algorithm SHA256).Hash

    # Compare the calculated hash with the expected hash
    if ($actual_hash -ne $expected_hash) {
        Write-Host "WARNING: File hash mismatch for $file_path"
        Write-Host "Expected file hash: $expected_hash"
        Write-Host "Actual file hash  : $actual_hash"
        $response = Read-Host "Do you want to proceed at your own risk? (y/n)"
        if ($response -ne 'y' -and $response -ne 'Y') {
            Write-Host "Aborting setup."
            exit 1
        } else {
            Write-Host "Extracting file..."
        }
    } else {
        Write-Host "File hash check passed for $file_path"
        return $true
    }
}

# Parse Command-Line Arguments
$installForAllUsers = $false
if ($args -contains '--all-users') {
    $installForAllUsers = $true
}

# Check for Admin Privileges if Necessary
if ($installForAllUsers) {
    $isAdmin = ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole] "Administrator")
    if (-Not $isAdmin) {
        Write-Host "Installing for all users requires administrative privileges. Please run the script as an administrator or remove the '--all-users' argument."
        exit 1
    }
}

# EvtxECmd Installation
function Install-EvtxECmd {
    $evtxecmd_url = "https://f001.backblazeb2.com/file/EricZimmermanTools/net6/EvtxECmd.zip"
    $evtxecmd_path = "$toolkit_dir\tmp\EvtxECmd.zip"
    $evtxecmd_expected_hash = "e1b4a5f9b09eca3c057cdc2d0ed1a28fe0c24dc90f9f68b7e0572e373dce86a6"

    Invoke-WebRequest -Uri $evtxecmd_url -OutFile $evtxecmd_path
    $hashCheck = Check-Hash -file_path $evtxecmd_path -expected_hash $evtxecmd_expected_hash
    if (-not $hashCheck) {
        Write-Host "EvtxECmd hash check failed. Exiting..."
        exit 1
    }

    Expand-Archive -Path $evtxecmd_path -DestinationPath "$toolkit_dir\tmp\EvtxECmd\"
    Move-Item -Path "$toolkit_dir\tmp\EvtxECmd\EvtxECmd\*" -Destination "$toolkit_dir\bin\evtx_explorer\"
    Remove-Item -Recurse -Force "$toolkit_dir\tmp\EvtxECmd\"
}

# Install Python
function Install-Python {
    # Check if Python 3.12.4 is already installed
    $installedVersion = & python --version 2>&1
    if ($installedVersion -match "Python 3.12.4") {
        Write-Host "Python 3.12.4 is already installed."
        return
    }

    $pythonUrl = "https://www.python.org/ftp/python/3.12.4/python-3.12.4-amd64.exe"
    $pythonHash = "F3DF1BE26CC7CBD8252AB5632B62D740"
    $pythonInstaller = "$env:TEMP\python.exe"

    Write-Host "Downloading Python installer..."
    try {
        Invoke-WebRequest -Uri $pythonUrl -OutFile $pythonInstaller
        $installerHash = (Get-FileHash -Path $pythonInstaller -Algorithm MD5).Hash
        if ($installerHash -ne $pythonHash) {
            Write-Host "Hash mismatch! Installer may have been tampered with. Exiting..."
            exit 1
        }
    } catch {
        Write-Host "Failed to download Python installer. Please check your internet connection and try again."
        exit 1
    }

    Write-Host "Installing Python..."
    try {
        $installAllUsersArg = if ($installForAllUsers) { "1" } else { "0" }
        Start-Process -FilePath $pythonInstaller -ArgumentList "/quiet InstallAllUsers=$installAllUsersArg PrependPath=1 Include_pip=1" -Wait
    } catch {
        Write-Host "Python installation failed: $_"
        exit 1
    }

    Write-Host "Cleaning up downloaded files..."
    Remove-Item -Path $pythonInstaller -Force
    Write-Host "Python installation complete!"

    # Install Python modules
    $pip_modules = @("pandas", "pyboof", "numpy", "pyarrow", "tika")
    foreach ($module in $pip_modules) {
        & "$env:localappdata\Programs\Python\Python312\python" -m pip install $module --break-system-packages
    }
}

# Install Java Runtime
function Install-Java {
    $url = "https://github.com/adoptium/temurin21-binaries/releases/download/jdk-21.0.3+9/OpenJDK21U-jre_x64_windows_hotspot_21.0.3_9.msi"
    $output = "$toolkit_dir\tmp\OpenJDK21U-jre_x64_windows_hotspot_21.0.3_9.msi"

    Write-Host "Downloading Java installer..."
    Invoke-WebRequest -Uri $url -OutFile $output

    $installerPath = $output

    Write-Host "Installing Java..."
    Start-Process -FilePath "msiexec.exe" -ArgumentList "/i `"$installerPath`" INSTALLLEVEL=1 /quiet" -Wait
    Write-Host "Java installation complete!"
}

# Function to install .NET Framework
function Install-DotNetFramework {
    $dotnet_url = "https://download.visualstudio.microsoft.com/download/pr/6b96c97d-9b8c-4141-a32a-5848d3369dbf/9972321cb7af5938fecdee2d8ebd72bb/dotnet-runtime-6.0.0-win-x64.zip"
    $dotnet_path = "$toolkit_dir\tmp\dotnet-runtime-6.0.0-win-x64.zip"
    $dotnet_expected_hash = "095C8284ACECB07532390FF8ABDEDCF4E2F39005A4C58BD51CB5661A8379A6F6"
    
    # Ensure the directory exists
    $dir = [System.IO.Path]::GetDirectoryName($dotnet_path)
    if (-Not (Test-Path -Path $dir)) {
        New-Item -ItemType Directory -Path $dir -Force
    }
    
    Invoke-WebRequest -Uri $dotnet_url -OutFile $dotnet_path
    Check-Hash -file_path $dotnet_path -expected_hash $dotnet_expected_hash
    Expand-Archive -Path $dotnet_path -DestinationPath "$toolkit_dir\bin\dotnet-runtime-600\" -Force
}

# Main script execution
Write-Host "Starting toolkit setup..."

# Execute functions
Install-EvtxECmd
Install-Python
Install-Java
Install-DotNetFramework

Write-Host "Toolkit setup complete. The script will exit in 10 seconds..."
Start-Sleep -Seconds 10
exit
