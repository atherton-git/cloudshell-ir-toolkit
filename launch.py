import subprocess
from scripts.process_evtx import process_evtx_files

clouddrive_dir = "/usr/csuser/clouddrive"

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
            process_evtx_files(clouddrive_dir)
        elif choice == '2':
            process_all_inputs()
        elif choice == '3':
            break
        else:
            print("Invalid choice. Please enter a valid option.")

if __name__ == "__main__":
    main()
