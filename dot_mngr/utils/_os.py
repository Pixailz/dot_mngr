from dot_mngr import os
from dot_mngr import shutil

from dot_mngr import NB_PROC, PREFIX

class Os():

	@staticmethod
	def mkdir(path: str, clean: bool = False):
		if os.path.exists(path):
			if clean or not os.path.isdir(path):
				shutil.rmtree(path)
			else:
				return
		os.makedirs(path)

	@staticmethod
	def take(path: str, clean: bool = False):
		mkdir(path, clean)
		os.chdir(path)

	@staticmethod
	def get_env():
		env = os.environ
		env["MAKEFLAGS"] = f"-j{NB_PROC} -I{PREFIX}/include -l{PREFIX}/lib"
		env["INCLUDE_PATH"] = f"{PREFIX}/include"
		env["LIBRARY_PATH"] = f"{PREFIX}/lib"
		return env
