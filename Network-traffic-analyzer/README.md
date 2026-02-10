<h1>📘 Network Traffic Analyzer</h1>

<p>
A Python-based packet capture and analysis tool that demonstrates how real monitoring systems ingest, classify, and analyze network traffic.
Built with Scapy, Rich, and Matplotlib, this project provides a hands-on look at producer–consumer capture engines, protocol identification,
bandwidth sampling, and kernel-level BPF filtering.
</p>

<hr />

<h2>📚 Documentation</h2>

<p>Full documentation is available in the <code>/docs</code> folder:</p>

<ul>
  <li><a href="./docs/00-OVERVIEW.md">00 – Overview</a></li>
  <li><a href="./docs/01-LAB-GUIDE.md">01 – Lab Guide (Setup & Usage)</a></li>
  <li><a href="./docs/04-CHALLENGES.md">04 – Challenges & Future Work</a></li>
</ul>

<hr />

<h1>📡 Network Traffic Analyzer</h1>

<h2>What This Is</h2>

<p>
A Python-based packet capture and analysis tool that inspects live network traffic, identifies protocols, tracks bandwidth usage, 
and generates visual reports. Built with <strong>Scapy</strong> for packet capture, <strong>Rich</strong> for terminal output, and 
<strong>Matplotlib</strong> for charts, this project provides a hands-on look at how real monitoring systems ingest, classify, and analyze packets.
</p>

<h2>Why This Matters</h2>

<p>
Network visibility is the foundation of security monitoring. Without packet-level insight, you cannot detect intrusions, 
data exfiltration, or policy violations. This project teaches you how packet capture works at the kernel level — not just how to run Wireshark.
</p>

<p><strong>Real world scenarios where this applies:</strong></p>

<ul>
  <li><strong>Incident response:</strong> During the 2013 Target breach, unusual outbound connections from POS systems could have been detected through packet-level monitoring.</li>
  <li><strong>Performance troubleshooting:</strong> Packet captures reveal latency, retransmissions, and protocol-level issues that application logs often miss.</li>
  <li><strong>Security baselining:</strong> Understanding normal protocol distribution and bandwidth usage is essential for anomaly detection.</li>
</ul>

<h2>What You'll Learn</h2>

<p>This project teaches you how network packet capture works at the system level. By building and running it, you'll understand:</p>

<h3>Security Concepts</h3>
<ul>
  <li><strong>Raw socket access</strong> — Why packet capture requires elevated privileges and how CAP_NET_RAW works on Linux.</li>
  <li><strong>Protocol layer inspection</strong> — How to dissect packets from Ethernet (L2) through HTTP (L7).</li>
  <li><strong>Network baseline establishment</strong> — How to identify anomalies using protocol and bandwidth patterns.</li>
</ul>

<h3>Technical Skills</h3>
<ul>
  <li><strong>Producer–consumer threading</strong> — Capture packets at wire speed while processing them safely in parallel.</li>
  <li><strong>Kernel-level BPF filtering</strong> — Offload filtering to the kernel for massive performance gains.</li>
  <li><strong>Time-series data collection</strong> — Track bandwidth and packet rates over time.</li>
</ul>

<h3>Tools and Techniques</h3>
<ul>
  <li><strong>Scapy</strong> — Capture and dissect packets using Python’s most powerful packet manipulation library.</li>
  <li><strong>Rich</strong> — Build real-time dashboards with colorful tables and live updates.</li>
  <li><strong>Matplotlib</strong> — Generate protocol distribution charts, bandwidth graphs, and top talker visualizations.</li>
</ul>

<h2>Prerequisites</h2>

<p>Before starting, you should understand:</p>

<h3>Required Knowledge</h3>
<ul>
  <li><strong>Python basics</strong> — Dataclasses, type hints, context managers, async/await.</li>
  <li><strong>TCP/IP networking</strong> — IP addresses, TCP vs UDP, common ports, three-way handshake.</li>
  <li><strong>Command line usage</strong> — Running CLI tools, navigating directories, reading output.</li>
