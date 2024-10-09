from dot_mngr import os

import dot_mngr as dm

class PackageChroot(object):
	def chroot(self, dest: str = None):
		self.real_root = os.open("/", os.O_RDONLY)

		if dest is None:
			dest = dm.ROOT_PATH

		os.chroot(dest)
		os.chdir(".")
		self.chrooted = dest

	def unchroot(self):
		os.fchdir(self.real_root)
		os.chroot(".")
		os.close(self.real_root)
		if self.oldpwd:
			os.chdir(self.oldpwd)
		else:
			os.chdir(".")
		self.chrooted = None

	def chrooted_get_path(self, path = None, chroot = None):
		if chroot is None:
			chroot = self.chrooted
		if chroot and not path is None:
			if path.startswith(chroot):
				return path.removeprefix(chroot)
		return path
