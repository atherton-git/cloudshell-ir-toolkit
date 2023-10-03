#!/bin/bash

# Define the cloud drive directory
cloud_drive="/usr/csuser/clouddrive"

# Clone the IR Toolkit Repository
if git clone https://github.com/atherton-git/incident-response-toolkit.git "$cloud_drive"; then
    echo "IR Toolkit repository cloned successfully."
else
    echo "Failed to clone IR Toolkit repository."
    exit 1
fi

# Download and unzip EvtxECmd
evtx_url="https://f001.backblazeb2.com/file/EricZimmermanTools/net6/EvtxECmd.zip"
if curl -o "$cloud_drive/log-parse-toolkit/tmp/EvtxECmd.zip" "$evtx_url" && unzip "$cloud_drive/log-parse-toolkit/tmp/EvtxECmd.zip" -d "$cloud_drive/log-parse-toolkit/tmp/EvtxECmd/"; then
    mkdir -p "$cloud_drive/log-parse-toolkit/tools/evtx_explorer/"
    mv "$cloud_drive/log-parse-toolkit/tmp/EvtxECmd/EvtxECmd/"* "$cloud_drive/log-parse-toolkit/tools/evtx_explorer/"
    rm -r "$cloud_drive/log-parse-toolkit/tmp/EvtxECmd/"
    echo "EvtxECmd downloaded and extracted successfully."
else
    echo "Failed to download and extract EvtxECmd."
    exit 1
fi

# Download and extract .NET runtime
dotnet_url="https://download.visualstudio.microsoft.com/download/pr/0ce1c34f-0d9e-4d9b-964e-da676c8e605a/7a6c353b36477fa84f85b2821f2350c2/dotnet-runtime-6.0.0-linux-x64.tar.gz"
if curl -o "$cloud_drive/log-parse-toolkit/tmp/dotnet-runtime-6.0.0-linux-x64.tar.gz" "$dotnet_url" && tar -xzvf "$cloud_drive/log-parse-toolkit/tmp/dotnet-runtime-6.0.0-linux-x64.tar.gz" -C "$cloud_drive/log-parse-toolkit/bin/dotnet-runtime-600/"; then
    echo ".NET runtime downloaded and extracted successfully."
else
    echo "Failed to download and extract .NET runtime."
    exit 1
fi

echo "Setup for log-parse-toolkit has completed."
