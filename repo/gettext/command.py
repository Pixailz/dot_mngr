#!/usr/bin/env python3

from dot_mngr import p, DefaultCommand

class Command(DefaultCommand):
	def __init__(self, package):
		super().__init__(package)
