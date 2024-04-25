#!/usr/bin/env python3

from dot_mngr import *

def configure(self):
	self.cmd_run(
		f"./configure --prefix={PREFIX}"
		f" --docdir={PREFIX}/share/doc/{self.name}-{self.version}"
		 " --disable-static"
	)

def compile(self):
	self.cmd_run("make")

def check(self):
	self.cmd_run("make check")

def install(self):
	self.cmd_run(f"sudo make docdir={PREFIX}/share/doc/{self.name}-{self.version} install ")

def uninstall(self):
	self.cmd_run("sudo make uninstall")
