from dot_mngr import os
from dot_mngr import shutil

import dot_mngr as dm

from dot_mngr import p, Os

class PackageCmdUtils(object):
	def load_env(self):
		path = "/usr/bin:/usr/sbin"
		if os.path.exists("/bin") and not os.path.islink("/bin"):
			path = f"/bin:{path}"

		self.env = {
			"PATH": path,
		}

	def add_path(self, path):
		self.env["PATH"] = f"{path}:{self.env['PATH']}"

	def get_env(self, nb_proc = dm.NB_PROC):
		self.env["MAKEFLAGS"] = f"-j{nb_proc}"
		return self.env

	def add_env(self, env: dict):
		self.env.update(env)

	def take_build(self):
		path = os.path.join(self.archive_folder, "build")
		if not self.chrooted is None:
			path = path.replace(self.chrooted, "")
		Os.take(path)

	def copy(self, file_name: str, dest_path: str):
		file_path = os.path.join(self.archive_folder, file_name)
		copy_func = None
		if not os.path.exists(file_path):
			p.fail(f"File not found: {file_name}")
		elif os.path.isdir(file_path):
			copy_func = shutil.copytree
		else:
			copy_func = shutil.copy2

		copy_func(file_path, dest_path)

	def	install_blfs_systemd_units(self, unit_name: str):
		# if not dm.conf.is_installed("systemd"):
		# 	p.warn("Systemd is not installed")
		# 	return
		systemd_units = dm.conf.get_package("blfs-systemd-units")
		systemd_units.prepare_archive(chroot = self.chrooted)
		Os.take(self.chrooted_get_path(systemd_units.archive_folder, self.chrooted))
		self.cmd_run(f"make install-{unit_name}")

	def generate_configure(self):
		if not os.path.exists("configure") and os.path.exists("autogen.sh"):
			self.cmd_run("sh autogen.sh")