meta:
  id: unicode_string
  endian: le
seq:
  - id: len
    type: u4
  - id: val
    type: str
    size: len
    encoding: UTF-8