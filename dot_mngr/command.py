from dot_mngr import os
from dot_mngr import shutil

import dot_mngr as dm

from dot_mngr import p

def default_configure(self):
	p.warn(f"Configure command not found for {self.name}")

def default_compile(self):
	p.warn(f"Compile command not found for {self.name}")

def default_check(self):
	p.warn(f"Check command not found for {self.name}")

def default_install(self):
	p.warn(f"Install command not found for {self.name}")

def default_uninstall(self):
	p.warn(f"Uninstall command not found for {self.name}")

def default_suite(self):
	if not os.path.exists("configure") and os.path.exists("autogen.sh"):
		self.cmd_run("sh autogen.sh")

	self.cmd["configure"]()
	configure_kernel = self.cmd.get("configure_kernel", None)
	if configure_kernel is not None:
		configure_kernel()
	do_compile = configure_kernel is None or self.name == "linux-compile"

	if do_compile:
		self.cmd["compile"]()

	if dm.DO_CHECK:
		self.cmd["check"]()

	if do_compile:
		self.cmd["install"]()
	else:
		self.cmd_run(f"cp -fv .config /boot/config-{self.version}")

	if self.chrooted:
		self.unchroot()

	os.chdir(self.oldpwd)
	shutil.rmtree(self.tar_folder)

def a_cmd(self, func, title = None):
	def wrapper():
		if title and not dm.DRY_RUN:
			p.info(f"Running {title} for {self.name}-{self.version}")
		if not self.prepared:
			self.prepare()
		func(self)
	return wrapper
