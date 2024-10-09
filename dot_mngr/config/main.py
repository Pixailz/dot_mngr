from dot_mngr import os
from dot_mngr import copy
from dot_mngr import shutil
from dot_mngr import subprocess

import dot_mngr as	 dm
from dot_mngr import p
from dot_mngr import Json, Os, Package, Parsing, Repository

from dot_mngr import DIR_CONFIG, DIR_RSC, DIR_REPO, DIR_CACHE, DIR_LOG
from dot_mngr import FILE_META, PREFIX

from .utils			import ConfigUtils
from .install		import ConfigInstall
from .dependency	import ConfigDependency

from dot_mngr	import pprint

class Config(
		ConfigUtils,
		ConfigInstall,
		ConfigDependency,
	):
	# INIT
	def	__init__(self):
		self.parsing = Parsing()
		self.create_dir()
		self.copy_default_file()
		self.load_meta()

	def	create_dir(self):
		Os.mkdir(DIR_CONFIG)
		Os.mkdir(DIR_REPO)
		Os.mkdir(DIR_CACHE)
		Os.mkdir(DIR_LOG)

		# for dir in ["bin", "etc", "lib", "lib64", "share", "var"]:
		# 	Os.mkdir(os.path.join(PREFIX, dir))

	def	copy_default_file(self):
		env_file_path = os.path.join(DIR_CONFIG, ".env")
		if not os.path.isfile(env_file_path):
			shutil.copy2(os.path.join(DIR_RSC, ".env.template"), env_file_path)

		source_list_path = os.path.join(DIR_CONFIG, "sources.list")
		if not os.path.isfile(source_list_path):
			shutil.copy2(os.path.join(DIR_RSC, "sources.list"), source_list_path)

	def	load_meta(self):
		meta = Json.load(os.path.join(DIR_REPO, FILE_META))
		if not meta:
			meta = dict()
		self.last_checked = meta.get("last_checked")
		self.list_packages = meta.get("packages")

	def	load_repository(self):
		with open(os.path.join(DIR_CONFIG, "sources.list")) as f:
			sources = [ i.split(" ") for i in f.read().splitlines() ]

		self.repository = dict()

		for source in sources:
			self.repository[source[0]] = Repository(source)

		for repo in self.repository.values():
			for k, v in repo.packages.items():
				if getattr(v, "reference", None) is not None:
					v.load_metas_ref()

	# UPDATE
	def	update_repo(self):
		to_update = copy.deepcopy(getattr(self.parsing.args, "update_package", None))
		for repo in self.repository.values():
			repo.update(self.parsing.args.glob_no_thread, to_update)

	# INFO
	def	print_last_checked(self):
		msg = "Last checked: "
		if self.last_checked:
			msg += datetime.datetime.fromtimestamp(self.last_checked) \
				.strftime(" %d/%m/%Y %H:%M:%S")
		else:
			msg += "Never"
		p.info(msg + "\n")

	def	info_package(self):
		self.print_last_checked()
		to_get_info = copy.deepcopy(getattr(self.parsing.args, "info_package", None))
		Package.hdr_info()
		for repo in self.repository.values():
			p.set_lvl(0)
			p.title(repo.name)
			p.set_lvl(1)
			for package in repo.packages.values():
				if not to_get_info or (
					package.name in to_get_info or package.real_name in to_get_info
				):
					package.info()
			print()

conf = Config()
