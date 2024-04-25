#!/usr/bin/env python3

from dot_mngr import *

def configure(self):
	take(os.path.join(self.tar_folder, "build"))
	self.cmd_run(
		f"../configure --prefix={PREFIX}"
		 " --enable-gold"
		 " --enable-ld=default"
		 " --enable-plugins"
		 " --enable-shared"
		 " --disable-werror"
		 " --enable-64-bit-bfd"
		 " --with-system-zlib"
		 " --enable-default-hash-style=gnu"
	)

def compile(self):
	self.cmd_run("make tooldir=" + PREFIX)

def check(self):
	self.cmd_run("make -k check")

def install(self):
	self.cmd_run(
		f"sudo make install tooldir={PREFIX} && "
		f"rm -fv {PREFIX}/lib/lib"
		"{bfd,ctf,ctf-nobfd,gprofng,opcodes,sframe}.a"
	)

def uninstall(self):
	self.cmd_run(f"sudo make uninstall tooldir={PREFIX}")
