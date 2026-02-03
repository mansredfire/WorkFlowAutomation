import subprocess
import os
import logging

# Configure logging
logging.basicConfig(
    format="%(levelname)s [%(asctime)s] %(name)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    level=logging.DEBUG
)

# Function to execute scanner command and save results to a text file
def execute_scanner(scanner_name, command, result_directory, file_name):
    output_file = os.path.join(result_directory, file_name)
    with open(output_file, 'w', encoding='utf-8') as file:
        process = subprocess.Popen(
            command,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            encoding='utf-8',  # Changed from universal_newlines=True
            errors='replace'   # Handle encoding errors gracefully
        )
        # Read and display the output in real-time
        if process.stdout:
            for line in process.stdout:
                logging.debug(f"[{scanner_name}] {line.strip()}")
                file.write(line)
        process.wait()
        logging.info(f"Scan with {scanner_name} completed. Results saved to {output_file}.")

# Function to read file and extract data
def read_results(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        data = file.read()
    return data

# Specify the directory where the result files will be saved
result_directory = r"C:\Users\Owner\Desktop\output"

# Check if output directory exists, create if not
if not os.path.exists(result_directory):
    os.makedirs(result_directory)
    logging.info(f"Created output directory: {result_directory}")

# Specify the commands for each scanner
scanner_commands = {
    "CT-Exposer Domain, URL": "python ct-exposer.py -u -d amazon.com",    
    "Nmap DNS": r'nmap -p 53 --script dns-brute --script-args newtargets,threads=5,"useragent= whenallelsefails" -iL "C:\\Users\\Owner\\Desktop\\output\\domain_output.txt"',
    "Nmap Open Ports": r'nmap -p 1-65535 --open --max-rate 5/s --script banner --script-args "useragent= whenallelsefails" -iL "C:\\Users\\Owner\\Desktop\\output\\domain_output.txt"',
    #"Ffuf Directory and File Discovery": 'ffuf -w /path//to//wordlist.txt -u "http://smile.amazon.com/FUZZ?param=FFUFHASH" -o "C:\Users\mosic\OneDrive\Desktop\Amazon\Amazon Results\directory_output.txt" -mc 200,302 -fs -H "User-Agent: amazonvrpresearcher_whenallelsefails@hacker1" -rate 5 -X proxy -x http://127.0.0.1:8080 -v',
}

# Iterate through the scanners and execute the commands
for scanner_name, command in scanner_commands.items():
    file_name = f"{scanner_name}_results.txt"
    execute_scanner(scanner_name, command, result_directory, file_name)
    # Read the result file
    file_path = os.path.join(result_directory, file_name)
    data = read_results(file_path)
    logging.info(f"Data from {file_path} exported to {scanner_name} table.")
