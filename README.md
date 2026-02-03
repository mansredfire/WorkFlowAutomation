# Workflow Automation - Security Scanning Pipeline Orchestrator

## 📋 Overview

Workflow Automation is a lightweight, flexible security scanning orchestrator that automates the execution of multiple reconnaissance and vulnerability assessment tools in a coordinated pipeline. Designed for bug bounty hunters, penetration testers, and security researchers who need to run multiple tools sequentially without manual intervention.

## 🎯 Purpose

Security researchers and penetration testers often need to run multiple tools sequentially, manually managing outputs and feeding results from one tool into another. This creates inefficiencies:
- **Time waste** switching between tools and terminals
- **Manual file management** copying outputs between tools
- **Inconsistent logging** hard to track what ran when
- **Error-prone** forgetting to run certain scans
- **No visibility** into scan progress and failures

Workflow Automation solves this by:
1. **Automating tool execution** - Run entire scanning pipelines with one command
2. **Real-time logging** - See exactly what's happening with colored, timestamped output
3. **Centralized output** - All results saved to organized directory structure
4. **Error handling** - Continues pipeline even if individual tools fail
5. **Flexible configuration** - Easy to add, remove, or modify scanners
6. **Local payload support** - Use your own wordlists and payload files

## 🚀 Key Features

### Automated Tool Orchestration
- **Sequential execution** of multiple security tools
- **Automatic input/output chaining** - One tool's output feeds the next
- **Configurable scanner list** - Easy to add or remove tools
- **Custom command templates** - Full control over tool arguments
- **Zero dependencies** - Uses only Python standard library
- **Local payload integration** - Reference any wordlist/payload file on your system

### Intelligent Pipeline Management
- **Real-time console output** - See tool output as it runs
- **Detailed logging** - DEBUG, INFO, WARNING, ERROR levels
- **Timestamped logs** - Know exactly when each scan ran
- **Per-tool result files** - Organized output for each scanner
- **Automatic directory creation** - Sets up output folders automatically

### Robust Error Handling
- **UTF-8 encoding support** - Works on Windows and Linux
- **Subprocess error capture** - Catches and logs tool failures
- **Pipeline continuation** - Doesn't stop on single tool failure
- **Exit code tracking** - Know which tools succeeded/failed

### Supported Tools (Tool Agnostic - Works with ANY CLI Tool)
1. **CT-Exposer Enhanced** - Multi-source subdomain enumeration
2. **Nmap** - Port scanning and service detection
3. **Ffuf** - Web fuzzing and directory discovery
4. **Wfuzz** - Web application fuzzing
5. **Gobuster** - Directory/file brute-forcing
6. **Nuclei** - Vulnerability scanning with templates
7. **Nikto** - Web server scanning
8. **SQLMap** - SQL injection testing
9. **Sublist3r** - Subdomain enumeration
10. **...and any other command-line tool**

## 📦 Using Local Payload Files

### Overview

Workflow Automation allows you to use **any local wordlist or payload file** in your scanner commands. This gives you complete control over your fuzzing, brute-forcing, and enumeration workflows.

### Setting Up Your Payload Directory

**Step 1: Create a Payload Directory Structure**

```bash
# Windows
mkdir C:\Users\Owner\Desktop\payloads
cd C:\Users\Owner\Desktop\payloads
mkdir dns directories parameters fuzzing credentials

# Linux/Mac
mkdir -p ~/payloads/{dns,directories,parameters,fuzzing,credentials}
```

**Recommended Structure:**
```
C:\Users\Owner\Desktop\payloads\
├── dns\
│   ├── subdomains-1000.txt
│   ├── subdomains-10000.txt
│   └── subdomains-all.txt
├── directories\
│   ├── common.txt
│   ├── directory-list-2.3-medium.txt
│   ├── admin-panels.txt
│   └── backup-files.txt
├── parameters\
│   ├── common-params.txt
│   ├── burp-parameter-names.txt
│   └── api-params.txt
├── fuzzing\
│   ├── xss-payloads.txt
│   ├── sqli-payloads.txt
│   ├── lfi-payloads.txt
│   ├── ssrf-payloads.txt
│   └── rce-payloads.txt
└── credentials\
    ├── usernames.txt
    ├── passwords.txt
    └── common-passwords.txt
```

