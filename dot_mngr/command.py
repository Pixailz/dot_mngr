from dot_mngr import os
from dot_mngr import sys
from dot_mngr import shutil

from dot_mngr import DO_CHECK, DRY_RUN

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
	self.cmd["configure"]()
	self.cmd["compile"]()
	if DO_CHECK:
		self.cmd["check"]()
	self.cmd["install"]()

	os.chdir(self.oldpwd)
	shutil.rmtree(self.tar_folder)

def a_cmd(self, func, title = None):
	def wrapper():
		if title and not DRY_RUN:
			p.info(f"Running {title} for {self.name}-{self.version}")
		if not self.prepared:
			self.prepare()
		func(self)
	return wrapper
