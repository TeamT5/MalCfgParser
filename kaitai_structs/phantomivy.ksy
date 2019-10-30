meta:
  id: phantomivy
  endian: le
seq:
  - id: password
    type: str
    encoding: ASCII
    size: 0x10
  - id: unused
    size: 0x37
  - id: cnc_count
    type: u4
  - id: cnc
    type: cnc
    repeat: expr
    repeat-expr: cnc_count+1

instances:
   mutex:
    io: _root._io
    pos: 0x2b6
    size: 0x9
    type: str
    encoding: ASCII

types:
  cnc:
    seq:
      - id: len
        type: u1
      - id: host
        type: str
        encoding: ASCII
        size: len
      - id: type
        type: u1
      - id: port
        type: u2
      