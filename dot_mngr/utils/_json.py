from dot_mngr import *

def json_load(file):
	if os.path.exists(file):
		with open(file, "r") as f:
			return json.load(f)
	else:
		return None
