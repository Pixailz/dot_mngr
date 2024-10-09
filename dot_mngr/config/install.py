from dot_mngr import sys

from dot_mngr import p
from dot_mngr import copy
from dot_mngr import get_real_name
from dot_mngr import pprint

class ConfigInstall(object):
	def	install_package(self):
		to_install = copy.deepcopy(getattr(self.parsing.args, "inst_package", None))

		if not to_install:
			p.fail("No package to install")

		for pack in self.parsing.args.inst_package:
			if not self.is_in_packages(pack):
				p.fail(f"Package {pack} not found")

		self.depth_first_search(to_install)

		print(len(self.to_install))
		pprint(self.to_install)

		for pack in self.to_install:
			_pack = self.get_package(pack)
			print(_pack.real_name)
			if _pack is None:
				p.fail(f"Fatal error: {pack}")
			_pack.cmd["suite"]()