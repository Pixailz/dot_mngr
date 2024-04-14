from dot_mngr import *

def a_method(func):
	def wrapper(self):
		if not self.prepared:
			self.prepare()
		func(self)
	return wrapper

class DefaultCommand():
	def __init__(self, package):
		self.package = package
		self.prepared = False

	def suite(self):
		self.configure()
		self.compile()
		if DO_CHECK:
			self.check()
		self.install()

	def prepare(self):
		from dot_mngr import conf
		if not os.path.exists(self.package.file_path):
			self.package.get_file()
		if tar.is_tarfile(self.package.file_path):
			self.prepare_tarball()
		self.conf = conf
		self.prepared = True

	def prepare_tarball(self):
		ftar = tar.open(self.package.file_path, "r")
		ftar_names = ftar.getnames()
		if len(ftar_names) > 0:
			self.package.tar_folder = os.path.join(DIR_CACHE, ftar_names[0])
			if os.path.exists(self.package.tar_folder):
				shutil.rmtree(self.package.tar_folder)
				p.warn("Removing old tar folder")
		ftar.extractall(DIR_CACHE)

	@a_method
	def configure(self):
		pass

	@a_method
	def compile(self):
		pass

	@a_method
	def check(self):
		pass

	@a_method
	def install(self):
		pass
