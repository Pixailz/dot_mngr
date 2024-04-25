#!/usr/bin/env python3

from dot_mngr import *

def configure(self):
	self.dapply_patch("https://www.linuxfromscratch.org/patches/lfs/12.1/coreutils-9.4-i18n-1.patch",
		"-fNp1","patch_coreutils-intl"
	)
	self.cmd_run(
		 "sed -e '/n_out += n_hold/,+4 s|.*bufsize.*|//&|' -i src/split.c && "
		 "autoreconf -fiv && "
		 "FORCE_UNSAFE_CONFIGURE=1 ./configure"
		f" --prefix={PREFIX}"
		f" --enable-no-install-program=kill,uptime"
	)

def compile(self):
	self.cmd_run("make")

def install(self):
	self.cmd_run("sudo make install")

def uninstall(self):
	self.cmd_run("sudo make uninstall")
