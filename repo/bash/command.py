#!/usr/bin/env python3

from dot_mngr import *

class Command(DefaultCommand):
	def __init__(self, package):
		super().__init__(package)

	def configure(self):
		super().configure(True)
		self.apply_patch(
			"https://ftp.gnu.org/gnu/bash/bash-5.2-patches/bash52-022",
			"-p0",
			"bash-5.2.22"
		)
		self.apply_patch(
			"https://ftp.gnu.org/gnu/bash/bash-5.2-patches/bash52-023",
			"-p0",
			"bash-5.2.23"
		)
		self.apply_patch(
			"https://ftp.gnu.org/gnu/bash/bash-5.2-patches/bash52-024",
			"-p0",
			"bash-5.2.24"
		)
		self.apply_patch(
			"https://ftp.gnu.org/gnu/bash/bash-5.2-patches/bash52-025",
			"-p0",
			"bash-5.2.25"
		)
		self.apply_patch(
			"https://ftp.gnu.org/gnu/bash/bash-5.2-patches/bash52-026",
			"-p0",
			"bash-5.2.26"
		)
		proc = self.cmd_run(
			"./configure --prefix=/usr"
			" --without-bash-malloc"
			" --with-installed-readline"
			" --docdir=/usr/share/doc/bash-" + self.package.version
		)

	def compile(self):
		super().compile(True)
		proc = self.cmd_run("make")

	def check(self):
		super().check(True)
		proc = self.cmd_run("make tests")

	def install(self):
		super().install(True)
		proc = self.cmd_run("sudo make install")

	def uninstall(self):
		super().uninstall(True)
		proc = self.cmd_run("sudo make uninstall")
