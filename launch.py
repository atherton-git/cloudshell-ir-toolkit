import subprocess

clouddrive_dir = "/usr/csuser/clouddrive"

command = [
    f'./bin/dotnet-runtime-600/dotnet',
    f'./tools/evtx_explorer/EvtxECmd.dll',
    "-d", f'./_input/win/',
    "--csv", f'./_output/'
]

try:
    subprocess.run(command, check=True)
    print("Command executed successfully.")
except subprocess.CalledProcessError as e:
    print(f"Command failed with error code {e.returncode}: {e.stderr}")
except Exception as e:
    print(f"An error occurred: {str(e)}")
