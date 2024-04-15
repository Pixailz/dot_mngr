from dot_mngr import *

def a_method(func):
	def wrapper(self, is_implemented = False):
		if not self.prepared:
			self.prepare()
		func(self, is_implemented)
	return wrapper

class DefaultCommand():
	def __init__(self, package):
		self.package = package
		self.log_out = os.path.join(DIR_LOG, f"{self.package.name}.out.log")
		self.log_err = os.path.join(DIR_LOG, f"{self.package.name}.err.log")
		self.prepared = False

	def suite(self):
		self.configure()
		self.compile()
		if DO_CHECK:
			self.check()
		self.install()
		shutil.rmtree(self.package.tar_folder)

	def prepare(self):
		from dot_mngr import conf

		if not os.path.exists(self.package.file_path):
			self.package.get_file()
		if tar.is_tarfile(self.package.file_path):
			self.prepare_tarball()
		self.conf = conf
		self.f_log_out = open(self.log_out, "ab")
		self.f_log_err = open(self.log_err, "ab")
		self.prepared = True

	def prepare_tarball(self):
		ftar = tar.open(self.package.file_path, "r")
		ftar_names = ftar.getnames()
		if len(ftar_names) > 0:
			self.package.tar_folder = os.path.join(DIR_CACHE, ftar_names[0])
			if os.path.exists(self.package.tar_folder):
				shutil.rmtree(self.package.tar_folder)
				p.warn("Removing old tar folder")
		ftar.extractall(DIR_CACHE)

	def cmd_run(self, cmd : str):
		def p_out(stream):
			out = stream.readline()
			if out:
				self.f_log_out.write(out)
				p.cmd(out.decode("utf-8").strip("\n"))

		def p_err(stream):
			err = stream.readline()
			if err:
				self.f_log_err.write(err)
				p.warn(err.decode("utf-8").strip("\n"))

		proc = subprocess.Popen(cmd,
			stdout=subprocess.PIPE,
			stderr=subprocess.PIPE,
			shell=True,
			close_fds=True,
			cwd=self.package.tar_folder,
		)

		sel = selectors.DefaultSelector()
		sel.register(proc.stdout, selectors.EVENT_READ, p_out)
		sel.register(proc.stderr, selectors.EVENT_READ, p_err)

		while proc.poll() is None:
			events = sel.select()
			for key, mask in events:
				callback = key.data
				callback(key.fileobj)

		retv = proc.wait()
		sel.close()

		if retv != 0:
			p.fail(f"Command failed:\n[{cmd}]({retv})")

		return retv

	@a_method
	def configure(self, is_implemented):
		if is_implemented:
			p.info(f"Configuring {self.package.name} {self.package.version}")
		else:
			p.warn(f"Configure command not found for {self.package.name}")

	@a_method
	def compile(self, is_implemented):
		if is_implemented:
			p.info(f"Compiling {self.package.name} {self.package.version}")
		else:
			p.warn(f"Compile command not found for {self.package.name}")

	@a_method
	def check(self, is_implemented):
		if is_implemented:
			p.info(f"Checking {self.package.name} {self.package.version}")
		else:
			p.warn(f"Check command not found for {self.package.name}")

	@a_method
	def install(self, is_implemented):
		if is_implemented:
			p.info(f"Installing {self.package.name} {self.package.version}")
		else:
			p.warn(f"Install command not found for {self.package.name}")

	@a_method
	def uninstall(self, is_implemented):
		if is_implemented:
			p.info(f"Uninstalling {self.package.name} {self.package.version}")
		else:
			p.warn(f"Uninstall command not found for {self.package.name}")
