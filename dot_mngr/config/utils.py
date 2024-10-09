import dot_mngr as dm

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

def	download_package(self, package_name: str):
	package = dm.conf.get_package(package_name)
	if package is None:
		return
	package.get_file(self.chrooted)

def	extract_file_from_package(
		package_name: str,
		dest: str = None,
		chroot = None,
	):
	package = dm.conf.get_package(package_name)
	if package is None:
		return

	package.get_file(chroot)
	package.prepare_tarball(dest, chroot)

def	get_version_from_package(
		package_name: str
	):
	package = dm.conf.get_package(package_name)
	if package is None:
		return
	return package.version

class ConfigUtils(object):
	def	__get_package(self, pack_name):
		splitted = pack_name.split(dm.REPO_SEP)
		repos = None

		if len(splitted) == 2:
			if splitted[0] not in self.repository:
				p.fail(f"Repository {splitted[0]} not found")
			repos = {
				splitted[0]: self.repository[splitted[0]]
			}
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
		pack = self.get_package(pack_name)
		return pack is not None

	def	is_installed(self, p, force: bool = None):
		if force is None:
			force = dm.FORCE_INSTALL
		if force:
			return False
		pack = self.get_package(p)
		if pack is None:
			return False
		print(pack.name)
		return pack.is_installed()
