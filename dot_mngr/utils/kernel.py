from dot_mngr import re

class Kernel():

	def __init__(self, conf_path):
		self.conf_path = conf_path

	def config(self, key, value, prefix="CONFIG_"):
		with open(self.conf_path, "r") as f:
			file_str = f.read()

		if prefix + key not in file_str:
			file_str += f"# {prefix}{key} is not set\n"

		pre_key = f"{prefix}{key}"
		file_str = re.sub(
			r".*" + re.escape(f"{pre_key}") + r"[ =].*",
			f"{pre_key}={value}",
			file_str
		)

		with open(self.conf_path, "w") as f:
			f.write(file_str)
