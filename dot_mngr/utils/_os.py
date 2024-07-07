from dot_mngr import os
from dot_mngr import shutil

from dot_mngr import NB_PROC, PREFIX

from pprint import pprint

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
