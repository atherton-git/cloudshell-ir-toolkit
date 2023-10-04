#!/bin/bash

# Download and unzip EvtxECmd
curl -o ./tmp/EvtxECmd.zip "https://f001.backblazeb2.com/file/EricZimmermanTools/net6/EvtxECmd.zip"
unzip ./tmp/EvtxECmd.zip -d ./tmp/EvtxECmd/
mkdir -p ./tools/; mkdir -p ./tools/evtx_explorer/
mv "./tmp/EvtxECmd/EvtxECmd/"* ./tools/evtx_explorer/
rm -r "./tmp/EvtxECmd/"

# Download and extract dotnet runtime
curl -o ./tmp/dotnet-runtime-6.0.0-linux-x64.tar.gz "https://download.visualstudio.microsoft.com/download/pr/0ce1c34f-0d9e-4d9b-964e-da676c8e605a/7a6c353b36477fa84f85b2821f2350c2/dotnet-runtime-6.0.0-linux-x64.tar.gz"
tar -xzvf ./tmp/dotnet-runtime-6.0.0-linux-x64.tar.gz -C ./bin/dotnet-runtime-600/

echo "Setup for log-parse-toolkit has completed."
