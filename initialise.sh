#!/bin/bash

# Define the toolkit directory
toolkit_dir=$PWD

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

# Download dotnet runtime
curl -o "$toolkit_dir/tmp/dotnet-runtime-6.0.0-linux-x64.tar.gz" "https://download.visualstudio.microsoft.com/download/pr/0ce1c34f-0d9e-4d9b-964e-da676c8e605a/7a6c353b36477fa84f85b2821f2350c2/dotnet-runtime-6.0.0-linux-x64.tar.gz"
dotnet_expected_hash="1a4076139944f3b16d9a0fc4841190cf060a9d93ebc13330821a2e97f6d4db91"
check_hash "$toolkit_dir/tmp/dotnet-runtime-6.0.0-linux-x64.tar.gz" "$dotnet_expected_hash"
tar -xzvf "$toolkit_dir/tmp/dotnet-runtime-6.0.0-linux-x64.tar.gz" -C "$toolkit_dir/bin/dotnet-runtime-600/"

# Install Python modules
yes | pip install pandas --break-system-packages
yes | pip install pyboof --break-system-packages
yes | pip install numpy --break-system-packages
yes | pip install pyarrow --break-system-packages
yes | pip install tika --break-system-packages

echo "Setup has completed."
