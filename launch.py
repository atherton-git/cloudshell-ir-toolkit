import subprocess
import os
from datetime import datetime

# Currently unused variable
clouddrive_dir = "/usr/csuser/clouddrive"

script_dir = os.path.dirname(os.path.abspath(__file__))

# Change the current working directory
os.chdir('scripts')

current_datetime = datetime.now().strftime("%Y%m%d%H%M%S")

def run_command(command, success_message):
    try:
        subprocess.run(command, check=True)
        print(success_message)
    except subprocess.CalledProcessError as e:
        print(f"Command failed with error code {e.returncode}: {e.stderr}")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

def process_evtx_files():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    bin_dir = os.path.join(script_dir, "bin")
    dotnet_dir = os.path.join(bin_dir, "dotnet-runtime-600", "dotnet")
    evtx_dir = os.path.join(bin_dir, "evtx_explorer", "EvtxECmd.dll")
    input_dir = os.path.join(script_dir, "_input", "win")
    output_dir = os.path.join(script_dir, "_output")
    command = [
        dotnet_dir,
        evtx_dir,
        "-d", input_dir,
        "--csv", output_dir
    ]
    run_command(command, "Command executed successfully.")

def search_wordlist():
    convert = input("Would you like to convert PDF/OpenXML (Microsoft Office) documents to text files? This is is a requirement for bstrings to parse these files (y/n): ").lower().strip()
    if convert == "y":
        os.system("python extract_openxml.py")
        print("OpenXML/PDF documents converted to text files successfully.")
    elif convert == "n":
        print("Skipping document conversion.")
    else:
        print("Invalid input. Skipping document conversion.")
    script_path = os.path.join(os.path.dirname(__file__), "scripts", "search_wordlist.sh")
    os.system(script_path)
    print("bstrings input searched for wordlist successfully. Please see '_output' directory for results.")

def search_regex():
    script_path = os.path.join(os.path.dirname(__file__), "scripts", "search_regex.py")
    run_command(["python", script_path], "RegEx list searched successfully.")

def parse_linux_log_timestamps():
    script_path = os.path.join(os.path.dirname(__file__), "scripts", "parse_linux_datetime.py")
    run_command(["python", script_path], "Linux log timestamps parsed successfully.")

def decode_qrcodes():
    script_path = os.path.join(os.path.dirname(__file__), "scripts", "decode_qrcodes.py")
    run_command(["python", script_path], "QR codes decoded successfully. Please see '_output' directory for results.")

def search_freetext():
    script_path = os.path.join(os.path.dirname(__file__), "scripts", "search_freesearch.py")
    run_command(["python", script_path], "Free text search completed. Please see '_output' directory for results.")

def search_ipv4():
    script_path = os.path.join(os.path.dirname(__file__), "scripts", "search_ipv4.py")
    run_command(["python", script_path], "IPv4 search completed. Please see '_output' directory for results.")

def main():
	print("""
        __                __     __         ____      _            __              ____   _ __ 
  _____/ /___  __  ______/ /____/ /_  ___  / / /     (_)____      / /_____  ____  / / /__(_) /_
 / ___/ / __ \/ / / / __  / ___/ __ \/ _ \/ / /_____/ / ___/_____/ __/ __ \/ __ \/ / //_/ / __/
/ /__/ / /_/ / /_/ / /_/ (__  ) / / /  __/ / /_____/ / /  /_____/ /_/ /_/ / /_/ / / ,< / / /_  
\___/_/\____/\__,_/\__,_/____/_/ /_/\___/_/_/     /_/_/         \__/\____/\____/_/_/|_/_/\__/  
                                                                                               
	""")
	while True:
		print("Options:")
		print("1) Quit")
		print("2) Log Parsing: Windows Events (EvtxECmd)")
		print("3) Log Parsing: Linux Timestamps")
		print("4) Search: bstrings wordlist (input_wordlist.txt)")
		print("5) Search: RegEx list (input_regex.txt)")
		print("6) Search: Free-text")
		print("7) Search: IPv4")
		print("8) Decode: QR codes")

		choice = input("Enter your choice: ")

		if choice == '1':
			break
		elif choice == '2':
			process_evtx_files()
		elif choice == '3':
			parse_linux_log_timestamps()
		elif choice == '4':
			search_wordlist()
		elif choice == '5':
			search_regex()
		elif choice == '6':
			search_freetext()
		elif choice == '7':
			search_ipv4()
		elif choice == '8':
			decode_qrcodes()
		else:
			print("Invalid choice. Please enter a valid option.")

if __name__ == "__main__":
	main()
