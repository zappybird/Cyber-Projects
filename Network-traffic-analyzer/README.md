<h2>📘 Network Traffic Analyzer Lab</h2>

<p>
This project demonstrates how a modern, Python-based network traffic analyzer is built and operated end-to-end.
It focuses on safe, structured packet capture, protocol classification, and statistics aggregation using a producer–consumer architecture,
Scapy for packet dissection, and Rich/Matplotlib for visualization.
</p>

<p>
By running this on a Raspberry Pi (or Pi-hosted VM), you get a practical feel for how real monitoring tools ingest traffic,
avoid packet loss under load, and turn raw packets into actionable insights like protocol distribution, bandwidth trends, and top talkers.
</p>

<hr />

<h2>🎯 Objective</h2>

<ul>
<li>Understand how the capture engine uses a bounded queue and background threads to avoid dropping packets.</li>
<li>Observe live protocol distribution, bandwidth, and endpoint statistics on a real network segment.</li>
<li>See how BPF filters offload work to the kernel for performance and safety.</li>
<li>Connect the CLI commands (<code>netanal capture</code>, filters, stats) to the underlying modules in <code>src/netanal/</code>.</li>
</ul>

<hr />

<h2>🧪 Lab Environment</h2>

<ul>
<li><strong>Host:</strong> Raspberry Pi (or Pi-hosted VM) running a recent Linux distribution.</li>
<li><strong>Python:</strong> Python 3.14 installed on the Pi/VM.</li>
<li><strong>Project:</strong> Your <code>Cyber-Projects</code> repo cloned locally, using the <code>Network-traffic-analyzer</code> subfolder.</li>
<li><strong>Networking:</strong> Either the Pi’s physical interface (e.g., <code>eth0</code>, <code>wlan0</code>) or a VM interface (e.g., <code>ens33</code>).</li>
<li><strong>Permissions:</strong> Ability to run packet capture (root or appropriate capabilities).</li>
</ul>

<hr />

<h2>🖥️ Setting Up the VM (VirtualBox)</h2>

<p>
If you prefer to run this lab inside a virtual machine instead of directly on a Raspberry Pi, VirtualBox provides an easy and isolated environment for testing packet capture tools.
Below is a step-by-step guide to setting up a Linux VM suitable for running the Network Traffic Analyzer.
</p>

<h3>1. Download and Install VirtualBox</h3>
<ul>
<li>Visit: <a href="https://www.virtualbox.org/">https://www.virtualbox.org/</a></li>
<li>Download the latest version for your operating system.</li>
<li>Install using the default settings.</li>
</ul>

<h3>2. Download a Linux ISO</h3>
<p>Recommended options:</p>
<ul>
<li><strong>Ubuntu Server</strong> (lightweight, ideal for CLI tools)</li>
<li><strong>Ubuntu Desktop</strong> (if you prefer a GUI)</li>
<li><strong>Debian</strong> (stable and minimal)</li>
</ul>

<h3>3. Create a New Virtual Machine</h3>
<ul>
<li>Open VirtualBox → <strong>New</strong></li>
<li>Name: <code>NetAnal-VM</code></li>
<li>Type: <strong>Linux</strong></li>
<li>Version: <strong>Ubuntu (64-bit)</strong> or your chosen distro</li>
<li>Memory: <strong>2GB–4GB</strong></li>
<li>Disk: <strong>20GB</strong> dynamically allocated</li>
</ul>

<h3>4. Configure Networking</h3>
<p>
To capture real traffic, the VM must be attached to a network mode that exposes actual packets.
</p>

<ul>
<li>Go to <strong>Settings → Network</strong></li>
<li>Set <strong>Adapter 1</strong> to:
<ul>
<li><strong>Bridged Adapter</strong> (recommended — VM behaves like a real device on your LAN)</li>
<li>or <strong>Host-Only Adapter</strong> (isolated testing)</li>
</ul>
</li>
<li>Enable <strong>Promiscuous Mode → Allow All</strong></li>
</ul>

<p><strong>Why this matters:</strong> Promiscuous mode allows the VM to see packets not addressed directly to it, which is essential for realistic packet capture.</p>

