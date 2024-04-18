from dot_mngr import *

def mkdir(path, clean = False):
	if os.path.exists(path):
		if clean or not os.path.isdir(path):
			shutil.rmtree(path)
		else:
			return
	os.mkdir(path)

def take(path, clean = False):
	mkdir(path, clean)
	os.chdir(path)
