from dot_mngr import os
from dot_mngr import shutil

from dot_mngr import NB_PROC, PREFIX

class Os():
	path = "/usr/bin:/usr/sbin"
	if os.path.exists("/bin") and not os.path.islink("/bin"):
		path = f"/bin:{path}"
	path = f"{PREFIX}/tools/bin:{path}"
	env = {
		"LC_ALL": "POSIX",
		"PATH": path,
	}
	make_flags = f"-I{PREFIX}/include -l{PREFIX}/lib"

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
	def get_env(nb_proc):
		Os.env["MAKEFLAGS"] = f"-j{nb_proc} {Os.make_flags}"
		return Os.env
