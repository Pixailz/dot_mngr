#!/usr/bin/env python3

from dot_mngr import *

class Command(DefaultCommand):
	def __init__(self, package):
		super().__init__(package)

	def configure(self):
		super().configure(True)
		proc = self.cmd_run(
			"./configure --prefix=/usr"
			" --disable-static"
			" --docdir=/usr/share/doc/acl-" + self.package.version
		)

	def check(self):
		super().check(True)
		proc = self.cmd_run("make check")

	def compile(self):
		super().compile(True)
		proc = self.cmd_run("make")

	def install(self):
		super().install(True)
		proc = self.cmd_run("sudo make install")

	def uninstall(self):
		super().uninstall(True)
		proc = self.cmd_run("sudo make uninstall")