**Step 2: Download Wordlists**

```bash
# Download SecLists (comprehensive collection)
cd C:\Users\Owner\Desktop\payloads
git clone https://github.com/danielmiessler/SecLists.git

# Copy specific wordlists to your structure
# DNS wordlists
copy SecLists\Discovery\DNS\subdomains-top1million-5000.txt dns\subdomains-1000.txt
copy SecLists\Discovery\DNS\subdomains-top1million-20000.txt dns\subdomains-10000.txt

# Directory wordlists
copy SecLists\Discovery\Web-Content\common.txt directories\common.txt
copy SecLists\Discovery\Web-Content\directory-list-2.3-medium.txt directories\

# Parameter wordlists
copy SecLists\Discovery\Web-Content\burp-parameter-names.txt parameters\

# Fuzzing payloads
copy SecLists\Fuzzing\XSS\XSS-Bypass-Strings-BruteLogic.txt fuzzing\xss-payloads.txt
copy SecLists\Fuzzing\SQLi\quick-SQLi.txt fuzzing\sqli-payloads.txt
copy SecLists\Fuzzing\LFI\LFI-Jhaddix.txt fuzzing\lfi-payloads.txt

# Credentials
copy SecLists\Usernames\Names\names.txt credentials\usernames.txt
copy SecLists\Passwords\Common-Credentials\10-million-password-list-top-1000.txt credentials\passwords.txt
```

### How to Reference Payload Files in Commands

**Basic Syntax:**

```python
scanner_commands = {
    "Tool Name": r'tool -w "C:\full\path\to\wordlist.txt" -u target.com',
}
```

