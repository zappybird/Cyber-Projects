<h1>Network &amp; Vulnerability Scanner (Educational Cybersecurity Demo)</h1>

<p>
  This project is an educational, transparency‑focused tool that demonstrates how
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
  <li>Scans a target IP for <strong>open TCP ports</strong> across a user‑defined range</li>
  <li>Performs <strong>banner grabbing</strong> to identify exposed service information</li>
  <li>Uses <strong>Nmap</strong> (<code>-O -sV --script=vuln</code>) for OS detection and vulnerability enumeration</li>
  <li>Simple, readable Python code designed for learning and experimentation</li>
  <li>Timestamped scan duration for basic performance insight</li>
</ul>

<hr />

<h2>Project Structure</h2>

<pre><code>Port-Scanner/
│
├── scanner.py            # Main script; handles port scan, banners, and Nmap vuln scan
├── requirements.txt      # Python dependencies
└── README.md             # Project documentation
</code></pre>

<hr />

<h2>How It Works</h2>

<h3>1. Port Scanning</h3>
<p>
  The <code>port_scan()</code> function iterates over a user‑supplied port range and attempts a TCP connection
  using <code>socket.connect_ex()</code>. If the result is <code>0</code>, the port is considered <strong>open</strong>.
</p>

<h3>2. Banner Grabbing</h3>
<p>
  For each open port, <code>banner_grab()</code> connects to the service and reads up to 1024 bytes.
  Many services expose protocol or version information in this initial response, which is printed as the banner.
</p>

<h3>3. Vulnerability &amp; OS Detection</h3>
<p>
  The <code>vulnerability_scan()</code> function uses the Python Nmap wrapper:
</p>
<ul>
  <li><code>-O</code> for OS fingerprinting</li>
  <li><code>-sV</code> for service version detection</li>
  <li><code>--script=vuln</code> to run Nmap’s vulnerability scripts</li>
</ul>
<p>
  When available, results include hostnames, OS matches, and vulnerability information.
</p>

<h3>4. Full Scan Orchestration</h3>
<p>
  The <code>network_scan()</code> function ties everything together:
</p>
<ul>
  <li>Runs the port scan and prints any open ports</li>
  <li>Performs banner grabbing on each open port</li>
  <li>Runs the Nmap‑based vulnerability scan</li>
  <li>Prints total scan duration using <code>datetime</code></li>
</ul>

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

<h3>5. Run the scanner</h3>
<pre><code>python scanner.py
</code></pre>

<p>You will be prompted for:</p>
<ul>
  <li>Target IP address</li>
  <li>Starting port</li>
  <li>Ending port</li>
</ul>

<hr />

<h2>Example Output</h2>

<pre><code>Scanning ports from 1 to 1000 on 192.168.1.1...
Open ports found: 192.168.1.1: [22, 80, 443]
Banner for 192.168.1.1:80 - Apache httpd 2.4.41
Operating System Match: Linux 3.X
Vulnerabilities: {...}
Scan completed in: 0:00:12.482193
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
