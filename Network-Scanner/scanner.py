import socket
import nmap
from datetime import datetime


# ──────────────────────────────────────────────
# ANSI color codes for terminal formatting
# ──────────────────────────────────────────────
class Color:
    HEADER = '\033[95m'
    BLUE   = '\033[94m'
    CYAN   = '\033[96m'
    GREEN  = '\033[92m'
    YELLOW = '\033[93m'
    RED    = '\033[91m'
    BOLD   = '\033[1m'
    RESET  = '\033[0m'


def divider(char="─", length=50):
    print(Color.BLUE + char * length + Color.RESET)


def section_header(title):
    divider()
    print(f"{Color.BOLD}{Color.CYAN}  {title}{Color.RESET}")
    divider()


# ──────────────────────────────────────────────
# Core scanning functions
# ──────────────────────────────────────────────
def port_scan(target, start_port, end_port):
    open_ports = []
    for port in range(start_port, end_port + 1):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        result = sock.connect_ex((target, port))
        if result == 0:
            open_ports.append(port)
        sock.close()
    return open_ports


def banner_grab(target, port):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(2)
            sock.connect((target, port))
            banner = sock.recv(1024).decode('utf-8', errors='ignore')
            return banner.strip()
    except (socket.timeout, ConnectionRefusedError, OSError):
        return None


def vulnerability_scan(target):
    nm = nmap.PortScanner()
    try:
        nm.scan(hosts=target, arguments="-O -sV --script=vuln")
        return nm[target]
    except Exception as e:
        print(f"{Color.RED}  [!] Error during vulnerability scan: {e}{Color.RESET}")
        return None


# ──────────────────────────────────────────────
# Formatted output functions
# ──────────────────────────────────────────────
def print_open_ports(open_ports, banners):
    section_header("PORT SCAN RESULTS")
    if not open_ports:
        print(f"  {Color.YELLOW}No open ports found in the scanned range.{Color.RESET}")
        return

    print(f"  {'PORT':<10} {'STATE':<20} {'BANNER'}")
    print(f"  {'────':<10} {'─────':<20} {'──────'}")
    for port in open_ports:
        banner = banners.get(port) or "—"
        state  = f"{Color.GREEN}OPEN{Color.RESET}"
        print(f"  {port:<10} {state:<29} {banner}")


def print_host_info(vuln_info):
    section_header("HOST INFORMATION")

    hostnames = vuln_info.get('hostnames', [])
    if hostnames:
        names = ", ".join(h['name'] for h in hostnames if h.get('name'))
        print(f"  {Color.BOLD}Hostname(s):{Color.RESET}  {names}")

    os_matches = vuln_info.get('osmatch', [])
    if os_matches:
        print(f"\n  {Color.BOLD}OS Detection (Top Matches):{Color.RESET}")
        for i, match in enumerate(os_matches[:3], start=1):
            name     = match.get('name', 'Unknown')
            accuracy = match.get('accuracy', '?')
            osclass  = match.get('osclass', [{}])
            dev_type = osclass[0].get('type', '—') if osclass else '—'
            print(f"    {i}. {name}")
            print(f"       Accuracy: {accuracy}%   |   Type: {dev_type}")
    else:
        print(f"  {Color.YELLOW}No OS match data available.{Color.RESET}")


def print_vulns(vuln_info):
    section_header("VULNERABILITY SCAN")
    vulns = vuln_info.get('vulns')
    if not vulns:
        print(f"  {Color.GREEN}No known vulnerabilities detected.{Color.RESET}")
        return
    for vuln_id, details in vulns.items():
        state = details.get('state', 'unknown')
        color = Color.RED if state == 'VULNERABLE' else Color.YELLOW
        print(f"  {color}[{state}]{Color.RESET}  {vuln_id}")
        if details.get('description'):
            desc = details['description'].strip().replace('\n', ' ')
            print(f"    └─ {desc[:120]}{'...' if len(desc) > 120 else ''}")


# ──────────────────────────────────────────────
# Main scan orchestrator
# ──────────────────────────────────────────────
def network_scan(target, start_port, end_port):
    start_time = datetime.now()

    print(f"\n{Color.BOLD}{Color.HEADER}{'═' * 50}{Color.RESET}")
    print(f"{Color.BOLD}{Color.HEADER}   NETWORK SCANNER{Color.RESET}")
    print(f"{Color.BOLD}{Color.HEADER}{'═' * 50}{Color.RESET}")
    print(f"  Target : {Color.CYAN}{target}{Color.RESET}")
    print(f"  Ports  : {start_port} → {end_port}")
    print(f"  Started: {start_time.strftime('%Y-%m-%d %H:%M:%S')}\n")

    print(f"  {Color.YELLOW}[*] Running port scan...{Color.RESET}")
    open_ports = port_scan(target, start_port, end_port)

    print(f"  {Color.YELLOW}[*] Grabbing banners...{Color.RESET}")
    banners = {}
    for port in open_ports:
        banners[port] = banner_grab(target, port)

    print(f"  {Color.YELLOW}[*] Running vulnerability scan (this may take a while)...{Color.RESET}\n")
    vuln_info = vulnerability_scan(target)

    print_open_ports(open_ports, banners)

    if vuln_info:
        print_host_info(vuln_info)
        print_vulns(vuln_info)
    else:
        section_header("HOST & VULNERABILITY INFO")
        print(f"  {Color.RED}No data returned from vulnerability scan.{Color.RESET}")

    end_time = datetime.now()
    elapsed  = end_time - start_time
    divider("═")
    print(f"  Scan completed at {end_time.strftime('%H:%M:%S')}  |  Duration: {str(elapsed).split('.')[0]}")
    divider("═")
    print()


if __name__ == "__main__":
    target_ip  = input("Enter the target IP address: ")
    start_port = int(input("Enter the starting port number: "))
    end_port   = int(input("Enter the ending port number: "))
    network_scan(target_ip, start_port, end_port)