**Key Points:**
- Use raw strings (`r'...'`) for Windows paths to handle backslashes
- Use full absolute paths to payload files
- Wrap paths in quotes if they contain spaces
- Use forward slashes `/` on Linux/Mac, backslashes `\` on Windows

### Examples: Using Payload Files with Different Tools

**Example 1: Ffuf Directory Discovery**

```python
scanner_commands = {
    # Using common wordlist
    "Ffuf Directory Discovery": r'ffuf -w "C:\Users\Owner\Desktop\payloads\directories\common.txt" -u "http://target.com/FUZZ" -mc 200,301,302,403',
    
    # Using medium wordlist
    "Ffuf Directory Medium": r'ffuf -w "C:\Users\Owner\Desktop\payloads\directories\directory-list-2.3-medium.txt" -u "http://target.com/FUZZ" -mc 200,301,302,403 -o "C:\Users\Owner\Desktop\output\ffuf-dirs.json" -of json',
}
```

**Example 2: Ffuf Parameter Discovery**

```python
scanner_commands = {
    # GET parameter fuzzing
    "Ffuf GET Parameter Discovery": r'ffuf -w "C:\Users\Owner\Desktop\payloads\parameters\common-params.txt" -u "http://target.com/search?FUZZ=test" -mc 200,400,401,403,500',
    
    # POST parameter fuzzing
    "Ffuf POST Parameter Discovery": r'ffuf -w "C:\Users\Owner\Desktop\payloads\parameters\burp-parameter-names.txt" -u "http://target.com/login" -X POST -d "FUZZ=test" -mc 200,302',
}
```

**Example 3: XSS Payload Fuzzing**

```python
scanner_commands = {
    # XSS fuzzing with custom payloads
    "Ffuf XSS Fuzzing": r'ffuf -w "C:\Users\Owner\Desktop\payloads\fuzzing\xss-payloads.txt" -u "http://target.com/search?q=FUZZ" -mc 200 -mr "<script|onerror|onload"',
}
```

**Example 4: SQL Injection Fuzzing**

```python
scanner_commands = {
    # SQLi fuzzing
    "Ffuf SQLi Fuzzing": r'ffuf -w "C:\Users\Owner\Desktop\payloads\fuzzing\sqli-payloads.txt" -u "http://target.com/product?id=FUZZ" -mc 200,500 -mr "mysql|syntax|error|database"',
}
```

**Example 5: Nmap DNS Brute-force**

```python
scanner_commands = {
    # DNS bruteforce with custom wordlist
    "Nmap DNS Bruteforce": r'nmap -p 53 --script dns-brute --script-args "dns-brute.hostlist=C:\Users\Owner\Desktop\payloads\dns\subdomains-10000.txt,dns-brute.threads=10" -iL "C:\Users\Owner\Desktop\output\domain_output.txt"',
}
```

**Example 6: Gobuster with Custom Wordlist**

```python
scanner_commands = {
    # Gobuster directory scan
    "Gobuster Directory Scan": r'gobuster dir -u "http://target.com" -w "C:\Users\Owner\Desktop\payloads\directories\common.txt" -o "C:\Users\Owner\Desktop\output\gobuster_output.txt" -t 50',
    
    # Gobuster DNS subdomain scan
    "Gobuster DNS Scan": r'gobuster dns -d target.com -w "C:\Users\Owner\Desktop\payloads\dns\subdomains-1000.txt" -o "C:\Users\Owner\Desktop\output\gobuster_dns.txt"',
}
```

**Example 7: Wfuzz with Multiple Wordlists**

```python
scanner_commands = {
    # Wfuzz with custom wordlist
    "Wfuzz Directory Scan": r'wfuzz -w "C:\Users\Owner\Desktop\payloads\directories\common.txt" -u "http://target.com/FUZZ" --hc 404 -o "C:\Users\Owner\Desktop\output\wfuzz_output.txt"',
    
    # Wfuzz with multiple wordlists
    "Wfuzz Multi-Wordlist": r'wfuzz -w "C:\Users\Owner\Desktop\payloads\directories\common.txt" -w "C:\Users\Owner\Desktop\payloads\parameters\common-params.txt" -u "http://target.com/FUZZ?FUZ2Z=test" --hc 404',
}
```

**Example 8: Multiple Payload Files in One Command**

```python
scanner_commands = {
    # Ffuf with multiple wordlists using keyword substitution
    "Ffuf Multi-Wordlist Scan": r'ffuf -w "C:\Users\Owner\Desktop\payloads\directories\common.txt:DIRS" -w "C:\Users\Owner\Desktop\payloads\parameters\common-params.txt:PARAMS" -u "http://target.com/DIRS?PARAMS=test" -mc 200,301,302',
}
```

### Advanced Payload Configuration

**Using Variables for Cleaner Code:**

```python
# Define payload directory at the top
PAYLOAD_DIR = r"C:\Users\Owner\Desktop\payloads"

scanner_commands = {
    "Ffuf Directory Scan": f'ffuf -w "{PAYLOAD_DIR}\\directories\\common.txt" -u "http://target.com/FUZZ" -mc 200,301,302',
    
    "Ffuf XSS Fuzzing": f'ffuf -w "{PAYLOAD_DIR}\\fuzzing\\xss-payloads.txt" -u "http://target.com/search?q=FUZZ" -mc 200',
    
    "Nmap DNS Bruteforce": f'nmap --script dns-brute --script-args "dns-brute.hostlist={PAYLOAD_DIR}\\dns\\subdomains-10000.txt"',
}
```

**Creating Custom Payload Files:**

```python
# Create a custom wordlist for specific target
with open(r"C:\Users\Owner\Desktop\payloads\custom\target-specific.txt", "w") as f:
    f.write("api\n")
    f.write("admin\n")
    f.write("dashboard\n")
    f.write("portal\n")

