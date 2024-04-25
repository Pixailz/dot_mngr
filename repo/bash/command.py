#!/usr/bin/env python3

from dot_mngr import *

def configure(self):
	self.apply_patch("-p0",
		os.path.join(self.d_base, "bash52-upstream-022_026.patch"))
	self.cmd_run(
		f"./configure --prefix={PREFIX}"
		f" --docdir={PREFIX}/share/doc/{self.name}-{self.version}"
		 " --without-bash-malloc"
		 " --with-installed-readline"
	)

def compile(self):
	self.cmd_run("make")

def check(self):
	self.cmd_run("make tests")

def install(self):
	self.cmd_run("sudo make install")

def uninstall(self):
	self.cmd_run("sudo make uninstall")
