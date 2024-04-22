#!/usr/bin/env python3

from dot_mngr import *

def configure(self):
	self.cmd_run(
		f"./configure --prefix={CNF_PREFIX}"
		f" --docdir={CNF_PREFIX}/share/doc/{self.name}-{self.version}"
		" --disable-static"
	)

def compile(self):
	self.cmd_run("make")

def check(self):
	self.cmd_run("make check")

def install(self):
	self.cmd_run(
		 "sudo make install && "
		f"sudo ln -sfv flex {CNF_PREFIX}/bin/lex && "
		f"sudo ln -sfv flex.1 {CNF_PREFIX}/share/man/man1/lex.1"
	)

def uninstall(self):
	self.cmd_run("sudo make uninstall")
