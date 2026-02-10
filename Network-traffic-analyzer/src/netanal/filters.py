import ipaddress

class FilterBuilder:
    def __init__(self):
        self.parts = []

    def port(self, port: int):
        if not 0 <= port <= 65535:
            raise ValueError("Invalid port")
        self.parts.append(f"port {port}")
        return self

    def host(self, ip: str):
        ipaddress.ip_address(ip)
        self.parts.append(f"host {ip}")
        return self

    def build(self):
        return " and ".join(self.parts) if self.parts else None
