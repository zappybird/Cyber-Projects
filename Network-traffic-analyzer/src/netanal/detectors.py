from collections import defaultdict

syn_counter = defaultdict(int)

def detect_syn_flood(packet):
    if packet.get("type") == "TCP" and "S" in str(packet.get("flags")):
        syn_counter[packet["src"]] += 1
        if syn_counter[packet["src"]] > 100:
            return f"Possible SYN flood from {packet['src']}"
