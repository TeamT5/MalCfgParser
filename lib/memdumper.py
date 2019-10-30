import sys
import os
from ctypes import *

class MEMORY_BASIC_INFORMATION (Structure):
	_fields_ = [
		("BaseAddress",  c_ulong),
		("AllocationBase", c_ulong),
		("AllocationProtect", c_long),
		("RegionSize", c_long),
		("State", c_long),
		("Protect", c_long),
		("Type", c_long)]

OpenProcess = windll.kernel32.OpenProcess
ReadProcessMemory = windll.kernel32.ReadProcessMemory
GetLastError = windll.kernel32.GetLastError
CloseHandle = windll.kernel32.CloseHandle
VirtualQueryEx = windll.kernel32.VirtualQueryEx
WaitForInputIdle = windll.user32.WaitForInputIdle

PROCESS_ALL_ACCESS = 0x1F0FFF
MEM_COMMIT = 0x00001000
MEM_PRIVATE = 0x20000
PAGE_EXECUTE_READWRITE = 0x40

class MemDumper(object):
	def __init__(self, pid):
		self.work_folder = os.path.dirname(os.path.abspath(__file__))
		self.task_folder = 'memdump_{}'.format(pid)
		self.pid = pid
		self.current_task_path = os.path.join(self.work_folder, self.task_folder)
		if not os.path.exists(self.current_task_path):
			os.makedirs(self.current_task_path)
	
	def dump(self):
		hProcess = OpenProcess(PROCESS_ALL_ACCESS, False, self.pid)
		if hProcess == 0:
			print('[!] Unable to OpenProcess: {}'.format(GetLastError()))
			exit()

		memlist = []
		address = 0
		while True:
			mbi = MEMORY_BASIC_INFORMATION()
			size = c_int(sizeof(mbi))
			RetVal = VirtualQueryEx(hProcess, address, byref(mbi), size)
			if (RetVal == 0):
				break

			if (mbi.State == MEM_COMMIT and mbi.Type == MEM_PRIVATE and mbi.BaseAddress < 0x70000000):
				start = mbi.BaseAddress
				memlist.append(mbi)
			
			address = c_long(mbi.BaseAddress + mbi.RegionSize)

		matches = {}
		for mbi in memlist:
			buffer = create_string_buffer(mbi.RegionSize)
			address = c_long(mbi.BaseAddress)

			#mbi.AllocationProtect == PAGE_EXECUTE_READWRITE
			bytesRead = c_ulong(0)
			ReadProcessMemory(hProcess, address, buffer, mbi.RegionSize, bytesRead)
			with open(os.path.join(self.current_task_path, '%d_0x%x' % (self.pid, mbi.BaseAddress)), 'wb') as f:
				f.write(buffer.raw)
		return None

if __name__ == '__main__':
	if len(sys.argv) < 2:
		print ("Syntex : \n\t%s [pid]" % sys.argv[0])
		exit()

	dumper = MemDumper(int(sys.argv[1]))
	dumper.dump()
