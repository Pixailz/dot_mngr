from dot_mngr import *

class Config():
	def __init__(self, ):
		self.create_dir()
		self.get_packages()
		self.load_meta()

	def create_dir(self):
		if not os.path.exists(DIR_REPO):
			os.mkdir(DIR_REPO)
		if not os.path.exists(DIR_CACHE):
			os.mkdir(DIR_CACHE)
		if not os.path.exists(DIR_LOG):
			os.mkdir(DIR_LOG)

	def get_packages(self):
		self.packages = dict()
		for package in PACKAGES:
			self.packages[package] = Package(package)

	def load_meta(self):
		meta = None
		if os.path.exists(os.path.join(DIR_REPO, FILE_META)):
			with open(os.path.join(DIR_REPO, FILE_META), "r") as f:
				try:
					meta = json.load(f)
				except json.JSONDecodeError:
					p.fail("Failed to load repo meta.json")

		self.last_checked = None
		if meta:
			self.last_checked = meta.get("last_checked")

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
