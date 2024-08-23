from dot_mngr import os
from dot_mngr import sys
from dot_mngr import datetime
from dot_mngr import ThreadPoolExecutor

from dot_mngr import Package
from dot_mngr import Json
from dot_mngr import Git
from dot_mngr import RepoError
from dot_mngr import p
from dot_mngr import DIR_REPO, FILE_META, NB_PROC

from dot_mngr import p_elapsed
from dot_mngr import pprint
from dot_mngr import REPO_SEP

class Repository():
	def __init__(self, line: str):
		tmp = line
		tmp_len = len(tmp)

		if tmp_len <= 1 or tmp_len > 3:
			raise RepoError(f"Wrong line in sources.list\n{line}")

		self.name = tmp[0]
		self.base_dir = os.path.join(DIR_REPO, self.name)
		self.f_meta = os.path.join(self.base_dir, FILE_META)
		self.link = tmp[1]
		self.branch = None
		if len(tmp) == 3:
			self.branch = tmp[2]
		self.init_repo()

	def init_repo(self):
		if os.path.isdir(self.base_dir):
			print("Repo already here")
			# Git.update(self.base_dir)
		else:
			print("Repo not here")
			Git.clone(self.link, self.branch, self.base_dir)
		self.load_packages()

	def get_packages(self):
		readed = Json.load(self.f_meta)
		self.list_packages = readed["packages"]

	def load_packages(self):
		self.get_packages()
		nb_packages = len(self.list_packages)
		p.info(f"Loading {nb_packages} packages")
		self.packages = dict()
		for package in self.list_packages:
			pack_name = f"{self.name}{REPO_SEP}{package}"
			self.packages[package] = Package(pack_name, self.base_dir)
		p.success(f"Loaded {nb_packages} packages")

	def update(self, threaded, to_update):
		p.info("Updating packages")
		Package.hdr_info()
		if threaded:
			self.update_no_thread(to_update)
		else:
			self.update_thread(to_update)

		self.last_checked = datetime.datetime.now().timestamp()
		Json.dump({
			"last_checked": self.last_checked,
			"packages": self.list_packages
		}, self.f_meta)

	def update_thread(self, to_update):
		pool = ThreadPoolExecutor(NB_PROC)
		p.info(f"Pool worker: {pool._max_workers}")
		for package in self.packages.values():
			if to_update and package.name not in to_update:
				continue
			pool.submit(package.update)

		pool.shutdown(wait=True, cancel_futures=False)

	def update_no_thread(self, to_update):
		for package in self.packages.values():
			if to_update and package.name not in to_update:
				continue
			package.update()
