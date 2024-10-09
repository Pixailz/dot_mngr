from dot_mngr import os
from dot_mngr import sys

from dot_mngr import url_handler
from dot_mngr import p, a

import dot_mngr as dm

class PackagePatch(object):
	def patch_get_path(self, name, chroot = None):
		if chroot is None:
			chroot = self.chrooted
		path = self.chrooted_get_path(self.archive_folder, chroot)
		return os.path.join(path, f"{name}.patch")

	def download_patch(self, name, path = None):
		url = self.patchs[name]
		if path is None:
			path = self.patch_get_path(name)
		if os.path.exists(path):
			return
		if dm.DRY_RUN:
			p.dr(f"Patch: Downloading {a.RED}{url}{a.RST} into {a.GRE}{path}{a.RST}")
		else:
			if not url_handler.download_file(url, path):
				sys.exit(1)

	def apply_patch(self, name, opt):
		# TODO:
		# 	- Check if patch is already downloaded
		path = self.patch_get_path(name)
		self.download_patch(name, path)
		self.cmd_run(f"patch {opt} -i {path}")