scanner_commands = {
    "Ffuf Custom Wordlist": r'ffuf -w "C:\Users\Owner\Desktop\payloads\custom\target-specific.txt" -u "http://target.com/FUZZ" -mc 200,301,302',
}
```

### Common Payload File Options for Popular Tools

**Ffuf Options:**
```python
# -w : Wordlist file path
# -u : URL with FUZZ keyword
# -mc : Match HTTP status codes
# -mr : Match regex pattern
# -fw : Filter by word count
# -fs : Filter by response size
# -rate : Requests per second
# -o : Output file
# -of : Output format (json, csv, etc.)

"Ffuf Example": r'ffuf -w "path\to\wordlist.txt" -u "http://target.com/FUZZ" -mc 200 -o "output.json" -of json'
```

**Gobuster Options:**
```python
# -w : Wordlist file path
# -u : Target URL
# -o : Output file
# -t : Number of threads
# --hc : Hide status codes

"Gobuster Example": r'gobuster dir -u "http://target.com" -w "path\to\wordlist.txt" -o "output.txt" -t 50'
```

**Wfuzz Options:**
```python
# -w : Wordlist file path
# -u : URL with FUZZ keyword
# --hc : Hide status codes
# -o : Output file

"Wfuzz Example": r'wfuzz -w "path\to\wordlist.txt" -u "http://target.com/FUZZ" --hc 404 -o "output.txt"'
```

**Nmap Options:**
```python
# --script-args : Script arguments including wordlist path
# -iL : Input list of hosts

"Nmap Example": r'nmap --script dns-brute --script-args "dns-brute.hostlist=path\to\wordlist.txt"'
```

### Troubleshooting Payload File Issues

**Issue: "File not found" error**

```python
# Solution 1: Use absolute paths
# Wrong:
"Ffuf": 'ffuf -w wordlist.txt -u target.com'

# Right:
"Ffuf": r'ffuf -w "C:\Users\Owner\Desktop\payloads\wordlist.txt" -u target.com'

# Solution 2: Check file exists
import os
wordlist_path = r"C:\Users\Owner\Desktop\payloads\directories\common.txt"
if os.path.exists(wordlist_path):
    print(f"Found: {wordlist_path}")
else:
    print(f"Missing: {wordlist_path}")
```

**Issue: Path with spaces not working**

```python
# Wrong:
"Ffuf": r'ffuf -w C:\My Files\wordlist.txt'

# Right:
"Ffuf": r'ffuf -w "C:\My Files\wordlist.txt"'
```

**Issue: Windows vs Linux paths**

```python
# Windows:
"Ffuf": r'ffuf -w "C:\Users\Owner\Desktop\payloads\common.txt"'

# Linux/Mac:
"Ffuf": r'ffuf -w "/home/user/payloads/common.txt"'

# Cross-platform (using os.path):
import os
payload_path = os.path.join("payloads", "directories", "common.txt")
"Ffuf": f'ffuf -w "{payload_path}"'
```

## 📊 Output Structure

```
C:\Users\Owner\Desktop\output\
├── CT-Exposer_Domain_URL_results.txt
├── Nmap_DNS_results.txt
├── Nmap_Open_Ports_results.txt
├── Ffuf_Directory_Discovery_results.txt
├── Ffuf_XSS_Fuzzing_results.txt
├── Nuclei_Vulnerability_Scan_results.txt
└── [Tool_Name]_results.txt
```

## 🛠️ Technical Architecture

### Core Components

**1. Logging System**
```python
logging.basicConfig(
    format="%(levelname)s [%(asctime)s] %(name)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    level=logging.DEBUG
)
```
- Configurable log levels
- Timestamp tracking
- Tool identification
- Structured output

**2. Scanner Execution Engine**
```python
def execute_scanner(scanner_name, command, result_directory, file_name):
    # Subprocess management
    # Real-time output streaming
    # Error capture
    # Result file saving
