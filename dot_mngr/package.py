from dot_mngr import *

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

def get_dependencies(pack):
	from dot_mngr import conf

	to_install = list()
	package = conf.packages[pack]

	if package.dependencies:
		if package.dependencies.get("required"):
			to_install += [ pack for pack in package.dependencies["required"] if pack in conf.packages ]
		# if package.dependencies.get("optional"):
		#	to_install += package.dependencies["optional"]

	return to_install

def is_installed(pack):
	if pack.files == None:
		return False
	for file in pack.files:
		if file[0] == "/":
			file = file[1:]
		print(os.path.join(CNF_PREFIX, file))

		if not os.path.exists(os.path.join(CNF_PREFIX, file)):
			return False
	return True

def install_depencencies(self):
	from dot_mngr import conf

	to_install = list()

	def get_all_dependencies(target):
		to_install = get_dependencies(target.name)
		prev_len = len(to_install)

		while True:
			for pack in to_install:
				to_install += get_dependencies(pack)

			tmp = set(to_install)
			to_install = list(tmp)

			cur_len = len(to_install)
			print(f"{cur_len = }")
			print(f"{prev_len = }")

			if prev_len == cur_len:
				break
			else:
				prev_len = cur_len
		return to_install

	def get_not_installed_dependencies(to_install):
		new_to_install = list()
		for pack in to_install:
			if not is_installed(conf.packages[pack]):
				new_to_install.append(pack)

		return to_install

	to_install = get_all_dependencies(self)
	to_install = get_not_installed_dependencies(to_install)

	pprint(to_install)

	# for i in to_install:
	# 	if not self.conf.packages.get(i):
	# 		p.warn(f"Dependency {i} not found")
	# 		continue

	# 	self.conf.packages[i].cmd["suite"]()

def default_suite(self):
	install_depencencies(self)

	self.cmd["configure"]()
	self.cmd["compile"]()
	if DO_CHECK:
		self.cmd["check"]()
	self.cmd["install"]()

	os.chdir(self.oldpwd)
	shutil.rmtree(self.tar_folder)

def a_cmd(self, func, title = None):
	def wrapper():
		if title:
			p.info(f"Running {title} for {self.name}-{self.version}")
		if not self.prepared:
			self.prepare()
		func(self)
	return wrapper

