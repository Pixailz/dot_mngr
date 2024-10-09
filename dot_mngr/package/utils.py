from dot_mngr import os

import dot_mngr as dm

from dot_mngr import p
from dot_mngr import REPO_SEP

from dot_mngr import pprint

def get_real_name(pack_name: str):
	splitted = pack_name.split(dm.REPO_SEP)
	return splitted[1] if len(splitted) == 2 else splitted[0]

class PackageUtils(object):
	def is_good_link(self, link_path):
		ptr_path = os.readlink(link_path)
		root_path = dm.ROOT_PATH
		if root_path == "":
			root_path = "/"
		joined_path = os.path.join(root_path, ptr_path.removeprefix("/"))
		if os.path.exists(joined_path):
			return True
		if os.path.islink(joined_path):
			return self.is_good_link(joined_path)
		return False

	def	is_good_cmd(self, cmd):
		for path in dm.PATH:
			root_path = os.path.join(os.path.join(dm.ROOT_PATH, path.removeprefix("/")), cmd)
			if os.path.islink(root_path):
				# return self.is_good_link(root_path)
				return True
			if os.path.exists(root_path):
				return True
		return False

	def is_installed(self):
		# print(self.name)
		# pprint(self.files)
		if self.files == None:
			return False
		for file in self.files:
			if file.startswith("/"):
				tmp_path = os.path.join(dm.ROOT_PATH, dm.PREFIX.removeprefix("/"))
				tmp_path = os.path.join(tmp_path, file.removeprefix("/"))
				if not os.path.islink(tmp_path) and not os.path.exists(tmp_path):
					p.warn(file)
					return False
			else:
				if not self.is_good_cmd(file):
					p.warn(file)
					return False
		return True

	def int2ver(self):
		try:
			major = self.version[0]
			minor = self.version[1:3].rstrip("0")
			patch = self.version[4:6].rstrip("0")
			version = f"{major}.{minor}.{patch}"
		except IndexError:
			# int(self)
			p.warn(f"int2ver: {self.version} cannot be converted to version notation")
			return None
		print(version)
		return version