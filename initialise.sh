#!/bin/bash

# Define the toolkit directory
toolkit_dir="/usr/csuser/clouddrive/cloudshell-ir-toolkit"

# Download and unzip EvtxECmd
curl -o "$toolkit_dir/tmp/EvtxECmd.zip" "https://f001.backblazeb2.com/file/EricZimmermanTools/net6/EvtxECmd.zip"
unzip "$toolkit_dir/tmp/EvtxECmd.zip" -d "$toolkit_dir/tmp/EvtxECmd/"
mv "$toolkit_dir/tmp/EvtxECmd/EvtxECmd/"* "$toolkit_dir/tools/evtx_explorer/"
rm -r "$toolkit_dir/tmp/EvtxECmd/"

# Download and extract dotnet runtime
curl -o "$toolkit_dir/tmp/dotnet-runtime-6.0.0-linux-x64.tar.gz" "https://download.visualstudio.microsoft.com/download/pr/0ce1c34f-0d9e-4d9b-964e-da676c8e605a/7a6c353b36477fa84f85b2821f2350c2/dotnet-runtime-6.0.0-linux-x64.tar.gz"
tar -xzvf "$toolkit_dir/tmp/dotnet-runtime-6.0.0-linux-x64.tar.gz" -C "$toolkit_dir/bin/dotnet-runtime-600/"

# Install Python modules
yes | pip install pandas
yes | pip install pyboof

echo "Setup has completed."
