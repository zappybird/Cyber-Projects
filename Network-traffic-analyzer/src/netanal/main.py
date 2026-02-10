import typer
from netanal.capture import capture_packets
from netanal.parser import parse_packet
from netanal.detectors import detect_syn_flood
from netanal.stats import update_stats

app = typer.Typer()

def handle_packet(pkt):
    parsed = parse_packet(pkt)
    if not parsed:
        return

    update_stats(parsed)

    alert = detect_syn_flood(parsed)
    if alert:
        typer.echo(f"[ALERT] {alert}")

@app.command()
def capture(interface: str = "eth0", count: int = 0):
    """
    Capture live packets from an interface.
    """
    typer.echo(f"Starting capture on {interface}...")
    capture_packets(handle_packet, interface=interface, count=count)

def run():
    app()