<h3>5. Boot and Install Linux</h3>
<ul>
<li>Start the VM</li>
<li>Select your downloaded ISO</li>
<li>Install Linux using default settings</li>
</ul>

<h3>6. Install Python 3.14</h3>
<p>Inside the VM:</p>
<pre><code>sudo apt update
sudo apt install python3.14 python3.14-venv python3.14-dev
</code></pre>

<h3>7. Install Git</h3>
<pre><code>sudo apt install git
</code></pre>

<p>Your VM is now ready to run the Network Traffic Analyzer.</p>

<hr />

<h2>🛠 Tools</h2>

<h3>Python 3.14 + Virtual Environment</h3>
<p>
The analyzer is packaged as a modern Python project using <code>pyproject.toml</code> and Hatch.
A dedicated virtual environment keeps dependencies isolated and ensures the correct interpreter version is used.
</p>

<h3>Scapy</h3>
<p>
A powerful packet manipulation library used under the hood for live capture and protocol dissection.
It feeds raw packets into the capture engine’s queue for further analysis.
</p>

<h3>Typer CLI</h3>
<p>
A modern command-line framework that powers the <code>netanal</code> command.
Each subcommand (e.g., <code>capture</code>) maps directly to functions in <code>src/netanal/main.py</code>.
</p>

<hr />

<h2>📦 Setup & Installation (on the Pi / VM)</h2>

<h3>1. Clone the Cyber-Projects repository</h3>
<pre><code>cd ~
git clone https://github.com/&lt;your-username&gt;/Cyber-Projects.git
cd Cyber-Projects/Network-traffic-analyzer
</code></pre>

<h3>2. Create and activate a virtual environment (Python 3.14)</h3>
<pre><code>python3.14 -m venv .venv
source .venv/bin/activate
</code></pre>

<h3>3. Install the analyzer in editable mode</h3>
<p>This uses <code>pyproject.toml</code> and Hatchling to expose the <code>netanal</code> CLI.</p>
<pre><code>pip install --upgrade pip
pip install -e .
</code></pre>

<h3>4. Verify the CLI is available</h3>
<pre><code>netanal --help
</code></pre>

<p>
You should see Typer-generated help output listing commands like <code>capture</code>.
If this fails, confirm you are inside the virtual environment and that <code>pyproject.toml</code> is in the current directory.
</p>

<hr />

<h2>📡 Discovering Interfaces & Permissions</h2>

<h3>1. List available interfaces</h3>
<pre><code>sudo netanal interfaces
</code></pre>

<p>
This command queries the system for capture-capable interfaces and prints them using Rich tables.
Internally, it calls helper functions in <code>capture.py</code> to enumerate interfaces and format them for display.
</p>

<h3>2. Check capture permissions</h3>
<pre><code>sudo netanal capture --help
</code></pre>

<p>
If you lack permissions, the tool will surface a clear, platform-specific error message (e.g., requiring root, CAP_NET_RAW, or Npcap+Admin).
This logic lives in <code>check_capture_permissions()</code> inside <code>capture.py</code>, which branches on the OS and tests raw socket access.
</p>

<hr />

<h2>🎧 Running a Basic Capture</h2>

<h3>1. Start a short capture on a chosen interface</h3>
<pre><code>sudo netanal capture -i eth0 -c 50 --verbose
</code></pre>

<ul>
<li><strong>-i eth0</strong>: Interface to capture on (replace with your Pi/VM interface).</li>
<li><strong>-c 50</strong>: Stop after 50 packets.</li>
<li><strong>--verbose</strong>: Print per-packet details as they are processed.</li>
</ul>

<p>
Under the hood, this command:
</p>
<ul>
<li>Builds a <code>CaptureConfig</code> dataclass instance in <code>main.py</code>.</li>
<li>Instantiates <code>CaptureEngine</code> from <code>capture.py</code> with that config.</li>
<li>Starts an <code>AsyncSniffer</code> producer and a consumer thread reading from a bounded <code>Queue[Packet]</code>.</li>
<li>Transforms raw packets into <code>PacketInfo</code> models and records them via <code>StatisticsCollector</code>.</li>
</ul>

