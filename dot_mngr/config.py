from dot_mngr import *


class Config():
	def __init__(self, ):
		self.create_dir()
		self.load_meta()

	def create_dir(self):
		mkdir(DIR_REPO)
		mkdir(DIR_CACHE)
		mkdir(DIR_LOG, True)

	def load_meta(self):
		meta = json_load(os.path.join(DIR_REPO, FILE_META))

		if not meta:
			meta = dict()
		self.last_checked = meta.get("last_checked")
		self.list_packages = meta.get("packages")

	def load_packages(self):
		self.packages = dict()
		for package in PACKAGES:
			self.packages[package] = Package(package)

	def print_last_checked(self):
		msg = "Last checked: "
		if self.last_checked:
			msg += datetime.datetime.fromtimestamp(self.last_checked) \
				.strftime(" %d/%m/%Y %H:%M:%S")
		else:
			msg += "Never"
		p.info(msg + "\n")

	def info_package(self):
		self.print_last_checked()
		Package.hdr_info()
		for package in self.packages.values():
			package.info()

	def update_repo(self, ):
		p.info("Updating packages")
		Package.hdr_info()

		# self.update_repo_normal()
		self.update_repo_threaded()

		self.last_checked = datetime.datetime.now().timestamp()
		with open(os.path.join(DIR_REPO, FILE_META), "w") as f:
			json.dump({
				"last_checked": self.last_checked,
				"packages": self.list_packages
			}, f, indent=4)

	def update_repo_threaded(self):
		pool = ThreadPoolExecutor()
		p.info(f"Pool worker: {pool._max_workers}")
		for package in self.packages.values():
			pool.submit(package.update)

		pool.shutdown(wait=True, cancel_futures=False)

	def update_repo_normal(self):
		for package in self.packages.values():
			package.update()

conf = Config()
