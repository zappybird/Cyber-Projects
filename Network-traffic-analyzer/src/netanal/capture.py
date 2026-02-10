from scapy.all import sniff

def capture_packets(callback, count=0, iface=None):
    sniff(prn=callback, count=count, iface=iface, store=False)
