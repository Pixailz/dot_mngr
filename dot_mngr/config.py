import os

from dot_mngr import PACKAGES, DIR_REPO, DIR_CACHE
from dot_mngr.package import Package

class Config():
	def __init__(self, ):
		self.create_dir()
		self.get_packages()

	def create_dir(self):
		if not os.path.exists(DIR_REPO):
			os.mkdir(DIR_REPO)
		if not os.path.exists(DIR_CACHE):
			os.mkdir(DIR_CACHE)

	def info_package(self):
		Package.hdr_info()
		for package in self.packages.values():
			package.info()

	def get_packages(self):
		self.packages = dict()
		for package in PACKAGES:
			self.packages[package] = Package(package)

	def update_repo(self, ):
		print("Updating packages")
		Package.hdr_info()
		for package in self.packages.values():
			package.update()

config = Config()
