from scapy.layers.inet import IP, TCP, UDP

def parse_packet(pkt):
    if IP not in pkt:
        return None

    data = {
        "src": pkt[IP].src,
        "dst": pkt[IP].dst,
        "protocol": pkt[IP].proto,
        "length": pkt[IP].len
    }

    if TCP in pkt:
        data.update({
            "type": "TCP",
            "sport": pkt[TCP].sport,
            "dport": pkt[TCP].dport,
            "flags": pkt[TCP].flags
        })

    elif UDP in pkt:
        data.update({
            "type": "UDP",
            "sport": pkt[UDP].sport,
            "dport": pkt[UDP].dport
        })

    return data
