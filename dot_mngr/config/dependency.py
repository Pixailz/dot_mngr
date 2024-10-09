from dot_mngr import p

class ConfigDependency(object):
	def	dependencies_get(self, pack):
		to_install = list()
		if not getattr(pack, "dependencies", None) is None:
			if pack.dependencies.get("required"):
				for pak in pack.dependencies["required"]:
					if not self.is_in_packages(pak):
						p.fail(f"Package {pak} not found")
					to_install.append(pak)
		return to_install

	def depth_first_search_visit(self, node):
		if not self.is_in_packages(node):
			p.fail(f"Package {node} not found")
		if node in self.perm_mark:
			return
		if self.is_installed(node):
			if node not in self.perm_mark:
				self.perm_mark.append(node)
			return

		if node in self.temp_mark:
			print("Cyclic dependencies")
			if node in self.to_install:
				self.to_install.remove(node)
			self.to_install.append(node)
			return

		self.temp_mark.append(node)

		for pack in self.dependencies_get(self.get_package(node)):
			self.depth_first_search_visit(pack)

		self.perm_mark.append(node)
		if node in self.to_install:
			self.to_install.remove(node)
		self.to_install.append(node)

	def depth_first_search(self, to_install):
		len_to_install = len(to_install)
		self.to_install = []
		self.perm_mark = []
		self.temp_mark = []
		self.depth = 0

		while len(self.perm_mark) != len_to_install:
			for pack in to_install:
				self.depth_first_search_visit(pack)
			self.depth += 1
			print(f"Current depth: {self.depth}")
			if (self.depth > 50):
				break
