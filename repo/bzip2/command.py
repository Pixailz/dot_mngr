#!/usr/bin/env python3

from dot_mngr import *

def configure(self):
	self.dapply_patch("https://www.linuxfromscratch.org/patches/lfs/12.1/bzip2-1.0.8-install_docs-1.patch",
		"-Np1","patch_bzip2-documentation"
	)
	self.cmd_run(
		"sed -i 's@\\(ln -s -f \\)\\$(PREFIX)/bin/@\\1@' Makefile && "
		"sed -i 's@(PREFIX)/man@(PREFIX)/share/man@g' Makefile && "
		"make -f Makefile-libbz2_so && make clean"
	)

def compile(self):
	self.cmd_run("make")

def check(self):
	self.cmd_run("make check")

def install(self):
	self.cmd_run(
		f"sudo make PREFIX={PREFIX} install && "
		f"sudo cp -av libbz2.so.* {PREFIX}/lib && "
		f"sudo ln -fsv libbz2.so.${self.version} {PREFIX}/lib/libbz2.so && "
	 	f"sudo cp -v bzip2-shared {PREFIX}/bin/bzip2 && "
		f"for i in {PREFIX}/bin/""{bzcat,bunzip2}; do sudo ln -sfv bzip2 $i; done && "
		f"sudo rm -fv {PREFIX}/lib/libbz2.a"
	)

def uninstall(self):
	self.cmd_run("sudo make uninstall")
