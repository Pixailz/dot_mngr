#!/usr/bin/env python3

from dot_mngr import *

def configure(self):
	self.cmd_run(f"./configure --prefix={PREFIX}")

def compile(self):
	self.cmd_run("make")

def check(self):
	self.cmd_run("make check")

def install(self):
	self.cmd_run(
		 "sudo make install && "
		f"sudo make TEXMF={PREFIX}/share/texmf install-tex"
	)

def uninstall(self):
	self.cmd_run("sudo make uninstall")
