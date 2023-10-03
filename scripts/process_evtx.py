import subprocess

def process_evtx_files(clouddrive_dir):
    command = [
        f'{clouddrive_dir}/log-parse-toolkit_v0-1/bin/dotnet-runtime-600/dotnet',
        f'{clouddrive_dir}/log-parse-toolkit_v0-1/tools/evtx_explorer/EvtxECmd.dll',
        "-d", f'{clouddrive_dir}/_input/win/',
        "--csv", f'{clouddrive_dir}/_output/'
    ]

    try:
        subprocess.run(command, check=True)
        print("Command executed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Command failed with error code {e.returncode}: {e.stderr}")
    except Exception as e:
        print(f"An error occurred: {str(e)}")
