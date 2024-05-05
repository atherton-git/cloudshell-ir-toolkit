#!/bin/bash

# Define the toolkit directory
toolkit_dir="/usr/csuser/clouddrive/cloudshell-ir-toolkit"

# Function to calculate hash and compare with expected hash
check_hash() {
    file_path=$1
    expected_hash=$2

    # Check if the file exists
    if [ ! -f "$file_path" ]; then
        echo "WARNING: File not found: $file_path"
        return
    fi

    # Calculate the file hash
    actual_hash=$(sha256sum "$file_path" | awk '{print $1}')

    # Compare the calculated hash with the expected hash
    if [ "$actual_hash" != "$expected_hash" ]; then
        echo "WARNING: File hash mismatch for $file_path"
        echo "Expected file hash: $expected_hash"
        echo "Actual file hash  : $actual_hash"
        read -p "Do you want to proceed at your own risk? (y/n): " -r
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            echo "Extracting file..."
        else
            echo "Aborting setup."
            exit 1
        fi
    else
        echo "File hash check passed for $file_path"
    fi
}

# EvtxECmd Installation
curl -o "$toolkit_dir/tmp/EvtxECmd.zip" "https://f001.backblazeb2.com/file/EricZimmermanTools/net6/EvtxECmd.zip"
evtxecmd_expected_hash="e1b4a5f9b09eca3c057cdc2d0ed1a28fe0c24dc90f9f68b7e0572e373dce86a6"
check_hash "$toolkit_dir/tmp/EvtxECmd.zip" "$evtxecmd_expected_hash"
unzip "$toolkit_dir/tmp/EvtxECmd.zip" -d "$toolkit_dir/tmp/EvtxECmd/"
mv "$toolkit_dir/tmp/EvtxECmd/EvtxECmd/"* "$toolkit_dir/bin/evtx_explorer/"
rm -r "$toolkit_dir/tmp/EvtxECmd/"

# bstrings Installation
curl -o "$toolkit_dir/tmp/bstrings.zip" "https://f001.backblazeb2.com/file/EricZimmermanTools/net6/bstrings.zip"
bstrings_expected_hash="1521031bab2843757bb701b75741a24154965ba219a57cbfefddb792c6d5b301"
check_hash "$toolkit_dir/tmp/bstrings.zip" "$bstrings_expected_hash"
unzip "$toolkit_dir/tmp/bstrings.zip" -d "$toolkit_dir/tmp/bstrings/"
mv "$toolkit_dir/tmp/bstrings/bstrings/"* "$toolkit_dir/bin/bstrings/"
rm -r "$toolkit_dir/tmp/bstrings/"

# Download dotnet runtime
curl -o "$toolkit_dir/tmp/dotnet-runtime-6.0.0-linux-x64.tar.gz" "https://download.visualstudio.microsoft.com/download/pr/0ce1c34f-0d9e-4d9b-964e-da676c8e605a/7a6c353b36477fa84f85b2821f2350c2/dotnet-runtime-6.0.0-linux-x64.tar.gz"

# Check the integrity of dotnet-runtime-6.0.0-linux-x64.tar.gz
dotnet_expected_hash="1a4076139944f3b16d9a0fc4841190cf060a9d93ebc13330821a2e97f6d4db91"
check_hash "$toolkit_dir/tmp/dotnet-runtime-6.0.0-linux-x64.tar.gz" "$dotnet_expected_hash"

# Extract dotnet runtime
tar -xzvf "$toolkit_dir/tmp/dotnet-runtime-6.0.0-linux-x64.tar.gz" -C "$toolkit_dir/bin/dotnet-runtime-600/"

# Install Python modules
yes | pip install pandas
yes | pip install pyboof
yes | pip install numpy
yes | pip install pyarrow

echo "Setup has completed."
