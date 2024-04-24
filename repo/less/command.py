#!/usr/bin/env python3

from dot_mngr import *

def configure(self):
	self.cmd_run("echo | gcc -xc -E -v -")
	self.cmd_run(
		f"env CPPFLAGS=-I{CNF_PREFIX}/include ./configure --prefix={CNF_PREFIX}"
		f" --docdir={CNF_PREFIX}/share/doc/{self.name}-{self.version}"
		f" --sysconfdir={CNF_PREFIX}/etc"
	)

def compile(self):
	self.cmd_run("make")

def check(self):
	self.cmd_run("make check")

def install(self):
	self.cmd_run("sudo make install")

def uninstall(self):
	self.cmd_run("sudo make uninstall")
