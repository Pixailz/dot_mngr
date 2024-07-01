from dot_mngr import subprocess

class Git():
	@staticmethod
	def clone(link, branch=None, dest=None):
		cmd = f"git clone {link}"

		if dest is not None:
			cmd += f" {dest}"
		if branch is not None:
			cmd += f" --branch {branch}"

		return subprocess.Popen(cmd,
			shell=True,
			close_fds=True,
		).wait()

	@staticmethod
	def update(dest):
		cmd = f"git -C {dest} pull"

		return subprocess.Popen(cmd,
			shell=True,
			close_fds=True,
		).wait()
