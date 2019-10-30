import subprocess

class VMControl(object):

	def __init__(self, config):
		self.config = config

	def send_file(self, src, dst):
		vmrun_command = [self.config.vmrun, '-gu', self.config.vm_user, '-gp', self.config.vm_password, 'copyFileFromHostToGuest', self.config.vmx, src, dst]
		result = self._vmrun_exec(vmrun_command)
		if result != 0:
			return False, result
		else:
			return True, None

	def retrieve_file(self, src, dst):
		vmrun_command = [self.config.vmrun, '-gu', self.config.vm_user, '-gp', self.config.vm_password, 'copyFileFromGuestToHost', self.config.vmx, src, dst]
		result = self._vmrun_exec(vmrun_command)
		if result != 0:
			return False, result
		else:
			return True, None

	def exec_cmd(self, cmd):
		vmrun_command = [self.config.vmrun, '-gu', self.config.vm_user, '-gp', self.config.vm_password, 'runScriptInGuest', self.config.vmx, '', cmd]
		result = self._vmrun_exec(vmrun_command)
		if result != 0:
			return False, result
		else:
			return True, None

	def _vmrun_exec(self, command):
		result, error = subprocess.Popen(command, stdout=subprocess.PIPE).communicate()
		result = result.decode('utf-8', errors='ignore')
		if 'exited with non-zero' in result:
			return result
		return 0


