import sys
import os
import importlib
import yara
import subprocess
import configparser

from lib.vmcontrol import VMControl


class Config(object):
	def __init__(self, cfg_file):
		self._read_config(cfg_file)

	def _read_config(self, cfg_file):
		config = configparser.ConfigParser()
		config.read(cfg_file)
		for key in config['default']:
			setattr(self, key, config['default'][key])

class PidHandler(object):
	def __init__(self, config, param1):
		self.config = config
		self.param1 = param1
		self.memdumper_filename = 'memdumper.py'
		self.memdumper_local_path = os.path.abspath(os.path.join('lib', self.memdumper_filename))
		self.memdumper_remote_path = self.config.work_folder + '\\' + self.memdumper_filename
		self.dump_files_folder = 'memdump_' + self.param1
		self.dump_files_local_path = os.path.abspath(os.path.join(self.config.dump_files_folder, self.dump_files_folder))
		self.dump_files_remote_path = self.config.work_folder + '\\' + self.dump_files_folder
		self.my_vmcontrol = VMControl(self.config)

	def _create_work_folder(self):
		
		status, errors = self.my_vmcontrol.exec_cmd('dir '+self.config.work_folder)
		# errors when dir does not exists
		if status:
			print('[+] work_folder {} was already in VM'.format(self.config.work_folder))
			return

		status, errors = self.my_vmcontrol.exec_cmd('mkdir '+self.config.work_folder)
		if status:
			print('[+] work_folder {} was created in VM'.format(self.config.work_folder))
		else:
			print('[!] Error when creating work_folder: {}'.format(result))
			exit()

	def _send_memdumper(self):
		if not os.path.isfile(self.memdumper_local_path):
			print('[!] {} does not exists'.format(self.memdumper_local_path))
			exit()
		
		status, errors = self.my_vmcontrol.send_file(self.memdumper_local_path, self.memdumper_remote_path)
		if status:
			print('[+] memdumper.py is transmitted to VM')
		else:
			print('[!] Error when sending memdumper: {}'.format(result))
			exit()

	def _retreive_dump_file(self):
		status, errors = self.my_vmcontrol.retrieve_file(self.dump_files_remote_path, self.dump_files_local_path)
		if status:
			print('[+] Memory dump files from VM are retreived')
		else:
			print('[!] Error when retreiving memory dump files: {}'.format(result))
			exit()

	def _memdump_by_pid(self,pid):
		status, errors = self.my_vmcontrol.exec_cmd('{} {}'.format(self.memdumper_remote_path, pid))
		if status:
			print('[+] Memory dump {} is OK in VM'.format(param1))
		else:
			print('[!] Error when dumping memory: {}'.format(result))
			exit()
	def parse_memdump_folder(self,memdump_folder):
		memdmp_data = b''
		for memdump_file_path in os.listdir(self.dump_files_local_path):
			with open(os.path.join(self.dump_files_local_path, memdump_file_path), 'rb') as f:
				memdmp_data += f.read()

		mem_handler = MemoryHandler()
		matches = mem_handler._yara_scan(memdmp_data)
		if matches:
			match = matches[0].rule
			print('[+] Detect: {}'.format(match))
			results = {'raw_memory':memdmp_data, 'match':match}
			ret = mem_handler._parse_results(results)

			if not ret and once:
				print('[!] Not able to parse config properly.')
				exit()
			else:
				return ret

		print('[!] No supported malware detected.')

	def memdump_by_pid(self,pid):
		self._create_work_folder()
		self._send_memdumper()
		self._memdump_by_pid(pid)
		return self._retreive_dump_file()

	def run(self):
		files =  self.memdump_by_pid(int(self.param1))
		self.parse_memdump_folder(files)

class MemoryHandler():
	def __init__(self):
		pass

	def _yara_scan(self, memblock):
		rules = yara.compile('yara.txt', includes=True)
		matches = rules.match(data=memblock)
		return matches

	def _put_on_parser(self, results):
		imported_module = importlib.import_module("parsers."+results['match'])

		malparser_class = getattr(imported_module, "MalParser")
		malparser_instance = malparser_class()
		malparser_instance.mem_parse(results['raw_memory'])
		return malparser_instance

	def _parse_results(self, results):
		malparser_instance = self._put_on_parser(results)
		
		if malparser_instance.pretty_cfg:
			for key in malparser_instance.pretty_cfg:
				print('{}: {}'.format(key, malparser_instance.pretty_cfg[key]))
			return True

def parse_memdump_file(memdump_file_path, once=True):
	memdmp_data = None
	with open(memdump_file_path, 'rb') as f:
		memdmp_data = f.read()

		mem_handler = MemoryHandler()
		matches = mem_handler._yara_scan(memdmp_data)
		if matches:
			match = matches[0].rule
			print('[+] Detect: {}'.format(match))
			results = {'raw_memory':memdmp_data, 'match':match}
			ret = mem_handler._parse_results(results)

			if not ret and once:
				print('[!] Not able to parse config properly.')
				exit()
			else:
				return ret

if __name__ == '__main__':

	if len(sys.argv) < 2:
		print ("Syntex : \n\t%s ( [pid] | [proc dump file] | [cfg blob] [parsers] )" % sys.argv[0])
		exit()

	param1 = sys.argv[1]

	if param1.isnumeric():
		config = Config('default.cfg')
		if 'vmx' not in dir(config) and os.path.isfile(config.vmx):
			print('[!] Please set correct `vmx` file path of VM in default.cfg.')
			exit()
		if 'vmrun' not in dir(config):
			print('[!] Please set `vmrun` path of VMWare in default.cfg.')
			exit()
		else:
			result, error = subprocess.Popen([config.vmrun], stdout=subprocess.PIPE).communicate()
			if error:
				print('[!] Please set  correct `vmrun` path of VMWare in default.cfg.')
				exit()
		if 'work_folder' not in dir(config):
			print('[!] Please set correct`work_folder` in default.cfg to specify the workspace in VM.')
			exit()

		handler = PidHandler(config, param1)
		handler.run()

	elif os.path.isfile(param1):
		if not parse_memdump_file(param1):
			print('[!] No supported malware detected.')
	else:
		print('[!] Input PID or process dump file.')


