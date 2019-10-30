from common.abstracts import MalParserBase
from structs.waterbear import Waterbear
from lib.struct_formatter import dive_struct

class MalParser(MalParserBase):
	def __init__(self):
		super().__init__()
		self.cfg_structs = Waterbear
		self.magic = b'\x00\x30\x2E(?:\x31|\x32|\x33).{13}(?:\x4D|\x20)'
		self.cfg_start_offset = -0x13
		self.cfg_size = 0xb0
		self.json_key = ['pattern', 'version', 'mutex', 'c2_server', 'port']

	def make_json(self):
		self.pretty_cfg = {}
		for key in self.raw_cfg.__dict__:
			if key not in self.json_key:
				continue
			value = self.raw_cfg.__dict__[key]
			if key == 'c2_server':
				if b'\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff' in value:
				    value = b"".join(bytes([offset ^ 0xff]) for offset in value)
				self.pretty_cfg[key] = value.decode('utf-8','ignore').rstrip('\x00')
			else:
			    dict_strcut = dive_struct(key, value)
			    self.pretty_cfg.update(dict_strcut)