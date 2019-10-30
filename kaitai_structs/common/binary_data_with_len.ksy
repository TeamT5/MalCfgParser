meta:
  id: binary_data_with_len
  endian: le
seq:
  - id: len
    type: u4
  - id: val
    size: len
  