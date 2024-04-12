import os
import json

from dot_mngr import DIR_REPO, DIR_CACHE
from dot_mngr import p, r, scrap, url_handler

class Package():
	def __init__(self, name):

		self.name = name
		self.meta = os.path.join(DIR_REPO, self.name)

		if os.path.exists(self.meta):
			with open(self.meta, "r") as f:
				self.load_meta_in(f)
		else:
			self.meta = None

	def load_meta_in(self, f):
		try:
			meta = json.load(f)
		except json.JSONDecodeError:
			p.fail(f"Failed to load {self.meta}")

		self.value = meta.get("value")
		self.type = meta.get("type")
		self.prefix = meta.get("prefix")
		self.suffix = meta.get("suffix")
		self.link = meta.get("link")
		self.version = meta.get("version")
		self.repo_status = None

	@staticmethod
	def hdr_info():
		print("\nID\x1b[20GVersion\x1b[40GStatus\x1b[60GLink\n")

	def info(self):
		status = "Not checked"
		if self.repo_status == 0:
			status = "Failed to scrap"
		elif self.repo_status == 1:
			status = "Updated"
		elif self.repo_status == 2:
			status = "Up to date"
		print(f"{self.name}\x1b[20G{self.version}\x1b[40G{status}\x1b[60G{self.link}")

	def save_update(self):
		if self.new_link == None:
			self.repo_status = 0
			return
		elif self.new_link != self.link:
			self.repo_status = 1
		else:
			self.repo_status = 2

		self.link = self.new_link
		self.version = self.new_version if self.new_version else self.version
		with open(self.meta, "w") as f:
			json.dump({
				"value": self.value,
				"type": self.type,
				"prefix": self.prefix,
				"suffix": self.suffix,
				"link": self.link,
				"version": self.version
			}, f, indent=4)

	def update(self):
		self.new_link, self.new_version = scrap.latest_link(self)
		self.save_update()
		self.info()

	def get_file(self):
		self.tar_name = f"{self.name}-{self.version}.tar.gz"
		self.tar_path = os.path.join(DIR_CACHE, self.tar_name)
		if not os.path.exists(self.tar_path):
			if not url_handler.download_package(self):
				return False
			else:
				return True
		p.success(f"{self.tar_name} already exists")
		return True

	def install(self):
		if not self.get_file():
			return False
		p.info(f"installing {self.name}")
