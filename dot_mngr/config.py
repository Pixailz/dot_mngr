import os
import sys

from dot_mngr import PACKAGES, DIR_REPO, DIR_CACHE
from dot_mngr import p
from dot_mngr.package import Package

from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import wait

class Config():
	def __init__(self, ):
		self.create_dir()
		self.get_packages()

	def create_dir(self):
		if not os.path.exists(DIR_REPO):
			os.mkdir(DIR_REPO)
		if not os.path.exists(DIR_CACHE):
			os.mkdir(DIR_CACHE)

	def get_packages(self):
		self.packages = dict()
		for package in PACKAGES:
			self.packages[package] = Package(package)

	def info_package(self):
		Package.hdr_info()
		for package in self.packages.values():
			package.info()

	def update_repo(self, ):
		p.info("Updating packages")
		Package.hdr_info()

		# self.update_repo_normal()
		self.update_repo_threaded()

	def update_repo_threaded(self):
		pool = ThreadPoolExecutor()
		p.info(f"Pool worker: {pool._max_workers}")
		for package in self.packages.values():
			pool.submit(package.update)

		pool.shutdown(wait=True, cancel_futures=False)

	def update_repo_normal(self):
		for package in self.packages.values():
			package.update()

config = Config()