```

**3. Output Management**
```python
def read_results(file_path):
    # UTF-8 encoded file reading
    # Result parsing
    # Data extraction
```

**4. Scanner Configuration**
```python
scanner_commands = {
    "Scanner Name": r'command with args and "path\to\payload.txt"',
    # Easy to add more scanners with custom payloads
}
```

### Pipeline Flow

```
┌─────────────────────────────────────────────────────┐
│ 1. Workflow Automation Starts                       │
│    └─> Creates output directory                     │
│    └─> Initializes logging                          │
└─────────────────────────────────────────────────────┘
                      ▼
┌─────────────────────────────────────────────────────┐
│ 2. CT-Exposer Enhanced                              │
│    └─> Queries 11+ CT log sources                   │
│    └─> Deduplicates subdomains                      │
│    └─> Saves to domain_output.txt                   │
└─────────────────────────────────────────────────────┘
                      ▼
┌─────────────────────────────────────────────────────┐
│ 3. Nmap DNS Brute-force (with custom wordlist)     │
│    └─> Reads domain_output.txt                      │
│    └─> Uses local DNS wordlist                      │
│    └─> Discovers additional subdomains              │
└─────────────────────────────────────────────────────┘
                      ▼
┌─────────────────────────────────────────────────────┐
│ 4. Ffuf Directory Discovery (with custom wordlist) │
│    └─> Uses local directory wordlist                │
│    └─> Identifies hidden paths                      │
│    └─> Saves findings to JSON                       │
└─────────────────────────────────────────────────────┘
                      ▼
┌─────────────────────────────────────────────────────┐
│ 5. Ffuf Vulnerability Fuzzing (with payload files) │
│    └─> Uses XSS/SQLi/LFI payload files              │
│    └─> Tests for vulnerabilities                    │
│    └─> Logs successful payloads                     │
└─────────────────────────────────────────────────────┘
                      ▼
┌─────────────────────────────────────────────────────┐
│ 6. Results Processing                               │
│    └─> Exports data to individual files             │
│    └─> Logs completion status                       │
│    └─> Ready for manual analysis                    │
└─────────────────────────────────────────────────────┘
```

## 💻 Usage

### Basic Execution
```bash
python workflow-automation.py
```

### What Happens
1. Output directory is checked/created
2. Each scanner executes in sequence
3. Real-time output is displayed and logged
4. Results are saved to organized text files
5. Summary shows completion status

### Customizing Scanners

**Add a New Scanner:**
```python
scanner_commands = {
    "CT-Exposer Domain, URL": "python ct-exposer.py -u -d amazon.com",
    "Your New Tool": r'toolname -w "C:\payloads\wordlist.txt" -u target.com',
}
```

**Modify Existing Scanner:**
```python
# Change target domain
"CT-Exposer Domain, URL": "python ct-exposer.py -u -d yourtarget.com"

# Change wordlist
"Ffuf Directory Scan": r'ffuf -w "C:\payloads\directories\custom-wordlist.txt" -u "http://target.com/FUZZ"'
```

**Remove a Scanner:**
```python
# Simply comment out or delete the line
# "Scanner Name": "command",
```

## 📈 Example Output

```
INFO [2026-02-03 14:23:15] root - Created output directory: C:\Users\Owner\Desktop\output

DEBUG [2026-02-03 14:23:16] root - [CT-Exposer Domain, URL] [+]: Starting CT log enumeration for amazon.com
DEBUG [2026-02-03 14:23:16] root - [CT-Exposer Domain, URL] [+]: Querying 11 different sources...
DEBUG [2026-02-03 14:23:18] root - [CT-Exposer Domain, URL] [+]: Querying crt.sh...
DEBUG [2026-02-03 14:23:22] root - [CT-Exposer Domain, URL]     [+] Found 2847 domain(s) from crt.sh
DEBUG [2026-02-03 14:23:22] root - [CT-Exposer Domain, URL] [+]: Total unique domains found: 2847

