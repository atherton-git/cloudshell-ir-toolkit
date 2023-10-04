import subprocess
import os

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

def parse_linux_log_timestamps():
    # Run the parse_linux_datetime.py script in the same directory
    script_path = os.path.join(os.path.dirname(__file__), "parse_linux_datetime.py")
    try:
        subprocess.run(["python", script_path], check=True)
        print("Linux log timestamps parsed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Command failed with error code {e.returncode}: {e.stderr}")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

def main():
    while True:
        print("Options:")
        print("1) Process .evtx files")
        print("2) Parse Linux log timestamps")
        print("3) Process all inputs")
        print("4) Quit")

        choice = input("Enter your choice: ")

        if choice == '1':
            process_evtx_files()
        elif choice == '2':
            parse_linux_log_timestamps()
        elif choice == '3':
            process_all_inputs()
        elif choice == '4':
            break
        else:
            print("Invalid choice. Please enter a valid option.")

if __name__ == "__main__":
    main()
