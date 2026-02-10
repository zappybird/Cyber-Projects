<h1>📘 Network Traffic Analyzer</h1>

<p>
A Python-based packet capture and analysis tool that demonstrates how real monitoring systems ingest, classify, and analyze network traffic. 
Built with Scapy for packet capture, Rich for terminal output, and Matplotlib for visualization, this project provides a hands-on look at 
producer–consumer capture engines, protocol identification, bandwidth sampling, and kernel-level BPF filtering.
</p>

<hr />

<h2>📚 Documentation</h2>

<p>Full documentation is available in the <code>/docs</code> folder:</p>

<ul>
  <li><a href="./docs/01-OVERVIEW.md">01 – Overview</a></li>
  <li><a href="./docs/02-CONCEPTS.md">02 – Core Security Concepts</a></li>
  <li><a href="./docs/03-ARCHITECTURE.md">03 – System Architecture</a></li>
  <li><a href="./docs/04-IMPLEMENTATION.md">04 – Implementation Guide</a></li>
  <li><a href="./docs/05-CHALLENGES.md">05 – Challenges & Future Work</a></li>
</ul>

<hr />

<h2>🖥️ Setting Up a VM (VirtualBox)</h2>

<p>
If you're running this project inside a virtual machine, VirtualBox provides an isolated and flexible environment for testing packet capture.
Below is a quick setup guide.
</p>

<h3>1. Install VirtualBox</h3>
<ul>
  <li>Download from: <a href="https://www.virtualbox.org/">https://www.virtualbox.org/</a></li>
  <li>Install using default settings.</li>
</ul>

<h3>2. Download a Linux ISO</h3>
<ul>
  <li>Ubuntu Server (recommended)</li>
  <li>Ubuntu Desktop</li>
  <li>Debian</li>
</ul>

<h3>3. Create a New VM</h3>
<ul>
  <li>Name: <code>NetAnal-VM</code></li>
  <li>Type: Linux</li>
  <li>Version: Ubuntu (64-bit)</li>
  <li>Memory: 2–4 GB</li>
  <li>Disk: 20 GB dynamically allocated</li>
</ul>

<h3>4. Configure Networking</h3>
<ul>
  <li>Settings → Network → Adapter 1</li>
  <li>Set to <strong>Bridged Adapter</strong> (recommended)</li>
  <li>Promiscuous Mode → <strong>Allow All</strong></li>
</ul>

<h3>5. Install Linux + Python 3.14</h3>
<pre><code>sudo apt update
sudo apt install python3.14 python3.14-venv python3.14-dev git
</code></pre>

<h3>6. Clone and Install the Analyzer</h3>
<pre><code>git clone https://github.com/&lt;your-username&gt;/Cyber-Projects.git
cd Cyber-Projects/Network-traffic-analyzer
python3.14 -m venv .venv
source .venv/bin/activate
pip install -e .
</code></pre>

<hr />

<h2>🚀 Quick Start</h2>

<pre><code># List interfaces
sudo netanal interfaces

# Capture 50 packets
sudo netanal capture -i eth0 -c 50 --verbose

# Analyze a pcap file
netanal analyze traffic.pcap

# Generate charts
netanal chart traffic.pcap --type all -d ./charts/
</code></pre>

<hr />

<h2>🔒 Educational Purpose</h2>

<p>
This project is intended for defensive security learning, network engineering education, and understanding packet capture internals. 
Use only in controlled environments where you have authorization to capture traffic.
</p>
