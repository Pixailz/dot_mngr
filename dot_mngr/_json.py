from dot_mngr import os
from dot_mngr import json

class Json():
	@staticmethod
	def load(file):
		if os.path.exists(file):
			with open(file, "r") as f:
				return json.load(f)
		else:
			return None

	@staticmethod
	def dump(obj, file_path):
		with open(file_path, "w") as f:
			json.dump(obj, f, indent='\t')
