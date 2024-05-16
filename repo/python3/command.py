#!/usr/bin/env python3

from dot_mngr import *

def configure(self):
	self.cmd_run(
		f"./configure --prefix={PREFIX}"
		 " --enable-shared"
		 " --with-system-expat"
		 " --enable-optimizations"
		f" --docdir={PREFIX}/share/doc/{self.name}-{self.version}"
	)

def compile(self):
	self.cmd_run("make")

def check(self):
	self.cmd_run("make check")

def install(self):
	self.cmd_run("sudo make install")

def uninstall(self):
	self.cmd_run("sudo make uninstall")
