from dot_mngr import os
from dot_mngr import copy
from dot_mngr import shutil
from dot_mngr import subprocess

import dot_mngr as	 dm
from dot_mngr import p
from dot_mngr import Json, Os, Package, Parsing, Repository
from dot_mngr import RepoError

from dot_mngr import DIR_CONFIG, DIR_RSC, DIR_REPO, DIR_CACHE, DIR_LOG
from dot_mngr import FILE_META, PREFIX, NB_PROC, REPO_SEP

from dot_mngr import sys

from dot_mngr import pprint
from dot_mngr import get_real_name

def	uniq_list_deps(lst):
	new_list = list()
	item_dic = dict()
	for i in lst:
		if i not in item_dic:
			item_dic[i] = 1
		else:
			item_dic[i] += 1

	for i in lst:
		if item_dic[i] == 1:
			new_list.append(i)
		else:
			item_dic[i] -= 1

	return new_list

def	uniq_list(lst):
	new_list = list()
	for item in lst:
		if item not in new_list:
			new_list.append(item)
	return new_list

class Config():
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

	def	__get_package(self, pack_name):
		splitted = pack_name.split(REPO_SEP)
		repos = None

		if len(splitted) == 2:
			if splitted[0] not in self.repository:
				p.fail(f"Repository {splitted[0]} not found")
			repos = self.repository[splitted[0]]
			splitted[0] = splitted[1]
		else:
			repos = self.repository
		return splitted[0], repos

	def	get_package(self, pack_name):
		pack_name, repos = self.__get_package(pack_name)

		for k, v in repos.items():
			pack = v.packages.get(pack_name, None)
			if pack is not None:
				return pack
		return None

	def	is_in_packages(self, pack_name):
		pack = self.__get_package(pack_name)
		return pack is not None

	def	is_installed(self, p, force: bool = None):
		if force is None:
			force = dm.FORCE_INSTALL
		if force:
			return False
		pack = self.get_package(p)
		if pack is None:
			return False
		return pack.is_installed()

	# UPDATE
	def	update_repo(self):
		to_update = copy.deepcopy(getattr(self.parsing.args, "update_package", None))
		for repo in self.repository.values():
			repo.update(self.parsing.args.glob_no_thread, to_update)

	# INSTALL

	## DEPENDENCIES
	def	dependencies_get(self, pack):
		to_install = list()
		if not getattr(pack, "dependencies", None) is None:
			if pack.dependencies.get("required"):
				for pak in pack.dependencies["required"]:
					if not self.is_in_packages(pak):
						p.fail(f"Package {pak} not found")
					if not self.is_installed(pak):
						to_install.append(pak)
		return to_install

	def	dependencies_get_all(self, pack):
		i = 1
		to_install = [pack]
		prev_len = len(to_install)
		while i:
			tmp_to_install = list()
			for p in to_install:
				tmp_to_install += self.dependencies_get(self.get_package(p))
				print(p)
			if i == 1 and self.is_installed(pack):
				to_install = uniq_list_deps(tmp_to_install)
			else:
				to_install = uniq_list_deps(to_install + tmp_to_install)

			new_len = len(to_install)
			if prev_len == new_len:
				break
			prev_len = new_len
			i += 1
		print("Dependencies to install:")
		pprint(to_install)
		return to_install

	def	install_package(self):
		to_install = copy.deepcopy(getattr(self.parsing.args, "inst_package", None))

		if not to_install:
			p.fail("No package to install")

		for pack in self.parsing.args.inst_package:
			if	not self.is_in_packages(pack) and \
				not self.is_in_packages(get_real_name(pack)):
				p.fail(f"Package {pack} not found")

		tmp_to_install = list()
		for pack in to_install:
			tmp_to_install += self.dependencies_get_all(get_real_name(pack))

		to_install = tmp_to_install
		to_install.reverse()

		for pack in to_install:
			self.get_package(pack).cmd["suite"]()

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

def	get_package_from_name(package_name: str):
	package = conf.get_package(package_name)
	if package is None:
		p.fail(f"Package {package_name} not found")
	return package

def	download_package(self, package_name: str):
	package = get_package_from_name(package_name)
	if package is None:
		return
	package.get_file(self.chrooted)

def	extract_file_from_package(
		package_name: str,
		dest: str = None,
		chroot = None,
	):
	package = get_package_from_name(package_name)
	if package is None:
		return

	package.get_file(chroot)
	package.prepare_tarball(dest, chroot)

def	get_version_from_package(
		package_name: str
	):
	package = get_package_from_name(package_name)
	if package is None:
		return
	return package.version