<h3>2. Observe the output</h3>
<p>
As packets flow, verbose mode uses functions in <code>output.py</code> to render human-readable summaries.
When the capture ends, Rich tables summarize protocol distribution, bandwidth, and top talkers based on data from <code>statistics.py</code>.
</p>

<hr />

<h2>🎛 Using BPF Filters (Kernel-Level Filtering)</h2>

<h3>1. Capture only HTTP traffic</h3>
<pre><code>sudo netanal capture -i eth0 --filter "tcp port 80" -c 50
</code></pre>

<p>
The <code>--filter</code> argument is passed directly into Scapy’s <code>AsyncSniffer</code> as a BPF expression.
Before capture starts, <code>validate_bpf_filter()</code> in <code>filters.py</code> compiles the filter to catch syntax errors early.
</p>

<h3>2. Build filters programmatically (conceptual)</h3>
<p>
Internally, the project uses a <code>FilterBuilder</code> class in <code>filters.py</code> to construct safe BPF expressions:
</p>
<pre><code>builder = FilterBuilder().protocol(Protocol.HTTP).port(80)
expr = builder.build()
</code></pre>

<p>
This pattern prevents injection and enforces valid ports/IPs via helper validators, ensuring only well-formed filters reach the kernel.
</p>

<hr />

<h2>📊 Inspecting Protocol & Endpoint Statistics</h2>

<h3>1. Run a capture with mixed traffic</h3>
<pre><code>sudo netanal capture -i eth0 -c 200
</code></pre>

<h3>2. Read the protocol distribution table</h3>
<p>
At the end of the capture, you’ll see a “Protocol Distribution” table.
This is generated by <code>print_protocol_table()</code> in <code>output.py</code>, which pulls from:
</p>

<ul>
<li><code>protocol_distribution</code> and <code>protocol_bytes</code> in <code>CaptureStatistics</code>.</li>
<li>Percentages computed by <code>get_protocol_percentages()</code> in <code>statistics.py</code>.</li>
</ul>

<p>
Behind the scenes, each packet is classified by <code>identify_protocol()</code> in <code>analyzer.py</code>,
which walks Scapy layers (DNS, TCP, UDP, ICMP, ARP) and uses ports to distinguish HTTP/HTTPS from generic TCP.
</p>

<h3>3. Observe top talkers</h3>
<p>
The “Top Talkers” section aggregates per-endpoint and per-conversation statistics.
This is driven by <code>_update_endpoint()</code> and <code>_update_conversation()</code> inside <code>statistics.py</code>,
all guarded by a single lock to keep counts consistent across threads.
</p>

<hr />

<h2>📈 Bandwidth & Performance Behavior</h2>

<h3>1. Run a longer capture</h3>
<pre><code>sudo netanal capture -i eth0 -c 1000
</code></pre>

<p>
During this run, the analyzer periodically samples bandwidth using <code>_check_bandwidth_sample()</code> in <code>statistics.py</code>.
It computes bytes/sec and packets/sec from interval counters and stores them as <code>BandwidthSample</code> entries.
</p>

<h3>2. Connect behavior to design</h3>

<ul>
<li>The bounded queue in <code>CaptureEngine</code> prevents unbounded memory growth.</li>
<li>Lock-protected counters ensure packet totals and protocol percentages remain accurate under concurrency.</li>
<li>BPF filters reduce user-space load by discarding irrelevant packets in the kernel.</li>
</ul>

<hr />

<h2>🔒 Educational Purpose</h2>

<p>
This lab is intended solely for defensive security and systems engineering education in a controlled environment.
It is designed to build intuition for how real-world network monitoring tools are architected:
from safe packet capture and protocol identification to thread-safe statistics and kernel-assisted filtering.
</p>

<p>
By experimenting on a Raspberry Pi or VM, you can safely explore how traffic patterns, filters, and load affect the analyzer’s behavior—
and connect those observations back to the underlying implementation in <code>src/netanal/</code>.
</p>