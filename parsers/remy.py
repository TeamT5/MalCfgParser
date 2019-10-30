from common.abstracts import MalParserBase
from structs.remy import Remy
from lib.struct_formatter import dive_struct


class MalParser(MalParserBase):
	def __init__(self):
		super().__init__()
		self.cfg_structs = Remy
		self.magic = b'\w{1,10}\.\w{1,20}\.\w{1,6}:\d{4}\x0a'
		self.cfg_start_offset = 0
		self.cfg_size = 0x100
		self.json_key = ['c2_blocks']

	def make_json(self):
		self.pretty_cfg = {}
		print(self.raw_cfg.__dict__)
		for key in self.raw_cfg.__dict__:
			if key not in self.json_key:
				continue
			value = self.raw_cfg.__dict__[key]
			if key == 'c2_blocks':
			    self.pretty_cfg['c2_blocks'] = []
			    for c2_block in value:
				    c2_server = c2_block.__dict__['c2_server']
				    port = c2_block.__dict__['port']
				    self.pretty_cfg[key].append({'c2_server': c2_server, 'port':port})
