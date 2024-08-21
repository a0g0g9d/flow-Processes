# Chunk size of reading the flow logs
CHUNK_SIZE = 1024 * 1024  # 1 MB chunk size

# File encoding types
ENCODING = {
    'ASCII': 'ascii',
    'UTF8': 'utf-8'
}
# Define constants for protocol numbers
TCP = 6
UDP = 17
ICMP = 1
IGMP = 2
GRE = 47
ESP = 50
AH = 51
EIGRP = 88
OSPF = 89
SCTP = 132

# Protocol mapping dictionary
PROTOCOL_MAP = {
    TCP: 'tcp',
    UDP: 'udp',
    ICMP: 'icmp',
    IGMP: 'igmp',
    GRE: 'gre',
    ESP: 'esp',
    AH: 'ah',
    EIGRP: 'eigrp',
    OSPF: 'ospf',
    SCTP: 'sctp'
}