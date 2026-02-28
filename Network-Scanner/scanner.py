import socket
import requests
import nmap
from datetime import datetime

def port_scan(target, start_port, end_port): 
    print(f"Scanning ports from {start_port} to {end_port} on {target}...")
    open_ports = []
    for port in range(start_port, end_port + 1):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)  # Set a timeout for the connection attempt
        result = sock.connect_ex((target, port))
        if result == 0:
            open_ports.append(port)
        sock.close()
    return open_ports


def banner_grab(target, port):
    print(f"Grabbing banner for {target}:{port}...")
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(2)
            sock.connect((target, port))
            banner = sock.recv(1024).decode('utf-8', errors='ignore')
            return banner.strip()
    except (socket.timeout, ConnectionRefusedError, OSError):
        return None
    
def vulnerability_scan(target):
    print(f"Scanner target {target} for vulnerabilities...")
    nm = nmap.PortScanner()
    try:
        nm.scan(hosts=target, arguments="-O -sV --script=vuln")
        return nm[target]
    except Exception as e:
        print(f"Error scanning for vulnerabilities: {e}")
        return None
    
def network_scan(target, start_port, end_port): #scans a range of ports on a target IP address
    print(f"Scanning target: {target}...")
    start_time = datetime.now()

    open_ports = port_scan(target, start_port, end_port) #function returns open ports stored in this variable
    if open_ports:
        print(f"Open ports found: {target}: {open_ports}")
    else:
        print(f"No open ports found on {target}.")

    for port in open_ports:
        banner = banner_grab(target, port)
        if banner:
            print(f"Banner for {target}:{port} - {banner}")
        else:
            print(f"No banner found for {target}:{port}.")

    vuln_info = vulnerability_scan(target)
    if vuln_info:
        if 'hostnames' in vuln_info:
            print(f"Hostnames: {vuln_info['hostnames']}")
        if 'osmatch' in vuln_info:
            print(f"Operating System Match: {vuln_info['osmatch']}")
        if 'vulns' in vuln_info:
            print(f"Vulnerabilities: {vuln_info['vulns']}")
    else:
        print(f"No vulnerability information found for {target}.")

    end_time = datetime.now()
    print(f"Scan completed in: {end_time - start_time}")

if __name__ == "__main__":
    target_ip = input("Enter the target IP address: ")
    start_port = int(input("Enter the starting port number: "))
    end_port = int(input("Enter the ending port number: "))

    network_scan(target_ip, start_port, end_port)
