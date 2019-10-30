meta:
  id: plugx_x2_0x724
  endian: le
seq:
  - id: flag
    type: u4
  - id: installname
    type: str
    encoding: ASCII
    size: 0x100
  - id: cnc
    type: cnc
    repeat: expr
    repeat-expr: 4

enums:
  protocol:
    0: unknown
    1: tcp
    2: http
    3: tcp_http
    4: udp
    5: tcp_udp
    6: http_udp
    7: tcp_http_udp
    8: icmp
    16: dns
    31: unknown

types:
  cnc:
    seq:
      - id: proto
        type: u2
        enum: protocol
      - id: port
        type: u2
      - id: host
        type: str
        encoding: ASCII
        size: 0xc0