INFO [2026-02-03 14:25:45] root - Scan with CT-Exposer Domain, URL completed. Results saved to C:\Users\Owner\Desktop\output\CT-Exposer Domain, URL_results.txt.
INFO [2026-02-03 14:25:45] root - Data from C:\Users\Owner\Desktop\output\CT-Exposer Domain, URL_results.txt exported to CT-Exposer Domain, URL table.

DEBUG [2026-02-03 14:25:46] root - [Ffuf Directory Discovery] [INF] Using wordlist: C:\Users\Owner\Desktop\payloads\directories\common.txt
DEBUG [2026-02-03 14:25:47] root - [Ffuf Directory Discovery] [INF] Starting FUZZ with 4614 entries
DEBUG [2026-02-03 14:26:32] root - [Ffuf Directory Discovery] [Status: 200, Size: 1234, Words: 89] /admin
DEBUG [2026-02-03 14:26:35] root - [Ffuf Directory Discovery] [Status: 301, Size: 234, Words: 12] /api

INFO [2026-02-03 14:28:15] root - Scan with Ffuf Directory Discovery completed. Results saved to C:\Users\Owner\Desktop\output\Ffuf_Directory_Discovery_results.txt.
```

## 🎓 Use Cases

### 1. Bug Bounty Reconnaissance
Run the entire recon pipeline against a target domain to quickly map attack surface.

```python
PAYLOAD_DIR = r"C:\Users\Owner\Desktop\payloads"

scanner_commands = {
    "CT-Exposer Subdomain Enum": "python ct-exposer.py -u -d bugcrowd-target.com",
    "Nmap Service Detection": r'nmap -sV -sC -p- --open -iL "output\domain_output.txt"',
    "Ffuf Directory Discovery": f'ffuf -w "{PAYLOAD_DIR}\\directories\\common.txt" -u "http://target.com/FUZZ"',
    "Ffuf XSS Testing": f'ffuf -w "{PAYLOAD_DIR}\\fuzzing\\xss-payloads.txt" -u "http://target.com/search?q=FUZZ"',
}
```

### 2. Penetration Testing Kickoff
Start comprehensive scanning at the beginning of an engagement while you work on other tasks.

### 3. Continuous Monitoring
Schedule with cron/Task Scheduler to run daily and detect infrastructure changes.

```bash
# Linux cron example
0 2 * * * /usr/bin/python3 /path/to/workflow-automation.py >> /var/log/recon.log 2>&1
```

### 4. Client Reporting
Automatically generate scan data for inclusion in penetration test reports.

### 5. Training & Education
Demonstrate security tool workflows to students and junior security analysts.

## 🔧 Dependencies

### Required Tools
- **Python 3.7+** (no additional Python packages required - uses only standard library!)

### Optional Security Tools (Install as needed for your workflow)
- **CT-Exposer Enhanced** (included in toolkit)
- **Nmap** - https://nmap.org/download.html
- **Ffuf** - https://github.com/ffuf/ffuf
- **Gobuster** - https://github.com/OJ/gobuster
- **Nuclei** - https://github.com/projectdiscovery/nuclei
- **Nikto** - https://cirt.net/Nikto2
- **SQLMap** - https://sqlmap.org/
- **Wfuzz** - https://github.com/xmendez/wfuzz

### Python Libraries
**NONE!** - This script uses only Python's standard library:
- `subprocess` - Process execution
- `os` - File system operations
- `logging` - Logging functionality

### Wordlist/Payload Resources
- **SecLists** - https://github.com/danielmiessler/SecLists (Most comprehensive)
- **FuzzDB** - https://github.com/fuzzdb-project/fuzzdb
- **PayloadsAllTheThings** - https://github.com/swisskyrepo/PayloadsAllTheThings
- **Assetnote Wordlists** - https://wordlists.assetnote.io/

### Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/workflow-automation.git
cd workflow-automation

# No pip install required!

# Download wordlists (recommended)
cd C:\Users\Owner\Desktop
mkdir payloads
cd payloads
git clone https://github.com/danielmiessler/SecLists.git

# Install security tools (optional - install what you need)
# Nmap (Windows)
# Download from https://nmap.org/download.html

# Nmap (Linux)
sudo apt-get install nmap

# Ffuf
go install github.com/ffuf/ffuf@latest

# Gobuster
go install github.com/OJ/gobuster/v3@latest

# Nuclei
go install -v github.com/projectdiscovery/nuclei/v2/cmd/nuclei@latest

# Run the script
python workflow-automation.py
```

