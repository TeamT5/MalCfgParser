meta:
  id: remy
  endian: le
seq:
  - id: c2_blocks
    type: c2_block
    repeat: expr
    repeat-expr: 8
      
types:
  c2_block:
    seq:
      - id: c2_server
        type: str
        terminator: 0x3a
        encoding: ASCII
      - id: port
        type: str
        terminator: 0xa
        encoding: ASCII