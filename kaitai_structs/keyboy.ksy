meta:
  id: keyboy
  endian: be
seq:
  - id: magic
    type: str
    encoding: ASCII
    size: 0x40
  - id: reverse_host_1
    type: str
    encoding: ASCII
    size: 0x40
  - id: reverse_host_2
    type: str
    encoding: ASCII
    size: 0x40
  - id: reverse_host_3
    type: str
    encoding: ASCII
    size: 0x40
  - id: reverse_port_1
    type: str
    encoding: ASCII
    size: 0x40
  - id: reverse_port_2
    type: str
    encoding: ASCII
    size: 0x40
  - id: reverse_port_3
    type: str
    encoding: ASCII
    size: 0x40
  - id: payload_url_1
    type: str
    encoding: ASCII
    size: 0x80
  - id: payload_url_2
    type: str
    encoding: ASCII
    size: 0x80
  - id: payload_url_3
    type: str
    encoding: ASCII
    size: 0x80
  - id: control_port
    type: str
    encoding: ASCII
    size: 0x40
  - id: login_password
    type: str
    encoding: ASCII
    size: 0x40
  - id: campaign_code
    type: str
    encoding: ASCII
    size: 0x40
  - id: usb
    type: str
    encoding: ASCII
    size: 0x40