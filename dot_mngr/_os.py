from dot_mngr import os
from dot_mngr import shutil

import dot_mngr as dm

class Os():
	@staticmethod
	def mkdir(path: str, clean: bool = False):
		if os.path.exists(path):
			if clean or not os.path.isdir(path):
				Os.rmdir(path)
			else:
				return
		os.makedirs(path)

	@staticmethod
	def take(path: str, clean: bool = False):
		Os.mkdir(path, clean)
		os.chdir(path)

	@staticmethod
	def rmdir(path: str):
		return shutil.rmtree(path)

	@staticmethod
	def get_path_is_bad_directory(root):
		splitted = root.removeprefix(os.sep).split(os.sep)
		match splitted[0]:
			case "proc":
				return True
			case "dev":
				return True
			case "sys":
				return True
		return False

	@staticmethod
	def	find(self, target, path = None):
		if path is None:
			path = dm.PREFIX

		for root, dirs, files in os.walk(path, followlinks=False):
			if Os.get_path_is_bad_directory(root.removeprefix(dm.PREFIX)):
				break
			for file in files:
				if file == target:
					return os.path.join(path, file)
			for directory in dirs:
				tmp = Os.get_path(target, os.path.join(path, directory))
				if tmp is not None:
					return tmp
		return None

	@staticmethod
	def	shrink_path(path: str):
		if path.startswith(CWD):
			return path.replace(CWD, ".")
		if path.startswith(HOME):
			return path.replace(HOME, "~")
		return path