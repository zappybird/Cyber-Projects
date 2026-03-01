<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Network &amp; Vulnerability Scanner (Educational Cybersecurity Demo)</title>
<style>
  body {
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif;
    font-size: 16px;
    line-height: 1.6;
    color: #24292e;
    background: #ffffff;
    max-width: 800px;
    margin: 0 auto;
    padding: 32px 24px 64px;
  }

  h1 {
    font-size: 2em;
    font-weight: 600;
    border-bottom: 1px solid #eaecef;
    padding-bottom: 0.3em;
    margin-top: 0;
    margin-bottom: 16px;
  }

  h2 {
    font-size: 1.5em;
    font-weight: 600;
    border-bottom: 1px solid #eaecef;
    padding-bottom: 0.3em;
    margin-top: 24px;
    margin-bottom: 16px;
  }

  h3 {
    font-size: 1.25em;
    font-weight: 600;
    margin-top: 24px;
    margin-bottom: 16px;
  }

  p {
    margin-top: 0;
    margin-bottom: 16px;
  }

  ul {
    padding-left: 2em;
    margin-top: 0;
    margin-bottom: 16px;
  }

  li {
    margin-bottom: 4px;
  }

  hr {
    border: none;
    border-top: 1px solid #eaecef;
    margin: 24px 0;
  }

  code {
    font-family: "SFMono-Regular", Consolas, "Liberation Mono", Menlo, monospace;
    font-size: 85%;
    background-color: rgba(27,31,35,0.05);
    border-radius: 3px;
    padding: 0.2em 0.4em;
  }

  pre {
    font-family: "SFMono-Regular", Consolas, "Liberation Mono", Menlo, monospace;
    font-size: 85%;
    background-color: #f6f8fa;
    border-radius: 6px;
    padding: 16px;
    overflow: auto;
    line-height: 1.45;
    margin-top: 0;
    margin-bottom: 16px;
  }

  pre code {
    background: none;
    padding: 0;
    font-size: 100%;
  }

  strong { font-weight: 600; }
</style>
</head>
<body>

<h1>Network &amp; Vulnerability Scanner (Educational Cybersecurity Demo)</h1>

<p>
  This project is an educational, transparency-focused tool that demonstrates how
  <strong>port scanning</strong>, <strong>banner grabbing</strong>, and
  <strong>basic vulnerability detection</strong> work under the hood.
  It is intended <strong>solely for personal cybersecurity learning, debugging, and defensive research</strong>.
</p>

<p>
  The scanner identifies open ports, retrieves service banners, and uses Nmap to detect OS information and known vulnerabilities.
  Use it only on systems you own and control.
</p>

<hr />

<h2>Features</h2>
<ul>
  <li>Scans a target IP for <strong>open TCP ports</strong> across a user-defined range</li>
  <li>Performs <strong>banner grabbing</strong> to identify exposed service information</li>
  <li>Uses <strong>Nmap</strong> (<code>-O -sV --script=vuln</code>) for OS detection and vulnerability enumeration</li>
  <li>Simple, readable Python code designed for learning and experimentation</li>
  <li>Timestamped scan duration for basic performance insight</li>
  <li>Color-coded terminal output for fast, legible result reading</li>
  <li>Browser-based GUI with live streaming output, accessible at <code>http://127.0.0.1:5000</code></li>
</ul>

<hr />

<h2>Project Structure</h2>

<pre><code>Port-Scanner/
│
├── scanner.py            # CLI entry point; handles port scan, banners, and Nmap vuln scan
├── app.py                # GUI entry point; Flask server with live-streaming browser interface
├── requirements.txt      # Python dependencies
└── README.html           # Project documentation
</code></pre>

<hr />

<h2>How It Works</h2>

<h3>1. Port Scanning</h3>
<p>
  The <code>port_scan()</code> function iterates over a user-supplied port range and attempts a TCP connection
  using <code>socket.connect_ex()</code>. If the result is <code>0</code>, the port is considered <strong>open</strong>.
  Results are collected silently and displayed as a formatted table once the phase is complete.
</p>

<h3>2. Banner Grabbing</h3>
<p>
  For each open port, <code>banner_grab()</code> connects to the service and reads up to 1024 bytes.
  Many services expose protocol or version information in this initial response. Banners are stored and
  rendered alongside their port in the results table rather than printed mid-scan.
</p>

<h3>3. Vulnerability &amp; OS Detection</h3>
<p>
  The <code>vulnerability_scan()</code> function uses the Python Nmap wrapper:
</p>
<ul>
  <li><code>-O</code> for OS fingerprinting</li>
  <li><code>-sV</code> for service version detection</li>
  <li><code>--script=vuln</code> to run Nmap's vulnerability scripts</li>
</ul>
<p>
  Results include hostnames, the top three OS matches with accuracy percentage and device type,
  and vulnerability entries labeled by severity state.
</p>

<h3>4. Full Scan Orchestration</h3>
<p>
  The <code>network_scan()</code> function ties everything together:
</p>
<ul>
  <li>Runs the port scan and displays open ports in a formatted table</li>
  <li>Performs banner grabbing on each open port</li>
  <li>Runs the Nmap-based vulnerability scan</li>
  <li>Prints total scan duration using <code>datetime</code></li>
</ul>

<h3>5. GUI Mode</h3>
<p>
  <code>app.py</code> runs a Flask server on <code>127.0.0.1:5000</code>. The browser interface accepts
  the same three inputs as the CLI — target IP, start port, and end port — and streams scan output
  line-by-line using Server-Sent Events (SSE). Results appear as they arrive rather than after the full
  scan completes. A live elapsed timer is displayed in the status bar throughout the scan.
</p>

<hr />

<h2>Installation (from source)</h2>

<h3>1. Clone the repository</h3>
<pre><code>git clone https://github.com/yourusername/Port-Scanner.git
cd Port-Scanner
</code></pre>

<h3>2. Create a virtual environment</h3>
<pre><code>python -m venv .venv
</code></pre>

<h3>3. Activate it (Windows)</h3>
<pre><code>.venv\Scripts\activate
</code></pre>

<h3>4. Install dependencies</h3>
<pre><code>pip install -r requirements.txt
</code></pre>

<h3>5. Install Nmap on your system</h3>
<pre><code># Windows — https://nmap.org/download.html
sudo apt install nmap   # Debian / Ubuntu
brew install nmap       # macOS
</code></pre>
<p>OS detection may require running as Administrator or root.</p>

<h3>6. Run the scanner</h3>
<pre><code># CLI mode
python scanner.py

# GUI mode — then open http://127.0.0.1:5000 in your browser
python app.py
</code></pre>

<p>You will be prompted for:</p>
<ul>
  <li>Target IP address</li>
  <li>Starting port</li>
  <li>Ending port</li>
</ul>

<hr />

<h2>Example Output</h2>

<pre><code>══════════════════════════════════════════════════
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
</code></pre>

<hr />

<h2>Legal &amp; Ethical Notice</h2>

<p>
  This project is provided for <strong>educational and defensive purposes only</strong>.
  You must <strong>never</strong> use it to scan networks, devices, or systems you do not own
  or lack explicit permission to test.
</p>

<p>
  Unauthorized scanning may violate laws or terms of service.
  Use responsibly and ethically.
</p>

</body>
</html>