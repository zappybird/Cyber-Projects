from netanal.capture import capture_packets
from netanal.parser import parse_packet
from netanal.detectors import detect_syn_flood
from netanal.stats import update_stats

def handle_packet(pkt):
    parsed = parse_packet(pkt)
    if not parsed:
        return

    update_stats(parsed)

    alert = detect_syn_flood(parsed)
    if alert:
        print("[ALERT]", alert)

if __name__ == "__main__":
    print("Starting network analyzer...")
    capture_packets(handle_packet)
