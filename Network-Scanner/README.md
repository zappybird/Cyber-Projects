# Network & Vulnerability Scanner (Educational Cybersecurity Demo)

This project is an educational, transparency-focused tool that demonstrates how **port scanning**, **banner grabbing**, and **basic vulnerability detection** work under the hood. It is intended **solely for personal cybersecurity learning, debugging, and defensive research**.

The scanner identifies open ports, retrieves service banners, and uses Nmap to detect OS information and known vulnerabilities. Use it only on systems you own and control.

---

## Features

- Scans a target IP for **open TCP ports** across a user-defined range
- Performs **banner grabbing** to identify exposed service information
- Uses **Nmap** (`-O -sV --script=vuln`) for OS detection and vulnerability enumeration
- Simple, readable Python code designed for learning and experimentation
- Timestamped scan duration for basic performance insight
- Color-coded terminal output for fast, legible result reading
- Browser-based GUI with live streaming output, accessible at `http://127.0.0.1:5000`

---

## Project Structure

```
Port-Scanner/
│
├── scanner.py            # CLI entry point; handles port scan, banners, and Nmap vuln scan
├── app.py                # GUI entry point; Flask server with live-streaming browser interface
├── requirements.txt      # Python dependencies
└── README.md             # Project documentation
```

---

## How It Works

### 1. Port Scanning

The `port_scan()` function iterates over a user-supplied port range and attempts a TCP connection using `socket.connect_ex()`. If the result is `0`, the port is considered **open**. Results are collected silently and displayed as a formatted table once the phase is complete.

### 2. Banner Grabbing

For each open port, `banner_grab()` connects to the service and reads up to 1024 bytes. Many services expose protocol or version information in this initial response. Banners are stored and rendered alongside their port in the results table rather than printed mid-scan.

### 3. Vulnerability & OS Detection

The `vulnerability_scan()` function uses the Python Nmap wrapper:

- `-O` for OS fingerprinting
- `-sV` for service version detection
- `--script=vuln` to run Nmap's vulnerability scripts

Results include hostnames, the top three OS matches with accuracy percentage and device type, and vulnerability entries labeled by severity state.

### 4. Full Scan Orchestration

The `network_scan()` function ties everything together:

- Runs the port scan and displays open ports in a formatted table
- Performs banner grabbing on each open port
- Runs the Nmap-based vulnerability scan
- Prints total scan duration using `datetime`

### 5. GUI Mode

`app.py` runs a Flask server on `127.0.0.1:5000`. The browser interface accepts the same three inputs as the CLI — target IP, start port, and end port — and streams scan output line-by-line using Server-Sent Events (SSE). Results appear as they arrive rather than after the full scan completes. A live elapsed timer is displayed in the status bar throughout the scan.

---

## Installation (from source)

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/Port-Scanner.git
cd Port-Scanner
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

### 3. Activate it

```bash
# Windows
.venv\Scripts\activate

# macOS / Linux
source .venv/bin/activate
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

### 5. Install Nmap on your system

```bash
# Windows — https://nmap.org/download.html
sudo apt install nmap   # Debian / Ubuntu
brew install nmap       # macOS
```

> OS detection may require running as Administrator or root.

### 6. Run the scanner

```bash
# CLI mode
python scanner.py

# GUI mode — then open http://127.0.0.1:5000 in your browser
python app.py
```

You will be prompted for:

- Target IP address
- Starting port
- Ending port

---

## Example Output

```
══════════════════════════════════════════════════
   NETWORK SCANNER
══════════════════════════════════════════════════
  Target : 192.168.1.254
  Ports  : 1 → 100
  Started: 2026-02-28 14:22:01

  [*] Running port scan...
  [*] Grabbing banners...
  [*] Running vulnerability scan (this may take a while)...

──────────────────────────────────────────────────
  PORT SCAN RESULTS
──────────────────────────────────────────────────
  PORT       STATE      BANNER
  ────       ─────      ──────
  53         OPEN       —
  80         OPEN       —

──────────────────────────────────────────────────
  HOST INFORMATION
──────────────────────────────────────────────────
  Hostname(s):  dsldevice

  OS Detection (Top Matches):
    1. Linux 4.15 - 5.19
       Accuracy: 100%   |   Type: general purpose
    2. OpenWrt 21.02 (Linux 5.4)
       Accuracy: 100%   |   Type: general purpose
    3. MikroTik RouterOS 7.2 - 7.5 (Linux 5.6.3)
       Accuracy: 100%   |   Type: router

──────────────────────────────────────────────────
  VULNERABILITY SCAN
──────────────────────────────────────────────────
  No known vulnerabilities detected.

══════════════════════════════════════════════════
  Scan completed at 14:26:39  |  Duration: 0:04:37
══════════════════════════════════════════════════
```

---

## Legal & Ethical Notice

This project is provided for **educational and defensive purposes only**. You must **never** use it to scan networks, devices, or systems you do not own or lack explicit permission to test.

Unauthorized scanning may violate laws or terms of service. Use responsibly and ethically.