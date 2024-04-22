#!/usr/bin/env python3

from dot_mngr import *

def configure(self):
	self.cmd_run(
		f"./configure --prefix={CNF_PREFIX}"
		 " --disable-static"
		f" --docdir={CNF_PREFIX}/share/doc/{self.name}-{self.version}"
	)

def compile(self):
	self.cmd_run("make")

def check(self):
	self.cmd_run("make check")

def install(self):
	self.cmd_run(
		"sudo make install && "
		f"sudo chmod -v 0755 {CNF_PREFIX}/lib/preloadable_libintl.so"
	)

def uninstall(self):
	self.cmd_run("sudo make uninstall")