class Package():
	def __init__(self, name):
		self.name = name
		self.d_base = os.path.join(DIR_REPO, self.name)
		self.f_meta = os.path.join(self.d_base, FILE_META)
		self.f_command = os.path.join(self.d_base, FILE_COMMAND)

		self.prepared = False
		self.log_out = os.path.join(DIR_LOG, f"{self.name}.out.log")
		self.log_err = os.path.join(DIR_LOG, f"{self.name}.err.log")
		self.f_log_out = None
		self.f_log_err = None

		self.load_meta()
		self.load_command()

	def __del__(self):
		if self.f_log_out and not self.f_log_out.closed:
			self.f_log_out.close()
		if self.f_log_err and not self.f_log_err.closed:
			self.f_log_err.close()

	def load_meta(self):
		meta = json_load(self.f_meta)
		if not meta:
			return None
		self.value = meta.get("value")
		self.type = meta.get("type")
		self.prefix = meta.get("prefix")
		self.suffix = meta.get("suffix")
		self.link = meta.get("link")
		self.version = meta.get("version")
		self.files = meta.get("files")
		self.dependencies = meta.get("dependencies")
		self.file_name = f"{self.name}-{self.version}{self.suffix}"
		self.file_path = os.path.join(DIR_CACHE, self.file_name)
		self.repo_status = None

	def load_command(self):
		self.cmd = dict()
		tmp_cmd = None
		if os.path.exists(self.f_command):
			spec = importlib.util.spec_from_file_location("command", self.f_command)
			tmp_cmd = importlib.util.module_from_spec(spec)
			spec.loader.exec_module(tmp_cmd)

		if getattr(tmp_cmd, "configure", None):
			self.cmd["configure"] = a_cmd(self, tmp_cmd.configure, "configure")
		else:
			self.cmd["configure"] = a_cmd(self, default_configure)

		if getattr(tmp_cmd, "compile", None):
			self.cmd["compile"] = a_cmd(self, tmp_cmd.compile, "compile")
		else:
			self.cmd["compile"] = a_cmd(self, default_compile)

		if getattr(tmp_cmd, "check", None):
			self.cmd["check"] = a_cmd(self, tmp_cmd.check, "check")
		else:
			self.cmd["check"] = a_cmd(self, default_check)

		if getattr(tmp_cmd, "install", None):
			self.cmd["install"] = a_cmd(self, tmp_cmd.install, "install")
		else:
			self.cmd["install"] = a_cmd(self, default_install)

		if getattr(tmp_cmd, "uninstall", None):
			self.cmd["uninstall"] = a_cmd(self, tmp_cmd.uninstall, "uninstall")
		else:
			self.cmd["uninstall"] = a_cmd(self, default_uninstall)

		if getattr(tmp_cmd, "suite", None):
			self.cmd["suite"] = a_cmd(self, tmp_cmd.suite, "suite")
		else:
			self.cmd["suite"] = a_cmd(self, default_suite)

	def prepare(self):
		from dot_mngr import conf

		if not os.path.exists(self.file_path):
			self.get_file()
		if tar.is_tarfile(self.file_path):
			self.prepare_tarball()
		self.conf = conf

		self.f_log_out = open(self.log_out, "ab")
		self.f_log_err = open(self.log_err, "ab")

		cwd = os.getcwd()
		if cwd != self.tar_folder:
			self.oldpwd = cwd
			os.chdir(self.tar_folder)

		self.prepared = True

	def prepare_tarball_real(self):
		ftar = tar.open(self.file_path, "r")
		ftar_names = ftar.getnames()
		if len(ftar_names) > 0:
			match = r.tar_dir.match(ftar_names[0])
			if match:
				ftar_name = match.group(1)
			else:
				ftar_name = ftar_names[0]
			self.tar_folder = os.path.join(DIR_CACHE, ftar_name)
			if os.path.exists(self.tar_folder):
				shutil.rmtree(self.tar_folder)
				p.warn("Removing old tar folder")
		p.info(f"Extracting {self.name}")
		ftar.extractall(DIR_CACHE)
		p.success(f"Extracted {self.name}")

	def prepare_tarball(self):
		if DRY_RUN:
			self.tar_folder = os.path.join(DIR_CACHE, self.name)
			mkdir(self.tar_folder)
			p.dr(f"Creating {self.tar_folder}")
		else:
			self.prepare_tarball_real()

	@staticmethod
	def info_col(
			name,
			status,
			version = "None",
			link = "None"
		):
		return p.col([
			(name, 20),
			(version, 15),
			(status, 15),
			(link, 30),
		])

	@staticmethod
	def hdr_info():
		p.title(Package.info_col("Name","Status", "Version", "Link") + "\n")

	def info(self):
		pfunc = p.info
		status = "Untouched"
		if self.repo_status == 0:
			status = "Failed"
			pfunc = p.fail
		elif self.repo_status == 1:
			status = "Updated"
		elif self.repo_status == 2:
			status = "Up-to-date"

		pfunc(Package.info_col(self.name, status, self.version, self.link))

		if self.dependencies:
			p.title(f"  - Dependencies:")
			if self.dependencies.get("required"):
				p.info(f"    - Required:")
				for i in self.dependencies["required"]:
					p.info(f"      - {i}")
			if self.dependencies.get("optional"):
				p.info(f"    - Optional:")
				for i in self.dependencies["optional"]:
					p.info(f"      - {i}")
			print()

	def save_update(self):
		if self.new_link == None:
			self.repo_status = 0
			return
		elif self.new_link != self.link:
			self.repo_status = 1
		else:
			self.repo_status = 2

		self.link = self.new_link
		self.version = self.new_version if self.new_version else self.version
		self.file_name = f"{self.name}-{self.version}{self.suffix}"
		self.file_path = os.path.join(DIR_CACHE, self.file_name)
		with open(self.f_meta, "w") as f:
			json.dump({
				"value": self.value,
				"type": self.type,
				"prefix": self.prefix,
				"suffix": self.suffix,
				"link": self.link,
				"version": self.version,
				"dependencies": self.dependencies
			}, f, indent=4)

	def update(self):
		self.new_link, self.new_version = scrap.latest_link(self)
		self.save_update()
		self.info()

	def get_file(self):
		if not os.path.exists(self.file_path):
			if not url_handler.download_package(self):
				return False
			else:
				return True
		p.success(f"{self.file_name} already exists")
		return True

	def cmd_run_real(self, cmd):
		def p_out(stream):
			out = stream.readline()
			if out:
				self.f_log_out.write(out)
				try:
					p.cmdo(out.decode("utf-8").strip("\n"))
				except UnicodeDecodeError as e:
					p.warn("Cannot decode output")

		def p_err(stream):
			err = stream.readline()
			if err:
				self.f_log_err.write(err)
				try:
					p.cmde(err.decode("utf-8").strip("\n"))
				except UnicodeDecodeError as e:
					p.warn("Cannot decode output")

		proc = subprocess.Popen(cmd,
			stdout=subprocess.PIPE,
			stderr=subprocess.PIPE,
			shell=True,
			close_fds=True,
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

	def cmd_run(self, cmd : str):
		if DRY_RUN:
			p.dr(cmd)
		else:
			return self.cmd_run_real(cmd)

	def apply_patch(self, opt, path):
		self.cmd_run(f"patch {opt} -i {path}")

	def dapply_patch(self, url, opt, name):
		url_handler.download_file(url, self.tar_folder + name)
		self.apply_patch(opt, self.tar_folder + name)
