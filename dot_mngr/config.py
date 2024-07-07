from dot_mngr import os
from dot_mngr import copy
from dot_mngr import shutil

from dot_mngr import p
from dot_mngr import Json, Os, Package, Parsing, Repository
from dot_mngr import RepoError

from dot_mngr import DIR_CONFIG, DIR_RSC, DIR_REPO, DIR_CACHE, DIR_LOG
from dot_mngr import FILE_META, PREFIX, NB_PROC

from dot_mngr import sys
from dot_mngr import pprint

def uniq_list(lst):
	new_list = list()
	for item in lst:
		if item not in new_list:
			new_list.append(item)
	return new_list

def dependencies_get(pack):
	to_install = list()
	package = conf.packages[pack]

	if not getattr(package, "dependencies", None) is None:
		if package.dependencies.get("required"):
			for pak in package.dependencies["required"]:
				if pak in conf.packages:
					to_install.append(pak)
		# if package.dependencies.get("optional"):
		#	to_install += pass
	return to_install

def is_installed(pack):
	if pack.files == None:
		return False
	for file in pack.files:
		if file[0] == "/":
			file = file[1:]
		# print(os.path.join(PREFIX, file))

		if not os.path.exists(os.path.join(PREFIX, file)):
			return False
	return True

def dependencies_get_all(target):
	to_install = dependencies_get(target.name)
	prev_len = len(to_install)

	while True:
		tmp_to_install = list()
		for pack in to_install:
			tmp_to_install += dependencies_get(pack)
		to_install = uniq_list(to_install + tmp_to_install)
		cur_len = len(to_install)
		if prev_len == cur_len:
			break
		else:
			prev_len = cur_len
	return to_install

def dependencies_get_not_installed(to_install):
	new_to_install = list()
	for pack in to_install:
		if not is_installed(conf.packages[pack]):
			new_to_install.append(pack)

	return to_install

	# sys.exit(130)
	# for i in to_install:
	# 	if not self.conf.packages.get(i):
	# 		p.warn(f"Dependency {i} not found")
	# 		continue

	# 	self.conf.packages[i].cmd["suite"]()

class Config():
	# INIT
	def __init__(self):
		self.parsing = Parsing()
		self.create_dir()
		self.copy_default_file()
		self.load_meta()

	def create_dir(self):
		Os.mkdir(DIR_CONFIG)
		Os.mkdir(DIR_REPO)
		Os.mkdir(DIR_CACHE)
		Os.mkdir(DIR_LOG)

		# for dir in ["bin", "etc", "lib", "lib64", "share", "var"]:
		# 	Os.mkdir(os.path.join(PREFIX, dir))

	def copy_default_file(self):
		env_file_path = os.path.join(DIR_CONFIG, ".env")
		if not os.path.isfile(env_file_path):
			shutil.copy2(os.path.join(DIR_RSC, ".env.template"), env_file_path)
		source_list_path = os.path.join(DIR_CONFIG, "sources.list")
		if not os.path.isfile(source_list_path):
			shutil.copy2(os.path.join(DIR_RSC, "sources.list"), source_list_path)

	def load_meta(self):
		meta = Json.load(os.path.join(DIR_REPO, FILE_META))

		if not meta:
			meta = dict()
		self.last_checked = meta.get("last_checked")
		self.list_packages = meta.get("packages")

	def load_repository(self):
		with open(os.path.join(DIR_CONFIG, "sources.list")) as f:
			sources = f.read().splitlines()

		self.repository = dict()

		for source in sources:
			self.repository[source[0]] = Repository(source)

		self.packages = dict()

		for repo in self.repository.values():
			for k, v in repo.packages.items():
				self.packages[k] = v

	# UPDATE
	def update_repo(self):
		for repo in self.repository.values():
			repo.update(self.parsing.args.glob_no_thread)

	# INSTALL
	def install_package(self):
		to_install = copy.deepcopy(getattr(self.parsing.args, "inst_package", None))

		if not to_install:
			p.fail("No package to install")

		for pack in self.parsing.args.inst_package:
			if pack not in self.packages:
				p.fail(f"Package {pack} not found")
			to_install.append(pack)

		tmp_to_install = list()
		for pack in to_install:
			tmp_to_install += dependencies_get_all(self.packages[pack])

		to_install = uniq_list(
			dependencies_get_not_installed(to_install + tmp_to_install)
		)

		# Now that we have the list of packages and dependencies, in this order
		# we can install them, in reverse so dependencies are installed first
		for pack in sorted(to_install, reverse=True):
			self.packages[pack].cmd["suite"]()

	# INFO
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
		for repo in self.repository.values():
			p.set_lvl(0)
			p.title(repo.name)
			p.set_lvl(1)
			for package in repo.packages.values():
				package.info()
			print()

conf = Config()

def get_package_from_name(package_name: str):
	package = conf.packages.get(package_name, None)
	if package is None:
		p.fail(f"Package {package_name} not found")
		return
	return package

def download_package(self, package_name: str):
	package = get_package_from_name(package_name)
	if package is None:
		return
	package.get_file(self.chrooted)

def extract_file_from_package(
		package_name: str,
		dest: str = None,
		chroot = None,
	):
	package = get_package_from_name(package_name)
	if package is None:
		return

	package.get_file(chroot)
	package.prepare_tarball(dest, chroot)

def get_version_from_package(
		package_name: str
	):
	package = get_package_from_name(package_name)
	if package is None:
		return
	return package.version
