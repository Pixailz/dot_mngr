from dot_mngr import os
from dot_mngr import sys
from dot_mngr import shutil

import dot_mngr as dm

from dot_mngr import p, Os, Json
from dot_mngr import scrap
from dot_mngr import url_handler

class PackageUpdate(object):
	def update(self):
		if not self.reference:
			self.new_link, self.new_version = scrap.latest_link(self)
			self.save_update()
		self.info()

	def save_update(self):
		if self.new_link == None:
			self.repo_status = 0
			return
		elif self.new_link != self.link:
			self.repo_status = 1
		else:
			self.repo_status = 2

		self.link = self.new_link
		self.version = self.new_version if self.new_version else self.version
		self.file_name = f"{self.name}-{self.version}{self.suffix}"
		self.file_path = os.path.join(dm.DIR_CACHE, self.file_name)
		Json.dump({
			"value": self.value,
			"type": self.type,
			"prefix": self.prefix,
			"suffix": self.suffix,
			"link": self.link,
			"version": self.version,
			"patchs": self.patchs,
			"files": self.files,
			"dependencies": self.dependencies
		}, self.f_meta)


	def get_file(self, chroot = None):
		if chroot is None:
			chroot = self.chrooted
		if not os.path.exists(self.chrooted_get_path(self.file_path, chroot)):
			if not url_handler.download_package(self):
				return False
			else:
				return True
		p.success(f"{self.file_name} already exists")
		return True

	def chrooted_get_path(self, path = None, chroot = None):
		if chroot is None:
			chroot = self.chrooted
		if chroot and not path is None:
			if path.startswith(chroot):
				return path.removeprefix(chroot)
		return path

	def take_build(self):
		path = os.path.join(self.archive_folder, "build")
		if not self.chrooted is None:
			path = path.replace(self.chrooted, "")
		Os.take(path)

	def chroot(self, dest: str = None):
		if dest is None:
			if dm.ROOT_PATH == "":
				return
			dest = dm.ROOT_PATH

		self.real_root = os.open("/", os.O_RDONLY)

		os.chroot(dest)
		os.chdir(".")
		self.chrooted = dest

	def unchroot(self):
		if getattr(self, "real_root", None) is None:
			return

		os.fchdir(self.real_root)
		os.chroot(".")
		os.close(self.real_root)
		if self.oldpwd:
			os.chdir(self.oldpwd)
		else:
			os.chdir(".")
		self.chrooted = None

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
		systemd_units.prepare_tarball(chroot = self.chrooted)
		Os.take(self.chrooted_get_path(systemd_units.archive_folder, self.chrooted))
		self.cmd_run(f"make install-{unit_name}")