</ul>

<h3>Tools You'll Need</h3>
<ul>
  <li><strong>Python 3.14+</strong></li>
  <li><strong>Root/admin access</strong> for packet capture</li>
  <li><strong>Scapy, Rich, Matplotlib</strong> (installed via pip)</li>
</ul>

<h3>Helpful but Not Required</h3>
<ul>
  <li>Wireshark experience</li>
  <li>Basic systems programming knowledge</li>
</ul>

<h2>Quick Start</h2>

<p>Get the project running locally:</p>

<pre><code># Navigate to the project directory
cd network-traffic-analyzer

# Install dependencies
pip install -e .

# List available network interfaces
sudo netanal interfaces

# Capture 50 packets on your loopback interface
sudo netanal capture -i lo -c 50 --verbose

# Analyze an existing pcap file
netanal analyze traffic.pcap --top-talkers 20

# Generate charts from captured data
netanal chart traffic.pcap --type all -d ./charts/
</code></pre>

<p><strong>Expected output:</strong> A real-time packet stream showing source/destination IPs, protocols, and packet sizes. After capture, summary statistics and charts are generated.</p>

<h2>Project Structure</h2>

<pre><code>network-traffic-analyzer/
├── src/netanal/
│   ├── capture.py        # Producer-consumer packet capture engine
│   ├── analyzer.py       # Protocol identification and packet parsing
│   ├── filters.py        # BPF filter builder with validation
│   ├── statistics.py     # Thread-safe stats collector
│   ├── models.py         # Data structures (PacketInfo, Protocol enum)
│   ├── visualization.py  # Matplotlib chart generation
│   ├── export.py         # JSON/CSV data export
│   ├── output.py         # Rich console formatting
│   ├── main.py           # Typer CLI command definitions
│   ├── constants.py      # Configuration values
│   └── exceptions.py     # Custom exception hierarchy
├── tests/
│   ├── test_filters.py   # BPF filter builder tests
│   └── test_models.py    # Data model tests
└── pyproject.toml        # Project dependencies and metadata
</code></pre>

<h2>Next Steps</h2>

<ol>
  <li><strong>Understand the concepts</strong> — See <code>docs/00-OVERVIEW.md</code></li>
  <li><strong>Study the architecture</strong> — See <code>docs/03-ARCHITECTURE.md</code></li>
  <li><strong>Walk through the code</strong> — See <code>docs/01-LAB-GUIDE.md</code></li>
  <li><strong>Extend the project</strong> — See <code>docs/04-CHALLENGES.md</code></li>
</ol>

<h2>Common Issues</h2>

<p><strong>Permission denied when capturing packets</strong></p>
<pre><code>PermissionError: [Errno 1] Operation not permitted
</code></pre>
<p>Run with <code>sudo</code> or grant CAP_NET_RAW:</p>
<pre><code>sudo setcap cap_net_raw+ep $(which python3)
</code></pre>

<p><strong>Npcap not installed (Windows)</strong></p>
<pre><code>NpcapNotFoundError: Npcap is not installed
</code></pre>
<p>Install from <a href="https://npcap.com">https://npcap.com</a></p>

<p><strong>No packets captured on wireless interface</strong></p>
<pre><code>Total Packets: 0
</code></pre>
<p>Many wireless adapters block promiscuous mode. Try loopback (<code>lo</code>) or use monitor mode.</p>

<h2>Related Projects</h2>

<ul>
  <li><strong>Port Scanner</strong> — Active probing using raw sockets.</li>
  <li><strong>Intrusion Detection System</strong> — Signature-based packet inspection.</li>
  <li><strong>SSL/TLS Inspector</strong> — Analyze encrypted traffic metadata.</li>
</ul>


<h2>🔒 Educational Purpose</h2>

<p>
This project is intended for defensive security learning, network engineering education, and understanding packet capture internals.
Use only in controlled environments where you have authorization to capture traffic.
</p>
