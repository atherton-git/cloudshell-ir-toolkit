#!/bin/bash

# Get the current directory
CURRENT_DIR="$PWD"

# Download and unzip EvtxECmd
curl -o "$CURRENT_DIR/tmp/EvtxECmd.zip" "https://f001.backblazeb2.com/file/EricZimmermanTools/net6/EvtxECmd.zip"
unzip "$CURRENT_DIR/tmp/EvtxECmd.zip" -d "$CURRENT_DIR/tmp/EvtxECmd/"
mkdir -p "$CURRENT_DIR/tools/"; mkdir -p "$CURRENT_DIR/tools/evtx_explorer/"
mv "$CURRENT_DIR/tmp/EvtxECmd/EvtxECmd/"* "$CURRENT_DIR/tools/evtx_explorer/"
rm -r "$CURRENT_DIR/tmp/EvtxECmd/"

# Download and extract dotnet runtime
curl -o "$CURRENT_DIR/tmp/dotnet-runtime-6.0.0-linux-x64.tar.gz" "https://download.visualstudio.microsoft.com/download/pr/0ce1c34f-0d9e-4d9b-964e-da676c8e605a/7a6c353b36477fa84f85b2821f2350c2/dotnet-runtime-6.0.0-linux-x64.tar.gz"
tar -xzvf "$CURRENT_DIR/tmp/dotnet-runtime-6.0.0-linux-x64.tar.gz" -C "$CURRENT_DIR/bin/dotnet-runtime-600/"

echo "Setup for log-parse-toolkit has completed."
