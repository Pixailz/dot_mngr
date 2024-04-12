from dot_mngr import p

class DefaultCommand():
	def __init__(self, package):
		self.package = package

	def configure(self):
		p.warn(f"Configure command not found for {self.package.name}")

	def compile(self):
		p.warn(f"Compile command not found for {self.package.name}")

	def check(self):
		p.warn(f"Check command not found for {self.package.name}")

	def install(self):
		p.warn(f"Install command not found for {self.package.name}")
