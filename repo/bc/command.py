#!/usr/bin/env python3

from dot_mngr import *

class Command(DefaultCommand):
	def __init__(self, package):
		super().__init__(package)

	def configure(self):
		super().configure()
		p.info(f"Configuring {self.package.name} {self.package.version}")

	def compile(self):
		super().configure()
		p.info(f"Compiling {self.package.name} {self.package.version}")
