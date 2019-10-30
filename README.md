# MalCfgParser

![](https://github.com/teamt5/malcfgparser/raw/master/logo.png)

MalCfgParser is a malware configuration parser that:

- Brute-forcely parses memory -- No need to decode and specify the configuration size!
- Accepts the PID or use process dump files
- Easy to implement your parser by adding yara and malware configuration structs

## Requirements
### Local machine
- VMWare
- python3
- yara-python
> For Windows, the installers are put under `requirements`

### Remote machine: Windows7 on VMware
- python (Any version is OK)

## Configuration
In default.cfg, set up:
```
vmrun=<Path to vmrun>
vmx=<Path to vmx file of remote machine>
vm_user=<Username of remote machine>
vm_password=<Password of remote machine>
work_folder=<Workspace in remote machine, work_folder=C:\MalCfgParser by default>
dump_files_folder=<Folder to save the memory dump files in local machine>
```

## Usage
### Parse by PID in running machine
```
> python3 main.py <pid>
```

Example: 
```
> python3 main.py 6264
[+] work_folder C:\MalCfgParser was already in VM
[+] memdumper.py is transmitted to VM
[+] Memory dump 6264 is OK in VM
[+] Memory dump files from VM are retreived
[+] Detect: phantomivy
password: Ib@1ie
cnc0_type: 0
cnc0_port: 80
cnc0_host: 5.189.173.32
cnc1_type: 0
cnc1_port: 8081
cnc1_host: 5.189.173.32
mutex: C^Xe3(@Yx
```

### Parse by memory dump file
```
> python3 main.py <memory dump file>
```

Example:
```
> python3 main.py test/malware/plugx_0x2d58/memdump/iexplore.exe_0x300000-0x2a000.bin
[+] Detect: plugx_0x724
flag: 1000
installname: Microsoft Malware ProtectionoYS
cnc0_proto: TCP
cnc0_port: 80
cnc0_host: update.olk4.com
cnc1_proto: TCP
cnc1_port: 8080
cnc1_host: update.olk4.com
cnc2_proto: TCP
cnc2_port: 80
cnc2_host: www.olk4.com
cnc3_proto: TCP
cnc3_port: 8080
cnc3_host: www.olk4.com
```

## Add Your Malware Configuration Parser
- Add yara signature for the malware to `yara.txt`
- Use Kaitai (https://ide.kaitai.io) to parse the configuration
- Generate the python file for structure parsing by `kaitai-struct-compiler --target python <malware_name>.ksy`
- Move `<malware_name>.py` to `/structs`
- Add `<malware_name>.py`  to `/parsers`

### Design of Parser
```
class MalParser(MalParserBase):
	def __init__(self):
		super().__init__()
		self.cfg_structs = <The structure parsing file name>
		self.magic = <Signature to help identify the start of configuration>
		self.cfg_start_offset = <The offset of the magic to configuration>
		self.cfg_size = <Configuration size>
		self.json_key = <A list cotains the key to print in json format>

	def make_json(self):
	   # (Required) Implement the parse result shown in json format 
	   pass

	def validate(self):
	   # (Required) To validate the parse result is correct or not
	   pass
	   
	def decode(self):
	   # (Optional) Additional decode on the configuration block
	   pase
```