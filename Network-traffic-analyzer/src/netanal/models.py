from dataclasses import dataclass
from enum import Enum
from typing import Optional


class Protocol(Enum):
    TCP = "TCP"
    UDP = "UDP"
    ICMP = "ICMP"
    DNS = "DNS"
    HTTP = "HTTP"
    HTTPS = "HTTPS"
    OTHER = "OTHER"


@dataclass
class PacketInfo:
    timestamp: float
    src_ip: str
    dst_ip: str
    protocol: Protocol
    size: int
    src_port: Optional[int] = None
    dst_port: Optional[int] = None
