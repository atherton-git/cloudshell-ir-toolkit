import subprocess

clouddrive_dir = "/usr/csuser/clouddrive"

def process_evtx_files():
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

def process_all_inputs():
    # Add code to process all inputs here
    print("Processing all inputs...")

def main():
    while True:
        print("Options:")
        print("1) Process .evtx files")
        print("2) Process all inputs")
        print("3) Quit")

        choice = input("Enter your choice: ")

        if choice == '1':
            process_evtx_files()
        elif choice == '2':
            process_all_inputs()
        elif choice == '3':
            break
        else:
            print("Invalid choice. Please enter a valid option.")

if __name__ == "__main__":
    main()
