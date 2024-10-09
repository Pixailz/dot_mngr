from dot_mngr import os
from dot_mngr import importlib
from dot_mngr import subprocess

import dot_mngr as dm

from dot_mngr import p
from dot_mngr import a_cmd

# PROFILE
## DEFAULT
from dot_mngr import default_configure
from dot_mngr import default_compile
from dot_mngr import default_check
from dot_mngr import default_install
from dot_mngr import default_uninstall
from dot_mngr import default_suite

## KERNEL
from dot_mngr import default_kernel_configure
from dot_mngr import default_kernel_configure_kernel
from dot_mngr import default_kernel_compile
from dot_mngr import default_kernel_install


from dot_mngr import pprint

CMD_PROFILE = {
	"default": {
		"configure": default_configure,
		"compile": default_compile,
		"check": default_check,
		"install": default_install,
		"uninstall": default_uninstall,
		"suite": default_suite,
	},
	"kernel": {
		"configure": default_kernel_configure,
		"configure_kernel": default_kernel_configure_kernel,
		"compile": default_kernel_compile,
		"check": default_check,
		"install": default_kernel_install,
		"uninstall": default_uninstall,
		"suite": default_suite,
	}
}

class PackageCmd(object):

	def load_command(self, cmd_name: str, default_cmd: callable):
		cmd = getattr(self.tmp_cmd, cmd_name, None)

		if cmd is not None:
			self.cmd[cmd_name] = a_cmd(self, cmd, cmd_name)
		else:
			self.cmd[cmd_name] = a_cmd(self, default_cmd)

	def load_commands_profile(self, profile):
		cmd = CMD_PROFILE.get(profile, None)
		if cmd is None:
			p.fail(f"Profile {profile} not found")

		for k, v in cmd.items():
			self.load_command(k, v)

	def load_commands(self):
		self.cmd = dict()
		self.tmp_cmd = None

		if os.path.exists(self.f_command):
			# return
			spec = importlib.util.spec_from_file_location("command", self.f_command)
			# if self.debug == 1:
			self.tmp_cmd = importlib.util.module_from_spec(spec)
			spec.loader.exec_module(self.tmp_cmd)

		configure_kernel = getattr(self.tmp_cmd, "configure_kernel", None)
		if configure_kernel is not None:
			self.cmd["configure_kernel"] = configure_kernel
			self.load_commands_profile("kernel")
		else:
			self.load_commands_profile("default")
		from pprint import pprint


	def cmd_run_real(self, cmd: str, nb_proc: int):
		def p_out(line):
			self.f_log_out.write(line)
			p.cmdo(line.strip("\n"))

		def p_err(line):
			self.f_log_err.write(line)
			p.cmde(line.strip("\n"))

		proc = subprocess.Popen(cmd,
			stdout=subprocess.PIPE,
			stderr=subprocess.PIPE,
			env=self.get_env(nb_proc),
			universal_newlines=True,
			shell=True,
			close_fds=True,
		)

		os.set_blocking(proc.stdout.fileno(), False)
		os.set_blocking(proc.stderr.fileno(), False)

		while True:
			line_out = proc.stdout.readline()
			line_err = proc.stderr.readline()
			line_out_empty = line_out == ''
			line_err_empty = line_err == ''
			if line_out_empty and line_err_empty and proc.poll() is not None:
				break
			if not line_out_empty:
				p_out(line_out)
			if not line_err_empty:
				p_err(line_err)

		proc.wait()
		retv = proc.returncode

		if retv != 0:
			p.fail(f"Command failed:\n({retv})[{cmd}]")

		return retv

	def cmd_run(self, cmd: str, nb_proc: int = dm.NB_PROC):
		if dm.DRY_RUN:
			p.dr(cmd)
		else:
			return self.cmd_run_real(cmd, nb_proc)
