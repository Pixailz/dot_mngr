#!/usr/bin/env python3

from dot_mngr import *

def configure(self):
	self.cmd_run(
		f"./configure --prefix={PREFIX}"
		f" --mandir={PREFIX}/share/man"
		 " --with-shared"
		 " --without-debug"
		 " --without-normal"
		 " --with-cxx-shared"
		 " --enable-pc-files"
		 " --enable-widec"
		f" --with-pkg-config-libdir={PREFIX}/lib/pkgconfig"
	)

def compile(self):
	self.cmd_run("make")

def check(self):
	self.cmd_run("make check")

def install(self):
	self.cmd_run(
		 "sudo make install && "
		 "make distclean && "
		f"./configure --prefix={PREFIX}"
		 " --with-shared"
		 " --without-normal"
		 " --without-debug"
		 " --without-cxx-binding"
		 " --with-abi-version=5"
		f" && make sources libs"
	)

def uninstall(self):
	self.cmd_run("sudo make uninstall")
