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
