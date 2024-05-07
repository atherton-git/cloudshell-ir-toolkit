#!/bin/bash

current_datetime=$(date +"%Y%m%d%H%M%S_wordlist.txt")
cloudshell_dir=$(dirname "$PWD")

$cloudshell_dir/bin/dotnet-runtime-600/dotnet $cloudshell_dir/bin/bstrings/bstrings.dll -q -d "$cloudshell_dir/_input/bstrings" --fs "$cloudshell_dir/input_bstrings.txt" -o "$cloudshell_dir/_output/$current_datetime"
