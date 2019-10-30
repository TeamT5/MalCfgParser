meta:
  id: waterbear
  endian: le

seq:
  - id: pattern
    size: 0x10
  - id: len
    type: u4
  - id: version
    type: str
    encoding: ASCII
    size: 0x10
  - id: mutex
    type: str
    encoding: ASCII
    size: 0x10
  - id: c2_server
    size: 0x78
  - id: port
    type: u2
    
  