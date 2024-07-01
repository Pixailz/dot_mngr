from dot_mngr import os
from dot_mngr import tar
from dot_mngr import shutil
from dot_mngr import importlib
from dot_mngr import selectors
from dot_mngr import subprocess

from dot_mngr import FILE_META, FILE_COMMAND, DIR_CACHE, DIR_LOG
from dot_mngr import DRY_RUN

from dot_mngr import p, r, Os, Json
from dot_mngr import a_cmd
from dot_mngr import scrap
from dot_mngr import url_handler
from dot_mngr import default_configure
from dot_mngr import default_compile
from dot_mngr import default_check
from dot_mngr import default_install
from dot_mngr import default_uninstall
from dot_mngr import default_suite

class Package():
	def __init__(self, name, dir_repo):
		self.name = name
		self.dir_repo = dir_repo
		self.d_base = os.path.join(self.dir_repo, self.name)
		self.f_meta = os.path.join(self.d_base, FILE_META)
		self.f_command = os.path.join(self.d_base, FILE_COMMAND)

		self.prepared = False
		self.log_out = os.path.join(DIR_LOG, f"{self.name}.out.log")
		self.log_err = os.path.join(DIR_LOG, f"{self.name}.err.log")
		self.f_log_out = None
		self.f_log_err = None

		self.load_meta()
		self.load_commands()

	def __del__(self):
		if self.f_log_out and not self.f_log_out.closed:
			self.f_log_out.close()
		if self.f_log_err and not self.f_log_err.closed:
			self.f_log_err.close()

	def load_meta(self):
		meta = Json.load(self.f_meta)
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

	def load_command(self, cmd_name: str, default_cmd: callable):
		cmd = getattr(self.tmp_cmd, cmd_name, None)
		if cmd:
			self.cmd[cmd_name] = a_cmd(self, cmd, cmd_name)
		else:
			self.cmd[cmd_name] = a_cmd(self, default_cmd)

	def load_commands(self):
		self.cmd = dict()
		self.tmp_cmd = None
		if os.path.exists(self.f_command):
			spec = importlib.util.spec_from_file_location("command", self.f_command)
			self.tmp_cmd = importlib.util.module_from_spec(spec)
			spec.loader.exec_module(self.tmp_cmd)

		self.load_command("configure",	default_configure)
		self.load_command("compile", 	default_compile)
		self.load_command("check",		default_check)
		self.load_command("install",	default_install)
		self.load_command("uninstall",	default_uninstall)
		self.load_command("suite",		default_suite)

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
		have_dir = True
		if len(ftar_names) > 0:
			match = r.tar_dir.match(ftar_names[0])
			if match:
				ftar_name = match.group(1)
			else:
				ftar_name = ftar_names[0]
			if ftar.getmember(ftar_name).isdir():
				self.tar_folder = os.path.join(DIR_CACHE, ftar_name)
			else:
				self.tar_folder = os.path.join(DIR_CACHE, self.name)
				have_dir = False

			if os.path.exists(self.tar_folder):
				shutil.rmtree(self.tar_folder)
				p.warn("Removing old tar folder")

		p.info(f"Extracting {self.name}")
		if have_dir:
			ftar.extractall(DIR_CACHE)
		else:
			ftar.extractall(self.tar_folder)
		p.success(f"Extracted {self.name}")

	def prepare_tarball(self):
		if DRY_RUN:
			self.tar_folder = os.path.join(DIR_CACHE, self.name)
			Os.mkdir(self.tar_folder)
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

		# if self.dependencies:
		# 	p.title(f"  - Dependencies:")
		# 	if self.dependencies.get("required"):
		# 		p.info(f"    - Required:")
		# 		for i in self.dependencies["required"]:
		# 			p.info(f"      - {i}")
		# 	if self.dependencies.get("optional"):
		# 		p.info(f"    - Optional:")
		# 		for i in self.dependencies["optional"]:
		# 			p.info(f"      - {i}")
		# 	print()

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
		Json.dump({
			"value": self.value,
			"type": self.type,
			"prefix": self.prefix,
			"suffix": self.suffix,
			"link": self.link,
			"version": self.version,
			"files": self.files,
			"dependencies": self.dependencies
		}, self.f_meta)

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
			env=Os.get_env(),
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