## 🔒 Security Considerations

### Ethical Usage
- **Only scan authorized targets** - Unauthorized scanning is illegal
- **Respect rate limits** - Don't overload target infrastructure
- **Follow disclosure policies** - Report findings responsibly
- **User-Agent identification** - Tool uses identifiable UA for transparency

### Operational Security
- **Protect output files** - May contain sensitive reconnaissance data
- **Protect payload files** - Some payloads could be flagged by antivirus
- **Log management** - Logs contain target information
- **Network visibility** - Scanning creates network traffic footprint

## ⚙️ Configuration

### Output Directory
```python
result_directory = r"C:\Users\Owner\Desktop\output"
```
Change this to your preferred output location.

### Payload Directory
```python
# Define at top of script for easy reference
PAYLOAD_DIR = r"C:\Users\Owner\Desktop\payloads"

scanner_commands = {
    "Scanner": f'tool -w "{PAYLOAD_DIR}\\wordlist.txt"',
}
```

### Scanner Rate Limiting
```python
# In Nmap commands
--max-rate 5/s  # 5 packets per second

# In Ffuf commands
-rate 10  # 10 requests per second
```

### Logging Level
```python
level=logging.DEBUG  # Change to INFO, WARNING, or ERROR
```

### Custom User-Agent
```python
# In individual tool configs
--script-args "useragent=youruseragent"
-H "User-Agent: youruseragent"
```

## 🚧 Current Limitations

- Sequential execution (tools run one at a time)
- No parallel scanning capabilities
- Limited error recovery options
- Manual target configuration required
- Windows path format in examples (needs modification for Linux)
- No built-in result correlation
- Payload files must be managed manually

## 🔮 Planned Enhancements

- [ ] **Parallel scanner execution** - Run multiple tools simultaneously
- [ ] **Configuration file** - JSON/YAML based scanner configs
- [ ] **Result aggregation** - Combine outputs into single report
- [ ] **Progress indicators** - Visual progress bars for long scans
- [ ] **Email notifications** - Alert when scans complete
- [ ] **Web dashboard** - Real-time scan monitoring interface
- [ ] **Docker support** - Containerized scanning environment
- [ ] **CI/CD integration** - GitHub Actions/Jenkins pipeline
- [ ] **Database backend** - Store results in SQLite/PostgreSQL
- [ ] **API interface** - REST API for triggering scans
- [ ] **Result diffing** - Compare scans over time
- [ ] **Screenshot integration** - Automatic visual recon
- [ ] **Automatic wordlist selection** - Smart payload file chooser

## 🤝 Contributing

Contributions welcome! Areas for improvement:

### Easy Contributions
- Add new scanner integrations
- Improve logging messages
- Add more example configurations
- Documentation improvements
- Share your custom payload files

### Medium Contributions
- Implement parallel execution
- Add configuration file support
- Create result parsers
- Build progress indicators
- Payload file validator

### Advanced Contributions
- Web dashboard development
- Database integration
- API development
- Cross-platform compatibility

## 📝 Integration Examples

### With Other Tools

