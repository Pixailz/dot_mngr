from dot_mngr import os
from dot_mngr import tar
from dot_mngr import shutil

import zipfile

import dot_mngr as dm

from dot_mngr import p, r, Os

PROFILE = {
	"tarball": {
		"check": tar.is_tarfile,
		"open": tar.open,
		"getnames": "getnames",
		"extractall": "extractall",
	},
	"zipfile":  {
		"check": zipfile.is_zipfile,
		"open": zipfile.ZipFile,
		"getnames": "namelist",
		"extractall": "extractall",
	}
}

class PackagePrepareArchive(object):
	def take_archive_folder(self):
		cwd = os.getcwd()
		if cwd != self.archive_folder:
			self.oldpwd = cwd
		os.chdir(self.archive_folder)

	def prepare_archive_real(self, src: str, dest: str, profile_key: str):
		profile = PROFILE[profile_key]
		file = profile["open"](src, "r")
		file_names = getattr(file, profile["getnames"])()
		have_dir = True
		if len(file_names) > 0:
			for i in range(0, 2):
				match = r.archive_dir.match(file_names[i])
				if match:
					break

			if match:
				self.archive_folder = os.path.join(dm.DIR_CACHE, match.group(1))
			else:
				self.archive_folder = os.path.join(dm.DIR_CACHE, self.name)
				have_dir = False
		extract_func = getattr(file, profile["extractall"])
		if os.path.exists(self.archive_folder):
			shutil.rmtree(self.archive_folder)
			p.warn("Removing old archive folder")

		if dest is None:
			p.info(f"Extracting {self.name}")
			if have_dir:
				extract_func(dm.DIR_CACHE)
			else:
				extract_func(self.archive_folder)
			p.success(f"Extracted {self.name}")
		else:
			if not os.path.exists(dest):
				Os.mkdir(dest)
			p.info(f"Extracting {self.name} into {dest}")
			extract_func(dest)
			p.success(f"Extracted {self.name} into {dest}")

	def prepare_archive(self, dest: str = None, chroot: str = None):
		if chroot is None:
			chroot = self.chrooted
		if self.file_path is None:
			self.archive_folder = os.path.join(dm.DIR_CACHE, self.name)
			print(self.archive_folder)
			Os.mkdir(self.archive_folder)
			return
		src = self.chrooted_get_path(self.file_path, chroot)
		if dm.DRY_RUN:
			if dest is None:
				self.archive_folder = os.path.join(dm.DIR_CACHE, self.name)
				dest = self.archive_folder

			dest = self.chrooted_get_path(dest, chroot)
			Os.mkdir(dest)
			p.dr(f"Creating {dest}")
		else:
			chrooted_path = self.chrooted_get_path(dest, chroot)
			print(f"{chrooted_path = }")
			print(f"{src           = }")
			for key in PROFILE:
				if PROFILE[key]["check"](src):
					self.prepare_archive_real(src, chrooted_path, key)
					return
			_, ext = os.splitext(src)
			p.warn(f"Archive format {ext}")