**Chain with Nuclei:**
```python
scanner_commands = {
    # ... existing scanners
    "Nuclei Vulnerability Scan": r'nuclei -l "C:\Users\Owner\Desktop\output\domain_output.txt" -t "C:\Users\Owner\Desktop\payloads\nuclei-templates\cves\" -o nuclei_results.txt',
}
```

**Chain with Aquatone:**
```python
scanner_commands = {
    # ... existing scanners
    "Aquatone Screenshots": r'cat domain_output.txt | aquatone -out screenshots/',
}
```

**Chain with Subjack:**
```python
scanner_commands = {
    # ... existing scanners
    "Subjack Takeover": r'subjack -w domain_output.txt -t 100 -timeout 30 -o subjack_results.txt',
}
```

### CI/CD Pipeline Example

```yaml
# .github/workflows/recon.yml
name: Automated Reconnaissance

on:
  schedule:
    - cron: '0 2 * * *'  # Daily at 2 AM

jobs:
  recon:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.9'
      - name: Install Nmap
        run: sudo apt-get install nmap
      - name: Download Wordlists
        run: |
          mkdir payloads
          cd payloads
          git clone https://github.com/danielmiessler/SecLists.git
      - name: Run Workflow Automation
        run: python workflow-automation.py
      - name: Upload results
        uses: actions/upload-artifact@v2
        with:
          name: recon-results
          path: output/
```

## 📜 License

MIT License - Free to use in commercial and open-source projects

## 👨‍💻 Author

Created for security professionals who value automation and efficiency in their reconnaissance workflows.

## 🙏 Acknowledgments

- Nmap project for comprehensive network scanning
- CT-Exposer Enhanced for subdomain enumeration
- Security community for tool development
- SecLists for comprehensive wordlist collection
- Bug bounty platforms for testing opportunities

---

## 📸 Sample Workflow

### Step 1: Setup Payloads
```bash
# Create payload directory
mkdir C:\Users\Owner\Desktop\payloads
cd C:\Users\Owner\Desktop\payloads

# Download SecLists
git clone https://github.com/danielmiessler/SecLists.git

# Organize wordlists
mkdir dns directories parameters fuzzing
copy SecLists\Discovery\DNS\*.txt dns\
copy SecLists\Discovery\Web-Content\*.txt directories\
```

### Step 2: Configuration
```python
# Edit scanner commands with your payload paths
PAYLOAD_DIR = r"C:\Users\Owner\Desktop\payloads"

scanner_commands = {
    "CT-Exposer Domain": "python ct-exposer.py -u -d target.com",
    "Ffuf Directory Scan": f'ffuf -w "{PAYLOAD_DIR}\\directories\\common.txt" -u "http://target.com/FUZZ"',
}
```

### Step 3: Execution
```bash
python workflow-automation.py
```

### Step 4: Monitor Progress
```
INFO [2026-02-03 14:23:15] root - Created output directory
DEBUG [2026-02-03 14:23:16] root - [CT-Exposer] Starting...
DEBUG [2026-02-03 14:23:16] root - [Ffuf] Using wordlist: C:\...\payloads\directories\common.txt
```

### Step 5: Review Results
```bash
cd C:\Users\Owner\Desktop\output
dir
# See all result files organized by scanner
```

---

## 🎯 Quick Start Checklist

- [ ] Install Python 3.7+
- [ ] Install security tools you want to use (Nmap, Ffuf, etc.)
- [ ] Clone repository
- [ ] **No pip install needed!**
- [ ] Create payload directory structure
- [ ] Download SecLists wordlists
- [ ] Edit scanner commands with payload file paths
- [ ] Edit target domain in `scanner_commands`
- [ ] Run `python workflow-automation.py`
- [ ] Check output directory for results
- [ ] Analyze findings and proceed with testing

---

**⭐ Star this repo if automated workflows saved you hours of manual work!**

**🐛 Found a bug? Open an issue!**

**💡 Have an idea? Submit a pull request!**

---
